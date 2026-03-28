# Qwen 3.5 Max Preview - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** qwen3.5-max-preview.txt
**Overall Score:** 2 / 6 (33%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Qwen 3.5 demonstrated correct procd and C ubus knowledge. Its init script was solid. Its C handler was correct. However, Scenario 10 omits `exit 0` — the script ends after `uci commit system` with no exit statement. Per the Golden Key, this means the `uci-defaults` framework cannot guarantee deletion. Scenario 05 used Lua `.htm` templates. Scenarios 13 and 16 used shell-level tooling.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   None new.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `config_get` using `@my_daemon[0]` syntax, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template with `luci.util` ubus wrapper.
*   **Scenario 07:** 1 (Pass) - Correct C code. Static `blob_buf`, `blobmsg_add_string`, `ubus_send_reply`.
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_MISSING_EXIT_0`. Script omits `exit 0`, relying on last command's exit code. The Golden Key requires explicit `exit 0`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` shell wrapper instead of native `ucode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `while read` instead of `ucode` `uloop` async.
