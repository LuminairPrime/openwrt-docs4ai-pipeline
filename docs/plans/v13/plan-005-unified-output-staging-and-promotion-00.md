# Plan-005: Unified Output Staging And Promotion

## Status
Proposed (2026-03-28)

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

---

## Locked Decisions

### D1: `openwrt-condensed-docs/` becomes publish-only by contract

It remains committed, inspectable, and promotable, but it is no longer the
default `OUTDIR` for direct local script execution.

### D2: `staging/` becomes the canonical repo-root scratch output for ad hoc runs

This is the least risky unification path because:

- the workflow already uses `${workspace}/staging`
- `.gitignore` already ignores `staging/`
- the workflow artifact and contract naming already use "staging"
- this minimizes churn compared with inventing a new scratch root name

This means:

- default local ad hoc `OUTDIR` becomes `staging`
- default hosted CI `OUTDIR` remains `staging`
- local smoke runners may still use temp directories because they are test
  harnesses, not maintainer publish targets

### D3: Local smoke runners stay temp-based

The local smoke runners already do the right thing: they create isolated temp
trees, set `WORKDIR` and `OUTDIR` explicitly, and never depend on the tracked
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

- `publish_root -> gh-pages worktree`
- `release-tree/ -> distribution zip root`
- `release-tree/ -> external release repo checkout`

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
5. when promoting a generated root, source contains at least the expected top
   level generated tree surfaces required for promotion

### D7: Existing fail-fast guards remain mandatory

The `03` and `05a` strict-subset guards already landed and must remain in place.
This refactor complements them; it does not replace them.

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

## Exact File Surfaces Likely To Change

### Required code surfaces

| Path | Why it changes |
| --- | --- |
| `lib/config.py` | change default `OUTDIR` from `openwrt-condensed-docs` to `staging` |
| `lib/` new helper module | shared path checks and tree sync logic |
| `tools/` new CLI wrapper | explicit promote/sync entry point for local and CI |
| `.github/workflows/openwrt-docs4ai-00-pipeline.yml` | replace `rsync` source-repo promotion and downstream mirrors with Python tool invocation |

### Likely test surfaces

| Path | Why it changes |
| --- | --- |
| `tests/pytest/pytest_01_workflow_contract_test.py` | assert workflow uses Python sync tool instead of `rsync` for source-repo promotion |
| `tests/pytest/pytest_07_partial_rerun_guard_test.py` | preserve guard coverage after default `OUTDIR` flip |
| `tests/pytest/` new sync-helper test file | validate mirror semantics, path safety, and generated-root preflight |
| `tests/smoke/` selective updates | add one end-to-end scratch-then-promote proof, if needed |
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

### Likely script copy and wording audit surfaces

| Path | Why it needs audit |
| --- | --- |
| `.github/scripts/openwrt-docs4ai-07-generate-web-index.py` | human-facing wording currently says "staging tree" while rendering `openwrt-condensed-docs` |
| `.github/scripts/openwrt-docs4ai-08-validate-output.py` | path checks likely remain valid, but wording and assumptions should be reviewed |
| docs containing `OUTDIR = openwrt-condensed-docs` | old default becomes wrong |

---

## Shared Sync Helper Contract

Implement one shared library and one shared CLI.

### Library location

- `lib/output_sync.py`

### CLI location

- `tools/sync_tree.py`

### Required library functions

```python
from pathlib import Path

def resolve_tree(path: str | Path) -> Path: ...

def assert_safe_tree_sync(source: Path, destination: Path) -> None: ...

def validate_generated_root(source: Path) -> list[str]: ...

def sync_tree(
    source: Path,
    destination: Path,
    *,
    delete_extraneous: bool = True,
    exclude_names: set[str] | None = None,
) -> None: ...
```

### Required CLI modes

```text
python tools/sync_tree.py promote-generated --src staging --dest openwrt-condensed-docs
python tools/sync_tree.py mirror-tree --src <path> --dest <path> --exclude .git
```

