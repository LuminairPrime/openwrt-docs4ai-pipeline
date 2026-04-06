# Zeta Batch Answer Key

**Batch:** `01f-batch-zeta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 15, 18, 20

---

## Scenario 15 — C blobmsg Dictionary Parsing

**PASS criteria:**

- Must parse the input through a declared `blobmsg_policy` array.
- Must call `blobmsg_parse()` over the incoming blob message.
- Must treat the data as blobmsg attributes rather than raw memory.

**Immediate fails:**

- Blind pointer casting of message memory.
- Ad hoc parsing without the blobmsg policy/parse boundary.

---

## Scenario 18 — LuCI JS Async Status Form Lifecycle

**PASS criteria:**

- Must define a LuCI `rpc.declare()` call for the live status surface.
- Must load live RPC data in `load()` and pass resolved data into `render()`.
- Must render the page as a modern LuCI JS `form.Map` view.

**Immediate fails:**

- Issuing live RPC calls directly inside `render()`.
- Raw `fetch()` or non-LuCI runtime networking.

---

## Scenario 20 — uci-defaults Mutation Only

**PASS criteria:**

- Must live in `/etc/uci-defaults/`.
- Must mutate UCI state, commit it, and end with `exit 0`.
- Must not start, reload, or otherwise manage a service lifecycle from this script.

**Immediate fails:**

- Calling `/etc/init.d/...` from inside the script.
- Marker files or sentinel-state logic.
