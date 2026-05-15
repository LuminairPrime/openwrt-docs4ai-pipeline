# AGENTS.md — Source Repo Validation Guide

## Validation Order

1. Run `python tools/testing/run_source_validation.py` for source-only diffs.
2. Run `vendors\\mise\\bin\\mise.exe run qa-stage01` for the cheapest Docker-backed proof.
3. Run `vendors\\mise\\bin\\mise.exe run qa` for the full Linux-mirrored pipeline proof.
4. Run `vendors\\mise\\bin\\mise.exe run qa-ai` when the AI stage or AI-facing metadata is part of the change.
5. If the vendored `mise` binary is unavailable, fall back to `.venv\\Scripts\\python.exe tests\\qa_pipeline_orchestrator.py`.

## Rules

1. Do not manually chain numbered `.github/scripts/openwrt-docs4ai-*` scripts for end-to-end validation.
2. Treat any non-zero exit code from the QA runner as unresolved unless you are explicitly triaging a known pre-existing content defect.
3. Inspect `tmp/ci/qa/<timestamp>/summary.json` and the per-stage logs before relying on raw terminal scrollback.

## Notes

- `tests/qa_pipeline_orchestrator.py` mirrors stages `01` through `08` inside an ephemeral Linux container.
- `qa-stage01` is the cheapest Docker-backed proof, `qa` is the full mirror, and `qa-ai` enables the cache-backed AI stage without changing the AI-store promotion workflow.
- `qa-wiki-cache` warms or refreshes the shared wiki cache under `tmp/ci/qa/shared/wiki-cache/`, and every `qa*` task restores and persists that cache automatically.
- `--skip-wiki` remains available from `tests/qa_pipeline_orchestrator.py` for CI-parity diagnosis, but it is not the default maintainer proof path.
- `tools/testing/` remains the fast operator surface for source validation, targeted pytest, and smoke runners.
- `QA_CONTAINER_IMAGE` and `QA_MAX_AI_FILES` can override the default container image and AI-file budget without editing the task definition.