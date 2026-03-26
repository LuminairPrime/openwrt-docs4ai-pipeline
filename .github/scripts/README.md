# .github/scripts — Pipeline Scripts Reference

This directory contains the numbered pipeline stages for openwrt-docs4ai.

Use these docs alongside it:

- [docs/specs/pipeline-stage-catalog.md](../../docs/specs/pipeline-stage-catalog.md) for stage order and rerun guidance
- [docs/specs/script-dependency-map.md](../../docs/specs/script-dependency-map.md) for the per-script read/write contract
- [docs/specs/schema-definitions.md](../../docs/specs/schema-definitions.md) for field and output contracts

## Quick Reference

| Script | Role |
| --- | --- |
| `openwrt-docs4ai-01-clone-repos.py` | clone upstream source repos |
| `openwrt-docs4ai-02a-scrape-wiki.py` | ingest wiki content |
| `openwrt-docs4ai-02b-scrape-ucode.py` | extract ucode content |
| `openwrt-docs4ai-02c-scrape-jsdoc.py` | extract LuCI API content |
| `openwrt-docs4ai-02d-scrape-core-packages.py` | extract OpenWrt core docs |
| `openwrt-docs4ai-02e-scrape-example-packages.py` | extract LuCI example content |
| `openwrt-docs4ai-02f-scrape-procd-api.py` | extract procd content |
| `openwrt-docs4ai-02g-scrape-uci-schemas.py` | extract UCI schema content |
| `openwrt-docs4ai-02h-scrape-hotplug-events.py` | extract hotplug content |
| `openwrt-docs4ai-02i-ingest-cookbook.py` | ingest hand-authored cookbook content |
| `openwrt-docs4ai-03-normalize-semantic.py` | normalize L1 into L2 |
| `openwrt-docs4ai-04-generate-ai-summaries.py` | optional AI enrichment |
| `openwrt-docs4ai-05a-assemble-references.py` | assemble module reference surfaces |
| `openwrt-docs4ai-05b-generate-agents-and-readme.py` | generate root companion docs |
| `openwrt-docs4ai-05c-generate-ucode-ide-schemas.py` | generate ucode type declarations |
| `openwrt-docs4ai-05d-generate-api-drift-changelog.py` | generate telemetry outputs |
| `openwrt-docs4ai-05e-generate-luci-dts.py` | generate LuCI type declarations |
| `openwrt-docs4ai-06-generate-llm-routing-indexes.py` | generate routing indexes |
| `openwrt-docs4ai-07-generate-web-index.py` | finalize overlays and web landing page |
| `openwrt-docs4ai-08-validate-output.py` | validate the staged output |

## Shared Libraries

Scripts import shared code from `lib/`, especially:

- `lib/config.py`
- `lib/extractor.py`
- `lib/source_provenance.py`
- `lib/ai_store.py`
- `lib/ai_store_checks.py`
- `lib/ai_store_workflow.py`
- `lib/ai_enrichment.py`

Do not hardcode `tmp/`, `staging/`, or output paths directly when `lib.config` already defines them.

## AI Summary Stage

Script `04` is the only numbered AI stage.

- It reads `data/base/` and `data/override/`.
- It can migrate legacy cache entries when needed.
- It enriches L2 frontmatter with AI fields.
- It may write new JSON records into `data/base/` when live generation is enabled.

The maintained operator workflow lives outside the numbered pipeline in `tools/manage_ai_store.py`.

Use these references:

- [docs/guides/runbook-ai-summary-operations.md](../../docs/guides/runbook-ai-summary-operations.md)
- [data/base/README.md](../../data/base/README.md)
- [tools/README.md](../../tools/README.md)

## Adding A New Script

1. Name it `openwrt-docs4ai-NN-descriptive-name.py`.
2. Add a clear module-level docstring covering purpose, phase, inputs, outputs, environment variables, and notes.
3. Use `lib.config` for shared paths.
4. Wire it into the hosted workflow when appropriate.
5. Update the active specs under `docs/specs/`.
6. Update this README when the stage surface changes.
