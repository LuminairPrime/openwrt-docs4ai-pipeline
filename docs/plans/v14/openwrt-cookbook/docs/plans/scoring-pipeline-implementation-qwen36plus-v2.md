# Scoring Pipeline Implementation Plan — qwen36plus-v2

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

This plan defines the concrete file changes, new artifacts, process gates, and agent-launch templates to make that shift durable. It also captures the scoring AI's own mistakes as a separate "scorer lessons" data file.

**Existing plans to reference:**
- [scoring-implementation-plan-gemini31pro-v0.md](scoring-implementation-plan-gemini31pro-v0.md) — concise 5-file action plan with human operator integration note
- [scoring-pipeline-implementation-qwen36plus-v1.md](scoring-pipeline-implementation-qwen36plus-v1.md) — prior iteration with file change summary and seeded lessons table

---

## 2. Current-State Inventory

| Artifact | Location | Status | Fate |
|---|---|---|---|
| `scoring-prompt-v2.md` | `artifacts/scoring/scoring-prompt-v2.md` | Legacy — embeds hardcoded OpenWrt calibration patterns (lines 187-196) and ad-hoc orchestrator synthesis (lines 134-182) | **Archive** |
| `openwrt-test-scoring-prompt-v2.md` | `artifacts/scoring/openwrt-test-scoring-prompt-v2.md` | Strong baseline but lacks calibration gate, primary-answer isolation, verbatim evidence | **Archive** — superseded by v4 |
| `scoring-plan-draft-for-haiku.txt` | `artifacts/scoring/scoring-plan-draft-for-haiku.txt` | Scratch draft | **Archive** — convert to Markdown |
| `01a-key.md` through `01i-key.md` | `artifacts/tests-keys/` | Inconsistent structure; uses "PASS criteria"/"Immediate fails" instead of the 4-section contract | **Rewrite** — standardize all 9 |
| Calibration fixtures | — | Do not exist | **Create** |
| Scorecard schema | — | Informal only (v2 output schema is underspecified) | **Create** |
| Failure-synthesis agent | — | Does not exist; synthesis currently ad-hoc in orchestrator instructions (lines 134-182 of scoring-prompt-v2.md) | **Create** |
| Scorer lessons log | — | Does not exist | **Create** — captures scorer's own mistakes |

---

## 3. Implementation Phases

Phases are ordered by dependency. Each phase must be complete before the next begins.

### Phase 1 — Archive Legacy Prompts

| Step | Action |
|---|---|
| 1.1 | Create `artifacts/scoring/archive/` directory |
| 1.2 | Move `scoring-prompt-v2.md` to `artifacts/scoring/archive/scoring-prompt-v2.md` — prepend `> Superseded by openwrt-test-scoring-prompt-v4.md` |
| 1.3 | Move `openwrt-test-scoring-prompt-v2.md` to `artifacts/scoring/archive/openwrt-test-scoring-prompt-v2.md` — prepend `> Superseded by openwrt-test-scoring-prompt-v4.md` |
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
| Allowed Variants | Explicitly permitted deviations that must NOT be failed | New — eliminates lenience drift by making permissiveness explicit |
| Scoring Notes | Edge cases, historical context, known hallucination traps | New — from v2 calibration notes (lines 187-196 of scoring-prompt-v2.md) |

#### Execution Steps

| Step | Action |
|---|---|
| 2.1 | Read each existing key (`01a-key.md` through `01i-key.md`) |
| 2.2 | For each scenario, decompose existing "PASS criteria" into **Required Signals** |
| 2.3 | Move existing "Immediate fails" into **Automatic Fails** verbatim |
| 2.4 | Add **Allowed Variants** — derive from known acceptable patterns in the cookbook corpus and prior scoring runs |
| 2.5 | Add **Scoring Notes** — include any calibration patterns from `scoring-prompt-v2.md` lines 187-196 that are scenario-specific, so the key itself carries the domain guardrail instead of the prompt |
| 2.6 | Verify all 9 keys parse cleanly into the 4-section structure |

**Acceptance:** Every key file has exactly the 4 sections per scenario. No scenario is missing any section (use "None" if a section is genuinely empty).

---

### Phase 3 — Create Calibration Fixtures

**Source:** Assessment "Files to Edit/Create", row 2; Process Plan step 1.

**File:** `artifacts/scoring/openwrt-calibration-fixtures.md`

