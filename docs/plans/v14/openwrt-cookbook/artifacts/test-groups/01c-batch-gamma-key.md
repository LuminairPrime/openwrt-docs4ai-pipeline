# Gamma Batch Answer Key

**Batch:** `01c-batch-gamma.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 07, 05, 10

---

## Scenario 07 — C ubus RPC Handler

**PASS criteria:**

- Must build the reply with `struct blob_buf` and blobmsg helpers.
- Must add the `status` field through blobmsg helpers such as `blobmsg_add_string()`.
- Must return the reply with `ubus_send_reply()`.

**Immediate fails:**

- Raw JSON string assembly in C.
- `printf`-style output in place of a ubus reply object.

---

## Scenario 05 — LuCI JS Live Status Table

**PASS criteria:**

- Must use LuCI JS runtime helpers such as `rpc.declare()` and `L.resolveDefault`.
- Must build the rendered table through LuCI DOM helpers such as `E('table')`.
- Must fetch live system data over ubus instead of inventing an external REST layer.

**Immediate fails:**

- Raw `fetch()` or `XMLHttpRequest` as the main system-data path.
- Static HTML table without a runtime ubus-backed data source.

---

## Scenario 10 — UCI Defaults First-Boot

**PASS criteria:**

- Must place the script in `/etc/uci-defaults/`.
- Must mutate UCI state and finish with `exit 0` so the framework deletes the script.
- Must describe it as a first-boot mutation boundary, not as a normal service lifecycle script.

**Immediate fails:**

- `/etc/init.d/` placement.
- Sentinel files, marker files, or manual self-removal logic.
- Starting or reloading services directly from the `uci-defaults` script.