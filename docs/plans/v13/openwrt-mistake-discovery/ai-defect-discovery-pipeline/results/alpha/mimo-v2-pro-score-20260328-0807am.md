# Mimo v2 Pro - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** mimo-v2-pro.txt
**Overall Score:** 1 / 6 (17%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Mimo v2 Pro showed significant architectural misunderstanding. The procd init script was correct (Scenario 01 passes). However, Scenario 07 used `json-c` (`json_object_new_object`, `json_object_to_json_string`) to build a JSON string and then used `blobmsg_add_json_from_string()` to double-wrap it — this is explicitly the wrong pattern per the Golden Key (building raw JSON strings manually). Scenario 10 created a sentinel file (`/etc/first_boot_done`) and omitted `exit 0`. Scenario 05 used Lua `.htm` templates. Scenario 13 preferenced `jq` over native tools. Scenario 16 used FIFOs with background jobs.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   **`blobmsg_add_json_from_string()` pattern**: Building a JSON string with `json-c` and then calling `blobmsg_add_json_from_string()` to inject it into a blob buffer is a double-wrapping anti-pattern. The correct approach is individual `blobmsg_add_*` calls.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `config_get`, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template.
*   **Scenario 07:** 0 (Fail) - Taxonomy: `ERR_RAW_JSON_BUILD`. Used `json-c` (`json_object_new_object` + `json_object_to_json_string`) then `blobmsg_add_json_from_string()` — builds raw JSON string instead of using `blobmsg_add_string` directly.
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_ANTI_PATTERN`. Created sentinel file `/etc/first_boot_done`. Also omitted `exit 0`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Preferenced `jq` as primary parser, `jsonfilter` only as fallback.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used FIFOs (`mkfifo`) with background jobs instead of `ucode` `uloop` async.
