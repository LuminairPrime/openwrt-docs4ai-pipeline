import datetime
import json
import os
import secrets
from dataclasses import dataclass
from typing import cast


_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_RUN_STATE = os.path.join("tmp", "pipeline-run-state.json")
VALID_AI_MODES = {"skip", "stored", "generate"}


@dataclass(frozen=True)
class AiModeSettings:
    """Describe the normalized AI execution contract for one process."""

    mode: str
    skip_ai: bool
    write_ai: bool
    token: str | None
    token_source: str | None
    used_legacy_flags: bool


def _resolve_repo_path(raw_path: str) -> str:
    if os.path.isabs(raw_path):
        return raw_path
    return os.path.join(_REPO_ROOT, raw_path)


def _normalize_repo_relative(raw_path: str) -> str:
    absolute_path = os.path.abspath(_resolve_repo_path(raw_path))
    repo_root = os.path.abspath(_REPO_ROOT)

    try:
        if os.path.commonpath([repo_root, absolute_path]) == repo_root:
            return os.path.relpath(absolute_path, repo_root).replace("\\", "/")
    except ValueError:
        pass

    return os.path.normpath(raw_path).replace("\\", "/")


def _utc_now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_env_bool(environ: dict[str, str], name: str, default: bool) -> bool:
    """Parse a boolean-like environment variable using the repo's convention."""

    value = environ.get(name)
    if value is None:
        return default
    return value.strip().lower() == "true"


def _resolve_ai_token(environ: dict[str, str]) -> tuple[str | None, str | None]:
    """Return the preferred AI token and its source name when configured."""

    for env_name in ("LOCAL_DEV_TOKEN", "GITHUB_TOKEN"):
        token_value = environ.get(env_name, "").strip()
        if token_value:
            return token_value, env_name
    return None, None


def resolve_ai_mode_settings(
    environ: dict[str, str] | None = None,
) -> AiModeSettings:
    """Resolve AI_MODE and legacy flag compatibility into one normalized view."""

    env = dict(os.environ if environ is None else environ)
    raw_ai_mode = env.get("AI_MODE", "").strip().lower()
    used_legacy_flags = False

    if raw_ai_mode:
        if raw_ai_mode not in VALID_AI_MODES:
            valid_modes = ", ".join(sorted(VALID_AI_MODES))
            raise RuntimeError(f"Invalid AI_MODE value: {raw_ai_mode}. Expected one of: {valid_modes}.")
        mode = raw_ai_mode
    else:
        used_legacy_flags = "SKIP_AI" in env or "WRITE_AI" in env
        skip_ai = _read_env_bool(env, "SKIP_AI", True)
        if skip_ai:
            mode = "skip"
        else:
            write_ai = _read_env_bool(env, "WRITE_AI", True)
            mode = "generate" if write_ai else "stored"

    skip_ai = mode == "skip"
    write_ai = mode == "generate"
    token = None
    token_source = None
    if write_ai:
        token, token_source = _resolve_ai_token(env)

    return AiModeSettings(
        mode=mode,
        skip_ai=skip_ai,
        write_ai=write_ai,
        token=token,
        token_source=token_source,
        used_legacy_flags=used_legacy_flags,
    )


