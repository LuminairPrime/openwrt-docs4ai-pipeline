# Significant Otter - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** significantotter.txt
**Overall Score:** 1 / 6 (17%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Significant Otter showed strong reasoning about modern vs legacy LuCI architecture. Its Scenario 05 was the most interesting: it used client-side JavaScript with `L.ready()` and `L.rpc.call()` which is a valid modern LuCI pattern. However, the specific API call `L.rpc.call('network', 'get_wireless_clients', {})` is not a real ubus method — it should be `rpc.declare({object:'hostapd.wlan0', method:'get_clients'})`. The `L.rpc.call` syntax used here is also not the standard `rpc.declare` pattern required by the Golden Key for Scenario 05. So this is a **near-miss** but still fails. Scenario 10 omits `exit 0` and creates an unnecessary symlink to `/usr/share/zoneinfo/UTC`. Scenarios 13 and 16 used shell-level tooling.

### New Truths Discovered
*   **`L.ready()` + `L.rpc.call()` as a valid LuCI JS entry point**: While the specific API call was wrong, the JavaScript architectural approach using `L.ready()` shows awareness of the modern LuCI JS runtime.

### New Falsenesses Discovered
*   **Non-existent ubus methods**: `network.get_wireless_clients` is not a real ubus method. This reveals a common AI pattern of inventing plausible-sounding but fictitious API endpoints.

## Scenario Breakdown
*   **Scenario 01:** 1 (Pass) - Correct `USE_PROCD=1`, `uci -q get` for config, `procd_set_param respawn`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `L.rpc.call` (non-standard) with a fabricated method name `get_wireless_clients`. Should use `rpc.declare` with real ubus objects.
*   **Scenario 07:** 0 (Fail) - Taxonomy: `ERR_API_MISMATCH`. Used incorrect function signatures (`struct ubus_request *req` instead of `struct ubus_request_data *req`), `BLOB_BUF_INIT(0)` macro (doesn't exist), `ubus_send_reply(req, &b.buf)` (wrong arguments), `blobmsg_free` (not the correct cleanup function), and `UBUS_METHOD_BUF` (doesn't exist).
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_MISSING_EXIT_0`. Script omits `exit 0`. Also creates unnecessary symlink to `/usr/share/zoneinfo/UTC`.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used `jsonfilter` shell wrapper instead of native `ucode`. Also has incorrect invocation syntax (missing `-i` flag).
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used shell `&` background jobs with `while read` instead of `ucode` `uloop` async.
