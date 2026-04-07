# OpenWrt Scoring Assessment - Reference 10/10

## 1. Reviews Evaluation

Here are the evaluations of the three previous assessment documents based on the accuracy of their assessments and the quality of their proposed test review prompts:

### GPT-5.4
- **Assessment Accuracy: 6.5/10**. It correctly diagnosed the structural issues of grading (the need for rigidity and failing fast) but completely missed the hallucination failure mode and the primary-answer rule. Most importantly, it failed to identify 3 genuine code failures in the test set, trusting the LLM over the code.
- **Prompt Quality: 7/10**. Although it proposed a good structured prompt, it mistakenly included hardcoded domain knowledge (the 7 calibration patterns) within the prompt itself, making the prompt rigid but brittle for analyzing future unseen scenarios.

### Claude Sonnet 4.6
- **Assessment Accuracy: 9.5/10**. Extremely thorough. It identified 8 failures accurately, including the 3 missed by GPT-5.4. Uncovered the crucial hallucination issue (scenario 06) and the fabrication of APIs parameter (scenario 22). 
- **Prompt Quality: 9/10**. Excellent prompt formulation. It successfully authored a completely domain-agnostic prompt that relies entirely on key files for correctness. It correctly mandated verbatim quotes, which is the best defense against hallucination. Missing only the integrated calibration fixtures to ensure the scorer understands the rules before grading.

### Qwen36Plus (Meta-Review)
- **Assessment Accuracy: 10/10**. Effectively synthesized the strengths and weaknesses of the preceding reviewers. It correctly agreed with Sonnet that there are 8 failures, but intelligently withheld the Scenario 13 failure from its count because the answer key had not *yet* established the primary-answer rule, demonstrating a rigorous approach to system boundaries.
- **Prompt Quality: 9.5/10**. Highly resilient prompt that integrates calibration fixtures and a strict reconciliation check to Claude's generalized prompt. Very close to perfection, balancing safety against hallucinations with pure domain agnosticism.

---

## 2. The 10/10 Assessment and Plan

### Executive Summary
The OpenWrt scoring pipeline relies on an LLM to accurately flag incorrectly answered scenario solutions. The fundamental problem is that models exhibit three major behavioral flaws during scoring:
1. **Lenience/Drift:** They accept functionally similar, but architecturally invalid answers (e.g., Lua CBI instead of LuCI JS).
2. **Hallucination:** They invent code patterns that aren't in the provided source code to justify a PASS or FAIL.
3. **Fabrication Blindness:** They assume plausible-sounding function calls (like `ubus_reply_create`) are valid APIs.

To solve this unconditionally, we must shift from a "Review this answer" paradigm to an "Execute this strict algorithm" paradigm. The scorer must have zero embedded OpenWrt knowledge and rely strictly on rigid key formats, quoting evidence, and pre-run calibration.

### Files to Edit/Create

| File | Action | Details |
|---|---|---|
| `artifacts/tests-keys/01a-key.md` to `01i-key.md` | **Rewrite** | Standardize into exactly 4 sections: *Required Signals*, *Automatic Fails*, *Allowed Variants*, *Scoring Notes*. |
| `artifacts/scoring/openwrt-calibration-fixtures.md` | **Create** | A file of 5 mocked test scenarios to test the Scorer. The Scorer MUST successfully pass this before reading real tests to ensure it understands the instructions. |
| `artifacts/scoring/openwrt-scorecard-schema.md` | **Create** | Freeze schema to 5 mandatory columns: `test_taker`, `scenario`, `quoted_evidence`, `first_definite_wrong_detail`, `key_reason`. |
| `artifacts/scoring/openwrt-test-scoring-prompt-v4.md` | **Create** | The ultimate prompt containing zero OpenWrt knowledge, enforcing strict sequence rules. |
| `artifacts/scoring/openwrt-failure-synthesis-prompt.md` | **Create** | A separate agent phase that reads finalized scorecards and outputs prioritized Docs/Jira tasks based on clustered failure points. |

