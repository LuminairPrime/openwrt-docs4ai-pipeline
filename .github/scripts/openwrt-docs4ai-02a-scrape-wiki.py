"""
Purpose: Scrape OpenWrt wiki pages to pure markdown format (L1 target).
Phase: Extraction
Layers: L0 -> L1
Inputs: https://openwrt.org/docs/
Outputs: tmp/L1-raw/wiki/*.md and tmp/L1-raw/wiki/*.meta.json
Environment Variables: WORKDIR, SKIP_WIKI, WIKI_MAX_PAGES
Dependencies: requests, pandoc (system binary), lib.config, lib.extractor
Notes: Enforces 1.5s delay to prevent bot rate-limits. Uses cache logic.
"""

import os
import re
import time
import datetime
import subprocess
import sys
import json
from collections import defaultdict

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config, extractor

sys.stdout.reconfigure(line_buffering=True)

try:
    import requests
except ImportError:
    print("[02a] FAIL: 'requests' package not installed")
    sys.exit(1)

if config.SKIP_WIKI:
    print("[02a] SKIP: Wiki scraping disabled (SKIP_WIKI=true)")
    sys.exit(0)

print("[02a] Scrape OpenWrt wiki (crawl namespace indexes, last 2 years)")

DELAY = 1.5
CUTOFF = datetime.datetime.now(datetime.UTC).replace(tzinfo=None) - datetime.timedelta(days=730)
RUN_START = time.perf_counter()
TIMINGS = defaultdict(float)
COUNTS = defaultdict(int)
HEAD_DISCOVERY_LIMIT = 5

# Namespaces to crawl.
NAMESPACES = [
    ("/docs/techref/", "docs%3Atechref"),
    ("/docs/guide-developer/", "docs%3Aguide-developer"),
    ("/docs/guide-user/base-system/uci/", "docs%3Aguide-user%3Abase-system%3Auci"),
]

# Explicit pages that MUST be scraped regardless of age or index presence.
MANDATORY_PAGES = [
    "/docs/techref/ubus",
]

SKIP_PATTERNS = [
    "/toh/", "/inbox/", "/meta/", "/playground/", "changelog", "release_notes"
]

session = requests.Session()

CACHE_DIR = os.path.join(config.WORKDIR, ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, "wiki-lastmod.json")

def log_phase_start(name, detail=""):
    suffix = f" | {detail}" if detail else ""
    print(f"[02a][TIMER] START {name}{suffix}")
    return time.perf_counter()

def log_phase_end(name, started_at, detail=""):
    elapsed = time.perf_counter() - started_at
    TIMINGS[name] += elapsed
    COUNTS[name] += 1
    suffix = f" | {detail}" if detail else ""
    print(f"[02a][TIMER] END   {name} | {elapsed:.3f}s{suffix}")
    return elapsed

def timed_sleep(seconds, reason):
    started_at = log_phase_start("sleep", reason)
    time.sleep(seconds)
    log_phase_end("sleep", started_at, reason)

def load_cache():
    started_at = log_phase_start("load_cache", CACHE_FILE)
    if not os.path.isfile(CACHE_FILE):
        log_phase_end("load_cache", started_at, "cache-miss")
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = data if isinstance(data, dict) else {}
        log_phase_end("load_cache", started_at, f"entries={len(result)}")
        return result
    except (json.JSONDecodeError, ValueError):
        log_phase_end("load_cache", started_at, "invalid-json")
        return {}
    except Exception:
        log_phase_end("load_cache", started_at, "read-error")
        return {}

    log_phase_end("load_cache", started_at, "fallback-empty")
    return {}

def save_cache(cache):
    started_at = log_phase_start("save_cache", f"entries={len(cache)}")
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f)
    log_phase_end("save_cache", started_at, f"entries={len(cache)}")

def path_to_filename(url_path):
    parts = url_path.strip("/").split("/")
    if parts and parts[0] == "docs":
        parts = parts[1:]
    if parts and parts[-1] == "start":
        parts = parts[:-1]
    slug = "-".join(p for p in parts if p)
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug if slug else "misc"

def fetch_page_lastmod(url):
    started_at = log_phase_start("head_lastmod", url)
    try:
        r = session.head(url, timeout=15, allow_redirects=True)
        lm = r.headers.get("Last-Modified")
        if lm:
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(lm)
                value = datetime.datetime(dt.year, dt.month, dt.day)
                log_phase_end("head_lastmod", started_at, f"last-modified={value.isoformat()}")
                return value
            except Exception:
                pass
    except Exception:
        pass
    log_phase_end("head_lastmod", started_at, "last-modified=unknown")
    return None

