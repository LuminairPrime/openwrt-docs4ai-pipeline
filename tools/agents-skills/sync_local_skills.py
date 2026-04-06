from __future__ import annotations

import argparse
import json
import stat
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).with_name("skill-layout.json")
FILE_ATTRIBUTE_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)


def _load_layout() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _resolve_repo_path(relative_path: str) -> Path:
    resolved = (REPO_ROOT / Path(relative_path)).resolve()

    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(
            f"path resolves outside repository root: {relative_path} -> {resolved}"
        ) from exc

    return resolved


def _is_reparse_point(path: Path) -> bool:
    if sys.platform != "win32" or not FILE_ATTRIBUTE_REPARSE_POINT:
        return False

    file_attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
    return bool(file_attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def _remove_path(target_path: Path) -> None:
    if _is_reparse_point(target_path):
        target_path.rmdir()
    elif target_path.is_symlink() or target_path.is_file():
        target_path.unlink()
    else:
        shutil.rmtree(target_path)


def _sync_skill(
    source_root: Path,
    target_root: Path,
    skill_name: str,
    dry_run: bool,
    force: bool,
) -> str:
    source_skill = source_root / skill_name
    target_skill = target_root / skill_name

    if not source_skill.exists():
        raise FileNotFoundError(f"missing canonical skill: {source_skill}")

    if dry_run:
        return f"DRY-RUN sync {skill_name} -> {target_root.relative_to(REPO_ROOT)}"

    if target_skill.exists():
        if not force:
            raise FileExistsError(
                f"refusing to overwrite existing mirror without --force: {target_skill}"
            )
        _remove_path(target_skill)

    shutil.copytree(source_skill, target_skill)
    return f"synced {skill_name} -> {target_root.relative_to(REPO_ROOT)}"


def _prune_mirror_root(
    target_root: Path,
    allowed_skill_names: set[str],
    dry_run: bool,
    force: bool,
) -> list[str]:
    messages: list[str] = []

    if not target_root.exists():
        return messages

    for child in sorted(target_root.iterdir(), key=lambda path: path.name.lower()):
        if not child.is_dir():
            continue
        if child.name in allowed_skill_names:
            continue
        if not force:
            raise FileExistsError(
                f"refusing to prune unmanaged mirror directory without --force: {child}"
            )
        if dry_run:
            messages.append(
                f"DRY-RUN prune {child.name} from {target_root.relative_to(REPO_ROOT)}"
            )
            continue
        _remove_path(child)
        messages.append(f"pruned {child.name} from {target_root.relative_to(REPO_ROOT)}")

    return messages


def run_sync(target_filter: set[str] | None, dry_run: bool, force: bool, prune: bool) -> int:
    layout = _load_layout()
    source_root = _resolve_repo_path(layout["canonical_root"])

    if not source_root.exists():
        raise FileNotFoundError(f"canonical root does not exist: {source_root}")

    messages: list[str] = []

    for relative_target, skill_names in layout["mirrors"].items():
        if target_filter and relative_target not in target_filter:
            continue

        target_root = _resolve_repo_path(relative_target)
        if not dry_run:
            target_root.mkdir(parents=True, exist_ok=True)

        for skill_name in skill_names:
            messages.append(_sync_skill(source_root, target_root, skill_name, dry_run, force))

        if prune:
            messages.extend(
                _prune_mirror_root(
                    target_root=target_root,
                    allowed_skill_names=set(skill_names),
                    dry_run=dry_run,
                    force=force,
                )
            )

    for message in messages:
        print(message)

    print(f"completed {len(messages)} sync operation(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync canonical repo-local skills into IDE-specific mirror roots."
    )
    parser.add_argument(
        "--target",
        action="append",
        help="Limit sync to one or more relative mirror roots from skill-layout.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned sync operations without changing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting existing mirror directories.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove unmanaged skill directories from mirror roots so they exactly match the curated set.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target_filter = set(args.target) if args.target else None
    return run_sync(
        target_filter=target_filter,
        dry_run=args.dry_run,
        force=args.force,
        prune=args.prune,
    )


if __name__ == "__main__":
    raise SystemExit(main())