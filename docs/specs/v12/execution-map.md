# openwrt-docs4ai v12 Execution Map

## Transition Note

This document is being updated for the V5a release-tree contract. When `ENABLE_RELEASE_TREE=true`, late-stage scripts produce output into `release-tree/` instead of directly into `OUTDIR`. See [feature-flag-contract.md](../specs/v12/feature-flag-contract.md) and [release-tree-contract.md](release-tree-contract.md) for details.

## Layer Locations

- `L0`: `tmp/repo-*`
- `L1`: `tmp/L1-raw/{module}/` during build, optionally copied to `openwrt-condensed-docs/L1-raw/{module}/`
- `L2`: `tmp/L2-semantic/{module}/` during build, optionally copied to `openwrt-condensed-docs/L2-semantic/{module}/`
- `L3`: `openwrt-condensed-docs/` root and per-module subdirectories
- `L4`: `openwrt-condensed-docs/{module}/`
- `L5`: `openwrt-condensed-docs/`
- `release-tree/`: validated publishable output (V5a, when `ENABLE_RELEASE_TREE=true`)
- `support-tree/`: ephemeral CI support artifacts (V5a)

## Ordered Script Flow

1. `01-clone-repos.py`
2. `02a-scrape-wiki.py` (independent branch in hosted workflow)
3. `02b` through `02h` (repo-backed extractors, gated on `01`)
4. `03-normalize-semantic.py`
5. `04-generate-ai-summaries.py` when AI enrichment is enabled; it performs its own AI-store preflight before enrichment
6. `05a-assemble-references.py`
7. `05e-assemble-release-tree.py` (V5a, when `ENABLE_RELEASE_TREE=true`) — assembles the release-tree from existing pipeline output; in Phase 4 this script is retired and its functionality is absorbed into the modified late stages
8. `05b-generate-agents-and-readme.py`
9. `05c-generate-ucode-ide-schemas.py`
10. `05d-generate-api-drift-changelog.py`
11. `06-generate-llm-routing-indexes.py`
12. `07-generate-web-index.py`
13. `08-validate-output.py`

Letter suffixes denote scripts that are parallelizable in deployment. Local smoke tests may still execute them sequentially.

`tools/manage_ai_store.py` is the maintained local scratch-first helper.

Hosted Option B topology now runs `02a` in a separate job without waiting on `initialize`, while repo-backed `02b` through `02h` remain in a matrix job that depends on `initialize`.

## Execution Contract Matrix

This matrix defines placement rationale, mutability boundaries, dependencies, and failure power.

| Step | Mutability & atomicity | Primary dependencies | Failure mode in current workflow | Deploy impact |
| --- | --- | --- | --- | --- |
| `01` | Writes L0 clones and `repo-manifest.json` under `WORKDIR`; isolated to initialize job | Git checkout, network access | Hard fail (`initialize` fails) | No deploy; published output unchanged |
| `02a` | Writes only wiki L1 outputs and wiki cache under `WORKDIR` | Internet/wiki availability, `WORKDIR` | Hard fail (`extract_wiki` job fails) | No deploy; published output unchanged |
| `02b`-`02h` | Write module L1 outputs under `WORKDIR`; no publish writes | L0 clone artifacts from `01`, toolchain deps | Hard fail (repo-backed matrix leg fails) | No deploy; published output unchanged |
| `03` | Converts L1 to L2 and promotes staged intermediates inside `OUTDIR`; atomic within process job sandbox | L1 artifacts, metadata sidecars | Hard fail | No deploy; published output unchanged |
| `04` | Optional in-place L2 enrichment in staged `OUTDIR`; no direct publish writes | `SKIP_AI`, cache availability, optional token | If `SKIP_AI=true`, skipped cleanly. If enabled and it fails, hard fail in `process` | No deploy; published output unchanged |
| `05a`-`05d` | Deterministic generation of publish companions inside `OUTDIR` | Staged L2 and registry outputs | Hard fail | No deploy; published output unchanged |
| `05e` (V5a) | Writes `release-tree/` and `support-tree/` from existing OUTDIR output; feature-flagged (`ENABLE_RELEASE_TREE`); retired at Phase 4+ when late stages write directly into `release-tree/` | Complete staged OUTDIR from `05a` through `07`; only runs when `ENABLE_RELEASE_TREE=true` | Hard fail in process (but only runs when flag is true) | No deploy if fails; existing OUTDIR output unchanged |
| `06` | Builds routing/index artifacts inside `OUTDIR` | L2 metadata and reference outputs | Hard fail | No deploy; published output unchanged |
| `07` | Generates `index.html` inside `OUTDIR` | Prior index inputs | Hard fail | No deploy; published output unchanged |
| `08` | Validation gate over full staged `OUTDIR`; no external writes | Complete staged corpus | Hard fail on hard checks | No deploy; published output unchanged |
| `deploy` | `rsync -a --delete` from staging into `openwrt-condensed-docs/` and optional bot commit | Successful `process` job and `final-staging` artifact | Hard fail in deploy only | Only step that can change published output |

