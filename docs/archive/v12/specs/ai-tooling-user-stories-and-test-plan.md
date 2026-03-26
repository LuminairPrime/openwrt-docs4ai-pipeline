# AI Tooling User Stories And Test Plan

## Purpose

This document turns the current AI-tool surface into an operator backlog plus an
acceptance test plan.

The active tool surface is:

- local scratch-first workflow via `tools/manage_ai_store.py`
- committed authority in `data/base/` and `data/override/`
- hosted optional enrichment via stage `04`
- remote verification and publication via the main GitHub Actions workflow

This plan intentionally excludes the retired numbered AI helpers.

## User Stories

### Story 1: Safe Scratch Review

As a local maintainer, I want to prepare and review a scratch AI-store workspace
without touching committed AI data, so I can inspect changes safely before
promotion.

Acceptance criteria:

- `python tools/manage_ai_store.py --option review --no-write-ai --keep-scratch`
  creates a scratch tree under `tmp/ai-summary-run` by default.
- The command completes the `prepare -> generate -> validate -> audit` sequence.
- Committed `data/base/` and `data/override/` remain unchanged.

### Story 2: Bounded Live Generation

As a local maintainer, I want to generate live AI summaries into scratch with an
explicit token source and file cap, so I can expand coverage incrementally and
control cost and risk.

Acceptance criteria:

- `python tools/manage_ai_store.py --option review --write-ai --max-ai-files 5`
  uses a configured token source and reports which one was used.
- The command respects `--max-ai-files`.
- Writes are limited to scratch paths until promotion.

### Story 3: Independent Validation And Audit

As a local maintainer, I want standalone validate and audit actions, so I can
separate structural integrity checks from coverage and hygiene checks.

Acceptance criteria:

- `python tools/manage_ai_store.py --option validate` checks scratch JSON shape,
  title integrity, and hash integrity against the active L2 corpus.
- `python tools/manage_ai_store.py --option audit` checks missing, stale,
  orphan, invalid, and precedence behavior.
- Both actions fail clearly when scratch state is intentionally broken.

### Story 4: Reviewed Promotion Only

As a local maintainer, I want to promote only reviewed scratch base records into
the permanent base store, so canonical summaries move forward only after review.

Acceptance criteria:

- `python tools/manage_ai_store.py --option promote` copies reviewed JSON from
  scratch into `data/base/`.
- Promotion reruns validate and audit checks against the permanent store.
- Promotion does not mutate `data/override/`.

### Story 5: Override Precedence

As a human curator, I want pinned overrides that take precedence over generated
base records, so hand-authored summaries survive regeneration and promotion
cycles.

Acceptance criteria:

- An override created per `data/override/README.md` wins over base resolution.
- Review, promotion, and hosted stage `04` runs do not erase override
  precedence.

### Story 6: Hosted Verification And Publication Control

As a release operator, I want to run the hosted workflow with `skip_ai` and
`max_ai_files` controls, so I can choose between non-AI publication proof and
bounded remote AI verification.

Acceptance criteria:

- Workflow runs obey the inputs defined in
  `.github/workflows/openwrt-docs4ai-00-pipeline.yml`.
- Remote verification is pinned to the pushed commit SHA.
- Published outputs reflect committed authority, not scratch-only state.

### Story 7: Fast Maintainer Regression Proof

As a maintainer changing AI tooling, I want one-command local regression proof
plus AI-specific smoke checks, so I can catch workflow drift, output drift, and
AI propagation regressions before pushing.

Acceptance criteria:

- `python tests/run_smoke_and_pytest.py` passes.
- The AI-specific smoke path also passes when enabled.

## Test Plan

## Track A: Fast Regression

1. Run `python tests/run_pytest.py`.
2. Run `python tests/run_smoke.py`.
3. Treat this as the cheapest pre-push proof for Story 7.

Expected result:

- focused pytest passes
- maintained smoke stages pass

## Track B: Cache-Backed AI Placement

1. Run `python tests/run_smoke.py --run-ai`.
2. Optionally run `python tests/smoke/smoke_00_post_extract_pipeline.py --run-ai`
   when you want a narrower proof.
3. Optionally run `python tests/smoke/smoke_01_full_local_pipeline.py --run-ai`
   when you want the sequential lane directly.

Expected result:

- stage `04` AI placement succeeds in the cache-backed local lane
- downstream generated outputs still validate

## Track C: Scratch-First CLI Acceptance

1. Run `python tools/manage_ai_store.py --option review --no-write-ai --keep-scratch`.
2. Run `python tools/manage_ai_store.py --option validate --scratch-root tmp/ai-summary-run`.
3. Run `python tools/manage_ai_store.py --option audit --scratch-root tmp/ai-summary-run`.
4. Run `python tools/manage_ai_store.py --option cleanup`.

Expected result:

- the scratch-first workflow completes cleanly
- committed authority remains unchanged until promotion

## Track D: Live AI And Negative Paths

1. Export `LOCAL_DEV_TOKEN` or `GITHUB_TOKEN`.
2. Run `python tools/manage_ai_store.py --option review --write-ai --max-ai-files 5 --keep-scratch`.
3. Repeat without a token to verify the early-failure path.
4. Seed one invalid, stale, or orphan scratch record and rerun `validate` and
   `audit`.

Expected result:

- live generation stays bounded and scratch-only
- missing-token and bad-state failures are clear and local

## Track E: Promotion And Override Proof

1. Manually review the scratch diff.
2. Run `python tools/manage_ai_store.py --option promote`.
3. Create or edit one override and rerun the local review/apply flow.

Expected result:

- base receives only reviewed records
- override precedence remains intact

## Track F: Remote Workflow Proof

1. Trigger a remote run with `skip_ai=true` for non-AI publication proof.
2. Trigger a remote run with `skip_ai=false` and a small `max_ai_files` value
   for bounded AI verification.
3. Pin run inspection to the pushed commit SHA and inspect the workflow summary
   artifacts.

Expected result:

- the run completes green
- published outputs reflect committed authority

## Recommended Execution Order

1. Track A
2. Track B
3. Track C
4. Track D
5. Track E
6. Track F

## Current Gaps

- The focused pytest lane needs direct coverage for the `manage_ai_store` CLI
  surface.
- The local regression runners prove cache-backed AI placement, but not by
  themselves the full scratch-first promotion workflow.
- Promotion is copy-then-check rather than transactional, so manual review and
  rollback discipline remain part of the acceptance bar.

## Primary References

- [ai-summary-operations-runbook.md](./ai-summary-operations-runbook.md)
- [ai-summary-feature-spec.md](./ai-summary-feature-spec.md)
- [data/base/README.md](../../../data/base/README.md)
- [data/override/README.md](../../../data/override/README.md)
- [manage_ai_store.py](../../../tools/manage_ai_store.py)
- [tests/README.md](../../../tests/README.md)