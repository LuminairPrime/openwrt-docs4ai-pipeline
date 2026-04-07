# Scoring Prompt v2 — OpenWrt Cookbook Test Results

**Supersedes:** `scoring-plan-draft-for-haiku.txt`  
**Purpose:** Grade AI model test results for incorrectness, then synthesize failure documentation.

---

## Background and Goal

You are grading code answers produced by AI models taking OpenWrt development tests. The goal is not to find every imperfection — it is to identify **definite wrong answers** so we can write targeted documentation that teaches the correct patterns.

Each failure you find will later be turned into documentation. A false positive (marking a correct answer as wrong) wastes documentation effort. A false negative (missing a clear failure) leaves a documentation gap. Aim for high precision: only mark FAIL when you are confident the key's **Immediate Fails** criteria are triggered.

---

## Test Structure

Each test batch file (`01a.md`, `01b.md`, etc.) contains:
- Three **common anchor scenarios**: 26, 27, 17 (appear in every batch)
- Three **unique scenarios** specific to that batch

Each **key file** covers the scenarios being evaluated for that batch:
- `01a-key.md` → evaluates scenarios 01, 03, 04
- `01b-key.md` → evaluates scenarios 02, 06, 09
- `01c-key.md` → evaluates scenarios 07, 05, 10
- `01d-key.md` → evaluates scenarios 08, 11, 12
- `01e-key.md` → evaluates scenarios 13, 14, 19
- `01f-key.md` → evaluates scenarios 15, 18, 20
- `01g-key.md` → evaluates scenarios 16, 21, 23
- `01h-key.md` → evaluates scenarios 22, 24, 25
- `01i-key.md` → evaluates scenarios 26, 27, 17

Result files are in each test-taker's folder:  
`artifacts/runs/<test-taker-name>/results/01a-result.md`, etc.

---

## Scoring Agents Setup

Spin up **one agent per key file** (9 agents total). Each key agent will:

1. Load its assigned key file
2. For each test-taker in alphabetical order, open the corresponding result file
3. Find the relevant scenario answer in that result file
4. Apply criteria (see below)
5. Output a **structured per-key report** (format specified below)

Test-takers to score (alphabetical):
- big-pickle
- dola-seed-20-pro
- gemini-3-flash
- grok-code-fast-1-optimized
- haiku-46
- minimax-m25
- nemotron-3-super-120b
- qwen-36-plus
- raptor-mini

---

## Grading Criteria (READ CAREFULLY)

### The FAIL threshold

Mark FAIL **only when** both conditions are true:
1. The answer violates one of the key's listed **Immediate fails** criteria
2. The violation is in **the primary answer** — the first code block or prose that directly addresses the prompt

### Multi-answer handling

Many test-takers provide a primary answer followed by "alternatives," "fallbacks," or secondary examples. Apply these rules:

- **Primary answer wrong, alternative correct → FAIL.** The primary answer is what matters. A model that defaults to the wrong pattern first is demonstrating the failure mode we want to document, even if it also knows the right pattern.
- **Primary answer correct, alternative wrong → PASS.** Note the problematic alternative in the observation field, but do not fail the test-taker.
- **Only one answer provided, and it is wrong → FAIL.** Standard case.

### The language-boundary rule (critical)

Several scenarios explicitly require **native ucode** (`#!/usr/bin/ucode`) rather than shell. The key Immediate Fails for those scenarios include "shell wrappers" as a fail. Apply this strictly:

- A script that starts with `#!/bin/sh` and sources `jshn.sh`, `jsonfilter`, etc. is a **shell script**, not a ucode script. If the scenario requires ucode, this is an immediate fail regardless of how competent the shell script is.
- A script that starts with `#!/usr/bin/ucode` and uses native `import` / `require` of ucode modules is a ucode script. PASS.

### Fabricated API rule

If an answer uses library function names that **do not exist** in the real API (e.g., calling `ubus_reply_create()` when the real function is `ubus_send_reply()` after `blob_buf_init()`), mark FAIL as "fabricated API." This applies to any library: libubus, libubox/blobmsg, LuCI JS, ucidef, etc.

---

## Per-Key Agent Output Format

