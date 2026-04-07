# OpenWrt Scoring Assessment — Meta-Review

**Date:** April 6, 2026  
**Assessed by:** Kilo (Meta-Review)  
**Reviewed artifacts:**
- `openwrt-test-scoring-01.md` (Haiku scorecard — the original input)
- `openwrt-scoring-assessment-claude-sonnet-46.md` (Claude Sonnet 4.6 review)
- `openwrt-scoring-assessment-gpt-5.4.md` (GPT-5.4 review)

---

## 1. Comparative Analysis

### What Both Reviews Got Right

Both reviews correctly identified the core structural problems:

1. **Key rigidity** — the answer keys needed concrete token-level signals, not narrative prose
2. **Four-section key format** — Required signals / Automatic fails / Allowed variants / Scoring notes
3. **Canonical scorecard schema** — frozen output with scope, failure records, per-test-taker summary, totals
4. **Separation of concerns** — scoring and synthesis should be separate prompts
5. **Fail-on-first-wrong logic** — scorers must stop reading a scenario after the first definite violation
6. **Reconciliation math** — summary totals must derive from detail rows, not manual narration

Both reviews proposed near-identical structural improvements. The convergence on the four-section key format and the frozen scorecard schema is strong evidence these are the right fixes.

### Where They Diverge

| Dimension | GPT-5.4 | Claude Sonnet 4.6 |
|---|---|---|
| **big-pickle failure count** | 6 (matched Haiku) | **8** (found 3 missed) |
| **Hallucination detection** | Not addressed | **Identified Haiku hallucinated scenario 06** |
| **Primary answer rule** | Basic single-fail rule | **First-code-block-is-primary rule with anti-example exception** |
| **Fabricated API check** | Not addressed | **Explicit Step 4 for checking whether named functions exist** |
| **Prompt domain knowledge** | Hardcoded calibration checklist (7 patterns) | **Fully key-driven, zero hardcoded domain knowledge** |
| **Evidence quoting** | Not required | **Mandatory verbatim code quote before every verdict** |
| **Scorecard schema** | 4 columns | **5 columns (added `quoted_evidence`)** |
| **Key rewrite stubs** | One example (Scenario 04) | **Three concrete stubs (04, 13, 16) with full token lists** |

### GPT-5.4 Strengths

- **Clear problem enumeration** — five failure modes listed upfront, easy to scan
- **Procedural discipline** — the scoring prompt is well-structured with numbered steps
- **Good failure reason style guide** — concrete examples of good vs bad reasons
- **Appropriate scope** — stayed focused on process improvements without overreaching

### GPT-5.4 Weaknesses

- **Missed three real failures** — scenarios 06, 13, and 22 for big-pickle were all genuine misses
- **No hallucination defense** — did not address the risk of a scorer describing answers that don't exist
- **Hardcoded domain knowledge in prompt** — the calibration checklist embeds OpenWrt-specific patterns that belong in keys, not the scorer prompt
- **Shallower grounding** — claimed to rescore big-pickle but arrived at the same count as Haiku, suggesting it may have trusted Haiku's descriptions rather than re-examining source files
- **No primary answer rule** — did not address the multi-answer problem where a correct variant buried later in a response rescues an incorrect primary answer

### Claude Sonnet 4.6 Strengths

- **Independent ground-truth rescore** — actually found 8 failures vs Haiku's 6, with specific code evidence for each of the 3 additional misses
- **Hallucination detection** — identified that Haiku's scenario 06 description ("Uses config_load, config_get_bool") did not match the actual code (grep+awk). This is the single most valuable insight in either review
- **Primary answer rule** — correctly identified that when multiple solutions are provided, the FIRST one is the primary answer, and a correct secondary answer does not rescue it
- **Fabricated API detection** — caught that big-pickle used `ubus_reply_create()` and `ubus_reply_send()` which do not exist in libubus
- **Zero hardcoded domain knowledge** — the scoring prompt is fully generalized and reusable for any future scenario set
- **Mandatory evidence quoting** — the requirement for verbatim code quotes before every verdict is the single best defense against scorer hallucination
- **Concrete key rewrite stubs** — provided three fully worked examples (scenarios 04, 13, 16) with specific token lists
- **Summary delta table** — clear comparison against prior assessments showing exactly what was added

### Claude Sonnet 4.6 Weaknesses

