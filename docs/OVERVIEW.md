# openwrt-docs4ai Maintainer Overview

This directory is the active maintainer documentation surface for the repository. Use it for current contracts, operator workflows, architecture, and roadmap context. Historical V12 material and transitional V13 scaffold content have been moved out of the active path.

## Recommended Read Order

1. [GETTING_STARTED.md](GETTING_STARTED.md) for setup, validation commands, and the day-one maintainer workflow.
2. [ARCHITECTURE.md](ARCHITECTURE.md) for the layer model, repository zones, and the current document taxonomy.
3. The active specs under [specs](specs/) for release-tree, routing, provenance, stage order, and cookbook authoring.
4. The operator guides under [guides](guides/) when you need a specific procedure such as AI-store review and promotion.

## Active Document Map

| Path | Role |
| --- | --- |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Local setup, validation commands, AI-store workflow entry points, and CI basics |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Durable architecture, repository zones, layer model, and archive policy |
| [specs/release-tree-contract.md](specs/release-tree-contract.md) | Public output contract for the published `release-tree/` layout |
| [specs/pipeline-stage-catalog.md](specs/pipeline-stage-catalog.md) | Stage ordering, stage ownership, and rerun sequences |
| [specs/script-dependency-map.md](specs/script-dependency-map.md) | Per-script read/write contract and dependency summary |
| [specs/schema-definitions.md](specs/schema-definitions.md) | Data and filesystem contracts for L1, L2, and the published routing surfaces |
| [specs/glossary-and-naming-contract.md](specs/glossary-and-naming-contract.md) | Canonical field names, module names, origin types, and naming rules |
| [specs/regeneration-rules.md](specs/regeneration-rules.md) | Hosted trigger rules, local rerun expectations, and overlay behavior |
| [specs/cookbook-authoring-spec.md](specs/cookbook-authoring-spec.md) | Durable cookbook authoring contract extracted from the V13 implementation plan |
| [guides/runbook-ai-summary-operations.md](guides/runbook-ai-summary-operations.md) | Scratch-first AI-store workflow and promotion procedures |
| [roadmap/deferred-features.md](roadmap/deferred-features.md) | Deferred V13 work and known soft deferrals |
| [plans/v13](plans/v13/) | V13 planning and debrief material |
| [archive](archive/) | Historical plans, retired specs, and superseded helper docs |

## What Is No Longer Active

- `docs/specs/v12/` is archived. It is useful for history, not for current implementation guidance.
- `docs/docs-new/` was a temporary V13 scaffold. Its durable content has been promoted into the active taxonomy.
- `docs/helpers/` was a transitional reference bucket and is now historical material.

## Working Rules

- Treat active specs under `docs/specs/` as the current contract surface.
- Treat `README.md`, `DEVELOPMENT.md`, and `CLAUDE.md` as high-level repo entry points that should stay aligned with the active docs set.
- When a change alters stage order, output layout, provenance fields, or operator workflow, update the relevant active spec or guide in the same change.
- When older material still matters for context, keep it under `docs/archive/` rather than leaving it in the active navigation path.