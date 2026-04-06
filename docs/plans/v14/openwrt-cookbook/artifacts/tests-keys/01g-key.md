# Batch 01g Answer Key

**Batch:** `01g.md`
**Type:** Canonical cookbook-center answer key
**Scenarios:** 16, 21, 23

---

## Scenario 16 — uCode Parallel Async Ping

**PASS criteria:**

- Must use the native ucode async runtime boundary such as `uloop` plus asynchronous process handles.
- Must run both ping commands in parallel rather than serially.
- Must stream output live with per-target identification.

**Immediate fails:**

- Bash background jobs with `&`, FIFOs, or manual shell multiplexing.
- Sequential ping execution.

---

## Scenario 21 — ucidef Helper Boundary

**PASS criteria:**

- Must source `/lib/functions/uci-defaults.sh`.
- Must use a helper such as `ucidef_set_interface_wan()`.
- Must treat this as a board-default helper boundary, not raw UCI mutation.

**Immediate fails:**

- Handwritten `uci set network.wan...` commands.
- Using the wrong helper library.

---

## Scenario 23 — Package Install Layout

**PASS criteria:**

- Must use an OpenWrt `Package/.../install` block.
- Must place the LuCI view, ACL, rpcd helper, config file, and `uci-defaults` script into correct package destinations.
- Must cover runtime install layout, not only compile boilerplate.

**Immediate fails:**

- Repeating only the compile-oriented Makefile structure from Scenario 11.
- Generic Linux install logic outside the OpenWrt package DSL.
