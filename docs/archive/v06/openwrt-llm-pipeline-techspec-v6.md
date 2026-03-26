# OpenWrt LLM Documentation Pipeline
# Technical Design Document — v6
# Status: Draft — Pending Review
# Supersedes: v5 (incorporates field-test corrections from first successful v5 run)

---

## 1. Purpose and Scope

This document defines the complete design for an automated GitHub Actions
pipeline that collects, processes, and publishes OpenWrt developer documentation
in formats optimized for LLM consumption (large language models).

The pipeline runs monthly at no cost (GitHub Actions free tier + GitHub Models
free tier), publishes results to a GitHub Pages URL, and produces a file layout
designed for both RAG (retrieval-augmented generation) use cases and direct
context-window injection.

A separate, manually-maintained set of static "rulebook" files is maintained
locally by the user and uploaded to the `static-docs/` folder in the repository.
The pipeline promotes these files to the GitHub Pages root on each run.

**What changed from v5:** This document incorporates corrections discovered
during the first successful v5 workflow run and incorporates the modular
refactoring addendum (Section 12) as a first-class design requirement rather
than an afterthought. Key corrections:
- jsdoc config detection strategy replaced (live-site scraping never worked)
- LuCI upstream jsdoc config must be explicitly skipped (causes stack overflow)
- Two-Pass JSON AST approach replaced with proven per-file invocation
- Step execution order corrected (llms.txt generation before output validation)
- Git identity configuration added to commit step
- Modular script architecture updated per reviewer feedback

---

## 2. High-Level Architecture

### 2.1 Two-Tier Split

**Tier 1 — Automated (GitHub Actions, monthly, $0)**

Handles everything that can be done mechanically and repeatably:
- Cloning upstream source repositories
- Generating API documentation from annotated source code (jsdoc-to-markdown)
- Scraping the OpenWrt wiki using the DokuWiki raw export endpoint
- Extracting curated LuCI application examples (raw, unmodified source files)
- Extracting package metadata from the OpenWrt buildroot source
- Injecting cross-references between all generated files (root-relative links)
- Detecting deprecated symbols and injecting warnings into wiki docs
- Running lightweight AI post-processing via GitHub Models (free tier)
- Assembling single-file merged references for each documentation set
- Publishing everything to GitHub Pages
- Committing generated files back to the repository for version-controlled access

**Tier 2 — Static / manual (local machine, updated rarely)**

Handles content that requires deep judgment and significant AI processing.
Generated locally with a capable model, reviewed manually, and uploaded when
substantially stale:
- `SYSTEM-PROMPT.md` — platform "rules" for injecting into LLM custom instructions
- `concepts-glossary.md` — plain-English definitions of all major OpenWrt concepts
- `openwrt-recipes.md` — curated "how to do X" code patterns with working examples

These files live in `static-docs/` in the repo root. The pipeline copies them
to the GitHub Pages root unchanged on each run. They are not regenerated.

### 2.2 Data Flow

```
upstream repos (GitHub)          openwrt.org wiki         static-docs/ (manual)
        |                               |                          |
        v                               v                          |
  [clone / sparse-checkout]    [sitemap → age filter]              |
        |                               |                          |
        v                               v                          |
  [jsdoc2md per file]          [?do=export_raw + pandoc]           |
        |                               |                          |
        v                               v                          |
  [per-file .md output]        [per-file .md output]               |
        |                               |                          |
        +-------------------+-----------+                          |
                            |                                      |
                            v                                      |
              [Step 8: cross-reference injection]                  |
                            |                                      |
                            v                                      |
              [Step 9: deprecation checker]                        |
                            |                                      |
                            v                                      |
              [Step 10: AI module summaries]                       |
                            |                                      |
                            v                                      |
              [Step 11: assemble single-file references]           |
                            |                                      |
                            v                                      |
              [Step 12: generate root llms.txt]  ←── BEFORE validation
                            |                                      |
                            v                                      |
              [Step 13: validate outputs]        ←── AFTER llms.txt
                            |                                      |
                            +--------------------------------------+
                            |
                            v
              [Step 14: GitHub Pages publish]
              https://[user].github.io/[repo]/
              [Step 15: commit back to repo]
```

---

## 3. Repository Structure

### 3.1 Source layout (this repo, maintained by user)

```
.github/
  workflows/
    generate-llm-docs.yml        ← thin orchestrator (see Section 12)
  scripts/
    requirements.txt             ← Python dependencies
    01-setup-and-clone.sh        ← Steps 0-2: cleanup, clone, env vars
    02-generate-jsdoc.py         ← Steps 3-4: jsdoc2md for ucode and LuCI
    03-scrape-wiki.py            ← Step 5: sitemap fetch, DokuWiki export, pandoc
    04-extract-buildroot.sh      ← Steps 6-7: buildroot Makefiles, LuCI examples
    05-inject-refs.py            ← Steps 8-9: cross-references, deprecation checker
    06-ai-summarize.py           ← Step 10: GitHub Models AI summarization
    07-assemble-publish.sh       ← Steps 11-15: references, llms.txt, validate, deploy

.gitattributes                   ← forces LF line endings on scripts (Section 12.5)

static-docs/                     ← manually maintained, user-uploaded
  SYSTEM-PROMPT.md
  concepts-glossary.md
  openwrt-recipes.md

README.md                        ← describes the project and how to use the outputs
```

### 3.2 Generated output layout (committed to repo + published to Pages)

```
ucode-docs/
  llms.txt
  ucode-tutorial-*.md
  ucode-module-*.md

luci-docs/
  llms.txt
  luci-api-*.md

openwrt-wiki-docs/
  llms.txt
  openwrt-techref-*.md
  openwrt-guide-developer-*.md

openwrt-buildroot-docs/
  llms.txt
  openwrt-buildroot-*.md

openwrt-examples/
  llms.txt
  luci-app-example/              ← raw unmodified .uc and .js files
  luci-app-commands/
  luci-app-ddns/
  luci-app-dockerman/

SYSTEM-PROMPT.md                 ← promoted from static-docs/
concepts-glossary.md
openwrt-recipes.md

ucode-complete-reference.md      ← all ucode content merged
luci-jsapi-complete-reference.md
openwrt-wiki-complete-reference.md
openwrt-buildroot-complete-reference.md
openwrt-examples-complete-reference.md

CHANGES.md                       ← diff of this run vs previous
llms.txt                         ← root index (llmstxt.org standard)
```

