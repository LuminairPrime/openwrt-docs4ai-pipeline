# Hearth - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** hearth.txt
**Overall Score:** 3 / 6 (50%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Hearth identifies as a "Classic" OpenWrt developer. It correctly implements `procd`, `uci-defaults`, and `libubus`, but consciously decides against modern LuCI JS and `uCode`, opting for legacy Lua templates and `jsonfilter`. While it reasons through these choices well, they fail the modern Docs4AI standard which prioritizes the current `uCode` ecosystem.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct execution using `USE_PROCD=1` and `config_load`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used legacy LuCI Lua templates instead of modern LuCI JS `rpc.declare`.
*   **Scenario 07:** 1 (Pass) - Correct C code using `blobmsg_add_string`.
*   **Scenario 10:** 1 (Pass) - Perfect use of `/etc/uci-defaults/` and `exit 0`. 
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` instead of native `uCode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell backgrounding jobs instead of `uloop` within `uCode`.
