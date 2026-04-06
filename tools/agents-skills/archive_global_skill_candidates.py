from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("global-customization-roots.json")


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _expand_user_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _default_archive_root() -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return Path.home() / ".claude" / "archive" / "cross-ide-skill-cleanup" / timestamp


def _skill_names_for_profile(config: dict, profile_name: str) -> set[str]:
    try:
        keep_names = set(config["profiles"][profile_name]["keep_global_skill_names"])
    except KeyError as exc:
        raise ValueError(f"unknown profile: {profile_name}") from exc

    archive_names: set[str] = set()

    for skill_root in _skill_roots(config):
        if not skill_root.exists():
            continue

        for child in skill_root.iterdir():
            if not child.is_dir():
                continue
            if child.name in keep_names:
                continue
            archive_names.add(child.name)

    return archive_names


def _skill_roots(config: dict) -> list[Path]:
    roots: list[Path] = []

    for root_string in config["user_managed_global_roots"]:
        expanded_root = _expand_user_path(root_string)
        if expanded_root.name == "skills":
            roots.append(expanded_root)

    return roots


def _archive_target(source_skill: Path, archive_root: Path) -> Path:
    return archive_root / source_skill.drive.replace(":", "") / source_skill.relative_to(source_skill.anchor)


def _archive_skill(source_skill: Path, archive_root: Path, dry_run: bool) -> str:
    target_skill = _archive_target(source_skill, archive_root)

    if dry_run:
        return f"DRY-RUN archive {source_skill} -> {target_skill}"

    try:
        target_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_skill), str(target_skill))
    except (OSError, shutil.Error) as exc:
        return f"FAILED archive {source_skill}: {exc}"

    return f"archived {source_skill} -> {target_skill}"


def run_archive(archive_root: Path, dry_run: bool, profile_name: str | None) -> int:
    config = _load_config()
    archive_candidates = (
        _skill_names_for_profile(config, profile_name)
        if profile_name
        else set(config["archive_candidates"])
    )
    messages: list[str] = []

    for skill_root in _skill_roots(config):
        if not skill_root.exists():
            messages.append(f"SKIP missing {skill_root}")
            continue

        for skill_name in sorted(archive_candidates):
            source_skill = skill_root / skill_name
            if not source_skill.exists():
                continue
            messages.append(_archive_skill(source_skill, archive_root, dry_run))

    for message in messages:
        print(message)

    print(f"completed {len(messages)} archive operation(s)")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive explicit or profile-selected global skills from user-managed global skill roots."
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=_default_archive_root(),
        help="Archive destination root. Defaults to a timestamped directory under ~/.claude/archive/.",
    )
    parser.add_argument(
        "--profile",
        help="Archive every global skill not retained by the named profile from global-customization-roots.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned archive operations without moving directories.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_archive(
        archive_root=args.archive_root,
        dry_run=args.dry_run,
        profile_name=args.profile,
    )


if __name__ == "__main__":
    raise SystemExit(main())