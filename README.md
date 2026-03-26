# openwrt-docs4ai

OpenWrt documentation production pipeline for humans, tooling, and LLM workflows.

## What This Repository Does

This repository pulls documentation from multiple OpenWrt-related sources, normalizes it through stable layer boundaries, and publishes compact outputs intended for:

- targeted human lookup
- LLM context ingestion
- IDE and tooling support
- repeatable local and hosted regeneration

The current maintainer surface is the V13 documentation set under `docs/`. The current public output contract is V6. The hosted workflow name still carries the historical `v12` label, but the active repository and output contracts do not.

## Source Families

- OpenWrt wiki pages
- `jow-/ucode`
- `openwrt/luci`
- `openwrt/openwrt`
- hand-authored cookbook content under `content/cookbook-source/`

## Output Model

Generated artifacts live under `openwrt-condensed-docs/` locally.

- `L1-raw/` contains normalized raw Markdown plus sidecar metadata.
- `L2-semantic/` contains semantic Markdown with YAML frontmatter and cross-links.
- `release-tree/` is the only publishable surface.
- `support-tree/` is internal pipeline state and is never published.

The exact output layout is defined in `docs/specs/release-tree-contract.md`.

## Maintainer Guidance

- Read `docs/OVERVIEW.md` for the active maintainer doc map.
- Read `DEVELOPMENT.md` for setup, validation, and CI operations.
- Read `docs/ARCHITECTURE.md` for repository zones, layer model, and doc taxonomy.
- Read `docs/specs/` for the active technical contracts.
- Read `docs/guides/runbook-ai-summary-operations.md` for the AI-store workflow.
- Treat `docs/archive/` as historical context only.

## Status

- local deterministic validation remains the first gate
- GitHub Actions is the verified remote execution and publication path
- the cookbook module and LuCI type surface are now part of the active contract
- publication targets consume the validated `release-tree/` surface rather than the full internal staging tree

## License

Licensed under the Apache License, Version 2.0. See `LICENSE` for details. Generated documentation derives from upstream OpenWrt project sources and retains their respective upstream licensing context.
