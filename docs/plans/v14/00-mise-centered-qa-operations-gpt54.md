## Plan: Mise-Centered QA Operations

Adopt Variant 1 with a stricter and more explicit operational contract: `mise` becomes the canonical human and agent task surface, while Python remains the source of truth for stage sequencing, cache validation, container execution, and AI-mode semantics. Durable mutable caches move out of `tmp/` into a repo-local `.cache/` namespace, `AI_MODE=skip|stored|generate` becomes the canonical stage-04 contract, and public task names describe exactly what they do: smoke, refresh, cached proof, AI generate, and full proof.

**Steps**
1. Phase 1: Reframe the storage taxonomy and ignore policy.
   - keep per-run evidence under `tmp/ci/qa/<timestamp>/`
   - keep per-run pipeline scratch under `tmp/pipeline-*/`
   - move durable mutable shared caches to `.cache/shared/`
   - use `.cache/shared/wiki/http-metadata/` for last-modified and request metadata
   - use `.cache/shared/wiki/l1-raw/` for reusable wiki artifacts if the refresh contract is expanded to match CI more closely
   - keep `static/data/base/`, `static/data/override/`, `static/cookbook-source/`, and `static/release-inputs/` as authoritative checked-in inputs, not caches
   - keep `vendors/` as vendored dependencies, not caches
   - update `.gitignore` so `.cache/` or at minimum `.cache/shared/` is ignored while a tracked `.cache/README.md` remains visible; do not keep mutable machine-local caches tracked just because `.cache/` is currently not ignored
   - add a tracked `.cache/README.md` that defines the shared cache layout, cold-start expectations, and which paths are safe to delete locally
   - change `DEFAULT_WIKI_CACHE_DIR` in the orchestrator and `QA_WIKI_CACHE_DIR` in `mise.toml` atomically so the documented cache root and the runner default cannot drift
   - if the team wants tracked seed data later, place it under an explicit seed or fixture path rather than under `.cache/`
2. Phase 2: Make `mise` the operator contract, not the pipeline engine.
   - use `mise.toml` to centralize public task names, descriptions, shared env, and task dependencies
   - keep the project-root `mise.toml` as the authoritative shared task definition and avoid redefining the same QA task names in parent configs or `mise.local.toml`, because mise replaces tasks wholesale by name across config layers
   - keep numbered stage execution, container bootstrapping, Testcontainers behavior, artifact collection, and cache-cold validation in Python
   - standardize docs on explicit task invocation without relying on shorthand: keep repo-guaranteed copy-paste examples on `vendors\\mise\\bin\\mise.exe run <task>` for now, and reserve bare `mise run <task>` for conceptual descriptions unless a later bootstrap follow-up replaces the vendored entrypoint
   - prefer task descriptions and a small stable task menu over many bespoke wrapper scripts
3. Phase 3: Replace boolean AI control flags with a single mode.
   - make `AI_MODE=skip|stored|generate` the canonical contract across orchestrator, stage 04, config, and docs
   - centralize `AI_MODE` parsing and `skip_ai` or `write_ai` derivation in one helper in `lib/config.py`, and have stage 04, the orchestrator, smoke helpers, and workflow glue consume that shared mapping
   - add `AI_MODE` to the orchestrator's forwarded container env list during the compatibility window so task-level env settings actually reach the container
   - migrate the GitHub Actions `process` job env block to emit `AI_MODE` derived from the new workflow input and compat fallback, and retire workflow-level `WRITE_AI` forwarding at the same time so CI exercises the same canonical contract as local runs
   - `skip` means stage 04 does not execute
   - `stored` means stage 04 executes in stored-summary mode with no API generation
   - `generate` means stage 04 executes and may generate missing summaries when a token is available
   - implement a temporary compatibility shim only where needed: if `AI_MODE` is absent but legacy `SKIP_AI` or `WRITE_AI` is present, translate once and emit a deprecation note; treat `AI_MODE` as the source of truth immediately in docs and tasks
   - include `tools/manage_ai_store.py` in the migration surface for `AI_MODE` immediately so its deliberate stage-04 invocation also uses the canonical mode contract rather than relying on the boolean compatibility shim indefinitely
4. Phase 4: Replace ambiguous task names with explicit operation names.
   Public tasks:
   - `qa-smoke` — cheapest Docker-backed proof
   - `qa-wiki-refresh` — refresh the reusable wiki cache from upstream and validate stage `02a`
   - `qa` — default cached local proof; full stage `01` through `08`; requires a warm wiki cache; runs with `AI_MODE=stored`
   - `qa-ai-generate` — full stage `01` through `08` cached local proof with `AI_MODE=generate`; requires a warm wiki cache
   - `qa-full` — broadest local proof; refresh wiki cache, then run the full AI-generate proof
   Internal hidden tasks inside `mise.toml`:
   - one hidden task for the cached full run in stored mode
   - one hidden task for the cached full run in generate mode
   - optionally one hidden support task for common runner invocation if that reduces duplication without obscuring behavior
   - during the transition, add hidden deprecated compatibility tasks for `qa-stage01`, `qa-ai`, and `qa-wiki-cache` that print the rename guidance and forward to the new task names for one release cycle
