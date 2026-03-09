# v12 Implementation Status

## Current State

v12 contains substantial implementation work, but the repository is not yet treated as fully verified.

The current authoritative position is:

- code exists for the numbered pipeline stages
- documentation and local test surfaces had drifted out of sync with the current script layout
- local-first stabilization is now the active development strategy
- GitHub Actions behavior is not yet treated as verified for release automation

## Verification Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Script implementation surface | present | `.github/scripts/` contains the numbered v12 pipeline family |
| Active spec structure | complete | Active specs moved to `docs/specs/v12/` on 2026-03-09 |
| Archive separation | complete | Historical planning and bug notes moved to `docs/archive/v12/` |
| Root documentation accuracy | complete | Root docs now point to the current architecture, specs, and local smoke paths |
| Deterministic local smoke test | verified | `python tests/00-smoke-test.py` passes locally |
| Sequential local smoke runner | verified | `python tests/openwrt-docs4ai-00-smoke-test.py` passes locally |
| Local AI-summary integration | verified | Cache-backed local AI path passes via `--run-ai` without requiring a live token |
| GitHub Actions remote verification | not yet verified | Deferred until a remote test repository exists |

## Historical Note

Older status claims from early March 2026 described the pipeline as fully complete and production-ready. Those claims are preserved as historical context only and are not the active engineering position unless supported by fresh local or remote verification.

## 2026-03-09 Milestone Log

### Milestone 1: Documentation and authority reset

- Created `docs/ARCHITECTURE.md` as the durable repository architecture reference.
- Split active v12 specifications into `docs/specs/v12/`.
- Moved historical planning and bug-review material into `docs/archive/v12/`.
- Removed `CONTRIBUTING.md` and consolidated maintainer guidance into `DEVELOPMENT.md`.
- Added an active stabilization plan and an active bug log under `docs/specs/v12/`.

### Milestone 2: Local smoke repair and runtime hardening

- Rewrote `tests/00-smoke-test.py` into a deterministic fixture-backed regression harness for the current L1 to L5 contract.
- Rewrote `tests/openwrt-docs4ai-00-smoke-test.py` into a sequential local runner with fixture-backed default mode and optional extractor mode.
- Repaired runtime issues in `03`, `04`, `05`, `06b`, and `06c` that were surfaced by the local smoke path.
- Verified local AI enrichment in cache-backed mode without external model calls.

### Next Priority

Generate and measure persistent local L1 and L2 outputs, then use those measurements to decide the long-term storage policy for those layers.

