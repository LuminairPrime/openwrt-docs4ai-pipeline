# OpenWrt Cookbook Strict Scoring Prompt v2

Use this prompt when assigning an agent to score one test batch across all test-takers.

## Mission

You are scoring OpenWrt cookbook test results for INCORRECTNESS only.

Your job is not to judge overall quality, plausibility, or completeness. Your job is only to count answers that are definitely wrong under the provided answer key.

If you are unsure whether something is wrong, do not count it as a failure.

## Inputs

You will receive:

- One batch answer key file such as `01a-key.md`
- The root folder containing all test-taker result folders
- The output folder where you must write the batch scorecard

Each test-taker folder contains a `results` folder with files like `01a-result.md`, `01b-result.md`, and so on.

## Non-Negotiable Rules

1. Score one batch key at a time.
2. First extract the exact scenario IDs named by the batch key.
3. Only those scenario IDs are in scope.
4. Ignore every other scenario in the result file, even if it appears nearby.
5. Count only definitely wrong details that violate the key.
6. Do not rescue an answer as a PASS because it looks functional, plausible, or close enough.
7. The answer key boundaries are binding.
8. For each scenario, record at most one failure.
9. The first definite wrong detail is the only failure detail you should record for that scenario.
10. As soon as you find that first definite wrong detail, stop reading that scenario answer for scoring purposes and move on.
11. If a detail is doubtful, borderline, or not explicitly resolved by the key, do not count it as a failure.
12. Do not invent new pass criteria while scoring.
13. You may record ideas for future key improvements, but keep them separate from the scoring decision.
14. Your summary totals must be derived from the detailed failure rows, not from manual narration.
15. Before finalizing, reconcile all totals against the detailed rows.

## Strict Scoring Procedure

Follow this exact order:

1. Read the batch key.
2. Extract the allowed scenario IDs from the key.
3. Read the matching result file for one test-taker.
4. Locate only the answers for the allowed scenario IDs.
5. Ignore out-of-scope scenarios in that result file.
6. For each allowed scenario, compare the answer only against:
   - the explicit PASS criteria
   - the explicit Immediate fails
7. Ask one question only: `Is there a definite wrong detail here under this key?`
8. If no, record PASS.
9. If yes, record FAIL with:
   - test-taker name
   - scenario ID
   - first definite wrong detail
   - short reason tied directly to the key
10. Stop reading that scenario after the first definite wrong detail.
11. Repeat for each in-scope scenario.
12. Repeat for each test-taker.
13. Build the summary from the fail rows only.
14. Run the self-check before writing the final scorecard.

## Decision Standard

Use this decision standard for each scenario:

- PASS only if there is no definite wrong detail under the key.
- FAIL only if you can point to one concrete detail that definitely violates the key.
- UNCERTAIN details do not count as failures.

Important:

- Missing polish is not a fail.
- Stylistic differences are not a fail.
- Different but acceptable implementation variants are not a fail unless the key explicitly excludes them.
- Apparent functionality is not enough to pass if the key defines a strict architecture or boundary and the answer violates it.

## Failure Logging Format

When a scenario fails, log only the first blocking issue in this form:

- `Scenario 04 FAIL: uses legacy Lua CBI controller/model pattern; key requires modern LuCI JS form.Map architecture.`

Good failure reasons are:

- concrete
- short
- tied to the key wording
- limited to the first definite wrong detail

Bad failure reasons are:

- broad judgments about the whole answer
- multiple stacked complaints for one scenario
- speculation
- invented requirements not present in the key

## Required Output Schema

Your final scorecard must use this structure.

```md
# Batch Scorecard

## Scope
- batch_key: 01a
- allowed_scenarios: [01, 03, 04]
- test_takers_scored: 8

## Failure Records
| test_taker | scenario | first_definite_wrong_detail | key_reason |
|---|---|---|---|
| big-pickle | 04 | uses Lua CBI controller/model pattern | scenario 04 requires modern LuCI JS form.Map architecture |

## Per-Test-Taker Summary
| test_taker | failure_scenarios | failure_count |
|---|---|---:|
| big-pickle | [04, 02, 05, 10, 18, 16] | 6 |

## Totals
- total_fail_rows: 6
- sum_of_failure_count: 6
- totals_match: yes

## Key Improvement Ideas
- Scenario 04 could explicitly say that Lua CBI and template-driven HTML are automatic fails even if functionally plausible.
```

## Self-Check

Before you finalize, verify all of the following:

1. Every scored scenario is listed in the batch key.
2. No out-of-scope scenario affected the score.
3. Every failed scenario has exactly one recorded failure reason.
4. Every failure reason points to a definite wrong detail.
5. `total_fail_rows` equals the count of all failure records.
6. `sum_of_failure_count` equals the sum of the per-test-taker counts.
7. `total_fail_rows` equals `sum_of_failure_count`.

If any check fails, fix the scorecard before returning it.

## Optional Enhancement Capture

If you notice recurring failure patterns that suggest documentation gaps, record them in `Key Improvement Ideas` using this format:

- scenario ID
- recurring mistake pattern
- one concrete wording improvement for the key
- one candidate cookbook documentation topic that could prevent that failure in the future

Keep these ideas separate from scoring. They must not change the current batch result.

## Ready-To-Use Assignment Template

Use this assignment wrapper when launching a batch scorer agent:

```md
Score the OpenWrt cookbook results for batch `01a-key.md` across all test-takers.

Rules:
- Score INCORRECTNESS only.
- Extract the in-scope scenarios from `01a-key.md` first and score only those scenarios.
- Ignore extra scenarios found in the result files.
- Count only definitely wrong details.
- Record only the first definite wrong detail per failed scenario.
- Stop reading a scenario once that first definite wrong detail is found.
- Do not rescue answers as PASS because they seem functionally close.
- Derive your totals from your failure records and reconcile the math before final output.

Output:
- Write one batch scorecard using the required schema.
- Include a short `Key Improvement Ideas` section at the end.
```