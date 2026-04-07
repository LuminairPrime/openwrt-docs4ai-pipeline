# Scoring Pipeline Implementation Plan — qwen36plus-v0

**Status:** Proposed
**Date:** 2026-04-07
**Source:** [openwrt-scoring-assessment-10-10.md](../../artifacts/scoring/openwrt-scoring-assessment-10-10.md)
**Scope:** Answer keys, calibration fixtures, scorecard schema, strict scoring prompt, failure-synthesis prompt, scorer-lessons-log, and the operational gates that bind them.

---

## 1. Purpose

The 10/10 scoring assessment identified three systemic failure modes in LLM-based scoring:

1. **Lenience/Drift** — accepting functionally similar but architecturally invalid answers (e.g., Lua CBI instead of LuCI JS)
2. **Hallucination** — inventing code patterns not in the provided source to justify a PASS or FAIL
3. **Fabrication Blindness** — assuming plausible-sounding function calls (like `ubus_reply_create`) are valid APIs

The prescribed fix: shift from a "review this answer" paradigm to an "execute this strict algorithm" paradigm. The scorer must have zero embedded OpenWrt knowledge and rely strictly on rigid key formats, quoting evidence, and pre-run calibration.

This plan defines the concrete file changes, new artifacts, and process gates to make that shift durable. It also incorporates the requirement to capture the scoring AI's own mistakes as a separate "scorer lessons" data file.

---

## 2. Current-State Inventory

| Artifact | Location | Status | Fate |
|---|---|---|---|
| `scoring-prompt-v2.md` | `artifacts/scoring/scoring-prompt-v2.md` | Legacy — embeds hardcoded OpenWrt calibration patterns (lines 187-196) | **Archive** |
| `openwrt-test-scoring-prompt-v2.md` | `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` | Strong baseline but lacks calibration gate, primary-answer isolation, verbatim evidence | **Archive** — superseded by v4 |
| `scoring-plan-draft-for-haiku.txt` | `artifacts/scoring/scoring-plan-draft-for-haiku.txt` | Scratch draft | **Archive** — convert to Markdown |
| `01a-key.md` through `01i-key.md` | `artifacts/tests-keys/` | Inconsistent structure; uses "PASS criteria"/"Immediate fails" instead of the 4-section contract | **Rewrite** — standardize all 9 |
| Calibration fixtures | — | Do not exist | **Create** |
| Scorecard schema | — | Informal only (v2 output schema is underspecified) | **Create** |
| Failure-synthesis agent | — | Does not exist; synthesis currently ad-hoc in orchestrator instructions (lines 134-182 of scoring-prompt-v2.md) | **Create** |
| Scorer lessons log | — | Does not exist | **Create** — captures scorer's own mistakes |

**Existing plans to reference:**
- [scoring-pipeline-implementation-v0.md](../plans/scoring-pipeline-implementation-v0.md) — detailed 7-phase plan with phase-by-phase execution steps and acceptance criteria
- [scoring-implementation-plan-gemini31pro-v0.md](../plans/scoring-implementation-plan-gemini31pro-v0.md) — concise 5-file action plan

This plan synthesizes both, adds the scorer-lessons-log requirement, and references the 10/10 assessment's universal strict scoring prompt (Section 3 of the assessment).

---

## 3. Implementation Phases

Phases are ordered by dependency. Each phase must be complete before the next begins.

### Phase 1 — Archive Legacy Prompts

| Step | Action |
|---|---|
| 1.1 | Create `artifacts/scoring/archive/` directory |
| 1.2 | Move `scoring-prompt-v2.md` to `artifacts/scoring/archive/scoring-prompt-v2.md` — add supersession header |
| 1.3 | Move `openwrt-test-scoring-prompt-v2.md` to `artifacts/scoring/archive/openwrt-test-scoring-prompt-v2.md` — add supersession header |
| 1.4 | Move `scoring-plan-draft-for-haiku.txt` to `artifacts/scoring/archive/scoring-plan-draft-haiku.md` — convert to Markdown |

