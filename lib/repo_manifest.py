from __future__ import annotations

import json
import os
import re
from collections.abc import Iterator
from typing import Any, cast

from lib import config


COMMIT_ENV_TO_MANIFEST_KEY = {
    "OPENWRT_COMMIT": "openwrt",
    "LUCI_COMMIT": "luci",
    "UCODE_COMMIT": "ucode",
}

SHORT_HASH_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")


class ManifestError(RuntimeError):
    pass


def validate_commit_hash(value: str | None, label: str = "commit") -> str:
    normalized = (value or "").strip()
    if not SHORT_HASH_RE.fullmatch(normalized):
        raise ManifestError(f"Invalid {label}: {value!r}")
    return normalized


def iter_manifest_paths(extra_paths: list[str] | None = None) -> Iterator[str]:
    seen: set[str] = set()
    candidates: list[str | None] = []

    if extra_paths:
        candidates.extend(extra_paths)

    candidates.extend(
        [
            config.REPO_MANIFEST_PATH,
            os.path.join(config.OUTDIR, "repo-manifest.json"),
        ]
    )

    for path in candidates:
        if not path:
            continue
        normalized = os.path.abspath(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        yield normalized


def load_manifest(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        raise ManifestError(f"Manifest file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except Exception as exc:
        raise ManifestError(f"Could not parse manifest {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise ManifestError(f"Manifest payload must be a JSON object: {path}")

    return cast(dict[str, Any], payload)


def find_manifest(extra_paths: list[str] | None = None) -> tuple[dict[str, Any], str]:
    for path in iter_manifest_paths(extra_paths):
        if os.path.isfile(path):
            return load_manifest(path), path
    raise ManifestError("repo-manifest.json not found in expected locations")


def resolve_commit_environment(
    env: dict[str, str | None] | None = None,
    extra_manifest_paths: list[str] | None = None,
) -> tuple[dict[str, str], str | None]:
    env_map = env if env is not None else os.environ
    resolved: dict[str, str | None] = {name: env_map.get(name) for name in COMMIT_ENV_TO_MANIFEST_KEY}
    manifest_path: str | None = None

    if any(not value for value in resolved.values()):
        try:
            manifest, manifest_path = find_manifest(extra_manifest_paths)
        except ManifestError:
            manifest = None

        if manifest is not None:
            for env_name, manifest_key in COMMIT_ENV_TO_MANIFEST_KEY.items():
                resolved[env_name] = resolved[env_name] or manifest.get(manifest_key)

    final: dict[str, str] = {}
    for env_name in COMMIT_ENV_TO_MANIFEST_KEY:
        val = resolved[env_name]
        final[env_name] = str(val) if val else "unknown"

    return final, manifest_path
