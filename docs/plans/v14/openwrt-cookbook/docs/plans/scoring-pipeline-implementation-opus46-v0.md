# Scoring Pipeline Implementation Plan — opus46-v0

**Status:** Proposed
**Date:** 2026-04-07
**Source:** [`artifacts/scoring/openwrt-scoring-assessment-10-10.md`](../../artifacts/scoring/openwrt-scoring-assessment-10-10.md)
**Scope:** Answer keys, calibration fixtures, scorecard schema, strict scoring prompt, failure-synthesis prompt, scorer-lessons log, legacy archival, and the operational gates that bind them.

---

## 1. Purpose

The 10/10 scoring assessment identified three systemic failure modes in LLM-based test scoring:

1. **Lenience/Drift** — accepting functionally similar but architecturally invalid answers (e.g., Lua CBI instead of LuCI JS)
2. **Hallucination** — inventing code patterns not in the provided source to justify a PASS or FAIL
3. **Fabrication Blindness** — assuming plausible-sounding function calls (like `ubus_reply_create`) are valid APIs

The prescribed fix: shift from a "review this answer" paradigm to an "execute this strict algorithm" paradigm. The scorer must have zero embedded OpenWrt knowledge and rely strictly on rigid key formats, verbatim quoting of evidence, and pre-run calibration.

This plan defines the concrete file changes, new artifacts, process gates, and agent-launch templates to make that shift durable. It also captures the scoring AI's own mistakes as a separate lessons file — a unique advantage of using a less-intelligent scorer.

### Prior work

- [`scoring-implementation-plan-gemini31pro-v0.md`](scoring-implementation-plan-gemini31pro-v0.md) — concise 5-file action plan
- [`scoring-pipeline-implementation-qwen36plus-v2.md`](scoring-pipeline-implementation-qwen36plus-v2.md) — thorough 7-phase plan with operational gates and agent templates
- Assessment evaluations: GPT-5.4 (6.5/10 accuracy, missed 3 failures, hardcoded calibration), Claude Sonnet 4.6 (9.5/10, found hallucination issue, missing calibration gate), Qwen36Plus (10/10, withheld Scenario 13 pending key update)

---

## 2. Current-State Inventory

Verify this inventory before starting Phase 1. If any file is missing or has moved, update the plan before proceeding.

| Artifact | Path (from cookbook root) | Status | Action |
|---|---|---|---|
| Legacy scoring prompt | `artifacts/scoring/scoring-prompt-v2.md` | Hardcoded OpenWrt patterns (lines 187–196), ad-hoc orchestrator synthesis (lines 134–182) | **Archive** |
| Baseline scoring prompt | `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` | Strong but lacks calibration gate, primary-answer isolation, verbatim evidence | **Archive** → superseded by v4 |
| Haiku scratch plan | `artifacts/scoring/scoring-plan-draft-for-haiku.txt` | Raw .txt draft | **Archive** → convert to .md |
| Answer keys 01a–01i | `artifacts/tests-keys/01a-key.md` through `01i-key.md` | Inconsistent format: "PASS criteria" / "Immediate fails" instead of 4-section standard | **Rewrite** all 9 |
| Scoring assessments (4) | `artifacts/scoring/openwrt-scoring-assessment-*.md` | Completed analysis from GPT-5.4, Sonnet, Qwen, and the 10/10 synthesis | **Keep** as evidence |
| Haiku scoring outputs | `artifacts/scoring/haiku/` | Historical scoring run data | **Keep** as evidence |
| Calibration fixtures | — | Do not exist | **Create** |
| Scorecard schema | — | Informal only (v2 output underspecified) | **Create** |
| Failure-synthesis prompt | — | Does not exist; synthesis is ad-hoc in scoring-prompt-v2.md lines 134–182 | **Create** |
| Scorer lessons log | — | Does not exist | **Create** |

---

## 3. Implementation Phases

Phases are dependency-ordered. Each must complete before the next begins.

### Phase 0 — Validate Current State

| Step | Action |
|---|---|
| 0.1 | Confirm all files in the inventory table above exist at their listed paths |
| 0.2 | Confirm `artifacts/tests-keys/` contains exactly 9 key files (01a through 01i) |
| 0.3 | Confirm `artifacts/scoring/` contains both v2 prompts and the haiku scratch plan |
| 0.4 | Record any discrepancies in a `## Pre-Implementation Notes` section appended to this plan |