cache = load_cache()
discovered_pages = set(MANDATORY_PAGES)
head_lastmod_probe_count = 0
head_lastmod_success_count = 0
head_lastmod_supported = None

for prefix, idx_param in NAMESPACES:
    index_url = f"https://openwrt.org{prefix}start?do=index&idx={idx_param}"
    print(f"[02a] Fetching namespace index: {prefix}")
    timed_sleep(DELAY, f"namespace-index {prefix}")
    fetch_started_at = log_phase_start("namespace_index", prefix)
    try:
        resp = session.get(index_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        log_phase_end("namespace_index", fetch_started_at, f"{prefix} failed")
        print(f"[02a] WARN: Could not fetch index for {prefix}: {e}")
        continue
    log_phase_end("namespace_index", fetch_started_at, f"{prefix} bytes={len(resp.text)}")

    html = resp.text
    parse_started_at = log_phase_start("namespace_parse", prefix)
    for m in re.finditer(r'href="([^"#?]*)"', html):
        href = m.group(1)
        path = None
        if href.startswith("https://openwrt.org"):
            path = href.replace("https://openwrt.org", "")
        elif href.startswith("/docs/"):
            path = href
        else:
            continue

        if not path.startswith(prefix): continue
        if path.rstrip("/").endswith("/start"): continue
        if any(pat in path for pat in SKIP_PATTERNS): continue
        if re.match(r'^/[a-z]{2}(-[a-z]+)?/', path): continue
        if "/_export/" in path or "/_detail/" in path or "/_media/" in path: continue
        discovered_pages.add(path)
    log_phase_end("namespace_parse", parse_started_at, f"{prefix} discovered={len(discovered_pages)}")

if not discovered_pages:
    print("[02a] WARN: No wiki pages discovered.")
    sys.exit(1)

saved = 0
skipped_old = 0
skipped_unchanged = 0
skipped_short = 0 # FIX BUG-032
failed = 0

for path in sorted(discovered_pages):
    page_started_at = log_phase_start("page_total", path)
    if saved >= config.WIKI_MAX_PAGES:
        log_phase_end("page_total", page_started_at, f"{path} stopped-by-cap")
        print(f"[02a] WARN: Reached WIKI_MAX_PAGES={config.WIKI_MAX_PAGES} cap. Stopping.")
        break

    url = f"https://openwrt.org{path}"
    slug = path_to_filename(path)

    # Probe a small sample of HEAD responses first; disable the extra request path
    # for the rest of the run if OpenWrt is not publishing Last-Modified headers.
    if head_lastmod_supported is not False:
        head_lastmod_probe_count += 1
        last_mod = fetch_page_lastmod(url)
        if last_mod is not None:
            head_lastmod_success_count += 1
            head_lastmod_supported = True
        elif head_lastmod_supported is None and head_lastmod_probe_count >= HEAD_DISCOVERY_LIMIT:
            head_lastmod_supported = False
            print(
                f"[02a] INFO: Disabling per-page HEAD last-modified probes after "
                f"{head_lastmod_probe_count} misses."
            )
    else:
        last_mod = None

    if last_mod and last_mod < CUTOFF and path not in MANDATORY_PAGES:
        skipped_old += 1
        log_phase_end("page_total", page_started_at, f"{path} skipped-old")
        continue

    last_mod_str = last_mod.isoformat() if last_mod else "unknown"
    if cache.get(url) == last_mod_str and last_mod_str != "unknown":
        fpath = os.path.join(config.L1_RAW_WORKDIR, "wiki", f"wiki_page-{slug}.md")
        if os.path.exists(fpath):
            skipped_unchanged += 1
            log_phase_end("page_total", page_started_at, f"{path} skipped-unchanged")
            continue

    timed_sleep(DELAY, f"raw-export {path}")
    raw_url = f"{url}?do=export_raw"
    raw_fetch_started_at = log_phase_start("raw_fetch", path)
    try:
        r = session.get(raw_url, timeout=20)
        r.raise_for_status()
        raw_content = r.text
    except Exception as e:
        log_phase_end("raw_fetch", raw_fetch_started_at, f"{path} failed")
        print(f"[02a] FAIL: {path} ({e})")
        failed += 1
        log_phase_end("page_total", page_started_at, f"{path} fetch-failed")
        continue
    log_phase_end("raw_fetch", raw_fetch_started_at, f"{path} bytes={len(raw_content)}")

    # FIX BUG-017: Hardened HTML leak detection
    # Must have structural tags (<!DOCTYPE or <html) AND an error signature
    has_structural = "<!DOCTYPE" in raw_content or "<html" in raw_content
    html_error_signatures = [
        "404 Not Found", "Cloudflare", "Access Denied", 
        "Just a moment...", "Checking your browser", "Service Temporarily Unavailable",
        "Rate limit exceeded", "captcha", "This topic does not exist"
    ]
    has_signature = any(sig in raw_content for sig in html_error_signatures)
    
    if (has_structural and has_signature) or not raw_content.strip():
        print(f"[02a] WARN: HTML error signature or ghost page detected for {path}. Skipping.")
        failed += 1
        log_phase_end("page_total", page_started_at, f"{path} ghost-or-html-error")
        continue

    pandoc_started_at = log_phase_start("pandoc", path)
    try:
        result = subprocess.run(
            ["pandoc", "-f", "dokuwiki", "-t", "gfm", "--wrap=none"],
            input=raw_content, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30
        )
        md = result.stdout or ""
        # FIX BUG-040: Check pandoc return code
        if result.returncode != 0:
            log_phase_end("pandoc", pandoc_started_at, f"{path} exit={result.returncode}")
            print(f"[02a] FAIL: pandoc failed for {path} (Exit {result.returncode})")
            failed += 1
            log_phase_end("page_total", page_started_at, f"{path} pandoc-failed")
            continue
    except Exception as e:
        log_phase_end("pandoc", pandoc_started_at, f"{path} exception")
        print(f"[02a] FAIL: pandoc error for {path} ({e})")
        failed += 1
        log_phase_end("page_total", page_started_at, f"{path} pandoc-exception")
        continue
    log_phase_end("pandoc", pandoc_started_at, f"{path} md-bytes={len(md)}")

    postprocess_started_at = log_phase_start("postprocess", path)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    if len(md) < 200:
        skipped_short += 1 # FIX BUG-032
        log_phase_end("postprocess", postprocess_started_at, f"{path} skipped-short")
        log_phase_end("page_total", page_started_at, f"{path} skipped-short")
        continue

    title_m = re.search(r"^#+ (.+)$", md, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.split("/")[-1]

    md = re.sub(r"^#+ .+\n\n?", "", md, count=1)
    
    final_content = f"# {title}\n\n{md}"
    log_phase_end("postprocess", postprocess_started_at, f"{path} title={title[:40]}")

    metadata = {
        "extractor": "02a-scrape-wiki.py",
        "origin_type": "wiki_page",
        "module": "wiki",
        "slug": slug,
        "original_url": url,
        "language": "text",
        "fetch_status": "success",
        "extraction_timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

    write_started_at = log_phase_start("write_output", path)
    extractor.write_l1_markdown("wiki", "wiki_page", slug, final_content, metadata)
    log_phase_end("write_output", write_started_at, f"{path} content-bytes={len(final_content)}")
    cache[url] = last_mod_str
    
    saved += 1
    log_phase_end("page_total", page_started_at, f"{path} saved slug={slug}")
    print(f"[02a] OK: {slug} [{last_mod_str}] -- {title[:55]}")

save_cache(cache)
run_elapsed = time.perf_counter() - RUN_START
print(f"[02a][TIMER] SUMMARY total-runtime={run_elapsed:.3f}s")
print(
    f"[02a][TIMER] SUMMARY head-lastmod-support: probes={head_lastmod_probe_count} "
    f"hits={head_lastmod_success_count} state={head_lastmod_supported}"
)
for name in sorted(TIMINGS):
    total = TIMINGS[name]
    count = COUNTS[name]
    average = total / count if count else 0.0
    print(f"[02a][TIMER] SUMMARY {name}: count={count} total={total:.3f}s avg={average:.3f}s")
print(f"[02a] Complete: {saved} fetched, {skipped_unchanged} unchanged, {skipped_old} too old, {skipped_short} too short, {failed} failed.")
if saved == 0 and skipped_unchanged == 0:
    print("[02a] FAIL: Zero output files generated. Exiting with error.")
    sys.exit(1)