Each key agent **must** produce output in this exact format. Do not deviate.

```
## Key: <key filename>
## Scenarios covered: <comma-separated scenario numbers>

### Test-taker: <name>

#### Scenario <N> — <name from key>
- **Primary answer type:** [describe in ≤10 words what approach the test-taker took]
- **Immediate fail triggered:** [YES / NO]
- **Fail criterion:** [copy the exact Immediate fail text from the key, or "N/A"]
- **Offending code (quote up to 2 lines):** [paste the exact line(s) that triggered the fail, or "N/A"]
- **VERDICT:** PASS | FAIL

#### Scenario <N> — <name from key>
[repeat for each scenario in this key]

**Test-taker total FAILs this key: <number>**
**Failed scenarios: <list of scenario numbers>**

---
```

Repeat the block above for each test-taker. After all test-takers are done, add:

```
## Cross-Taker Pattern Summary (this key only)

Per-scenario fail counts:
- Scenario <N>: <X> of <Y> test-takers FAILED

Most common fail reason per scenario:
- Scenario <N>: <brief description of dominant wrong pattern>

Suggested key enhancements:
- [Any new Immediate fail criterion the grading process revealed as useful]
- [Any ambiguity in the existing criteria that caused difficulty]
```

---

## Orchestrator Synthesis Instructions

After all 9 key agents have completed, the **orchestrator** collects all per-key reports and produces the final scorecard file in `artifacts/scoring/haiku/` (or the appropriate run subfolder).

The final scorecard must include:

### Section 1 — Summary Scorecard Table

| Test-Taker | Total Tests | Total Failures | Failure Rate | Grade |
|---|---|---|---|---|
...

Grading scale: 0 fails = A, 1-2 = B, 3 = C, 4-5 = D, 6+ = F.  
Mark as "NO RESULT" for any test-taker with no result files.

### Section 2 — Per-Batch Detailed Breakdown

For each batch (01a–01i), show a table:

| Test-Taker | Scen N | Scen N | Scen N | Batch FAILs |
|---|---|---|---|---|
| big-pickle | ✓ | ✗ FAIL | ✓ | 1 |
...

Include one sentence explaining each FAIL, quoting the trigger code.

### Section 3 — Failure Pattern Analysis

Group all FAILs by scenario. For each scenario that had any FAIL:
- How many test-takers failed
- The dominant wrong approach (with example)
- The correct approach (with brief example)
- Which documentation topic this gap should generate

### Section 4 — Recommended Key Enhancements

List specific new Immediate Fail criteria or clarifications surfaced during grading, grouped by scenario.

### Section 5 — Cookbook Documentation Backlog

For each documented failure pattern, generate one documentation task item:
```
[ ] DOC: <short title>
    Gap: <what the models got wrong>
    Correct pattern: <what the docs should teach>
    Affected scenarios: <list>
    Priority: HIGH / MEDIUM / LOW
```

---

## Important Calibration Notes

These patterns were observed in the first grading run and should be checked for **in every answer**:

1. **ucode boundary check:** Any scenario about ucode that receives a `#!/bin/sh` answer with jshn/jsonfilter = immediate fail.
2. **LuCI JS vs Lua CBI:** Any LuCI form scenario that receives Lua CBI (Map, TypedSection, ListValue in .lua files) = immediate fail.
3. **jsonfilter in ucode context:** Any answer that uses `jsonfilter` when the scenario asks for ucode = immediate fail.
4. **Service calls in uci-defaults:** Any `uci-defaults` answer that calls `/etc/init.d/` = immediate fail.
5. **Shell & background jobs in async ucode:** Any async/parallel ucode scenario where the answer uses `&` background jobs or `mkfifo` = immediate fail.
6. **Wrong config parsing:** Any procd/validation scenario where the answer uses `grep`/`awk` over `/etc/config/` = immediate fail.
7. **Fabricated C APIs:** Check function names in C answers against known libubus/blobmsg names.

---

## File Paths

```
Keys:    artifacts/tests-keys/<batch>-key.md
Results: artifacts/runs/<test-taker>/results/<batch>-result.md
Output:  artifacts/scoring/<run-name>/<scoring-report>.md
```
