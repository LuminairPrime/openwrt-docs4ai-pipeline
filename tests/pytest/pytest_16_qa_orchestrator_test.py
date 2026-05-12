import pytest


def test_imports_orchestrator():
    """Verify the orchestrator module is importable."""
    from tests.qa_pipeline_orchestrator import PIPELINE_SCRIPTS

    assert isinstance(PIPELINE_SCRIPTS, list)
    assert "openwrt-docs4ai-03-normalize-semantic.py" in PIPELINE_SCRIPTS


def test_orchestrator_pipeline_scripts_order():
    """Verify pipeline scripts are in correct dependency order."""
    from tests.qa_pipeline_orchestrator import PIPELINE_SCRIPTS

    # 03 must come before 04, 05 before 06, 06 before 07, 07 before 08
    indices = {script: idx for idx, script in enumerate(PIPELINE_SCRIPTS)}
    assert indices["openwrt-docs4ai-03-normalize-semantic.py"] < indices["openwrt-docs4ai-04-generate-ai-summaries.py"]
    assert indices["openwrt-docs4ai-05a-assemble-references.py"] < indices["openwrt-docs4ai-06-generate-llm-routing-indexes.py"]
    assert indices["openwrt-docs4ai-06-generate-llm-routing-indexes.py"] < indices["openwrt-docs4ai-07-generate-web-index.py"]
    assert indices["openwrt-docs4ai-07-generate-web-index.py"] < indices["openwrt-docs4ai-08-validate-output.py"]


def test_build_container_command_structure():
    """Verify container command includes key stages."""
    from tests.qa_pipeline_orchestrator import build_container_command

    command = build_container_command()
    assert isinstance(command, list)
    assert command[0] == "/bin/bash"
    assert command[1] == "-c"

    script_body = command[2]
    assert "mkdir -p /workspace/tmp/pipeline-ci" in script_body
    assert "pip install -r /workspace/.github/scripts/requirements.txt" in script_body
    assert "openwrt-docs4ai-03-normalize-semantic.py" in script_body
    assert "openwrt-docs4ai-08-validate-output.py" in script_body
    assert "exit 1" in script_body  # failure halting


def test_build_container_command_runs_every_script():
    """Verify every script in PIPELINE_SCRIPTS appears in the command."""
    from tests.qa_pipeline_orchestrator import build_container_command, PIPELINE_SCRIPTS

    command = build_container_command()
    script_body = command[2]

    for script in PIPELINE_SCRIPTS:
        assert script in script_body, f"{script} missing from container command"


def test_check_docker_available_graceful_when_missing():
    """Verify the check function handles Docker being unavailable gracefully."""
    from tests.qa_pipeline_orchestrator import _check_docker_available

    result = _check_docker_available()
    assert isinstance(result, bool)
    # If Docker is not available, test should still pass
    # (we're testing the function, not Docker availability)