5. Phase 5: Use `mise` features that reduce drift and avoid the ones that duplicate Python logic.
   Use:
   - `[env]` for shared paths like `QA_RESULTS_ROOT`, `QA_SHARED_CACHE_ROOT`, and `QA_WIKI_CACHE_DIR`
   - per-task `description`
   - per-task `env` overrides for `AI_MODE`
   - `depends` for `qa-full` chaining into `qa-wiki-refresh` plus the generate proof, but only if native Windows validation confirms the vendored mise binary executes those dependencies reliably; otherwise fall back to a sequential wrapper task
   - `hide = true` for internal implementation tasks
   - a deliberate `min_version` bump if newer task metadata or dependency semantics are required, rather than assuming older mise releases will behave the same
   - `run_windows` only when necessary; prefer forward-slash paths in commands where possible only after verifying them on the supported PowerShell baseline, otherwise keep the escaped backslash form instead of changing syntax cosmetically
   - `mise config ls` as a troubleshooting and validation tool to surface config precedence and detect unexpected parent or local overrides
   Avoid for this change:
   - migrating the whole repo toolchain into mise-managed `python`, `node`, or `pandoc`
   - `usage` fields that duplicate the existing `argparse` interface in `tests/qa_pipeline_orchestrator.py`
   - remote tasks, task inheritance, or dynamic stage discovery
   - storing tokens or other secrets in committed `mise.toml`; use existing environment variables or `mise.local.toml` for machine-local overrides instead
   - relying on `mise activate` for correctness on native Windows; keep the contract on `mise run`
   Defer:
   - `mise.lock` and tool-version locking, unless the repo later decides to let mise own more of the local toolchain
   - `mise generate task-docs`, unless its output format can replace the hand-maintained docs without introducing another source of drift
6. Phase 6: Encode Variant 1 behavior precisely in the runner.
   - `qa` must fail clearly and immediately when the wiki cache is cold, with a remediation message to run `qa-wiki-refresh`
   - a "warm" wiki cache must mean more than directory existence: require a refresh sentinel written only by a successful `qa-wiki-refresh` run plus expected cache content so an empty `mkdir` cannot fool the pre-flight check
   - `qa-wiki-refresh` should write a small sentinel manifest such as `.cache/shared/wiki/cache-state.json` only after a successful refresh, and `qa` or `qa-ai-generate` should require that sentinel before proceeding
   - `qa-ai-generate` must also require a warm wiki cache and fail clearly if it is absent
   - `qa-full` is the only public task allowed to refresh the wiki cache automatically as part of its contract
   - `qa-ai-generate` should also fail clearly when generation is requested but no token is configured, instead of silently degrading into stored-summary mode under a task named `generate`, and that pre-flight must happen in the orchestrator before the container starts
   - keep advanced stage-level selection on the Python CLI with `--only-stage`, `--result-root`, `--wiki-cache-dir`, and a new `--ai-mode` flag rather than exploding the top-level task menu
7. Phase 7: Roll the rename through the whole repo surface in one disciplined pass.
   - rename public task references in `README.md`, `tools/testing/README.md`, `DEVELOPMENT.md`, `AGENTS.md`, `CLAUDE.md`, and `tests/README.md`
   - update orchestrator and helper tests to assert the new names, task-level `AI_MODE` behavior, sentinel-based cold-cache detection, and missing-token pre-flight failures
   - update workflow and spec docs that currently describe `skip_ai` and `SKIP_AI`
   - keep workflow_dispatch backward compatibility for one transition window by accepting both `ai_mode` and deprecated `skip_ai`, with `ai_mode` taking precedence and a clear deprecation note for external callers
   - preserve a narrow compatibility layer only where external or manual callers may still use the legacy env names during transition

