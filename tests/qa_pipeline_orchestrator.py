"""QA Pipeline Orchestrator — mirrors GitHub Actions CI locally via testcontainers.

Uses testcontainers-python to spin up an ephemeral Linux container matching the
GitHub Actions runner image, bind-mount the project directory, inject CI
environment variables, and sequentially execute pipeline scripts 01 through 08
with exit-code validation and guaranteed teardown.
"""

from __future__ import annotations

import sys
import time
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

# Pipeline scripts executed sequentially, matching GitHub Actions CI order.
PIPELINE_SCRIPTS: list[str] = [
    ".github/scripts/openwrt-docs4ai-01-clone-repos.py",
    ".github/scripts/openwrt-docs4ai-02a-scrape-wiki.py",
    ".github/scripts/openwrt-docs4ai-02b-scrape-ucode.py",
    ".github/scripts/openwrt-docs4ai-02c-scrape-jsdoc.py",
    ".github/scripts/openwrt-docs4ai-02d-scrape-core-packages.py",
    ".github/scripts/openwrt-docs4ai-02e-scrape-example-packages.py",
    ".github/scripts/openwrt-docs4ai-02f-scrape-procd-api.py",
    ".github/scripts/openwrt-docs4ai-02g-scrape-uci-schemas.py",
    ".github/scripts/openwrt-docs4ai-02h-scrape-hotplug-events.py",
    ".github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py",
    ".github/scripts/openwrt-docs4ai-03-normalize-semantic.py",
    ".github/scripts/openwrt-docs4ai-04-generate-ai-summaries.py",
    ".github/scripts/openwrt-docs4ai-05a-assemble-references.py",
    ".github/scripts/openwrt-docs4ai-05b-generate-agents-and-readme.py",
    ".github/scripts/openwrt-docs4ai-05c-generate-ucode-ide-schemas.py",
    ".github/scripts/openwrt-docs4ai-05d-generate-api-drift-changelog.py",
    ".github/scripts/openwrt-docs4ai-05e-generate-luci-dts.py",
    ".github/scripts/openwrt-docs4ai-06-generate-llm-routing-indexes.py",
    ".github/scripts/openwrt-docs4ai-07-generate-web-index.py",
    ".github/scripts/openwrt-docs4ai-08-validate-output.py",
]

EXEC_TIMEOUT = 600  # seconds per pipeline script


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


def _exec(container: DockerContainer, cmd: str, timeout: int = EXEC_TIMEOUT) -> tuple[int, str]:
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


def _run_python_script(container: DockerContainer, script_path: str) -> tuple[int, str]:
    """Execute a Python script inside the container.

    *script_path* is treated as relative to the project root and resolved
    to an absolute container path.
    """
    abs_path = f"{CONTAINER_WORKSPACE}/{script_path}"
    return _exec(container, f"python {abs_path}")


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

        total = len(PIPELINE_SCRIPTS)
        for idx, script in enumerate(PIPELINE_SCRIPTS, start=1):
            name = Path(script).name
            print(f"[{idx}/{total}] Running {name} ...")
            t0 = time.monotonic()
            exit_code, output = _run_python_script(container, script)
            elapsed = time.monotonic() - t0

            if exit_code == 0:
                print(f"  ✓ PASS ({elapsed:.1f}s)")
            else:
                print(f"  ✗ FAIL (exit={exit_code}, {elapsed:.1f}s)")
                print(f"\nPipeline halted — {name} failed with exit code {exit_code}.")
                if output.strip():
                    print(f"Last output ({len(output)} bytes):")
                    # Print tail of output (last 2000 chars) for diagnostics.
                    print(output[-2000:])
                return 1

        # ── Summary ────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("All pipeline scripts passed.")
        print("=" * 60)
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
