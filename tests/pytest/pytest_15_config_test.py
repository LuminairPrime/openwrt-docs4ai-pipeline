import json
import os
from unittest.mock import patch

from lib.config import _write_json_atomic


def test_write_json_atomic_creates_file_with_correct_content(tmp_path):
    target_file = tmp_path / "subdir" / "test.json"
    payload = {"key": "value", "nested": {"a": 1}}

    _write_json_atomic(str(target_file), payload)

    assert target_file.exists()
    content = target_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    loaded_payload = json.loads(content)
    assert loaded_payload == payload

    # Check that it uses indent=2
    expected_content = '{\n  "key": "value",\n  "nested": {\n    "a": 1\n  }\n}\n'
    assert content == expected_content


def test_write_json_atomic_uses_temp_file_and_replaces(tmp_path):
    target_file = tmp_path / "test.json"
    temp_file = str(target_file) + ".tmp"
    payload = {"status": "ok"}

    # Track calls to os.replace
    original_replace = os.replace

    def mock_replace(src, dst):
        # Temp file should exist and have correct content before replace
        assert os.path.exists(src)
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
            assert json.loads(content) == payload
        original_replace(src, dst)

    with patch("os.replace", side_effect=mock_replace) as mock:
        _write_json_atomic(str(target_file), payload)

    mock.assert_called_once_with(temp_file, str(target_file))
    assert target_file.exists()
    assert not os.path.exists(temp_file)
