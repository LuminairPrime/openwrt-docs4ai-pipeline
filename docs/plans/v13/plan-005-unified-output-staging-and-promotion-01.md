# Plan-005: Unified Output Staging And Promotion (v01)

## Status

Proposed (2026-03-28)

Supersedes: `plan-005-unified-output-staging-and-promotion-00.md`

---

## Purpose

Refactor the pipeline so ad hoc local runs and GitHub Actions use the same
scratch-first output model, the same explicit promotion model, and the same
cross-platform file-tree sync logic.

This plan exists because the project currently mixes two different output
contracts:

- ad hoc local script runs default `OUTDIR` to `openwrt-condensed-docs/`
- hosted GitHub Actions runs override `OUTDIR` to `staging/` and promote later
- local smoke runners already use isolated scratch output trees under `tmp/`

That split is survivable, but it is not clean. It creates two mental models for
maintainers and makes the unsafe one the default for direct local work.

The goal of this plan is to make the safe model the default everywhere without
renaming the public contract or changing the published release-tree layout.

---

## Problem Summary

The project has one correct architectural idea already in production: generate
into scratch, validate scratch, then promote scratch into the tracked publish
tree only after the output is known-good.

GitHub Actions already follows that pattern. Direct local script execution does
not.

### Current divergence to remove

| Execution path | `WORKDIR` role | `OUTDIR` role | Promotion behavior | Safety level |
| --- | --- | --- | --- | --- |
| Direct local script run | scratch | `openwrt-condensed-docs/` by default | implicit because generation writes straight into tracked tree | lowest |
| Local smoke runner | scratch temp tree | scratch temp tree | none unless a test chooses to promote | high |
| Hosted CI process job | scratch | `${workspace}/staging` | explicit in deploy job | high |
| Hosted CI deploy job | n/a | consumes staged artifact | explicit `staging -> openwrt-condensed-docs/` mirror | high but shell-specific |

### Why this matters

The earlier cookbook-only regeneration incident was not caused by cookbook
content, module naming, or schema naming. It was caused by output-role drift.
The same logical output tree was serving as:

1. the canonical tracked generated corpus
2. the local generation target
3. the local validation target

That is the wrong default. A tracked generated corpus can be a promotion target
and an inspection surface, but it should not also be the default scratch output
root for destructive whole-tree pipeline stages.

---

## Goals

1. Make scratch-first generation the default for both ad hoc local runs and
   hosted CI runs.
2. Preserve the existing publish contract and path names:
   `openwrt-condensed-docs/`, `release-tree/`, `support-tree/`, `L1-raw/`, and
   `L2-semantic/` all stay.
3. Replace shell-specific source-repo promotion with one shared Python tree-sync
   implementation.
4. Keep the strict-subset fail-fast guards in `03` and `05a` as the first local
   safety line.
5. Keep local smoke tests isolated and scratch-based.
6. Make the delivery path more uniform by reusing the same Python sync helper
   for other workflow mirror operations where practical.
7. Avoid Windows/Linux behavior branches. Path inputs may differ; logic must not.

---

## Non-Goals

1. Do not rename `openwrt-condensed-docs/`.
2. Do not rename `release-tree/`, `support-tree/`, `L1-raw/`, or
   `L2-semantic/`.
3. Do not change the public `release-tree/` contract.
4. Do not change cookbook module purpose, frontmatter schema, or release-tree
   filenames as part of this refactor.
5. Do not collapse smoke-test isolation into one shared repo-root staging tree.
   Smoke runners should remain temp-tree-based.
6. Do not introduce concurrent-run safety. Single-writer semantics are assumed
   for all execution paths. Concurrent local script invocations writing to
   `staging/` are not a supported pattern, same as they are not supported today
   when writing to `openwrt-condensed-docs/`.

---

## Locked Decisions

### D1: `openwrt-condensed-docs/` becomes publish-only by contract

It remains committed, inspectable, and promotable, but it is no longer the
default `OUTDIR` for direct local script execution.

### D2: `staging/` becomes the canonical repo-root scratch output for ad hoc runs

This is the least risky unification path because:

- the workflow already uses `${workspace}/staging`
- `.gitignore` already ignores `staging/` (line 5)
- the workflow artifact and contract naming already use "staging"
- this minimizes churn compared with inventing a new scratch root name

This means:

- default local ad hoc `OUTDIR` becomes `staging`
- default hosted CI `OUTDIR` remains `staging`
- local smoke runners may still use temp directories because they are test
  harnesses, not maintainer publish targets

### D3: Local smoke runners stay temp-based

The local smoke runners already do the right thing: they create isolated temp
trees, set `WORKDIR` and `OUTDIR` explicitly via `build_env(workdir, outdir)` in
`tests/support/smoke_pipeline_support.py`, and never depend on the tracked
publish root.

Do not "unify" by making smoke scripts write to repo-root `staging/`.
That would reduce test isolation and make the test harness worse.

The unification target is the production contract, not the internal temp-path
choices of the test harness.

### D4: Promotion becomes explicit and Python-driven everywhere possible

The project should stop treating `rsync` as the canonical promotion contract for
the source repo tree. One Python sync implementation should define the behavior.

Shell steps may still invoke Python, but the tree-copy semantics must live in a
shared library and tool under version control.

### D5: Source-repo promotion and external delivery mirrors use the same sync helper

The first required consumer is:

- `staging/ -> openwrt-condensed-docs/`

The same helper should then be reused for:

- `publish_root -> gh-pages` worktree (mirror with `.git` exclusion)
- `release-tree/ -> distribution zip root` (mirror without exclusions)
- `release-tree/ -> external corpus repo` (mirror with `.git` exclusion)
- `release-tree/ -> external pages repo` (mirror with `.git` exclusion,
  **then** additive overlay of `pages-include/`)

