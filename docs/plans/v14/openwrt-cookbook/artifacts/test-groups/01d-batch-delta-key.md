# Delta Batch Answer Key

**Batch:** `01d-batch-delta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 08, 11, 12

---

## Scenario 08 — uCode UCI Modification

**PASS criteria:**

- Must use native ucode UCI access.
- Must import the uci module and use cursor methods such as `set()`, `save()`, and `commit()`.
- Must treat this as UCI mutation, not raw file editing.

**Immediate fails:**

- Writing directly into `/etc/config/network`.
- Shell `uci` command snippets in place of native ucode when the prompt boundary is already ucode.

---

## Scenario 11 — C Package Makefile

**PASS criteria:**

- Must be an OpenWrt package Makefile, not a generic C project Makefile.
- Must include `$(TOPDIR)/rules.mk` and `$(INCLUDE_DIR)/package.mk`.
- Must declare the libubus dependency through `DEPENDS:=+libubus`.

**Immediate fails:**

- Plain gcc/cmake build files without OpenWrt package DSL.
- Missing OpenWrt dependency declaration.

---

## Scenario 12 — C uloop Initialization

**PASS criteria:**

- Must initialize `uloop`.
- Must connect to ubus with `ubus_connect()` and attach it to the event loop with `ubus_add_uloop()`.
- Must block in `uloop_run()` as the main runtime loop.

**Immediate fails:**

- `sleep()` polling loops.
- Invented OpenWrt event-loop APIs.
