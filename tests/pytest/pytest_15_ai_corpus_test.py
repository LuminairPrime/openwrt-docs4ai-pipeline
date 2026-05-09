
from lib.ai_corpus import load_l2_documents

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