That keeps file-tree mutation semantics uniform across the whole delivery path.

### D6: Promotion helper preflight is small and specific

Do not duplicate the whole validator in the promotion helper.

Stage `08` remains the authoritative validation gate.
The promotion helper should only enforce a small set of path-safety and shape
checks:

1. source exists
2. destination path is valid
3. source and destination do not resolve to the same directory
4. source is not inside destination and destination is not inside source
5. when promoting a generated root (`promote-generated` mode only), source
   contains at least the expected top-level surfaces defined in
   the generated-root shape specification below

### D7: Existing fail-fast guards remain mandatory

The `03` and `05a` strict-subset guards already landed (in
`lib/partial_rerun_guard.py`) and must remain in place. This refactor
complements them; it does not replace them.

### D8: Exit code contract is explicit

All CLI tool invocations must follow a simple exit code contract:

- Exit `0` on success.
- Exit `1` on validation failure, unsafe path, or any operational error.
- No other exit codes. No partial-success semantics.

This matters because the workflow shell steps will call the Python tool and
expect a non-zero exit code to fail the step.

### D9: Timestamp preservation is best-effort and cross-platform

`shutil.copy2` preserves modification time on all platforms. Creation time
preservation is OS-specific (Windows supports it; Linux does not). No downstream
consumer depends on creation timestamps. Only modification-time fidelity is
required and tested.

---

## Canonical Role Model After Refactor

| Role | Path in direct local runs | Path in smoke tests | Path in hosted CI | Authoritative? |
| --- | --- | --- | --- | --- |
| L0/L1/L2 working scratch | `tmp/` or env override | temp dir under `tmp/` | `${workspace}/tmp` | no |
| generated scratch output root | `staging/` | temp dir chosen by smoke harness | `${workspace}/staging` | no |
| tracked publish root | `openwrt-condensed-docs/` | optional temp destination only if a test chooses to promote | `openwrt-condensed-docs/` in deploy job | yes, after explicit promotion |
| external distribution targets | n/a | n/a | gh-pages worktree, distribution zip root, external repo checkout | publish-only |

The important semantic boundary is:

- `OUTDIR` means generated scratch output
- `PUBLISH_DIR` means tracked promoted output

Do not use one variable to mean both.

---

## Generated-Root Shape Specification

The `promote-generated` CLI mode requires a **lightweight shape check** before
mirroring into the tracked publish tree. This is not a full contract
validation — stage `08` owns that. This is a minimum-viable "is this tree
plausibly a complete generated output?" gate.

### Required top-level files (must exist and be non-empty)

These paths are relative to the generated root (i.e. `staging/`):

| Path | Rationale |
| --- | --- |
| `AGENTS.md` | Root navigation surface |
| `README.md` | Root navigation surface |
| `llms.txt` | LLM routing entry point |
| `llms-full.txt` | Full LLM routing catalog |
| `index.html` | Web index entry point |
| `repo-manifest.json` | Source provenance metadata |
| `cross-link-registry.json` | Cross-link metadata |

### Required top-level directories (must exist and be non-empty)

| Path | Rationale |
| --- | --- |
| `L1-raw/` | Must contain at least one module subdirectory |
| `L2-semantic/` | Must contain at least one module subdirectory |
| `release-tree/` | Must contain at least 4 module subdirectories |
| `support-tree/` | Must exist |

### Shape check: `release-tree/` interior

| Path | Rationale |
| --- | --- |
| `release-tree/llms.txt` | Release-tree routing entry |
| `release-tree/index.html` | Release-tree web index |
| `release-tree/AGENTS.md` | Release-tree agent navigation |
| `release-tree/README.md` | Release-tree README |

### Shape check: `support-tree/` interior

| Path | Rationale |
| --- | --- |
| `support-tree/manifests/repo-manifest.json` | Mirrored provenance |
| `support-tree/manifests/cross-link-registry.json` | Mirrored cross-links |
| `support-tree/telemetry/CHANGES.md` | Changelog surface |
| `support-tree/telemetry/changelog.json` | Machine-readable changelog |
| `support-tree/telemetry/signature-inventory.json` | API drift baseline |

### Provenance

This list is derived from the workflow's inline staging contract validator
(lines 728–758 of
`.github/workflows/openwrt-docs4ai-00-pipeline.yml`) and the `08` stage's
`validate_release_tree_contract()` function. It is intentionally a strict subset
of what `08` checks. If new required surfaces are added to the `08` contract or
the workflow staging validator, this list should be updated to match.

### Implementation note

The shape check function should be a single function that returns a `list[str]`
of error descriptions. An empty list means the tree passes. The caller decides
whether to abort or warn.

```python
# Exact constant the implementation must use.
# Keep in sync with the staging-contract required_paths in the workflow.
GENERATED_ROOT_REQUIRED_FILES: list[str] = [
    "AGENTS.md",
    "README.md",
    "llms.txt",
    "llms-full.txt",
    "index.html",
    "repo-manifest.json",
    "cross-link-registry.json",
    "release-tree/AGENTS.md",
    "release-tree/README.md",
    "release-tree/llms.txt",
    "release-tree/llms-full.txt",
    "release-tree/index.html",
    "support-tree/manifests/repo-manifest.json",
    "support-tree/manifests/cross-link-registry.json",
    "support-tree/telemetry/CHANGES.md",
    "support-tree/telemetry/changelog.json",
    "support-tree/telemetry/signature-inventory.json",
]

GENERATED_ROOT_REQUIRED_DIRS: list[str] = [
    "L1-raw",
    "L2-semantic",
    "release-tree",
    "support-tree",
]

RELEASE_TREE_MIN_MODULES: int = 4
```

---

## Exact rsync Call Site Inventory

The workflow file contains exactly 6 `rsync` invocations. Each has different
semantics. The sync helper must support all of them without behavior regression.

