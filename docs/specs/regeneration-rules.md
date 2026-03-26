# Regeneration Rules

**Version:** V13  
**Status:** Active

This document defines hosted trigger behavior, local rerun expectations, overlay rules, and AI-store regeneration boundaries.

## Hosted Trigger Rules

The hosted workflow runs the full pipeline. It does not expose stage targeting.

### Push

- Trigger: push to `main`
- Behavior: full `01 -> 08` pipeline run

### Schedule

- Trigger: monthly CRON at `13:00 UTC` on the first day of the month
- Behavior: full `01 -> 08` pipeline run

### Manual dispatch

- Trigger: `workflow_dispatch`
- Inputs: `skip_wiki`, `skip_buildroot`, `skip_ai`, `max_ai_files`
- Behavior: full `01 -> 08` pipeline run with the selected skip knobs

The workflow does not support a `start_stage` input. If you need a partial rerun, use local script invocations with the correct prerequisite state already present.

## Local Partial Reruns

Local partial reruns are allowed when the maintainer knows earlier-stage artifacts are still valid.

- Use [pipeline-stage-catalog.md](pipeline-stage-catalog.md) for the supported rerun sequences.
- Do not attempt a partial rerun after deleting `WORKDIR` or `OUTDIR` state that the target stage depends on.
- When in doubt, rerun the smallest earlier stage that re-establishes a trustworthy state.

### Overlay-only local refresh

If only `release-inputs/` changed and the generated surfaces are otherwise valid, the minimal local proof is:

1. rerun `07`
2. rerun `08`

In CI, a push that changes `release-inputs/` still runs the full hosted workflow.

## Overlay System

Stage `07` merges static overlay files into the final published output.

### Overlay directory structure

```text
release-inputs/
├── release-include/          common overlay for all publication surfaces
│   ├── README.md
│   ├── cookbook/AGENTS.md
│   ├── luci/AGENTS.md
│   └── ucode/AGENTS.md
├── pages-include/            Pages-only overlay
└── release-repo-include/     release-repo-only overlay
```

### Merge rules

| Scenario | Behavior |
| --- | --- |
| overlay file exists and no generated counterpart exists | copy the overlay file |
| overlay file exists and a generated counterpart exists | overlay file wins |
| generated file exists and no overlay file exists | generated file stands |
| overlay targets a missing module directory | stage `07` logs a warning and skips it |

Overlay application must be idempotent.

## Module Lifecycle Rules

### Adding a module

1. Add the extractor or ingest stage.
2. Register the module and its category/description in `lib/config.py`.
3. Register provenance rules in `lib/source_provenance.py` when new origin types are introduced.
4. Add overlay material under `release-inputs/release-include/{module}/` if the module ships an `AGENTS.md` file.
5. Update workflow wiring, tests, and active specs.
6. Run the full validation path and confirm `08` passes.

### Removing a module

1. Remove or disable the extractor.
2. Remove the module from config and routing metadata.
3. Remove or archive overlay content for the module.
4. Remove fixtures and tests that still assume the module exists.
5. Update the published contract documents.

### Renaming a module

Renaming a published module is a breaking contract change. It requires:

1. an explicit contract update in [release-tree-contract.md](release-tree-contract.md)
2. corresponding routing and overlay updates
3. migration handling for any published links or downstream consumers

## AI Summary Regeneration Rules

Stage `04` is the only numbered AI enrichment stage.

| Condition | Behavior |
| --- | --- |
| `skip_ai=true` or `SKIP_AI=true` | stage `04` is skipped |
| local validation without `--run-ai` | cached AI data is used; no live generation |
| scratch review via `manage_ai_store.py --option review` | scratch store is prepared, `04` runs against scratch state, validation and audit follow |
| promotion via `manage_ai_store.py --option promote` | reviewed scratch JSON is copied into `data/base/` and revalidated |

Use [../guides/runbook-ai-summary-operations.md](../guides/runbook-ai-summary-operations.md) for the operator workflow.

## Determinism Rules

The pipeline is expected to be deterministic given the same inputs and the same selected skip knobs.

- Running the same stage twice against the same valid prerequisite state should produce the same output apart from expected timestamp fields.
- No stage should depend on undeclared scratch state.
- Timestamps must use ISO 8601 UTC.
- Validation and rerun guidance should assume deterministic output and fail loudly when that assumption breaks.
