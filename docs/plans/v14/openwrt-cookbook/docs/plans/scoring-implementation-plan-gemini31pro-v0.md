# Scoring Implementation Plan

**Target:** Implement the 10/10 scoring recommendations found in `docs/plans/v14/openwrt-cookbook/artifacts/scoring/openwrt-scoring-assessment-10-10.md`

## 1. Goal
Transition the OpenWrt test scoring loop to a strict algorithmic paradigm that relies on verbatim quoting, definite failures, and 0% embedded OpenWrt domain knowledge within the scoring agent.

## 2. Files to Modify and Create

### 2.1 Refactor Answer Keys
**Targets:** `artifacts/tests-keys/01a-key.md` through `01i-key.md`
**Action:** Overhaul ALL existing test keys to strictly conform to four rigorous sections. No other sections are permitted.
*   **Required Signals:** Mandatory code patterns the answer must have.
*   **Automatic Fails:** Explicit anti-patterns (e.g., using Lua `luci.controller` instead of `ucode`).
*   **Allowed Variants:** Permitted exceptions to the required signals.
*   **Scoring Notes:** Nuance notes directly meant for the scorer.

### 2.2 Create Calibration Fixtures
**Target:** `artifacts/scoring/openwrt-calibration-fixtures.md`
**Action:** Define 5 predetermined mock scenarios (including one clear hallucination trap, one leniency test, and one fabrication test). The scorer prompt will mandate running through this and matching an expected output before grading real test answers.

### 2.3 Establish the Scorecard Schema
**Target:** `artifacts/scoring/openwrt-scorecard-schema.md`
**Action:** Freeze the Markdown table format.
*   Columns must be exactly: `test_taker`, `scenario`, `quoted_evidence`, `first_definite_wrong_detail`, `key_reason`.
*   Establish strict math reconciliation rules (e.g., total fail rows equals sum of failure count vector).

### 2.4 Deploy Universal Strict Prompt V4
**Target:** `artifacts/scoring/openwrt-test-scoring-prompt-v4.md`
**Action:** Create the master prompt asset. 
*   **Reference:** Use the exact text provided in Section 3 of `openwrt-scoring-assessment-10-10.md`.
*   **Crucial Directives:** Mandate the "Primary Answer Rule" (first code block is the only one graded) and the "Verbatim Evidence Extraction" rule to prevent the agent from generalizing failures.

### 2.5 Scaffold Failure Synthesis
**Target:** `artifacts/scoring/openwrt-failure-synthesis-prompt.md`
**Action:** Write a prompt meant for the *next phase* of the pipeline. This prompt should instruct an agent to ingest multiple populated scorecards and aggregate the `key_reason` columns into actionable OpenWrt documentation tasks or "do's and don'ts" rules.

## 3. Human Operator Integration
The operator will invoke the scoring pipeline by loading the target test outputs, the revised batch keys, the calibration fixtures, and the `v4` scoring prompt into the test-grading AI (Haiku or similar). If the agent fails Phase 1 (Calibration), the operator must reset context and retry, preventing contaminated runs.