**Acceptance:** `artifacts/scoring/` contains only active artifacts plus the `archive/` subdirectory.

---

### Phase 2 — Standardize Answer Keys (01a through 01i)

**Source:** Assessment "Files to Edit/Create", row 1.

Every key file in `artifacts/tests-keys/` must be rewritten to follow exactly this 4-section structure:

```markdown
# Batch <ID> Answer Key

**Batch:** `<filename>`
**Scenarios:** <comma-separated IDs>

---

## Scenario <N> — <Name>

### Required Signals
- <pattern the correct answer must contain>

### Automatic Fails
- <pattern that causes immediate failure>

### Allowed Variants
- <acceptable alternative that does NOT trigger a fail>

### Scoring Notes
- <clarifications, boundary cases, key-improvement ideas>
```

| Section | Purpose | Maps From Old Format |
|---|---|---|
| Required Signals | What the scorer must find present | "PASS criteria" |
| Automatic Fails | What causes immediate FAIL regardless of other content | "Immediate fails" |
| Allowed Variants | Explicitly permitted deviations that must NOT be failed | New — eliminates lenience drift |
| Scoring Notes | Edge cases, historical context, known hallucination traps | New — from v2 calibration notes (lines 187-196 of scoring-prompt-v2.md) |

**Execution:** Read each existing key (e.g., 01a-key.md at `artifacts/tests-keys/01a-key.md`), decompose "PASS criteria" into Required Signals, move "Immediate fails" to Automatic Fails, derive Allowed Variants from known acceptable patterns in the cookbook corpus, add Scoring Notes from calibration patterns in the old v2 prompts.

**Acceptance:** Every key file has exactly 4 sections per scenario. No scenario is missing any section (use "None" if genuinely empty).

---

### Phase 3 — Create Calibration Fixtures

**Source:** Assessment "Files to Edit/Create", row 2; Process Plan step 1.

**File:** `artifacts/scoring/openwrt-calibration-fixtures.md`

This file contains 5 mocked test scenarios with pre-determined verdicts. The scoring agent MUST pass all 5 before grading real tests. If calibration fails, the run aborts.

#### Required Fixture Coverage

| Fixture | Failure Mode Tested | Verdict |
|---|---|---|
| 1 | Contains an Automatic Fails pattern | FAIL |
| 2 | Missing a Required Signal (not excused by Allowed Variants) | FAIL |
| 3 | Correct answer with superficially concerning but Allowed Variant | PASS |
| 4 | Primary answer wrong, alternative correct (primary-answer rule) | FAIL |
| 5 | Doubtful/borderline case not resolved by key | PASS (do not count) |

Fixtures must be domain-agnostic — they test the rule engine, not OpenWrt expertise. A fresh LLM with zero OpenWrt context should be able to correctly grade all 5 fixtures by following only the key excerpts and the v4 prompt rules.

**Acceptance:** Calibration fixtures exist, cover all 5 required failure modes, and are referenceable from the v4 prompt's Phase 1.

---

### Phase 4 — Freeze Scorecard Schema

**Source:** Assessment "Files to Edit/Create", row 3; Process Plan step 5.

**File:** `artifacts/scoring/openwrt-scorecard-schema.md`

Frozen schema with 5 mandatory columns:

| Column | Type | Description |
|---|---|---|
| `test_taker` | string | Name of the model/agent being scored |
| `scenario` | string | Scenario ID (e.g., `04`) |
| `quoted_evidence` | string | EXACT literal line(s) from the answer that triggered the violation. Paraphrasing forbidden. |
| `first_definite_wrong_detail` | string | Concise description of what is wrong (20 words or fewer) |
| `key_reason` | string | Short reason tied directly to the key's Automatic Fails or Required Signals |

#### Reconciliation Rules

The scorecard MUST include:
1. **Per-Test-Taker Summary** — one row per test-taker with `failure_scenarios` list and `failure_count`
2. **Totals** — `total_fail_rows`, `sum_of_failure_count`, `totals_match` (YES/NO)
3. The scorer must verify: `total_fail_rows == sum_of_failure_count` before finalizing

