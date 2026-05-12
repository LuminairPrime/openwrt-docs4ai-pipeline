"""
qa_pipeline_orchestrator.py

CI-in-a-box: Spins up an ephemeral Docker container mirroring the GitHub Actions
Linux runner, executes the numbered pipeline scripts sequentially inside it, and
tears down cleanly on completion or failure.

Intended entry point: mise run qa
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ─── Project root resolution ───────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ─── Container-scoped environment variables (mirrors CI env) ────────────
CONTAINER_ENV: dict[str, str] = {
    "PIPELINE_RUN_DIR": "/workspace/tmp/pipeline-ci",
    "WORKDIR": "/workspace/tmp/pipeline-ci/downloads",
    "PROCESSED_DIR": "/workspace/tmp/pipeline-ci/processed",
    "STAGED_DIR": "/workspace/tmp/pipeline-ci/staged",
    "OUTDIR": "/workspace/tmp/pipeline-ci/staged",
    "SKIP_AI": "true",
    "VALIDATE_MODE": "soft",
    "HOME": "/root",
}

# ─── Pipeline scripts in execution order ────────────────────────────────
PIPELINE_SCRIPTS: list[str] = [
    "openwrt-docs4ai-03-normalize-semantic.py",
    "openwrt-docs4ai-04-generate-ai-summaries.py",
    "openwrt-docs4ai-05a-assemble-references.py",
    "openwrt-docs4ai-05b-generate-agents-and-readme.py",
    "openwrt-docs4ai-05c-generate-ucode-ide-schemas.py",
    "openwrt-docs4ai-05d-generate-api-drift-changelog.py",
    "openwrt-docs4ai-05e-generate-luci-dts.py",
    "openwrt-docs4ai-06-generate-llm-routing-indexes.py",
    "openwrt-docs4ai-07-generate-web-index.py",
    "openwrt-docs4ai-08-validate-output.py",
    "openwrt-docs4ai-09-build-packages.py",
]

SCRIPTS_DIR_RELATIVE = ".github/scripts"
