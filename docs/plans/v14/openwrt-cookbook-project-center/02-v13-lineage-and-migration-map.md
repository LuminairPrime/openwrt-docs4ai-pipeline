# V13 Lineage And Migration Map

**Purpose:** Record what the v14 project center copied, summarized, referenced, or intentionally left behind from the v13 cookbook and defect-discovery work.

---

## 1. Copied Into V14 As Frozen Reproducibility Artifacts

| V13 source | V14 destination | Why copied |
| --- | --- | --- |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/00-batch-prompts.md` | `artifacts/test-pack/00-batch-prompts.md` | Canonical blind prompt packet |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/02-metadata-catalog.json` | `artifacts/test-pack/02-metadata-catalog.json` | Canonical expected-paradigm catalog |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/03-golden-answers-key.md` | `artifacts/test-pack/03-golden-answers-key.md` | Canonical truth and falseness schema |

These three files are the frozen rerun packet for this prototype center.

---

## 2. Summarized Into V14 Coordination Docs

| V13 source | V14 target | Treatment |
| --- | --- | --- |
| `mistake-discovery-plan-3-opus.md` | `00-openwrt-cookbook-project-center-operating-plan.md` | Summarized for durable decisions only |
| `cookbook-target-shortlist-2026-03-28.md` | `01-current-cookbook-state-and-gap-map.md` | Summarized as living gap logic rather than frozen shortlist |
| `03-v13-cookbook-content-spec-2026-03-22.md` | `00-openwrt-cookbook-project-center-operating-plan.md` and `02-v13-lineage-and-migration-map.md` | Historical sequencing logic only; not copied as active contract |
| `ai-defect-discovery-pipeline/04-pipeline-implementation-guide.md` | `03-test-generation-contract.md` | Summarized into current test-generation rules |
| `ai-defect-discovery-pipeline/05-evaluation-and-scoring-plan.md` | `03-test-generation-contract.md` | Summarized for binary grading and scoring logic |
| `ai-defect-discovery-pipeline/06-cross-batch-synthesis-and-golden-key-proposals.md` | `01-current-cookbook-state-and-gap-map.md` and `04-failure-family-framework.md` | Summarized for durable blind-spot findings |

---

## 3. Referenced But Not Duplicated

| Live reference | Reason |
| --- | --- |
| `docs/specs/cookbook-authoring-spec.md` | Active authoring contract |
| `docs/specs/schema-definitions.md` | Active filesystem and metadata contract |
| `static/cookbook-source/*.md` | Live authored cookbook corpus |
| `docs/guides/runbook-ai-summary-operations.md` | Example of disciplined review/promotion workflow |
| `docs/plans/v13/pipeline-folder-refactor-04.md` | Historical reference for the authored-source move |

These remain live references to avoid forking the repo's actual active contracts.

---

## 4. Intentionally Not Carried Forward

| Material left in place | Why |
| --- | --- |
| Raw results trees and per-model score sheets | Too bulky and partly derived; useful as history, not as copied coordination inputs |
| Batch-slice answer-key variants | Historical analysis value only |
| Empty or low-signal v13 stubs | They do not improve reproducibility |

---

## 5. Migration Decision Summary

The v14 center is intentionally small.

- copy only the minimal rerun packet
- centralize rationale in one operating plan
- keep supporting docs operational and factual
- rely on live contracts instead of cloning the whole spec surface again