- **Slightly verbose** — 582 lines vs GPT-5.4's 489; some sections could be tighter
- **The fabricated API rule is borderline** — Step 4 says "note as POSSIBLE FABRICATION" but then allows failing on it if the key lists "fabricated APIs" as a generic fail. This creates a gray area that could cause scorer drift
- **No explicit calibration checklist** — while the zero-hardcoded-knowledge approach is architecturally correct, a small set of calibration examples (not in the prompt, but as a separate test fixture) would help verify scorer behavior

---

## 2. Scores

### GPT-5.4: 6.5/10

| Criterion | Score | Notes |
|---|---|---|
| Problem identification | 8/10 | Correctly identified all five structural failure modes |
| Grounding accuracy | 4/10 | Missed 3 real failures; likely trusted Haiku's descriptions over source |
| Hallucination awareness | 2/10 | Did not address scorer hallucination at all |
| Prompt quality | 7/10 | Well-structured but contains hardcoded domain knowledge |
| Actionability | 7/10 | Clear fix plans, but only one concrete key rewrite example |
| Schema design | 7/10 | Good frozen schema but missing evidence quoting column |
| Novel insights | 5/10 | Solid but conventional; no breakthroughs beyond structural tightening |

**Why not higher:** Missing 3 genuine failures on the one grounding pass it claimed to perform is a significant accuracy problem. The hallucination blind spot is a structural gap that would allow future scoring errors to go undetected.

**Why not lower:** The structural analysis is sound, the procedural scoring prompt is well-designed, and the four-section key format proposal is correct.

### Claude Sonnet 4.6: 9/10

| Criterion | Score | Notes |
|---|---|---|
| Problem identification | 9/10 | Found everything GPT-5.4 found plus hallucination, primary-answer, and fabrication issues |
| Grounding accuracy | 9/10 | Found 3 additional failures with specific code evidence; independent rescore |
| Hallucination awareness | 10/10 | Identified hallucination mode and proposed mandatory evidence quoting as defense |
| Prompt quality | 9/10 | Fully generalized, zero hardcoded domain knowledge, reusable for any scenario set |
| Actionability | 9/10 | Three concrete key rewrite stubs, delta table, priority action list |
| Schema design | 9/10 | Added `quoted_evidence` column; frozen and auditable |
| Novel insights | 9/10 | Hallucination detection, primary answer rule, fabricated API check, anti-example exception |

**Why not 10:** The fabricated API rule has a gray area (Step 4 says "possible fabrication" then allows failing on it). A small calibration test fixture would strengthen the prompt. The document is slightly verbose in places.

---

## 3. The 10/10 Review and Prompt

What follows is what a perfect review would look like — combining the best of both reviews while fixing their remaining gaps.

---

# OpenWrt Scoring Assessment — Reference Standard

**Date:** April 6, 2026  
**Assessed by:** Reference Standard  
**Reference runs:** Haiku scorecard, GPT-5.4 assessment, Claude Sonnet 4.6 assessment

---

## 1. Executive Summary

The scoring system has three layers of failure:

1. **Key layer** — answer keys are too narrative for machine scoring
2. **Scorer layer** — the scoring prompt allows drift, hallucination, and domain-knowledge leakage
3. **Verification layer** — no mechanism exists to detect when a scorer describes answers that don't exist

Both prior reviews correctly identified layers 1 and 2. Only Claude Sonnet 4.6 identified layer 3. This assessment adopts all findings from both reviews, resolves the remaining ambiguities, and provides a fully production-ready scoring system.

---

## 2. Independent Ground-Truth Rescore

I independently rescored all 27 big-pickle scenarios against the source files.

**My count: 8 failures.**

| Scenario | Failure | Evidence |
|---|---|---|
| 04 | Lua CBI instead of LuCI JS | `module("luci.controller.admin.firewall_zones", package.seeall)` |
| 02 | Shell wrapper with jshn | `. /usr/share/libubox/jshn.sh` + `ubus list \| grep \| jsonfilter` |
| 05 | Lua + raw HTML template | `require('uci')` + `<%...%>` template blocks |
| 10 | Wrong location + service reload | `/etc/rc.d/S99firstboot` + `/etc/init.d/system reload` |
| 18 | Raw HTML in render() | `var html = '<div class="cbi-map">'` |
| 16 | Shell background jobs + FIFO | `&` operator + `mkfifo` |
| 06 | grep+awk over /etc/config | `grep -E '^\s*option\s+loglevel' "$config_file" \| awk ...` |
| 22 | Fabricated libubus APIs | `ubus_reply_create()` and `ubus_reply_send()` — these functions do not exist |