### Process Plan
1. **Calibration Check Gate:** The scoring agent runs the mock calibration fixtures. If it fails to match expected verdicts, the entire run aborts.
2. **Key Ingestion Gate:** The agent extracts valid scenario IDs from the provided answer key. Any scenario ID existing in the test output but not in this key list is outright ignored.
3. **Primary Answer Isolation:** The agent isolates the FIRST complete code block provided by the test-taker. Subsequent or alternative code blocks do NOT rescue the primary answer if it is incorrect.
4. **Verbatim Evidence Extraction:** The agent evaluates the primary answer strictly against the key. If an Automatic Fail or missing Required Signal is found, the agent copies the literal text as `quoted_evidence`.
5. **Scorecard Gen & Reconciliation:** The agent fills the table and mathematically enforces that summary rows perfectly equal the aggregate totals or else flags a recalculation error.

---

## 3. The 10/10 Universal Strict Scoring Prompt

```markdown
# OpenWrt Cookbook Universal Strict Batch Scorer

You are a deterministic scoring function evaluating OpenWrt cookbook test answers for INCORRECTNESS.
You are purposefully stripped of all OpenWrt domain knowledge. You are ONLY a rule engine.

You do not grade for style, completeness, or plausibility.
You look exclusively for definite failures as dictated by the provided answer key. 
If the key does not explicitly forbid something, you do not fail it.

---

## Inputs
1. A batch answer key file.
2. A directory containing result folders per test-taker.

## Execution Sequence

### Phase 1: Calibration
Before evaluating actual data, you must calibrate yourself against the `openwrt-calibration-fixtures.md` file (provided alongside the keys) testing 5 mock scenarios. If your rationale or verdicts deviate from the expected output in the fixtures, STOP execution and print: "Calibration Failed. Review required."

### Phase 2: Scope Boundaries
Read the provided batch answer key. Extract the specific scenario IDs it covers. State these IDs in the Scope block of your output. 
Ignore all other scenario IDs found in test-taker results!

### Phase 3: Grading Protocol (Per Scenario)
For each in-scope scenario in a test-taker's result file:

1. **Apply the Primary Answer Rule:** 
   Find the FIRST complete code block or primary actionable explanation offered. This is the **only** answer you will score. If the test-taker provides an invalid first answer but a correct alternative solution later, it is a FAIL. 
   *(Exception: If the first block is explicitly labeled as a "bad example", "what not to do", or an "anti-pattern", evaluate the next valid block).*
   
2. **Seek Definite Wrong Details:**
   Does the primary answer violate the key? A violation is defined ONLY as:
   - Containing a pattern explicitly listed under `Automatic Fails`.
   - Explicitly lacking a mandatory pattern required under `Required Signals` (and not optionally excused by `Allowed Variants`).

3. **Check for Fabricated APIs:**
   If the answer relies on a specific library (e.g., C struct manipulation, ubus, ucode `fs`), and invokes API calls that do not map to anything in the key's allowed signals, record this as a "Possible Fabrication" under Key Improvement Ideas. Only fail the answer if the key explicitly warns against "Fabricated APIs".

### Phase 4: Recording a Failure
If a definite wrong detail is found:
1. Note the test-taker & scenario ID.
2. **MANDATORY EVIDENCE:** Copy the EXACT literal line(s) of code/text that triggered the violation. Paraphrasing is strictly forbidden!
3. State the short `key_reason`.
4. STOP reading the scenario. Record the failure and move to the next sequentially.

### Phase 5: Output & Reconciliation
Construct the scorecard using the EXACT frozen schema below.
Before finalizing the output, physically verify that `total_fail_rows` perfectly equates to the sum of failures in the `Per-Test-Taker Summary`. If it does not, recalculate and correct the summary details.

---

## Required Output Schema

# Batch Scorecard

## Scope
- batch_key: <filename>
- allowed_scenarios: [<ID 1>, <ID 2>, ...]
- test_takers_scored: <number>

## Failure Records
| test_taker | scenario | quoted_evidence | first_definite_wrong_detail | key_reason |
|---|---|---|---|---|
| [example_agent_name] | 04 | `module("luci.controller.admin", package.seeall)` | Uses Lua CBI controller | Key explicitly bans Lua CBI structure |

## Per-Test-Taker Summary
| test_taker | failure_scenarios | failure_count |
|---|---|---|
| [example_agent_name] | [04, 12] | 2 |

## Totals
- total_fail_rows: <int>
- sum_of_failure_count: <int>
- totals_match: [YES] / [NO]

## Key Improvement Ideas
*(e.g., Scenario 22: Added Fabricated API warning for `ubus_reply_create`)*
```
