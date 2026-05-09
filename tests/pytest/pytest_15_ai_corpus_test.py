from lib.ai_corpus import load_l2_documents


def test_load_l2_documents_invalid_yaml_frontmatter(tmp_path):
    # Create L2 root directory
    l2_root = tmp_path / "L2-semantic"
    l2_root.mkdir()

    # Create a module directory
    module_dir = l2_root / "test_module"
    module_dir.mkdir()

    # Create a markdown file with invalid YAML frontmatter
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

    # Call the function
    documents, issues = load_l2_documents(str(l2_root))

    # Assert
    assert len(documents) == 0
    assert len(issues) == 1
    assert "Invalid YAML frontmatter in test_module/test_doc" in issues[0]
