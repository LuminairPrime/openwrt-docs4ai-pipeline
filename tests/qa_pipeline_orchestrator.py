"""QA Pipeline Orchestrator — mirrors GitHub Actions CI locally via testcontainers.

Uses testcontainers-python to spin up an ephemeral Linux container matching the
GitHub Actions runner image, bind-mount the project directory, inject CI
environment variables, and sequentially execute pipeline scripts 01 through 08
with exit-code validation and guaranteed teardown.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

from testcontainers.core.container import DockerContainer

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONTAINER_IMAGE = "python:3.12-slim"
CONTAINER_WORKSPACE = "/workspace"

CI_ENV = {
    "PIPELINE_RUN_DIR": f"{CONTAINER_WORKSPACE}/tmp/pipeline-ci",
    "WORKDIR": f"{CONTAINER_WORKSPACE}/tmp/pipeline-ci/downloads",
    "PROCESSED_DIR": f"{CONTAINER_WORKSPACE}/tmp/pipeline-ci/processed",
    "STAGED_DIR": f"{CONTAINER_WORKSPACE}/tmp/pipeline-ci/staged",
    "OUTDIR": f"{CONTAINER_WORKSPACE}/tmp/pipeline-ci/staged",
}

# ── Pipeline stage definitions ──────────────────────────────────────────────


@dataclass
class PipelineStage:
    """A single stage in the QA pipeline execution sequence."""

    script: str       # stem name, e.g. "01-clone-repos"
    label: str        # human-readable label, e.g. "Clone Repos"
    timeout: int = 300   # per-stage timeout in seconds
    optional: bool = False  # failure is non-fatal when True


PIPELINE_STAGES: tuple[PipelineStage, ...] = (
    PipelineStage("01-clone-repos", "Clone Repos", timeout=600),
    PipelineStage("02a-scrape-wiki", "Scrape Wiki", timeout=1200),
    PipelineStage("02i-ingest-cookbook", "Ingest Cookbook", timeout=300),
    PipelineStage("02b-scrape-ucode", "Scrape ucode", timeout=600),
    PipelineStage("02c-scrape-jsdoc", "Scrape LuCI jsdoc", timeout=900),
    PipelineStage("02d-scrape-core-packages", "Scrape Core Packages", timeout=600),
    PipelineStage("02e-scrape-example-packages", "Scrape Examples", timeout=600),
    PipelineStage("02f-scrape-procd-api", "Scrape procd", timeout=300),
    PipelineStage("02g-scrape-uci-schemas", "Scrape UCI Schemas", timeout=300),
    PipelineStage("02h-scrape-hotplug-events", "Scrape Hotplug", timeout=300),
    PipelineStage("03-normalize-semantic", "Normalize L2", timeout=900),
    PipelineStage("04-generate-ai-summaries", "AI Summaries", timeout=600, optional=True),
    PipelineStage("05a-assemble-references", "Assemble References", timeout=600),
    PipelineStage("05b-generate-agents-and-readme", "Generate Agents/README", timeout=300),
    PipelineStage("05c-generate-ucode-ide-schemas", "Generate ucode DTS", timeout=300),
    PipelineStage("05d-generate-api-drift-changelog", "API Drift Changelog", timeout=300),
    PipelineStage("05e-generate-luci-dts", "Generate LuCI DTS", timeout=300),
    PipelineStage("06-generate-llm-routing-indexes", "LLM Routing Indexes", timeout=300),
    PipelineStage("07-generate-web-index", "Web Index", timeout=300),
    PipelineStage("08-validate-output", "Validate Output", timeout=600),
)


def _script_path(stage: PipelineStage) -> str:
    """Resolve a PipelineStage to its full container script path."""
    script_filename = f"openwrt-docs4ai-{stage.script}.py"
    return f"{CONTAINER_WORKSPACE}/.github/scripts/{script_filename}"


# ── Container lifecycle ──────────────────────────────────────────────────────


def create_container() -> DockerContainer:
    """Build a configured but not-yet-started DockerContainer.

    Returns a testcontainers DockerContainer configured with bind mounts,
    CI environment variables, and an idle command (tail -f /dev/null).
    The caller must call ``container.start()`` before use.
    """
    container = (
        DockerContainer(CONTAINER_IMAGE)
        .with_bind_mount(str(PROJECT_ROOT), CONTAINER_WORKSPACE)
        .with_env("CI", "true")
        .with_command("tail -f /dev/null")
    )
    for key, value in CI_ENV.items():
        container = container.with_env(key, value)
    return container


# ── Remote execution helpers ─────────────────────────────────────────────────


_DEFAULT_TIMEOUT = 300  # seconds, used for non-pipeline commands


def _exec(container: DockerContainer, cmd: str, timeout: int = _DEFAULT_TIMEOUT) -> tuple[int, str]:
    """Execute a command inside the container.

    Returns ``(exit_code, output_text)``.  Both stdout and stderr are
    captured and combined so that error diagnostics are preserved.

    Uses the Docker SDK ``exec_run`` directly so that *timeout* is
    enforced — a hung command will not block the pipeline indefinitely.
    """
    exit_code, output = container.get_wrapped_container().exec_run(
        cmd, timeout=timeout
    )
    stdout = (output or b"").decode("utf-8", errors="replace")

    return exit_code, stdout


def _run_python_script(container: DockerContainer, stage: PipelineStage) -> tuple[int, str]:
    """Execute a pipeline stage's Python script inside the container.

    Uses the stage's *timeout* and resolves the script path via
    ``_script_path()``.
    """
    script_path = _script_path(stage)
    return _exec(container, f"python {script_path}", timeout=stage.timeout)


# ── Pipeline runner ───────────────────────────────────────────────────────────


def run_pipeline(
    container: DockerContainer, stages: tuple[PipelineStage, ...]
) -> int:
    """Execute stages sequentially, halting on first required-stage failure.

    Returns 0 on success, 1 on failure.
    """
    total = len(stages)
    failed_optional: list[str] = []

    for idx, stage in enumerate(stages, start=1):
        optional_tag = " [OPTIONAL]" if stage.optional else ""
        print(
            f"[{idx}/{total}] {stage.label} "
            f"({stage.script}){optional_tag} ..."
        )
        t0 = time.monotonic()
        exit_code, output = _run_python_script(container, stage)
        elapsed = time.monotonic() - t0

        if exit_code == 0:
            print(f"  ✓ PASS ({elapsed:.1f}s)")
        elif stage.optional:
            print(
                f"  ⚠ WARN — optional stage failed "
                f"(exit={exit_code}, {elapsed:.1f}s)"
            )
            failed_optional.append(stage.label)
            if output.strip():
                print(f"  Last output ({len(output)} bytes):")
                print(output[-2000:])
        else:
            print(f"  ✗ FAIL (exit={exit_code}, {elapsed:.1f}s)")
            print(
                f"\nPipeline halted — {stage.label} ({stage.script}) "
                f"failed with exit code {exit_code}."
            )
            if output.strip():
                print(f"Last output ({len(output)} bytes):")
                print(output[-2000:])
            return 1

    # ── Summary ────────────────────────────────────────────
    print("\n" + "=" * 60)
    if failed_optional:
        print(
            "All required stages passed. "
            f"Optional stage(s) skipped/failed: {', '.join(failed_optional)}"
        )
    else:
        print("All pipeline stages passed.")
    print("=" * 60)
    return 0


# ── Orchestrator entry point ─────────────────────────────────────────────────


def main() -> int:
    print("QA Pipeline Orchestrator starting...")
    container = create_container()
    try:
        print(f"Starting container ({CONTAINER_IMAGE})...")
        container.start()
        print("Container ready.")

        # Create required working directories inside the container.
        for dir_path in ("downloads", "processed", "staged"):
            exit_code, output = _exec(
                container,
                f"mkdir -p {CONTAINER_WORKSPACE}/tmp/pipeline-ci/{dir_path}",
            )
            if exit_code != 0:
                raise RuntimeError(
                    f"Failed to create {dir_path} dir (exit {exit_code}): "
                    f"{output[:300]}"
                )

        print("Installing dependencies...")
        exit_code, output = _exec(
            container,
            f"pip install -r {CONTAINER_WORKSPACE}/.github/scripts/requirements.txt",
        )
        if exit_code != 0:
            raise RuntimeError(
                f"pip install failed (exit {exit_code}): {output[:500]}"
            )
        print("Dependencies installed.")

        print()
        failed = run_pipeline(container, PIPELINE_STAGES)
        if failed:
            print("\nQA Pipeline FAILED.")
            return 1
        print("\nQA Pipeline PASSED.")
        return 0
    finally:
        print("\nTearing down container...")
        try:
            container.stop()
        except Exception as exc:
            print(f"Warning: container.stop() raised: {exc}")
        print("Container destroyed.")


if __name__ == "__main__":
    sys.exit(main())
