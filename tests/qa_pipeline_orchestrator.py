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
    "SKIP_WIKI": "true",
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


# ─── Container command builder ─────────────────────────────────────────

def build_container_command() -> list[str]:
    """Build the shell command that the container will execute.

    Creates the directory structure, installs dependencies from requirements.txt,
    then executes each pipeline script in order, halting on first failure.
    """
    mkdir_cmd = "mkdir -p /workspace/tmp/pipeline-ci/downloads /workspace/tmp/pipeline-ci/processed /workspace/tmp/pipeline-ci/staged"
    install_cmd = "pip install -r /workspace/.github/scripts/requirements.txt -q"

    script_commands: list[str] = []
    for script in PIPELINE_SCRIPTS:
        script_path = f"/workspace/{SCRIPTS_DIR_RELATIVE}/{script}"
        script_commands.append(
            f"echo '=== Running {script} ===' && "
            f"python {script_path} || (echo 'FAILED: {script}' && exit 1)"
        )

    pipeline_body = " && ".join([mkdir_cmd, install_cmd] + script_commands)
    return ["/bin/bash", "-c", pipeline_body]


# ─── Container orchestration ───────────────────────────────────────────

def run_pipeline_in_container() -> int:
    """Spin up container, execute pipeline, return exit code.

    Returns:
        0 on full success, 1 on any pipeline script failure.
    """
    from testcontainers.core.container import DockerContainer

    print("=== QA Pipeline Orchestrator ===")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Scripts directory: {PROJECT_ROOT / SCRIPTS_DIR_RELATIVE}")
    print()

    command = build_container_command()

    with DockerContainer("python:3.12-slim") as container:
        container.with_volume_mapping(
            str(PROJECT_ROOT), "/workspace"
        )
        for key, value in CONTAINER_ENV.items():
            container.with_env(key, value)

        result = container.exec(command)
        exit_code, output = result
        print(output.decode("utf-8", errors="replace"))

        if exit_code != 0:
            print(f"\nPipeline FAILED with exit code {exit_code}", file=sys.stderr)
            return 1

        print("\n=== Pipeline PASSED ===")
        return 0


# ─── Docker availability check ──────────────────────────────────────────

def _check_docker_available() -> bool:
    """Return True if Docker is running and accessible."""
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


# ─── CLI entry point ───────────────────────────────────────────────────

def main() -> int:
    """Entry point for mise run qa."""
    if not _check_docker_available():
        print(
            "Docker is not available. Ensure Docker Desktop is running "
            "or WSL integration is enabled.",
            file=sys.stderr,
        )
        return 2  # distinct exit code for environment issue

    return run_pipeline_in_container()


if __name__ == "__main__":
    sys.exit(main())