**Gate:** Proceed only when the inventory matches or discrepancies are documented and non-blocking.

---

### Phase 1 — Archive Legacy Prompts

| Step | Action |
|---|---|
| 1.1 | Create `artifacts/scoring/archive/` directory |
| 1.2 | Move `artifacts/scoring/scoring-prompt-v2.md` → `artifacts/scoring/archive/scoring-prompt-v2.md`. Prepend: `> Superseded by openwrt-test-scoring-prompt-v4.md` |
| 1.3 | Move `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` → `artifacts/scoring/archive/openwrt-test-scoring-prompt-v2.md`. Prepend same note. |
| 1.4 | Move `artifacts/scoring/scoring-plan-draft-for-haiku.txt` → `artifacts/scoring/archive/scoring-plan-draft-haiku.md`. Convert to markdown. |

**Acceptance:** `artifacts/scoring/` contains only active artifacts (assessments, haiku/, and the archive/ subdirectory). No v2 prompts at the top level.

---

### Phase 2 — Standardize Answer Keys (01a through 01i)

**Source:** Assessment Section 2, "Files to Edit/Create", row 1.

Every key file in `artifacts/tests-keys/` must be rewritten to exactly this 4-section structure per scenario:

```markdown
## Scenario <N> — <Name>

### Required Signals
- <pattern the correct answer MUST contain>

### Automatic Fails
- <pattern that causes immediate FAIL regardless of other content>

### Allowed Variants
- <acceptable alternative that must NOT trigger a fail>

### Scoring Notes
- <edge cases, known hallucination traps, boundary clarifications>
```

| Old Format | New Section | Purpose |
|---|---|---|
| "PASS criteria" | **Required Signals** | What the scorer must find present |
| "Immediate fails" | **Automatic Fails** | What causes immediate FAIL |
| *(did not exist)* | **Allowed Variants** | Explicitly permitted deviations — eliminates lenience drift by making permissiveness explicit |
| *(did not exist)* | **Scoring Notes** | Edge cases; absorbs domain-specific calibration from scoring-prompt-v2.md lines 187–196 |

| Step | Action |
|---|---|
| 2.1 | For each key file (01a through 01i): read existing content |
| 2.2 | Decompose "PASS criteria" into **Required Signals** |
| 2.3 | Move "Immediate fails" into **Automatic Fails** verbatim |
| 2.4 | Add **Allowed Variants** — derive from known acceptable patterns in the cookbook corpus, prior scoring runs in `artifacts/scoring/haiku/`, and `artifacts/runs/` evidence |
| 2.5 | Add **Scoring Notes** — migrate any scenario-specific calibration from `artifacts/scoring/archive/scoring-prompt-v2.md` lines 187–196 into the key itself so the key carries the guardrail |
| 2.6 | Verify all 9 keys parse cleanly: every scenario has all 4 sections (use "None" if genuinely empty) |

**Acceptance:** Every key file has exactly 4 sections per scenario. No scenario is missing any section.

---

### Phase 3 — Create Calibration Fixtures

**Source:** Assessment Section 2, "Process Plan" step 1.
**File:** `artifacts/scoring/openwrt-calibration-fixtures.md`

This file contains 5 mocked test scenarios with pre-determined verdicts. The scoring agent MUST pass all 5 before grading real tests. If calibration fails, the run aborts.

The fixtures are domain-agnostic — they test the scorer's ability to follow rules, NOT its OpenWrt knowledge. Each fixture simulates a pattern type that maps to real OpenWrt failure modes without requiring domain expertise to evaluate:

| Fixture | Tests This Rule | Simulates This Real Failure Mode | Expected Verdict |
|---|---|---|---|
| 1 | Automatic Fails detection | Deprecated API usage (e.g., Lua CBI instead of LuCI JS) | FAIL |
| 2 | Missing Required Signal detection | Omitting a mandatory pattern (e.g., missing procd lifecycle hook) | FAIL |
| 3 | Allowed Variant tolerance | Superficially suspicious but explicitly permitted alternative | PASS |
| 4 | Primary Answer Rule enforcement | First answer wrong, second answer correct (e.g., wrong API in first block, correct in second) | FAIL |
| 5 | Restraint under ambiguity | Borderline case not clearly resolved by key | PASS (do not count) |

