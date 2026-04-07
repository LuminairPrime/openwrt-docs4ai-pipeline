# Folder Reorganization Plan v0

**Status:** Proposed  
**Date:** 2026-04-07  
**Scope:** `docs/plans/v14/openwrt-cookbook/` and all subdirectories  

---

## 1. Current State Analysis

### 1.1 Root-Level Files

The cookbook center root contains 11 numbered contract files (`00` through `10`) plus `README.md`:

| File | Purpose |
| --- | --- |
| `README.md` | Operator-facing quick-start: batch structure, scoring flow, sandboxed execution rules |
| `00-openwrt-cookbook-project-center-operating-plan.md` | Master operating plan: three-loop model, decision rules, queue lifecycle, source-of-truth precedence |
| `01-current-cookbook-state-and-gap-map.md` | Factual inventory of live cookbook corpus and known gaps |
| `02-v13-lineage-and-migration-map.md` | Historical lineage from v13 mistake-discovery project |
| `03-test-generation-contract.md` | Scenario admission rules, prompt-writing rules, grouped delivery rules, discovery administration |
| `04-failure-family-framework.md` | Four-level family hierarchy for deduplicating blind failures |
| `05-promotion-and-review-contract.md` | How scored failures become cookbook work; promotion outcomes and gates |
| `06-test-bank-and-grouped-delivery.md` | Full 27-scenario pack inventory, 9 grouped batch files, result layout per agent, manual execution workflow |
| `07-test-expansion-and-key-sourcing-plan.md` | Systematic test creation from authoritative OpenWrt sources |
| `08-cookbook-authoring-execution-contract.md` | How a trusted agent turns an admitted scenario into a staged draft, creation log, and promoted page |
| `09-staged-authoring-lifecycle.md` | Staging-folder model: draft, creation log, review record, promotion target |
| `10-human-review-procedure.md` | Human review checklist and promotion decision recording |

### 1.2 Root-Level Directories

| Directory | Purpose |
| --- | --- |
| `artifacts/` | Working artifacts: test batches, answer keys, scenario packets, results, authoring staging, scoring prompts, templates, registries |
| `docs/` | Contains `development prompts/` (one prompt file) and `plans/` (one scoring pipeline plan) |
| `tmp/` | Scratch area with one gap analysis file |
| `.specstory/` | IDE/story tracking (out of scope for reorganization) |

### 1.3 `artifacts/` Subdirectories

| Directory | Contents |
| --- | --- |
| `authoring/` | Cookbook staging: `drafts/`, `logs/`, `reviews/`, `examples/`, and `00-open-authoring-briefs.md` |
| `authoring/drafts/` | Staged cookbook drafts plus `00-draft-template.md` |
| `authoring/examples/` | Complete worked example: draft, creation log, review record |
| `authoring/logs/` | Creation logs plus `00-creation-log-template.md` |
| `authoring/reviews/` | Review records plus `00-human-review-record-template.md` |
| `promotion/` | `00-release-candidate-checklist.md` |
| `registry/` | `00-failure-family-registry.seed.yaml` (frozen ontology), `01-failure-family-registry.live.yaml` (mutable state) |
| `results/` | Manual run outputs organized as `<agent>/<run>/<batch>/`; includes `_template/` with canonical artifact templates |
| `runs/` | Legacy raw agent run folders from prior blind testing sessions |
| `scenario-packets/` | 14 admitted machine-readable scenario YAML packets (numbered 01 through 14) |
| `scoring/` | Scoring prompt templates, assessment results for multiple models, `haiku/` subfolder |
| `templates/` | `00-scenario-admission-template.yaml`, `00-batch-prompt-header-template.md` |
| `tests-batches/` | 9 grouped batch prompt files (`01a.md` through `01i.md`) plus `README.md` |
| `tests-keys/` | 9 mirrored answer key files (`01a-key.md` through `01i-key.md`) |
| `tests-full/` | Frozen rerun packet: `full-prompts.md`, `golden-answers-key.md`, `metadata-catalog.json` |

