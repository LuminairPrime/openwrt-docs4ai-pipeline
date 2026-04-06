from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).with_name("global-customization-roots.json")


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _expand_user_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _default_backup_root() -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return Path.home() / ".claude" / "backups" / "cross-ide-skill-cleanup" / timestamp


def _copy_root(source_root: Path, backup_root: Path, dry_run: bool) -> str:
    if not source_root.exists():
        return f"SKIP missing {source_root}"

    target_root = backup_root / source_root.drive.replace(":", "") / source_root.relative_to(source_root.anchor)

    if dry_run:
        return f"DRY-RUN backup {source_root} -> {target_root}"

    target_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_root, target_root, dirs_exist_ok=True)
    return f"backed up {source_root} -> {target_root}"


def run_backup(output_root: Path, dry_run: bool) -> int:
    config = _load_config()
    messages: list[str] = []

    for root_string in config["user_managed_global_roots"]:
        messages.append(_copy_root(_expand_user_path(root_string), output_root, dry_run))

    for message in messages:
        print(message)

    print(f"completed {len(messages)} backup check(s)")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Back up user-managed machine-global skill, agent, and rule roots before cleanup."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=_default_backup_root(),
        help="Backup destination root. Defaults to a timestamped directory under ~/.claude/backups/.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned backup operations without copying files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_backup(output_root=args.output_root, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())