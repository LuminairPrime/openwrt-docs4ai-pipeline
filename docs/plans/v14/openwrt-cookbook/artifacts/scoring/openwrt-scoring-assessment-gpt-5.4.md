# OpenWrt Scoring Assessment - GPT-5.4

## Purpose

This assessment is based on:

- the original Haiku scoring prompt draft
- the resulting Haiku scorecard
- one full strict rescoring pass of `big-pickle`

The goal is to make the scoring process reliable enough that a weaker model can still produce a correct, synthesis-ready scorecard.

## Executive Assessment

The current scoring direction is good, but the first draft prompt is still too permissive for a weaker model.

The main failure modes are:

1. The scorer can accidentally grade scenarios that are present in a result file but not in scope for the matching batch key.
2. The scorer can soften strict answer-key boundaries into `close enough`, `functional`, or `plausible` passes.
3. The scorer can mix detailed reasoning with summary math and produce internal tally errors.
4. The scorer is not forced to stop at the first definite wrong detail, so weaker models may over-read, drift, or invent extra reasons.
5. The answer keys are still somewhat human-readable but not yet machine-rigid enough for a weaker model.

In short: the scoring task is workable, but the prompt and keys both need stronger rails.

## Grounding Pass: Big-Pickle

I performed a strict incorrectness-only rescoring pass for `big-pickle`.

Result:

- Total scored scenarios: 27
- Definite failures: 6
- Passed scenarios: 21

This matched Haiku's detailed per-scenario breakdown, but did not match Haiku's top summary table, which listed a smaller failure count.

That discrepancy matters because it proves the scorer prompt must require summary reconciliation against detailed fail rows.

## What A Weaker Scorer Needs

A weaker model should not be asked to "use judgment" broadly. It should be forced into a constrained procedure.

The scoring system should therefore do all of the following:

1. Scope first.
   The scorer must extract the exact scenario IDs from the batch key before reading results.

2. Compare only against explicit key boundaries.
   The scorer should use only the scenario's PASS criteria and Immediate fails.

3. Fail on the first definite wrong detail.
   The scorer should record one failure reason and stop reading that scenario.

4. Ignore uncertainty.
   If the model is not sure, it should not count a failure.

5. Derive all summary counts from a fail-only detail table.
   This prevents arithmetic drift.

## Files I Would Change

These are the files I would change next, and why.

### 1. [artifacts/scoring/openwrt-test-scoring-prompt-v2.md](c:/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/artifacts/scoring/openwrt-test-scoring-prompt-v2.md)

Status:

- Already created in this session.

Why:

- This becomes the base scorer prompt for one batch key at a time.

Fix plan:

- Keep it as the authoritative batch-scoring prompt.
- Use it for one-agent-per-key runs.
- Do not let individual batch scorers improvise their own output structure.

### 2. `artifacts/tests-keys/01a-key.md` through `artifacts/tests-keys/01i-key.md`

Why:

- The keys are decent for a strong human reviewer, but still too soft for a weaker model.

Fix plan:

- Rewrite each scenario into four explicit sections:
  - `Required signals`
  - `Automatic fails`
  - `Allowed variants`
  - `Scoring notes`
- Convert ambiguous language like `must use modern LuCI JS architecture` into concrete markers such as:
  - `must use L.view.extend()`
  - `must use form.Map`
  - `must not use Lua CBI`
  - `must not use raw HTML templates`
- For runtime-boundary scenarios, explicitly disallow hybrids such as shell wrappers around ubus or JSON helpers when the target is native ucode.
- For lifecycle scenarios, explicitly state order constraints such as `load() gathers data; render() consumes it`.

### 3. `artifacts/templates/00-batch-prompt-header-template.md`

Why:

- This is the right place to standardize the wrapper text used when launching a scorer agent.

Fix plan:

- Add a standard header that repeats the critical constraints:
  - score one batch only
  - extract in-scope scenario IDs first
  - ignore out-of-scope scenarios
  - record one failure per scenario maximum
  - derive totals from fail rows only
  - run a final reconciliation check

### 4. New recommended file: `artifacts/scoring/openwrt-scorecard-schema.md`

Why:

- We should freeze one canonical scorecard output shape.

Fix plan:

- Add a schema document with one required layout:
  - scope block
  - failure-record table
  - per-test-taker summary table
  - totals block
  - key improvement ideas
