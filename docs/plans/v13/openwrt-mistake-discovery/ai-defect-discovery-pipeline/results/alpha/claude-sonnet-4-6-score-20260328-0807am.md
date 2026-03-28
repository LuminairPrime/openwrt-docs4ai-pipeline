# Claude Sonnet 4.6 - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** claude-sonnet-4-6.txt
**Overall Score:** 3 / 6 (50%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Claude Sonnet produced the most verbose and well-documented outputs in the batch. Its procd init script was excellent, and it provided one of the most thorough C ubus handler implementations. The `uci-defaults` answer was correct with explicit `exit 0`. However, Scenario 05 used deprecated Lua `.htm` templates with server-side `ubus.connect()` instead of modern LuCI JS with `rpc.declare`. Scenarios 13 and 16 both used legacy shell approaches: `jsonfilter` instead of `ucode` for JSON parsing, and FIFOs with background `&` jobs instead of `ucode` `uloop` async. The FIFO approach in Scenario 16 was technically interesting but architecturally wrong for modern OpenWrt.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   **FIFO-based parallel processing**: Using `mkfifo` named pipes with `while read` loops is another variant of the "Shell Hacks" pattern banned under Universal General Falseness § Asynchronous Logic.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Excellent. `USE_PROCD=1`, `config_load`, `config_get`, `procd_set_param respawn`, `service_triggers`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua CBI `.htm` template with server-side `ubus.connect()` instead of LuCI JS `rpc.declare`.
*   **Scenario 07:** 1 (Pass) - Outstanding C code. Correct `blobmsg_add_string`, `ubus_send_reply`, `UBUS_METHOD_NOARG` registration.
*   **Scenario 10:** 1 (Pass) - Perfect `uci-defaults` placement with explicit `exit 0`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` bash wrapper instead of native `ucode` `fs.readfile()` + `json()`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used FIFOs (`mkfifo`) and `while read` background loops instead of `ucode` `uloop` async.
