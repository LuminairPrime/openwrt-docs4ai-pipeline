# ENABLE_RELEASE_TREE Feature Flag Contract

## Purpose

This document defines the `ENABLE_RELEASE_TREE` environment variable that controls the transition from the current output contract to the V5a release-tree contract. It is introduced in Phase 0 of the V5a refactor and removed in Phase 7 after live validation of the new contract.

The authoritative implementation plan is `docs/plans/v12/public-distribution-mirror-plan-2026-03-15-V5a.md`.

---

## Flag Definition

| Property | Value |
| --- | --- |
| Name | `ENABLE_RELEASE_TREE` |
| Type | Environment variable |
| Values | `true` / `false` (string, case-insensitive) |
| Default | `false` |
| Scope | Late-stage pipeline scripts: `05a`, `05b`, `06`, `07`, `08`, and `05e-assemble-release-tree.py` |

The default of `false` preserves the current output contract until the flag is explicitly activated.

---

## Behavior When `false` (Default)

- All pipeline stages produce output using the current contract.
- Output goes to `OUTDIR` (`openwrt-condensed-docs/`) with current filenames.
- Script `05e` is skipped entirely.
- All existing tests validate the current contract.
- No `release-tree/` or `support-tree/` directories are created.
- This is the safe rollback state for any failed phase.

---

## Behavior When `true`

The behavior changes by phase.

**Phase 1–3:** Script `05e` runs after existing stages and produces `release-tree/` alongside unchanged current output. Old output still exists under `OUTDIR/`.

**Phase 4:** Late stages (`05a`, `05b`, `06`, `07`, `08`) write into `release-tree/` instead of `OUTDIR/`. Script `05e` is retired.

**Phase 5:** Test suite switches to assert the new contract as primary. The flag default changes to `true`.

**Phase 6:** Deploy workflow publishes from `release-tree/`.

---

## Test Expectations Per Flag State

**`false`:** All existing tests pass. Release-tree tests either do not exist yet or skip gracefully if `release-tree/` is absent.

**`true` (Phase 1–3):** Existing tests still pass against `OUTDIR/`. New release-tree tests (`tests/pytest/pytest_09_release_tree_contract_test.py`) also pass against `release-tree/`.

**`true` (Phase 4+):** Old-contract assertions are removed. Tests validate `release-tree/` as primary.

---

## Flag Lifecycle

| Event | Phase |
| --- | --- |
| Introduced | Phase 0 |
| Default changes to `true` | Phase 5 |
| Removed | Phase 7 |

---

## Interaction With Other Variables

**`OUTDIR`:** Unchanged. Early stages (`01` through `04`) always write to `OUTDIR`. The flag controls only where late stages direct their final output.

**`WORKDIR`:** Unchanged. The scratch area under `tmp/` is unaffected by the flag.

**`VALIDATE_MODE`:** Unchanged. Validation severity is orthogonal to which contract is being checked. Both flag states respect `VALIDATE_MODE`.
