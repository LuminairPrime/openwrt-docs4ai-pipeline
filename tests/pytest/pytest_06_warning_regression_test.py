from __future__ import annotations

from pathlib import Path

from tests.support.pytest_pipeline_support import (
    load_script_module,
    load_workflow_text,
)


def test_workflow_uses_node24_native_action_majors() -> None:
    workflow_text = load_workflow_text()

    expected_versions = [
        "actions/checkout@v5",
        "actions/setup-python@v6",
        "actions/cache@v5",
        "actions/upload-artifact@v6",
        "actions/download-artifact@v7",
        "actions/upload-pages-artifact@v4",
        "actions/configure-pages@v5",
        "actions/deploy-pages@v4",
    ]
    removed_versions = [
        "actions/checkout@v4",
        "actions/setup-python@v5",
        "actions/cache@v4",
        "actions/upload-artifact@v4",
        "actions/download-artifact@v4",
        "actions/upload-pages-artifact@v3",
    ]

    for action_ref in expected_versions:
        assert action_ref in workflow_text
    for action_ref in removed_versions:
        assert action_ref not in workflow_text


def test_assemble_references_shards_oversized_modules() -> None:
    assemble = load_script_module(
        "assemble_references_warning_contract",
        "openwrt-docs4ai-05a-assemble-references.py",
    )

    layout = assemble.build_reference_layout(
        "wiki",
        [
            {"token_count": 60_000, "body_text": "# One"},
            {"token_count": 55_000, "body_text": "# Two"},
            {"token_count": 30_000, "body_text": "# Three"},
        ],
        token_limit=100_000,
    )

    assert layout["sharded"] is True
    assert layout["total_token_count"] == 145_000
    assert [part["filename"] for part in layout["parts"]] == [
        "wiki-complete-reference.part-01.md",
        "wiki-complete-reference.part-02.md",
    ]
    assert [part["token_count"] for part in layout["parts"]] == [60_000, 85_000]


def test_validate_known_dockerman_ucode_false_positive_is_exact() -> None:
    validate = load_script_module(
        "validator_known_ucode_false_positive",
        "openwrt-docs4ai-08-validate-output.py",
    )

    rel_path = (
        "L2-semantic/luci-examples/"
        "example_app-luci-app-dockerman-root-usr-share-rpcd-ucode-docker-rpc-uc.md"
    )

    assert validate.is_known_ucode_false_positive(
        rel_path,
        "Syntax error: return must be inside function body",
    )
    assert not validate.is_known_ucode_false_positive(
        rel_path,
        "Syntax error: unexpected token",
    )
    assert not validate.is_known_ucode_false_positive(
        "L2-semantic/luci-examples/other.md",
        "Syntax error: return must be inside function body",
    )


def test_validate_routing_requires_sharded_part_links(tmp_path: Path) -> None:
    validate = load_script_module(
        "validator_sharded_reference_contract",
        "openwrt-docs4ai-08-validate-output.py",
    )

    outdir = tmp_path
    module_dir = outdir / "wiki"
    l2_dir = outdir / "L2-semantic" / "wiki"
    module_dir.mkdir(parents=True)
    l2_dir.mkdir(parents=True)

    (l2_dir / "sample.md").write_text(
        "---\ntoken_count: 10\n---\n# Sample\n\nBody text.\n",
        encoding="utf-8",
    )
    (module_dir / "wiki-skeleton.md").write_text("# skeleton\n", encoding="utf-8")
    (module_dir / "wiki-complete-reference.md").write_text(
        "# complete reference index\n",
        encoding="utf-8",
    )
    (module_dir / "wiki-complete-reference.part-01.md").write_text(
        "# complete reference part 1\n",
        encoding="utf-8",
    )
    (module_dir / "llms.txt").write_text(
        "\n".join(
            [
                "# wiki module",
                "> Example wiki module",
                "> **Total Context:** ~10 tokens",
                "",
                "## Recommended Entry Points",
                "",
                "- [wiki-skeleton.md](./wiki-skeleton.md): skeleton (~1 tokens, l3-skeleton)",
                "- [wiki-complete-reference.md](./wiki-complete-reference.md): index (~1 tokens, l4-monolith)",
                "",
                "## Source Documents",
                "",
                "- [sample.md](../L2-semantic/wiki/sample.md): sample (~1 tokens, l2-source)",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (outdir / "llms-full.txt").write_text(
        "\n".join(
            [
                "# openwrt-docs4ai - Complete Flat Catalog",
                "",
                "- [wiki/llms.txt](./wiki/llms.txt): module index (~1 tokens, l3-module-index)",
                "- [wiki-skeleton.md](./wiki/wiki-skeleton.md): skeleton (~1 tokens, l3-skeleton)",
                "- [wiki-complete-reference.md](./wiki/wiki-complete-reference.md): index (~1 tokens, l4-monolith)",
                "- [sample.md](./L2-semantic/wiki/sample.md): sample (~1 tokens, l2-source)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    hard_failures: list[str] = []
    validate.validate_module_llms_contract(
        str(outdir),
        ["wiki"],
        hard_failures.append,
        lambda _message: None,
    )
    validate.validate_llms_full_contract(
        str(outdir),
        ["wiki"],
        hard_failures.append,
        lambda _message: None,
    )

    assert any(
        "wiki-complete-reference.part-01.md" in failure for failure in hard_failures
    )