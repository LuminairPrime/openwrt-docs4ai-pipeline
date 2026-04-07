# Folder Organization Plan — opus46-v0

**Status:** Proposed
**Date:** 2026-04-07
**Scope:** `docs/plans/v14/openwrt-cookbook/` and all subdirectories

---

## 1. Purpose

Reorganize the openwrt-cookbook folder so that:
- A human reads the root and understands the mission in 60 seconds
- AI prompt templates are centralized rather than scattered across 3 directories
- The staging/authoring surface has a name that matches the pipeline's language
- Legacy scoring prompts are archived, not deleted
- The parent docs4ai pipeline can find the latest cookbook outputs via a JSON marker
- The `runs/` vs `results/` split is acknowledged and documented

Out of scope: `.specstory/` (IDE tracking), `.gitkeep` files, anything outside `docs/plans/v14/openwrt-cookbook/`.

---

## 2. Current State Inventory

### Root (15 files)

| File | Purpose | Verdict |
|---|---|---|
| `README.md` | Operator quick-start | **Keep**, update references |
| `mission-statement-gemini31pro-v0.md` | Gemini's mission draft | **Archive** to `docs/plans/` |
| `mission-statement-qwen36plus-v0.md` | Qwen's mission draft | **Archive** to `docs/plans/` |
| `mission-statement-opus46-v0.md` | Opus's mission draft | **Archive** to `docs/plans/` |
| `00-openwrt-cookbook-project-center-operating-plan.md` | Master operating plan | **Rename** |
| `01-current-cookbook-state-and-gap-map.md` | Corpus inventory and gaps | **Rename** |
| `02` through `07` | Contracts | **Keep as-is** |
| `08-cookbook-authoring-execution-contract.md` | Staged draft authoring | **Rename** |
| `09-staged-authoring-lifecycle.md` | Draft → promotion lifecycle | **Keep as-is** |
| `10-human-review-procedure.md` | Review checklist | **Keep as-is** |

### `artifacts/` (11 subdirectories + 1 standalone)

| Path | Contents | Verdict |
|---|---|---|
| `authoring/` | `drafts/`, `logs/`, `reviews/`, `examples/`, `00-open-authoring-briefs.md` | **Rename** to `staging/` |
| `promotion/` | `00-release-candidate-checklist.md` | **Keep as-is** |
| `registry/` | Seed YAML (frozen) + live YAML (mutable) | **Keep as-is** |
| `results/` | `_template/`, `significantotter/`, `README.md` | **Keep as-is** — canonical new format |
| `runs/` | `big-pickle/`, `dola-seed-20-pro/`, `gemini-3-flash/`, etc. | **Keep as-is** — legacy evidence, read-only |
| `scenario-packets/` | 14 YAML packets (01–14) | **Keep as-is** |
| `scoring/` | v2 prompts, 4 assessments, `haiku/`, scratch plan | **Restructure**: archive v2, add v4 artifacts |
| `templates/` | `00-batch-prompt-header-template.md`, `00-scenario-admission-template.yaml` | **Split**: prompt → `prompts/`, YAML stays |
| `tests-batches/` | `01a.md`–`01i.md`, `README.md` | **Keep as-is** |
| `tests-full/` | `full-prompts.md`, `golden-answers-key.md`, `metadata-catalog.json` | **Keep as-is** — frozen rerun baseline |
| `tests-keys/` | `01a-key.md`–`01i-key.md` | **Rewrite** format (scoring plan), same location |
| `tests-batches-manifest.yaml` | Machine-readable batch inventory | **Keep as-is** |

### `docs/`

| Path | Contents | Verdict |
|---|---|---|
| `development prompts/` | 3 `.txt` development prompts | **Move** to `prompts/`, convert to `.md` |
| `plans/` | Plan files from various agents | **Keep as-is** |

### `tmp/`

| File | Verdict |
|---|---|
| `cookbook-test-coverage-gap-analysis.md` | **Integrate** into `01-cookbook-state-and-gap-map.md`, then delete |

### Out of scope

`.specstory/`, `.gitkeep` files — do not touch.

---

## 3. Files That Are Fine As-Is