- Require all scorer agents to emit this exact structure.

### 5. New recommended file: `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

Why:

- Your end goal is not just scoring. It is turning repeated failures into new documentation.

Fix plan:

- Add a second-stage prompt that consumes the canonical scorecard and produces:
  - recurring failure clusters
  - likely missing cookbook concepts
  - candidate new doc pages
  - candidate revisions to answer keys

## Fully Fleshed Out Fix Plans

### Fix Plan A: Strengthen The Keys For Machine Scoring

Current problem:

- The keys rely on human interpretation.
- A weaker model will often pass answers that are architecturally wrong but superficially plausible.

Planned change:

- Rewrite each scenario using this rigid pattern:

```md
## Scenario 04 - LuCI JS Dynamic Form

### Required Signals
- Must use `L.view.extend()` or equivalent LuCI JS view wrapper.
- Must instantiate `form.Map`.
- Must build options with LuCI JS form widgets.
- Must use a dynamic interface source from LuCI/OpenWrt APIs.

### Automatic Fails
- Any Lua CBI model/controller solution.
- Any raw HTML template as the main implementation.
- Any non-LuCI frontend framework.

### Allowed Variants
- Different LuCI JS import style is acceptable.
- Different widget names are acceptable if still within LuCI JS form architecture.

### Scoring Notes
- If the answer uses Lua CBI or template HTML, fail immediately and stop reading.
- Do not rescue the answer because it looks functionally similar.
```

Expected effect:

- Much lower scorer drift.
- Less hallucinated leniency.
- Easier parallel scoring.

### Fix Plan B: Freeze One Canonical Scorecard Shape

Current problem:

- Haiku's report was rich, but its summary math drifted from its detailed breakdown.

Planned change:

- Make the failure-record table the source of truth.
- Require the summary to be computed from that table only.

Required schema:

```md
## Scope
- batch_key: 01a
- allowed_scenarios: [01, 03, 04]
- test_takers_scored: 8

## Failure Records
| test_taker | scenario | first_definite_wrong_detail | key_reason |
|---|---|---|---|

## Per-Test-Taker Summary
| test_taker | failure_scenarios | failure_count |
|---|---|---:|

## Totals
- total_fail_rows: 0
- sum_of_failure_count: 0
- totals_match: yes
```

Expected effect:

- Summary and detail cannot silently diverge.
- Scorecards become machine-checkable.

### Fix Plan C: Add A Dedicated Synthesis Stage

Current problem:

- The scorer is being asked to both grade and think strategically about future documentation.
- That is useful, but it weakens scoring discipline.

Planned change:

- Keep scoring and synthesis as separate phases.

Phase 1:

- strict scoring only

Phase 2:

- doc-gap synthesis from completed scorecards

Expected effect:

- Cleaner grader behavior
- Better downstream cookbook planning

### Fix Plan D: Add A Preflight Rule For Out-Of-Scope Scenario Noise

Current problem:

- The result files contain scenarios not covered by the matching batch key.

Planned change:

- Every scorer must declare `allowed_scenarios` at the top of the report before scoring begins.
- Every failure row must use one of those declared scenario IDs.

Expected effect:

- Prevents batch contamination.
- Makes bad scoring auditable.

## Whole New Scoring Prompt For A Dumber AI

The prompt below is intentionally rigid. It assumes the model needs explicit control flow and should not improvise.

---

# OpenWrt Cookbook Batch Scorer

You are scoring OpenWrt cookbook test answers.

Your task is to find answers that are definitely wrong.

Do not grade overall quality.
Do not grade completeness unless the answer key makes incompleteness a definite fail.
Do not guess.

If you are unsure whether something is wrong, do not count it as a failure.

## Inputs

You will receive:

- one batch answer key file
- one folder containing all test-taker result folders
- one output location

## Your Job

Score one batch key across all test-takers.

## Rules You Must Follow

1. Read the batch answer key first.
2. Extract the exact scenario IDs named in that batch key.
3. Only those scenario IDs are allowed to affect scoring.
4. Ignore every other scenario in the result file.
5. For each allowed scenario, compare the answer only against:
   - the explicit PASS criteria
   - the explicit Immediate fails
