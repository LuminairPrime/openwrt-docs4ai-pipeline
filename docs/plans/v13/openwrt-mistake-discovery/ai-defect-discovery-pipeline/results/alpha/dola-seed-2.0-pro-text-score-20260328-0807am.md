# Dola Seed 2.0 Pro Text - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** dola-seed-2.0-pro-text.txt
**Overall Score:** 2 / 6 (33%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Dola Seed demonstrated solid procd, C, and shell JSON parsing knowledge. Its Scenario 01 was correctly structured with `USE_PROCD=1`. Its C handler in Scenario 07 was canonical. The `jsonfilter` usage in Scenario 13 was correct at the shell level (though not uCode). However, the critical failure was in Scenario 10: the script omitted `exit 0`, which per the Golden Key means the `uci-defaults` framework will NOT delete the script and it will re-execute on every boot. Scenario 05 used deprecated Lua `.htm` template. Scenario 16 used shell `&` and `sed -u` background jobs.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   None new.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `config_get`, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template with embedded server-side Lua and `ubus.connect()`.
*   **Scenario 07:** 1 (Pass) - Correct C code. `blobmsg_add_string`, `ubus_send_reply`. Clean implementation.
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_MISSING_EXIT_0`. Script is missing `exit 0` at the end, preventing correct auto-deletion by the `uci-defaults` framework.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` bash wrapper instead of native `ucode` `fs.readfile()` + `json()`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `sed -u` instead of `ucode` `uloop` async.
