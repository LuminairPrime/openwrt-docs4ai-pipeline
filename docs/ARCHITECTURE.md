# openwrt-docs4ai Architecture

## Purpose

This repository is a documentation production pipeline, not an application runtime. It gathers OpenWrt documentation from upstream repositories, the OpenWrt wiki, and hand-authored cookbook content; normalizes that material through stable intermediate layers; and publishes compact outputs for humans, IDE tooling, and LLM workflows.

The active operating model is Windows-first local validation with GitHub Actions as the verified remote execution and publication path. The current public output contract is V6. The workflow name still carries the historical `v12` label, but the generated output and maintainer documentation now follow the V13/V6 contract set.

## Documentation Surfaces

This repository has two distinct documentation surfaces:

- The source repository is the maintainer surface. Authoritative docs live in `README.md`, `DEVELOPMENT.md`, `CLAUDE.md`, and the active files under `docs/`.
- The generated corpus is the published navigation surface. Locally it lives under `openwrt-condensed-docs/release-tree/`; externally it is shipped as the direct-root `release-tree/` layout.

`openwrt-condensed-docs/` is an internal staging root only. It must never appear in public URLs or user-facing path contracts.

## Repository Zones

| Path | Role | Notes |
| --- | --- | --- |
| `.github/scripts/` | Numbered pipeline scripts | Whole numbers define stage boundaries; letter suffixes define sibling scripts inside one stage family. |
| `.github/workflows/` | Hosted workflow definitions | The main workflow is still named `openwrt-docs4ai pipeline (v12)`, but it runs the current V13/V6 pipeline. |
| `lib/` | Shared Python support code | Shared config, provenance helpers, AI-store helpers, and extraction utilities. |
| `tools/` | Non-numbered maintainer utilities | Local support CLIs such as `manage_ai_store.py`. |
| `tests/` | Local verification surface | Focused pytest suites, smoke runners, and lint wrappers. |
| `content/cookbook-source/` | Hand-authored cookbook source | Ingested by stage `02i` into the cookbook module. |
| `release-inputs/` | Overlay inputs | `release-include/` for common overlays, plus Pages-only and release-repo-only overlays. |
| `docs/` | Active maintainer docs | Overview, getting started, architecture, active specs, guides, roadmap, plans, and archive. |
| `docs/archive/` | Historical material | Preserved for context only; never authoritative over active docs. |
| `openwrt-condensed-docs/` | Local generated output root | Stable internal output root; do not treat it as the source of truth for maintainer docs. |
| `tmp/` | Ephemeral working area | Scratch space for local runs, CI artifacts, and rollback snapshots. |
| `templates/` | Static templates | Keep only templates that still have a real consumer. |

## Layer Model

| Layer | Meaning | Primary location | Lifetime |
| --- | --- | --- | --- |
| `L0` | Upstream source clones and fetched inputs | `tmp/repo-*` | Ephemeral |
| `L1` | Raw normalized Markdown plus `.meta.json` sidecars | `WORKDIR/L1-raw/{module}/` | Generated |
| `L2` | Semantic Markdown with YAML frontmatter and cross-links | `OUTDIR/L2-semantic/{module}/` | Generated |
| `L3` | Published navigation surfaces | `OUTDIR/release-tree/` | Published |
| `L4` | Published reference surfaces | `OUTDIR/release-tree/{module}/` | Published |
| `L5` | Telemetry and drift outputs | `OUTDIR/support-tree/telemetry/` | Internal |

For local committed inspection, the default `OUTDIR` is `openwrt-condensed-docs/`. In hosted workflow runs, `OUTDIR` is overridden to `staging/`.

## Pipeline Shape

1. `01` clones upstream repositories into L0.
2. `02a` scrapes the wiki and `02i` ingests hand-authored cookbook content without waiting on clones.
3. `02b` through `02h` extract repo-backed content into L1 after `01` completes.
4. `03` normalizes L1 content into L2 and emits cross-link state.
5. `04` optionally enriches L2 with AI summary metadata from the AI store or live generation.
6. `05a` through `05e` generate release-tree reference surfaces, companion docs, IDE surfaces, and telemetry.
7. `06` generates routing indexes.
8. `07` applies overlays, emits `index.html`, and materializes `support-tree/`.
9. `08` validates the staged output contract.

Use `docs/specs/pipeline-stage-catalog.md` for stage ordering and rerun sequences. Use `docs/specs/script-dependency-map.md` for the per-script read/write contract.

## Current Documentation Taxonomy

| Path | Role |
| --- | --- |
| `docs/OVERVIEW.md` | Maintainer entry point and document map |
| `docs/GETTING_STARTED.md` | Setup, validation, and first-step workflow |
| `docs/ARCHITECTURE.md` | Durable architecture, layer model, and repository zones |
| `docs/specs/` | Active technical contracts and data/layout specifications |
| `docs/guides/` | Operator workflows and procedural guidance |
| `docs/roadmap/` | Deferred or future-facing work that is still relevant |
| `docs/plans/v13/` | Working and historical V13 planning material |
| `docs/archive/` | Retired specs, superseded plans, and helper material |

## Local-First Verification Model

- Start with focused pytest, smoke tests, and `tests/check_linting.py`.
- Use the smallest proof that can fail before escalating to hosted workflow validation.
- Treat GitHub Actions as the remote confirmation path after local validation, not as the first debugger.
- Prefer summary artifacts such as `pipeline-summary` and `extract-summary` before raw CI logs.

## Remote Publication Contract

- Hosted workflow runs build into `staging/` and validate there first.
- Successful deploys synchronize staged output into `openwrt-condensed-docs/` and publish the validated `release-tree/` to external targets.
- Generated source-repo update commits use the `docs: v12 auto-update YYYY-MM-DD` format because the workflow name and automation history still use the older label.
- External publication targets receive only the `release-tree/` subtree plus the appropriate overlay material.

## Archive Policy

Archived material is preserved for historical context, review evidence, and recovery of older design decisions. It is never authoritative over active specs, active guides, or verified code behavior. When archive content conflicts with active documentation or the live pipeline, the active contract wins.