**Relevant files**
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\mise.toml` — public task menu, task descriptions, shared env, hidden internal tasks, compatibility wrappers, dependency graph, and minimum supported mise version
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\.gitignore` — ignore policy for `.cache/` versus `tmp/`
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\.cache\README.md` — tracked cache layout contract and operator guidance while mutable cache contents remain ignored
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tests\qa_pipeline_orchestrator.py` — authoritative runner behavior, `DEFAULT_WIKI_CACHE_DIR`, `FORWARDED_CONTAINER_ENV_NAMES`, cache-cold failure messaging, sentinel checks, `--ai-mode`, and full-run semantics
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tests\support\smoke_pipeline_support.py` — local helper env construction that still sets `SKIP_AI`
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\lib\config.py` — global env parsing and path defaults for `AI_MODE` and shared cache roots
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\.github\scripts\openwrt-docs4ai-04-generate-ai-summaries.py` — stage-04 environment contract and user-facing help text
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\lib\ai_enrichment.py` — internal stage-04 skip or stored or generate semantics
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tools\manage_ai_store.py` — deliberate AI-store generation and promotion workflow; migrate its stage-04 invocation to `AI_MODE=generate` while keeping the operator docs clearly separate from QA tasks
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\.github\workflows\openwrt-docs4ai-00-pipeline.yml` — workflow_dispatch transition from `skip_ai` to `ai_mode`, process-job env migration to `AI_MODE`, compatibility precedence, and CI parity
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\README.md` — top-level task summary and cache semantics
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tools\testing\README.md` — operator-facing task menu and first-run guidance
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\DEVELOPMENT.md` — maintainer workflow, prerequisites, and troubleshooting
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\AGENTS.md` — future-agent validation order and recommended task selection
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tests\README.md` — advanced runner documentation and flag contract
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\tests\pytest\pytest_16_qa_orchestrator_test.py` — contract tests for task names, cache paths, env names, and first-run failure behavior
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\specs\regeneration-rules.md` — legacy `skip_ai` documentation that will need the new `AI_MODE` language
- `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\specs\pipeline-stage-catalog.md` — workflow input and stage semantics references

**Verification**
1. Run `mise tasks ls`, `mise tasks validate`, and `mise config ls` to confirm the new task graph is internally consistent, the expected project config is active, and no parent or local config is shadowing the QA surface.
2. Confirm `qa-smoke`, `qa-wiki-refresh`, `qa`, `qa-ai-generate`, and `qa-full` are the only public QA tasks shown by default.
3. Confirm `qa` on a cold cache exits early with a message that points directly to `qa-wiki-refresh`.
4. Confirm `qa-wiki-refresh` populates `.cache/shared/wiki/`, writes the refresh sentinel manifest, and leaves per-run evidence under `tmp/ci/qa/<timestamp>/`.
5. Confirm `qa` runs with `AI_MODE=stored` and does not silently generate AI output.
6. Confirm `qa-ai-generate` runs with `AI_MODE=generate` and fails clearly before container startup when generation is requested without a token.
7. Confirm `qa-full` performs the refresh step and then the generate-mode proof in the documented order.
8. Confirm deprecated compatibility tasks or wrappers are hidden or clearly marked during the transition window if they are kept.
9. Confirm docs no longer describe durable shared caches under `tmp/` and no longer present `SKIP_AI` as the primary contract.
10. Confirm copy-paste docs preserve the repo-guaranteed vendored mise entrypoint for now and do not rely on shell activation behavior.
11. Confirm the GitHub Actions workflow now forwards `AI_MODE` into the `process` job env and that CI no longer depends on workflow-level `SKIP_AI` or `WRITE_AI` as the primary contract.
12. Confirm `tools/manage_ai_store.py` uses the canonical `AI_MODE` path for its stage-04 generation flow rather than only the legacy boolean compatibility path.

**Decisions**
- Variant 1 is the selected design.
- Durable mutable caches do not belong under `tmp/`; use `.cache/` for them and ignore that cache path in git.
- Ordinary reusable mutable caches do not belong in `static/`; `static/` stays for checked-in authoritative or seed content only.
- `AI_MODE=skip|stored|generate` is the target contract; legacy booleans are transitional only.
- Wiki uses the verb `refresh`; AI uses the verb `generate`.
- `mise` is the canonical task surface, but Python remains the canonical implementation layer.
- For this refactor, keep `vendors\\mise\\bin\\mise.exe run <task>` as the repo-guaranteed copy-paste invocation in docs and automation; treat bare `mise run <task>` as a conceptual shorthand unless a later bootstrap change replaces the vendored entrypoint.
- Local tokens and personal overrides belong in environment variables or `mise.local.toml`, never in committed `mise.toml`, and local files must not redefine shared QA task semantics.

**Further Considerations**
1. If the team later wants reproducible tool installs through mise rather than only task orchestration, that should be a separate follow-up that evaluates `[tools]`, `.venv` integration, and `mise.lock` without mixing it into this operational refactor.
2. If the repo later wants to replace the vendored mise executable with a committed bootstrap-generated wrapper such as `./bin/mise`, evaluate that as a separate change after the task and cache contracts are stable.
3. If future operators need richer argument handling for public tasks, consider `usage` fields only after deciding which arguments belong in `mise` versus the existing Python CLI.
