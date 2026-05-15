# ruff: noqa: E402

from __future__ import annotations

import argparse
import importlib.metadata as importlib_metadata
import os
import shlex
import sys
import textwrap
import time
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENDORED_TESTCONTAINERS_CORE = PROJECT_ROOT / "vendors" / "testcontainers-python" / "core"
DEFAULT_IMAGE = "python:3.12-slim"
DEFAULT_MAX_AI_FILES = 40
QA_RESULTS_ROOT = PROJECT_ROOT / "tmp" / "ci" / "qa"
DEFAULT_WIKI_CACHE_DIR = QA_RESULTS_ROOT / "shared" / "wiki-cache"
CONTAINER_WORKSPACE = "/workspace"
FORWARDED_CONTAINER_ENV_NAMES = (
    "AI_VALIDATE_PAYLOAD",
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "HTTPS_PROXY",
    "HTTP_PROXY",
    "LOCAL_DEV_TOKEN",
    "NO_PROXY",
    "WIKI_MAX_PAGES",
    "WRITE_AI",
)
FRESH_ISOLATED_STAGE_IDS = {"01", "02a"}
REQUIRED_CLONE_DIR_NAMES = ("repo-ucode", "repo-luci", "repo-openwrt")
PIPELINE_SCRIPTS_TO_STAGE_08 = [
    "openwrt-docs4ai-01-clone-repos.py",
    "openwrt-docs4ai-02a-scrape-wiki.py",
    "openwrt-docs4ai-02b-scrape-ucode.py",
    "openwrt-docs4ai-02c-scrape-jsdoc.py",
    "openwrt-docs4ai-02d-scrape-core-packages.py",
    "openwrt-docs4ai-02e-scrape-example-packages.py",
    "openwrt-docs4ai-02f-scrape-procd-api.py",
    "openwrt-docs4ai-02g-scrape-uci-schemas.py",
    "openwrt-docs4ai-02h-scrape-hotplug-events.py",
    "openwrt-docs4ai-02i-ingest-cookbook.py",
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
]
PRE_UCODE_STAGE_IDS = {
    "01",
    "02a",
    "02b",
    "02c",
    "02d",
    "02e",
    "02f",
    "02g",
    "02h",
    "02i",
}

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if VENDORED_TESTCONTAINERS_CORE.is_dir() and str(VENDORED_TESTCONTAINERS_CORE) not in sys.path:
    sys.path.insert(0, str(VENDORED_TESTCONTAINERS_CORE))

os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")


def read_env_text(name: str, default: str | None = None) -> str | None:
    """Return a normalized environment variable value when present."""

    value = os.environ.get(name)
    if value is None:
        return default
    stripped = value.strip()
    return stripped if stripped else default


