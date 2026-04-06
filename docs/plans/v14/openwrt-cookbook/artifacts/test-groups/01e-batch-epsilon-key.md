# Epsilon Batch Answer Key

**Batch:** `01e-batch-epsilon.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 13, 14, 19

---

## Scenario 13 — uCode Native fs/json Parsing

**PASS criteria:**

- Must read the file with native ucode file I/O such as `fs.readfile()`.
- Must parse the JSON with native ucode `json(...)`.
- Must keep this boundary in ucode rather than escaping into shell helpers.

**Immediate fails:**

- `jq`, `jsonfilter`, `jshn`, `grep`, `awk`, or `sed` as the main parsing path.
- Shell wrappers around the JSON file when the prompt is already inside ucode.

---

## Scenario 14 — LuCI JSON Menu Router

**PASS criteria:**

- Must register the node through the modern LuCI JSON menu system.
- Must include the key fields `title`, `action`, and `type: "view"`.
- Must place the definition in the LuCI JSON menu boundary rather than a legacy Lua controller.

**Immediate fails:**

- `index.lua` / dispatcher-Lua registration.
- Wrong menu directory or a noncanonical action/type structure.

---

## Scenario 19 — Hotplug Guarded ubus Forward

**PASS criteria:**

- Must guard on hotplug environment variables such as `$ACTION` and `$INTERFACE`.
- Must build a structured payload and forward it with `ubus call`.
- Must treat the script as event-driven hotplug logic rather than a generic monitoring script.

**Immediate fails:**

- Polling loops or cron-based monitoring.
- No early-exit guards for unrelated hotplug events.