**Acceptance:** Schema document is self-contained with valid and error example scorecards.

---

### Phase 5 — Create the V4 Strict Scoring Prompt

**Source:** Assessment Section 3 "The 10/10 Universal Strict Scoring Prompt" (lines 52-131 of `openwrt-scoring-assessment-10-10.md`).

**File:** `artifacts/scoring/openwrt-test-scoring-prompt-v4.md`

Use the exact prompt text from the 10/10 assessment. Key design principles:

1. **Zero embedded OpenWrt knowledge** — pure rule engine
2. **Strict execution sequence** — calibration, scope, grading, output, reconciliation
3. **Primary Answer Isolation** — first complete code block is the only answer scored
4. **Verbatim Evidence Extraction** — violations must be quoted literally
5. **Key Ingestion Gate** — valid scenario IDs extracted from key; all others ignored

**Acceptance:** Prompt is self-contained, references only key files and calibration fixtures, produces output matching the frozen schema.

---

### Phase 6 — Create Failure-Synthesis Prompt

**Source:** Assessment "Files to Edit/Create", row 5.

**File:** `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

A separate agent phase that runs AFTER scoring is complete. It reads finalized scorecards and outputs prioritized documentation tasks based on clustered failure points. This replaces the ad-hoc orchestrator synthesis instructions currently embedded in scoring-prompt-v2.md (lines 134-182).

#### Responsibilities

1. Read all batch scorecards produced by the v4 scorer
2. Cluster failures by scenario and failure pattern
3. For each cluster, determine: fail count, dominant wrong approach, whether cookbook already covers this, recommended action
4. Output prioritized task list with documentation backlog and key enhancement backlog

#### Output Schema

```markdown
# Failure Synthesis Report

## Cluster Summary
| Scenario | Fail Count | Dominant Pattern | Recommended Action | Priority |

## Documentation Backlog
[ ] DOC: <title>
    Gap: <what models got wrong>
    Correct pattern: <what docs should teach>
    Affected scenarios: <list>
    Priority: HIGH / MEDIUM / LOW

## Key Enhancement Backlog
- Scenario <N>: <specific wording improvement for the key>
```

**Acceptance:** Synthesis prompt produces structured output mapping directly to cookbook authoring decisions.

---

### Phase 7 — Create Scorer Lessons Log

**Source:** User requirement — the scoring AI's own mistakes and hallucinations are valuable data that should be captured in a separate file from the test results.

**File:** `artifacts/scoring/openwrt-scorer-lessons-log.md`

When the scorer misgrades a scenario (caught during calibration, reconciliation, or human review), that misgrading becomes a lesson that improves future scoring runs. This is a unique advantage of using a less-intelligent scorer: we learn about both the test-taker's mistakes AND the scorer's mistakes.

#### Log Entry Schema

```markdown
## Lesson <N> — <Short Title>

**Date:** <date>
**Run:** <batch key or calibration run>
**Scorer Model:** <model name>

### What the Scorer Got Wrong
<description of the misgrading>

### Root Cause
- [ ] Calibration gap (scorer did not understand a rule)
- [ ] Key ambiguity (key did not clearly forbid/require the pattern)
- [ ] Hallucination (scorer invented a pattern not in the answer or key)
- [ ] Lenience drift (scorer accepted functionally plausible but architecturally wrong answer)
- [ ] Primary-answer violation (scorer rescued an answer using a later alternative)

### Fix Applied
<what was changed — key wording, prompt wording, calibration fixture added, etc.>