Explicitly listing what needs NO changes to reduce scope anxiety:

- Numbered contracts `02` through `07`, `09`, `10` — content and location correct
- `artifacts/results/` — new template-based format is well-structured
- `artifacts/runs/` — legacy evidence in older format; do NOT migrate or restructure mid-flight
- `artifacts/scenario-packets/` — 14 packets with correct numbering
- `artifacts/registry/` — frozen/mutable separation is correct
- `artifacts/promotion/` — single checklist, right place
- `artifacts/tests-batches/` + `tests-keys/` — paired batch/key structure works (key FORMAT changes are in the scoring plan, not here)
- `artifacts/tests-full/` — frozen rerun baseline; relationship to `tests-batches/` is "full = all batches concatenated + golden key" per `06-test-bank-and-grouped-delivery.md`
- `artifacts/tests-batches-manifest.yaml` — single source of truth
- `docs/plans/` — plans accumulate here naturally

---

## 4. What Gets Renamed

| Current Name | New Name | Rationale |
|---|---|---|
| `00-openwrt-cookbook-project-center-operating-plan.md` | `00-operating-plan.md` | "Project center" is implicit; shorter improves scanability |
| `01-current-cookbook-state-and-gap-map.md` | `01-cookbook-state-and-gap-map.md` | "Current" is redundant |
| `08-cookbook-authoring-execution-contract.md` | `08-cookbook-authoring-contract.md` | "Execution" is redundant with "contract" |
| `artifacts/authoring/` | `artifacts/staging/` | Matches user language; aligns with `09-staged-authoring-lifecycle.md` terminology |

---

## 5. What Gets Moved or Archived

### 5a. Mission Statements — Consolidate

Three agent-versioned mission statements at root creates clutter and ambiguity about which is authoritative.

**Action:**
1. Human picks the best draft (or synthesizes from all three) → saves as `mission-statement.md` at root (no agent suffix)
2. Move all three versioned files to `docs/plans/` as historical plan artifacts
3. The single `mission-statement.md` becomes the authoritative entry point

### 5b. Scoring Prompts — Archive Superseded

**Action:** Per the scoring pipeline plan (Phases 1 and 5):
1. Create `artifacts/scoring/archive/`
2. Move `scoring-prompt-v2.md` → `artifacts/scoring/archive/` with supersession note
3. Move `openwrt-test-scoring-prompt-v2.md` → `artifacts/scoring/archive/`
4. Move `scoring-plan-draft-for-haiku.txt` → `artifacts/scoring/archive/` as `.md`
5. Keep scoring assessments (`openwrt-scoring-assessment-*.md`) at top level — they are completed evidence, not superseded prompts

### 5c. Prompt Consolidation

Prompt templates are scattered across `artifacts/templates/`, `artifacts/scoring/`, and `docs/development prompts/`.

**Action:** Create `prompts/` at cookbook root. Organize by descriptive name, NOT by number:

| From | To |
|---|---|
| `artifacts/templates/00-batch-prompt-header-template.md` | `prompts/batch-prompt-header-template.md` |
| `docs/development prompts/prompt for gemini...txt` | `prompts/pipeline-development-prompt-gemini.md` |
| `docs/development prompts/prompt for qwen36...txt` | `prompts/pipeline-development-prompt-qwen.md` |
| `docs/development prompts/prompt for opus...txt` | `prompts/pipeline-development-prompt-opus.md` |

Keep `artifacts/templates/00-scenario-admission-template.yaml` in place — it's a machine-readable data template, not a prompt.

**Important:** Scoring prompts (`openwrt-test-scoring-prompt-v4.md`, `openwrt-failure-synthesis-prompt.md`) stay in `artifacts/scoring/` because they are tightly coupled to calibration fixtures and scorecard schema. Cross-link from `prompts/README.md`.

After moves: delete empty `docs/development prompts/` directory. If `artifacts/templates/` only has the YAML file left, keep it.

### 5d. tmp/ Cleanup

Integrate useful content from `tmp/cookbook-test-coverage-gap-analysis.md` into `01-cookbook-state-and-gap-map.md`, then delete the file and `tmp/` directory.

---

## 6. What Gets Created