| Line | Source | Destination | Flags | Semantic | Sync mode required |
| --- | --- | --- | --- | --- | --- |
| 942 | `$OUTDIR/` | `$GITHUB_WORKSPACE/$PUBLISH_DIR/` | `-a --delete` | Full mirror: staging → tracked publish root | `promote-generated` |
| 990 | `$publish_root/` | `$branch_dir/` | `-a --delete --exclude=".git"` | Mirror publish root → gh-pages worktree, excluding `.git` | `mirror-tree --exclude .git` |
| 1104 | `$release_tree/` | `$zip_root/` | `-a --delete` | Mirror release-tree → zip staging root | `mirror-tree` |
| 1143 | `$release_tree/` | `$repo_dir/` (corpus) | `-a --delete --exclude=".git"` | Mirror release-tree → external corpus repo checkout, excluding `.git` | `mirror-tree --exclude .git` |
| 1206 | `$release_tree/` | `$repo_dir/` (pages) | `-a --delete --exclude=".git"` | Mirror release-tree → external pages repo checkout, excluding `.git` | `mirror-tree --exclude .git` |
| 1208 | `$pages_include_dir/` | `$repo_dir/` (pages) | `-a` (NO `--delete`) | **Additive overlay**: copy pages-include files on top of the mirrored tree without deleting anything | `overlay-tree` |

### Critical distinction: line 1208 is NOT a mirror

Line 1208 uses `rsync -a` **without** `--delete`. It overlays
`release-inputs/pages-include/` on top of the already-mirrored external pages
repo directory. If the sync helper replaces this call with a default
`delete_extraneous=True` mirror, it will **delete the release-tree content** that
was just mirrored in the previous step (line 1206).

The implementation must either:

1. Add an explicit `overlay-tree` CLI mode / `delete_extraneous=False` option, or
2. Invoke `sync_tree()` with `delete_extraneous=False` for this one call site.

Option 1 is cleaner. The CLI should support three modes:

- `promote-generated` — mirror with shape preflight
- `mirror-tree` — mirror with optional exclusions
- `overlay-tree` — additive copy without deletion

---

## Exact File Surfaces That Change

### Required code surfaces

| Path | Why it changes |
| --- | --- |
| `lib/config.py` | change default `OUTDIR` from `openwrt-condensed-docs` to `staging` |
| `lib/output_sync.py` (new) | shared path checks, shape validation, and tree sync logic |
| `tools/sync_tree.py` (new) | explicit promote/sync/overlay entry point for local and CI |
| `.github/workflows/openwrt-docs4ai-00-pipeline.yml` | replace all 6 `rsync` invocations with Python tool calls |

### Required test surfaces

| Path | Why it changes |
| --- | --- |
| `tests/pytest/pytest_01_workflow_contract_test.py` | assert workflow uses Python sync tool instead of `rsync` for source-repo promotion |
| `tests/pytest/pytest_07_partial_rerun_guard_test.py` | preserve guard coverage after default `OUTDIR` flip |
| `tests/pytest/pytest_08_output_sync_test.py` (new) | validate mirror, overlay, path safety, shape preflight, exit codes |
| `tests/smoke/` selective addition | one end-to-end scratch-then-promote proof |
| `tests/support/smoke_pipeline_support.py` | only if a shared promotion helper is exercised by smoke helpers |

### Required documentation surfaces

| Path | Why it changes |
| --- | --- |
| `DEVELOPMENT.md` | `OUTDIR` default, local workflow, and promotion guidance become stale |
| `CLAUDE.md` | repo rules and local validation guidance describe the old output role model |
| `docs/specs/pipeline-stage-catalog.md` | local rerun guidance must distinguish scratch generation from explicit promotion |
| `docs/ARCHITECTURE.md` | layer and output-role narrative must stop calling `openwrt-condensed-docs/` the default generation target |
| `tests/README.md` | direct entry-point guidance may need one note about explicit promotion and scratch outputs |
| `.github/scripts/README.md` | path-role guidance must mention the new default and shared sync helper |

### Script copy and wording audit surfaces

| Path | Why it needs audit |
| --- | --- |
| `.github/scripts/openwrt-docs4ai-07-generate-web-index.py` | `PUBLISH_PREFIX = "./openwrt-condensed-docs"` on line 35 must remain (it is a display-path prefix for the root `index.html`); the variable name and its purpose should be checked for clarity vs. the new OUTDIR semantics |
| `.github/scripts/openwrt-docs4ai-08-validate-output.py` | `validate_index_html_contract()` checks for `"./openwrt-condensed-docs/"` in `index.html` content (line 169); this is a publish-contract check and must remain; wording in docstrings should be audited |
| any doc containing `OUTDIR = openwrt-condensed-docs` | old default becomes wrong |

---

## Shared Sync Helper Contract

Implement one shared library and one shared CLI.

### Library location

`lib/output_sync.py`

### CLI location

`tools/sync_tree.py`

### Required library functions

```python
from pathlib import Path


def resolve_tree(path: str | Path) -> Path:
    """Resolve and normalize a path for safe tree operations.

    Returns the resolved absolute path.
    Raises ValueError if the path is empty or otherwise invalid.
    """
    ...


def assert_safe_tree_sync(source: Path, destination: Path) -> None:
    """Validate that source and destination are safe for sync.

    Raises ValueError if:
    - either path does not exist (source) or is not a valid parent (destination)
    - source and destination resolve to the same directory
    - source is inside destination
    - destination is inside source
    """
    ...


def validate_generated_root(source: Path) -> list[str]:
    """Validate that a generated root has the minimum required shape.

    Returns a list of error descriptions. Empty list means the tree passes.
    Checks against GENERATED_ROOT_REQUIRED_FILES,
    GENERATED_ROOT_REQUIRED_DIRS, and RELEASE_TREE_MIN_MODULES.
    """
    ...


def sync_tree(
    source: Path,
    destination: Path,
    *,
    delete_extraneous: bool = True,
    exclude_names: set[str] | None = None,
) -> None:
    """Mirror source tree into destination tree.

    - Copies files using shutil.copy2 (preserves modification time).
    - Creates destination directories as needed.
    - When delete_extraneous=True, removes files and directories in
      destination that do not exist in source (excluding names in
      exclude_names).
    - When delete_extraneous=False, only adds or updates files from source
      into destination without removing anything. This is the overlay mode.
    - Does not follow symlinks.
    - Does not introduce platform-dependent path handling.
    - Traverses deterministically (sorted directory listings).
    """
    ...
```

