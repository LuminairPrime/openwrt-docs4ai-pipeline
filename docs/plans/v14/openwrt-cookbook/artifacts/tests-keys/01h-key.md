# Batch 01h Answer Key

**Batch:** `01h.md`
**Type:** Canonical cookbook-center answer key
**Scenarios:** 22, 24, 25

---

## Scenario 22 — C blobmsg Parse Plus Nested Reply

**PASS criteria:**

- Must define a `blobmsg_policy` array and parse input with `blobmsg_parse()`.
- Must build a typed nested reply with blobmsg structures such as `blobmsg_open_table()`.
- Must send the reply through `ubus_send_reply()`.

**Immediate fails:**

- Raw pointer casting or raw JSON string construction.
- Solving only the parse half or only the reply half of the contract.

---

## Scenario 24 — rpcd ACL Silent-Failure Contract

**PASS criteria:**

- Must provide an ACL JSON file with explicit `read` and `write` sections.
- Must grant permissions through a `ubus` map.
- Must state that the file belongs under `/usr/share/rpcd/acl.d/<name>.json`.

**Immediate fails:**

- Claiming frontend code alone grants permission.
- Omitting the install path.
- Returning a UCI ACL example instead of rpcd/ubus permissions.

---

## Scenario 25 — Shell Config Helper API

**PASS criteria:**

- Must source `/lib/functions.sh`.
- Must use `config_load`, `config_get`, `config_get_bool`, and `config_list_foreach`.
- Must treat the problem as a shell helper-API boundary rather than raw file parsing.

**Immediate fails:**

- `grep`, `awk`, or `sed` over `/etc/config/network`.
- Replacing the helper API with raw `uci get` calls.