def read_env_int(name: str, default: int) -> int:
    """Parse an integer environment variable with a fallback."""

    raw_value = read_env_text(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError as exc:
        raise SystemExit(f"Invalid integer value for {name}: {raw_value}") from exc


def load_vendored_testcontainers_version() -> str:
    """Return the vendored Testcontainers version for metadata fallback."""

    pyproject_path = PROJECT_ROOT / "vendors" / "testcontainers-python" / "pyproject.toml"
    if not pyproject_path.is_file():
        return "vendored"

    with pyproject_path.open("rb") as handle:
        payload = tomllib.load(handle)

    project = payload.get("project", {})
    version = project.get("version")
    if isinstance(version, str) and version:
        return version.split("#", 1)[0].strip()
    return "vendored"


def patch_importlib_metadata_version() -> None:
    """Patch metadata lookup only when vendored Testcontainers needs it."""

    try:
        importlib_metadata.version("testcontainers")
        return
    except importlib_metadata.PackageNotFoundError:
        pass

    original_version = importlib_metadata.version
    vendored_version = load_vendored_testcontainers_version()

    def version_with_vendored_fallback(distribution_name: str) -> str:
        if distribution_name != "testcontainers":
            return original_version(distribution_name)
        try:
            return original_version(distribution_name)
        except importlib_metadata.PackageNotFoundError:
            return vendored_version

    importlib_metadata.version = version_with_vendored_fallback


patch_importlib_metadata_version()

from docker.errors import DockerException
from testcontainers.core.container import DockerContainer

from tests.support.runner_support import StageResult, StageSpec, build_summary, write_json
from tests.support.smoke_pipeline_support import select_pipeline_scripts


@dataclass(frozen=True)
class ContainerLayout:
    """Describe the host-mounted directories used by the QA container."""

    workspace: str
    pipeline_run_dir: str
    downloads_dir: str
    processed_dir: str
    staged_dir: str
    ai_data_base_dir: str
    ai_data_override_dir: str
    wiki_cache_dir: str
    ucode_bin_dir: str
    ucode_lib_dir: str


@dataclass(frozen=True)
class CommandOutcome:
    """Capture the result of a single container exec command."""

    exit_code: int
    output: str


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line interface for the QA orchestrator."""

    parser = argparse.ArgumentParser(
        description=("Run OpenWrt docs pipeline stages 01 through 08 in an ephemeral Linux container.")
    )
    parser.add_argument(
        "--result-root",
        type=str,
        default=read_env_text("QA_RESULT_ROOT"),
        help="Optional output directory override for QA logs and summaries.",
    )
    parser.add_argument(
        "--run-ai",
        action="store_true",
        help="Enable the cache-backed AI stage instead of forcing SKIP_AI=true.",
    )
    parser.add_argument(
        "--skip-wiki",
        action="store_true",
        help="Pass SKIP_WIKI=true into the containerized pipeline run.",
    )
    parser.add_argument(
        "--skip-buildroot",
        action="store_true",
        help="Pass SKIP_BUILDROOT=true into the containerized pipeline run.",
    )
    parser.add_argument(
        "--max-ai-files",
        type=int,
        default=read_env_int("QA_MAX_AI_FILES", DEFAULT_MAX_AI_FILES),
        help="Forward MAX_AI_FILES to the optional AI stage.",
    )
    parser.add_argument(
        "--only-stage",
        type=str,
        default=None,
        help=(
            "Optional stage id or exact script name to run. Fresh isolated runs "
            "are supported for stage 01 and 02a; later selectors require "
            "--result-root pointing at an existing QA bundle."
        ),
    )
    parser.add_argument(
        "--image",
        type=str,
        default=read_env_text("QA_CONTAINER_IMAGE", DEFAULT_IMAGE),
        help="Container image used for the Linux QA environment.",
    )
    parser.add_argument(
        "--wiki-cache-dir",
        type=str,
        default=read_env_text("QA_WIKI_CACHE_DIR"),
        help=("Persistent wiki cache directory. Defaults to tmp/ci/qa/shared/wiki-cache inside the repository."),
    )
    return parser


def resolve_repo_subdir(
    raw_path: str | None,
    *,
    default: Path,
    allowed_root: Path,
    label: str,
) -> Path:
    """Resolve a repository-local path and ensure it stays inside the allowed root."""

    if raw_path:
        candidate = Path(raw_path)
        resolved = candidate if candidate.is_absolute() else PROJECT_ROOT / candidate
    else:
        resolved = default

    resolved = resolved.resolve(strict=False)
    allowed_root_resolved = allowed_root.resolve(strict=False)
    try:
        resolved.relative_to(allowed_root_resolved)
    except ValueError as exc:
        raise SystemExit(
            f"The {label} must stay inside {allowed_root_resolved.relative_to(PROJECT_ROOT).as_posix()} "
            "so the container can access it through the workspace bind mount."
        ) from exc

    return resolved


def resolve_result_dir(result_root: str | None) -> Path:
    """Resolve the QA result directory inside the repository QA bundle root."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    resolved = resolve_repo_subdir(
        result_root,
        default=QA_RESULTS_ROOT / timestamp,
        allowed_root=QA_RESULTS_ROOT,
        label="QA result directory",
    )

    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def resolve_wiki_cache_dir(wiki_cache_dir: str | None) -> Path:
    """Resolve the shared wiki cache directory inside the repository."""

    resolved = resolve_repo_subdir(
        wiki_cache_dir,
        default=DEFAULT_WIKI_CACHE_DIR,
        allowed_root=PROJECT_ROOT,
        label="wiki cache directory",
    )
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def build_container_layout(result_dir: Path, wiki_cache_dir: Path) -> ContainerLayout:
    """Map the repository result directory to in-container pipeline paths."""

    relative_result_dir = result_dir.relative_to(PROJECT_ROOT)
    container_result_dir = Path(CONTAINER_WORKSPACE) / relative_result_dir.as_posix()
    relative_wiki_cache_dir = wiki_cache_dir.relative_to(PROJECT_ROOT)
    pipeline_run_dir = container_result_dir / "pipeline-run"
    downloads_dir = pipeline_run_dir / "downloads"
    processed_dir = pipeline_run_dir / "processed"
    staged_dir = pipeline_run_dir / "staged"
    ai_data_root = pipeline_run_dir / "ai-data"
    ucode_install_dir = downloads_dir / "repo-ucode" / "build-install"
    return ContainerLayout(
        workspace=CONTAINER_WORKSPACE,
        pipeline_run_dir=pipeline_run_dir.as_posix(),
        downloads_dir=downloads_dir.as_posix(),
        processed_dir=processed_dir.as_posix(),
        staged_dir=staged_dir.as_posix(),
        ai_data_base_dir=(ai_data_root / "base").as_posix(),
        ai_data_override_dir=(ai_data_root / "override").as_posix(),
        wiki_cache_dir=(Path(CONTAINER_WORKSPACE) / relative_wiki_cache_dir.as_posix()).as_posix(),
        ucode_bin_dir=(ucode_install_dir / "bin").as_posix(),
        ucode_lib_dir=(ucode_install_dir / "lib").as_posix(),
    )


