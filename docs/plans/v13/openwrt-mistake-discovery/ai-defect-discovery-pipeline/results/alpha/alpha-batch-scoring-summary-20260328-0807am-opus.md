# AI Evaluation Pipeline - Alpha Batch Scoring Summary (Re-evaluation)

**Date:** 2026-03-28 (Local Start Time: ~08:07 AM)
**Evaluator Model:** Claude Opus 4.6 (Thinking)
**Dataset:** 01a-batch-slice-alpha.md
**Scenarios Scored:** 01, 05, 07, 10, 13, 16
**Total Models Scored:** 16
**Golden Key Reference:** 03-golden-answers-key.md
**Authoritative Documentation:** openwrt-condensed-docs (common-ai-mistakes.md, procd-service-lifecycle.md, firstboot-uci-defaults-pattern.md)

This document summarizes the full re-evaluation of all 16 AI model outputs in the Alpha Batch, scored deterministically against the Golden Answers falsification schema.

## Performance Leaderboard

| Rank | Model | Score | % | Architectural Tier |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **GPT 5.2 High** | **4 / 6** | **67%** | **Elite.** Only model to correctly use modern LuCI JS `rpc.declare`. |
| 2 | Claude Opus 4.6 (Thinking) | 3 / 6 | 50% | Advanced. Flawless procd/C/uci-defaults. Failed LuCI JS and uCode. |
| 3 | Claude Sonnet 4.6 | 3 / 6 | 50% | Advanced. Most verbose, excellent C. Failed LuCI JS and uCode. |
| 4 | Gemini Flash Thinking | 3 / 6 | 50% | Standard. Solid core basics. No uCode or LuCI JS awareness. |
| 5 | Gemini Pro | 3 / 6 | 50% | Standard. Mirrors Gemini Flash findings. |
| 6 | GLM-5 | 3 / 6 | 50% | Standard. Added unnecessary `rm -f` but saved by `exit 0`. |
| 7 | Hearth | 3 / 6 | 50% | Legacy-Aware. Consciously chose legacy Lua despite knowing JS exists. |
| 8 | Kimi k2.5 | 3 / 6 | 50% | Standard. Wrote CGI script for S05 but core procd/C/uci-defaults correct. |
| 9 | DeepSeek V3 32B | 2 / 6 | 33% | Lower-Mid. Created banned sentinel file in Scenario 10. |
| 10 | Dola Seed 2.0 Pro | 2 / 6 | 33% | Lower-Mid. Missing `exit 0` in Scenario 10. |
| 11 | Grok 4.20 | 2 / 6 | 33% | Lower-Mid. Missing `exit 0` in Scenario 10. |
| 12 | Minimax m2.7 | 2 / 6 | 33% | Lower-Mid. Missing `exit 0`, manual `rm -f` in Scenario 10. |
| 13 | Qwen 3.5 Max | 2 / 6 | 33% | Lower-Mid. Missing `exit 0` in Scenario 10. |
| 14 | Significant Otter | 1 / 6 | 17% | Fragmented. Fabricated C API signatures. Fabricated ubus methods. Missing `exit 0`. |
| 15 | Mimo v2 Pro | 1 / 6 | 17% | Fragmented. Used `json-c` double-wrap pattern. Sentinel file. |
| 16 | Nvidia Nemotron | 0 / 6 | 0% | **Failed.** SysVinit, PID files, fabricated APIs, no `uci-defaults` awareness. |

## Score Distribution

| Score | Count | Models |
| :--- | :--- | :--- |
| 4/6 (67%) | 1 | GPT 5.2 High |
| 3/6 (50%) | 7 | Claude Opus, Claude Sonnet, Gemini Flash, Gemini Pro, GLM-5, Hearth, Kimi |
| 2/6 (33%) | 5 | DeepSeek, Dola Seed, Grok, Minimax, Qwen |
| 1/6 (17%) | 2 | Mimo v2 Pro, Significant Otter |
| 0/6 (0%) | 1 | Nvidia Nemotron |

