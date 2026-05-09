import json
import os
import hashlib
from unittest import mock
import pytest

from lib import extractor
from lib import config

def test_write_l1_markdown_creates_files_with_correct_content(tmp_path):
    # Setup
    module = "test_module"
    origin_type = "wiki"
    slug = "my_page"
    content = "# Hello World\nThis is a test."
    metadata = {"source": "test_script"}

    # Mock config to use tmp_path
    with mock.patch("lib.extractor.config.L1_RAW_WORKDIR", str(tmp_path)):
        extractor.write_l1_markdown(module, origin_type, slug, content, metadata)

        # Verify directory
        out_dir = tmp_path / module
        assert out_dir.is_dir()

        # Verify markdown file
        base_name = f"{origin_type}-{slug}"
        md_path = out_dir / f"{base_name}.md"
        assert md_path.is_file()
        assert md_path.read_text(encoding="utf-8") == content

        # Verify metadata file
        meta_path = out_dir / f"{base_name}.meta.json"
        assert meta_path.is_file()

        saved_metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        assert saved_metadata["source"] == "test_script"

        # Verify content hash
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]
        assert saved_metadata["content_hash"] == expected_hash

def test_write_l1_markdown_handles_none_metadata(tmp_path):
    module = "test_module"
    origin_type = "wiki"
    slug = "my_page"
    content = "# Content Only"

    with mock.patch("lib.extractor.config.L1_RAW_WORKDIR", str(tmp_path)):
        extractor.write_l1_markdown(module, origin_type, slug, content)

        out_dir = tmp_path / module
        base_name = f"{origin_type}-{slug}"
        meta_path = out_dir / f"{base_name}.meta.json"

        saved_metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]
        assert saved_metadata == {"content_hash": expected_hash}

def test_wrap_code_block():
    title = "my_script.sh"
    code = "echo 'hello'"
    lang = "bash"

    result = extractor.wrap_code_block(title, code, lang)
    expected = "# my_script.sh\n```bash\necho 'hello'\n```\n"

    assert result == expected