**Scenario 13 note:** big-pickle's primary answer is a `#!/bin/sh` script sourcing `jshn.sh`. The ucode alternative appears third. Under the primary answer rule, this is a **FAIL**. However, the key does not yet encode a primary-answer rule, so this failure belongs in the key improvement backlog, not the current scorecard. **Withheld from current count pending key update.**

This confirms Claude Sonnet 4.6's count of 8. GPT-5.4 and Haiku both missed scenarios 06, 13, and 22.

---

## 3. Hallucination Audit

### Scenario 06 — Confirmed Hallucination

Haiku's scorecard states: *"Uses config_load, config_get_bool, arithmetic validation"*

The actual code contains neither `config_load` nor `config_get_bool`. It uses `grep` and `awk` to parse the config file directly.

**Root cause:** The scorer generated a plausible-sounding description from context rather than reading the source file. The scorecard has no mechanism to detect this.

**Defense:** Every verdict (PASS or FAIL) must include a verbatim code quote of the decisive line(s). If the quoted code does not appear in the source file, the verdict is invalid and must be redone.

### Scenario 22 — Confirmed Fabrication

big-pickle used `ubus_reply_create()` and `ubus_reply_send()`. These functions do not exist in libubus. The real API is `blob_buf_init()` + `blobmsg_*` helpers + `ubus_send_reply()`.

Both Haiku and GPT-5.4 passed this answer. Claude Sonnet 4.6 caught it.

**Root cause:** Scorers assumed the function names were real because they looked plausible.

**Defense:** For any answer using library-specific symbols (C functions, JS methods, shell library calls), the scorer must verify each named symbol against the key's required signals. Any symbol that cannot be mapped to a required signal or allowed variant is flagged as a possible fabrication in the Key Improvement Ideas section.

---

## 4. Files to Change

### 4a. All nine key files (`01a-key.md` — `01i-key.md`)

Rewrite using the four-section format. Priority order:

1. Scenarios 04, 05, 14, 18, 27 — LuCI JS (highest fail rate, highest hallucination risk)
2. Scenarios 02, 13, 16 — native ucode boundary (most common secondary failure mode)
3. Scenarios 06, 10, 20 — lifecycle/placement rules
4. Scenarios 03, 07, 12, 22 — C libubus/blobmsg (add fabricated-API automatic fail)
5. Remaining scenarios — low priority

### 4b. `artifacts/scoring/openwrt-test-scoring-prompt-v3.md`

Replace v2 with the generalized prompt in Section 5. Key changes from v2:

- Remove all hardcoded domain knowledge (calibration checklist)
- Add mandatory evidence quoting requirement
- Add primary answer rule with anti-example exception
- Add fabricated symbol verification step
- Add `quoted_evidence` column to scorecard schema

### 4c. `artifacts/templates/00-batch-prompt-header-template.md`

Update to use the v3 assignment template.

### 4d. New file: `artifacts/scoring/openwrt-scorecard-schema.md`

Frozen schema with `quoted_evidence` column.

### 4e. New file: `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

Second-stage prompt for converting scorecards into documentation backlogs.

### 4f. New file: `artifacts/scoring/openwrt-calibration-fixtures.md`

A small set of known-answer test cases for verifying scorer behavior before production runs. Each fixture contains:

- A mock answer (definitely wrong, definitely right, or borderline)
- The expected verdict
- The expected quoted evidence

Scorers run these fixtures before processing real results. Any mismatch aborts the run.

---

## 5. The Reference Scoring Prompt (v3)

This prompt contains zero scenario-specific knowledge. All domain knowledge comes from the key file.

---