This file contains 5 mocked test scenarios with pre-determined verdicts. The scoring agent MUST pass all 5 before grading real tests. If calibration fails, the run aborts.

#### Fixture Design Template

Each fixture follows this structure:

```markdown
## Fixture <N>

### Scenario ID: <mock-ID>
### Key Excerpt:
<Required Signals / Automatic Fails / Allowed Variants / Scoring Notes>

### Test-Taker Answer:
<code block or prose simulating a model answer>

### Expected Verdict: PASS | FAIL
### Expected Key Reason: <one-line reason matching the key>
```

#### Required Fixture Coverage

| Fixture | Failure Mode Tested | Verdict |
|---|---|---|
| 1 | Contains an Automatic Fails pattern | FAIL |
| 2 | Missing a Required Signal (not excused by Allowed Variants) | FAIL |
| 3 | Correct answer with superficially concerning but Allowed Variant | PASS |
| 4 | Primary answer wrong, alternative correct (primary-answer rule) | FAIL |
| 5 | Doubtful/borderline case not resolved by key | PASS (do not count) |

#### Execution Steps

| Step | Action |
|---|---|
| 3.1 | Create `artifacts/scoring/openwrt-calibration-fixtures.md` |
| 3.2 | Write all 5 fixtures using domain-agnostic patterns (the fixtures should not require OpenWrt knowledge to grade — they test the rule engine, not domain expertise) |
| 3.3 | Include the expected verdict and key reason for each fixture |
| 3.4 | Reference this file from the v4 prompt's Phase 1 (Calibration) |

**Acceptance:** A fresh LLM with zero OpenWrt context can correctly grade all 5 fixtures by following only the key excerpts and the v4 prompt rules.

---

### Phase 4 — Freeze Scorecard Schema

**Source:** Assessment "Files to Edit/Create", row 3; Process Plan step 5.

**File:** `artifacts/scoring/openwrt-scorecard-schema.md`

This document freezes the scorecard output to 5 mandatory columns plus reconciliation math. It replaces the underspecified v2 output schema.

#### Schema Definition

| Column | Type | Description |
|---|---|---|
| `test_taker` | string | Name of the model/agent being scored |
| `scenario` | string | Scenario ID (e.g., `04`) |
| `quoted_evidence` | string | EXACT literal line(s) from the answer that triggered the violation. Paraphrasing is forbidden. |
| `first_definite_wrong_detail` | string | Concise description of what is wrong (20 words or fewer) |
| `key_reason` | string | Short reason tied directly to the key's Automatic Fails or Required Signals |

#### Reconciliation Rules

The scorecard MUST include these summary sections after the failure records:

1. **Per-Test-Taker Summary** — one row per test-taker with `failure_scenarios` list and `failure_count`
2. **Totals** — `total_fail_rows`, `sum_of_failure_count`, `totals_match` (YES/NO)
3. The scorer must verify: `total_fail_rows == sum_of_failure_count` before finalizing

#### Execution Steps

| Step | Action |
|---|---|
| 4.1 | Create `artifacts/scoring/openwrt-scorecard-schema.md` |
| 4.2 | Document the 5 mandatory columns with type and description |
| 4.3 | Document the reconciliation rules and summary sections |
| 4.4 | Include a complete example scorecard (valid) |
| 4.5 | Include an example of a reconciliation error and how the scorer must self-correct |

**Acceptance:** The schema document is self-contained and can be referenced by the v4 prompt without ambiguity.

---

### Phase 5 — Create the V4 Strict Scoring Prompt

**Source:** Assessment Section 3 "The 10/10 Universal Strict Scoring Prompt" (lines 52-131 of `openwrt-scoring-assessment-10-10.md`).

**File:** `artifacts/scoring/openwrt-test-scoring-prompt-v4.md`

This is the ultimate prompt. It supersedes both v2 prompts. Key design principles:

1. **Zero embedded OpenWrt knowledge** — the prompt is a pure rule engine
2. **Strict execution sequence** — calibration, scope, grading, output, reconciliation
3. **Primary Answer Isolation** — first complete code block is the only answer scored
4. **Verbatim Evidence Extraction** — violations must be quoted literally
5. **Key Ingestion Gate** — valid scenario IDs extracted from the key; all others ignored

#### Prompt Structure

