# Batch 01i Answer Key

**Batch:** `01i.md`
**Type:** Canonical cookbook-center answer key
**Scenarios:** 26, 27, 17

---

## Scenario 26 — Shell jshn Native JSON

**PASS criteria:**

- Must source `/usr/share/libubox/jshn.sh`.
- Must use native jshn helpers such as `json_load`, `json_select`, and `json_get_vars`.
- Must navigate back out cleanly with `json_select ..`.

**Immediate fails:**

- `jq` or `jsonfilter` as the main parsing path.
- Ad hoc string parsing of JSON.

---

## Scenario 27 — netifd Runtime State Shape

**PASS criteria:**

- Must call `network.interface` / `dump` through `rpc.declare()`.
- Must expect an `interface` array in the reply.
- Must treat `ipv4-address` as an array of objects and extract the `address` field.

**Immediate fails:**

- Treating the IPv4 value as a flat string.
- Using the wrong ubus object or method.

---

## Scenario 17 — Diagnostic Check

**PASS criteria:**

- Must identify `ucode` as the lightweight modern scripting language replacing Lua in major current-era OpenWrt surfaces.
- Must describe it as C-backed with JavaScript-like syntax and good fit for OpenWrt runtime tasks.

**Immediate fails:**

- Treating `ucode` as unrelated to OpenWrt runtime scripting.
- Claiming Lua remains the modern flagship framework for those same current surfaces.