### Required CLI modes

```text
python tools/sync_tree.py promote-generated --src staging --dest openwrt-condensed-docs
python tools/sync_tree.py mirror-tree --src <path> --dest <path> [--exclude .git]
python tools/sync_tree.py overlay-tree --src <path> --dest <path>
```

### Required `promote-generated` behavior

1. Resolve source and destination with `resolve_tree()`.
2. Call `assert_safe_tree_sync(source, destination)`.
3. Call `validate_generated_root(source)`.
4. If validation errors: print each error to stderr, exit `1`.
5. Call `sync_tree(source, destination, delete_extraneous=True)`.
6. Print summary line: `"Promoted {n} files from {source} to {destination}"`.
7. Exit `0`.

### Required `mirror-tree` behavior

1. Resolve source and destination with `resolve_tree()`.
2. Call `assert_safe_tree_sync(source, destination)`.
3. Build `exclude_names` set from repeated `--exclude` CLI arguments.
4. Call `sync_tree(source, destination, delete_extraneous=True,
   exclude_names=exclude_names)`.
5. Print summary line.
6. Exit `0`.

### Required `overlay-tree` behavior

1. Resolve source and destination with `resolve_tree()`.
2. Call `assert_safe_tree_sync(source, destination)`.
3. Call `sync_tree(source, destination, delete_extraneous=False)`.
4. Print summary line.
5. Exit `0`.

### Error handling

All exceptions from `assert_safe_tree_sync` and `validate_generated_root` must
produce a human-readable error message on stderr and exit `1`. The CLI must not
raise unhandled exceptions or print tracebacks in normal operation.

### Deliberate non-features for first implementation

1. **No dry-run mode.** Tests will create real temp trees and inspect them
   post-sync. This is sufficient and avoids the complexity of a separate
   dry-run code path that could diverge from the real path.
2. **No rename-based atomic swap.** Windows rename semantics on populated
   directories are not the place to be clever on attempt one. Non-atomic
   promotion is acceptable because `rsync` today is also non-atomic.
3. **No duplicate validator logic.** Stage `08` already owns full contract
   checks. The promotion preflight is intentionally minimal.
4. **No progress bars or verbose logging by default.** A single summary line
   on success is sufficient. Verbose output can be added later if needed.

---

## Implementation Plan

---

## Phase 0: Freeze The Contract Before Editing

### Objective

Write down the exact target behavior before changing any code.

### Required outputs

1. Confirm this plan (v01) as the implementation source of truth.
2. Preserve the current `03` and `05a` guard behavior.
3. Confirm that `.gitignore` already ignores `staging/` (line 5 — verified).

### Do not change in this phase

1. No path defaults yet.
2. No workflow behavior yet.
3. No external distribution behavior yet.

---

## Phase 1: Introduce Shared Sync Logic Without Changing Defaults Yet

### Objective

Land the reusable sync implementation before flipping any default path.

### Step 1.1: Create `lib/output_sync.py`

Implement:

- `GENERATED_ROOT_REQUIRED_FILES` constant (exact list from the shape
  specification above).
- `GENERATED_ROOT_REQUIRED_DIRS` constant.
- `RELEASE_TREE_MIN_MODULES` constant (value: `4`).
- `resolve_tree(path)` — resolve, validate non-empty.
- `assert_safe_tree_sync(source, destination)` — identity check, containment
  check.
- `validate_generated_root(source)` — check files exist and are non-empty,
  check directories exist, check release-tree module count.
- `sync_tree(source, destination, *, delete_extraneous, exclude_names)` — the
  actual recursive tree sync.

Implementation notes for `sync_tree`:

1. Use `pathlib.Path` internally.
2. Use `sorted()` on all directory listings for deterministic traversal.
3. Build the destination tree if missing with `mkdir(parents=True, exist_ok=True)`.
4. For each source file, compute the relative path and the destination path.
   Copy with `shutil.copy2` if the destination file does not exist or differs
   in size or modification time.
5. When `delete_extraneous=True`, after copying, walk the destination tree.
   For each file or directory in destination that is not in source (and whose
   name is not in `exclude_names`), delete it. Delete files first, then empty
   directories, bottom-up.
6. When `delete_extraneous=False`, skip all deletion logic. Only add or update.
7. Do not follow symlinks. If a symlink is encountered in source, skip it and
   log a warning to stderr.
8. The `exclude_names` set applies to **names** (not paths). A name like `.git`
   will exclude any directory or file named `.git` at any depth. This matches
   `rsync --exclude=".git"` behavior.

### Step 1.2: Create `tools/sync_tree.py`

Implement `argparse`-based CLI with three subcommands:

- `promote-generated` — `--src`, `--dest`
- `mirror-tree` — `--src`, `--dest`, `--exclude` (repeatable)
- `overlay-tree` — `--src`, `--dest`

All subcommands follow the behavior specified above. All errors print to stderr
and exit `1`.

### Step 1.3: Create `tests/pytest/pytest_08_output_sync_test.py`

Required test cases:

**Path safety tests:**

1. `test_assert_safe_rejects_identical_paths` — source == destination must raise
   `ValueError`.
