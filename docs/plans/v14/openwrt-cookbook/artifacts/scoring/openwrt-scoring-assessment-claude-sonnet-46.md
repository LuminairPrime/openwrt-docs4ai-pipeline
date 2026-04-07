# OpenWrt Scoring Assessment — Claude Sonnet 4.6

**Date:** April 6, 2026  
**Assessed by:** Claude Sonnet 4.6  
**Reference runs:** haiku-46 scorecard, GPT-5.4 assessment, independent big-pickle rescore

---

## 1. Executive Summary

Both the haiku scorecards and the GPT-5.4 assessment have already identified the correct structural problems with the original prompt. I fully agree with GPT-5.4's diagnosis. This document adds three things the prior assessments missed:

1. **The hallucination failure mode** — haiku described answers that do not match the actual code for at least one scenario. This is more dangerous than lenient grading, and it is not addressed by any prior fix plan.
2. **Three additional big-pickle failures** that both haiku and GPT-5.4 missed, with the specific evidence.
3. **A fully generalized scoring prompt** that is scenario-agnostic, key-driven, and designed to work with weaker models without any hardcoded domain assumptions.

---

## 2. Independent Rescore: big-pickle

I rescored all 27 big-pickle scenarios independently before reading the prior scorecards.

**My count: 8 failures.** Haiku's count: 6. GPT-5.4's count: 6.

### Failures Present in All Three Assessments

| Scenario | Failure Reason |
|---|---|
| 04 | Lua CBI (module/Map/TypedSection) instead of modern LuCI JS form.Map |
| 02 | Shell wrapper: `. /usr/share/libubox/jshn.sh` + `ubus list \| grep \| jsonfilter` |
| 05 | Lua + `<%...%>` raw HTML template instead of LuCI DOM helpers |
| 10 | Wrong location (`/etc/rc.d/S99firstboot`) + calls `/etc/init.d/system reload` |
| 18 | `render()` builds raw HTML string with `var html = '<div class="cbi-map">'` — not form.Map |
| 16 | Shell background jobs `&` + `mkfifo` — both explicit immediate fails |

### Three Failures I Found That Both Prior Assessments Missed

#### Scenario 06 — FAIL (missed by both)

**What the key requires:** `uci_load_validate` or `config_load`. **Immediate fail:** regex/text parsing of `/etc/config/*`.

**What big-pickle actually answered:**
```sh
loglevel=$(grep -E '^\s*option\s+loglevel' "$config_file" 2>/dev/null | \
           awk '{for(i=1;i<=NF;i++) if($i=="loglevel") print $(i+1)}' | \
           tr -d "'\"" | tr -d ' ')
```

This is direct `grep`+`awk` over an `/etc/config` file. It is the exact pattern the key lists as an immediate fail.

**Why haiku missed it:** Haiku's scorecard states: *"Uses config_load, config_get_bool, arithmetic validation"* — a description that does not match the actual code in any way. Haiku **hallucinated** this answer. The code contains no `config_load` or `config_get_bool` call.

**Why GPT-5.4 missed it:** GPT-5.4's rescore also returned 6 failures, which means it also missed scenario 06. This suggests it read haiku's description rather than the source file, or also hallucinated the answer.

#### Scenario 13 — FAIL (missed by both)

**What the key requires:** native ucode `fs.readfile()`, native `json()`. **Immediate fail:** `jshn`, shell wrappers.

**What big-pickle actually answered (primary answer):**
```sh
#!/bin/sh
. /usr/share/libubox/jshn.sh
json_load "$(cat "$CONFIG_FILE")"
json_get_var startup_delay "startup_delay"
```

This is a `#!/bin/sh` shell script sourcing `jshn.sh`. The scenario is in the ucode context. The ucode alternative is buried at the bottom as the third option. The primary answer is an immediate fail.

**Why both prior assessments missed it:** Neither the original prompt nor GPT-5.4's prompt enforces a **primary-answer-first rule**. When a correct variant exists anywhere in the response, both scorers defaulted to PASS.

#### Scenario 22 — FAIL (missed by both)

**What the key requires:** `blobmsg_policy` + `blobmsg_parse()`, `blobmsg_open_table()`, `ubus_send_reply()`. **Immediate fail:** raw pointer casting.

**What big-pickle actually answered:**
```c
void *reply = ubus_reply_create(ctx, req, 0);
...
ubus_reply_send(ctx, req, reply);
```

`ubus_reply_create()` and `ubus_reply_send()` **do not exist in libubus**. The real API is `blob_buf_init()` + `blobmsg_*` helpers + `ubus_send_reply()`. The `reply` variable is typed `void*` and then passed directly to `blobmsg_add_string(reply, ...)` — blobmsg functions require `struct blob_buf *`, not `void *`. This is both a fabricated API and a raw pointer cast.