### Required `promote-generated` behavior

1. Resolve source and destination with `Path.resolve()`.
2. Fail if either path is invalid for safe sync.
3. Run `validate_generated_root(source)`.
4. Fail if validation errors exist.
5. Mirror source into destination.
6. Delete extraneous destination content by default.
7. Preserve file contents and timestamps with `copy2`-style behavior.

### Required `mirror-tree` behavior

1. Resolve source and destination with `Path.resolve()`.
2. Fail on source/destination identity or containment hazards.
3. Support a repeatable `--exclude` list for names such as `.git`.
4. Mirror recursively.
5. Delete extraneous destination content by default.

### Deliberate non-features for first implementation

1. No dry-run mode in the first tranche unless tests show it is necessary.
2. No rename-based atomic swap implementation in the first tranche.
   Windows rename semantics on populated directories are not the place to be
   clever on attempt one.
3. No duplicate validator logic. Stage `08` already owns full contract checks.

---

## Implementation Plan

## Phase 0: Freeze The Contract Before Editing

### Objective

Write down the exact target behavior before changing any code.

### Required outputs

1. Confirm this plan as the implementation source of truth.
2. Preserve the current `03` and `05a` guard behavior.
3. Confirm that `.gitignore` already ignores `staging/` so no new ignore rule is
   required if `staging/` remains the scratch root.

### Do not change in this phase

1. No path defaults yet.
2. No workflow behavior yet.
3. No external distribution behavior yet.

---

## Phase 1: Introduce Shared Sync Logic Without Changing Defaults Yet

### Objective

Land the reusable sync implementation before flipping any default path.

### Exact changes

1. Add `lib/output_sync.py`.
2. Add `tools/sync_tree.py`.
3. Add focused pytest coverage for:
   - safe path rejection when source equals destination
   - safe path rejection when one path contains the other
   - generated-root preflight success and failure
   - recursive mirror behavior with deletion of extraneous files
   - exclusion behavior for `.git`

### Implementation notes

1. Use `pathlib.Path` internally.
2. Use deterministic recursive traversal.
3. Build the destination tree if missing.
4. Delete destination files and directories that are absent from the source when
   `delete_extraneous=True`.
5. Do not follow symlinks or introduce platform-dependent path handling.

### Validation for phase completion

1. New sync-helper pytest file passes.
2. Existing `pytest_07_partial_rerun_guard_test.py` still passes.

---

## Phase 2: Replace Source-Repo Promotion In CI With The Shared Tool

### Objective

Make the hosted `deploy` job use the same Python promotion logic that local
maintainers will use.

### Exact workflow changes

In `.github/workflows/openwrt-docs4ai-00-pipeline.yml`:

1. Keep `PUBLISH_DIR: openwrt-condensed-docs`.
2. Keep `OUTDIR: ${{ github.workspace }}/staging` in the first pass.
3. Replace the source-repo promotion step:

```bash
rsync -a --delete "$OUTDIR/" "$GITHUB_WORKSPACE/$PUBLISH_DIR/"
```

with a Python invocation of the shared tool.

### Required behavior

1. The `process` job still uploads the `final-staging` artifact.
2. The `deploy` job still downloads that artifact into `OUTDIR`.
3. The `deploy` job promotes into `openwrt-condensed-docs/` only after the
   existing staging contract checks pass.
4. `git add "$PUBLISH_DIR/"` remains unchanged.

### Required test updates

1. Update workflow contract tests to assert that the source-repo promotion step
   invokes the Python tool.
2. Remove assertions that require `rsync` for that one path.

### Do not change yet

1. Do not flip the local default `OUTDIR` yet.
2. Do not replace the other workflow `rsync` mirrors yet.

---

## Phase 3: Flip The Local Ad Hoc Default To Scratch Output

### Objective

Make direct local script execution safe by default.

### Exact changes

In `lib/config.py`:

1. Change:

```python
OUTDIR = os.environ.get("OUTDIR", "openwrt-condensed-docs")
```

to:

```python
OUTDIR = os.environ.get("OUTDIR", "staging")
```

### Required compatibility behavior

1. Any caller that explicitly sets `OUTDIR` keeps working.
2. Smoke runners keep setting explicit temp `OUTDIR` values and are therefore
   unaffected by the default change.
3. Hosted CI keeps setting explicit `OUTDIR` and is therefore unaffected by the
   default change.

### Required documentation updates in this phase

1. Update all maintainer docs that claim the default `OUTDIR` is
   `openwrt-condensed-docs`.
2. Replace language that implies direct generation into the tracked publish tree
   is the standard local path.
3. Add a documented explicit local promote command example using the shared
   Python tool.

### Required local command examples after this phase

```powershell
python .github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py
python .github/scripts/openwrt-docs4ai-03-normalize-semantic.py
python .github/scripts/openwrt-docs4ai-05a-assemble-references.py
python .github/scripts/openwrt-docs4ai-06-generate-llm-routing-indexes.py
python .github/scripts/openwrt-docs4ai-07-generate-web-index.py
python .github/scripts/openwrt-docs4ai-08-validate-output.py
python tools/sync_tree.py promote-generated --src staging --dest openwrt-condensed-docs
```

---

## Phase 4: Reuse The Same Sync Helper For Remaining Delivery Mirrors

### Objective

Finish the refactor so delivery behavior is defined by one Python sync contract,
not by a mix of Python and `rsync`.

### Workflow surfaces to update

Replace these remaining mirror steps in
`.github/workflows/openwrt-docs4ai-00-pipeline.yml` with the shared helper where
practical:

1. `publish_root -> gh-pages` worktree mirror excluding `.git`
2. `release-tree -> zip_root` mirror
3. `release-tree -> external repo` mirror excluding `.git`

### Required behavior

1. `.git` exclusion behavior remains preserved.
2. `--delete` semantics remain preserved.
3. Resulting artifacts and published trees remain byte-for-byte equivalent for
   the same input tree except for timestamp metadata.

### Important implementation guardrail

Do not refactor all mirrors in the same commit that flips the local default
`OUTDIR` unless the intermediate validations are already green.
This phase can follow immediately, but it should be a distinct implementation
step with its own focused validation.

---

## Phase 5: Fix Terminology Drift In Human-Facing Output And Docs

### Objective

Make the words match the new architecture.

### Required copy changes

1. Any maintainer doc that says `openwrt-condensed-docs/` is the default output
   root must be rewritten to say it is the tracked publish root.
2. Any wording that describes `openwrt-condensed-docs/` as "staging" must be
   revised.
3. Review `.github/scripts/openwrt-docs4ai-07-generate-web-index.py` strings
   such as the generated title and heading that currently say
   `openwrt-condensed-docs staging tree`.

### Acceptable new wording

- `generated corpus tree`
- `tracked publish tree`
- `source-repo generated output tree`

### Unacceptable new wording

- `production`
- `live`
- any wording that implies a runtime service rather than generated files

---

## Phase 6: Align Tests And Runbooks

### Objective

Make the tests prove the new contract instead of only describing it.

### Required tests

1. Unit tests for `lib/output_sync.py`.
2. Workflow contract tests that assert Python sync tool usage for source-repo
   promotion.
3. Guard regression tests remain green.
4. At least one end-to-end local proof of:
   - generate into scratch
   - validate scratch
   - promote scratch into a destination tree
   - confirm destination tree matches expected generated-root shape

### Optional but recommended smoke addition

Add one narrow smoke script or smoke branch that:

1. seeds fixture-backed inputs
2. runs the post-extract pipeline into a temp scratch outdir
3. validates the scratch tree
4. promotes into a second temp publish tree with `tools/sync_tree.py`
5. verifies key outputs exist in the promoted tree