### New directories

| Directory | Purpose |
|---|---|
| `prompts/` | Centralized AI prompt templates |
| `artifacts/scoring/archive/` | Superseded scoring prompts |

### New files

| File | Purpose | Priority | Effort |
|---|---|---|---|
| `mission-statement.md` | Canonical mission (human picks/synthesizes) | High | Small |
| `prompts/README.md` | Index of all prompts with pipeline stage mapping, including cross-links to scoring prompts in `artifacts/scoring/` | High | Small |
| `prompts/batch-prompt-header-template.md` | Moved from `artifacts/templates/` | High | Small (move) |
| `prompts/test-taker-instructions.md` | Consolidate "five hard rules" from `README.md` | Medium | Small |
| `prompts/cookbook-authoring-prompt.md` | Generate cookbook pages from scored failures | Medium | Medium |
| `prompts/veracity-check-prompt.md` | Verify cookbook claims against OpenWrt source | Medium | Medium |
| `prompts/dos-donts-upgrade-prompt.md` | Upgrade pipeline do's/don'ts each iteration | Medium | Medium |
| `prompts/pipeline-development-prompt-*.md` (3) | Moved + converted from `docs/development prompts/` | Low | Small |
| `11-pipeline-step-catalog.md` | Numbered step reference: inputs, outputs, responsibility per stage | High | Large |
| `12-how-to-run.md` | End-to-end operator guide | High | Large |
| `artifacts/staging/README.md` | Staging model usage and promotion pathway | Medium | Small |
| `latest_cookbook_staging.json` | JSON marker for parent pipeline integration | Medium | Small |

The scoring pipeline plan creates 5 additional files in `artifacts/scoring/`. Those are not duplicated here.

### Prompt naming convention

Prompts are named by pipeline stage/purpose, not numbered:

```
prompts/
  README.md                              # index with cross-links
  batch-prompt-header-template.md        # from artifacts/templates/
  test-taker-instructions.md             # new: from README.md rules
  cookbook-authoring-prompt.md            # new
  veracity-check-prompt.md              # new
  dos-donts-upgrade-prompt.md           # new
  pipeline-development-prompt-gemini.md  # moved from docs/development prompts/
  pipeline-development-prompt-qwen.md    # moved
  pipeline-development-prompt-opus.md    # moved
```

### `latest_cookbook_staging.json`

```json
{
  "status": "empty",
  "latest_run": null,
  "path": null,
  "note": "Updated by human operator after accepting a cookbook staging run"
}
```

---

## 7. Before/After Directory Tree

### Before

```
openwrt-cookbook/
  README.md
  mission-statement-gemini31pro-v0.md
  mission-statement-qwen36plus-v0.md
  mission-statement-opus46-v0.md
  00-openwrt-cookbook-project-center-operating-plan.md
  01-current-cookbook-state-and-gap-map.md
  02 through 07 (unchanged)
  08-cookbook-authoring-execution-contract.md
  09, 10 (unchanged)
  artifacts/
    authoring/ (drafts/, logs/, reviews/, examples/)
    promotion/
    registry/
    results/ (_template/, significantotter/)
    runs/ (big-pickle/, dola-seed-20-pro/, gemini-3-flash/, ...)
    scenario-packets/ (14 YAMLs)
    scoring/ (v2 prompts, assessments, haiku/)
    templates/ (prompt header + YAML admission)
    tests-batches/ (01a–01i)
    tests-full/ (frozen rerun packet)
    tests-keys/ (01a-key–01i-key)
    tests-batches-manifest.yaml
  docs/
    development prompts/ (3 .txt files)
    plans/ (agent plan files)
  tmp/ (gap analysis)
```

### After