Each fixture follows this template:

```markdown
## Fixture <N> — <Rule Being Tested>

### Key Excerpt
<Required Signals / Automatic Fails / Allowed Variants / Scoring Notes>

### Test-Taker Answer
<simulated code block or prose>

### Expected Verdict: PASS | FAIL
### Expected Reason: <one-line explanation tied to the key>
```

| Step | Action |
|---|---|
| 3.1 | Create `artifacts/scoring/openwrt-calibration-fixtures.md` |
| 3.2 | Write all 5 fixtures using generic patterns (e.g., "function uses `deprecated_call()`" instead of real OpenWrt APIs) |
| 3.3 | Include expected verdict and reason for each |
| 3.4 | Add a header note: "These fixtures test rule comprehension, not domain knowledge. A fresh LLM with zero OpenWrt context must pass all 5." |

**Acceptance:** A fresh LLM with no OpenWrt knowledge can correctly grade all 5 fixtures using only the fixture's key excerpt and the v4 prompt rules.

---

### Phase 4 — Freeze Scorecard Schema

**Source:** Assessment Section 2, "Process Plan" step 5; Assessment Section 3, "Required Output Schema".
**File:** `artifacts/scoring/openwrt-scorecard-schema.md`

| Column | Type | Description |
|---|---|---|
| `test_taker` | string | Name of the model/agent being scored |
| `scenario` | string | Scenario ID (e.g., `04`) |
| `quoted_evidence` | string | EXACT literal line(s) from the answer that triggered the violation. Paraphrasing is forbidden. |
| `first_definite_wrong_detail` | string | What is wrong (20 words max) |
| `key_reason` | string | Reason tied directly to the key's Automatic Fails or Required Signals |

The scorecard MUST include these summary sections after the failure records:

1. **Scope** — batch key filename, allowed scenario IDs, test-takers scored
2. **Failure Records** — one row per failure, using the 5-column schema
3. **Per-Test-Taker Summary** — one row per test-taker with `failure_scenarios` list and `failure_count`
4. **Totals** — `total_fail_rows`, `sum_of_failure_count`, `totals_match` (YES/NO)
5. **Key Improvement Ideas** — possible fabrications, ambiguous key wording, suggested additions

The scorer must verify `total_fail_rows == sum_of_failure_count` before finalizing. On mismatch: recalculate silently, do not narrate.

| Step | Action |
|---|---|
| 4.1 | Create `artifacts/scoring/openwrt-scorecard-schema.md` |
| 4.2 | Document the 5 mandatory columns |
| 4.3 | Document all 5 output sections with their rules |
| 4.4 | Include a complete valid example scorecard |
| 4.5 | Include an example of a reconciliation error and how to self-correct |

**Acceptance:** The schema is self-contained. Any reference to it from the v4 prompt resolves without ambiguity.

---

### Phase 5 — Create the V4 Strict Scoring Prompt

**Source:** Assessment Section 3, "The 10/10 Universal Strict Scoring Prompt" (the full prompt text).
**File:** `artifacts/scoring/openwrt-test-scoring-prompt-v4.md`

This is the master scoring prompt. It supersedes both v2 prompts. Design principles:

1. **Zero embedded OpenWrt knowledge** — the prompt is a pure rule engine
2. **Strict 5-phase execution sequence** — calibration → scope → grading → recording → reconciliation
3. **Primary Answer Isolation** — first complete code block is the only answer scored
4. **Verbatim Evidence Extraction** — violations must be quoted literally, never paraphrased
5. **Key Ingestion Gate** — valid scenario IDs are extracted from the key; all others are ignored

The prompt's content should be based on the assessment's Section 3 text (lines 52–131 of `artifacts/scoring/openwrt-scoring-assessment-10-10.md`), adapted to reference the calibration fixtures file and scorecard schema file created in Phases 3–4.

