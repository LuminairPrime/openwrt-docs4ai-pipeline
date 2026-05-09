import tempfile
from unittest.mock import patch

from lib.ai_corpus import load_l2_documents, split_frontmatter


def test_load_l2_documents_missing_yaml_dependency():
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch.dict('sys.modules', {'yaml': None}):
            documents, issues = load_l2_documents(temp_dir)

            assert documents == {}
            assert issues == ["Missing dependency: pyyaml"]


def test_load_l2_documents_unreadable_file(tmp_path, monkeypatch):
    l2_root = tmp_path / "l2"
    l2_root.mkdir()

    module_dir = l2_root / "test_module"
    module_dir.mkdir()

    test_file = module_dir / "unreadable.md"
    test_file.write_text("---\ntitle: Unreadable File\n---\nBody text")

    original_open = open

    def mock_open(*args, **kwargs):
        if "unreadable.md" in str(args[0]):
            raise PermissionError("Mocked unreadable file")
        return original_open(*args, **kwargs)

    monkeypatch.setattr("builtins.open", mock_open)

    documents, issues = load_l2_documents(str(l2_root))

    assert "Unreadable L2 file test_module/unreadable: Mocked unreadable file" in issues
    assert ("test_module", "unreadable") not in documents


def test_load_l2_documents_invalid_yaml_frontmatter(tmp_path):
    l2_root = tmp_path / "L2-semantic"
    l2_root.mkdir()

    module_dir = l2_root / "test_module"
    module_dir.mkdir()

    file_path = module_dir / "test_doc.md"
    file_path.write_text(
        """---
title: Test Document
invalid_yaml: [this, is, missing, a, closing, bracket
---

# Body
""",
        encoding="utf-8",
    )

    documents, issues = load_l2_documents(str(l2_root))

    assert len(documents) == 0
    assert len(issues) == 1
    assert "Invalid YAML frontmatter in test_module/test_doc" in issues[0]


def test_split_frontmatter_happy_path():
    content = "---\ntitle: Test\n---\nBody content here."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test"
    assert body == "Body content here."

def test_split_frontmatter_windows_newlines():
    content = "---\r\ntitle: Test\r\n---\r\nBody content here."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test"
    assert body == "Body content here."

def test_split_frontmatter_no_frontmatter():
    content = "Just body content here."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter is None
    assert body is None

def test_split_frontmatter_empty_frontmatter():
    content = "---\n\n---\nBody content here."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == ""
    assert body == "Body content here."

def test_split_frontmatter_empty_body():
    content = "---\ntitle: Test\n---"
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test"
    assert body == ""

def test_split_frontmatter_no_trailing_newline_after_frontmatter():
    # If the file ends right after ---
    content = "---\ntitle: Test\n---"
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test"
    assert body == ""

def test_split_frontmatter_multiline_frontmatter():
    content = "---\ntitle: Test\nauthor: Jules\n---\nBody content here.\nLine 2"
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test\nauthor: Jules"
    assert body == "Body content here.\nLine 2"

def test_split_frontmatter_malformed_not_at_start():
    content = "Some text before\n---\ntitle: Test\n---\nBody content here."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter is None
    assert body is None

def test_split_frontmatter_missing_closing_dashes():
    content = "---\ntitle: Test\nBody content here without closing dashes."
    frontmatter, body = split_frontmatter(content)
    assert frontmatter is None
    assert body is None

def test_split_frontmatter_extra_dashes_in_body():
    content = "---\ntitle: Test\n---\nBody content with ---\nmore dashes"
    frontmatter, body = split_frontmatter(content)
    assert frontmatter == "title: Test"
    assert body == "Body content with ---\nmore dashes"
