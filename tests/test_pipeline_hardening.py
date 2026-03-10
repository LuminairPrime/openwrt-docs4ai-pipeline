import importlib.util
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / ".github" / "scripts"
WIKI_L2_DIR = PROJECT_ROOT / "openwrt-condensed-docs" / "L2-semantic" / "wiki"

WIKI_ARTIFACT_PATTERNS = {
    "wrap": re.compile(r"(?:\\<|&lt;|<)\s*/?wrap\b", re.IGNORECASE),
    "color": re.compile(r"(?:\\<|&lt;|<)\s*/?color\b", re.IGNORECASE),
    "html_table": re.compile(r"<table|<tr\b|<td\b|<th\b", re.IGNORECASE),
    "sortable": re.compile(r"(?:\\?<\s*/?sortable\b[^>]*\\?>|&lt;\/?sortable\b[^&]*&gt;)", re.IGNORECASE),
    "footnote_aside": re.compile(r"<aside\b[^>]*\bfootnotes\b", re.IGNORECASE),
}


def load_script_module(module_name, script_name):
    script_path = SCRIPTS_DIR / script_name
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def summarize_wiki_l2_corpus(corpus_dir):
    files = sorted(corpus_dir.glob("*.md"))
    summary = {"files": len(files), "duplicate_lead_heading_files": 0}
    for key in WIKI_ARTIFACT_PATTERNS:
        summary[f"{key}_files"] = 0
        summary[f"{key}_occurrences"] = 0

    for markdown_file in files:
        content = markdown_file.read_text(encoding="utf-8")
        for key, pattern in WIKI_ARTIFACT_PATTERNS.items():
            matches = pattern.findall(content)
            if matches:
                summary[f"{key}_files"] += 1
                summary[f"{key}_occurrences"] += len(matches)
        if has_duplicate_lead_heading(content):
            summary["duplicate_lead_heading_files"] += 1

    return summary


def has_duplicate_lead_heading(content):
    top_heading = None
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            top_heading = stripped[2:].strip().casefold()
            continue
        if stripped.startswith("## "):
            return stripped[3:].strip().casefold() == top_heading
        return False
    return False


def classify_wiki_l2_sanity(summary):
    if summary["files"] < 80:
        return "abnormal"
    if summary["duplicate_lead_heading_files"] > 0:
        return "abnormal"
    for key in WIKI_ARTIFACT_PATTERNS:
        if summary[f"{key}_files"]:
            return "abnormal"
    return "clean"


def test_ucode_normalize_fenced_blocks_classifies_shell_json_and_pseudocode():
    ucode = load_script_module("ucode_scraper", "openwrt-docs4ai-02b-scrape-ucode.py")

    markdown = (
        "```\n"
        "$ echo hello\n"
        "```\n\n"
        "```\n"
        "{\n"
        '  "name": "demo"\n'
        "}\n"
        "```\n\n"
        "```\n"
        "listener(…)\n"
        "```\n"
    )

    normalized = ucode.normalize_fenced_blocks(markdown, "ucode")

    assert "```bash" in normalized
    assert "```json" in normalized
    assert "```text" in normalized


def test_ucode_fix_known_issues_rewrites_nl80211_named_const_import():
    ucode = load_script_module("ucode_scraper_fixups", "openwrt-docs4ai-02b-scrape-ucode.py")

    source = (
        "import { error, request, listener, waitfor, const } from 'nl80211';\n"
        "let response = request(cmd);\n"
        "let wifiListener = listener(mask);\n"
        "let event = waitfor(wifiListener);\n"
        "return const.NL80211_CMD_GET_INTERFACE;\n"
    )

    fixed = ucode.fix_known_ucode_example_issues(source)

    assert "import * as nl80211 from 'nl80211';" in fixed
    assert "nl80211.request(cmd)" in fixed
    assert "nl80211.listener(mask)" in fixed
    assert "nl80211.waitfor(wifiListener)" in fixed
    assert "nl80211.const.NL80211_CMD_GET_INTERFACE" in fixed