**Why both prior assessments missed it:** No prior prompt told the scorer to check whether named library functions actually exist. A scorer using only its OpenWrt knowledge might infer these are real APIs without verifying.

---

## 3. The Hallucination Problem

Scenario 06 reveals a failure mode more severe than lenient grading: **the scorer described an answer that does not exist in the source file**.

Haiku's scorecard reads:
> "Uses config_load, config_get_bool, arithmetic validation"

The actual code contains neither `config_load` nor `config_get_bool`. Haiku either:
a) generated a plausible-sounding answer description from prior context instead of reading the file, or
b) confused this test-taker's result with another test-taker's correct answer for the same scenario.

This failure mode is invisible in the final scorecard — there is no signal that haiku hallucinated. The only way to detect it is to read the source file and compare.

### Fix: Mandatory Code Quote Before Verdict

Every failure or near-failure verdict must be preceded by a **verbatim code quote** of the specific line(s) that triggered the decision. This makes hallucination immediately auditable. If the quoted code does not appear in the source file, the scoring result is invalid.

This single change would have caught the scenario 06 miss. A reviewer could see:

> Quoted code: `config_load my_daemon; config_get hostname...`  
vs.  
> Actual code: `grep -E '^\s*option\s+loglevel' "$config_file" | awk ...`

---

## 4. Files I Want to Change

### 4a. All nine key files (`01a-key.md` — `01i-key.md`)

**Problem:** The current key format is too narrative. Phrases like "must use modern LuCI JS view architecture" require the scorer to know what that means. A weaker model does not have that background, so it defaults to "this looks like a web page — probably fine."

**Fix plan:** Rewrite each key using a rigid four-section format. Full templates are in Section 6.

The four sections replace current free prose:

1. **`Required signals`** — concrete tokens/patterns that MUST appear in the answer. Examples: function name, file path, shell shebang, keyword.
2. **`Automatic fails`** — concrete tokens/patterns that trigger immediate FAIL if present. Should be checkable by grep where possible.
3. **`Allowed variants`** — explicitly whitelisted alternatives so the scorer does not fail correct-but-different answers.
4. **`Scoring notes`** — one or two sentences of disambiguation for the hardest judgment calls.

**Priority order for rewrites (highest risk first):**

1. Scenario 04, 05, 14, 18, 27 — LuCI JS architecture (highest hallucination risk, highest fail rate)
2. Scenario 02, 13, 16 — native ucode boundary (second most common failure mode)
3. Scenario 06, 10, 20 — lifecycle/placement rules (small but important)
4. Scenario 03, 07, 12, 22 — C libubus/blobmsg (mostly passing but scenario 22 has fabrication risk)
5. Remaining scenarios — low priority, already reasonably clear

**Exact rewrites for the two highest-impact scenarios:**

#### Scenario 04 — LuCI JS Dynamic Form (proposed new key section)