### 1.4 Standalone Files in `artifacts/`

| File | Purpose |
| --- | --- |
| `tests-batches-manifest.yaml` | Machine-readable batch inventory: batch IDs, file pairings, scenario membership |

### 1.5 `docs/` Subdirectories

| Directory | Contents |
| --- | --- |
| `development prompts/` | `prompt for qwen36 to develop the cookbook pipeline beyond prototype stage.txt` |
| `plans/` | `scoring-pipeline-implementation-v0.md`, `folder-reorganization-v0.md` (this document) |

### 1.6 `tmp/`

| File | Purpose |
| --- | --- |
| `cookbook-test-coverage-gap-analysis.md` | Scratch gap analysis |

---

## 2. What Should Stay

The following files are well-structured, essential, and should remain with minimal or no changes:

### 2.1 Numbered Contract Files

All 11 numbered files (`00` through `10`) contain durable operational contracts. Their content is sound. Their placement at the root is the primary issue (see Section 4).

### 2.2 Core Artifacts

| Path | Reason |
| --- | --- |
| `artifacts/tests-batches/01a.md` through `01i.md` | Active operator-facing batch prompts; stable, numbered, well-structured |
| `artifacts/tests-keys/01a-key.md` through `01i-key.md` | Mirrored answer keys; correct naming convention |
| `artifacts/tests-batches-manifest.yaml` | Machine-readable batch contract; single source of truth |
| `artifacts/tests-full/` | Frozen rerun packet; must stay discoverable and stable |
| `artifacts/scenario-packets/` | 14 admitted packets; correct naming convention |
| `artifacts/registry/` | Seed and live failure-family registries; correct separation of frozen vs mutable |
| `artifacts/templates/` | Reusable templates; correct placement |
| `artifacts/results/_template/` | Canonical artifact templates for new runs |
| `artifacts/results/` | Active run results tree; correct `<agent>/<run>/<batch>/` layout |
| `artifacts/authoring/drafts/`, `logs/`, `reviews/`, `examples/` | Staged authoring lifecycle; correct separation of concerns |
| `artifacts/promotion/00-release-candidate-checklist.md` | Promotion gate checklist |

### 2.3 README.md

The root `README.md` serves as the operator-facing quick-start. Its content is concise and actionable.

---

## 3. What Should Be Renamed

| Current Name | Proposed Name | Rationale |
| --- | --- | --- |
| `00-openwrt-cookbook-project-center-operating-plan.md` | `00-operating-plan.md` | "Project center" is implicit in the folder; shorter name improves scanability |
| `01-current-cookbook-state-and-gap-map.md` | `01-cookbook-state-and-gap-map.md` | Remove redundant "current" |
| `08-cookbook-authoring-execution-contract.md` | `08-cookbook-authoring-contract.md` | "Execution" is redundant with "contract" |
| `artifacts/scoring/scoring-prompt-v2.md` | `prompts/01-scoring-prompt.md` | Relocate to prompts folder |
| `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` | `prompts/02-test-scoring-prompt.md` | Relocate to prompts folder |
| `artifacts/scoring/scoring-plan-draft-for-haiku.txt` | `artifacts/scoring/archived/scoring-plan-draft-haiku.md` | Historical draft; archive and convert to Markdown |
| `docs/development prompts/prompt for qwen36....txt` | `prompts/03-pipeline-development-prompt.md` | Convert to markdown, relocate to prompts folder |
| `docs/plans/scoring-pipeline-implementation-v0.md` | `plans/00-scoring-pipeline-implementation.md` | Renumber for sequential ordering within plans/ |

---

## 4. Proposed Reorganization

### 4.1 Design Principles