def test_clean_wiki_semantic_content_strips_wrap_color_and_duplicate_rows():
    normalize = load_script_module("normalize_semantic", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# The Bootloader\n\n"
        "\\<WRAP round tip\\> Being firmware, \\<color red\\>**bootloader code matters**\\</color\\>.\\</WRAP\\>\n\n"
        "<table>\n"
        "<thead><tr><th>Name</th><th>Meaning</th></tr></thead>\n"
        "<tbody>\n"
        "<tr class=\"odd\"><td>A</td><td>alpha</td></tr>\n"
        "<tr class=\"odd\"><td>A</td><td>alpha</td></tr>\n"
        "</tbody>\n"
        "</table>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("The Bootloader", raw)

    assert "WRAP" not in cleaned
    assert "color red" not in cleaned
    assert "**bootloader code matters**" in cleaned
    assert "<table" not in cleaned
    assert "| Name | Meaning |" in cleaned
    assert cleaned.count("| A | alpha |") == 1


def test_clean_wiki_semantic_content_removes_immediate_duplicate_heading():
    normalize = load_script_module("normalize_semantic_headings", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = "# Adding new elements to LuCI\n\n## Adding new elements to LuCI\n\nBody text.\n"

    cleaned = normalize.clean_wiki_semantic_content("Adding new elements to LuCI", raw)

    assert cleaned.count("Adding new elements to LuCI") == 1
    assert "Body text." in cleaned


def test_clean_wiki_semantic_content_strips_sortable_and_converts_data_table():
    normalize = load_script_module("normalize_semantic_sortable", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# odhcpd\n\n"
        "\\<sortable\\>\n\n"
        "<table>\n"
        "<thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead>\n"
        "<tbody>\n"
        "<tr><td><code>ra</code></td><td>string</td><td>Router Advert service.<br />Use <code>server</code> or <code>relay</code>.</td></tr>\n"
        "</tbody>\n"
        "</table>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("odhcpd", raw)

    assert "sortable" not in cleaned.casefold()
    assert "<table" not in cleaned
    assert "| Name | Type | Description |" in cleaned
    assert "Router Advert service.; Use `server` or `relay`." in cleaned


def test_clean_wiki_semantic_content_converts_callout_table_to_admonition():
    normalize = load_script_module("normalize_semantic_callout", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# Hotplug -- Legacy\n\n"
        "<table>\n"
        "<tbody>\n"
        "<tr>\n"
        "<td><img src=\"/meta/icons/tango/48px-outdated.svg.png\" alt=\"48px-outdated.svg.png\" /></td>\n"
        "<td>See the <a href=\"/docs/guide-user/base-system/hotplug\">Hotplug article</a> for information on the current approach.<br /><br />The daemon was replaced with <a href=\"/docs/techref/procd\">procd</a>.</td>\n"
        "</tr>\n"
        "</tbody>\n"
        "</table>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("Hotplug -- Legacy", raw)

    assert "<table" not in cleaned
    assert "> [!WARNING]" in cleaned
    assert "[Hotplug article](/docs/guide-user/base-system/hotplug)" in cleaned
    assert "[procd](/docs/techref/procd)" in cleaned


def test_clean_wiki_semantic_content_converts_wide_layout_table_to_tsv():
    normalize = load_script_module("normalize_semantic_tsv", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# The OpenWrt Flash Layout\n\n"
        "<table>\n"
        "<thead><tr><th>Layer0</th><th>Layer1</th><th>Layer2</th><th>Layer3</th><th>Layer4</th></tr></thead>\n"
        "<tbody>\n"
        "<tr><td>raw flash</td><td>bootloader<br />partition</td><td>firmware</td><td><code>rootfs</code><br />mounted: <code>/rom</code></td><td>OverlayFS</td></tr>\n"
        "</tbody>\n"
        "</table>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("The OpenWrt Flash Layout", raw)

    assert "<table" not in cleaned
    assert "```tsv" in cleaned
    assert "Layer0\tLayer1\tLayer2\tLayer3\tLayer4" in cleaned


def test_clean_wiki_semantic_content_converts_footnotes_and_inline_html():
    normalize = load_script_module("normalize_semantic_footnotes", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# Architecture\n\n"
        "Raw NOR flash is <u>error-free</u><a href=\"#fn1\" class=\"footnote-ref\" id=\"fnref1\"><sup>1</sup></a>.\n\n"
        "<aside id=\"footnotes\" class=\"footnotes footnotes-end-of-document\">\n"
        "<ol>\n"
        "<li id=\"fn1\">Vendor claim. <a href=\"#fnref1\" class=\"footnote-back\">↩︎</a></li>\n"
        "</ol>\n"
        "</aside>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("Architecture", raw)

    assert "<aside" not in cleaned
    assert "<u>" not in cleaned
    assert "**error-free**[^1]" in cleaned
    assert "[^1]: Vendor claim." in cleaned


def test_clean_wiki_semantic_content_preserves_unsupported_table_shape():
    normalize = load_script_module("normalize_semantic_preserve", "openwrt-docs4ai-03-normalize-semantic.py")

    raw = (
        "# Preserved Table\n\n"
        "<table>\n"
        "<tbody>\n"
        "<tr><td rowspan=\"2\">A</td><td>B</td></tr>\n"
        "<tr><td>C</td></tr>\n"
        "</tbody>\n"
        "</table>\n"
    )

    cleaned = normalize.clean_wiki_semantic_content("Preserved Table", raw)

    assert "<table" in cleaned
    assert "rowspan=\"2\"" in cleaned


def test_validate_extract_markdown_code_blocks_handles_indented_fences():
    validate = load_script_module("validator_module", "openwrt-docs4ai-08-validate.py")

    markdown = (
        "- Example block:\n\n"
        "    ```ucode\n"
        "    export default 1;\n"
        "    ```\n"
    )

    blocks = validate.extract_markdown_code_blocks(markdown)

    assert blocks == [("ucode", "export default 1;")]


def test_validate_extract_ucode_imports_supports_multiple_import_forms():
    validate = load_script_module("validator_imports", "openwrt-docs4ai-08-validate.py")

    code = (
        "import * as nl from 'nl80211';\n"
        "import { readfile } from 'fs';\n"
        "import 'uloop';\n"
    )

    imports = validate.extract_ucode_imports(code)

    assert imports == ["fs", "nl80211", "uloop"]


def test_wiki_l2_committed_corpus_sanity_snapshot():
    assert WIKI_L2_DIR.exists(), f"Missing committed wiki corpus: {WIKI_L2_DIR}"

    summary = summarize_wiki_l2_corpus(WIKI_L2_DIR)
    status = classify_wiki_l2_sanity(summary)
    artifact_stats = " ".join(
        f"{name}={summary[f'{name}_files']}/{summary[f'{name}_occurrences']}"
        for name in WIKI_ARTIFACT_PATTERNS
    )

    print(
        "[sanity] wiki-l2 "
        f"status={status} "
        f"files={summary['files']} "
        f"{artifact_stats} "
        f"duplicate_lead_heading={summary['duplicate_lead_heading_files']}"
    )

    assert status == "clean"
    assert summary["duplicate_lead_heading_files"] == 0
    for key in WIKI_ARTIFACT_PATTERNS:
        assert summary[f"{key}_files"] == 0