def build_container_env(
    layout: ContainerLayout,
    *,
    run_ai: bool,
    skip_wiki: bool,
    skip_buildroot: bool,
    max_ai_files: int,
) -> dict[str, str]:
    """Build the environment contract mirrored from GitHub Actions."""

    env = {
        "PIPELINE_RUN_DIR": layout.pipeline_run_dir,
        "WORKDIR": layout.downloads_dir,
        "DOWNLOADS_DIR": layout.downloads_dir,
        "PROCESSED_DIR": layout.processed_dir,
        "STAGED_DIR": layout.staged_dir,
        "OUTDIR": layout.staged_dir,
        "AI_DATA_BASE_DIR": layout.ai_data_base_dir,
        "AI_DATA_OVERRIDE_DIR": layout.ai_data_override_dir,
        "CI": "true",
        "SKIP_AI": "false" if run_ai else "true",
        "SKIP_WIKI": "true" if skip_wiki else "false",
        "SKIP_BUILDROOT": "true" if skip_buildroot else "false",
        "MAX_AI_FILES": str(max_ai_files),
        "VALIDATE_MODE": "hard",
        "PYTHONUNBUFFERED": "1",
        "DEBIAN_FRONTEND": "noninteractive",
    }
    for env_name in FORWARDED_CONTAINER_ENV_NAMES:
        env_value = read_env_text(env_name)
        if env_value is not None:
            env[env_name] = env_value
    return env


def build_stage_specs(only_stage: str | None) -> list[StageSpec]:
    """Translate the selected pipeline scripts into execution specs."""

    try:
        selected_scripts = select_pipeline_scripts(PIPELINE_SCRIPTS_TO_STAGE_08, only_stage)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    return [
        StageSpec(
            label=script_name.removeprefix("openwrt-docs4ai-").removesuffix(".py"),
            slug=script_name.removeprefix("openwrt-docs4ai-").removesuffix(".py"),
            command=["python", f".github/scripts/{script_name}"],
        )
        for script_name in selected_scripts
    ]


