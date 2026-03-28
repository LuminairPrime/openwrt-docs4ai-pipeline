# Minimax m2.7 - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** minimax-m2.7.txt
**Overall Score:** 2 / 6 (33%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Minimax showed solid procd knowledge and correct C ubus handler. However, Scenario 10 committed two errors: it manually calls `rm -f` on itself AND omits `exit 0`, relying on the `rm` approach instead of the framework's self-cleaning contract. Without `exit 0`, even if the file is deleted, the contract is broken. Scenario 05 used Lua `.htm` templates. Scenario 13 used `jshn.sh` (a valid tool but not uCode). Scenario 16 used shell `&` background jobs.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   None new.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `config_get`, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template with server-side `ubus.connect()`. Called incorrect ubus path `wifi status` instead of `network.wireless status`.
*   **Scenario 07:** 1 (Pass) - Correct C code. `blobmsg_add_string`, `ubus_send_reply`, `blob_buf_free`, `ubus_add_object`.
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_MISSING_EXIT_0`. Script omits `exit 0` and instead uses manual `rm -f` to self-delete. The `uci-defaults` framework requires `exit 0` for its deletion contract.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jshn.sh` shell library instead of native `ucode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `while read` instead of `ucode` `uloop` async.