def _write_json_atomic(path: str, payload: dict[str, object]) -> None:
    absolute_path = _resolve_repo_path(path)
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    temp_path = f"{absolute_path}.tmp"

    with open(temp_path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")

    os.replace(temp_path, absolute_path)


def _read_json(path: str) -> dict[str, object] | None:
    absolute_path = _resolve_repo_path(path)
    if not os.path.isfile(absolute_path):
        return None

    try:
        with open(absolute_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    raw_payload = cast(dict[object, object], payload)
    normalized_payload: dict[str, object] = {}
    for key, value in raw_payload.items():
        if not isinstance(key, str):
            return None
        normalized_payload[key] = value

    return normalized_payload


def _read_state_file(path: str) -> str | None:
    payload = _read_json(path)
    if payload is None:
        return None

    pipeline_run_dir = payload.get("pipeline_run_dir")
    if not isinstance(pipeline_run_dir, str) or not pipeline_run_dir.strip():
        return None

    return os.path.normpath(pipeline_run_dir)


def _generate_and_save_new_run_dir() -> str:
    run_id = datetime.datetime.now(datetime.UTC).strftime("pipeline-%Y%m%d-%H%MUTC-") + secrets.token_hex(2)
    run_dir = os.path.join("tmp", run_id)
    _write_json_atomic(
        PIPELINE_RUN_STATE,
        {"pipeline_run_dir": _normalize_repo_relative(run_dir)},
    )
    return run_dir


def _resolve_pipeline_run_dir() -> str:
    env_run_dir = os.environ.get("PIPELINE_RUN_DIR")
    if env_run_dir:
        return os.path.normpath(env_run_dir)

    state_run_dir = _read_state_file(PIPELINE_RUN_STATE)
    if state_run_dir:
        return state_run_dir

    return _generate_and_save_new_run_dir()


PIPELINE_RUN_DIR = _resolve_pipeline_run_dir()
DOWNLOADS_DIR = os.path.normpath(
    os.environ.get("DOWNLOADS_DIR") or os.environ.get("WORKDIR") or os.path.join(PIPELINE_RUN_DIR, "downloads")
)
PROCESSED_DIR = os.path.normpath(os.environ.get("PROCESSED_DIR") or os.path.join(PIPELINE_RUN_DIR, "processed"))
STAGED_DIR = os.path.normpath(
    os.environ.get("STAGED_DIR") or os.environ.get("OUTDIR") or os.path.join(PIPELINE_RUN_DIR, "staged")
)
WORKDIR = DOWNLOADS_DIR
OUTDIR = STAGED_DIR
PACKAGES_DIR = os.path.join(STAGED_DIR, "packages")
RUN_RECORD_PATH = os.path.join(PIPELINE_RUN_DIR, "pipeline-run-record.json")

# Execution Flags & Quotas
SKIP_WIKI = os.environ.get("SKIP_WIKI", "false").lower() == "true"
AI_SETTINGS = resolve_ai_mode_settings()
AI_MODE = AI_SETTINGS.mode
SKIP_AI = AI_SETTINGS.skip_ai
WRITE_AI = AI_SETTINGS.write_ai
AI_TOKEN = AI_SETTINGS.token
AI_TOKEN_SOURCE = AI_SETTINGS.token_source
WIKI_MAX_PAGES = int(os.environ.get("WIKI_MAX_PAGES", "300"))
MAX_AI_FILES = int(os.environ.get("MAX_AI_FILES", "40"))
LLM_BUDGET_LIMIT = float(os.environ.get("LLM_BUDGET_LIMIT", "5.00").replace("$", ""))
VALIDATE_MODE = os.environ.get("VALIDATE_MODE", "hard")
MERMAID_INJECT = os.environ.get("MERMAID_INJECT", "true").lower() == "true"

# Token & Baseline Configs
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
LOCAL_DEV_TOKEN = os.environ.get("LOCAL_DEV_TOKEN", "")
TOKENIZER = os.environ.get("TOKENIZER", "cl100k_base")
DTS_GENERATE = os.environ.get("DTS_GENERATE", "true").lower() == "true"
BASELINE_SOURCE = os.environ.get("BASELINE_SOURCE", "github-release")

# Computed Paths
L1_RAW_WORKDIR = os.path.join(PROCESSED_DIR, "L1-raw")
L2_SEMANTIC_WORKDIR = os.path.join(PROCESSED_DIR, "L2-semantic")
REPO_MANIFEST_PATH = os.path.join(PROCESSED_DIR, "manifests", "repo-manifest.json")
CROSS_LINK_REGISTRY = os.path.join(PROCESSED_DIR, "manifests", "cross-link-registry.json")

# V5a Release Tree Configuration
RELEASE_TREE_DIR = os.path.join(STAGED_DIR, "release-tree")
SUPPORT_TREE_DIR = os.path.join(STAGED_DIR, "support-tree")

# V5a Public Output Name Constants
MODULE_MAP_FILENAME = "map.md"
MODULE_BUNDLED_REF_FILENAME = "bundled-reference.md"
MODULE_CHUNKED_REF_DIRNAME = "chunked-reference"
MODULE_TYPES_DIRNAME = "types"

# V5a Release Include Paths (relative to repo root)
RELEASE_INCLUDE_DIR = os.path.join(_REPO_ROOT, "static", "release-inputs", "release-include")
PAGES_INCLUDE_DIR = os.path.join(_REPO_ROOT, "static", "release-inputs", "pages-include")

# AI Summary Data Store
# Defaults to static/data/base/ and static/data/override/ relative to the repository root.
# Can be overridden by environment variables for non-standard layouts.
AI_DATA_BASE_DIR = os.environ.get(
    "AI_DATA_BASE_DIR",
    os.path.join(_REPO_ROOT, "static", "data", "base"),
)
AI_DATA_OVERRIDE_DIR = os.environ.get(
    "AI_DATA_OVERRIDE_DIR",
    os.path.join(_REPO_ROOT, "static", "data", "override"),
)


def _run_record_payload(status: str) -> dict[str, object]:
    existing_payload = _read_json(RUN_RECORD_PATH) or {}
    created_utc = existing_payload.get("created_utc")

    return {
        "schema_version": 1,
        "run_id": os.path.basename(os.path.normpath(PIPELINE_RUN_DIR)),
        "created_utc": created_utc if isinstance(created_utc, str) and created_utc else _utc_now_iso(),
        "status": status,
        "pipeline_run_dir": _normalize_repo_relative(PIPELINE_RUN_DIR),
    }


def _write_run_record(status: str) -> None:
    _write_json_atomic(RUN_RECORD_PATH, _run_record_payload(status))


def ensure_dirs() -> None:
    run_dir = _resolve_repo_path(PIPELINE_RUN_DIR)
    run_record_path = _resolve_repo_path(RUN_RECORD_PATH)
    run_dir_exists = os.path.isdir(run_dir)

    directories = [
        _resolve_repo_path(os.path.join("tmp", "logs")),
        run_dir,
        _resolve_repo_path(DOWNLOADS_DIR),
        _resolve_repo_path(os.path.join(DOWNLOADS_DIR, "repos")),
        _resolve_repo_path(os.path.join(DOWNLOADS_DIR, "wiki", "raw")),
        _resolve_repo_path(PROCESSED_DIR),
        _resolve_repo_path(L1_RAW_WORKDIR),
        _resolve_repo_path(L2_SEMANTIC_WORKDIR),
        _resolve_repo_path(os.path.join(PROCESSED_DIR, "manifests")),
        _resolve_repo_path(STAGED_DIR),
        _resolve_repo_path(RELEASE_TREE_DIR),
        _resolve_repo_path(SUPPORT_TREE_DIR),
        _resolve_repo_path(PACKAGES_DIR),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    if not run_dir_exists or not os.path.isfile(run_record_path):
        _write_run_record("running")


def mark_run_complete() -> None:
    _write_run_record("complete")


def mark_run_failed() -> None:
    _write_run_record("failed")