def build_wiki_cache_restore_script(layout: ContainerLayout) -> str:
    """Create the shell snippet that restores the shared wiki cache into the run workspace."""

    downloads_cache_dir = Path(layout.downloads_dir) / ".cache"
    return textwrap.dedent(
        f"""
        mkdir -p {shlex.quote(layout.wiki_cache_dir)} {shlex.quote(downloads_cache_dir.as_posix())}
        find {shlex.quote(downloads_cache_dir.as_posix())} -mindepth 1 -exec rm -rf {{}} +
        tar -C {shlex.quote(layout.wiki_cache_dir)} -cf - . | tar -C {shlex.quote(downloads_cache_dir.as_posix())} -xf -
        """
    ).strip()


def build_wiki_cache_sync_script(layout: ContainerLayout) -> str:
    """Create the shell snippet that persists the run wiki cache back to the shared cache."""

    downloads_cache_dir = Path(layout.downloads_dir) / ".cache"
    return textwrap.dedent(
        f"""
        set -euo pipefail
        mkdir -p {shlex.quote(layout.wiki_cache_dir)}
        if [ -d {shlex.quote(downloads_cache_dir.as_posix())} ]; then
          find {shlex.quote(layout.wiki_cache_dir)} -mindepth 1 -exec rm -rf {{}} +
          tar -C {shlex.quote(downloads_cache_dir.as_posix())} -cf - . | tar -C {shlex.quote(layout.wiki_cache_dir)} -xf -
        fi
        """
    ).strip()


def ensure_isolated_stage_inputs(stage_specs: Sequence[StageSpec], result_dir: Path) -> None:
    """Reject isolated stage selectors that lack prerequisite inputs in the selected bundle."""

    if not stage_specs:
        return

    if len(stage_specs) == 1 and stage_specs[0].slug.split("-", 1)[0] in FRESH_ISOLATED_STAGE_IDS:
        return

    pipeline_run_dir = result_dir / "pipeline-run"
    downloads_dir = pipeline_run_dir / "downloads"
    processed_dir = pipeline_run_dir / "processed"
    staged_dir = pipeline_run_dir / "staged"
    missing_paths: list[str] = []
    prerequisite_tier = max(get_isolated_stage_prerequisite_tier(spec) for spec in stage_specs)

    if prerequisite_tier >= 1:
        if not (downloads_dir / "repo-manifest.json").is_file():
            missing_paths.append("pipeline-run/downloads/repo-manifest.json")
        for repo_dir_name in REQUIRED_CLONE_DIR_NAMES:
            if not (downloads_dir / repo_dir_name).is_dir():
                missing_paths.append(f"pipeline-run/downloads/{repo_dir_name}/")
    if prerequisite_tier >= 2 and not (processed_dir / "L1-raw").is_dir():
        missing_paths.append("pipeline-run/processed/L1-raw/")
    if prerequisite_tier >= 3 and not (processed_dir / "L2-semantic").is_dir():
        missing_paths.append("pipeline-run/processed/L2-semantic/")
    if prerequisite_tier >= 4 and not (staged_dir / "release-tree").is_dir():
        missing_paths.append("pipeline-run/staged/release-tree/")

    if not missing_paths:
        return

    missing_text = ", ".join(missing_paths)
    raise SystemExit(
        "Fresh isolated runs are supported only for a single 01 or 02a stage. "
        f"This selector requires an existing QA bundle via --result-root containing: {missing_text}"
    )


def get_isolated_stage_prerequisite_tier(spec: StageSpec) -> int:
    """Return the prerequisite tier needed to run the selected stage in isolation."""

    stage_id = spec.slug.split("-", 1)[0]
    if stage_id in FRESH_ISOLATED_STAGE_IDS:
        return 0
    if stage_id.startswith("02"):
        return 1
    if stage_id == "03":
        return 2
    if stage_id == "04" or stage_id.startswith("05"):
        return 3
    return 4