6. Count only definitely wrong details.
7. If an answer seems questionable but not definitely wrong, do not count it as a failure.
8. For each scenario, record at most one failure.
9. The first definite wrong detail is the only failure detail you may record.
10. As soon as you find that first definite wrong detail, stop reading that scenario and continue to the next scenario.
11. Do not rescue an answer as a pass because it seems functionally similar.
12. Do not invent new pass or fail criteria.
13. Your summary totals must be computed from your detailed failure rows.
14. Before finalizing, check that your totals match exactly.

## Required Procedure

Follow these steps in order.

### Step 1: Scope

Read the batch key and write down the allowed scenario IDs.

### Step 2: Read One Test-Taker

Open that test-taker's matching result file for the batch.

### Step 3: Ignore Noise

If the result file contains extra scenarios not listed in the batch key, ignore them completely.

### Step 4: Score Each In-Scope Scenario

For each allowed scenario:

- look for a definite wrong detail
- if none is found, mark PASS
- if one is found, mark FAIL and record only:
  - test-taker name
  - scenario ID
  - first definite wrong detail
  - short reason tied directly to the key

Then stop reading that scenario.

### Step 5: Build Summary From Fail Rows Only

After all test-takers are scored:

- create a fail-only detail table
- create one per-test-taker summary table from that fail table
- create totals from that summary table

### Step 6: Reconcile Math

Before finalizing, verify:

- every failure row uses an allowed scenario ID
- each failed scenario appears once at most
- total fail rows equals the sum of per-test-taker failure counts

If the numbers do not match, fix them before you return the report.

## Required Output Format

Use exactly this structure.

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
- Scenario 04: explicitly say Lua CBI and raw HTML templates are automatic fails even when functionally plausible.
```

## Failure Reason Style Guide

Good failure reason:

- `uses shell wrapper around ubus with jsonfilter; key requires native ucode ubus access`

Bad failure reason:

- `this solution is weak and probably not what OpenWrt wants`

Good failure reasons are:

- short
- concrete
- based on the key
- limited to the first definite wrong detail

## Important Reminder

You are not trying to prove an answer correct.
You are only trying to catch definite incorrectness.

Unknown is not a fail.
Plausible is not automatically a pass.
Only the key decides.

---

## Additional Key Improvements I Recommend

These are the scenario families most worth tightening first.

### High Priority

1. LuCI JS architecture scenarios
   Files affected: `01a-key.md`, `01c-key.md`, `01f-key.md`

   Plan:

   - explicitly distinguish LuCI JS from Lua CBI and template HTML
   - list exact fail markers such as `entry(..., cbi(...))`, raw `<table>`, template tags, or missing `form.Map`

2. Native ucode boundary scenarios
   Files affected: `01b-key.md`, `01d-key.md`, `01e-key.md`, `01g-key.md`

   Plan:

   - explicitly prohibit shell-first wrappers like `ubus call | jsonfilter`, `jshn`, `jq`, FIFOs, and background jobs when native ucode is the target
   - define whether hybrid shell/ucode variants are accepted or not

3. Lifecycle-order scenarios
   Files affected: `01c-key.md`, `01f-key.md`

   Plan:

   - spell out sequence requirements directly in the key
   - example: `rpc.declare()` at module scope, `load()` for async retrieval, `render()` for presentation only

### Medium Priority

1. Add `Allowed variants` sections to every scenario.
2. Add one canonical fail example per scenario.
3. Add one canonical pass skeleton per high-drift scenario family.

## Suggested New Scoring Subproject Files

These would improve the workflow beyond the prompt itself.

1. `artifacts/scoring/openwrt-scorecard-schema.md`
   Purpose: freeze the report format.

2. `artifacts/scoring/openwrt-scorecard-reconciliation-checklist.md`
   Purpose: give the scorer a final arithmetic and scope checklist.

3. `artifacts/scoring/openwrt-failure-synthesis-prompt.md`
   Purpose: convert recurring failures into documentation work items.

4. `artifacts/scoring/openwrt-key-rewrite-guide.md`
   Purpose: standardize how answer keys are rewritten for weaker-model scoring.

## Bottom Line

The first draft prompt was directionally correct, but it still relied too much on the model behaving like a careful human reviewer.

For a weaker model, the process must be constrained by:

- strict scenario scoping
- fail-on-first-definite-wrong logic
- no functional-variant leniency
- fail-row-derived summaries
- a frozen output schema

If you apply those changes, the scorecards should become reliable enough to support the next step: synthesizing missing cookbook documentation directly from recurring failure clusters.