This test should not touch the real repo-root `openwrt-condensed-docs/`.

---

## Phase 7: Rollout Sequence

### Recommended implementation order

1. Land `lib/output_sync.py` and `tools/sync_tree.py` plus unit tests.
2. Swap CI source-repo promotion from `rsync` to the Python tool.
3. Flip the local default `OUTDIR` to `staging`.
4. Update docs and wording.
5. Replace the remaining workflow `rsync` mirrors.
6. Run final focused local validation.
7. Push to a branch and verify the hosted workflow on that exact commit SHA.

### Why this order is safest

It keeps the most dangerous behavioral change, the local default flip, behind an
already-tested promotion helper and an already-updated hosted promotion path.

---

## Validation Checklist

Run these proofs in order.

### Focused local proofs

```powershell
python -m pytest tests/pytest/pytest_07_partial_rerun_guard_test.py -q
python -m pytest tests/pytest/<new_output_sync_test_file>.py -q
python -m pytest tests/pytest/pytest_01_workflow_contract_test.py -q
python tests/check_linting.py
```

### Maintained local validation

```powershell
python tests/run_smoke_and_pytest.py
```

### Hosted proof

1. Push the branch.
2. Pin the exact workflow run to the commit SHA.
3. Verify:
   - staging contract passes
   - deploy job promotes with the Python tool
   - published branch mirrors still complete successfully
   - no path regressions show up in `pipeline-summary` or `process-summary`

---

## Acceptance Criteria

The refactor is complete only when all of the following are true.

1. Direct local script execution defaults `OUTDIR` to `staging`, not
   `openwrt-condensed-docs/`.
2. `openwrt-condensed-docs/` is only updated by an explicit promote/sync step.
3. Hosted CI still builds into `staging/` and promotes later.
4. The source-repo promotion path uses the shared Python helper, not `rsync`.
5. Remaining workflow delivery mirrors either use the same helper or are
   intentionally deferred with a documented reason.
6. Smoke runners remain temp-tree-based and isolated.
7. Existing `03` and `05a` fail-fast guards still pass their regression tests.
8. Documentation consistently describes:
   - `staging/` as scratch generated output
   - `openwrt-condensed-docs/` as tracked publish output
9. No Windows/Linux behavior branches were introduced.
10. A maintainer can perform the local sequence "generate -> validate -> promote"
    using documented Python commands only.

---

## Rollback Plan

If the refactor causes regressions, roll back in this order:

1. Revert the workflow step from Python sync back to the prior `rsync` line.
2. Revert `lib/config.py` default `OUTDIR` from `staging` back to
   `openwrt-condensed-docs`.
3. Keep the `03` and `05a` fail-fast guards unless they are directly implicated.
4. Revert docs that describe the new model only after the code rollback lands.

Do not partially roll back the docs while leaving the code on the new model.
That would recreate the same local/CI drift this plan is trying to remove.

---

## First-Try Error Avoidance Notes

These are the mistakes most likely to break the first implementation attempt.

1. Do not change smoke runners to use repo-root `staging/`.
2. Do not rename `openwrt-condensed-docs/` or any layer folders.
3. Do not leave the workflow using Python sync for one mirror and stale tests
   still asserting `rsync` on that path.
4. Do not flip the local default `OUTDIR` before a promote command exists.
5. Do not duplicate stage `08` inside the promote helper.
6. Do not implement path sync with shell-specific commands.
7. Do not forget wording audits in generated HTML and maintainer docs.
8. Do not promote scratch output into the tracked tree unless validation has
   already passed.

---

## Short Version

The correct long-term model is:

- generate into `staging/`
- validate `staging/`
- explicitly promote `staging/` into `openwrt-condensed-docs/`
- use one Python sync helper for local and CI
- keep smoke tests isolated
- keep path names and public contracts unchanged

That unifies the safe behavior everywhere without reopening the naming or schema
surfaces that were not actually at fault.