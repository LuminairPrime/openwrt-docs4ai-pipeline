# v12 Bug Log

This is the active bug log for the current stabilization pass.

Rules:

- Only log issues that were reproduced locally or verified directly in the current repository state.
- Treat `docs/archive/v12/v12-bugs-3-9-opus.md` and `docs/archive/v12/v12-bugs-3-9.md` as historical context only.
- Track status transitions clearly: `open`, `fixed-pending-test`, `fixed-and-verified`, `deferred`, `not-reproduced`.

## Active Entries

| ID | Status | Area | Summary | Notes |
| --- | --- | --- | --- | --- |
| LOCAL-001 | fixed-and-verified | local-tests | `tests/openwrt-docs4ai-00-smoke-test.py` referenced obsolete script names and phase numbers | Rewritten as a sequential fixture-backed runner for the current `03` through `08` flow. Verified with `python tests/openwrt-docs4ai-00-smoke-test.py`. |
| LOCAL-002 | fixed-and-verified | local-tests | `tests/00-smoke-test.py` seeded `tmp/.L1-raw` instead of `tmp/L1-raw` | Rewritten as a deterministic fixture-backed harness using the current non-dotted path contract. Verified with `python tests/00-smoke-test.py`. |
| LOCAL-003 | fixed-and-verified | documentation | Root documentation authority boundaries were unclear and active specs lived beside archival planning material | Fixed by the docs/specs and docs/archive reorganization in the current milestone. |
| LOCAL-004 | fixed-and-verified | documentation | `CONTRIBUTING.md` duplicated maintainer guidance without providing meaningful contributor process | Removed and folded into `DEVELOPMENT.md` as part of repo simplification. |
| LOCAL-005 | fixed-and-verified | normalization | `03-normalize-semantic.py` over-protected document bodies during cross-link injection and over-broadened deprecation detection across sections | Fixed by narrowing header protection, protecting frontmatter explicitly, and limiting deprecation scans to the current section. Verified by both smoke runners. |
| LOCAL-006 | fixed-and-verified | assembly-indexing | `05-assemble-references.py`, `06b-generate-agents-md.py`, and `06c-generate-ide-schemas.py` contained runtime or output-shape defects surfaced by fixture tests | Fixed by correcting monolith assembly, rebuilding AGENTS summary generation, and repairing the ucode `.d.ts` generator. Verified by both smoke runners. |
| LOCAL-007 | fixed-and-verified | ai-enrichment | `04-generate-ai-summaries.py` only worked safely in skip mode and could not be exercised locally without external tokens | Fixed by adding a cache-backed local enrichment path and verifying it with `python tests/00-smoke-test.py --run-ai` and `python tests/openwrt-docs4ai-00-smoke-test.py --run-ai`. |

## Verification Notes

- Update this file when a bug is reproduced, fixed, or explicitly not reproduced.
- When a bug is fixed, note the validation command or smoke test that proved it.