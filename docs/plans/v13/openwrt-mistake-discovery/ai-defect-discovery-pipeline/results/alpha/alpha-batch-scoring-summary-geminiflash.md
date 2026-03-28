# AI Evaluation Pipeline - Alpha Batch Scoring Summary

**Date:** 2026-03-28 (Local Start Time: ~07:30 AM)
**Dataset:** 01a-batch-slice-alpha.md
**Scenarios Scored:** 01, 05, 07, 10, 13, 16
**Total Models Scored:** 15

This document summarizes the results of the deterministic AI evaluation pipeline for the **Alpha Batch**. Each model was benchmarked against the "Golden Truths" of modern OpenWrt development to identify architectural hallucinations and legacy patterns.

## Performance Leaderboard

| Model | Score | Architectural Tier |
| :--- | :--- | :--- |
| **GPT 5.2 High** | **4 / 6 (67%)** | **Elite.** Correctly identified Modern LuCI JS (`rpc.declare`) and standard `procd` primitives. |
| **Significant Otter** | **3 / 6 (50%)** | **Advanced.** Correct modern LuCI JS logic; failed `uci-defaults` due to missing `exit 0`. |
| **Claude Sonnet 4.6** | **3 / 6 (50%)** | **Standard.** Strong grasp of `procd` and `libubus`; unaware of front-end modernization. |
| **DeepSeek V3 32B** | **3 / 6 (50%)** | **Standard.** Proficient in C/IPC; stuck in the Legacy LuCI trap. |
| **Dola Seed 2.0 Pro** | **3 / 6 (50%)** | **Standard.** Consistent with canonical init and RPC; failed uCode/LuCI JS. |
| **Gemini Flash Thinking**| **3 / 6 (50%)** | **Standard.** Solid core basics, but no uCode or LuCI JS awareness. |
| **Gemini Pro** | **3 / 6 (50%)** | **Standard.** Corresponds to Gemini Flash findings. |
| **GLM-5** | **3 / 6 (50%)** | **Standard.** Canonical C and UCI patterns; legacy front-end. |
| **Hearth** | **3 / 6 (50%)** | **Legacy-Aware.** Consciously chose legacy patterns in reasoning; failed modern strict tests. |
| **Kimi k2.5** | **3 / 6 (50%)** | **Standard.** Provided standalone CGI instead of LuCI integration. |
| **Minimax m2.7** | **3 / 6 (50%)** | **Standard.** Solid libubus and uci-defaults; legacy web/uCode. |
| **Qwen 3.5 Max** | **2 / 6 (33%)** | **Lower-Mid.** Correct procd/C; failed uci-defaults `exit 0` requirement. |
| **Grok 4.20** | **2 / 6 (33%)** | **Lower-Mid.** Missing `exit 0` in first-boot scripts. |
| **Mimo v2 Pro** | **1 / 6 (17%)** | **Fragmented.** Incorrectly proposed `json-c` raw string builds in ubus handlers. |
| **Nvidia Nemotron** | **0 / 6 (0%)** | **Failed.** Recommended 2010-era PID file hacks and SysVinit style watchdogs. |

## Critical Discoveries

1.  **The uCode knowledge Gap:** 0/15 models identified `uCode` as the current standard for JSON parsing or asynchronous `uloop` scripting. This highlights a significant training data lag regarding the 2023-2025 OpenWrt paradigm shift.
2.  **The Legacy UI Trap:** 13/15 models still recommend server-side Lua templates (`.htm`), which are deprecated for new development in modern LuCI.
3.  **Core IPC Proficiency:** 14/15 models successfully used `libubus` and `blobmsg` for C-based RPC, showing that the core communication layer is well-represented in training data.

## Actions Taken
*   **Golden Key Updated:** Added "Asynchronous Logic Hacks" and "Missing exit 0" to the Universal Falsenesses database in `03-golden-answers-key.md`.
*   **Score Files Generated:** 15 individual score files with corrected timestamps (`0730am-0800am`) are available in the results directory.
