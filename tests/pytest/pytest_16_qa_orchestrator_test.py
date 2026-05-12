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
