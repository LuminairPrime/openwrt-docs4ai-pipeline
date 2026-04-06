# Beta Batch Answer Key

**Batch:** `01b-batch-beta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 02, 06, 09

---

## Scenario 02 — uCode Network Interfaces

**PASS criteria:**

- Must use native ucode ubus access.
- Must explicitly import the ubus module and connect via `ubus.conn()`.
- Must treat OpenWrt network state as ubus data, not as shell-parsed command output.

**Immediate fails:**

- Shell wrappers around `ubus call ... | jsonfilter`.
- Raw `ip`, `/sys/class/net`, or `jq` parsing as the main boundary.

---

## Scenario 06 — Procd Validation Function

**PASS criteria:**

- Must use `uci_load_validate` for the validation boundary.
- Must keep the validation inside the OpenWrt init/procd model rather than a generic ad hoc shell validator.

**Immediate fails:**

- Custom regex or text parsing of `/etc/config/*`.
- Generic shell validation detached from the procd/UCI context.

---

## Scenario 09 — Hotplug.d Event Trigger

**PASS criteria:**

- Must be a hotplug event script using the environment pushed by hotplug.
- Must read `$ACTION` and `$INTERFACE` and gate behavior on them.
- Must rely on the event-driven boundary rather than polling.

**Immediate fails:**

- Cron, `while true`, or manual interface polling.
- Ignoring the hotplug environment and restarting on every invocation.