```md
### Required signals
- Answer must include `L.view.extend(` or equivalent LuCI JS view class declaration.
- Answer must instantiate `form.Map` (or `form.JSONMap`).
- Answer must populate the form with LuCI JS widget/option objects.

### Automatic fails
- Any file with `module("luci.controller` — this is the Lua CBI controller pattern.
- Any file with `Map(` and a Lua table argument — this is the Lua CBI model pattern.
- Any file with `TypedSection(` or `ListValue(` — these are Lua CBI-only APIs.
- Any raw HTML file using `<%` template tags as the main solution.
- Any use of a non-LuCI frontend framework (React, Vue, plain fetch + innerHTML).

### Allowed variants
- Different ways of importing LuCI JS modules are fine.
- Different form.Map option types are fine as long as they are LuCI JS types.
- A view that extends `LuCI.view` instead of using `L.view.extend` is acceptable.

### Scoring notes
- If the answer contains both a Lua CBI section and a LuCI JS section, the Lua CBI section
  is the primary answer if it appears first. Apply the automatic fail.
- Do not rescue because the interface list is fetched dynamically — the architecture must still be LuCI JS.
```

#### Scenario 13 — uCode Native fs/json Parsing (proposed new key section)

```md
### Required signals
- Answer's main code block must start with `#!/usr/bin/ucode` or use ucode `import`/`require` syntax.
- Must use native ucode file I/O: `fs.open(`, `fs.readfile(`, or equivalent ucode fs module call.
- Must parse JSON with native ucode: `json(`, `JSON.parse(` in ucode context, or import of ucode json module.

### Automatic fails
- Answer's primary code block starts with `#!/bin/sh` or `#!/bin/ash` — this is a shell script, not ucode.
- Any use of `. /usr/share/libubox/jshn.sh` or `json_load` shell helpers in the primary answer.
- Any use of `jsonfilter` as the main parsing path.
- Any use of `jq` as the main parsing path.
- Shell subprocess substitution like `$(cat file | jsonfilter ...)` in the primary answer.

### Allowed variants
- Any ucode module import style is fine.
- The exact fs function name may vary (`readfile`, `open`+`read`, etc.) as long as it is ucode native.

### Scoring notes
- PRIMARY ANSWER RULE: if the answer provides multiple solutions, the FIRST complete code block
  is the primary answer. Score only that. If it is a shell script, that is an automatic fail
  regardless of whether a correct ucode solution also appears later in the response.
- A `#!/usr/bin/ucode` shebang that then does `system("cat file | jsonfilter ...")` is still
  a shell wrapper fail — check what happens inside, not just the shebang.
```

---

### 4b. `artifacts/scoring/scoring-prompt-v2.md` (mine, from this session)

**Problem:** My v2 prompt has good rules but includes a hardcoded calibration checklist of seven specific patterns (LuCI CBI, jsonfilter in ucode, etc.). This means the prompt encodes scenario knowledge that belongs in the keys.

**Fix plan:** Remove the hardcoded pattern list. Replace it with a generalized "boundary detection" section that teaches the scorer HOW to check for violations rather than WHAT violations to look for. The key files should be the only source of "what." See the new prompt in Section 5.

---

### 4c. `artifacts/templates/00-batch-prompt-header-template.md`

**Problem:** The current template exists but has not been updated to reflect lessons from the first scoring run.

**Fix plan:** Replace its contents with the wrapper template from the new scoring prompt (Section 5, subsection "Ready-To-Use Assignment Template").

The template should also add one new instruction: **Every verdict must be preceded by a verbatim code quote.** This is the primary defense against hallucination.

---

### 4d. New file: `artifacts/scoring/openwrt-scorecard-schema.md`

**Problem:** No canonical schema exists. Each assessor has proposed slight variations.

**Fix plan:** Create a single frozen schema that the v2 prompt and all future scorers reference. GPT-5.4 proposed a good schema — adopt it with one addition: a `quoted_evidence` column in the failure records table.

```md
## Failure Records
| test_taker | scenario | quoted_evidence | first_definite_wrong_detail | key_reason |
|---|---|---|---|---|
```

`quoted_evidence` must be an exact copy of the line(s) from the source file that triggered the fail. If it is blank, the verdict is invalid.

---

### 4e. New file: `artifacts/scoring/openwrt-failure-synthesis-prompt.md`

**Problem (agreed with GPT-5.4):** Scoring and documentation planning are mixed in the same prompt, which degrades both.

**Fix plan:** Create a second-stage synthesis prompt. Its input is the completed scorecard. Its output is a set of documentation work items. Defined in Section 5b below.

---

## 5. The New Generalized Scoring Prompt

This prompt contains zero scenario-specific knowledge. All domain knowledge must come from the key file. This makes it reusable for any future scenario set without modification.

---

```md
# OpenWrt Cookbook Strict Batch Scorer

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

## Step 3: Record Fails

When you find a definite wrong detail:

1. Write down the test-taker name and scenario ID.
2. Copy the exact line or code fragment that is wrong. This is REQUIRED. Do not paraphrase.
3. Write one short reason tied directly to key wording.
4. Stop reading that scenario. Move to the next scenario immediately.

When you find no definite wrong detail, record PASS. No further documentation required.

---

## Step 4: Fabricated Symbol Check

For any scenario answer that uses code from a specific library (C, JavaScript, shell library functions):

If a function name, struct name, macro, or constant appears that you cannot relate to any of the key's listed required signals, note it as a POSSIBLE FABRICATION in your Key Improvement Ideas section. Do not fail the answer solely on this basis — only fail if the key explicitly names it. But flag it so the key can be updated.

Exception: if the key's Automatic fails section lists "fabricated APIs" as a generic fail, you MAY fail an answer for using function names that clearly do not match real library functions known to exist. Explain your reasoning.

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

Use the strict batch scorer rules:
- Score INCORRECTNESS only.
- Extract allowed scenario IDs from the key before reading any results.
- Apply the PRIMARY ANSWER RULE: score the first complete code block or prose response only.
- Record only the FIRST definite wrong detail per failed scenario, with verbatim quoted evidence.
- Stop reading a scenario once a fail is recorded.
- Do not count uncertain or borderline details as failures.
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

## 5b. Synthesis Stage Prompt (second-stage, separate from scoring)

After all batch scorecards are collected, run this prompt once:

---

```md
# OpenWrt Cookbook Failure Synthesis

You are NOT scoring. Scoring is already done.
You are reading completed batch scorecards and producing a documentation backlog.

## Input

All batch scorecard files from a scoring run.

## Your Task

1. Aggregate all failure records across all batches.
2. Group failures by scenario ID.
3. For each scenario with 2+ failures across test-takers, produce one documentation work item.
4. For each scenario with 5+ failures across test-takers, mark priority HIGH.

## Output Format

```md
# Documentation Backlog — [Run Name]

## Failure Cluster Summary
| scenario | scenario_name | total_failures | test_takers_affected | priority |
|---|---|---|---|---|

## Documentation Work Items

### DOC-[N]: <short title>
- **Scenario:** <N>
- **Priority:** HIGH / MEDIUM / LOW
- **What models got wrong:** <one sentence describing the dominant wrong pattern, with example>
- **What the docs should teach:** <one sentence describing the correct pattern>
- **Suggested cookbook page title:** <title>
- **Suggested cookbook section:** <section>
- **Key revision needed:** YES / NO
- **Key revision note:** <if YES: one sentence of new Automatic fail or Required signal wording>
```

Keep documentation work items separate from any commentary about scoring quality.
```

---

## 6. Proposed Key Rewrite Stubs

Below are proposed header sections for the highest-priority key rewrites. These are stubs — fill in the tokens from the existing key content.

### `01a-key.md` — Scenario 04

```md
## Scenario 04 — LuCI JS Dynamic Form

### Required signals
- `L.view.extend(` OR `LuCI.view.extend(` — LuCI JS view class
- `form.Map(` — LuCI JS form instantiation
- Dynamic interface data source from LuCI JS API (not a hardcoded array)

### Automatic fails
- `module("luci.controller` — Lua CBI controller
- `Map(` as a Lua function call in a .lua file
- `TypedSection(` — Lua CBI only
- `ListValue(` — Lua CBI only
- `<%` template tags as the main form rendering method
- `entry({...}, cbi(` — legacy Lua CBI dispatcher registration

### Allowed variants
- Different LuCI JS import styles are fine
- Different widget types within the LuCI JS form system are fine
- `form.JSONMap` is acceptable

### Scoring notes
- If the answer provides Lua CBI first and LuCI JS second, apply automatic fail without reading the JS section.
```

### `01e-key.md` — Scenario 13

(See full version in Section 4a above)

### `01g-key.md` — Scenario 16

```md
## Scenario 16 — uCode Parallel Async Ping

### Required signals
- Script shebang `#!/usr/bin/ucode` OR ucode module syntax
- Evidence of async/parallel execution using ucode native primitives (uloop handles, process objects, promises)
- Per-target output identification (both ping targets labeled in output)

### Automatic fails
- Any background job operator `&` in the primary answer
- `mkfifo` — FIFO-based shell multiplexing
- `while true; do ... done &` — shell polling loop in background
- Sequential execution (one ping completes before the other starts)
- `#!/bin/sh` shebang — this is a shell script, not ucode

### Allowed variants
- Different ucode async primitives are fine as long as they are native ucode (not shell)
- Output format may vary

### Scoring notes
- The core requirement is PARALLEL execution in native ucode. Any solution that reduces to shell background processes is an automatic fail even if the shebang says ucode.
```

---

## 7. Summary of Deltas from Prior Assessments

| Issue | GPT-5.4 | This assessment |
|---|---|---|
| big-pickle failure count | 6 (same as haiku) | 8 |
| Scenario 06 missed | Yes | Caught + hallucination explanation |
| Scenario 13 missed | Yes | Caught + primary-answer-first rule |
| Scenario 22 missed | Yes | Caught + fabricated API rule |
| Prompt: hardcoded domain knowledge | Hardcoded calibration checklist | Fully key-driven, zero hardcoded domain |
| Prompt: multi-answer rule | Yes, basic | Yes, with exception for anti-examples |
| Prompt: hallucination defense | Not addressed | Mandatory verbatim evidence quote |
| Prompt: fabricated symbol check | Not addressed | Explicit step 4 |
| Synthesis stage | Recommended | Fully specified separate prompt |
| Key rewrite format | Four sections proposed | Four sections + concrete stubs for top 3 scenarios |
| Scorecard schema | Frozen | Frozen + added `quoted_evidence` column |

---

## 8. One-Page Priority Action List

In recommended execution order:

1. **Add `quoted_evidence` to scorecard schema** — one column addition, eliminates hallucination invisibility.
2. **Rewrite `01a-key.md` scenario 04** — highest fail rate, most scoring confusion.
3. **Rewrite `01e-key.md` scenario 13** — second most missed; primary-answer rule must be in the key.
4. **Rewrite `01g-key.md` scenario 16** — third most missed; all models hallucinate ucode async.
5. **Add fabricated-API automatic fail to `01h-key.md` scenario 22** — simple one-liner addition.
6. **Deploy new generalized scoring prompt** (Section 5) for next scoring run.
7. **Add `quoted_evidence` to key stubs** so key-writing authors know it will be required.
8. **Create `openwrt-failure-synthesis-prompt.md`** (Section 5b) before next doc sprint.