2. `test_assert_safe_rejects_source_inside_destination` — source is a child of
   destination must raise `ValueError`.
3. `test_assert_safe_rejects_destination_inside_source` — destination is a child
   of source must raise `ValueError`.
4. `test_assert_safe_accepts_sibling_paths` — two sibling directories must pass.

**Shape validation tests:**

5. `test_validate_generated_root_passes_complete_tree` — build a complete
   fixture tree with all required files and directories; assert empty error list.
6. `test_validate_generated_root_fails_missing_file` — omit `llms.txt` from
   fixture; assert error list contains an error mentioning `llms.txt`.
7. `test_validate_generated_root_fails_empty_file` — create `llms.txt` as
   0 bytes; assert error.
8. `test_validate_generated_root_fails_missing_directory` — omit `release-tree/`;
   assert error.
9. `test_validate_generated_root_fails_insufficient_release_modules` — create
   `release-tree/` with only 2 module subdirectories; assert error mentioning
   module count.

**Mirror tests:**

10. `test_sync_tree_mirrors_files` — create source with files; sync to empty
    destination; assert all files exist in destination with correct content.
11. `test_sync_tree_deletes_extraneous_files` — pre-populate destination with
    extra files; sync with `delete_extraneous=True`; assert extra files are gone.
12. `test_sync_tree_preserves_extraneous_when_disabled` — pre-populate
    destination with extra files; sync with `delete_extraneous=False`; assert
    extra files remain.
13. `test_sync_tree_excludes_named_entries` — pre-populate destination with
    `.git/` directory; sync with `exclude_names={".git"}`; assert `.git/`
    directory is preserved.
14. `test_sync_tree_creates_destination_if_missing` — sync to a non-existent
    destination path; assert destination is created.
15. `test_sync_tree_updates_changed_files` — modify a file in source after
    initial sync; re-sync; assert destination has updated content.

**Overlay tests:**

16. `test_overlay_preserves_existing_destination_files` — destination has
    file A; source has file B; overlay; assert both A and B exist in
    destination.
17. `test_overlay_updates_existing_files_from_source` — destination has file A
    with old content; source has file A with new content; overlay; assert
    destination A has new content.

**CLI tests:**

18. `test_cli_promote_generated_exits_zero_on_success` — build complete
    fixture tree; run CLI; assert exit code 0; assert destination populated.
19. `test_cli_promote_generated_exits_one_on_shape_failure` — build incomplete
    fixture tree; run CLI; assert exit code 1; assert destination unchanged.
20. `test_cli_mirror_tree_with_exclude` — run CLI with `--exclude .git`;
    assert `.git` preserved in destination.
21. `test_cli_overlay_tree_preserves_destination` — run CLI overlay mode;
    assert existing destination files preserved.

**Edge case tests:**

22. `test_sync_tree_handles_empty_source` — sync empty source to populated
    destination with `delete_extraneous=True`; assert destination is empty.
23. `test_sync_tree_handles_nested_directories` — deep directory nesting
    (3+ levels) in source; assert full recursive copy.

All tests should use `tmp_path` fixture for isolated temporary directories.

### Validation for phase completion

1. `python -m pytest tests/pytest/pytest_08_output_sync_test.py -q` — all pass.
2. `python -m pytest tests/pytest/pytest_07_partial_rerun_guard_test.py -q` —
   all pass (regression proof).
3. `python tests/check_linting.py` — clean.

---

## Phase 2: Replace Source-Repo Promotion In CI With The Shared Tool

### Objective

Make the hosted `deploy` job use the same Python promotion logic that local
maintainers will use.

### Step 2.1: Replace rsync line 942 in the workflow

In `.github/workflows/openwrt-docs4ai-00-pipeline.yml`, the `Promote & Commit`
step currently has:

```bash
echo "Promoting staging to $PUBLISH_DIR"
rsync -a --delete "$OUTDIR/" "$GITHUB_WORKSPACE/$PUBLISH_DIR/"
```

Replace with:

```bash
echo "Promoting staging to $PUBLISH_DIR"
python tools/sync_tree.py promote-generated --src "$OUTDIR" --dest "$GITHUB_WORKSPACE/$PUBLISH_DIR"
```

Keep everything else in the step unchanged:

- `git config` lines remain.
- `git add "$PUBLISH_DIR/"` remains.
- `git diff --cached --quiet` check remains.
- `git commit`, `git pull --rebase`, `git push` remain.

### Step 2.2: Update workflow contract tests

In `tests/pytest/pytest_01_workflow_contract_test.py`:

1. Add a new test `test_deploy_promotes_with_python_sync_tool` that reads the
   deploy block and asserts `"tools/sync_tree.py promote-generated"` appears in
   the text.
2. If any existing test asserts `rsync` specifically for the source-repo
   promotion line, update it.

### Step 2.3: Validate

1. `python -m pytest tests/pytest/pytest_01_workflow_contract_test.py -q` — all
   pass.
2. `python -m pytest tests/pytest/ -q` — full pytest suite green.
3. `python tests/check_linting.py` — clean.

### Do not change yet

1. Do not flip the local default `OUTDIR` yet.
2. Do not replace the other 5 workflow `rsync` invocations yet.

---

## Phase 3: Flip The Local Ad Hoc Default To Scratch Output

### Objective

Make direct local script execution safe by default.

### Step 3a: Flip the default

In `lib/config.py`, line 5:

```python
# Before:
OUTDIR = os.environ.get("OUTDIR", "openwrt-condensed-docs")

# After:
OUTDIR = os.environ.get("OUTDIR", "staging")
```

### Step 3b: Update primary maintainer docs (same commit as 3a)

The default flip and the doc updates must land in the same commit. A maintainer
reading stale docs after the default flip would be confused.

**`DEVELOPMENT.md`:**