```
openwrt-cookbook/
  README.md                              # updated references
  mission-statement.md                   # canonical (human-selected)
  latest_cookbook_staging.json            # new: parent pipeline marker
  00-operating-plan.md                   # renamed
  01-cookbook-state-and-gap-map.md        # renamed
  02 through 07 (unchanged)
  08-cookbook-authoring-contract.md       # renamed
  09, 10 (unchanged)
  11-pipeline-step-catalog.md            # new
  12-how-to-run.md                       # new
  prompts/                               # new directory
    README.md
    batch-prompt-header-template.md
    test-taker-instructions.md
    cookbook-authoring-prompt.md
    veracity-check-prompt.md
    dos-donts-upgrade-prompt.md
    pipeline-development-prompt-gemini.md
    pipeline-development-prompt-qwen.md
    pipeline-development-prompt-opus.md
  artifacts/
    staging/                             # renamed from authoring/
      drafts/, logs/, reviews/, examples/
      00-open-authoring-briefs.md
      README.md                          # new
    promotion/
    registry/
    results/                             # unchanged
    runs/                                # unchanged (legacy, read-only)
    scenario-packets/
    scoring/
      archive/                           # new
        scoring-prompt-v2.md
        openwrt-test-scoring-prompt-v2.md
        scoring-plan-draft-haiku.md
      openwrt-scoring-assessment-*.md    # kept as evidence
      openwrt-calibration-fixtures.md    # new (scoring plan)
      openwrt-scorecard-schema.md        # new (scoring plan)
      openwrt-test-scoring-prompt-v4.md  # new (scoring plan)
      openwrt-failure-synthesis-prompt.md # new (scoring plan)
      openwrt-scorer-lessons-log.md      # new (scoring plan)
      haiku/                             # kept
    templates/
      00-scenario-admission-template.yaml # kept (YAML, not a prompt)
    tests-batches/
    tests-full/                          # kept as frozen rerun baseline
    tests-keys/                          # format rewrite (scoring plan)
    tests-batches-manifest.yaml
  docs/
    plans/                               # kept, plus archived missions
      mission-statement-gemini31pro-v0.md
      mission-statement-qwen36plus-v0.md
      mission-statement-opus46-v0.md
      (scoring and organization plans)
  (docs/development prompts/ — deleted after move)
  (tmp/ — deleted after integration)
```

---

## 8. Migration Steps

Grouped by risk. Complete each group before the next.

### Group A — Low Risk: Renames

| Step | Action | Effort |
|---|---|---|
| A1 | `git mv` `00-openwrt-cookbook-project-center-operating-plan.md` → `00-operating-plan.md` | Small |
| A2 | `git mv` `01-current-cookbook-state-and-gap-map.md` → `01-cookbook-state-and-gap-map.md` | Small |
| A3 | `git mv` `08-cookbook-authoring-execution-contract.md` → `08-cookbook-authoring-contract.md` | Small |
| A4 | `git mv` `artifacts/authoring` → `artifacts/staging` | Small |

### Group B — Low Risk: Directory creation

| Step | Action | Effort |
|---|---|---|
| B1 | Create `prompts/` | Small |
| B2 | Create `artifacts/scoring/archive/` | Small |

### Group C — Medium Risk: File moves

| Step | Action | Effort |
|---|---|---|
| C1 | Move `artifacts/templates/00-batch-prompt-header-template.md` → `prompts/batch-prompt-header-template.md` | Small |
| C2 | Move 3 mission statements from root → `docs/plans/` | Small |
| C3 | Move + convert `docs/development prompts/*.txt` → `prompts/*.md` | Small |
| C4 | Move v2 scoring prompts + haiku draft → `artifacts/scoring/archive/` (scoring plan Phase 1) | Small |
| C5 | Delete empty `docs/development prompts/` | Small |
| C6 | Keep `artifacts/templates/` if YAML remains; delete only if truly empty | Small |

### Group D — Medium Risk: New file creation

| Step | Action | Effort |
|---|---|---|
| D1 | Human selects/synthesizes → `mission-statement.md` at root | Small |
| D2 | Write `prompts/README.md` | Small |
| D3 | Write `prompts/test-taker-instructions.md` | Small |
| D4 | Write `prompts/cookbook-authoring-prompt.md` | Medium |
| D5 | Write `prompts/veracity-check-prompt.md` | Medium |
| D6 | Write `prompts/dos-donts-upgrade-prompt.md` | Medium |
| D7 | Write `artifacts/staging/README.md` | Small |
| D8 | Write `latest_cookbook_staging.json` | Small |
| D9 | Write `11-pipeline-step-catalog.md` | Large |
| D10 | Write `12-how-to-run.md` | Large |

