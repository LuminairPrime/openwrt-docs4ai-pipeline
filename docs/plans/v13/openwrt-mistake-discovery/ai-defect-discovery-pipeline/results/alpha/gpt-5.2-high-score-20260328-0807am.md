# GPT 5.2 High - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** gpt-5.2-high.txt
**Overall Score:** 4 / 6 (67%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
GPT 5.2 High was the top performer in the Alpha batch. It correctly identified modern LuCI JS architecture in Scenario 05, using `rpc.declare` to call `hostapd.wlan0 get_clients` — this is the CORRECT modern frontend pattern. Its procd init was flawless, its C handler perfect, and its `uci-defaults` properly included `exit 0`. It also notably used `jshn.sh` (a valid native OpenWrt tool) instead of `jq` or `awk` for JSON parsing, which while not uCode, is more "native" than `jsonfilter`. However, Scenarios 13 and 16 still fell back to shell-level tooling (jshn and `while read &` background jobs) instead of native `ucode`.

### New Truths Discovered
*   **`jshn.sh` as a valid intermediate pattern**: `jshn.sh` (`/usr/share/libubox/jshn.sh`) with `json_init`, `json_load`, `json_get_var` is a valid native OpenWrt JSON parsing API at the shell level. It is more "native" than `jsonfilter` but still not uCode.

### New Falsenesses Discovered
*   None new.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Excellent. `USE_PROCD=1`, `config_load` via `. /lib/functions.sh`, `config_get`, `procd_set_param respawn`.
*   **Scenario 05:** 1 (Pass) - **CORRECT modern pattern.** Used LuCI JS with `rpc.declare()` to call `hostapd.wlan0 get_clients`. Used `E()` DOM helper.
*   **Scenario 07:** 1 (Pass) - Correct C code. `blobmsg_add_string`, `ubus_send_reply`.
*   **Scenario 10:** 1 (Pass) - Perfect `uci-defaults` with `uci -q batch` and explicit `exit 0`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jshn.sh` shell library instead of native `ucode` `fs.readfile()` + `json()`. While `jshn` is native, it's not the modern `ucode` standard.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `while read` instead of `ucode` `uloop` async.
