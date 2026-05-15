from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.pytest_pipeline_support import PROJECT_ROOT
from tests.support.runner_support import _resolve_repo_python


REPO_PYTHON = _resolve_repo_python()
QA_ORCHESTRATOR_PATH = PROJECT_ROOT / "tests" / "qa_pipeline_orchestrator.py"


def load_qa_orchestrator_module():
    spec = importlib.util.spec_from_file_location("qa_pipeline_orchestrator_test_module", QA_ORCHESTRATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


qa_orchestrator = load_qa_orchestrator_module()


def build_demo_layout() -> qa_orchestrator.ContainerLayout:
    return qa_orchestrator.ContainerLayout(
        workspace="/workspace",
        pipeline_run_dir="/workspace/tmp/ci/qa/demo/pipeline-run",
        downloads_dir="/workspace/tmp/ci/qa/demo/pipeline-run/downloads",
        processed_dir="/workspace/tmp/ci/qa/demo/pipeline-run/processed",
        staged_dir="/workspace/tmp/ci/qa/demo/pipeline-run/staged",
        ai_data_base_dir="/workspace/tmp/ci/qa/demo/pipeline-run/ai-data/base",
        ai_data_override_dir="/workspace/tmp/ci/qa/demo/pipeline-run/ai-data/override",
        wiki_cache_dir="/workspace/.cache/shared/wiki",
        ucode_bin_dir="/workspace/tmp/ci/qa/demo/pipeline-run/downloads/repo-ucode/build-install/bin",
        ucode_lib_dir="/workspace/tmp/ci/qa/demo/pipeline-run/downloads/repo-ucode/build-install/lib",
    )


def seed_clone_bundle(result_dir: Path) -> None:
    downloads_dir = result_dir / "pipeline-run" / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    (downloads_dir / "repo-manifest.json").write_text("{}", encoding="utf-8")
    for repo_dir_name in qa_orchestrator.REQUIRED_CLONE_DIR_NAMES:
        (downloads_dir / repo_dir_name).mkdir(parents=True, exist_ok=True)


def test_qa_surface_files_exist() -> None:
    expected_files = [
        "AGENTS.md",
        "mise.toml",
        "tests/qa_pipeline_orchestrator.py",
    ]

    for relative_path in expected_files:
        assert (PROJECT_ROOT / relative_path).is_file(), relative_path


def test_qa_docs_reference_the_containerized_runner() -> None:
    expected_docs = [
        "AGENTS.md",
        "CLAUDE.md",
        "DEVELOPMENT.md",
        "README.md",
        "tests/README.md",
        "tools/testing/README.md",
    ]

    for relative_path in expected_docs:
        text = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        assert "run qa" in text, relative_path


def test_qa_docs_promote_optional_mise_modes() -> None:
    doc_expectations = {
        "AGENTS.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
        "CLAUDE.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
        "DEVELOPMENT.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
        "README.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
        "tests/README.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
        "tools/testing/README.md": ["qa-smoke", "qa-wiki-refresh", "qa-ai-generate", "qa-full"],
    }

    for relative_path, snippets in doc_expectations.items():
        text = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        for snippet in snippets:
            assert snippet in text, f"{relative_path}: missing {snippet}"


def test_mise_toml_promotes_first_class_qa_tasks() -> None:
    mise_text = (PROJECT_ROOT / "mise.toml").read_text(encoding="utf-8")

    assert 'QA_WIKI_CACHE_DIR = ".cache/shared/wiki"' in mise_text
    assert "[tasks.qa-smoke]" in mise_text
    assert "[tasks.qa-wiki-refresh]" in mise_text
    assert "[tasks.qa-ai-generate]" in mise_text
    assert "[tasks.qa-full]" in mise_text


def test_qa_orchestrator_help_exposes_cli_surface() -> None:
    completed = subprocess.run(
        [str(REPO_PYTHON), str(QA_ORCHESTRATOR_PATH), "--help"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "--only-stage" in completed.stdout
    assert "--ai-mode" in completed.stdout
    assert "--skip-buildroot" in completed.stdout
    assert "--image" in completed.stdout
    assert "--wiki-cache-dir" in completed.stdout


def test_qa_orchestrator_stage_window_reaches_stage_08() -> None:
    specs = qa_orchestrator.build_stage_specs(None)

    assert len(specs) == len(qa_orchestrator.PIPELINE_SCRIPTS_TO_STAGE_08)
    assert specs[0].slug == "01-clone-repos"
    assert specs[-1].slug == "08-validate-output"


def test_qa_orchestrator_build_container_env_matches_ci_contract() -> None:
    layout = build_demo_layout()

    env = qa_orchestrator.build_container_env(
        layout,
        ai_mode="stored",
        skip_wiki=True,
        skip_buildroot=False,
        max_ai_files=17,
    )

    assert env["CI"] == "true"
    assert env["PIPELINE_RUN_DIR"] == layout.pipeline_run_dir
    assert env["AI_MODE"] == "stored"
    assert env["SKIP_WIKI"] == "true"
    assert env["SKIP_BUILDROOT"] == "false"
    assert env["MAX_AI_FILES"] == "17"


def test_qa_orchestrator_forwards_opt_in_env_values(monkeypatch: pytest.MonkeyPatch) -> None:
    layout = build_demo_layout()
    monkeypatch.setenv("LOCAL_DEV_TOKEN", "demo-token")
    monkeypatch.setenv("WIKI_MAX_PAGES", "1")
    monkeypatch.setenv("AI_VALIDATE_PAYLOAD", "false")
    monkeypatch.setenv("NO_PROXY", "   ")

    env = qa_orchestrator.build_container_env(
        layout,
        ai_mode="generate",
        skip_wiki=False,
        skip_buildroot=True,
        max_ai_files=9,
    )

    assert env["LOCAL_DEV_TOKEN"] == "demo-token"
    assert env["WIKI_MAX_PAGES"] == "1"
    assert env["AI_MODE"] == "generate"
    assert env["AI_VALIDATE_PAYLOAD"] == "false"
    assert "WRITE_AI" not in env
    assert "NO_PROXY" not in env


def test_qa_orchestrator_rejects_cached_runs_without_refresh_sentinel(
    tmp_path: Path,
) -> None:
    with pytest.raises(SystemExit, match="qa-wiki-refresh"):
        qa_orchestrator.ensure_cached_run_prerequisites(
            wiki_cache_dir=tmp_path / "wiki",
            ai_mode="stored",
            only_stage=None,
        )


def test_qa_orchestrator_rejects_generate_mode_without_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wiki_cache_dir = tmp_path / "wiki"
    metadata_dir = wiki_cache_dir / "http-metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    (metadata_dir / "wiki-lastmod.json").write_text("{}", encoding="utf-8")
    (wiki_cache_dir / qa_orchestrator.WIKI_CACHE_SENTINEL_NAME).write_text(
        json.dumps({"schema_version": 1, "status": "ready"}),
        encoding="utf-8",
    )
    monkeypatch.delenv("LOCAL_DEV_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    with pytest.raises(SystemExit, match="LOCAL_DEV_TOKEN or GITHUB_TOKEN"):
        qa_orchestrator.ensure_cached_run_prerequisites(
            wiki_cache_dir=wiki_cache_dir,
            ai_mode="generate",
            only_stage=None,
        )


def test_qa_orchestrator_rejects_result_roots_outside_repo(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="must stay inside tmp/ci/qa"):
        qa_orchestrator.resolve_result_dir(str(tmp_path / "outside-qa-root"))


def test_qa_orchestrator_rejects_result_root_at_repo_root() -> None:
    with pytest.raises(SystemExit, match="must stay inside tmp/ci/qa"):
        qa_orchestrator.resolve_result_dir(".")


def test_qa_orchestrator_rejects_invalid_stage_selector() -> None:
    with pytest.raises(SystemExit, match="No scripts match selector"):
        qa_orchestrator.build_stage_specs("99")


def test_qa_orchestrator_rejects_fresh_post_extract_isolation(tmp_path: Path) -> None:
    result_dir = qa_orchestrator.resolve_result_dir(f"tmp/ci/qa/{tmp_path.name}-isolation")
    stage_specs = qa_orchestrator.build_stage_specs("03")

    with pytest.raises(SystemExit, match="Fresh isolated runs are supported only for a single 01 or 02a stage"):
        qa_orchestrator.ensure_isolated_stage_inputs(stage_specs, result_dir)


def test_qa_orchestrator_rejects_family_02_isolation_without_clone_bundle(tmp_path: Path) -> None:
    result_dir = qa_orchestrator.resolve_result_dir(f"tmp/ci/qa/{tmp_path.name}-family-02")
    stage_specs = qa_orchestrator.build_stage_specs("02")

    with pytest.raises(SystemExit, match="Fresh isolated runs are supported only for a single 01 or 02a stage"):
        qa_orchestrator.ensure_isolated_stage_inputs(stage_specs, result_dir)


def test_qa_orchestrator_rejects_stage_05_without_l2_bundle(tmp_path: Path) -> None:
    result_dir = qa_orchestrator.resolve_result_dir(f"tmp/ci/qa/{tmp_path.name}-stage-05a")
    seed_clone_bundle(result_dir)
    (result_dir / "pipeline-run" / "processed" / "L1-raw").mkdir(parents=True, exist_ok=True)
    stage_specs = qa_orchestrator.build_stage_specs("05a")

    with pytest.raises(SystemExit, match="pipeline-run/processed/L2-semantic/"):
        qa_orchestrator.ensure_isolated_stage_inputs(stage_specs, result_dir)


def test_qa_orchestrator_starts_ucode_build_after_stage_02() -> None:
    pre_ucode = qa_orchestrator.StageSpec(
        label="02i-ingest-cookbook",
        slug="02i-ingest-cookbook",
        command=["python", ".github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py"],
    )
    post_ucode = qa_orchestrator.StageSpec(
        label="03-normalize-semantic",
        slug="03-normalize-semantic",
        command=["python", ".github/scripts/openwrt-docs4ai-03-normalize-semantic.py"],
    )

    assert qa_orchestrator.stage_requires_ucode_build(pre_ucode) is False
    assert qa_orchestrator.stage_requires_ucode_build(post_ucode) is True
