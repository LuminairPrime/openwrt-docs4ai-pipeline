# Hearth - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** hearth.txt
**Overall Score:** 3 / 6 (50%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Hearth demonstrated strong awareness of OpenWrt patterns and explicitly acknowledged the modern JS vs legacy Lua debate in its reasoning. It consciously chose the Lua template path "because it's still supported and needs no build step" — showing it knew the correct answer but deliberately chose the legacy approach. The procd init script and C handler were both excellent. The `uci-defaults` answer correctly used `uci -q batch` and `exit 0`. However, Scenarios 05, 13, and 16 all used legacy patterns.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   None new.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `config_get`, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template with `ubus:objects()` iteration. Consciously chose legacy approach.
*   **Scenario 07:** 1 (Pass) - Correct C code. `blobmsg_add_string`, `ubus_send_reply`, `blob_buf_free`, `UBUS_METHOD_NOARG`.
*   **Scenario 10:** 1 (Pass) - Perfect `uci-defaults` with `uci -q batch` and explicit `exit 0`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` shell wrapper instead of native `ucode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `sed -u` instead of `ucode` `uloop` async.