def build_bootstrap_script(layout: ContainerLayout) -> str:
    """Create the shell script that prepares the Linux container."""

    return textwrap.dedent(
        f"""
        set -euo pipefail
        apt-get update -qq
        apt-get install -y -qq \
          build-essential \
          cmake \
          git \
          libjson-c-dev \
          nodejs \
          npm \
          pandoc \
          pkg-config
        python -m pip install --upgrade pip
        python -m pip install -r .github/scripts/requirements.txt
        npm install -g jsdoc-to-markdown@9.1.1
        mkdir -p \
          {shlex.quote(layout.pipeline_run_dir)} \
          {shlex.quote(layout.downloads_dir)} \
          {shlex.quote(layout.processed_dir)} \
          {shlex.quote(layout.staged_dir)} \
                    {shlex.quote(layout.wiki_cache_dir)} \
          {shlex.quote(layout.ai_data_base_dir)} \
          {shlex.quote(layout.ai_data_override_dir)}
                {build_wiki_cache_restore_script(layout)}
        """
    ).strip()


def build_ucode_script(layout: ContainerLayout) -> str:
    """Create the shell script that mirrors the CI ucode host build."""

    repo_ucode_dir = Path(layout.downloads_dir) / "repo-ucode"
    build_host_dir = repo_ucode_dir / "build-host"
    install_dir = repo_ucode_dir / "build-install"
    return textwrap.dedent(
        f"""
        set -euo pipefail
        cmake -S {shlex.quote(repo_ucode_dir.as_posix())} \
          -B {shlex.quote(build_host_dir.as_posix())} \
          -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_INSTALL_PREFIX={shlex.quote(install_dir.as_posix())} \
          -DDEBUG_SUPPORT=OFF \
          -DFS_SUPPORT=OFF \
          -DIO_SUPPORT=OFF \
          -DMATH_SUPPORT=OFF \
          -DUBUS_SUPPORT=OFF \
          -DUCI_SUPPORT=OFF \
          -DRTNL_SUPPORT=OFF \
          -DNL80211_SUPPORT=OFF \
          -DRESOLV_SUPPORT=OFF \
          -DSTRUCT_SUPPORT=OFF \
          -DULOOP_SUPPORT=OFF \
          -DLOG_SUPPORT=OFF \
          -DSOCKET_SUPPORT=OFF \
          -DZLIB_SUPPORT=OFF \
          -DDIGEST_SUPPORT=OFF \
          -DDIGEST_SUPPORT_EXTENDED=OFF
        cmake --build {shlex.quote(build_host_dir.as_posix())} --parallel
        cmake --install {shlex.quote(build_host_dir.as_posix())}
        """
    ).strip()


def build_stage_script(spec: StageSpec, layout: ContainerLayout) -> str:
    """Create the per-stage shell command executed inside the container."""

    command = shlex.join(spec.command)
    return textwrap.dedent(
        f"""
        set -euo pipefail
        export PATH={shlex.quote(layout.ucode_bin_dir)}:$PATH
        export LD_LIBRARY_PATH={shlex.quote(layout.ucode_lib_dir)}:${{LD_LIBRARY_PATH:-}}
        mkdir -p \
          {shlex.quote(layout.pipeline_run_dir)} \
          {shlex.quote(layout.downloads_dir)} \
          {shlex.quote(layout.processed_dir)} \
          {shlex.quote(layout.staged_dir)}
        {command}
        """
    ).strip()


def write_command_log(
    log_path: Path,
    *,
    title: str,
    command: str,
    outcome: CommandOutcome,
) -> None:
    """Persist a single container command transcript to disk."""

    body = f"TITLE: {title}\nCOMMAND: {command}\n\nOUTPUT:\n{outcome.output}\nEXIT CODE: {outcome.exit_code}\n"
    log_path.write_text(body, encoding="utf-8")


