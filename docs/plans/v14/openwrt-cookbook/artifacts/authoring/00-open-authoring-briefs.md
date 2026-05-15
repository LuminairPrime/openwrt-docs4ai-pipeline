# Open Authoring Briefs

**Purpose:** Translate the admitted scenario packets into concrete authoring tasks for the live cookbook corpus.

Use these briefs with [08-cookbook-authoring-execution-contract.md](../../08-cookbook-authoring-execution-contract.md), not as standalone instructions.

---

## Shared Execution Contract

Before the creating agent drafts any cookbook page from this file, it must read all of:

1. the source packet named in the brief
2. the blind prompt or grouped prompt file for that scenario boundary
3. the frozen answer key for that scenario or grouped batch
4. at least one archived raw blind-failure response from `artifacts/results/` when the page is being authored as remediation work
5. the authority source files or URLs cited by the packet
6. the existing cookbook pages considered during the packet's coverage check

The creating agent must then:

- write the working draft to `artifacts/authoring/drafts/<slug>-draft.md`
- write the companion creation log to `artifacts/authoring/logs/<slug>-creation-log.md`
- keep the page scoped to the failure boundary rather than rewriting the full subsystem
- front-load the corrective pattern and wrong pattern in the draft overview
- record any token-budget exception in the creation log before promotion into `static/cookbook-source/`

> Token budget: target roughly 700 to 1400 tokens per page. If the page exceeds
> that range, record the reason in the creation log and follow the durable rules in
> [../../../../specs/cookbook-authoring-spec.md](../../../../specs/cookbook-authoring-spec.md).

---

## 1. ucode Async Process Pattern

- Target page: `static/cookbook-source/ucode-async-process-pattern.md`
- Draft path: `artifacts/authoring/drafts/ucode-async-process-pattern-draft.md`
- Creation log: `artifacts/authoring/logs/ucode-async-process-pattern-creation-log.md`
- Source packet: `artifacts/scenario-packets/01-scn-2026-001-ucode-async-ping-streams.yaml`
- Publication shape: new standalone page
- Must teach:
  - `fs.popen()` as the process launch boundary
  - `uloop.handle(..., uloop.ULOOP_READ)` as the monitoring boundary
  - incremental `read("line")` consumption
  - why shell `&` and FIFO fan-in are the wrong abstraction
- Done when:
  - the page has one complete working example
  - verification notes cite the packet and current evidence sources
  - the page can serve as the remediation target for Scenario 16

## 2. ucode Native File IO and JSON

- Target page: `static/cookbook-source/ucode-native-file-io-and-json.md`
- Draft path: `artifacts/authoring/drafts/ucode-native-file-io-and-json-draft.md`
- Creation log: `artifacts/authoring/logs/ucode-native-file-io-and-json-creation-log.md`
- Source packet: `artifacts/scenario-packets/02-scn-2026-002-ucode-native-json-file-read.yaml`
- Publication shape: new standalone page
- Must teach:
  - `fs.readfile()` for native reads
  - `json()` for native parsing
  - explicit separation of file-read, parse, and missing-key failures
  - why `jq`, `jsonfilter`, and shell parsing are wrong inside ucode
- Done when:
  - the page clearly distinguishes this boundary from UCI mutation
  - verification notes cite the packet and current evidence sources
  - the page can serve as the remediation target for Scenario 13

## 3. C libubus Daemon Skeleton

- Target page: `static/cookbook-source/c-libubus-daemon-runtime-pattern.md`
- Draft path: `artifacts/authoring/drafts/c-libubus-daemon-skeleton-draft.md`
- Creation log: `artifacts/authoring/logs/c-libubus-daemon-skeleton-creation-log.md`
- Source packet: `artifacts/scenario-packets/03-scn-2026-003-c-libubus-daemon-skeleton.yaml`
- Publication shape: new standalone page
- Must teach:
  - `uloop_init()` before `ubus_connect()`
  - `ubus_add_uloop()` before `uloop_run()`
  - why `sleep()` loops and generic daemon patterns are wrong here
  - where this stops and more advanced object registration begins
- Done when:
  - the page demonstrates the minimal working startup contract
  - verification notes cite the packet and current evidence sources
  - the page can serve as the remediation target for Scenario 12

## 4. procd `uci_load_validate` Treatment

- Target page: `static/cookbook-source/procd-service-lifecycle.md`
- Draft path: `artifacts/authoring/drafts/procd-service-lifecycle-draft.md`
- Creation log: `artifacts/authoring/logs/procd-service-lifecycle-creation-log.md`
- Source packet: `artifacts/scenario-packets/04-scn-2026-004-procd-uci-load-validate-loglevel.yaml`
- Publication shape: extend existing page
- Must teach:
  - the call shape of `uci_load_validate`
  - how validation and `config_foreach` pair together
  - when to use `procd_add_validation`
  - why parsing `/etc/config/*` with grep or regex is the wrong boundary
- Done when:
  - the page contains a focused validation section with a complete code example
  - verification notes cite the packet and current evidence sources
  - the page can serve as the remediation target for Scenario 01 and Scenario 06