```
# OpenWrt Cookbook Universal Strict Batch Scorer

## Identity
You are a deterministic scoring function. You are purposefully stripped of all OpenWrt domain knowledge. You are ONLY a rule engine.

## Inputs
1. A batch answer key file
2. A directory containing result folders per test-taker

## Execution Sequence

### Phase 1: Calibration
Run against openwrt-calibration-fixtures.md. If verdicts deviate from expected, STOP.

### Phase 2: Scope Boundaries
Extract valid scenario IDs from the key. State them. Ignore all others.

### Phase 3: Grading Protocol (Per Scenario)
1. Apply the Primary Answer Rule
2. Seek Definite Wrong Details (Automatic Fails or missing Required Signals)
3. Check for Fabricated APIs

### Phase 4: Recording a Failure
1. Note test-taker & scenario ID
2. Copy EXACT literal line(s) as quoted_evidence
3. State short key_reason
4. STOP reading that scenario

### Phase 5: Output & Reconciliation
Build scorecard per openwrt-scorecard-schema.md. Verify math.
```

#### Execution Steps

| Step | Action |
|---|---|
| 5.1 | Create `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` |
| 5.2 | Write the full prompt incorporating all 5 phases from the assessment (use the exact text from lines 52-131 of `openwrt-scoring-assessment-10-10.md`) |
| 5.3 | Reference the calibration fixtures file |
| 5.4 | Reference the scorecard schema file |
| 5.5 | Include the frozen output schema (Scope, Failure Records, Per-Test-Taker Summary, Totals, Key Improvement Ideas) |
| 5.6 | Include the Ready-To-Use Assignment Template for launching scorer agents (see Section 8) |

**Acceptance:** The prompt is self-contained, references only the key files and calibration fixtures (no hardcoded domain knowledge), and produces output matching the frozen schema.

---

### Phase 6 — Create Failure-Synthesis Prompt

**Source:** Assessment "Files to Edit/Create", row 5.

**File:** `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

This is a separate agent phase that runs AFTER scoring is complete. It reads finalized scorecards and outputs prioritized documentation and Jira tasks based on clustered failure points.

#### Prompt Responsibilities

1. Read all batch scorecards produced by the v4 scorer
2. Cluster failures by scenario and failure pattern
3. For each cluster, determine:
   - How many test-takers failed
   - The dominant wrong approach
   - Whether the cookbook already covers this lesson
   - Recommended action (new page, extend existing page, golden-key update, reject)
4. Output prioritized task list

#### Output Schema

```markdown
# Failure Synthesis Report

## Cluster Summary
| Scenario | Fail Count | Dominant Pattern | Recommended Action | Priority |
|---|---|---|---|---|

## Documentation Backlog
[ ] DOC: <title>
    Gap: <what models got wrong>
    Correct pattern: <what docs should teach>
    Affected scenarios: <list>
    Priority: HIGH / MEDIUM / LOW

