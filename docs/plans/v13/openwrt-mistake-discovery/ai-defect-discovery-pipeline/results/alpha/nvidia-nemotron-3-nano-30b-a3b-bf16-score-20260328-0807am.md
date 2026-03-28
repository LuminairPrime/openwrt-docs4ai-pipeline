# Nvidia Nemotron 3 Nano 30B - Alpha Batch Evaluation

**Date:** 2026-03-28
**Batch Evaluated:** 01a-batch-slice-alpha.md
**Raw Output File:** nvidia-nemotron-3-nano-30b-a3b-bf16.txt
**Overall Score:** 0 / 6 (0%)

## Evaluation Methodology (Concept-by-Concept)
Strict adherence to the `03-golden-answers-key.md` falsification rules. Any architectural "strike" resulted in an immediate 0 for the scenario.

## Conversational Synthesis & Findings
Nvidia Nemotron demonstrated catastrophic architectural misunderstanding of modern OpenWrt across every scenario. **Scenario 01** used a SysVinit-style `start()` function with `my_daemon &` background launching and PID file management — this is the exact anti-pattern banned by the Golden Key's Universal General Falseness. No `USE_PROCD=1`. **Scenario 05** used raw `XMLHttpRequest` to a non-existent `/ubus` HTTP endpoint. **Scenario 07** used completely fabricated APIs (`ubus_request_set_result`, `ubus_add_workhandler`, manual `strdup(json)` of a raw JSON string). **Scenario 10** used `/etc/rc.local` with a `/tmp` lockfile — explicitly rejecting the existence of `uci-defaults`. **Scenario 13** correctly identified `jsonfilter` but the script has syntax errors. **Scenario 16** used `stdbuf -oL` which is not available on stock OpenWrt.

### New Truths Discovered
*   None new.

### New Falsenesses Discovered
*   **Fabricated ubus API functions**: `ubus_request_set_result()`, `ubus_add_workhandler()`, `ubus_request_set_error()` — these functions do not exist in the real libubus API. This is a hallucination pattern.
*   **PID file management in init scripts**: Using `echo $! > /var/run/my_daemon.pid` and `cat /var/run/my_daemon.pid` for daemon management is a SysVinit-era pattern completely replaced by procd supervision.
*   **`/tmp` lockfile for first-boot**: Using `/tmp/.first_boot_tz_done` as a lockfile to prevent re-execution is exactly the pattern `uci-defaults` was designed to replace. `/tmp` is cleared on every reboot, so the script would run on EVERY boot, never just "first boot."

## Scenario Breakdown
*   **Scenario 01:** 0 (Fail) - Taxonomy: `ERR_INIT_SYSTEM`. No `USE_PROCD=1`. Used SysVinit `start()`/`stop()` with `my_daemon &` and PID file. Named script `S99my_daemon`.
*   **Scenario 05:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. Used raw `XMLHttpRequest` to non-existent `/ubus` endpoint. Not a LuCI view at all — standalone HTML page.
*   **Scenario 07:** 0 (Fail) - Taxonomy: `ERR_RAW_JSON_BUILD`. Built raw JSON string `"{\"status\":\"ok\"}"` via `strdup()`. Used fabricated API functions (`ubus_request_set_result`, `ubus_add_workhandler`).
*   **Scenario 10:** 0 (Fail) - Taxonomy: `ERR_INIT_SYSTEM`. Used `/etc/rc.local` with `/tmp` lockfile. Explicitly stated "OpenWrt provides no built-in 'run-once' hook" — factually wrong, `uci-defaults` exists.
*   **Scenario 13:** 0 (Fail) - Taxonomy: `ERR_LEGACY_API`. While it identified `jsonfilter`, the script has syntax errors (`exit 1fi` without linebreak). Not native `ucode`.
*   **Scenario 16:** 0 (Fail) - Taxonomy: `ERR_NON_CANONICAL`. Used `stdbuf -oL` (not available on stock OpenWrt) and shell `&` background jobs. Also incorrectly placed script as `/etc/init.d/S99dual_ping`.
