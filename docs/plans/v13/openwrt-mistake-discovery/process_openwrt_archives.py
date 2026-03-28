from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.policy import default
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_ROOT = ROOT / "OpenWrt_Archives"
DEFAULT_OUTPUT_ROOT = ROOT / "OpenWrt_Archives_Processed_Small"

MBOX_BOUNDARY_RE = re.compile(
    rb"^From\s+\S+(?:@\S+|\s+at\s+\S+)\s{2}\w{3}\s+\w{3}\s{1,2}\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}\s*$",
    re.MULTILINE,
)

PROBLEM_RE = re.compile(
    r"fail|error|crash|regression|broken|bug|doesn't work|not working|segfault|panic|leak|"
    r"inaccessible|wrong|not building|not compiling|warning|oops|backtrace",
    re.IGNORECASE,
)
CORRECTION_RE = re.compile(
    r"should\s+(?:use|be|have|call)|instead of|proper(?:ly)?|correct(?:ly)?|wrong|incorrect|"
    r"mistake|you need to|you must|do not|don't|better way|the right way|the fix|this fixes|"
    r"must be|use .+ not",
    re.IGNORECASE,
)
PATCH_REVISION_RE = re.compile(r"\[PATCH\s+v[2-9]", re.IGNORECASE)

KEYWORD_PATTERNS = [
    r"error:",
    r"warning:",
    r"fail(?:ed|ure|ing)?",
    r"broken",
    r"regression",
    r"crash",
    r"segfault",
    r"panic",
    r"oops",
    r"backtrace",
    r"bug",
    r"should\s+(?:use|be|have|call)",
    r"instead\s+of",
    r"proper(?:ly)?",
    r"correct(?:ly)?",
    r"wrong",
    r"incorrect",
    r"mistake",
    r"typo",
    r"you\s+need\s+to",
    r"you\s+must",
    r"do\s+not|don't",
    r"better\s+(?:to|way|approach)",
    r"right\s+way",
    r"memory\s+leak",
    r"use[-.\s]after[-.\s]free",
    r"double\s+free",
    r"null[-.\s]pointer",
    r"buffer[-.\s]overflow",
    r"heap",
    r"stack\s+overflow",
    r"uninitialized",
    r"out[-.\s]of[-.\s]bounds",
    r"undefined\s+behavior",
    r"race[-.\s]condition",
    r"deadlock",
    r"mutex",
    r"lock(?:ing)?",
    r"atomic",
    r"thread[-.\s]safe",
    r"synchroniz",
    r"CFLAGS",
    r"LDFLAGS",
    r"Makefile",
    r"PKG_",
    r"compile",
    r"linker",
    r"undefined\s+reference",
    r"implicit\s+declaration",
    r"-Werror",
    r"-Wno-",
    r"out[-.\s]of[-.\s]tree",
    r"kmod",
    r"ubus",
    r"uci",
    r"procd",
    r"netifd",
    r"hotplug",
    r"rpcd",
    r"luci",
    r"uhttpd",
    r"libubox",
    r"ustream",
    r"blobmsg",
    r"init\.d",
    r"rc\.d",
    r"\[PATCH\s+v[2-9]",
    r"Fixes:",
    r"inline",
    r"static",
    r"volatile",
    r"const",
    r"malloc",
    r"calloc",
    r"realloc",
    r"free\(",
    r"strlen",
    r"strcpy",
    r"strncpy",
    r"snprintf",
    r"sprintf",
    r"socket",
    r"bind\(",
    r"ioctl",
    r"netlink",
]
KEYWORD_REGEXES = [(pattern, re.compile(pattern, re.IGNORECASE)) for pattern in KEYWORD_PATTERNS]

CATEGORY_PATTERNS = {
    "memory-management": re.compile(
        r"malloc|calloc|realloc|free\(|memory\s+leak|use[-.\s]after[-.\s]free|double\s+free|"
        r"null[-.\s]pointer|buffer[-.\s]overflow|heap|segfault",
        re.IGNORECASE,
    ),
    "concurrency": re.compile(r"thread|mutex|lock(?:ing)?|race[-.\s]condition|deadlock|atomic|synchron", re.IGNORECASE),
    "build-system": re.compile(r"Makefile|PKG_|CONFIG_|compile|linker|CFLAGS|LDFLAGS|kmod|out[-.\s]of[-.\s]tree|-Werror|-Wno-", re.IGNORECASE),
    "c-language": re.compile(r"inline|static\s+.*void|implicit\s+declaration|undefined\s+behavior|cast|const|volatile|gcc|musl", re.IGNORECASE),
    "uci-config": re.compile(r"uci[_\s]|/etc/config|uci\.batch|uci-defaults|option|config\s+\w+", re.IGNORECASE),
    "procd-init": re.compile(r"procd|init\.d|rc\.d|respawn|service|procd_set_param|procd_close_instance", re.IGNORECASE),
    "networking": re.compile(r"netifd|firewall|nftables|iptables|bridge|vlan|interface|socket|netlink|bind\(", re.IGNORECASE),
    "ubus-ipc": re.compile(r"ubus|blobmsg|libubox|ustream|uloop", re.IGNORECASE),
    "luci-frontend": re.compile(r"luci|uhttpd|rpcd|cbi|\.js|javascript|rpc", re.IGNORECASE),
    "kernel-driver": re.compile(r"kmod|dts|device[-.\s]tree|kernel|insmod|modprobe|module_init", re.IGNORECASE),
    "patch-maintenance": re.compile(r"bump|upstream|obsolete|remove.*patch|supersed|cherry[-.\s]pick|backport", re.IGNORECASE),
    "package-packaging": re.compile(r"ipk|opkg|feed|PKG_SOURCE|PKG_HASH|PKG_VERSION", re.IGNORECASE),
}