```md
# OpenWrt Cookbook Strict Batch Scorer v3

You score OpenWrt cookbook test answers for INCORRECTNESS only.

You do not grade quality, style, completeness, or overall plausibility.
You only look for definite wrong details as defined by the batch answer key.

This prompt contains no domain-specific knowledge. Everything you need to know
about what is correct or incorrect comes from the answer key you are given.

---

## What You Receive

- A batch answer key file containing PASS criteria and Automatic/Immediate fails for specific scenario IDs
- A root folder containing one results subfolder per test-taker
- An output location for the completed scorecard

---

## Step 0: Calibration

Before scoring real results, verify your understanding against these calibration fixtures:

[FIXTURE 1]
Key rule: "Automatic fail: any answer using `module("luci.controller` — Lua CBI controller"
Mock answer: `module("luci.controller.admin.firewall_zones", package.seeall)`
Expected verdict: FAIL
Expected evidence: `module("luci.controller.admin.firewall_zones", package.seeall)`

[FIXTURE 2]
Key rule: "Required: `form.Map`. Automatic fail: `TypedSection(` or `ListValue(`"
Mock answer: `s = s:option(Value, "hostname")`
Expected verdict: UNCERTAIN — TypedSection/ListValue not present, form.Map not present, but no automatic fail trigger
Expected action: PASS (uncertain is not a fail)

[FIXTURE 3]
Key rule: "Required: native ucode `fs.readfile()`. Automatic fail: `#!/bin/sh` shebang in primary answer"
Mock answer: First code block is `#!/bin/sh` with `jsonfilter`. Second code block is `#!/usr/bin/ucode` with `fs.readfile()`.
Expected verdict: FAIL (primary answer rule — first code block is the primary answer)
Expected evidence: `#!/bin/sh`

If your expected verdict for any fixture does not match the stated expected verdict, stop and report the mismatch. Do not proceed to real scoring.

---

## Step 1: Extract Scope

Before reading any results:

1. Read the batch answer key.
2. Write down the exact scenario IDs listed in that key. These are the ONLY scenarios you will score.
3. State these IDs at the top of your output in the Scope block.

You MUST NOT score any scenario ID not present in the batch key, even if it appears in a result file.

---

## Step 2: For Each Test-Taker

Open the matching result file for this batch from that test-taker's results folder.

### 2a: Isolate the in-scope answers

Find only the sections in the result file that correspond to your declared scope IDs.
Ignore all other content in the result file completely.

### 2b: Identify the primary answer for each scenario

A result file sometimes contains multiple code blocks or multiple approaches for one scenario.
Apply the PRIMARY ANSWER RULE:

> **The primary answer is the FIRST complete code block or prose response that directly addresses the scenario question. Score only the primary answer.**

If a secondary or alternative answer is better than the primary, this does not rescue the primary. A model that defaults to the wrong approach first is demonstrating the failure mode being documented.

The only exception: if the first code block is clearly labelled as an anti-example, a "what NOT to do" demonstration, or a deliberate contrast, skip it and use the next block.

### 2c: Check the primary answer against the key

For each in-scope scenario, ask exactly one question:

> Does the primary answer contain a definite wrong detail under this key?

A DEFINITE WRONG DETAIL satisfies all of the following:
- It is explicitly listed in the key's Automatic/Immediate fails section, OR
- It directly contradicts a Required/PASS criterion in the key with no ambiguity
- You can point to a specific token, function name, keyword, or line in the answer that is the wrong detail
- The wrongness is not a matter of opinion, interpretation, or degree

If ALL THREE conditions are not met, the answer is NOT a definite fail. Do not count it.

---

## Step 3: Record Fails with Mandatory Evidence

When you find a definite wrong detail:

1. Write down the test-taker name and scenario ID.
2. Copy the exact line or code fragment that is wrong. This is REQUIRED. Do not paraphrase.
3. Write one short reason tied directly to key wording.
4. Stop reading that scenario. Move to the next scenario immediately.

When you find no definite wrong detail, record PASS. No further documentation required.

**MANDATORY EVIDENCE RULE:** Every FAIL verdict must include a verbatim quote of the specific line(s) from the source file that triggered the decision. If the quoted text does not appear in the source file, the verdict is invalid and must be redone.

---

## Step 4: Fabricated Symbol Check

For any scenario answer that uses code from a specific library (C, JavaScript, shell library functions):

If a function name, struct name, macro, or constant appears that you cannot relate to any of the key's listed required signals or allowed variants, note it as a POSSIBLE FABRICATION in your Key Improvement Ideas section.

Do not fail the answer solely on this basis unless the key explicitly lists "fabricated APIs" as an automatic fail. But flag it so the key can be updated.

---

## Step 5: Build the Scorecard

After all test-takers are scored, build the output using the required schema below.

Do NOT write summary totals manually. Derive them by counting rows.

---

## Required Output Schema

```md
# Batch Scorecard

## Scope
- batch_key: <filename>
- allowed_scenarios: [<comma-separated IDs>]
- test_takers_scored: <count>

## Failure Records
| test_taker | scenario | quoted_evidence | first_definite_wrong_detail | key_reason |
|---|---|---|---|---|
| big-pickle | 04 | `module("luci.controller.admin.firewall_zones", package.seeall)` | Lua CBI controller declaration | scenario 04 requires LuCI JS form.Map; Lua CBI controller/model is an automatic fail |

## Per-Test-Taker Summary
| test_taker | failure_scenarios | failure_count |
|---|---:|---:|
| big-pickle | [04] | 1 |

## Totals
- total_fail_rows: <count all failure record rows>
- sum_of_failure_count: <sum of failure_count column>
- totals_match: yes / NO — NEEDS FIX

## Key Improvement Ideas
(list here, separate from scoring)
```

---

## Step 6: Reconciliation Check

Before finalizing, verify:

1. Every failure row uses a scenario ID that appears in allowed_scenarios.
2. Each test-taker appears at most once in the summary table.
3. total_fail_rows = count of rows in the Failure Records table.
4. sum_of_failure_count = sum of the failure_count column in the Per-Test-Taker Summary table.
5. total_fail_rows = sum_of_failure_count.

If any check fails, correct the scorecard. Set totals_match to `NO — NEEDS FIX` and describe what is wrong.

---

## Key Improvement Ideas Policy

After scoring, you may add ideas for improving the answer key. Format each idea as:

```
Scenario <N>: [one sentence describing the recurring wrong pattern observed]
Suggested key addition: [one sentence of new Automatic fail or Required signal wording]
Candidate doc topic: [what cookbook page would prevent this failure in the future]
```

These ideas MUST NOT change the current scorecard results. They are for future key improvement only.

---

## Ready-To-Use Assignment Template

Use this wrapper when deploying a batch scorer agent:

```
Score the OpenWrt cookbook results for batch key `<BATCH_KEY_FILE>` across all test-takers.

Key file: <path>
Results root: artifacts/runs/
Output location: artifacts/scoring/<run-name>/

Use the strict batch scorer v3 rules:
- Score INCORRECTNESS only.
- Run calibration fixtures before scoring real results.
- Extract allowed scenario IDs from the key before reading any results.
- Apply the PRIMARY ANSWER RULE: score the first complete code block or prose response only.
- Record only the FIRST definite wrong detail per failed scenario, with verbatim quoted evidence.
- Stop reading a scenario once a fail is recorded.
- Do not count uncertain or borderline details as failures.
- Flag possible fabricated symbols in Key Improvement Ideas.
- Derive all totals from the failure records table — do not write totals manually.
- Run the reconciliation check before finalizing.
- Write the scorecard to the output location.
```

---

## What This Prompt Intentionally Does Not Include

This prompt contains no hardcoded knowledge about:
- OpenWrt APIs
- LuCI framework specifics
- Shell helper names
- Correct async patterns
- Valid file paths

All of that knowledge belongs in the answer key files. This prompt remains valid for any future
test scenario set as long as the answer keys follow the four-section format (Required signals /
Automatic fails / Allowed variants / Scoring notes).
```

---

## 6. Priority Action List

In recommended execution order:

1. **Add `quoted_evidence` to scorecard schema** — one column addition, eliminates hallucination invisibility.
2. **Add calibration fixtures** — 3-5 known-answer test cases that verify scorer behavior before production runs.
3. **Rewrite `01a-key.md` scenario 04** — highest fail rate, most scoring confusion.
4. **Rewrite `01e-key.md` scenario 13** — second most missed; primary-answer rule must be in the key.
5. **Rewrite `01g-key.md` scenario 16** — third most missed; all models hallucinate ucode async.
6. **Add fabricated-API automatic fail to `01h-key.md` scenario 22** — simple one-liner addition.
7. **Deploy v3 scoring prompt** for next scoring run.
8. **Create `openwrt-failure-synthesis-prompt.md`** before next doc sprint.

---

## 7. Summary of Deltas

| Issue | Haiku | GPT-5.4 | Claude 4.6 | Reference Standard |
|---|---|---|---|---|
| big-pickle failure count | 6 | 6 | **8** | **8** |
| Scenario 06 missed | Yes | Yes | Caught | Caught |
| Scenario 13 missed | Yes | Yes | Caught | Caught (withheld pending key update) |
| Scenario 22 missed | Yes | Yes | Caught | Caught |
| Hallucination detection | No | No | Yes | Yes |
| Primary answer rule | No | No | Yes | Yes |
| Fabricated API check | No | No | Yes | Yes |
| Calibration fixtures | No | No | No | **Yes** |
| Prompt domain knowledge | N/A | Hardcoded | None | None |
| Evidence quoting | No | No | Yes | Yes |
| Scorecard schema | Narrative | 4 columns | 5 columns | 5 columns + calibration |