1. **A human reads the root and understands the mission in 60 seconds.** The root should contain the mission statement, the pipeline stage catalog, and a "how to run" guide.
2. **Numbered files stay sequential.** All operational contracts remain numbered `00-` through `10-` but move into a dedicated subfolder.
3. **Prompts are centralized.** All AI prompt templates (test generation, scoring, cookbook authoring, verification, test-taker commands) live in one `prompts/` folder.
4. **Artifacts are the working surface.** The `artifacts/` folder stays as the live execution surface for test batches, keys, packets, results, and authoring staging.
5. **A `staging/` folder is the cookbook output destination.** The user requirement specifies a staging folder for cookbook outputs. The current `artifacts/authoring/` structure becomes `staging/`.

### 4.2 Two Options for Contract File Placement

**Option A -- Flat (recommended for v14 prototype):** Keep all numbered contracts at the root. This preserves the current reading experience where a maintainer opens the folder and sees the full numbered sequence immediately. Add `11-pipeline-step-catalog.md` and `12-how-to-run.md` to extend the sequence.

**Option B -- Nested under `contracts/`:** Move all numbered contracts into a `contracts/` subfolder. This keeps the root cleaner and creates a clear boundary between contracts, plans, prompts, and artifacts. Requires updating all cross-references in the contract files.

Option A is recommended for now because:
- The current flat structure works well for the 11-file sequence
- Cross-references use relative paths that would all need updating
- The operating plan (00) is the intended first-read entry point and benefits from root visibility

Option B becomes the right choice when the contract count exceeds 15 files or when additional top-level documents (plans, prompts, guides) accumulate enough to clutter the root.

### 4.3 Before and After Directory Trees

#### Before

```
openwrt-cookbook/
  README.md
  00-openwrt-cookbook-project-center-operating-plan.md
  01-current-cookbook-state-and-gap-map.md
  02-v13-lineage-and-migration-map.md
  03-test-generation-contract.md
  04-failure-family-framework.md
  05-promotion-and-review-contract.md
  06-test-bank-and-grouped-delivery.md
  07-test-expansion-and-key-sourcing-plan.md
  08-cookbook-authoring-execution-contract.md
  09-staged-authoring-lifecycle.md
  10-human-review-procedure.md
  artifacts/
    authoring/
      drafts/
      examples/
      logs/
      reviews/
      00-open-authoring-briefs.md
    promotion/
      00-release-candidate-checklist.md
    registry/
      00-failure-family-registry.seed.yaml
      01-failure-family-registry.live.yaml
    results/
      _template/
      README.md
      significantotter/
    runs/
      (legacy agent run folders)
    scenario-packets/
      (14 YAML packets)
    scoring/
      haiku/
      openwrt-scoring-assessment-*.md (4 files)
      openwrt-test-scoring-prompt-v2.md
      scoring-plan-draft-for-haiku.txt
      scoring-prompt-v2.md
    templates/
      00-batch-prompt-header-template.md
      00-scenario-admission-template.yaml
    tests-batches/
      01a.md through 01i.md
      README.md
    tests-full/
      full-prompts.md
      golden-answers-key.md
      metadata-catalog.json
    tests-keys/
      01a-key.md through 01i-key.md
    tests-batches-manifest.yaml
  docs/
    development prompts/
      prompt for qwen36....txt
    plans/
      scoring-pipeline-implementation-v0.md
  tmp/
    cookbook-test-coverage-gap-analysis.md
```

#### After (Option A -- Flat, Recommended)