STRUCTURAL_SIGNAL_PATTERNS = {
    "has_compiler_error": re.compile(r"\w+\.[ch]:\d+:\d+:\s*(?:error|warning):", re.IGNORECASE),
    "has_stack_trace": re.compile(r"Call Trace:|BUG:|Oops:|Unable to handle|RIP:|PC is at", re.IGNORECASE),
    "has_shell_error": re.compile(r"command not found|No such file|Permission denied|Segmentation fault", re.IGNORECASE),
    "has_build_error": re.compile(r"make\[\d+\]: \*\*\*|ERROR:|FATAL:.*not found|collect2: error", re.IGNORECASE),
    "has_code_block": re.compile(r"(?m)(^[\t ]{4,}\S.*\n){3,}"),
    "has_reference_urls": re.compile(r"https?://(?:bugs\.|github\.com/|git\.|lore\.kernel\.org/|patchwork\.)", re.IGNORECASE),
    "has_patch_revision": re.compile(r"\[PATCH\s+v[2-9]", re.IGNORECASE),
}

FILE_REF_RE = re.compile(
    r"\b(?:package|target|feeds|toolchain|tools|include|scripts|lib|netifd|procd|luci|ucode)/[^\s:()\[\]{}<>\"']+\.(?:c|h|mk|js|uc|json|sh|patch|lua|py|pl|awk|dts|yaml|yml)\b",
    re.IGNORECASE,
)
COMMIT_RE = re.compile(r"\b[a-f0-9]{7,12}\b", re.IGNORECASE)

SEARCH_HINTS = {
    "build-system": [
        "grep -R \"EXTRA_CFLAGS\" package/ target/",
        r"grep -R \"PKG_VERSION|PKG_SOURCE|PKG_HASH\" package/",
    ],
    "procd-init": [
        r"grep -R \"procd_set_param|procd_open_instance|USE_PROCD\" package/",
        "find package -path \"*/files/*\" -name \"*.init\"",
    ],
    "uci-config": [
        r"grep -R \"uci commit|uci set|uci add_list\" package/",
        "grep -R \"/etc/config\" package/",
    ],
    "luci-frontend": [
        r"grep -R \"require view|require form|rpc.declare\" .",
        "find . -path \"*luci*\" -name \"*.js\"",
    ],
    "networking": [
        r"grep -R \"bridge|vlan|firewall|netifd\" package/ target/",
    ],
    "memory-management": [
        r"grep -R \"malloc|calloc|realloc|free(\" package/ tools/",
    ],
    "patch-maintenance": [
        r"grep -R \"PKG_SOURCE_VERSION|backport|upstream\" package/",
    ],
}


@dataclass
class RawMessage:
    source_file: str
    archive_url: str
    byte_offset: int
    from_line: str
    message_bytes: bytes


def decode_header_value(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def normalize_email(value: str) -> str:
    normalized = value.strip().replace(" at ", "@")
    return normalized.strip("<>")


def parse_from_header(value: str) -> tuple[str, str]:
    addresses = getaddresses([decode_header_value(value)])
    if addresses:
        name, address = addresses[0]
        return decode_header_value(name).strip(), normalize_email(address)
    return "", normalize_email(decode_header_value(value))


def parse_message_ids(value: str | None) -> list[str]:
    if not value:
        return []
    found = re.findall(r"<[^>]+>", value)
    return found or [value.strip()]


def parse_mail_date(value: str | None) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    cleaned = re.sub(r"\s*\([^)]+\)\s*$", "", value).strip()
    try:
        parsed = parsedate_to_datetime(cleaned)
        return cleaned, parsed.isoformat()
    except Exception:
        return cleaned, None


def read_text_with_fallback(path: Path) -> bytes:
    return path.read_bytes()


def split_messages(raw_bytes: bytes, relative_path: str) -> list[RawMessage]:
    matches = list(MBOX_BOUNDARY_RE.finditer(raw_bytes))
    messages: list[RawMessage] = []
    archive_url = build_archive_url(relative_path)
    if not matches:
        return messages
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw_bytes)
        chunk = raw_bytes[start:end]
        first_newline = chunk.find(b"\n")
        payload = chunk[first_newline + 1 :] if first_newline >= 0 else b""
        messages.append(
            RawMessage(
                source_file=relative_path,
                archive_url=archive_url,
                byte_offset=start,
                from_line=match.group(0).decode("utf-8", errors="replace").strip(),
                message_bytes=payload,
            )
        )
    return messages