- Update any section describing `OUTDIR` default.
- Replace language that implies direct generation into the tracked publish tree
  is the standard local path.
- Add a documented explicit local promote command example.

**`CLAUDE.md`:**

- Update the "Local Validation Commands" section if it references `OUTDIR`
  behavior.
- Update the "Architecture: Layer Model" section if it describes
  `openwrt-condensed-docs/` as the default generation target.
- Add a note that `openwrt-condensed-docs/` is the tracked publish root, not the
  default generation target.

**`docs/ARCHITECTURE.md`:**

- Update the output-role narrative to describe the new model.

**`docs/specs/pipeline-stage-catalog.md`:**

- Update local rerun guidance to distinguish scratch generation from explicit
  promotion.

### Remaining doc surfaces (can be same commit or next commit)

- `tests/README.md` — add one note about scratch vs. publish.
- `.github/scripts/README.md` — mention the new default and shared sync helper.

### Required compatibility behavior

1. Any caller that explicitly sets `OUTDIR` keeps working.
2. Smoke runners keep setting explicit temp `OUTDIR` values and are therefore
   unaffected by the default change.
3. Hosted CI keeps setting explicit `OUTDIR=${{ github.workspace }}/staging`
   and is therefore unaffected by the default change.

### Required local command examples after this phase

```powershell
# Generate into scratch (default OUTDIR=staging)
python .github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py
python .github/scripts/openwrt-docs4ai-03-normalize-semantic.py
python .github/scripts/openwrt-docs4ai-05a-assemble-references.py
python .github/scripts/openwrt-docs4ai-06-generate-llm-routing-indexes.py
python .github/scripts/openwrt-docs4ai-07-generate-web-index.py
python .github/scripts/openwrt-docs4ai-08-validate-output.py

# Explicitly promote validated scratch into tracked publish tree
python tools/sync_tree.py promote-generated --src staging --dest openwrt-condensed-docs
```

### Validation for phase completion

1. `python -m pytest tests/pytest/ -q` — full suite green.
2. `python tests/check_linting.py` — clean.
3. Confirm no test or script hardcodes the assumption that `config.OUTDIR`
   defaults to `openwrt-condensed-docs`.

---

## Phase 4: Reuse The Same Sync Helper For Remaining Delivery Mirrors

### Objective

Finish the refactor so delivery behavior is defined by one Python sync contract,
not by a mix of Python and `rsync`.

### Step 4.1: Replace rsync line 990 (gh-pages mirror)

Replace:

```bash
rsync -a --delete --exclude=".git" "$publish_root/" "$branch_dir/"
```

With:

```bash
python tools/sync_tree.py mirror-tree --src "$publish_root" --dest "$branch_dir" --exclude .git
```

The `touch "$branch_dir/.nojekyll"` line that follows must remain unchanged.

### Step 4.2: Replace rsync line 1104 (zip root mirror)

Replace:

```bash
rsync -a --delete "$release_tree/" "$zip_root/"
```

With:

```bash
python tools/sync_tree.py mirror-tree --src "$release_tree" --dest "$zip_root"
```

### Step 4.3: Replace rsync line 1143 (corpus repo mirror)

Replace:

```bash
rsync -a --delete --exclude=".git" "$release_tree/" "$repo_dir/"
```

With:

```bash
python tools/sync_tree.py mirror-tree --src "$release_tree" --dest "$repo_dir" --exclude .git
```

### Step 4.4: Replace rsync lines 1206+1208 (external pages mirror + overlay)

This is the most subtle replacement. The current pattern is:

```bash
rsync -a --delete --exclude=".git" "$release_tree/" "$repo_dir/"
if [ -d "$pages_include_dir" ]; then
    rsync -a "$pages_include_dir/" "$repo_dir/"
fi
```

Replace with:

```bash
python tools/sync_tree.py mirror-tree --src "$release_tree" --dest "$repo_dir" --exclude .git
if [ -d "$pages_include_dir" ]; then
    python tools/sync_tree.py overlay-tree --src "$pages_include_dir" --dest "$repo_dir"
fi
```

**Critical implementation note:** The second invocation uses `overlay-tree`, not
`mirror-tree`. This preserves the additive-only semantics of the original
`rsync -a` (without `--delete`). Using `mirror-tree` here would delete the
release-tree content that was just mirrored.

### Important implementation guardrail

Do not refactor all mirrors in the same commit that flips the local default
`OUTDIR` unless the intermediate validations are already green.
This phase can follow immediately after Phase 3, but it should be a distinct
implementation step with its own focused validation.

### Validation for phase completion

1. `python -m pytest tests/pytest/ -q` — full suite green.
2. `python tests/check_linting.py` — clean.
3. `grep -rn "rsync" .github/workflows/openwrt-docs4ai-00-pipeline.yml` returns
   zero matches (all 6 invocations replaced).

---

## Phase 5: Fix Terminology Drift In Human-Facing Output And Docs

### Objective

Make the words match the new architecture.

### Required copy changes

1. Any maintainer doc that says `openwrt-condensed-docs/` is the default output
   root must be rewritten to say it is the tracked publish root.
2. Any wording that describes `openwrt-condensed-docs/` as "staging" must be
   revised. The word "staging" now specifically means the scratch generation
   output directory.
3. Review `.github/scripts/openwrt-docs4ai-07-generate-web-index.py` line 35:
   `PUBLISH_PREFIX = "./openwrt-condensed-docs"`. This is a display-path prefix
   for the root `index.html` and must remain as-is because the root index
   renders paths as they appear in the committed source-repo tree. Add a comment
   explaining this: `# Display-path prefix for source-repo root index.html
   (not the generation target)`.
4. Review `.github/scripts/openwrt-docs4ai-08-validate-output.py` line 169:
   the check `if "./openwrt-condensed-docs/" not in content:` validates that the
   root `index.html` contains display paths. This must remain as-is. Add a
   clarifying comment if the current context is ambiguous.

