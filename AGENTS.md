# AGENTS.md — Source Repo Validation Guide

## Validation Order

1. Run `python tools/testing/run_source_validation.py` for source-only diffs.
2. Run `vendors\\mise\\bin\\mise.exe run qa-smoke` for the cheapest Docker-backed proof.
3. Run `vendors\\mise\\bin\\mise.exe run qa-wiki-refresh` before cached full proofs that need the wiki scraper cache.
4. Run `vendors\\mise\\bin\\mise.exe run qa` for the cached full Linux-mirrored pipeline proof.
5. Run `vendors\\mise\\bin\\mise.exe run qa-ai-generate` when the AI stage or AI-facing metadata is part of the change.
6. Run `vendors\\mise\\bin\\mise.exe run qa-full` when you want the refresh-plus-generate proof in one command.
7. If the vendored `mise` binary is unavailable, fall back to `.venv\\Scripts\\python.exe tests\\qa_pipeline_orchestrator.py`.

## Rules

1. Do not manually chain numbered `.github/scripts/openwrt-docs4ai-*` scripts for end-to-end validation.
2. Treat any non-zero exit code from the QA runner as unresolved unless you are explicitly triaging a known pre-existing content defect.
3. Inspect `tmp/ci/qa/<timestamp>/summary.json` and the per-stage logs before relying on raw terminal scrollback.

## Notes

- `tests/qa_pipeline_orchestrator.py` mirrors stages `01` through `08` inside an ephemeral Linux container.
- `qa-smoke` is the cheapest Docker-backed proof, `qa` is the cached full mirror in `AI_MODE=stored`, `qa-ai-generate` is the cached full mirror in `AI_MODE=generate`, and `qa-full` is the refresh-plus-generate proof.
- `qa-wiki-refresh` warms or refreshes the shared wiki cache under `.cache/shared/wiki/`, and cached `qa*` tasks restore and persist the `http-metadata/` cache payload automatically.
- `--skip-wiki` remains available from `tests/qa_pipeline_orchestrator.py` for CI-parity diagnosis, but it is not the default maintainer proof path.
- `tools/testing/` remains the fast operator surface for source validation, targeted pytest, and smoke runners.
- `QA_CONTAINER_IMAGE` and `QA_MAX_AI_FILES` can override the default container image and AI-file budget without editing the task definition.