def exec_in_container(container: DockerContainer, shell_script: str) -> CommandOutcome:
    """Run a shell command inside the QA container."""

    result = container.exec(["bash", "-lc", shell_script])
    output = result.output.decode("utf-8", errors="replace")
    return CommandOutcome(exit_code=result.exit_code, output=output)


def run_support_command(
    container: DockerContainer,
    *,
    title: str,
    shell_script: str,
    log_path: Path,
) -> CommandOutcome:
    """Run a bootstrap or support command and save its transcript."""

    print(title)
    outcome = exec_in_container(container, shell_script)
    write_command_log(log_path, title=title, command=shell_script, outcome=outcome)
    if outcome.output:
        print(outcome.output, end="" if outcome.output.endswith("\n") else "\n")
    print(f"    Exit code: {outcome.exit_code}")
    return outcome


def stage_requires_ucode_build(spec: StageSpec) -> bool:
    """Return True when the stage depends on the CI-style ucode host build."""

    stage_id = spec.slug.split("-", 1)[0]
    return stage_id not in PRE_UCODE_STAGE_IDS


def run_stage_specs_in_container(
    container: DockerContainer,
    stage_specs: Sequence[StageSpec],
    result_dir: Path,
    layout: ContainerLayout,
) -> tuple[list[StageResult], CommandOutcome | None]:
    """Execute the selected pipeline stages sequentially inside Docker."""

    results: list[StageResult] = []
    ucode_outcome: CommandOutcome | None = None

    for index, spec in enumerate(stage_specs, start=1):
        if ucode_outcome is None and stage_requires_ucode_build(spec):
            ucode_log = result_dir / "00-ucode-build.txt"
            ucode_outcome = run_support_command(
                container,
                title="[bootstrap] Build ucode validation binary",
                shell_script=build_ucode_script(layout),
                log_path=ucode_log,
            )
            if ucode_outcome.exit_code != 0:
                break

        log_file = result_dir / f"{index:02d}-{spec.slug}.txt"
        shell_script = build_stage_script(spec, layout)
        print(f"[{index}] {spec.label}")
        print(f"    Log: {log_file}")
        started = time.time()
        outcome = exec_in_container(container, shell_script)
        duration_seconds = round(time.time() - started, 1)
        write_command_log(log_file, title=spec.label, command=shell_script, outcome=outcome)
        if outcome.output:
            print(outcome.output, end="" if outcome.output.endswith("\n") else "\n")
        status = "PASS" if outcome.exit_code == 0 else "FAIL"
        print(f"    Result: {status} ({duration_seconds:.1f}s)")
        results.append(
            StageResult(
                index=index,
                label=spec.label,
                slug=spec.slug,
                command=spec.command,
                log_file=str(log_file),
                exit_code=outcome.exit_code,
                status=status,
                duration_seconds=duration_seconds,
            )
        )
        if outcome.exit_code != 0:
            break

    return results, ucode_outcome


def qa_success(
    bootstrap_outcome: CommandOutcome,
    ucode_outcome: CommandOutcome | None,
    wiki_cache_outcome: CommandOutcome | None,
    results: Sequence[StageResult],
) -> bool:
    """Return True only when bootstrap and every executed stage succeed."""

    if bootstrap_outcome.exit_code != 0:
        return False
    if ucode_outcome is not None and ucode_outcome.exit_code != 0:
        return False
    if wiki_cache_outcome is not None and wiki_cache_outcome.exit_code != 0:
        return False
    return bool(results) and all(result.exit_code == 0 for result in results)


def create_container(image: str, env: dict[str, str]) -> DockerContainer:
    """Create the long-lived container used for the staged QA run."""

    return (
        DockerContainer(image)
        .with_volume_mapping(PROJECT_ROOT, CONTAINER_WORKSPACE, "rw")
        .with_envs(**env)
        .with_command(["bash", "-lc", "while true; do sleep 3600; done"])
        .with_kwargs(working_dir=CONTAINER_WORKSPACE)
    )