### Acceptable new wording

- `generated corpus tree` (for what OUTDIR produces)
- `tracked publish tree` (for `openwrt-condensed-docs/`)
- `source-repo generated output root` (for the functional role of OUTDIR)

### Unacceptable new wording

- `production`
- `live`
- any wording that implies a runtime service rather than generated files

### Validation for phase completion

1. `grep -rn "OUTDIR.*openwrt-condensed" docs/ DEVELOPMENT.md CLAUDE.md` returns
   zero matches (all old-default references updated).
2. Manual review of generated HTML title/heading strings.

---

## Phase 6: Align Tests And Runbooks

### Objective

Make the tests prove the new contract instead of only describing it.

### Required test state after this phase

1. Unit tests for `lib/output_sync.py` in
   `tests/pytest/pytest_08_output_sync_test.py` — all passing.
2. Workflow contract tests that assert Python sync tool usage for source-repo
   promotion — passing.
3. Guard regression tests in `tests/pytest/pytest_07_partial_rerun_guard_test.py`
   — all passing.
4. At least one end-to-end local proof of the generate→validate→promote cycle.

### End-to-end proof specification

Add one test (either as a pytest test or a narrow smoke script) that:

1. Creates an isolated temp directory structure: `$tmp/scratch/` and
   `$tmp/publish/`.
2. Seeds `$tmp/scratch/` with a minimal fixture tree that satisfies the
   generated-root shape specification (all required files and directories,
   at least 4 release-tree module stubs).
3. Invokes `tools/sync_tree.py promote-generated --src $tmp/scratch --dest
   $tmp/publish` as a subprocess.
4. Asserts exit code 0.
5. Asserts all required files from the shape specification exist in
   `$tmp/publish/`.
6. Asserts no extraneous files from a prior population of `$tmp/publish/` remain
   (pre-populate with one extra file, verify it is gone after promotion).

This test must not touch the real repo-root `openwrt-condensed-docs/` or
`staging/`.

### Optional but recommended smoke addition

Add one narrow smoke script (e.g., `tests/smoke/smoke_02_promote_cycle.py`) or
smoke branch that:

1. Seeds fixture-backed inputs.
2. Runs the post-extract pipeline into a temp scratch outdir.
3. Validates the scratch tree.
4. Promotes into a second temp publish tree with `tools/sync_tree.py`.
5. Verifies key outputs exist in the promoted tree.

---

## Phase 7: Rollout Sequence

### Recommended implementation order

1. **Land `lib/output_sync.py` and `tools/sync_tree.py` plus unit tests.**
   This is zero-risk: no existing behavior changes.
2. **Swap CI source-repo promotion** from `rsync` to the Python tool (line 942
   only). This is the smallest possible behavioral change in CI.
3. **Flip the local default `OUTDIR` to `staging`.**
   This is the largest behavioral change. It must happen after a promote
   command exists (step 1) and after CI is already using it (step 2).
4. **Update docs and wording** in the same commit as step 3 or immediately
   after.
5. **Replace the remaining 5 workflow `rsync` mirrors** with Python tool
   invocations (lines 990, 1104, 1143, 1206, 1208).
6. **Run final focused local validation** (`run_smoke_and_pytest.py`).
7. **Push to a branch and verify** the hosted workflow on that exact commit SHA.

### Why this order is safest

It keeps the most dangerous behavioral change, the local default flip, behind an
already-tested promotion helper and an already-updated hosted promotion path.

### Commit strategy

| Commit | Content | Risk |
| --- | --- | --- |
| 1 | `lib/output_sync.py` + `tools/sync_tree.py` + `pytest_08_output_sync_test.py` | Zero (additive only) |
| 2 | Workflow line 942 swap + `pytest_01` update | Low (CI-only change, one line) |
| 3 | `lib/config.py` default flip + all doc updates | Medium (local behavior change) |
| 4 | Remaining 5 workflow `rsync` replacements (lines 990, 1104, 1143, 1206, 1208) | Low (CI-only, uses tested tool) |
| 5 | End-to-end promotion test + optional smoke addition | Zero (test-only) |

If any commit fails validation, stop and fix before proceeding to the next.

---

## Validation Checklist

Run these proofs in order after each phase.

### Focused local proofs

```powershell
python -m pytest tests/pytest/pytest_08_output_sync_test.py -q
python -m pytest tests/pytest/pytest_07_partial_rerun_guard_test.py -q
python -m pytest tests/pytest/pytest_01_workflow_contract_test.py -q
python tests/check_linting.py
```

### Maintained local validation

```powershell
python tests/run_smoke_and_pytest.py
```

### Hosted proof

1. Push the branch.
2. Pin the exact workflow run to the commit SHA using:
   ```powershell
   git rev-parse HEAD
   gh run list --workflow "openwrt-docs4ai-pipeline" --limit 5 --json databaseId,headSha,status,conclusion,url
   gh run watch <run_id> --exit-status --interval 15
   ```
3. Verify:
   - staging contract passes
   - deploy job promotes with the Python tool
   - published branch mirrors still complete successfully
   - no path regressions show up in `pipeline-summary` or `process-summary`
4. Triage artifacts before raw logs:
   ```powershell
   gh run download <run_id> -n pipeline-summary -D tmp/ci/pipeline-summary
   gh run download <run_id> -n extract-summary -D tmp/ci/extract-summary
   gh run view <run_id> --log-failed
   ```

---

## Acceptance Criteria

The refactor is complete only when all of the following are true.

1. Direct local script execution defaults `OUTDIR` to `staging`, not
   `openwrt-condensed-docs/`.