### 3.3 Root llms.txt Format

The root `llms.txt` follows the official llms.txt standard (https://llmstxt.org):
an H1 title, a blockquote summary, and H2-sectioned bulleted markdown links in
the format `- [Name](url): Description`. It is generated dynamically from files
that actually exist in the output — not from a hardcoded template — so it
remains accurate when steps are skipped.

---

## 4. Data Sources

### 4.1 ucode Scripting Language

| Property | Value |
|---|---|
| Source repository | https://github.com/jow-/ucode |
| Live documentation | https://ucode.mein.io/ |
| Config detection | Post-clone search inside `repo-ucode/` for `jsdoc/conf.json`, `jsdoc.conf.json`, `.jsdoc.json` (in that order). Use `--configure` only if found. |
| Tutorial source | `docs/tutorial-*.md` — already markdown, copy directly with metadata header prepended |
| API Processing tool | `jsdoc-to-markdown` — **per-file invocation** on `lib/*.js` and `lib/*.c`. Each source file produces one output `.md` file. |
| Output prefix | `ucode-tutorial-` for tutorials, `ucode-module-` for API modules |
| Minimum content threshold | Skip output with fewer than 15 words (filters out empty boilerplate) |

### 4.2 LuCI Client-Side JS API

| Property | Value |
|---|---|
| Source repository | https://github.com/openwrt/luci |
| Live documentation | https://openwrt.github.io/luci/jsapi/ |
| Config detection | **Explicitly skip upstream config.** LuCI's `jsdoc.conf.json` references `clean-jsdoc-theme` and other npm plugins that cause `RangeError: Maximum call stack size exceeded` in `jsdoc2md`'s `anchorName` helper when the plugins are not installed. Run `jsdoc2md` without `--configure`. |
| Source directory | `modules/luci-base/htdocs/luci-static/resources/*.js` (non-recursive; top-level only) |
| API Processing tool | `jsdoc-to-markdown` — **per-file invocation** (same as ucode) |
| Output prefix | `luci-api-` |
| Minimum content threshold | Skip output with fewer than 15 words |

> **v5 field-test finding:** The v5 run discovered that LuCI's upstream
> `jsdoc.conf.json` includes template plugins (`clean-jsdoc-theme`,
> `jaguarjs-jsdoc`) that are only available in the LuCI project's local
> `node_modules/`. When `jsdoc2md` loads this config on the CI runner, the
> missing template triggers an infinite recursion in the `anchorName` helper,
> producing a `Maximum call stack size exceeded` error for every `.js` file.
> The fix is to run `jsdoc2md` without any `--configure` flag for LuCI. This
> produces correct Markdown output because `jsdoc2md` does not need the HTML
> theme configuration — it generates Markdown, not HTML.

### 4.3 OpenWrt Wiki

| Property | Value |
|---|---|
| Source | https://openwrt.org/ |
| Discovery method | Sitemap XML at `https://openwrt.org/sitemap.xml` |
| Age filter | Read `<lastmod>` from sitemap XML; skip pages older than 2 years |
| Export endpoint | Append `?do=export_raw` — returns raw DokuWiki markup |
| Conversion tool | `pandoc -f dokuwiki -t gfm --wrap=none` |
| Crawl scope | Pages under `/docs/techref/` and `/docs/guide-developer/` only |
| Skip patterns | `/toh/`, `/inbox/`, `/meta/`, `/playground/`, `changelog`, `release_notes` |
| Minimum content length | 200 characters after conversion |
| Request delay | 1.5 seconds between HTTP requests |
| On failure | Non-fatal — the workflow continues without wiki output |

### 4.4 OpenWrt Buildroot Source Annotations

| Property | Value |
|---|---|
| Source repository | https://github.com/openwrt/openwrt |
| Clone strategy | `git clone --depth=1 --filter=blob:none --sparse` |
| Sparse checkout paths | `package/network`, `package/kernel`, `package/utils`, `package/system`, `package/libs`, `package/firmware`, `package/boot`, `package/multimedia`, `include`, `scripts` |
| Extracted content | `PKG_DESCRIPTION`, `PKG_VERSION`, `PKG_LICENSE`, `PKG_MAINTAINER`, `PKG_SOURCE_URL` from Makefiles; README files (capped at 2000 chars); header comments from `include/*.mk` |
| Output grouping | One file per top-level package category, plus one file for `include/*.mk` |
| Output prefix | `openwrt-buildroot-` |

### 4.5 Curated LuCI Application Examples

Source location: `applications/` within `repo-luci/`.

Four apps selected, each demonstrating a distinct development pattern:

| App | Pattern | Key concepts |
|---|---|---|
| `luci-app-example` | Hello world / baseline | Minimum viable app structure, ucode↔JS bridge, ACL |
| `luci-app-commands` | HTTP API / controller | Custom endpoints, URL parsing, secure `popen` |
| `luci-app-ddns` | Standard config app | Service state checking, rpcd, deep UCI config |
| `luci-app-dockerman` | Advanced / streaming | UNIX sockets, HTTP streaming, multi-file architecture |

Extraction rules:
- Copy all `.uc` and `.js` files, preserving directory structure
- Do not copy images, Makefiles, translations, or test fixtures
- Leave files completely unmodified — no header injection
- Skip apps with fewer than 3 `.uc`/`.js` files (log warning, don't fail)

### 4.6 GitHub Models AI Summarization

| Property | Value |
|---|---|
| Model identifier | `openai/gpt-4o-mini` (provider prefix required) |
| API endpoint | `https://models.github.ai/inference/chat/completions` |
| Authentication | `$GITHUB_TOKEN` — automatically available in Actions |
| Rate limit | ~150 requests/day |

The old endpoint `https://models.inference.ai.azure.com` is deprecated. The
model name must include the provider prefix `openai/`.

---

## 5. Processing Steps (Workflow Order)

### Step 0: Setup and Cleanup

Install and configure the processing environment:
- Node.js 20 (via `actions/setup-node` with `cache: 'npm'`)
- Python 3.12 (via `actions/setup-python` with `cache: 'pip'`)
- System packages: `pandoc` (via `apt-get`)
- Node packages: `jsdoc-to-markdown` (global via `npm install -g`)
- Python packages: `requests`, `beautifulsoup4`, `lxml`
- Create all output directories
- **Clear stale files** from previous runs to prevent accumulating artifacts
  from renamed or removed upstream pages:

```bash
for d in ucode-docs luci-docs openwrt-wiki-docs openwrt-buildroot-docs openwrt-examples; do
    mkdir -p "$d"
    rm -f "$d"/*.md "$d"/llms.txt
done
rm -f ucode-complete-reference.md luci-jsapi-complete-reference.md
rm -f openwrt-wiki-complete-reference.md openwrt-buildroot-complete-reference.md
rm -f openwrt-examples-complete-reference.md llms.txt CHANGES.md
```

**Ownership:** This cleanup belongs in `01-setup-and-clone.sh` (see Section 12).
It must run *before* any cloning or generation.

### Step 1: jsdoc Config Detection (Post-Clone)

> **v5/v6 change:** v4 attempted to detect jsdoc config by scraping the live
> documentation websites. This never worked — jsdoc does not embed the config
> path in its HTML output. Config detection is now a simple post-clone file
> search inside each cloned repository.

**ucode:** Search `repo-ucode/` for common config filenames in order:
`jsdoc/conf.json`, `jsdoc.conf.json`, `.jsdoc.json`, `.jsdoc.conf.json`.
Use `--configure <path>` if found; proceed without it otherwise.

```python
# In 02-generate-jsdoc.py
UCODE_CONF = None
for candidate in ["jsdoc/conf.json", "jsdoc.conf.json", ".jsdoc.json"]:
    if os.path.isfile(os.path.join("repo-ucode", candidate)):
        UCODE_CONF = candidate
        break
```

**LuCI:** Do **not** search for or use the upstream config. LuCI's
`jsdoc.conf.json` references `clean-jsdoc-theme` and `jaguarjs-jsdoc` template
plugins that crash `jsdoc2md` with `RangeError: Maximum call stack size exceeded`.
Always run without `--configure` for LuCI. See Section 4.2 for full diagnosis.

### Step 2: Clone Upstream Repositories

All `git clone` commands must use `|| { echo "..."; exit 1; }`. Clone failures
are **fatal** because no downstream step can produce output without source repos.

```bash
git clone --depth=1 https://github.com/jow-/ucode.git repo-ucode \
  || { echo "ERROR: Failed to clone ucode repo"; exit 1; }

git clone --depth=1 https://github.com/openwrt/luci.git repo-luci \
  || { echo "ERROR: Failed to clone luci repo"; exit 1; }

git clone --depth=1 --filter=blob:none --sparse \
  https://github.com/openwrt/openwrt.git repo-openwrt \
  || { echo "ERROR: Failed to clone openwrt repo"; exit 1; }

cd repo-openwrt
git sparse-checkout set \
  package/network package/kernel package/utils package/system \
  package/libs package/firmware package/boot package/multimedia \
  include scripts
cd ..
```

Record commit hashes to `$GITHUB_ENV` for traceability in file headers and
the final commit message:
```bash
echo "UCODE_COMMIT=$(git -C repo-ucode rev-parse --short HEAD)" >> "$GITHUB_ENV"
echo "LUCI_COMMIT=$(git -C repo-luci rev-parse --short HEAD)" >> "$GITHUB_ENV"
echo "OPENWRT_COMMIT=$(git -C repo-openwrt rev-parse --short HEAD)" >> "$GITHUB_ENV"
```

### Step 3: Generate ucode Documentation

**Per-file invocation** of `jsdoc2md` on each source file in `lib/*.js` and
`lib/*.c`. This is the proven pattern from the v5 field test — it produced
15 module files with correct content on the first run.

Processing order:
1. **Tutorials:** Loop through `repo-ucode/docs/tutorial-*.md`. These are
   already Markdown. Prepend a metadata header (source URL, live docs link,
   commit hash, timestamp) and copy to `ucode-docs/`.
2. **API Modules:** For each source file, invoke `jsdoc2md` with:
   - `--configure <conf>` if detected in Step 1
   - `--heading-depth 2` (keeps headings from conflicting with the H1 title)
   - `--global-index-format none`
   - Stderr redirected to `jsdoc-ucode.err` (append mode, not overwrite)
   - `|| true` to prevent non-zero exit from killing the loop
3. **15-word minimum filter:** Count words in output. If fewer than 15, skip
   the file silently (boilerplate-only modules).
4. **Output format:** H1 title → blockquote metadata → `---` → jsdoc2md output.
5. **Index generation:** Append each successful file to `ucode-docs/llms.txt`.
6. **Error reporting:** After the loop, if `jsdoc-ucode.err` is non-empty,
   dump its contents to stdout so warnings appear in the Actions log.

```python
# Core loop in 02-generate-jsdoc.py
for src in sorted(glob.glob("repo-ucode/lib/*.js") + glob.glob("repo-ucode/lib/*.c")):
    mod = os.path.splitext(os.path.basename(src))[0]
    
    cmd = ["jsdoc2md", "--heading-depth", "2", "--global-index-format", "none"]
    if ucode_conf:
        cmd.extend(["--configure", ucode_conf])
    cmd.append(src)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stderr:
        with open("jsdoc-ucode.err", "a") as f:
            f.write(f"Stderr for {mod}:\n{result.stderr}\n")
    
    output = result.stdout.strip()
    if len(output.split()) < 15:
        continue
    
    # Write output with metadata header...
```

Do **not** assemble the single-file reference yet — cross-reference injection
(Step 8) must run first.

### Step 4: Generate LuCI JS API Documentation

Same per-file invocation architecture as Step 3, adapted for LuCI:
- **No `--configure` flag** — upstream config crashes jsdoc2md (see Section 4.2)
- Source: `repo-luci/modules/luci-base/htdocs/luci-static/resources/*.js`
- Stderr redirected to `jsdoc-luci.err`
- Live URL convention: top-level `LuCI` class → `LuCI.html`;
  other modules → `LuCI.{mod}.html`
- Generate `luci-docs/llms.txt` index

> **v5 field-test result:** With the upstream config skipped, this step now
> needs to produce output. In the v5 test, `jsdoc2md` *without* `--configure`
> returned empty output for all 17 LuCI files. This is being investigated.
> The most likely cause is that LuCI's JS files use `'require baseclass'`
> string directives that `jsdoc2md` doesn't understand without the config's
> `includePattern`.
>
> **Safety fallback implementation:** `02-generate-jsdoc.py` must include a
> safety net. If the single-file invocation loop returns < 15 words for *all*
> LuCI files, the script must automatically fall back to invoking `jsdoc2md`
> on the whole directory at once (which succeeded in v4), rather than failing
> or producing an empty `luci-docs` folder.

Do **not** assemble single-file references yet.

### Step 5: Scrape OpenWrt Wiki

**Non-fatal step.** All failures must use `exit(0)`, not `exit(1)`. If
openwrt.org is unreachable, the workflow continues and produces all other outputs.

Processing order:
1. Fetch `https://openwrt.org/sitemap.xml`
2. Parse `<loc>` and `<lastmod>` for every `<url>` entry
3. Filter to `/docs/techref/` and `/docs/guide-developer/` paths only
4. Apply skip patterns: `/toh/`, `/inbox/`, `/meta/`, `/playground/`,
   `changelog`, `release_notes`
5. Drop pages with `<lastmod>` older than 2 years
6. **Incremental scraping:** Compare `<lastmod>` with existing file's
   modification time. Skip pages that haven't changed since last run.
7. Fetch `{url}?do=export_raw` for remaining pages
8. Run `pandoc -f dokuwiki -t gfm --wrap=none` on raw response
9. Skip output under 200 characters
10. Prepend metadata block (source URL, lastmod, fetch timestamp)
11. Write `openwrt-wiki-docs/llms.txt`
12. Enforce 1.5-second delay between HTTP requests

### Step 6: Extract OpenWrt Buildroot Documentation

1. Iterate over top-level category directories in `repo-openwrt/package/`
2. Extract Makefile metadata (`PKG_DESCRIPTION`, `PKG_VERSION`, `PKG_LICENSE`,
   `PKG_MAINTAINER`, `PKG_SOURCE_URL`) and README content per package
3. Group by category into one output file per category
4. Extract leading comment blocks from `include/*.mk`
5. Skip packages with no extractable content
6. Cap README at 2000 characters with a source link note if truncated
7. Write `openwrt-buildroot-docs/llms.txt`

Do **not** assemble single-file reference yet.

### Step 7: Extract Curated LuCI Application Examples

For each of the four apps (`luci-app-example`, `luci-app-commands`,
`luci-app-ddns`, `luci-app-dockerman`):
1. Check directory exists; skip with warning if not
2. Count `.uc` and `.js` files; if fewer than 3, log warning and skip
3. Copy with `cp --parents` to preserve directory structure
4. Files are raw and unmodified — no header injection

Generate `openwrt-examples/llms.txt` with a file tree view per app showing
the directory structure and file types (ucode backend vs JS frontend).

Do **not** assemble single-file reference yet.

### Step 8: Cross-Reference Injection (Pure Python, No AI, No Cost)

Runs **before** Step 11 (assembly) so both individual files and the concatenated
complete references contain the cross-reference links.

All injected links use **absolute root-relative paths** (e.g.
`/luci-docs/luci-api-rpc.md`), not relative paths between files. Relative paths
break when individual files are concatenated into the root-level complete
reference documents at a different directory depth.

**Symbol index construction:**
1. Scan all generated `.md` files in `ucode-docs/`, `luci-docs/`,
   `openwrt-wiki-docs/`, `openwrt-buildroot-docs/`
2. For each heading matching a symbol name pattern, record the root-relative URL
3. **Code-like name filter:** Only index symbols matching `camelCase`,
   `dotted.name`, or `underscore_style` patterns. Exclude common English words.
4. **Priority rule:** API reference files (`ucode-docs/`, `luci-docs/`) take
   precedence over wiki and buildroot as the canonical definition source
5. **Collision logging:** When two API reference files define the same symbol,
   log a warning rather than silently overwriting
6. Minimum symbol name length: 4 characters

**Injection algorithm — collect-then-apply-reverse (required pattern):**

Do **not** use offset tracking. The correct approach:

1. Collect all insertion positions into a list: `(start, end, replacement)`
2. Sort the list in **reverse order** by start position
3. Apply insertions from the end of the file backwards

```python
# CORRECT: collect, sort reverse, apply
insertions = []
for symbol, target_url in sorted(symbol_index.items(), key=lambda x: -len(x[0])):
    if target_url == this_root_url:
        continue
    for m in re.finditer(rf'\b({re.escape(symbol)})\b(?!\()', original):
        if not any(i in protected for i in range(m.start(), m.end())):
            insertions.append((m.start(), m.end(), f"[{symbol}]({target_url})"))
            protected.update(range(m.start(), m.end()))

insertions.sort(key=lambda x: x[0], reverse=True)
for start, end, replacement in insertions:
    modified = modified[:start] + replacement + modified[end:]
```

**Protected range tracking:** Before scanning for symbol names, build a set of
character positions inside fenced code blocks, inline code spans, and existing
markdown links `[...]({...})`. The regex for existing markdown links must be
robust (e.g., `\[.*?\]\(.*?\)`) to accurately identify them. Do not inject links
into these ranges. This also provides the **idempotency guard** — if the script
runs twice on the same file, already-injected links are added to the protected
set and skipped, preventing double-wrapping.

All file writes must use `with open()` context managers.

### Step 9: Deprecation Checker (Pure Python, No AI, No Cost)

Use a **1500-character** lookahead window after each symbol heading, not 300.
The `**Deprecated**` marker in jsdoc-to-markdown output may appear after a
description, parameter list, and return value documentation.

When a deprecated symbol is found in a wiki file, inject a GitHub-flavored
markdown `> [!WARNING]` callout after the first `---` separator.

All file writes must use `with open()` context managers.

### Step 10: AI Post-Processing via GitHub Models

**API endpoint and model identifier:**

| Property | Correct value | Deprecated / wrong value |
|---|---|---|
| Endpoint | `https://models.github.ai/inference/chat/completions` | `https://models.inference.ai.azure.com/...` |
| Model name | `openai/gpt-4o-mini` | `gpt-4o-mini` |

**API response validation:** Always use `.get()`:
```python
choices = resp_json.get("choices") or []
if not choices:
    return "SKIP"
content = choices[0].get("message", {}).get("content", "")
```

**Budget management:**
- Hard cap: 40 files per run
- Priority: ALL `ucode-module-*.md` first, then `luci-api-*.md`
- Skip files already containing `**Summary:**` (idempotent across runs)
- 1.5-second delay between API calls
- On HTTP 429: stop cleanly, log files processed, don't retry, don't fail
- Skippable via `workflow_dispatch` input `skip_ai`

### Step 11: Assemble Single-File References + Promote Static Docs

Runs **after** Steps 8–10 so all enhancements (cross-references, deprecation
warnings, AI summaries) are present in both modular and concatenated files.

Five complete reference files produced at repo root:
- `ucode-complete-reference.md`
- `luci-jsapi-complete-reference.md`
- `openwrt-wiki-complete-reference.md`
- `openwrt-buildroot-complete-reference.md`
- `openwrt-examples-complete-reference.md`

Each file: title + source URLs + timestamp → description → TOC →
`---` separator → all individual files concatenated, separated by `---`.

For examples, each source file is wrapped in a labelled fenced code block
identifying the app, filename, and type (ucode backend vs JS frontend).

**Static docs promotion:** Copy `static-docs/*.md` to repo root. If absent
or empty, log a note and continue.

### Step 12: Generate Root llms.txt

Generate `llms.txt` dynamically from files that actually exist. Do not
hardcode — files may be absent if steps were skipped.

**Critical:** Use `|| true` on all `grep` and `cat` operations to prevent
`set -e` from killing the script when a directory is empty:
```bash
[ -f ucode-docs/llms.txt ] && cat ucode-docs/llms.txt | grep -v "^#" || true
```

> **v5 field-test finding:** The original v5 had output validation (Step 13)
> running *before* llms.txt generation, causing a false "llms.txt is MISSING"
> warning. The correct order is: generate llms.txt first, then validate.

### Step 12a: Generate CHANGES.md

Diff each `llms.txt` index against its last-committed version using
`git diff HEAD -- <file>`. Write results to `CHANGES.md` with fenced
diff blocks per file. If no changes detected, write a "no changes" note.

### Step 13: Validate Outputs

Check critical files exist and are not suspiciously small. Thresholds:
- `ucode-complete-reference.md`: ≥ 200 lines
- `luci-jsapi-complete-reference.md`: ≥ 200 lines
- `ucode-docs/`: ≥ 3 `.md` files
- `luci-docs/`: ≥ 3 `.md` files
- `llms.txt`: ≥ 10 lines

**Warning-only mode** — print warnings but do NOT fail the workflow.
A partial deployment is more useful than no deployment.

### Step 14: Publish to GitHub Pages

```yaml
- uses: actions/upload-pages-artifact@v4
  with:
    path: '.'
- uses: actions/deploy-pages@v4
```

**Before upload,** remove all intermediate build artifacts to prevent them
from being served on the GitHub Pages site:
```bash
rm -rf repo-ucode repo-luci repo-openwrt
rm -f jsdoc-ucode.err jsdoc-luci.err jsdoc.err
rm -rf node_modules/ .venv/
```

Note: `.github/` is ignored by GitHub Pages by default.

Requires `pages: write` and `id-token: write` permissions. GitHub Pages
source must be set to "GitHub Actions" in repository settings.

### Step 15: Commit Generated Files Back to Repository

**Git identity is required** — Actions runners have no default user configured:
```bash
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
```

**`git add` with `--all`:** Tracks additions, modifications, AND deletions.
Without `--all`, deleted files remain in the repo indefinitely.

**`git push` is non-fatal:** The Pages artifact is uploaded before this step,
so a push failure does not prevent documentation from being published:
```bash
git add --all .
git commit -m "docs: auto-update LLM-optimized documentation" || echo "No changes to commit"
git push || echo "Git push failed — artifact was still deployed to Pages"
```

---

## 6. Workflow Trigger and Schedule

```yaml
on:
  schedule:
    - cron: '0 2 1 * *'      # Monthly on the 1st at 02:00 UTC
  workflow_dispatch:
    inputs:
      skip_wiki:
        description: 'Skip OpenWrt wiki scraping (faster run)'
        type: choice
        options: ['false', 'true']
        default: 'false'
      skip_buildroot:
        description: 'Skip buildroot source extraction (faster run)'
        type: choice
        options: ['false', 'true']
        default: 'false'
      skip_ai:
        description: 'Skip AI summarization (saves GitHub Models quota)'
        type: choice
        options: ['false', 'true']
        default: 'false'

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: generate-llm-docs
  cancel-in-progress: true
```

Monthly cadence aligns with the pace of OpenWrt upstream changes, minimizes
load on openwrt.org servers, and fits within all free tier limits.

---

## 7. Tool Selection Rationale

| Tool | Alternative | Reason |
|---|---|---|
| `?do=export_raw` + pandoc | `?do=export_xhtml` + html2text | Raw markup is the actual source; pandoc has native DokuWiki parser |
| `sitemap.xml` for age filtering | Fetch each page for date | 1 HTTP request for all age data vs N |
| `jsdoc-to-markdown` per file | Single run or JSON AST | Per-file produces granular named outputs; JSON AST added complexity without resolving LuCI's config crash |
| Sparse checkout for buildroot | Full clone | Full buildroot is multi-gigabyte |
| `openai/gpt-4o-mini` via GitHub Models | External AI API | Zero cost; uses `$GITHUB_TOKEN`; no extra secrets |
| Root-relative paths in cross-refs | Relative paths | Relative paths break when files concatenated into root-level references |
| Collect-then-apply-reverse | Offset tracking | Offset tracking fragile with multiple insertions; reverse is correct by construction |
| `with open()` context managers | Bare `open().write()` | Guarantees handles closed on exception; prevents silent truncation |
| `git add --all` | Plain `git add` | Tracks deletions in addition to additions and modifications |

---

## 8. Error Handling and Resilience

The distinction between **fatal** and **non-fatal** failures is a first-class
design requirement:

| Category | Examples | Handling |
|---|---|---|
| **Fatal** — abort the run | git clone fails, npm install fails | `\|\| { echo "..."; exit 1; }` |
| **Non-fatal** — skip and continue | wiki unreachable, single page fails, AI rate-limited, app dir missing | `exit(0)` in Python; `\|\| true` or `\|\| echo "..."` in shell |

Full error handling reference:

| Failure scenario | Category | Handling |
|---|---|---|
| `git clone` fails | Fatal | `\|\| { echo "Failed to clone X"; exit 1; }` |
| `npm install` fails | Fatal | `\|\| { echo "npm install failed"; exit 1; }` |
| jsdoc2md produces no output | Non-fatal | 15-word filter silently skips |
| jsdoc2md produces stderr | Informational | Redirect to `jsdoc.err`; not `/dev/null` |
| `sitemap.xml` unreachable | Non-fatal | Python `exit(0)` with warning |
| Individual wiki page fetch fails | Non-fatal | Log and continue |
| AI step hits HTTP 429 | Non-fatal | Stop cleanly; log progress; continue workflow |
| `static-docs/` absent | Non-fatal | Log note; skip; continue |
| App has < 3 source files | Non-fatal | Log warning; skip app; continue |
| No changes since last run | Non-fatal | `git commit ... \|\| echo "No changes"` |
| `git push` fails | Non-fatal | `git push \|\| echo "Push failed — Pages deployed"` |

---

## 9. Shell Scripting Standards

- **Variable quoting:** Quote all expansions used as paths
- **Heredoc indentation:** In standalone `.sh` files, write at column 0
  (no YAML indentation context)
- **Tool stderr:** Never discard to `/dev/null` — use named files (`jsdoc.err`)
- **Fatal pattern:** `some_cmd || { echo "Descriptive message"; exit 1; }`
- **Non-fatal pattern:** `some_cmd || echo "Optional step failed — continuing"`
- **Idempotent pattern:** `git commit -m "..." || echo "No changes to commit"`

---

## 10. Python Coding Standards

- **Context managers** for all file writes: `with open(path, "w") as f:`
- **Safe dictionary access** for API responses: `.get()` with fallbacks
- **Non-fatal exits:** `sys.exit(0)` on recoverable failures, never `exit(1)`
- **Imports:** All standard library modules at file top; no deferred imports
- **Output buffering:** `PYTHONUNBUFFERED=1` set at job level in YAML
- **Encoding:** Always specify `encoding="utf-8"` in `open()` calls

---

## 11. What Is Intentionally Excluded

| Feature | Reason |
|---|---|
| SYSTEM-PROMPT / glossary / recipes generation | Requires deep judgment; better generated locally |
| Forum Q&A scraping | Separate project (Discourse API) |
| Git commit message extraction | Deferred to v7 |
| Map-reduce synthesis | Exceeds GitHub Models free daily quota |
| Archive.org fallback for deleted pages | Adds significant complexity; deferred |
| Version-tagged GitHub Releases | Deferred to v7 after core pipeline validated |

---

## 12. Pipeline Refactoring: Modular Script Architecture

### 12.1 Objective

The monolithic `generate-llm-docs.yml` has exceeded 90 KB. All embedded
business logic — Bash heredocs, inline Python, jsdoc invocations — is mixed
into YAML with compounding indentation and escaping constraints. This creates
four compounding problems:

- LLMs and code editors lose context and produce incorrect edits as the file grows
- The heredoc indentation rule is easily violated and fails silently
- None of the logic can be run or tested locally without triggering a full
  GitHub Actions run
- Debuggability is poor: a failure in the middle of a 400-line `run:` block
  produces minimal context

The refactoring moves all business logic to standalone, version-controlled
script files in `.github/scripts/`. The `.github/workflows/generate-llm-docs.yml`
becomes a thin orchestrator responsible only for: triggers, runtime setup, and
sequentially invoking the scripts.

All functional behavior defined in Sections 1–11 of this document remains
unchanged.

***

### 12.2 Target Script Layout

```text
.github/scripts/
  requirements.txt              # Python dependencies for all .py scripts
  01-setup-and-clone.sh         # Steps 0-2: env cleanup, repo clones, GITHUB_ENV writes
  02-generate-jsdoc.py          # Steps 3-4: jsdoc2md for ucode AND LuCI (pure Python)
  03-scrape-wiki.py             # Step 5: sitemap fetch, DokuWiki raw export, pandoc
  04-extract-buildroot.sh       # Steps 6-7: buildroot Makefile extraction, LuCI examples
  05-inject-refs.py             # Steps 8-9: cross-reference injection, deprecation checker
  06-ai-summarize.py            # Step 10: GitHub Models AI summarization
  07-assemble-publish.sh        # Steps 11-15: assemble refs, llms.txt, validate, cleanup, commit
```

The numerical prefix documents execution order and makes the pipeline flow
self-evident without reading the workflow YAML.

> **Design decision (from reviewer feedback):** Steps 3-4 use a **Python**
> script (`02-generate-jsdoc.py`), not a Bash script with embedded Python
> heredocs. Python's `subprocess` module handles the `jsdoc2md` invocation,
> and the same script handles output parsing, metadata injection, and
> `llms.txt` generation. This gives full IDE linting, syntax highlighting,
> and avoids the "Python inside Bash" anti-pattern that plagued the monolithic
> YAML.

***

### 12.3 Script Responsibility Matrix

Each script owns a well-defined set of responsibilities. This table maps
every pipeline step to its owning script and lists the key operations:

| Script | Steps | Key Responsibilities |
|---|---|---|
| `01-setup-and-clone.sh` | 0, 1*, 2 | Create/clean output dirs; clone ucode, luci, openwrt (sparse); write `UCODE_COMMIT`, `LUCI_COMMIT`, `OPENWRT_COMMIT` to `$GITHUB_ENV` |
| `02-generate-jsdoc.py` | 1*, 3, 4 | Detect ucode jsdoc config (post-clone); skip LuCI config; run `jsdoc2md` per-file for both repos; generate per-folder `llms.txt`; report jsdoc stderr |
| `03-scrape-wiki.py` | 5 | Fetch sitemap; age-filter; incremental scrape; pandoc conversion; generate `llms.txt` |
| `04-extract-buildroot.sh` | 6, 7 | Makefile metadata extraction; README capping; example app file copy with `cp --parents`; generate both `llms.txt` files |
| `05-inject-refs.py` | 8, 9 | Build symbol index; collect-then-apply-reverse cross-refs; deprecation lookahead; idempotency guard |
| `06-ai-summarize.py` | 10 | Budget management; priority ordering; `**Summary:**` idempotency check; rate limit handling; token fallback for local dev |
| `07-assemble-publish.sh` | 11-15 | Assemble 5 complete references; promote static-docs; generate root `llms.txt`; generate `CHANGES.md`; validate outputs; remove build artifacts; git identity + commit + push |

*Step 1 (config detection) is split: the file-search logic lives in
`02-generate-jsdoc.py` since it needs the result immediately, but the
cloning that makes the files available happens in `01-setup-and-clone.sh`.

***

### 12.3 The Thin Orchestrator

`generate-llm-docs.yml` must contain no embedded Bash logic beyond the setup
calls defined below. Its responsibilities are:

1. Declare triggers (cron, `workflow_dispatch` with skip inputs)
2. Declare permissions (`contents: write`, `pages: write`, `id-token: write`)
3. Configure `PYTHONUNBUFFERED=1` as a job-level environment variable
4. Install runtimes: Node.js 20, Python 3.12
5. Install system tools and dependencies
6. Invoke each numbered script as a sequential `run:` step
7. Pass skip inputs to scripts via `if:` conditions on steps

```yaml
name: Generate LLM-Optimized Documentation

on:
  schedule:
    - cron: '0 2 1 * *'
  workflow_dispatch:
    inputs:
      skip_wiki:
        description: 'Skip OpenWrt wiki scraping (faster run)'
        type: choice
        options: ['false', 'true']
        default: 'false'
      skip_buildroot:
        description: 'Skip buildroot source extraction (faster run)'
        type: choice
        options: ['false', 'true']
        default: 'false'
      skip_ai:
        description: 'Skip AI summarization (saves GitHub Models quota)'
        type: choice
        options: ['false', 'true']
        default: 'false'

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: generate-llm-docs
  cancel-in-progress: true

env:
  PYTHONUNBUFFERED: "1"

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install tools and dependencies
        run: |
          sudo apt-get update -qq && sudo apt-get install -y pandoc
          npm install -g jsdoc-to-markdown
          pip install -r .github/scripts/requirements.txt

      - name: "Steps 0-2: Setup and clone"
        run: ./.github/scripts/01-setup-and-clone.sh

      - name: "Steps 3-4: Generate API documentation"
        run: python .github/scripts/02-generate-jsdoc.py

      - name: "Step 5: Scrape OpenWrt wiki"
        if: ${{ inputs.skip_wiki != 'true' }}
        run: python .github/scripts/03-scrape-wiki.py

      - name: "Steps 6-7: Extract buildroot docs and examples"
        if: ${{ inputs.skip_buildroot != 'true' }}
        run: ./.github/scripts/04-extract-buildroot.sh

      - name: "Steps 8-9: Cross-reference injection"
        run: python .github/scripts/05-inject-refs.py

      - name: "Step 10: AI summarization"
        if: ${{ inputs.skip_ai != 'true' }}
        run: python .github/scripts/06-ai-summarize.py

      - name: "Steps 11-15: Assemble, validate, and publish"
        run: ./.github/scripts/07-assemble-publish.sh

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: '.'

  deploy-pages:
    needs: generate-docs
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

The `if:` conditions on skip-able steps replace the inline conditional guards
from v5.

***

### 12.4 File Permissions (Critical for Windows Developers)

Git on Windows does not preserve Unix file permissions. Bash scripts pushed
from a Windows machine will be committed without the executable bit, causing
`Permission denied` failures on the Ubuntu runner.

Do **not** add `chmod +x` inside the YAML — if the runner can't execute the
script, the `chmod` step will never be reached.

**Do** set the executable bit in the Git index directly:

```bash
git update-index --chmod=+x .github/scripts/*.sh
git update-index --chmod=+x .github/scripts/*.py
git commit -m "Set executable bit on pipeline scripts"
```

This permanently stores the permission in the Git object model and survives
re-cloning on any OS.

***

### 12.5 Line Endings (Critical for Windows Developers)

If `.sh` or `.py` files are saved with CRLF line endings, Linux will fail
with: `/usr/bin/env: bad interpreter: No such file or directory`

Add `.gitattributes` at repo root:
```text
.github/scripts/*.sh  text eol=lf
.github/scripts/*.py  text eol=lf
```

Commit this **before** committing any scripts.

***

### 12.6 Python Requirements

```text
# .github/scripts/requirements.txt
requests
beautifulsoup4
lxml
```

Local installation: `pip install -r .github/scripts/requirements.txt`

***

### 12.7 Bash Script Standards

Every `.sh` script must begin with:
```bash
#!/bin/bash
set -euo pipefail
set -x
trap 'echo "ERROR in $0 at line $LINENO: $BASH_COMMAND" >&2' ERR
```

| Flag | Behavior |
|---|---|
| `set -e` | Exit immediately on non-zero exit code |
| `set -u` | Treat undefined variables as errors |
| `set -o pipefail` | Catch failures inside pipes |
| `set -x` | Print each command to stderr (execution trace) |
| `trap ... ERR` | Report line number and command on failure |

Fatal/non-fatal distinction from Section 8 is preserved exactly within scripts.

***

### 12.8 Python Script Standards

- **Output buffering:** `PYTHONUNBUFFERED=1` at job level (Section 12.3)
- **Imports:** All standard library modules at file top
- **Non-fatal:** `sys.exit(0)` on recoverable failures, not `sys.exit(1)`
- **Error Tracing/Logging:** Include simple `print()` statements with timestamps
  at the start of major processing loops so GitHub Actions logs clearly show
  which file or URL was being processed if a script hangs or fails.
- **State reporting:** Use `$GITHUB_OUTPUT` (not deprecated `::set-output`).
  Guard for local testing:
  ```python
  github_output = os.environ.get("GITHUB_OUTPUT")
  if github_output:
      with open(github_output, "a") as f:
          f.write(f"processed_files={count}\n")
  ```
- **File writes:** `with open(...)` context managers everywhere
- **API access:** `.get()` with fallbacks, never bare bracket indexing

***

### 12.9 Sharing State Between Scripts via GITHUB_ENV

Each script runs in a separate shell process. `export` inside a script is
not visible to subsequent scripts. Write to `$GITHUB_ENV` instead:

```bash
# In 01-setup-and-clone.sh:
echo "UCODE_COMMIT=$(git -C repo-ucode rev-parse --short HEAD)" >> "$GITHUB_ENV"
```

```python
# In 02-generate-jsdoc.py, 05-inject-refs.py, etc:
ucode_commit = os.environ.get("UCODE_COMMIT", "unknown")
```

| Variable | Set in | Consumed in |
|---|---|---|
| `UCODE_COMMIT` | `01` | `02`, `05`, `07` |
| `LUCI_COMMIT` | `01` | `02`, `05`, `07` |
| `OPENWRT_COMMIT` | `01` | `05`, `07` |

***

### 12.10 Local Testing

This is the primary benefit of the refactoring. Any script can now be run
locally to debug failures without consuming GitHub Actions minutes or API quota.

```bash
# Prerequisites
git clone <repo> && cd <repo>
pip install -r .github/scripts/requirements.txt
npm install -g jsdoc-to-markdown
sudo apt-get install -y pandoc    # or: brew install pandoc on macOS

# Run individual scripts
export UCODE_COMMIT="abc1234"
export LUCI_COMMIT="def5678"
bash .github/scripts/01-setup-and-clone.sh
python .github/scripts/02-generate-jsdoc.py
python .github/scripts/05-inject-refs.py
```

**Idempotency note:** Because `05-inject-refs.py` modifies files in-place,
running it multiple times locally during debugging could double-wrap links
(e.g., `[[symbol](...)](...)`). The protected-range set must include existing
Markdown links so already-injected references are skipped on re-runs.

**Token fallback for AI testing:**
```python
api_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("LOCAL_DEV_TOKEN")
if not api_token:
    print("WARNING: No API token. Skipping AI summarization.")
    sys.exit(0)
```

Do **not** hardcode any token value in any script file, even temporarily.

***

### 12.11 Refactoring Execution Plan

The recommended sequence for actually performing the refactoring from the
monolithic `generate-llm-docs-v5.yml` to the modular architecture:

1. **Create the folder structure:**
   ```bash
   mkdir -p .github/scripts
   ```

2. **Add `.gitattributes`** (before any scripts):
   ```bash
   echo '.github/scripts/*.sh  text eol=lf' >> .gitattributes
   echo '.github/scripts/*.py  text eol=lf' >> .gitattributes
   git add .gitattributes && git commit -m "Add .gitattributes for LF line endings"
   ```

3. **Create `requirements.txt`:**
   ```bash
   echo -e "requests\nbeautifulsoup4\nlxml" > .github/scripts/requirements.txt
   ```

4. **Port the Python scripts first** (these are the most complex):
   - Extract the Step 3/4 heredocs into `02-generate-jsdoc.py`
   - Extract Step 5 into `03-scrape-wiki.py`
   - Extract Steps 8-9 into `05-inject-refs.py`
   - Extract Step 10 into `06-ai-summarize.py`

5. **Port the Bash scripts second:**
   - Write `01-setup-and-clone.sh` (Steps 0-2 + cleanup)
   - Write `04-extract-buildroot.sh` (Steps 6-7)
   - Write `07-assemble-publish.sh` (Steps 11-15, including git identity config)

6. **Set executable permissions:**
   ```bash
   git update-index --chmod=+x .github/scripts/*.sh
   git update-index --chmod=+x .github/scripts/*.py
   ```

7. **Replace the YAML:** Create the new thin orchestrator as
   `generate-llm-docs.yml`, replacing the 90 KB monolith.

8. **Test:** Run the workflow with all skip flags enabled to verify the
   orchestrator correctly invokes each script.

***

### 12.12 Changes to Earlier Sections

The following rules from earlier sections are **superseded** or **simplified**
by the refactoring:

| Section | Original Rule | Status in v6 |
|---|---|---|
| §9: Heredoc indentation | Heredoc delimiters must match YAML indent | **Eliminated.** Standalone scripts have no YAML context. Write heredocs at column 0. |
| §5 Step 1: Config detection | Scrape live documentation sites | **Replaced.** Post-clone file search for ucode; explicit skip for LuCI. |
| §5 Steps 3-4: Two-Pass JSON AST | Extract AST, render per-entity with Handlebars | **Replaced.** Per-file invocation proved reliable in v5 field test. JSON AST added complexity without resolving the LuCI config crash. |
| §8: Fatal vs non-fatal | Enforced inline via YAML `exit 1` or `true` | **Unchanged in behavior.** Now enforced inside individual scripts using the same exit code patterns. |
| §10: Embedded Python | Python heredocs inside `run:` blocks | **Eliminated.** Python logic lives in `.py` files with full IDE support. |

No changes to output directory structure, file naming conventions, metadata
header format, llms.txt format, cross-reference algorithm, deprecation
detection window, AI budget rules, or GitHub Pages deployment steps.