```
openwrt-cookbook/
  README.md                          # New: mission statement + quick-start + how to run
  00-operating-plan.md               # Renamed from 00-openwrt-cookbook-project-center-operating-plan.md
  01-cookbook-state-and-gap-map.md   # Renamed from 01-current-cookbook-state-and-gap-map.md
  02-v13-lineage-and-migration-map.md
  03-test-generation-contract.md
  04-failure-family-framework.md
  05-promotion-and-review-contract.md
  06-test-bank-and-grouped-delivery.md
  07-test-expansion-and-key-sourcing-plan.md
  08-cookbook-authoring-contract.md  # Renamed from 08-cookbook-authoring-execution-contract.md
  09-staged-authoring-lifecycle.md
  10-human-review-procedure.md
  11-pipeline-step-catalog.md        # New: numbered pipeline stage catalog
  12-how-to-run.md                   # New: human operator guide
  prompts/                           # New: AI prompt templates
    00-batch-prompt-header-template.md    # from artifacts/templates/
    01-scoring-prompt.md                  # from artifacts/scoring/scoring-prompt-v2.md
    02-test-scoring-prompt.md             # from artifacts/scoring/openwrt-test-scoring-prompt-v2.md
    03-pipeline-development-prompt.md     # from docs/development prompts/
    04-test-taker-instructions.md         # New: consolidated README.md rules
    05-cookbook-generation-prompt.md      # New: prompt for authoring cookbooks from data store
    06-veracity-check-prompt.md           # New: prompt for checking against OpenWrt codebase
    07-upgrade-dos-donts-prompt.md        # New: prompt for upgrade do's/don'ts
  plans/                             # Implementation plans (existing, expanded)
    00-scoring-pipeline-implementation.md
    folder-reorganization-v0.md      # This document
  staging/                           # New: cookbook output staging surface
    drafts/
      00-draft-template.md
      (staged cookbook drafts)
    logs/
      00-creation-log-template.md
      (creation logs)
    reviews/
      00-human-review-record-template.md
      (review records)
    examples/
      (worked example: draft, log, review)
    00-authoring-briefs.md
    README.md
  artifacts/                         # Restructured (see 4.4)
    tests-batches/
      01a.md through 01i.md
      README.md
    tests-keys/
      01a-key.md through 01i-key.md
    tests-batches-manifest.yaml
    tests-full/
      full-prompts.md
      golden-answers-key.md
      metadata-catalog.json
    scenario-packets/
      (14 YAML packets)
    registry/
      00-failure-family-registry.seed.yaml
      01-failure-family-registry.live.yaml
    results/
      _template/
      README.md
      significantotter/
      (legacy scoring assessment files moved here)
    runs/
      (legacy agent run folders)
    promotion/
      00-release-candidate-checklist.md
    scoring/
      archived/
        scoring-plan-draft-haiku.md
    templates/
      00-scenario-admission-template.yaml   # kept: machine-readable, not a prompt
```

### 4.4 Artifacts Restructuring Rationale

| Change | Rationale |
| --- | --- |
| Move `artifacts/templates/00-batch-prompt-header-template.md` to `prompts/` | It is a prompt template, not a data template |
| Keep `artifacts/templates/00-scenario-admission-template.yaml` | Machine-readable data template, not a prompt |
| Move scoring assessment files to `artifacts/results/` | They are completed run evidence, not reusable prompts |
| Add `artifacts/scoring/archived/` | Separate historical drafts from active scoring work |
| Move `artifacts/authoring/` to `staging/` | User requirement: staging folder for cookbook outputs; "staging" is clearer than "authoring" |
| Keep `artifacts/runs/` as-is | The agent-labeled execution surface is already well-structured |
| Keep `artifacts/results/` as-is | The result layout per agent is already well-documented in `06-test-bank-and-grouped-delivery.md` |

---

## 5. New Files To Create

### 5.1 Prompt Templates

