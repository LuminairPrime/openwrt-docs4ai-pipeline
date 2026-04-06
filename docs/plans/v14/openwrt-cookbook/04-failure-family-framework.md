# Failure Family Framework

**Purpose:** Define the programming-family layer that sits between raw blind failures and cookbook publication decisions.

---

## 1. Why Families Exist

The same OpenWrt lesson can fail in many different surface forms.

Examples:

- writing a SysV-style init script
- managing a daemon with a PID file
- adding a manual watchdog loop

These are different wrong snippets, but they all reveal the same family-level mistake:

> applying generic Linux service supervision habits where OpenWrt expects procd.

Without families, the system creates too many pages and too many duplicated tests.

---

## 2. Family Hierarchy

Use this four-level model.

```text
Programming domain
  -> OpenWrt boundary
    -> Failure family
      -> Concrete falseness or repeated wrong pattern
```

Example:

```text
Service lifecycle
  -> OpenWrt init and supervision
    -> FAM-INIT-PROCD
      -> missing USE_PROCD=1
      -> PID file management
      -> manual watchdog loop
```

---

## 3. Family List For The Current System

| Family ID | Programming family | OpenWrt boundary | Typical wrong outputs |
| --- | --- | --- | --- |
| `FAM-ERA` | Era mismatch | Current vs legacy OpenWrt patterns | Lua CBI for new LuCI work, swconfig assumptions, pre-ucode habits |
| `FAM-INIT-PROCD` | Service lifecycle | procd init and supervision | generic init scripts, PID files, manual restarts |
| `FAM-UCI-PERSISTENCE` | Config storage and persistence | UCI instead of ad hoc file mutation | editing `/etc/config` directly, missing commit/save |
| `FAM-FIRSTBOOT` | One-shot boot sequencing | `uci-defaults` and first-boot mutation | sentinel files, service orchestration inside `uci-defaults`, missing `exit 0` |
| `FAM-HOTPLUG-EVENTS` | Event-driven shell behavior | hotplug environment and event taxonomy | polling loops, ignoring `$ACTION`, side effects on unrelated events |
| `FAM-UBUS-SURFACES` | IPC and runtime state | ubus-first service and identity surfaces | ad hoc sockets, direct shell-out state duplication, wrong runtime identity surface |
| `FAM-LUCI-JS` | Frontend architecture | modern LuCI JS runtime | Lua CBI, raw HTML forms, raw fetch instead of `rpc.declare`, missing `L.ui` patterns |
| `FAM-UCODE-NATIVE` | Native scripting runtime | ucode modules, file I/O, JSON, and runtime model | `require()`, shell parsing, `jq`, invented APIs |
| `FAM-UCODE-ASYNC` | Async scripting | `uloop` and async process handling | shell `&`, FIFO hacks, missing `uloop.ULOOP_READ` |
| `FAM-C-LIBUBUS` | C daemon and RPC contracts | `libubus`, `libubox`, `blobmsg`, `uloop` | raw JSON strings, missing `blobmsg_parse`, missing `ubus_add_uloop()` |
| `FAM-BUILDROOT` | Packaging and build | OpenWrt package Makefile contract | generic `Makefile`, missing `rules.mk`, missing `DEPENDS` |

---

## 4. Family Matching Rules

Match failures to the same family when all of the following are true.

1. the same corrective lesson would fix them
2. the same cookbook destination would likely teach them
3. the same authority source family underlies the correction

Open a new family when the wrong outputs look similar but the corrective lesson is materially different.

---

## 5. Family Severity

Families can be prioritized by severity.

| Severity | Meaning |
| --- | --- |
| Structural | A foundational OpenWrt boundary is being missed; one failure is enough to justify serious cookbook attention |
| Operational | The lesson affects common real-world OpenWrt work but may be narrower |
| Idiomatic | The lesson is still useful, but is more about current best practice than architectural correctness |

Examples:

- `FAM-INIT-PROCD`: Structural
- `FAM-UCODE-ASYNC`: Structural
- `FAM-LUCI-JS`: Structural
- `FAM-BUILDROOT`: Operational

---

## 6. Family Confidence States

| State | Meaning |
| --- | --- |
| Seed | One blind failure opened the family |
| Confirmed | Multiple failures, multiple sources, or strong cross-scenario breadth confirm it |
| Settled | A cookbook page exists and the family has entered verification or benchmark use |

The system allows a **seed** family to open cookbook work. Confirmation only changes priority and publishing confidence.

---

## 7. Family To Cookbook Mapping Rules

Possible mappings:

- one family -> extend one existing page
- one family -> new standalone page
- several families -> one umbrella page

Examples:

- `FAM-FIRSTBOOT` may map to `firstboot-uci-defaults-pattern.md` and `firstboot-wifi-policy.md`
- `FAM-LUCI-JS` may map to `luci-form-with-uci.md` or a future dedicated live-status / widget page
- `FAM-UCODE-ASYNC` likely deserves its own page if not covered strongly elsewhere

---

## 8. Minimal Family Record

Every family tracked by the operator should at least record:

- family ID
- short definition
- severity
- confidence state
- first triggering scenario
- authority source set
- current cookbook destination
- current status

Suggested status values:

- open
- merged
- covered by existing page
- new page needed
- authored pending verification
- benchmark-only

The seeded machine-readable registry for this prototype lives at [artifacts/registry/00-failure-family-registry.seed.yaml](./artifacts/registry/00-failure-family-registry.seed.yaml).

---

## 9. Seeded Registry Usage

The seeded registry is not the final ontology for all future cookbook work. It is the first practical working set derived from the strongest currently documented v13 findings.

Use it to:

- map new failures onto existing families before creating new ones
- see which families are already covered by live cookbook pages
- identify which families still have open documentation or verification gaps
- keep later family additions structurally consistent with the current prototype

Record mutable operator workflow state in [artifacts/registry/01-failure-family-registry.live.yaml](./artifacts/registry/01-failure-family-registry.live.yaml) rather than rewriting the seed file.