## Return-State Guarantees

1. If any `process`-phase script fails, `final-staging` is not promoted and deploy does not run.
2. Because promotion is isolated to the deploy job, partially generated outputs from `03` through `08` stay sandboxed in runner staging.
3. This means a failed `08` cannot publish a mismatched `07` web index to the committed output tree.
4. `SKIP_AI=true` is the explicit optional path for AI enrichment; AI failure is not ignored once the AI step is enabled.

## Key Handoffs

- `01` produces cloned repositories and any repo manifest data required by downstream stages.
- `02*` scripts write L1 markdown plus `.meta.json` sidecars.
- `02b` now exposes import-safe helper surfaces for fenced-block normalization and example fixups so targeted tests can import it directly.
- `03` reads only L1 plus metadata and writes L2 plus a cross-link registry before promoting stable intermediates into `OUTDIR`.
- `03` is also the correct place for bounded module-specific cleanup that should not mutate L1 raw retention; the current live example is wiki-only cleanup for residual DokuWiki and pandoc artifacts.
- `04` mutates staged L2 files in place when enabled.
- `05` consumes staged L2 files and emits skeletons plus monolithic references.
- `05e` (V5a transition) reads from existing `OUTDIR` output and writes the V5a `release-tree/` layout with renamed files (`map.md`, `bundled-reference.md`, `chunked-reference/`); it also moves support-only artifacts into `support-tree/`. When `ENABLE_RELEASE_TREE=true` at Phase 4+, `05a` through `08` write directly into `release-tree/` and `05e` is retired.
- `06*` scripts consume staged L2 metadata and generated references to emit maps, agent instructions, IDE schemas, and telemetry.
- `07` consumes the map outputs and writes the HTML landing page.
- `08` validates the full `OUTDIR` tree and now exposes import-safe parsing helpers for direct unit coverage.

## Observability Baseline

Current hosted logs expose started/completed timestamps per job and per step via `gh run view --json jobs`.

Example timing snapshot from successful run `22901854476`:

- `initialize`: ~31s total, with `Clone repositories` ~9s
- `extract_wiki (02a-scrape-wiki.py)`: ~211s
- `process`: ~56s
- `deploy`: ~18s

Current workflow observability artifacts now include:

- extractor-level status manifests (`extract-status-*`)
- an always-generated `extract-summary` artifact
- a `process-summary` staging contract artifact
- an always-generated `pipeline-summary` artifact

These artifacts are intended to be the first-stop troubleshooting surface before deep log forensics.

## Scope Note

The current AI-alignment slice keeps `04` as the single numbered AI stage and
moves local review, audit, validation, and promotion into `tools/manage_ai_store.py`.
Deeper model-selection and quality-scoring work remains deferred.

## High-Value Debugging Paths

- If the issue is stale or malformed wiki prose in committed outputs, inspect `02a` for source/cache behavior and `03` for semantic cleanup.
- If the issue is misclassified ucode examples or false syntax warnings, inspect `02b` and `08` together because the extractor and validator now share regression coverage boundaries.
- If the issue is missing, stale, or structurally invalid AI summaries, inspect `04`, `tools/manage_ai_store.py`, and the `data/base/` plus `data/override/` store roots together.
- If the issue is missing or overwritten generated outputs, inspect the workflow `process` to `deploy` handoff because `staging/` is now the authoritative promotion source.
- If the issue is only visible in committed `openwrt-condensed-docs/`, compare it against the focused corpus sanity snapshot from `tests/pytest/pytest_03_wiki_corpus_sanity_test.py` to decide whether the repo tree is stale or the normalization logic is still wrong.

## Required Environment Variables

- `WORKDIR`
- `OUTDIR`
- `SKIP_WIKI`
- `SKIP_AI`
- `WIKI_MAX_PAGES`
- `MAX_AI_FILES`
- `VALIDATE_MODE`
- `ENABLE_RELEASE_TREE` (V5a; default `false`; when `true`, activates `05e-assemble-release-tree.py` and the release-tree validation path in `08`)

## Required Schema Facts

- L1 files are pure markdown and must not begin with YAML frontmatter.
- L1 sidecars are `.meta.json` files stored beside the markdown file.
- L2 files require YAML frontmatter with at least `title`, `module`, `origin_type`, `token_count`, and `version`.
- L4 files use one top-level YAML block for the full monolith rather than reusing L2 frontmatter inline.

## Verified Execution Priority

The first required execution proof remains local and sequential. GitHub Actions is now a verified second-stage execution and publication layer, so pipeline debugging should distinguish between local logic regressions and remote promotion or cache-state effects.