| File | Purpose | Input | Output | Source |
| --- | --- | --- | --- | --- |
| `prompts/00-batch-prompt-header-template.md` | Shared execution contract for grouped batch files | None | Header text for batch files | Existing: `artifacts/templates/` |
| `prompts/01-scoring-prompt.md` | Score agent responses against answer keys | Raw response, answer key, scenario packet | Score record with pass/fail per scenario | Existing: `artifacts/scoring/scoring-prompt-v2.md` |
| `prompts/02-test-scoring-prompt.md` | Alternative scoring prompt variant | Raw response, answer key | Score record | Existing: `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` |
| `prompts/03-pipeline-development-prompt.md` | Command AI to develop the pipeline further | Current state, gap analysis | Development plan | Existing: `docs/development prompts/` |
| `prompts/04-test-taker-instructions.md` | Instructions for AI agents taking the test (the "five hard rules") | Batch prompt file | Raw responses routed to `artifacts/results/` | Extract from current `README.md` |
| `prompts/05-cookbook-generation-prompt.md` | Generate cookbook pages from the data store | Scenario packet, raw failure responses, authority sources, existing cookbook pages | Staged draft + creation log | New: derived from `08-cookbook-authoring-contract.md` |
| `prompts/06-veracity-check-prompt.md` | Verify cookbook claims against the OpenWrt codebase | Draft cookbook page, authority source paths | Veracity report with confirmed/flagged claims | New |
| `prompts/07-upgrade-dos-donts-prompt.md` | Guide upgrade decisions when OpenWrt patterns change | Failure family record, current cookbook page | Do/don't list with source citations | New |

### 5.2 `11-pipeline-step-catalog.md`

Modeled after the main pipeline's `docs/specs/pipeline-stage-catalog.md`. Each step documents step number, name, input artifacts, output artifacts, human vs. AI responsibility, failure mode, and retry guidance.

Proposed step ordering:

| Step | Name | Responsibility | Input | Output |
| --- | --- | --- | --- | --- |
| 01 | Scenario Admission | Human + AI | Inspiration source, authority source | Admitted scenario packet |
| 02 | Batch Assembly | Human | Admitted scenarios, grouping rules | Grouped batch files + manifest |
| 03 | Blind Execution | AI (test-taker) | Batch prompt, clean-room rules | Raw responses in `artifacts/results/` |
| 04 | Scoring | Human + AI | Raw responses, answer keys, scenario packets | Score records |
| 05 | Failure Classification | Human + AI | Scored failures, family registry | Family assignments |
| 06 | Promotion Decision | Human | Failure families, cookbook gap map | Outcome decision (reject/extend/new/umbrella) |
| 07 | Cookbook Drafting | AI | Scenario packet, raw failures, authority sources | Staged draft + creation log |
| 08 | Human Review | Human | Staged draft, creation log, source packet | Review record with decision |
| 09 | Promotion | Human | Accepted review, promotion checklist | Promoted page in `static/cookbook-source/` |
| 10 | Verification | AI + Human | Promoted page, associated scenarios | Verification outcome |

### 5.3 `12-how-to-run.md`

A single-page guide that answers:
- What this folder does (mission statement)
- How to run a full discovery cycle end-to-end
- Which files to read first
- Which steps require human interaction vs. AI prompt execution
- Where outputs land at each step
- How to add a new scenario
- How to add a new cookbook page

### 5.4 New `README.md`

The current `README.md` is an operator quick-start for running batches. A new root `README.md` should serve as the mission statement and entry point:
- One-paragraph mission statement
- Link to `00-operating-plan.md` for the full operating contract
- Link to `12-how-to-run.md` for the operator guide
- Link to `11-pipeline-step-catalog.md` for the step-by-step pipeline
- High-level directory map
- Quick reference: which folder holds what

### 5.5 `staging/README.md`

Explain the staging model, artifact types (draft, creation log, review record), and the promotion pathway to `static/cookbook-source/`.

---

## 6. Documentation Health

### 6.1 Files That Need Updates

| File | Required Update |
| --- | --- |
| All 11 numbered contracts | Update internal cross-references to reflect any renamed or moved files |
| `06-test-bank-and-grouped-delivery.md` | Update file location tables to reflect `prompts/` folder and `staging/` folder |
| `08-cookbook-authoring-contract.md` | Update filesystem contract section to reference new `staging/` path |
| `09-staged-authoring-lifecycle.md` | Reference new `staging/` layout; update anti-patterns section |
| `artifacts/tests-batches/README.md` | Update references to prompt header template location |
| `artifacts/results/README.md` | Confirm result layout documentation still matches `_template/` |

### 6.2 Files That Need Creation

