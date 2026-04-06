from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LAYOUT_PATH = REPO_ROOT / "tools" / "agents-skills" / "skill-layout.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _directory_tree_hashes(root: Path) -> dict[Path, str]:
    return {
        path.relative_to(root): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _expected_skill_names(layout: dict) -> set[str]:
    expected: set[str] = set()

    for mirror_skills in layout["mirrors"].values():
        expected.update(mirror_skills)

    return expected


def _skill_directories(root: Path) -> set[str]:
    return {child.name for child in root.iterdir() if child.is_dir()}


def test_skill_layout_config_exists() -> None:
    assert LAYOUT_PATH.exists()


def test_canonical_root_exists() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    canonical_root = REPO_ROOT / layout["canonical_root"]
    assert canonical_root.exists()
    assert canonical_root.is_dir()


def test_mirror_skills_exist_in_canonical_root() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    canonical_root = REPO_ROOT / layout["canonical_root"]

    for mirror_skills in layout["mirrors"].values():
        for skill_name in mirror_skills:
            assert (canonical_root / skill_name / "SKILL.md").exists(), skill_name


def test_canonical_root_contains_only_curated_skill_set() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    canonical_root = REPO_ROOT / layout["canonical_root"]
    assert _skill_directories(canonical_root) == _expected_skill_names(layout)


def test_layout_paths_are_repo_relative() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    all_paths = [layout["canonical_root"], *layout["independent_roots"], *layout["mirrors"]]

    for relative_path in all_paths:
        path = Path(relative_path)
        assert not path.is_absolute(), relative_path
        assert ".." not in path.parts, relative_path


def test_mirror_roots_match_canonical_content() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    canonical_root = REPO_ROOT / layout["canonical_root"]

    for relative_mirror_root, mirror_skills in layout["mirrors"].items():
        mirror_root = REPO_ROOT / relative_mirror_root
        assert mirror_root.exists(), relative_mirror_root
        assert _skill_directories(mirror_root) == set(mirror_skills)

        for skill_name in mirror_skills:
            canonical_skill = canonical_root / skill_name
            mirror_skill = mirror_root / skill_name
            canonical_file = canonical_skill / "SKILL.md"
            mirror_file = mirror_skill / "SKILL.md"

            assert mirror_file.exists(), f"missing mirror: {relative_mirror_root}/{skill_name}"
            assert _sha256(mirror_file) == _sha256(canonical_file), skill_name
            assert _directory_tree_hashes(mirror_skill) == _directory_tree_hashes(
                canonical_skill
            ), skill_name


def test_independent_roots_are_not_used_as_mirrors() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    independent_roots = set(layout["independent_roots"])
    mirror_roots = set(layout["mirrors"])
    assert independent_roots.isdisjoint(mirror_roots)


def test_canonical_root_is_not_listed_as_a_mirror() -> None:
    layout = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    canonical_root = layout["canonical_root"]
    mirror_roots = set(layout["mirrors"])
    assert canonical_root not in mirror_roots