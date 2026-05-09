import tempfile
from unittest.mock import patch

from lib.ai_corpus import load_l2_documents, split_frontmatter

def test_load_l2_documents_missing_yaml_dependency():
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch.dict('sys.modules', {'yaml': None}):
            documents, issues = load_l2_documents(temp_dir)

            assert documents == {}
            assert issues == ["Missing dependency: pyyaml"]

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