| File | Purpose | Priority |
| --- | --- | --- |
| `README.md` (rewritten) | Mission statement + quick-start + how to run | High |
| `11-pipeline-step-catalog.md` | Numbered pipeline stage catalog | High |
| `12-how-to-run.md` | Human operator end-to-end guide | High |
| `prompts/04-test-taker-instructions.md` | Consolidate "five hard rules" from current README.md | Medium |
| `prompts/05-cookbook-generation-prompt.md` | Prompt template for generating cookbook pages | Medium |
| `prompts/06-veracity-check-prompt.md` | Prompt template for verifying against OpenWrt source | Medium |
| `prompts/07-upgrade-dos-donts-prompt.md` | Prompt template for upgrade decisions | Medium |
| `staging/README.md` | Staging folder usage guide | Medium |

### 6.3 Files That Can Be Archived or Removed

| File | Recommendation |
| --- | --- |
| `tmp/cookbook-test-coverage-gap-analysis.md` | Archive or integrate into `01-cookbook-state-and-gap-map.md` |
| `artifacts/scoring/scoring-plan-draft-for-haiku.txt` | Archive as scratch or delete if superseded by `scoring-prompt-v2.md` |
| `docs/development prompts/` | Remove directory after moving its content to `prompts/` |

---

## 7. Migration Steps

1. Create `prompts/`, `staging/`, and `plans/` directories
2. Move prompt templates from `artifacts/scoring/` and `artifacts/templates/` to `prompts/`
3. Move `docs/development prompts/` content to `prompts/`
4. Move `artifacts/authoring/` contents to `staging/`
5. Create new prompt templates (`04` through `07`)
6. Create `11-pipeline-step-catalog.md`
7. Create `12-how-to-run.md`
8. Rewrite root `README.md` as mission statement
9. Create `staging/README.md`
10. Move scoring assessment files to `artifacts/results/`
11. Create `artifacts/scoring/archived/` and move historical drafts
12. Rename `00-openwrt-cookbook-project-center-operating-plan.md` to `00-operating-plan.md`
13. Rename `01-current-cookbook-state-and-gap-map.md` to `01-cookbook-state-and-gap-map.md`
14. Rename `08-cookbook-authoring-execution-contract.md` to `08-cookbook-authoring-contract.md`
15. Update all internal cross-references in moved and renamed files
16. Remove empty `docs/development prompts/` directory
17. Move `docs/plans/scoring-pipeline-implementation-v0.md` to `plans/00-scoring-pipeline-implementation.md`
18. Verify all relative links resolve correctly

---

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Broken cross-references after rename/move | Medium | Update all references in the same commit; run a link check |
| Operator confusion during transition | Low | Keep Option A (flat) for v14; no structural disruption to contract file locations |
| Lost historical evidence in scoring/ | Low | Archive, do not delete; maintain `artifacts/scoring/archived/` |
| Prompt template duplication | Low | New `prompts/` files are canonical; old versions move to `scoring/archived/` |
| Disruption to active runs | Low | Do not move `artifacts/results/` or `artifacts/runs/` contents; only reorganize structure files |

---

## 9. Decision Log

| Decision | Rationale |
| --- | --- |
| Keep contracts flat at root (Option A) | Preserves current reading experience; avoids mass cross-reference updates; root visibility for operating plan is intentional |
| Create `prompts/` at root | Prompt templates are first-class pipeline inputs; separating them from scoring results clarifies the distinction between reusable prompts and one-off assessments |
| Create `staging/` at root | The staged authoring lifecycle (`09-staged-authoring-lifecycle.md`) references a staging model but has no dedicated directory; renaming from `authoring/` to `staging/` matches the user requirement |
| Add `11-pipeline-step-catalog.md` and `12-how-to-run.md` | The user requirements explicitly call for numbered pipeline steps, input/output documentation, and a human-readable run guide; these are currently scattered across multiple files |
| Archive rather than delete historical scoring drafts | Preserves evidence chain for auditability; keeps active scoring directory focused on current assessments |