### Preventive Rule
<one-line rule added to the prompt or key to prevent recurrence>
```

#### Seeded Lessons (from the 10/10 assessment)

| Lesson | Scorer | Mistake | Root Cause |
|---|---|---|---|
| 1 | GPT-5.4 | Missed 3 genuine code failures; trusted LLM over code | Lenience drift |
| 2 | GPT-5.4 | Hardcoded 7 calibration patterns in prompt, making it brittle | Prompt rigidity |
| 3 | Claude Sonnet 4.6 | Missing integrated calibration fixtures | Prompt incompleteness |
| 4 | All scorers | Scenario 13 primary-answer rule not yet in key | Key ambiguity |
| 5 | All scorers | Scenario 22 fabricated API `ubus_reply_create` not flagged | Key ambiguity |

**Acceptance:** The log contains at least 5 seeded lessons from the assessment and is structured for incremental growth after each scoring run.

---

## 4. File Change Summary

| File | Action | Phase |
|---|---|---|
| `artifacts/scoring/archive/` | Create directory | 1 |
| `artifacts/scoring/archive/scoring-prompt-v2.md` | Move + annotate | 1 |
| `artifacts/scoring/archive/openwrt-test-scoring-prompt-v2.md` | Move + annotate | 1 |
| `artifacts/scoring/archive/scoring-plan-draft-haiku.md` | Move + convert | 1 |
| `artifacts/tests-keys/01a-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01b-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01c-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01d-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01e-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01f-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01g-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01h-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/tests-keys/01i-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/scoring/openwrt-calibration-fixtures.md` | Create | 3 |
| `artifacts/scoring/openwrt-scorecard-schema.md` | Create | 4 |
| `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` | Create | 5 |
| `artifacts/scoring/openwrt-failure-synthesis-prompt.md` | Create | 6 |
| `artifacts/scoring/openwrt-scorer-lessons-log.md` | Create + seed | 7 |

---

## 5. Operational Gates

These gates define the scoring run lifecycle. Each gate must pass before the next begins.

```
Gate 1: Calibration          Scorer runs calibration fixtures. All 5 must match expected verdicts.
         |                   On failure: abort run, log lesson, fix prompt/key, retry.
         v
Gate 2: Key Ingestion         Scorer extracts valid scenario IDs from the key.
         |                   Any result-file scenario not in this list is ignored.
         v
Gate 3: Primary Answer        For each scenario, isolate FIRST complete code block.
    Isolation                 Subsequent alternatives do NOT rescue a wrong primary.
         |
         v
Gate 4: Verbatim              Every failure row has quoted_evidence copied literally.
    Evidence Extraction       No paraphrasing. No summaries. Exact text only.
         |
         v
Gate 5: Scorecard             Build scorecard per frozen schema.
    Gen & Reconciliation      Verify total_fail_rows == sum_of_failure_count.
         |                   On mismatch: recalculate, do not narrate.
         v
Gate 6: Synthesis             Run failure-synthesis agent on finalized scorecards.
    (Separate Agent)          Output prioritized docs/Jira backlog.
```

---

## 6. Acceptance Criteria

The implementation is complete when:

1. All 9 key files use the standardized 4-section format
2. Calibration fixtures exist and cover all 5 required failure modes
3. Scorecard schema is frozen and documented with examples
4. V4 prompt is self-contained, domain-agnostic, and references only key files and calibration fixtures
5. Failure-synthesis prompt produces structured output matching the defined schema
6. Scorer lessons log is seeded with assessment-derived lessons
7. Legacy v2 prompts are archived with supersession notes
8. A fresh LLM with zero OpenWrt context can successfully run a scoring end-to-end using only the v4 prompt, key files, and calibration fixtures

---

## 7. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Key rewrite introduces ambiguity | Scorer misgrades real scenarios | Run calibration fixtures after each key rewrite; any deviation triggers review |
| Calibration fixtures are too easy | False confidence in scorer | Include at least one borderline PASS case (fixture 5) that tests restraint |
| Scorer hallucinates quoted_evidence | Invalid scorecard rows | Enforce verbatim-only rule in prompt; human spot-check 10% of rows |
| Scorecard reconciliation fails silently | Math errors propagate | Gate 5 requires explicit YES/NO on totals_match; NO triggers auto-recalculation |
| Failure synthesis produces low-signal clusters | Wasted documentation effort | Synthesis agent must cite specific scorecard rows for each cluster |
