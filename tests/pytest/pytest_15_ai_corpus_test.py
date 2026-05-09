import sys
import tempfile
from unittest.mock import patch

from lib.ai_corpus import load_l2_documents

def test_load_l2_documents_missing_yaml_dependency():
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch.dict('sys.modules', {'yaml': None}):
            documents, issues = load_l2_documents(temp_dir)

            assert documents == {}
            assert issues == ["Missing dependency: pyyaml"]