### Group E — Higher Risk: Content integration + cross-reference fixes

| Step | Action | Effort |
|---|---|---|
| E1 | Integrate `tmp/cookbook-test-coverage-gap-analysis.md` into `01-cookbook-state-and-gap-map.md` | Medium |
| E2 | Delete `tmp/` | Small |
| E3 | Update `README.md` — new file names, `prompts/` folder, `authoring/` → `staging/` | Medium |
| E4 | Update `06-test-bank-and-grouped-delivery.md` location tables | Medium |
| E5 | Update `08-cookbook-authoring-contract.md` filesystem references → `artifacts/staging/` | Medium |
| E6 | Update `09-staged-authoring-lifecycle.md` → `artifacts/staging/` | Medium |
| E7 | Update `artifacts/tests-batches/README.md` prompt template location | Small |
| E8 | `grep -r` all `.md` and `.yaml` for old paths and fix stragglers | Medium |

---

## 9. Documentation Health

Files needing updates after reorganization:

| File | Required Update |
|---|---|
| `README.md` | Point to `mission-statement.md`, reference `prompts/`, update `authoring/` → `staging/` |
| `00-operating-plan.md` | Update any self-references to old filename |
| `06-test-bank-and-grouped-delivery.md` | Update file location tables for `prompts/` and `artifacts/staging/` |
| `08-cookbook-authoring-contract.md` | Filesystem contract section: `authoring/` → `staging/` |
| `09-staged-authoring-lifecycle.md` | All `authoring/` references → `staging/`; update anti-patterns section |
| `artifacts/tests-batches/README.md` | Update prompt header template location reference |
| `artifacts/results/README.md` | Confirm layout docs match `_template/`; document that `runs/` is legacy read-only |

---

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Broken cross-references after renames/moves | Medium | Group E fixes all references in same commit; `grep -r "old-name"` catches stragglers |
| Operator confusion during transition | Low | Contracts stay flat at root (no structural disruption); README update in E3 |
| Lost evidence from scoring archive | Low | Archive, never delete; `artifacts/scoring/archive/` preserves history |
| `runs/` vs `results/` divergence grows | Low | Accept the split: `runs/` is legacy read-only, `results/` is canonical for new runs. Document in `12-how-to-run.md` and `artifacts/results/README.md` |
| Prompt duplication after centralization | Low | `prompts/README.md` is the index; scoring prompts stay in `artifacts/scoring/` with cross-links |
| Active scoring runs disrupted by move | Medium | Complete scoring plan Phase 1 (archive) before this plan's Group C (moves) |

---

## 11. Decision Log

| Decision | Rationale |
|---|---|
| Keep numbered contracts flat at root | 11-file sequence is established; subfolder adds indirection without benefit at this scale. Revisit at 15+ files. |
| Create `prompts/` at root | Prompt templates are first-class pipeline inputs scattered across 3 locations; centralizing makes the operator's job clear. |
| Name prompts by stage, not by number | The prompt set is still growing; forced numbering (00–10) creates maintenance burden and makes additions awkward. Stage names are self-documenting. |
| Keep scoring prompts in `artifacts/scoring/` | They are tightly coupled to calibration fixtures and scorecard schema. Cross-link from `prompts/README.md`. |
| Rename `authoring/` → `staging/` | User's language says "staging"; `09-staged-authoring-lifecycle.md` already uses "staged draft" terminology. |
| Archive mission drafts to `docs/plans/` | Three agent-versioned drafts at root clutters the entry point. Promote one canonical `mission-statement.md`. |
| Keep `runs/` and `results/` separate | `runs/` is legacy with inconsistent format; `results/` uses the new template. Migrating runs mid-flight risks losing provenance. Document the split rather than force a merge. |
| Keep `tests-full/` as-is | Frozen rerun baseline used for regression. Its relationship to `tests-batches/` is documented in `06-test-bank-and-grouped-delivery.md`. Renaming adds no clarity. |
| `latest_cookbook_staging.json` at root | Simple pointer for parent pipeline integration. Human updates after accepting a staging run. |
