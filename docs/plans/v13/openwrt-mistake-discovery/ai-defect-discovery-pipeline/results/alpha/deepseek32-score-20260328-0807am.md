# DeepSeek V3 32B - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** deepseek32.txt
**Overall Score:** 2 / 6 (33%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
DeepSeek V3 32B showed decent procd and C ubus knowledge. However, it committed a critical error in Scenario 10 by creating a sentinel/marker file (`/etc/firstboot_completed`) along with a `touch` and `if` guard to track first-boot state. This is explicitly banned in the Golden Key as a "redundant marker file" pattern — the `uci-defaults` directory itself IS the state machine, and `exit 0` is all that's needed for auto-deletion. The script also omitted `exit 0`. Scenario 05 used deprecated Lua `.htm` templates. Scenario 13 preferenced `jq` over native tools and fell back to raw `awk` parsing. Scenario 16 used shell `&` background jobs.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   None new (marker file pattern already documented in Golden Key).

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `config_load`, `procd_set_param respawn`. Minor issues with `procd_kill` usage but core concept correct.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used deprecated Lua `.htm` template with server-side `ubus.connect()`.
*   **Scenario 07:** 1 (Pass) - Correct C code using `blobmsg_add_string` and `ubus_send_reply`.
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_ANTI_PATTERN`. Created redundant sentinel file `/etc/firstboot_completed` with `touch`. Also omitted `exit 0` from the script, preventing auto-deletion.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jq` (external binary) as primary parser and raw `awk` as fallback instead of native `ucode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used bash `&` background jobs instead of `ucode` `uloop` async.