| Step | Action |
|---|---|
| 5.1 | Create `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` |
| 5.2 | Start with the assessment's prompt text as the foundation |
| 5.3 | Replace inline schema references with: "Output per `openwrt-scorecard-schema.md`" |
| 5.4 | Replace inline calibration references with: "Run calibration per `openwrt-calibration-fixtures.md`" |
| 5.5 | Add the Primary Answer Rule exception clause (explicit "bad example" labeling) |
| 5.6 | Add the Fabricated API handling rule (record under Key Improvement Ideas, only fail if key warns) |
| 5.7 | Include the ready-to-use assignment template (see Section 8.1) at the bottom |

**Acceptance:** The prompt is self-contained, references only key files and calibration fixtures (no hardcoded domain knowledge), and would produce output matching the frozen schema.

---

### Phase 6 — Create Failure-Synthesis Prompt

**Source:** Assessment Section 2, "Files to Edit/Create", row 5.
**File:** `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

This is a separate agent phase that runs AFTER scoring is complete. It reads finalized scorecards and clusters failures into actionable documentation work.

The synthesis agent:
1. Reads all batch scorecards produced by the v4 scorer
2. Clusters failures by scenario and by dominant wrong pattern
3. For each cluster: counts how many test-takers failed, identifies the dominant wrong approach, checks whether the cookbook already covers this lesson, recommends action (new page / extend existing / golden-key update / reject)
4. Outputs a prioritized task list

Output schema:

```markdown
# Failure Synthesis Report

## Cluster Summary
| Scenario | Fail Count | Dominant Wrong Pattern | Cookbook Coverage | Recommended Action | Priority |
|---|---|---|---|---|---|

## Documentation Backlog
- [ ] DOC: <title>
      Gap: <what models got wrong>
      Correct pattern: <what docs should teach>
      Source: <OpenWrt repo path or authority>
      Affected scenarios: <list>
      Priority: HIGH / MEDIUM / LOW

## Key Enhancement Backlog
- Scenario <N>: <specific wording improvement for the key>
```

| Step | Action |
|---|---|
| 6.1 | Create `artifacts/scoring/openwrt-failure-synthesis-prompt.md` |
| 6.2 | Define the input contract: reads finalized scorecards from Phase 5 output |
| 6.3 | Define clustering rules: group by scenario, then by dominant pattern |
| 6.4 | Define the output schema above |
| 6.5 | Include the ready-to-use assignment template (see Section 8.2) |

**Acceptance:** The synthesis prompt produces structured, actionable output that maps directly to cookbook authoring decisions per `08-cookbook-authoring-execution-contract.md`.

---

### Phase 7 — Create Scorer Lessons Log

**Source:** User requirement — the scoring AI's own mistakes are valuable data about AI competency on OpenWrt. Using a less-intelligent scorer (like Haiku) reveals both the test-taker's mistakes AND the scorer's mistakes.
**File:** `artifacts/scoring/openwrt-scorer-lessons-log.md`

This is a persistent, append-only log. When the scorer misgrades a scenario — caught during calibration, reconciliation, or human review — that misgrading becomes a lesson.

Entry schema:

```markdown
## Lesson <N> — <Short Title>

**Date:** <date>
**Run:** <batch key or calibration run>
**Scorer Model:** <model name>

### What the Scorer Got Wrong
<description>