## Key Enhancement Backlog
- Scenario <N>: <specific wording improvement for the key>
```

#### Execution Steps

| Step | Action |
|---|---|
| 6.1 | Create `artifacts/scoring/openwrt-failure-synthesis-prompt.md` |
| 6.2 | Define the input contract (reads finalized scorecards from Phase 5 output) |
| 6.3 | Define the clustering rules (group by scenario, then by dominant pattern) |
| 6.4 | Define the output schema (cluster summary, documentation backlog, key enhancement backlog) |
| 6.5 | Include the Ready-To-Use Assignment Template for launching synthesis agents (see Section 8) |

**Acceptance:** The synthesis prompt produces structured, actionable output that maps directly to cookbook authoring decisions.

---

### Phase 7 — Create Scorer Lessons Log

**Source:** User requirement — the scoring AI's own mistakes and hallucinations are valuable data that should be captured in a separate file from the test results.

**File:** `artifacts/scoring/openwrt-scorer-lessons-log.md`

This is a persistent log that captures the scoring agent's own errors during calibration and scoring runs. When the scorer misgrades a scenario (caught during calibration, reconciliation, or human review), that misgrading itself becomes a lesson that improves future scoring runs. This is a unique advantage of using a less-intelligent scorer: we learn about both the test-taker's mistakes AND the scorer's mistakes.

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

#### Execution Steps

| Step | Action |
|---|---|
| 7.1 | Create `artifacts/scoring/openwrt-scorer-lessons-log.md` |
| 7.2 | Seed with the 5 lessons from the table above |
| 7.3 | Add a maintenance note: after each scoring run, the operator reviews any reconciliation failures or human-overturned verdicts and adds entries |
| 7.4 | Reference this log from the v4 prompt's Key Improvement Ideas section as a destination for recurring scorer mistakes |

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
┌──────────────────────┐
│  Gate 1: Calibration │  Scorer runs calibration fixtures. All 5 must match expected verdicts.
│                      │  On failure: abort run, log lesson, fix prompt/key, retry.
└──────────┬───────────┘
           │ PASS
           v
┌──────────────────────┐
│  Gate 2: Key         │  Scorer extracts valid scenario IDs from the key.
│  Ingestion           │  Any result-file scenario not in this list is ignored.
└──────────┬───────────┘
           │ PASS
           v
┌──────────────────────┐
│  Gate 3: Primary     │  For each scenario, isolate FIRST complete code block.
│  Answer Isolation    │  Subsequent alternatives do NOT rescue a wrong primary.
└──────────┬───────────┘
           │ PASS
           v
┌──────────────────────┐
│  Gate 4: Verbatim    │  Every failure row has quoted_evidence copied literally.
│  Evidence Extraction │  No paraphrasing. No summaries. Exact text only.
└──────────┬───────────┘
           │ PASS
           v
┌──────────────────────┐
│  Gate 5: Scorecard   │  Build scorecard per frozen schema.
│  Gen & Reconciliation│  Verify total_fail_rows == sum_of_failure_count.
│                      │  On mismatch: recalculate, do not narrate.
└──────────┬───────────┘
           │ PASS
           v
┌──────────────────────┐
│  Gate 6: Synthesis   │  Run failure-synthesis agent on finalized scorecards.
│  (Separate Agent)    │  Output prioritized docs/Jira backlog.
└──────────────────────┘
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

---

## 8. Ready-To-Use Assignment Templates

These templates are copy-paste surfaces for launching agents. They reference the artifacts created by this plan.

### 8.1 Scorer Agent Launch

```
You are the OpenWrt Cookbook Universal Strict Batch Scorer.

Read these files in order:
1. artifacts/scoring/openwrt-test-scoring-prompt-v4.md — your operating instructions
2. artifacts/scoring/openwrt-calibration-fixtures.md — your calibration test
3. artifacts/tests-keys/<batch>-key.md — the answer key for this batch
4. artifacts/runs/<test-taker>/results/<batch>-result.md — the test-taker's answers

Execute the v4 prompt exactly. If calibration fails, stop and report:
"Calibration Failed. Review required."

If calibration passes, grade all in-scope scenarios and output the scorecard
per the frozen schema in openwrt-scorecard-schema.md.
```

### 8.2 Failure-Synthesis Agent Launch

```
You are the OpenWrt Failure Synthesis Agent.

Read these files:
1. artifacts/scoring/openwrt-failure-synthesis-prompt.md — your operating instructions
2. All finalized scorecard files produced by the v4 scorer

Cluster the failures by scenario and pattern. Output the synthesis report
per the schema defined in your prompt.
```

### 8.3 Human Operator Quick Reference

| Step | What to Do | Files Involved |
|---|---|---|
| 1 | Archive old prompts | Phase 1 |
| 2 | Rewrite all 9 keys to 4-section format | Phase 2, `artifacts/tests-keys/` |
| 3 | Create calibration fixtures | Phase 3, `openwrt-calibration-fixtures.md` |
| 4 | Create scorecard schema | Phase 4, `openwrt-scorecard-schema.md` |
| 5 | Create v4 scoring prompt | Phase 5, `openwrt-test-scoring-prompt-v4.md` |
| 6 | Create failure-synthesis prompt | Phase 6, `openwrt-failure-synthesis-prompt.md` |
| 7 | Create and seed scorer lessons log | Phase 7, `openwrt-scorer-lessons-log.md` |
| 8 | Launch scorer agent using template 8.1 | Copy-paste from Section 8.1 |
| 9 | If calibration fails, fix and retry | Log lesson in scorer lessons log |
| 10 | If scoring passes, launch synthesis agent | Copy-paste from Section 8.2 |
| 11 | Review scorecard and synthesis output | Spot-check 10% of quoted_evidence rows |
| 12 | Record any scorer mistakes | Add entries to scorer lessons log |
