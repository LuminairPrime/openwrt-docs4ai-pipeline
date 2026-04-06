# Alpha Batch Answer Key

**Batch:** `01a-batch-alpha.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 01, 03, 04

---

## Scenario 01 — Procd Daemon & Config Validation

**PASS criteria:**

- Must use OpenWrt procd service structure with `USE_PROCD=1`.
- Must start the daemon through procd instance setup rather than a manual background job.
- Must fetch configuration through `uci_load_validate` instead of direct file scraping.

**Immediate fails:**

- `systemd`, generic LSB init, or manual PID-file watchdog logic.
- Parsing `/etc/config/my_daemon` with `cat`, `grep`, `awk`, or similar text slicing.

---

## Scenario 03 — C libubus Plugin

**PASS criteria:**

- Must include `libubus` usage, including `#include <libubus.h>`.
- Must register the object through the real OpenWrt ubus object-registration path such as `ubus_add_object()`.
- Must stay inside the libubus plugin model rather than inventing a custom IPC layer.

**Immediate fails:**

- Bypassing ubus with raw sockets or a custom RPC transport.
- Fabricated ubus registration APIs.

---

## Scenario 04 — LuCI JS Dynamic Form

**PASS criteria:**

- Must use the modern LuCI JavaScript view architecture.
- Must build the configuration UI around `form.Map` and related LuCI JS widgets.
- Must use a native LuCI/OpenWrt dynamic interface selector rather than a hand-maintained static dropdown.

**Immediate fails:**

- Raw handwritten HTML form markup as the main solution.
- Legacy Lua CBI or non-LuCI frontend frameworks.