### Root Cause
- [ ] Calibration gap (didn't understand a rule)
- [ ] Key ambiguity (key didn't clearly forbid/require the pattern)
- [ ] Hallucination (invented a pattern not in the answer or key)
- [ ] Lenience drift (accepted architecturally wrong but functionally plausible answer)
- [ ] Primary-answer violation (rescued an answer using a later alternative)

### Fix Applied
<what was changed — key wording, prompt wording, calibration fixture added>

### Preventive Rule
<one-line rule added to prevent recurrence>
```

Seed with these lessons from the assessment:

| # | Scorer | Mistake | Root Cause |
|---|---|---|---|
| 1 | GPT-5.4 | Missed 3 genuine code failures; trusted LLM output over code evidence | Lenience drift |
| 2 | GPT-5.4 | Hardcoded 7 calibration patterns in prompt, making it brittle for unseen scenarios | Prompt rigidity (not a root cause category — file as calibration gap) |
| 3 | Claude Sonnet 4.6 | Missing integrated calibration fixtures; no pre-run verification | Calibration gap |
| 4 | All scorers | Scenario 13: primary-answer rule not yet established in key | Key ambiguity |
| 5 | All scorers | Scenario 22: fabricated API `ubus_reply_create` not flagged in key | Key ambiguity |

| Step | Action |
|---|---|
| 7.1 | Create `artifacts/scoring/openwrt-scorer-lessons-log.md` |
| 7.2 | Seed with the 5 lessons above, using the full entry schema |
| 7.3 | Add a maintenance note: after each scoring run, the operator reviews any reconciliation failures or human-overturned verdicts and adds entries |
| 7.4 | Reference this log from the v4 prompt's Key Improvement Ideas section |

**Acceptance:** The log contains at least 5 seeded lessons and is structured for incremental growth.

---

## 4. File Change Summary

| File | Action | Phase |
|---|---|---|
| `artifacts/scoring/archive/` | Create directory | 1 |
| `artifacts/scoring/archive/scoring-prompt-v2.md` | Move + supersession note | 1 |
| `artifacts/scoring/archive/openwrt-test-scoring-prompt-v2.md` | Move + supersession note | 1 |
| `artifacts/scoring/archive/scoring-plan-draft-haiku.md` | Move + convert from .txt | 1 |
| `artifacts/tests-keys/01a-key.md` through `01i-key.md` | Rewrite to 4-section format | 2 |
| `artifacts/scoring/openwrt-calibration-fixtures.md` | Create | 3 |
| `artifacts/scoring/openwrt-scorecard-schema.md` | Create | 4 |
| `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` | Create | 5 |
| `artifacts/scoring/openwrt-failure-synthesis-prompt.md` | Create | 6 |
| `artifacts/scoring/openwrt-scorer-lessons-log.md` | Create + seed | 7 |

Total: 3 moves, 9 rewrites, 5 creates.

---

## 5. Operational Gates

These gates define the scoring run lifecycle. Each must pass before the next.

```
Phase 0: Validate Inventory
    │ All files exist at expected paths
    v
┌──────────────────────────┐
│  Gate 1: Calibration     │  Scorer runs 5 fixtures.
│                          │  All verdicts must match expected.
│                          │  On failure: ABORT, log lesson, fix, retry.
└────────────┬─────────────┘
             │ PASS
             v
┌──────────────────────────┐
│  Gate 2: Key Ingestion   │  Scorer extracts valid scenario IDs from key.
│                          │  Any result-file scenario not in key → ignored.
└────────────┬─────────────┘
             │ PASS
             v
┌──────────────────────────┐
│  Gate 3: Primary Answer  │  For each scenario, isolate FIRST code block.
│  Isolation               │  Later alternatives do NOT rescue a wrong primary.
└────────────┬─────────────┘
             │ per scenario
             v
┌──────────────────────────┐
│  Gate 4: Verbatim        │  Every failure row has quoted_evidence copied
│  Evidence Extraction     │  literally. No paraphrasing. No summaries.
└────────────┬─────────────┘
             │ per failure
             v
┌──────────────────────────┐
│  Gate 5: Scorecard Gen   │  Build scorecard per frozen schema.
│  & Reconciliation        │  Verify total_fail_rows == sum_of_failure_count.
│                          │  On mismatch: recalculate silently.
└────────────┬─────────────┘
             │ PASS
             v
┌──────────────────────────┐
│  Gate 6: Synthesis       │  Separate agent reads finalized scorecards.
│  (Post-scoring)          │  Outputs prioritized documentation backlog.
└──────────────────────────┘
```

---

## 6. Integration with Parent Pipeline

Scoring outputs feed into the cookbook authoring workflow defined by two existing contracts:

- **`08-cookbook-authoring-execution-contract.md`** — defines how an agent turns an admitted scenario (with its scored failures) into a staged draft with creation log. The failure-synthesis report from Gate 6 provides the prioritized input queue for this contract.

- **`09-staged-authoring-lifecycle.md`** — defines the draft → log → review → promotion lifecycle. Scored failures with their `quoted_evidence` and `key_reason` fields become the primary evidence cited in cookbook drafts.

The flow: Gate 5 (scorecards) → Gate 6 (synthesis report) → `08` (authoring) → `09` (staging) → `10-human-review-procedure.md` (promotion) → `static/cookbook-source/`.

---

## 7. Acceptance Criteria

The implementation is complete when:

1. All 9 key files use the standardized 4-section format with no missing sections
2. Calibration fixtures exist and cover all 5 required rule-comprehension tests
3. Scorecard schema is frozen and documented with valid and invalid examples
4. V4 prompt is self-contained, domain-agnostic, and references only key files and calibration fixtures
5. Failure-synthesis prompt produces structured output mapping to cookbook authoring decisions
6. Scorer lessons log is seeded with 5 assessment-derived lessons
7. Legacy v2 prompts are archived with supersession notes
8. A fresh LLM with zero OpenWrt context can successfully run calibration and score a batch using only the v4 prompt, key files, and calibration fixtures

---

## 8. Ready-To-Use Assignment Templates

### 8.1 Scorer Agent Launch

```
You are the OpenWrt Cookbook Universal Strict Batch Scorer.

Read these files in order:
1. artifacts/scoring/openwrt-test-scoring-prompt-v4.md — your operating instructions
2. artifacts/scoring/openwrt-calibration-fixtures.md — your calibration test (run this FIRST)
3. artifacts/tests-keys/<batch>-key.md — the answer key for this batch
4. artifacts/runs/<test-taker>/results/<batch>-result.md — the test-taker's answers

Execute the v4 prompt exactly. If calibration fails, stop and report:
"Calibration Failed. Review required."

If calibration passes, grade all in-scope scenarios and output the scorecard
per the frozen schema in artifacts/scoring/openwrt-scorecard-schema.md.
```

### 8.2 Failure-Synthesis Agent Launch

```
You are the OpenWrt Failure Synthesis Agent.

Read these files:
1. artifacts/scoring/openwrt-failure-synthesis-prompt.md — your operating instructions
2. All finalized scorecard files produced by the v4 scorer for this round

Cluster the failures by scenario and pattern. Output the synthesis report
per the schema defined in your operating instructions.
```

### 8.3 Human Operator Quick Reference

| Step | Action | Files |
|---|---|---|
| 0 | Verify inventory matches this plan | Section 2 table |
| 1 | Archive old prompts | Phase 1 |
| 2 | Rewrite all 9 keys to 4-section format | Phase 2, `artifacts/tests-keys/` |
| 3 | Create calibration fixtures | Phase 3, `artifacts/scoring/openwrt-calibration-fixtures.md` |
| 4 | Create scorecard schema | Phase 4, `artifacts/scoring/openwrt-scorecard-schema.md` |
| 5 | Create v4 scoring prompt | Phase 5, `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` |
| 6 | Create failure-synthesis prompt | Phase 6, `artifacts/scoring/openwrt-failure-synthesis-prompt.md` |
| 7 | Create and seed scorer lessons log | Phase 7, `artifacts/scoring/openwrt-scorer-lessons-log.md` |
| 8 | Launch scorer agent | Copy template 8.1 |
| 9 | If calibration fails: log lesson, fix, retry | Add entry to scorer lessons log |
| 10 | If scoring passes: launch synthesis agent | Copy template 8.2 |
| 11 | Review scorecard + synthesis output | Spot-check 10% of `quoted_evidence` rows |
| 12 | Record any scorer mistakes | Add entries to scorer lessons log |

---

## 9. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Key rewrite introduces ambiguity | Scorer misgrades real scenarios | Run calibration fixtures after each key rewrite; deviation triggers review |
| Calibration fixtures are too easy | False confidence in scorer ability | Fixture 5 (borderline PASS) specifically tests restraint under ambiguity |
| Scorer hallucinates `quoted_evidence` | Invalid scorecard rows | Verbatim-only rule in prompt + human spot-check of 10% of rows |
| Scorecard math fails silently | Propagated errors in synthesis | Gate 5 requires explicit YES/NO on `totals_match`; NO triggers auto-recalculation |
| Synthesis produces low-signal clusters | Wasted documentation effort | Synthesis agent must cite specific scorecard rows for each cluster; minimum 2 test-taker failures to warrant a DOC task |