2. `openwrt-condensed-docs/` is only updated by an explicit promote/sync step.
3. Hosted CI still builds into `staging/` and promotes later.
4. The source-repo promotion path uses the shared Python helper, not `rsync`.
5. All 6 workflow `rsync` invocations are replaced with Python tool calls, or
   remaining ones are intentionally deferred with a documented reason.
6. Smoke runners remain temp-tree-based and isolated.
7. Existing `03` and `05a` fail-fast guards still pass their regression tests.
8. Documentation consistently describes:
   - `staging/` as scratch generated output
   - `openwrt-condensed-docs/` as tracked publish output
9. No Windows/Linux behavior branches were introduced.
10. A maintainer can perform the local sequence "generate → validate → promote"
    using documented Python commands only.
11. The `overlay-tree` mode correctly handles the `pages-include` additive
    overlay without deleting mirrored release-tree content.
12. Exit codes are deterministic: `0` on success, `1` on any failure.
13. At least one end-to-end test proves the full promote cycle in isolation.

---

## Rollback Plan

If the refactor causes regressions, roll back in this order:

1. Revert the workflow steps from Python sync back to the prior `rsync` lines
   (all 6).
2. Revert `lib/config.py` default `OUTDIR` from `staging` back to
   `openwrt-condensed-docs`.
3. Keep the `03` and `05a` fail-fast guards unless they are directly implicated.
4. Revert docs that describe the new model only after the code rollback lands.

Do not partially roll back the docs while leaving the code on the new model.
That would recreate the same local/CI drift this plan is trying to remove.

### Partial rollback alternative

If only the remaining mirrors (Phase 4) cause issues but the source-repo
promotion (Phase 2) is working:

1. Revert only the Phase 4 workflow changes (lines 990, 1104, 1143, 1206, 1208)
   back to `rsync`.
2. Keep the Python promotion on line 942.
3. Keep the local default flip.
4. File a tracking issue for the remaining mirror migration.

This keeps the most important behavioral improvement (safe local defaults) while
reverting only the lower-value delivery mirror changes.

---

## First-Try Error Avoidance Notes

These are the mistakes most likely to break the first implementation attempt.

1. **Do not change smoke runners to use repo-root `staging/`.** They must
   continue using isolated temp directories via `build_env()`.
2. **Do not rename `openwrt-condensed-docs/` or any layer folders.**
3. **Do not leave the workflow using Python sync for one mirror and stale tests
   still asserting `rsync` on that path.** Update tests in the same commit.
4. **Do not flip the local default `OUTDIR` before a promote command exists.**
   Phase 1 must complete before Phase 3.
5. **Do not duplicate stage `08` inside the promote helper.** The shape check
   is intentionally minimal.
6. **Do not implement path sync with shell-specific commands.**
7. **Do not forget wording audits in generated HTML and maintainer docs.**
8. **Do not promote scratch output into the tracked tree unless validation has
   already passed.**
9. **Do not use `mirror-tree` for the `pages-include` overlay step (workflow
   line 1208).** This is an additive overlay; use `overlay-tree` mode with
   `delete_extraneous=False`.
10. **Do not forget the `--exclude .git` argument** when mirroring into git
    worktrees or external repo checkouts (lines 990, 1143, 1206).
11. **Do not skip `assert_safe_tree_sync` before any sync operation.** All three
    CLI modes must call it.
12. **Do not forget to handle the case where destination does not exist yet.**
    `sync_tree()` must create it. This is relevant for the first local run
    into a fresh `staging/`.
13. **Do not assume `shutil.copy2` preserves creation timestamps on Linux.** Only
    modification time is guaranteed cross-platform.
14. **Do not introduce separate code paths for Windows and Linux.** Use
    `pathlib.Path` and `shutil` consistently. Do not use `os.system()` or
    subprocess calls to shell utilities.
15. **Do not batch the doc updates into a later commit if the default flip is
    landing now.** A maintainer reading stale docs after the flip will be
    confused. Phase 3a and 3b must be atomic or same-session.

---

## Short Version

The correct long-term model is:

- generate into `staging/`
- validate `staging/`
- explicitly promote `staging/` into `openwrt-condensed-docs/`
- use one Python sync helper for local and CI (mirror, overlay, promote)
- keep smoke tests isolated
- keep path names and public contracts unchanged

That unifies the safe behavior everywhere without reopening the naming or schema
surfaces that were not actually at fault.

---

## Changes From v00

| Area | v00 | v01 |
| --- | --- | --- |
| Generated-root shape check | Unspecified — only said "expected top-level surfaces" | Fully enumerated with exact file list, directory list, and `RELEASE_TREE_MIN_MODULES` constant |
| rsync line 1208 (additive overlay) | Not distinguished from mirrors | Explicitly called out as non-mirror; added `overlay-tree` CLI mode |
| Concurrent local runs | Not addressed | D6 added: single-writer semantics are assumed |
| Exit code contract | Implied | D8 added: exit 0 on success, exit 1 on failure, no other codes |
| Timestamp semantics | Said "copy2-style" without platform caveat | D9 added: only modification time is guaranteed cross-platform |
| Phase 3 doc atomicity | Doc updates in same phase but not explicitly same-commit | Step 3a and 3b explicitly must be same commit |
| Test cases | High-level descriptions | 23 individually named test cases with exact behaviors specified |
| Commit strategy | Implicit | Explicit 5-commit sequence with per-commit risk assessment |
| rsync inventory | Mentioned 6 sites | Full table with line numbers, flags, semantic description, and required sync mode |
| Partial rollback | Not addressed | Added partial rollback alternative for Phase 4 isolation |
| `overlay-tree` mode | Not present | Added as third CLI mode with explicit `delete_extraneous=False` semantics |
| Error handling | Implicit | Explicit: stderr messages, no tracebacks, human-readable errors |
| First-try avoidance | 8 items | 15 items, including overlay mode, `.git` exclusion, doc atomicity, and shutil caveats |