def write_summary_file(
    result_dir: Path,
    *,
    args: argparse.Namespace,
    layout: ContainerLayout,
    bootstrap_outcome: CommandOutcome,
    ucode_outcome: CommandOutcome | None,
    wiki_cache_outcome: CommandOutcome | None,
    results: Sequence[StageResult],
) -> None:
    """Persist a machine-readable QA summary for the current run."""

    payload = build_summary(
        results,
        kind="qa",
        image=args.image,
        only_stage=args.only_stage,
        run_ai=args.run_ai,
        skip_wiki=args.skip_wiki,
        skip_buildroot=args.skip_buildroot,
        max_ai_files=args.max_ai_files,
        pipeline_run_dir=layout.pipeline_run_dir,
        bootstrap={
            "exit_code": bootstrap_outcome.exit_code,
            "log_file": str(result_dir / "00-bootstrap.txt"),
        },
        wiki_cache=(
            {
                "directory": layout.wiki_cache_dir,
                "exit_code": wiki_cache_outcome.exit_code,
                "log_file": str(result_dir / "00-wiki-cache-sync.txt"),
            }
            if wiki_cache_outcome is not None
            else {"directory": layout.wiki_cache_dir}
        ),
        ucode_build=(
            {
                "exit_code": ucode_outcome.exit_code,
                "log_file": str(result_dir / "00-ucode-build.txt"),
            }
            if ucode_outcome is not None
            else None
        ),
        success=qa_success(bootstrap_outcome, ucode_outcome, wiki_cache_outcome, results),
    )
    write_json(result_dir / "summary.json", payload)


def main() -> int:
    """Run the QA pipeline inside an ephemeral Linux container."""

    args = build_parser().parse_args()
    result_dir = resolve_result_dir(args.result_root)
    wiki_cache_dir = resolve_wiki_cache_dir(args.wiki_cache_dir)
    layout = build_container_layout(result_dir, wiki_cache_dir)
    container_env = build_container_env(
        layout,
        run_ai=args.run_ai,
        skip_wiki=args.skip_wiki,
        skip_buildroot=args.skip_buildroot,
        max_ai_files=args.max_ai_files,
    )
    stage_specs = build_stage_specs(args.only_stage)
    if args.only_stage is not None:
        ensure_isolated_stage_inputs(stage_specs, result_dir)

    try:
        with create_container(args.image, container_env) as container:
            bootstrap_outcome = run_support_command(
                container,
                title="[bootstrap] Install Linux QA dependencies",
                shell_script=build_bootstrap_script(layout),
                log_path=result_dir / "00-bootstrap.txt",
            )
            if bootstrap_outcome.exit_code != 0:
                write_summary_file(
                    result_dir,
                    args=args,
                    layout=layout,
                    bootstrap_outcome=bootstrap_outcome,
                    ucode_outcome=None,
                    wiki_cache_outcome=None,
                    results=[],
                )
                return 1

            results, ucode_outcome = run_stage_specs_in_container(container, stage_specs, result_dir, layout)
            wiki_cache_outcome = run_support_command(
                container,
                title="[cache] Persist shared wiki cache",
                shell_script=build_wiki_cache_sync_script(layout),
                log_path=result_dir / "00-wiki-cache-sync.txt",
            )
    except DockerException as exc:
        raise SystemExit(
            "Docker is required for `mise run qa`. Start Docker Desktop or the configured daemon, then rerun the task."
        ) from exc

    write_summary_file(
        result_dir,
        args=args,
        layout=layout,
        bootstrap_outcome=bootstrap_outcome,
        ucode_outcome=ucode_outcome,
        wiki_cache_outcome=wiki_cache_outcome,
        results=results,
    )
    return 0 if qa_success(bootstrap_outcome, ucode_outcome, wiki_cache_outcome, results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