def build_archive_url(relative_path: str) -> str:
    relative = relative_path.replace("\\", "/")
    if relative.startswith("devel/"):
        return f"https://lists.openwrt.org/pipermail/openwrt-devel/{relative.split('/', 1)[1]}"
    if relative.startswith("bugs/"):
        return f"https://lists.openwrt.org/pipermail/openwrt-bugs/{relative.split('/', 1)[1]}"
    return relative


def extract_body_text(message: Any) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_maintype() != "text":
                continue
            if part.get_content_disposition() == "attachment":
                continue
            try:
                payload = part.get_payload(decode=True)
                if payload is None:
                    text = part.get_content()
                    if isinstance(text, str) and text.strip():
                        return text
                    continue
                charset = part.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
            except Exception:
                continue
    payload = message.get_payload(decode=True)
    if isinstance(payload, bytes):
        charset = message.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset, errors="replace")
        except Exception:
            return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        return payload
    return ""


def remove_signature_block(lines: list[str]) -> list[str]:
    for index, line in enumerate(lines):
        if re.match(r"^--\s*$", line):
            return lines[:index]
    return lines


def extract_quoted_context_pairs(lines: list[str]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    quote_buffer: list[str] = []
    in_quote = False
    correction_re = re.compile(
        r"should|instead|wrong|incorrect|fix|proper|better|use\s+.+\s+not|the issue|problem here|"
        r"this\s+(?:is|was)\s+(?:because|due to)|you need|must be|don't do",
        re.IGNORECASE,
    )
    for index, line in enumerate(lines):
        if re.match(r"^\s*>", line):
            quote_buffer.append(re.sub(r"^\s*>\s?", "", line))
            in_quote = True
            continue
        if in_quote:
            end_index = min(index + 4, len(lines))
            following = " ".join(lines[index:end_index])
            if correction_re.search(following):
                pairs.append(
                    {
                        "quoted": "\n".join(quote_buffer).strip(),
                        "response": "\n".join(lines[index:end_index]).strip(),
                        "line_index": index,
                    }
                )
            quote_buffer = []
            in_quote = False
    return pairs


def summarize_diff(lines: list[str]) -> tuple[str, list[str]]:
    summarized: list[str] = []
    mentioned_files: list[str] = []
    in_diff = False
    hunk_line_count = 0
    max_hunk_lines = 5
    for line in lines:
        diff_match = re.match(r"^diff --git a/(\S+)", line)
        if diff_match:
            in_diff = True
            hunk_line_count = 0
            mentioned_files.append(diff_match.group(1))
            summarized.append(f"[diff: {diff_match.group(1)}]")
            continue
        if in_diff:
            hunk_match = re.match(r"^@@\s.*@@\s*(.*)", line)
            if hunk_match:
                context = hunk_match.group(1).strip()
                if context:
                    summarized.append(f"[hunk: {context}]")
                hunk_line_count = 0
                continue
            if re.match(r"^[+-][^+-]", line) and hunk_line_count < max_hunk_lines:
                summarized.append(line)
                hunk_line_count += 1
                continue
            if re.match(r"^--\s*$", line):
                in_diff = False
                break
            continue
        summarized.append(line)
    return "\n".join(summarized).strip(), sorted(set(mentioned_files))


def build_text_views(body_text: str) -> tuple[str, str, list[dict[str, Any]], list[str]]:
    lines = body_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines = remove_signature_block(lines)
    quoted_pairs = extract_quoted_context_pairs(lines)
    body_no_diff, diff_files = summarize_diff(lines)
    scoring_lines = [line for line in body_no_diff.splitlines() if not re.match(r"^\s*>", line)]
    body_for_scoring = "\n".join(scoring_lines).strip()
    extra_refs = FILE_REF_RE.findall(body_no_diff)
    return body_no_diff, body_for_scoring, quoted_pairs, sorted(set(diff_files + extra_refs))


def keyword_matches(text: str) -> list[str]:
    found: list[str] = []
    for pattern, regex in KEYWORD_REGEXES:
        if regex.search(text):
            found.append(pattern)
    return sorted(set(found))


def structural_signals(text: str) -> dict[str, bool]:
    return {name: bool(regex.search(text)) for name, regex in STRUCTURAL_SIGNAL_PATTERNS.items()}


def categorize(text: str) -> list[str]:
    categories = [name for name, regex in CATEGORY_PATTERNS.items() if regex.search(text)]
    return categories or ["uncategorized"]


def disposition(from_addr: str, subject: str, body_for_scoring: str, matched_keywords: list[str], in_reply_to: str | None) -> str:
    if re.search(r"noreply(?:@|\s+at\s+)github\.com|buildbot@|ci@|jenkins@", from_addr, re.IGNORECASE):
        return "dropped"
    if re.search(r"\[VOTE\]|\b(?:CI|buildbot|patchwork)\b", subject, re.IGNORECASE):
        return "sidelined"
    ascii_letters = len(re.findall(r"[A-Za-z]", f"{subject} {body_for_scoring}"))
    if ascii_letters < 20 and not in_reply_to:
        return "dropped"
    if not matched_keywords and not in_reply_to and len(body_for_scoring) < 40:
        return "dropped"
    return "primary"


def split_sentences(text: str) -> list[str]:
    if not text.strip():
        return []
    normalized = re.sub(r"\n{2,}", ".\n", text.replace("\r", ""))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", normalized)
    return [part.strip() for part in parts if part.strip()]


def load_message(raw_message: RawMessage) -> dict[str, Any]:
    message = BytesParser(policy=default).parsebytes(raw_message.message_bytes)
    from_name, from_addr = parse_from_header(message.get("From", ""))
    date_raw, date_iso = parse_mail_date(message.get("Date"))
    subject = decode_header_value(message.get("Subject", ""))
    refs = parse_message_ids(message.get("References"))
    in_reply_list = parse_message_ids(message.get("In-Reply-To"))
    in_reply_to = in_reply_list[0] if in_reply_list else None
    message_id = message.get("Message-ID") or f"<{raw_message.source_file.replace('/', '_')}:{raw_message.byte_offset}>"
    body_text = extract_body_text(message)
    body_no_diff, body_for_scoring, quoted_pairs, mentioned_files = build_text_views(body_text)
    matched_keywords = keyword_matches(f"{subject}\n{body_for_scoring}")
    commits = sorted(set(COMMIT_RE.findall(body_no_diff.lower())))
    categories = categorize(f"{subject}\n{body_no_diff}")
    signals = structural_signals(body_for_scoring)
    return {
        "source_file": raw_message.source_file,
        "archive_url": raw_message.archive_url,
        "byte_offset": raw_message.byte_offset,
        "mbox_from_line": raw_message.from_line,
        "message_id": message_id.strip(),
        "in_reply_to": in_reply_to,
        "references": refs,
        "from_addr": from_addr,
        "from_name": from_name,
        "date_raw": date_raw,
        "date_iso": date_iso,
        "subject": subject,
        "body_for_scoring": body_for_scoring,
        "body_no_diff": body_no_diff,
        "quoted_context_pairs": quoted_pairs,
        "mentioned_files": mentioned_files,
        "mentioned_commits": commits,
        "keyword_matches": matched_keywords,
        "structural_signals": signals,
        "categories": categories,
        "has_patch_subject": bool(re.search(r"\[PATCH", subject, re.IGNORECASE)),
        "has_keyword_match": bool(matched_keywords),
        "disposition": disposition(from_addr, subject, body_for_scoring, matched_keywords, in_reply_to),
    }


def write_jsonl(path: Path, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=False) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_samples(path: Path, items: list[dict[str, Any]], seed: int, count: int = 10) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    selected = items if len(items) <= count else rng.sample(items, count)
    lines = ["# QA Samples", "", "Randomly selected records for manual inspection.", ""]
    if not selected:
        lines.append("_No items available._")
    for index, item in enumerate(selected, start=1):
        lines.extend([f"## Sample {index}", "", "```json", json.dumps(item, indent=2, ensure_ascii=False), "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path: Path, title: str, bullets: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""] + [f"- {bullet}" for bullet in bullets]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_thread_root(message: dict[str, Any], by_id: dict[str, dict[str, Any]], cache: dict[str, str]) -> str:
    message_id = message["message_id"]
    if message_id in cache:
        return cache[message_id]
    seen: set[str] = set()
    current = message
    root_id = current["message_id"]
    while True:
        parent_id = current.get("in_reply_to")
        if not parent_id and current.get("references"):
            parent_id = current["references"][0]
        if not parent_id or parent_id in seen or parent_id not in by_id:
            break
        seen.add(parent_id)
        current = by_id[parent_id]
        root_id = current["message_id"]
    cache[message_id] = root_id
    return root_id


def sort_key_for_message(message: dict[str, Any]) -> tuple[str, int]:
    return (message.get("date_iso") or "9999-12-31T23:59:59", int(message.get("byte_offset", 0)))


def merge_signals(messages: list[dict[str, Any]]) -> dict[str, bool]:
    merged: dict[str, bool] = {name: False for name in STRUCTURAL_SIGNAL_PATTERNS}
    for message in messages:
        for name, value in message.get("structural_signals", {}).items():
            merged[name] = merged.get(name, False) or bool(value)
    return merged


def score_thread(thread: dict[str, Any]) -> float:
    messages = thread["messages"]
    all_text = "\n".join(message.get("body_for_scoring", "") for message in messages)
    subject = thread.get("subject", "")
    authors = {message.get("from_addr", "") for message in messages if message.get("from_addr")}
    score = 0.0
    if PROBLEM_RE.search(all_text):
        score += 0.30
    if CORRECTION_RE.search(all_text):
        score += 0.30
    if len(authors) >= 2:
        score += 0.15
    if thread["all_mentioned_files"] or thread["all_mentioned_commits"]:
        score += 0.10
    if len(messages) >= 2:
        score += 0.10
    if PATCH_REVISION_RE.search(subject):
        score += 0.05
    if re.search(r"\bNACK?\b", all_text, re.IGNORECASE):
        score += 0.05
    signals = thread["structural_signals"]
    if signals["has_compiler_error"]:
        score += 0.25
    if signals["has_stack_trace"]:
        score += 0.20
    if signals["has_build_error"]:
        score += 0.20
    if signals["has_code_block"] and len(authors) >= 2:
        score += 0.10
    if signals["has_reference_urls"]:
        score += 0.05
    if signals["has_patch_revision"]:
        score += 0.10
    if re.search(r"bump to", subject, re.IGNORECASE) and len(authors) < 2:
        score -= 0.20
    return round(max(0.0, min(1.0, score)), 2)


def primary_category(categories: list[str]) -> str:
    return categories[0] if categories else "uncategorized"


def build_threads(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {message["message_id"]: message for message in messages}
    cache: dict[str, str] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for message in messages:
        root = resolve_thread_root(message, by_id, cache)
        grouped[root].append(message)

    threads: list[dict[str, Any]] = []
    for root_id, group in grouped.items():
        sorted_messages = sorted(group, key=sort_key_for_message)
        all_files = sorted({ref for message in sorted_messages for ref in message.get("mentioned_files", [])})
        all_commits = sorted({ref for message in sorted_messages for ref in message.get("mentioned_commits", [])})
        all_categories = []
        for message in sorted_messages:
            for category in message.get("categories", []):
                if category not in all_categories:
                    all_categories.append(category)
        thread = {
            "thread_id": root_id,
            "subject": sorted_messages[0].get("subject", ""),
            "messages": sorted_messages,
            "message_count": len(sorted_messages),
            "author_count": len({message.get('from_addr', '') for message in sorted_messages if message.get('from_addr')}),
            "date_range": [sorted_messages[0].get("date_iso"), sorted_messages[-1].get("date_iso")],
            "all_mentioned_files": all_files,
            "all_mentioned_commits": all_commits,
            "categories": all_categories or ["uncategorized"],
            "structural_signals": merge_signals(sorted_messages),
            "source_refs": [
                {
                    "source_file": message["source_file"],
                    "archive_url": message["archive_url"],
                    "message_id": message["message_id"],
                    "byte_offset": message["byte_offset"],
                }
                for message in sorted_messages
            ],
        }
        thread["score"] = score_thread(thread)
        threads.append(thread)
    return sorted(threads, key=lambda item: (-item["score"], item["subject"].lower()))


def extract_snippet(messages: list[dict[str, Any]], pattern: re.Pattern[str], preferred_other_author: str | None = None) -> dict[str, Any] | None:
    candidate_messages = messages
    if preferred_other_author:
        filtered = [message for message in messages if message.get("from_addr") != preferred_other_author]
        if filtered:
            candidate_messages = filtered
    for message in candidate_messages:
        sentences = split_sentences(message.get("body_no_diff", ""))
        for index, sentence in enumerate(sentences):
            if pattern.search(sentence):
                start = max(0, index - 1)
                end = min(len(sentences), index + 3)
                return {
                    "from": message.get("from_addr"),
                    "snippet": " ".join(sentences[start:end]).strip(),
                    "message_id": message.get("message_id"),
                }
    return None


def derive_title(thread: dict[str, Any], problem: dict[str, Any] | None, fix: dict[str, Any] | None) -> str:
    subject = re.sub(r"^(?:Re:\s*)*(?:\[[^\]]+\]\s*)+", "", thread.get("subject", "")).strip()
    if problem and fix and problem.get("snippet") and fix.get("snippet"):
        return f"{subject}: mistake and correction"
    if problem and problem.get("snippet"):
        return f"{subject}: recurring problem pattern"
    return subject or thread.get("thread_id", "untitled thread")


def search_hints(categories: list[str], files: list[str]) -> list[str]:
    hints: list[str] = []
    for category in categories:
        hints.extend(SEARCH_HINTS.get(category, []))
    for file_ref in files[:5]:
        hints.append(f'grep -R "{Path(file_ref).name}" .')
    deduped: list[str] = []
    for hint in hints:
        if hint not in deduped:
            deduped.append(hint)
    return deduped


def extract_lessons(threads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    for index, thread in enumerate(threads, start=1):
        messages = thread["messages"]
        problem = extract_snippet(messages, PROBLEM_RE)
        problem_author = problem.get("from") if problem else None
        fix = extract_snippet(messages, CORRECTION_RE, preferred_other_author=problem_author)
        completeness = {
            "has_problem": bool(problem and problem.get("snippet")),
            "has_fix": bool(fix and fix.get("snippet")),
            "has_file_refs": bool(thread["all_mentioned_files"]),
            "has_commit_refs": bool(thread["all_mentioned_commits"]),
            "level": "fragmentary",
        }
        if completeness["has_problem"] and completeness["has_fix"]:
            completeness["level"] = "complete"
        elif completeness["has_problem"] and completeness["has_file_refs"]:
            completeness["level"] = "searchable"
        elif completeness["has_problem"]:
            completeness["level"] = "problem-only"

        lessons.append(
            {
                "lesson_id": f"lesson-{index:04d}",
                "thread_id": thread["thread_id"],
                "title": derive_title(thread, problem, fix),
                "score": thread["score"],
                "categories": thread["categories"],
                "problem": problem,
                "fix": fix,
                "mentioned_files": thread["all_mentioned_files"],
                "mentioned_commits": thread["all_mentioned_commits"],
                "source_refs": thread["source_refs"],
                "codebase_search_hints": search_hints(thread["categories"], thread["all_mentioned_files"]),
                "completeness": completeness,
            }
        )
    return lessons


def write_lesson_index(path: Path, lessons: list[dict[str, Any]], source_label: str) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for lesson in lessons:
        grouped[primary_category(lesson["categories"])].append(lesson)
    lines = [
        f"# OpenWrt Programming Lesson Ideas ({source_label})",
        "",
        f"Generated from {source_label} mailing-list archives.",
        "Each item should be paired later with a positive code example from the OpenWrt source tree.",
        "",
    ]
    for category in sorted(grouped):
        lines.extend([f"## {category}", ""])
        for lesson in sorted(grouped[category], key=lambda item: (-item["score"], item["title"].lower())):
            source = lesson["source_refs"][0]
            problem = lesson.get("problem") or {}
            fix = lesson.get("fix") or {}
            lines.append(f"### {lesson['title']}")
            lines.append("")
            lines.append(f"- Score: {lesson['score']}")
            lines.append(f"- Completeness: {lesson['completeness']['level']}")
            lines.append(f"- Source file: {source['source_file']}")
            lines.append(f"- Archive URL: {source['archive_url']}")
            lines.append(f"- Root message ID: {source['message_id']}")
            if problem.get("snippet"):
                lines.extend(["", "Problem:", f"> {problem['snippet']}"])
            if fix.get("snippet"):
                lines.extend(["", "Fix or correction:", f"> {fix['snippet']}"])
            else:
                lines.extend(["", "Fix or correction:", "> Not found in archive; search codebase for the correct pattern."])
            if lesson["mentioned_files"]:
                lines.extend(["", f"Files: {', '.join(lesson['mentioned_files'])}"])
            if lesson["codebase_search_hints"]:
                lines.extend(["", "Codebase search:", "```bash", *lesson["codebase_search_hints"], "```"])
            lines.extend(["", "---", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_codebase_search_guide(path: Path, lessons: list[dict[str, Any]]) -> None:
    grouped: dict[str, list[str]] = defaultdict(list)
    for lesson in lessons:
        for category in lesson["categories"]:
            grouped[category].extend(lesson["codebase_search_hints"])
    lines = [
        "# Codebase Search Guide",
        "",
        "Run these commands from the root of a cloned OpenWrt repository to find likely positive examples.",
        "",
    ]
    for category in sorted(grouped):
        seen: list[str] = []
        for hint in grouped[category]:
            if hint not in seen:
                seen.append(hint)
        lines.extend([f"## {category}", "", "```bash", *seen, "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_common_problem_summary(path: Path, lessons: list[dict[str, Any]]) -> None:
    category_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for lesson in lessons:
        category_groups[primary_category(lesson["categories"])].append(lesson)

    lines = [
        "# Common Problems Summary",
        "",
        "This file condenses the larger lesson report into recurring problem families that can later be paired with positive examples from the OpenWrt source tree.",
        "",
        "## Overview",
        "",
        f"- Total lesson candidates: {len(lessons)}",
        f"- Categories represented: {len(category_groups)}",
        "- Each section below shows high-frequency keyword signals and representative referenced threads.",
        "",
    ]

    for category in sorted(category_groups):
        grouped_lessons = sorted(category_groups[category], key=lambda item: (-item["score"], item["title"].lower()))
        keyword_counter: Counter[str] = Counter()
        completeness_counter: Counter[str] = Counter()
        for lesson in grouped_lessons:
            keyword_counter.update(lesson.get("categories", []))
            source_keywords = lesson.get("problem", {}) or {}
            snippet = source_keywords.get("snippet", "")
            if snippet:
                for token in re.findall(r"[A-Za-z][A-Za-z0-9_.:-]{2,}", snippet.lower()):
                    if token in {"the", "and", "for", "with", "that", "this", "from", "into", "have", "will", "when", "then", "not"}:
                        continue
                    keyword_counter[token] += 1
            completeness_counter[lesson["completeness"]["level"]] += 1

        lines.extend([f"## {category}", ""])
        lines.append(f"- Lesson candidates: {len(grouped_lessons)}")
        lines.append(
            "- Completeness: "
            + ", ".join(f"{name}={count}" for name, count in sorted(completeness_counter.items()))
        )
        top_keywords = [token for token, _count in keyword_counter.most_common(12)]
        if top_keywords:
            lines.append(f"- Common signals: {', '.join(top_keywords)}")
        lines.extend(["", "Representative referenced problems:", ""])

        for lesson in grouped_lessons[:5]:
            source = lesson["source_refs"][0]
            problem = lesson.get("problem") or {}
            lines.append(f"### {lesson['title']}")
            lines.append("")
            lines.append(f"- Score: {lesson['score']}")
            lines.append(f"- Completeness: {lesson['completeness']['level']}")
            lines.append(f"- Source file: {source['source_file']}")
            lines.append(f"- Archive URL: {source['archive_url']}")
            lines.append(f"- Root message ID: {source['message_id']}")
            if problem.get("snippet"):
                lines.append(f"- Problem excerpt: {problem['snippet']}")
            if lesson.get("mentioned_files"):
                lines.append(f"- Mentioned files: {', '.join(lesson['mentioned_files'][:5])}")
            lines.append("")

        lines.extend(["---", ""])

    path.write_text("\n".join(lines), encoding="utf-8")


def build_parse_stage(messages: list[dict[str, Any]], output_root: Path, seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    parsed_root = output_root / "parsed"
    primary = [message for message in messages if message["disposition"] == "primary"]
    sidelined = [message for message in messages if message["disposition"] == "sidelined"]
    dropped = [message for message in messages if message["disposition"] == "dropped"]
    write_jsonl(parsed_root / "messages-primary.jsonl", primary)
    write_jsonl(parsed_root / "messages-sidelined.jsonl", sidelined)
    write_jsonl(parsed_root / "messages-dropped.jsonl", dropped)
    write_json(
        parsed_root / "stats.json",
        {
            "stage": "parsed",
            "messages_parsed": len(messages),
            "messages_kept": {
                "primary": len(primary),
                "sidelined": len(sidelined),
                "dropped": len(dropped),
            },
            "keyword_match_rate": round(sum(1 for message in messages if message["has_keyword_match"]) / len(messages) * 100, 1) if messages else 0.0,
        },
    )
    write_samples(parsed_root / "samples.md", primary, seed)
    write_readme(
        parsed_root / "README.md",
        "OpenWrt Archive Parsed Output",
        [
            "messages-primary.jsonl contains messages kept for threading and scoring.",
            "messages-sidelined.jsonl contains lower-priority but potentially useful messages.",
            "messages-dropped.jsonl contains obvious noise and notification traffic.",
        ],
    )
    return primary, sidelined, dropped


def build_thread_stage(primary: list[dict[str, Any]], output_root: Path, seed: int) -> list[dict[str, Any]]:
    threaded_root = output_root / "threaded"
    threads = build_threads(primary)
    write_jsonl(threaded_root / "threads.jsonl", threads)
    cross_month_threads = 0
    for thread in threads:
        unique_files = {source["source_file"] for source in thread["source_refs"]}
        if len(unique_files) > 1:
            cross_month_threads += 1
    write_json(
        threaded_root / "stats.json",
        {
            "stage": "threaded",
            "threads_created": len(threads),
            "cross_month_threads": cross_month_threads,
            "messages_threaded": len(primary),
        },
    )
    write_samples(threaded_root / "samples.md", threads, seed)
    write_readme(
        threaded_root / "README.md",
        "OpenWrt Archive Threaded Output",
        [
            "threads.jsonl groups primary messages by Message-ID, In-Reply-To, and References.",
            "stats.json highlights cross-month threading behavior.",
        ],
    )
    return threads


def build_score_stage(threads: list[dict[str, Any]], output_root: Path, seed: int, threshold: float) -> list[dict[str, Any]]:
    scored_root = output_root / "scored"
    passing = [thread for thread in threads if thread["score"] >= threshold]
    write_jsonl(scored_root / "threads-scored.jsonl", threads)
    write_jsonl(scored_root / "threads-passing.jsonl", passing)
    write_json(
        scored_root / "stats.json",
        {
            "stage": "scored",
            "threads_total": len(threads),
            "threads_passing": len(passing),
            "threshold": threshold,
        },
    )
    write_samples(scored_root / "samples.md", passing, seed)
    write_readme(
        scored_root / "README.md",
        "OpenWrt Archive Scored Output",
        [
            "threads-scored.jsonl contains all threaded conversations with lesson-potential scores.",
            f"threads-passing.jsonl contains threads with score >= {threshold}.",
        ],
    )
    return passing


def build_lesson_stage(threads: list[dict[str, Any]], output_root: Path, seed: int) -> list[dict[str, Any]]:
    lessons_root = output_root / "lessons"
    lessons = extract_lessons(threads)
    write_jsonl(lessons_root / "lesson_candidates.jsonl", lessons)
    completeness_counts: dict[str, int] = defaultdict(int)
    for lesson in lessons:
        completeness_counts[lesson["completeness"]["level"]] += 1
    write_json(
        lessons_root / "stats.json",
        {
            "stage": "lessons",
            "lesson_candidates": len(lessons),
            "completeness": dict(sorted(completeness_counts.items())),
        },
    )
    write_samples(lessons_root / "samples.md", lessons, seed)
    write_readme(
        lessons_root / "README.md",
        "OpenWrt Lesson Candidates",
        [
            "lesson_candidates.jsonl contains extracted problem/fix candidates ready for human curation.",
            "Completeness labels distinguish complete, searchable, problem-only, and fragmentary lessons.",
        ],
    )
    return lessons


def build_reports(lessons: list[dict[str, Any]], output_root: Path) -> None:
    reports_root = output_root / "reports"
    top_lessons = sorted(lessons, key=lambda item: (-item["score"], item["title"].lower()))
    write_jsonl(reports_root / "top_lessons.jsonl", top_lessons)
    write_lesson_index(reports_root / "openwrt-programming-lesson-ideas.md", top_lessons, "OpenWrt archives")
    write_codebase_search_guide(reports_root / "codebase-search-guide.md", top_lessons)
    write_common_problem_summary(reports_root / "common-problems-summary.md", top_lessons)
    write_json(
        reports_root / "stats.json",
        {
            "stage": "reports",
            "top_lessons": len(top_lessons),
            "categories": sorted({category for lesson in top_lessons for category in lesson["categories"]}),
        },
    )
    write_readme(
        reports_root / "README.md",
        "OpenWrt Archive Reports",
        [
            "openwrt-programming-lesson-ideas.md is the human-readable shortlist for cookbook planning.",
            "common-problems-summary.md is the condensed recurring-problem view for faster review.",
            "codebase-search-guide.md provides commands for locating positive examples in OpenWrt source repositories.",
            "top_lessons.jsonl is the machine-readable ranked lesson list.",
        ],
    )


def collect_input_files(input_root: Path, explicit_files: list[Path] | None) -> list[Path]:
    if explicit_files:
        return [path.resolve() for path in explicit_files]
    return sorted(input_root.rglob("*.txt"))


def relative_source(path: Path, input_root: Path) -> str:
    return path.resolve().relative_to(input_root.resolve()).as_posix()


def process_archives(input_root: Path, output_root: Path, files: list[Path], seed: int, threshold: float) -> dict[str, Any]:
    all_messages: list[dict[str, Any]] = []
    for path in files:
        relative = relative_source(path, input_root)
        for raw_message in split_messages(read_text_with_fallback(path), relative):
            all_messages.append(load_message(raw_message))

    primary, sidelined, dropped = build_parse_stage(all_messages, output_root, seed)
    threads = build_thread_stage(primary, output_root, seed)
    passing = build_score_stage(threads, output_root, seed, threshold)
    lessons = build_lesson_stage(passing, output_root, seed)
    build_reports(lessons, output_root)

    return {
        "input_files": len(files),
        "messages": len(all_messages),
        "primary": len(primary),
        "sidelined": len(sidelined),
        "dropped": len(dropped),
        "threads": len(threads),
        "passing_threads": len(passing),
        "lessons": len(lessons),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process OpenWrt mailing-list archives into condensed lesson candidates.")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--files", nargs="*", type=Path, help="Optional explicit archive files to process.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--score-threshold", type=float, default=0.30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = collect_input_files(args.input_root, args.files)
    if not files:
        raise SystemExit("No archive .txt files found to process.")
    summary = process_archives(args.input_root, args.output_root, files, args.seed, args.score_threshold)
    print(f"[process] Input files: {summary['input_files']}")
    print(f"[process] Messages: {summary['messages']}")
    print(f"[process] Primary: {summary['primary']} | Sidelined: {summary['sidelined']} | Dropped: {summary['dropped']}")
    print(f"[process] Threads: {summary['threads']} | Passing: {summary['passing_threads']} | Lessons: {summary['lessons']}")
    print(f"[process] Output root: {args.output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())