## Per-Scenario Pass Rates

| Scenario | Description | Pass Count | Pass Rate | Key Finding |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Procd Daemon & Config | **15 / 16** | **94%** | Near-universal pass. Only Nvidia Nemotron used SysVinit `start()`/`stop()` with PID files. |
| **05** | LuCI JS Live Status | **1 / 16** | **6%** | Only GPT 5.2 used `rpc.declare`. 14 used Lua templates. 1 used CGI. |
| **07** | C ubus RPC Handler | **13 / 16** | **81%** | 13 correct. Nemotron fabricated APIs. Mimo double-wrapped. Significant Otter had wrong signatures. |
| **10** | UCI Defaults First-Boot | **8 / 16** | **50%** | 8 correctly included `exit 0`. 5 omitted it. 2 used sentinel files. 1 used `/etc/rc.local`. |
| **13** | Native JSON Parsing | **0 / 16** | **0%** | **Zero models used `ucode`.** All fell back to `jsonfilter`, `jshn`, `jq`, or `awk`. |
| **16** | Async Parallel Ping | **0 / 16** | **0%** | **Zero models used `ucode` `uloop`.** All used shell `&` background jobs. |

## Critical Discoveries

1. **The uCode Knowledge Gap (CONFIRMED):** 0/16 models identified `ucode` as the correct standard for JSON parsing (Scenario 13) or asynchronous parallel processing (Scenario 16). This is the single largest training data gap across the entire test matrix.

2. **The Modern LuCI JS Barrier:** Only 1/16 models (GPT 5.2) correctly used the modern `rpc.declare` pattern. 14/16 fell into the deprecated Lua `.htm` template trap. 1 wrote a standalone CGI script.

3. **The `exit 0` Trap:** 8/16 models (50%) correctly included `exit 0` in their `uci-defaults` scripts. The other 50% demonstrated one of:
   - Missing `exit 0` entirely (5 models)
   - Creating redundant sentinel files (2 models: DeepSeek, Mimo)
   - Using `/etc/rc.local` with `/tmp` lockfiles (1 model: Nemotron)

4. **Core IPC Proficiency:** 13/16 (81%) models correctly used `blobmsg_add_string` and `ubus_send_reply` for C-based RPC. The C IPC layer is well-represented in training data.

5. **procd Universality:** 15/16 (94%) models correctly identified `USE_PROCD=1` as the init pattern. Only Nvidia Nemotron used SysVinit-style `start()`/`stop()`.

## New Truths Added to Golden Key
*   `jshn.sh` (`/usr/share/libubox/jshn.sh`) with `json_init`, `json_load`, `json_get_var` is a valid native OpenWrt JSON parsing API at the shell level.
*   `L.ready()` + modern LuCI JS runtime is the correct client-side entry point.

## New Falsenesses Added to Golden Key
*   **FIFO-based parallel processing** (FIFOs with `while read` loops) — variant of banned "Shell Hacks" pattern.
*   **Standalone CGI scripts** (`/www/cgi-bin/`) for LuCI views — bypasses LuCI architecture entirely.
*   **`blobmsg_add_json_from_string()` double-wrap** — building JSON with `json-c` then injecting via `blobmsg_add_json_from_string()`.
*   **Fabricated ubus API functions** — `ubus_request_set_result()`, `ubus_add_workhandler()` do not exist.
*   **PID file management** — `echo $! > /var/run/my_daemon.pid` is a SysVinit-era pattern replaced by procd.
*   **`/tmp` lockfile for first-boot** — `/tmp` is cleared every reboot, so the script runs every boot.
*   **Non-existent ubus methods** — `network.get_wireless_clients` is fabricated.
*   **Self-deleting `uci-defaults` scripts** — Manual `rm -f` shows misunderstanding; `exit 0` is the contract.

## Score Files Generated
16 individual score files with timestamp suffix `20260328-0807am` written to the `results/alpha/` directory.
