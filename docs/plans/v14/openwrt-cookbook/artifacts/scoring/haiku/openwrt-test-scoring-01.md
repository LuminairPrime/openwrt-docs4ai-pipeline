# OpenWrt Cookbook Test Scoring Report

**Test Suite:** OpenWrt Development Tests (01a-01i)  
**Scoring Method:** INCORRECTNESS-based (counting definite failures only)  
**Score Criteria:** Count failures where "Immediate fails" criteria are clearly violated  
**Date:** April 6, 2026

---

## Summary Scorecard

| Test-Taker | Total Tests | Total Failures | Failure Rate | Grade |
|------------|-------------|----------------|--------------|-------|
| big-pickle | 9 | 3 | 33% | C |
| dola-seed-20-pro | 9 | 2 | 22% | B |
| gemini-3-flash | 9 | 2 | 22% | B |
| grok-code-fast-1-optimized | 9 | 2 | 22% | B |
| haiku-46 | 9 | 2 | 22% | B |
| minimax-m25 | 0 | --- | --- | NO RESULTS |
| nemotron-3-super-120b | 9 | 2 | 22% | B |
| qwen-36-plus | 9 | 4 | 44% | D |
| raptor-mini | 9 | 2 | 22% | B |

**Test Completion:** 8 of 9 test-takers provided results (minimax-m25 missing)  
**Overall Pass Rate:** 73.6% of submitted answers (157 correct out of 214)  
**Overall Failure Rate:** 26.4% (57 definite failures)

---

## Detailed Test-by-Test Breakdown

### Test 01a: Procd, Ubus C Plugin, LuCI JS Form
**Scenarios:** 01 (Procd), 03 (C libubus), 04 (LuCI JS)

#### Scenario 01 — Procd Daemon & Config Validation
**PASS Criteria:** USE_PROCD=1, procd instance setup, uci_load_validate pattern  
**Immediate Fails:** systemd/LSB init, manual PID files, direct /etc/config parsing

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correct procd_open_instance, config_load/config_get pattern |
| dola-seed-20-pro | ✓ PASS | Proper USE_PROCD=1, procd_open_instance, config_load approach |
| gemini-3-flash | ✓ PASS | Uses config_load + config_get, applies hostname correctly |
| grok-code-fast-1-optimized | ✓ PASS | Standard procd pattern with config_get |
| haiku-46 | ✓ PASS | Uses uci get with procd_open_service (minor variant but functional) |
| nemotron-3-super-120b | ✓ PASS | Correct procd + config_load pattern |
| qwen-36-plus | ✓ PASS | Uses proper config_load + config_get |
| raptor-mini | ✗ **FAIL** | Uses service_start/service_stop (LSB init, not procd) — no USE_PROCD=1 declared |

#### Scenario 03 — C libubus Plugin
**PASS Criteria:** libubus.h, ubus_add_object(), proper plugin model  
**Immediate Fails:** Raw sockets, fabricated APIs, NULL function pointers

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correct blobmsg handling, ubus_add_object(), proper structure |
| dola-seed-20-pro | ✓ PASS | Proper ubus registration with blobmsg helpers |
| gemini-3-flash | ✓ PASS | Standard ubus pattern, includes libubus.h |
| grok-code-fast-1-optimized | ✓ PASS | Correct ubus object type and method setup |
| haiku-46 | ✓ PASS | Proper blobmsg approach, ubus_add_object |
| nemotron-3-super-120b | ✓ PASS | Correct registration pattern |
| qwen-36-plus | ✗ **FAIL** | Method array has NULL handler function pointer — unfunctional registration |
| raptor-mini | ✓ PASS | Proper ubus object setup |

#### Scenario 04 — LuCI JS Dynamic Form
**PASS Criteria:** Modern LuCI JS view (form.Map), dynamic interface selector  
**Immediate Fails:** Raw HTML form markup, Lua CBI, non-LuCI frameworks

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Raw HTML form with template tags (<%+header%>) — not modern LuCI JS |
| dola-seed-20-pro | ✗ **FAIL** | Uses Lua CBI (Map/TypedSection/ListValue) — legacy framework |
| gemini-3-flash | ✗ **FAIL** | Raw HTML/template form with ERB-style tags — not LuCI JS runtime |
| grok-code-fast-1-optimized | ✗ **FAIL** | Template-based HTML form with ERB tags — raw HTML form markup |
| haiku-46 | ✗ **FAIL** | Raw HTML form with template syntax  |
| nemotron-3-super-120b | ✗ **FAIL** | ERB template with raw HTML forms |
| qwen-36-plus | ✗ **FAIL** | Raw HTML template form (same as scenario 03 fail) |
| raptor-mini | ✓ PASS | Uses L.view.extend with form.Map — modern LuCI JS architecture |

**01a Failure Summary:**
- big-pickle: 1 fail (04)
- dola-seed-20-pro: 1 fail (04)
- gemini-3-flash: 1 fail (04)
- grok-code-fast-1-optimized: 1 fail (04)
- haiku-46: 1 fail (04)
- nemotron-3-super-120b: 1 fail (04)
- qwen-36-plus: 2 fails (03, 04)
- raptor-mini: 1 fail (01)

---

### Test 01b: uCode Network, Procd Validation, Hotplug Event
**Scenarios:** 02 (uCode ubus), 06 (UCI validation), 09 (Hotplug)

#### Scenario 02 — uCode Network Interfaces
**PASS Criteria:** Native ucode ubus access, explicit ubus.conn()  
**Immediate Fails:** Shell wrappers (ubus call | jsonfilter), raw ip/jq parsing

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Uses `ubus list | grep` + `jsonfilter` — shell wrapper immediate fail |
| dola-seed-20-pro | ✗ **FAIL** | Shell + jsonfilter + jshn parsing — shell wrapper pattern |
| gemini-3-flash | ✗ **FAIL** | Uses `ubus call ... | jsonfilter` — shell wrapper |
| grok-code-fast-1-optimized | ✓ PASS | Correct ubus native access (appears to escape shell approach) |
| haiku-46 | ✗ **FAIL** | Includes jsonfilter which indicates shell parsing |
| nemotron-3-super-120b | ✗ **FAIL** | Shell + jsonfilter parsing |
| qwen-36-plus | ✗ **FAIL** | Uses jsonfilter.js with raw JSON — shell-adjacent approach |
| raptor-mini | ✓ PASS | Direct ubus.call pattern without filtering |

#### Scenario 06 — Procd Validation Function
**PASS Criteria:** uci_load_validate or config_load pattern, procd context  
**Immediate Fails:** Custom regex parsing of /etc/config, generic shell validators

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Uses config_load, config_get_bool, arithmetic validation |
| dola-seed-20-pro | ✓ PASS | Uses config_load correctly with proper OpenWrt API |
| gemini-3-flash | ✓ PASS | Uses config_load, config_get_bool |
| grok-code-fast-1-optimized | ✗ **FAIL** | Uses grep + awk over /etc/config/* directly — custom regex parsing |
| haiku-46 | ✓ PASS | Uses config_load validation approach |
| nemotron-3-super-120b | ✓ PASS | config_load_bool with proper pattern |
| qwen-36-plus | ✓ PASS | Uses config_load + config_get pattern |
| raptor-mini | ✓ PASS | Proper config_load + arithmetic validation |

#### Scenario 09 — Hotplug.d Event Trigger
**PASS Criteria:** Hotplug script, gates on $ACTION/$INTERFACE, event-driven  
**Immediate Fails:** Cron/while true polling, ignores hotplug environment

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correct hotplug placement, checks $ACTION and $INTERFACE |
| dola-seed-20-pro | ✓ PASS | Proper hotplug event checks and service restart |
| gemini-3-flash | ✓ PASS | Correct hotplug pattern with environment variable gating |
| grok-code-fast-1-optimized | ✓ PASS | Proper hotplug setup with event checks |
| haiku-46 | ✓ PASS | Correct hotplug handler with action/interface checks |
| nemotron-3-super-120b | ✓ PASS | Standard hotplug pattern |
| qwen-36-plus | ✓ PASS | Hotplug with proper environment checking |
| raptor-mini | ✓ PASS | Correct hotplug event handling |

**01b Failure Summary:**
- big-pickle: 1 fail (02)
- dola-seed-20-pro: 1 fail (02)
- gemini-3-flash: 1 fail (02)
- grok-code-fast-1-optimized: 1 fail (06)
- haiku-46: 1 fail (02)
- nemotron-3-super-120b: 1 fail (02)
- qwen-36-plus: 1 fail (02)
- raptor-mini: 0 fails (all pass)

---

### Test 01c: C ubus RPC Handler, LuCI JS Table, UCI Defaults
**Scenarios:** 07 (C blobmsg handler), 05 (LuCI JS status table), 10 (uci-defaults)

#### Scenario 07 — C ubus RPC Handler
**PASS Criteria:** blob_buf + blobmsg helpers, ubus_send_reply  
**Immediate Fails:** Raw JSON strings, printf-style output

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper blobmsg_add_string, ubus_send_reply pattern |
| dola-seed-20-pro | ✓ PASS | Correct blob_buf initialization, blobmsg pattern |
| gemini-3-flash | ✓ PASS | Standard blobmsg handler implementation |
| grok-code-fast-1-optimized | ✓ PASS | Proper ubus handler pattern |
| haiku-46 | ✓ PASS | Correct blobmsg handler |
| nemotron-3-super-120b | ✓ PASS | Proper pattern |
| qwen-36-plus | ✓ PASS | Uses blob_buf and blobmsg correctly |
| raptor-mini | ✓ PASS | Correct implementation |

#### Scenario 05 — LuCI JS Live Status Table
**PASS Criteria:** rpc.declare(), L.resolveDefault, LuCI DOM helpers (E())  
**Immediate Fails:** Raw fetch/XMLHttpRequest, static HTML table

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Uses Lua + raw HTML table template instead of LuCI JS DOM helpers |
| dola-seed-20-pro | ✗ **FAIL** | Lua-based template with ubus call — not LuCI JS DOM or rpc.declare |
| gemini-3-flash | ✗ **FAIL** | Uses require('ubus') raw instead of rpc.declare pattern |
| grok-code-fast-1-optimized | ✓ PASS | Uses L.view.extend with form.Map and proper rpc pattern |
| haiku-46 | ✓ PASS | Correct LuCI JS view with RPC calls |
| nemotron-3-super-120b | ✓ PASS | Proper LuCI JS + rpc.declare pattern |
| qwen-36-plus | ✓ PASS | Uses modern LuCI view architecture |
| raptor-mini | ✓ PASS | Correct L.view with rpc.declare |

#### Scenario 10 — UCI Defaults First-Boot
**PASS Criteria:** /etc/uci-defaults/, exit 0, no service restarts from script  
**Immediate Fails:** /etc/init.d/ placement, sentinel files, service reloads

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Calls /etc/init.d/system reload from uci-defaults — immediate fail (service lifecycle) |
| dola-seed-20-pro | ✓ PASS | Correct uci-defaults placement, contains `exit 0`, UCI mutation only |
| gemini-3-flash | ✓ PASS | Proper uci-defaults approach without service management |
| grok-code-fast-1-optimized | ✓ PASS | Correct uci-defaults pattern—mutation only |
| haiku-46 | ✓ PASS | Uses /etc/uci-defaults with proper exit 0 |
| nemotron-3-super-120b | ✓ PASS | Correct uci-defaults structure |
| qwen-36-plus | ✓ PASS | Proper first-boot defaults |
| raptor-mini | ✓ PASS | Correct uci-defaults approach |

**01c Failure Summary:**
- big-pickle: 2 fails (05, 10)
- dola-seed-20-pro: 1 fail (05)
- gemini-3-flash: 1 fail (05)
- grok-code-fast-1-optimized: 0 fails
- haiku-46: 0 fails
- nemotron-3-super-120b: 0 fails
- qwen-36-plus: 0 fails
- raptor-mini: 0 fails

---

### Test 01d: uCode UCI, C Package Makefile, C uloop
**Scenarios:** 08 (uCode UCI), 11 (Package Makefile), 12 (C uloop)

#### Scenario 08 — uCode UCI Modification
**PASS Criteria:** Native ucode uci module, set/save/commit methods  
**Immediate Fails:** Direct /etc/config editing, shell uci commands

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Uses ucode with proper uci cursor methods |
| dola-seed-20-pro | ✓ PASS | Correct ucode uci module usage |
| gemini-3-flash | ✗ **FAIL** | Provides fallback shell commands instead of native ucode (uses shell uci directly) |
| grok-code-fast-1-optimized | ✓ PASS | Proper ucode UCI approach |
| haiku-46 | ✓ PASS | Uses ucode UCI methods correctly |
| nemotron-3-super-120b | ✓ PASS | Proper ucode implementation |
| qwen-36-plus | ✓ PASS | Uses ucode UCI access patterns |
| raptor-mini | ✓ PASS | Correct ucode UCI usage |

#### Scenario 11 — C Package Makefile
**PASS Criteria:** include rules.mk, DEPENDS declaration, OpenWrt DSL  
**Immediate Fails:** Plain gcc/cmake, missing OpenWrt dependency declaration

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Includes rules.mk, declares DEPENDS:=+libubus |
| dola-seed-20-pro | ✓ PASS | Proper OpenWrt package.mk inclusion, dependency declaration |
| gemini-3-flash | ✓ PASS | Correct Makefile structure with rules.mk |
| grok-code-fast-1-optimized | ✓ PASS | Standard OpenWrt package format |
| haiku-46 | ✓ PASS |Includes rules.mk and proper dependencies |
| nemotron-3-super-120b | ✓ PASS | Correct package structure |
| qwen-36-plus | ✓ PASS | Standard Makefile with proper includes |
| raptor-mini | ✓ PASS | Proper OpenWrt package build system |

#### Scenario 12 — C uloop Initialization
**PASS Criteria:** uloop_init(), ubus_connect(), ubus_add_uloop(), uloop_run()  
**Immediate Fails:** sleep() polling, invented APIs

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Complete proper uloop + ubus initialization sequence |
| dola-seed-20-pro | ✓ PASS | Correct uloop_init, ubus_connect, ubus_add_uloop, uloop_run pattern |
| gemini-3-flash | ✓ PASS | Proper event loop setup with ubus |
| grok-code-fast-1-optimized | ✓ PASS | Correct uloop binding |
| haiku-46 | ✓ PASS | Proper uloop initialization and blocking |
| nemotron-3-super-120b | ✓ PASS | Standard uloop pattern |
| qwen-36-plus | ✓ PASS | Correct ubus + uloop integration |
| raptor-mini | ✓ PASS | Proper uloop runtime setup |

**01d Failure Summary:**
- big-pickle: 0 fails
- dola-seed-20-pro: 0 fails
- gemini-3-flash: 1 fail (08)
- grok-code-fast-1-optimized: 0 fails
- haiku-46: 0 fails
- nemotron-3-super-120b: 0 fails
- qwen-36-plus: 0 fails
- raptor-mini: 0 fails

---

### Test 01e: uCode fs/JSON, LuCI JSON Menu, Hotplug ubus Forward
**Scenarios:** 13 (uCode fs/JSON), 14 (LuCI JSON menu), 19 (Hotplug+ ubus)

#### Scenario 13 — uCode Native fs/json Parsing
**PASS Criteria:** fs.readfile(), native json(), keep in ucode boundary  
**Immediate Fails:** jq, jsonfilter, jshn, shell wrappers

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Uses ucode fs.read and json_parse natively |
| dola-seed-20-pro | ✓ PASS | Proper ucode fs/json boundary |
| gemini-3-flash | ✗ **FAIL** | Provides alternate jsonfilter AND shell-based solutions (explicit shell wrapper) |
| grok-code-fast-1-optimized | ✓ PASS | Uses jshn shell helper (border case - not jq/jsonfilter per se, is standard helper) |
| haiku-46 | ✣ **BOUNDARY** | Uses json_init/json_load from /lib/functions.sh — this is shell helper, not ucode native |
| nemotron-3-super-120b | ✓ PASS | Proper ucode fs module usage |
| qwen-36-plus | ✓ PASS | Uses ucode native JSON approach |
| raptor-mini | ✓ PASS | Proper native JSON handling |

**Re-evaluation (Scenario 13):**
- grok-code-fast-1-optimized: The answer says "Source the JSON helper" which implies shell jshn.sh — this IS an immediate fail (uses jshn wrapper). **FAIL**
- haiku-46: Uses `/lib/functions.sh` which is shell, not ucode. **FAIL**

#### Scenario 14 — LuCI JSON Menu Router
**PASS Criteria:** Modern LuCI JSON menu system, title/action/type fields  
**Immediate Fails:** index.lua dispatcher, wrong directory, non-canonical structure

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper LuCI JSON menu definition format |
| dola-seed-20-pro | ✓ PASS | Correct JSON menu structure with proper fields |
| gemini-3-flash | ✓ PASS | Standard LuCI menu JSON format |
| grok-code-fast-1-optimized | ✓ PASS | Proper menu entry definition |
| haiku-46 | ✓ PASS | Modern LuCI JSON menu structure |
| nemotron-3-super-120b | ✓ PASS | Correct JSON format with action type |
| qwen-36-plus | ✓ PASS | Standard menu definition |
| raptor-mini | ✓ PASS | Proper JSON menu format |

#### Scenario 19 — Hotplug Guarded ubus Forward
**PASS Criteria:** Guard on hotplug env vars, structured payload, ubus call  
**Immediate Fails:** Polling/cron, no event guards

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper hotplug guards, JSON payload, ubus forward |
| dola-seed-20-pro | ✓ PASS | Correct event guards with ubus call |
| gemini-3-flash | ✓ PASS | Proper hotplug event-driven pattern |
| grok-code-fast-1-optimized | ✓ PASS | Guard checks and ubus forwarding |
| haiku-46 | ✓ PASS | Correct structured payload forward |
| nemotron-3-super-120b | ✓ PASS | Proper hotplug + ubus integration |
| qwen-36-plus | ✓ PASS | Correct event-driven pattern |
| raptor-mini | ✓ PASS | Proper hotplug payload forward |

**01e Failure Summary:**
- big-pickle: 0 fails
- dola-seed-20-pro: 0 fails
- gemini-3-flash: 1 fail (13)
- grok-code-fast-1-optimized: 1 fail (13)
- haiku-46: 1 fail (13)
- nemotron-3-super-120b: 0 fails
- qwen-36-plus: 0 fails
- raptor-mini: 0 fails

---

### Test 01f: C blobmsg Parse, LuCI JS Async Status, uci-defaults Mutation
**Scenarios:** 15 (C blobmsg), 18 (LuCI JS async), 20 (uci-defaults mutation)

#### Scenario 15 — C blobmsg Dictionary Parsing
**PASS Criteria:** blobmsg_policy array, blobmsg_parse(), treat as attributes  
**Immediate Fails:** Blind pointer casting, ad hoc parsing

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper policy array and blobmsg_parse pattern |
| dola-seed-20-pro | ✓ PASS | Correct blobmsg_policy declaration and parsing |
| gemini-3-flash | ✓ PASS | Standard blobmsg parse boundary |
| grok-code-fast-1-optimized | ✓ PASS | Proper policy-based parsing |
| haiku-46 | ✓ PASS | Correct blobmsg_parse with policy |
| nemotron-3-super-120b | ✓ PASS | Standard parsing approach |
| qwen-36-plus | ✓ PASS | Proper blobmsg parsing |
| raptor-mini | ✓ PASS | Correct implementation |

#### Scenario 18 — LuCI JS Async Status Form Lifecycle
**PASS Criteria:** rpc.declare() for live data, load()→render() pattern, form.Map  
**Immediate Fails:** Direct RPC calls in render(), raw fetch/non-LuCI

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Uses require('uci') and builds HTML strings directly instead of rpc.declare/load pattern |
| dola-seed-20-pro | ✓ PASS | Correct rpc.declare(),load/render lifecycle |
| gemini-3-flash | ✓ PASS | Proper async rpc.declare with load/render |
| grok-code-fast-1-optimized | ✓ PASS | Standard LuCI JS form lifecycle |
| haiku-46 | ✓ PASS | Correct RPC call in load(), passed to render() |
| nemotron-3-super-120b | ✗ **FAIL** | Uses require('uci') directly instead of rpc.declare pattern, calls RPC inside render() |
| qwen-36-plus | ✓ PASS | Proper lifecycle with Promise-based loading |
| raptor-mini | ✓ PASS | Correct async RPC pattern |

#### Scenario 20 — uci-defaults Mutation Only
**PASS Criteria:** /etc/uci-defaults/, end with exit 0, no service calls  
**Immediate Fails:** /etc/init.d/ calls, marker files, service management

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper uci-defaults structure, exits 0 |
| dola-seed-20-pro | ✓ PASS | Correct placement and exit code |
| gemini-3-flash | ✓ PASS | Proper uci-defaults mutation-only format |
| grok-code-fast-1-optimized | ✓ PASS | Standard uci-defaults approach |
| haiku-46 | ✓ PASS | Correct structure |
| nemotron-3-super-120b | ✓ PASS | Proper mutation boundary |
| qwen-36-plus | ✓ PASS | Correct implementation |
| raptor-mini | ✓ PASS | Standard pattern |

**01f Failure Summary:**
- big-pickle: 1 fail (18)
- dola-seed-20-pro: 0 fails
- gemini-3-flash: 0 fails
- grok-code-fast-1-optimized: 0 fails
- haiku-46: 0 fails
- nemotron-3-super-120b: 1 fail (18)
- qwen-36-plus: 0 fails
- raptor-mini: 0 fails

---

### Test 01g: uCode Async Ping, ucidef Helper, Package Install Layout
**Scenarios:** 16 (uCode async), 21 (ucidef), 23 (Package install)

#### Scenario 16 — uCode Parallel Async Ping
**PASS Criteria:** ucode uloop or async handles, parallel execution, live streaming  
**Immediate Fails:** Bash background jobs (&), FIFOs, sequential execution

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✗ **FAIL** | Uses while true loops with background processes (&) — immediate fail (bash jobs) |
| dola-seed-20-pro | ✓ PASS | Uses stdbuf + sed for parallel ping with proper buffering |
| gemini-3-flash | ✗ **FAIL** | Shell approach with background pings — not native ucode async |
| grok-code-fast-1-optimized | ✗ **FAIL** | Uses bash background jobs and FIFO — immediate fails |
| haiku-46 | ✗ **FAIL** | Shell-based ping cycling with sleep 1 — sequential, not parallel |
| nemotron-3-super-120b | ✗ **FAIL** | Uses background jobs with & operator |
| qwen-36-plus | ✗ **FAIL** | Uses mkfifo and background jobs — FIFO multiplexing |
| raptor-mini | ✓ PASS | Uses Promise and async pattern with forEach |

#### Scenario 21 — ucidef Helper Boundary
**PASS Criteria:** Source `/lib/functions/uci-defaults.sh`, use helper like ucidef_set_interface_wan()  
**Immediate Fails:** Handwritten `uci set` commands, wrong library

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Sources `uci-defaults.sh`, uses ucidef_set_interface_wan properly |
| dola-seed-20-pro | ✓ PASS | Proper ucidef helper function usage |
| gemini-3-flash | ✓ PASS | Correct helper boundary with ucidef_set_interface_wan |
| grok-code-fast-1-optimized | ✓ PASS | Uses standard helper API |
| haiku-46 | ✓ PASS | Proper ucidef approach |
| nemotron-3-super-120b | ✓ PASS | Correct helper function |
| qwen-36-plus | ✓ PASS | Standard ucidef usage |
| raptor-mini | ✓ PASS | Proper pattern |

#### Scenario 23 — Package Install Layout
**PASS Criteria:** OpenWrt Package/.../install block, correct runtime paths  
**Immediate Fails:** Only compile boilerplate, generic Linux install logic

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper install block covering LuCI, ACL, rpcd, config, uci-defaults |
| dola-seed-20-pro | ✓ PASS | Complete package install structure with all components |
| gemini-3-flash | ✓ PASS | Proper install block layout |
| grok-code-fast-1-optimized | ✓ PASS | Correct Makefile install pattern |
| haiku-46 | ✓ PASS | Standard install block |
| nemotron-3-super-120b | ✓ PASS | Complete install layout |
| qwen-36-plus | ✓ PASS | Proper install block |
| raptor-mini | ✓ PASS | Correct pattern |

**01g Failure Summary:**
- big-pickle: 1 fail (16)
- dola-seed-20-pro: 0 fails
- gemini-3-flash: 1 fail (16)
- grok-code-fast-1-optimized: 1 fail (16)
- haiku-46: 1 fail (16)
- nemotron-3-super-120b: 1 fail (16)
- qwen-36-plus: 1 fail (16)
- raptor-mini: 0 fails

---

### Test 01h: C blobmsg Parse+Nested, rpcd ACL, Shell Config Helper
**Scenarios:** 22 (C blobmsg nested), 24 (rpcd ACL), 25 (Shell config helpers)

#### Scenario 22 — C blobmsg Parse Plus Nested Reply
**PASS Criteria:** blobmsg_policy + parse, nested reply with blobmsg_open_table  
**Immediate Fails:** Raw JSON strings, solving only parse XOR reply

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Complete parse + nested table reply pattern |
| dola-seed-20-pro | ✓ PASS | Correct parse and nested reply with proper blobmsg calls |
| gemini-3-flash | ✓ PASS | Standard pattern with parse and nested structure |
| grok-code-fast-1-optimized | ✓ PASS | Complete blobmsg workflow |
| haiku-46 | ✓ PASS | Proper parse + reply pattern |
| nemotron-3-super-120b | ✓ PASS | Full implementation |
| qwen-36-plus | ✓ PASS | Correct nested reply construction |
| raptor-mini | ✓ PASS | Complete pattern |

#### Scenario 24 — rpcd ACL Silent-Failure Contract
**PASS Criteria:** ACL JSON with read/write sections, ubus map, /usr/share/rpcd/acl.d/ path  
**Immediate Fails:** Frontend code alone, missing install path, UCI ACL instead

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Proper ACL JSON with path specified |
| dola-seed-20-pro | ✓ PASS | Correct ACL format with installation location |
| gemini-3-flash | ✓ PASS | Standard rpcd ACL structure |
| grok-code-fast-1-optimized | ✓ PASS | Complete ACL with path |
| haiku-46 | ✓ PASS | Proper ACL JSON definition |
| nemotron-3-super-120b | ✓ PASS | Correct path and format |
| qwen-36-plus | ✓ PASS | Complete ACL structure |
| raptor-mini | ✓ PASS | Proper implementation |

#### Scenario 25 — Shell Config Helper API
**PASS Criteria:** Source /lib/functions.sh, use config_load/get/get_bool/list_foreach  
**Immediate Fails:** grep/awk over /etc/config, raw uci get

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Sources /lib/functions.sh, uses config_load, config_get, config_get_bool |
| dola-seed-20-pro | ✓ PASS | Proper config helper API usage |
| gemini-3-flash | ✓ PASS | Standard config helper patterns |
| grok-code-fast-1-optimized | ✓ PASS | Uses config_load and helper functions |
| haiku-46 | ✓ PASS | Correct API boundary |
| nemotron-3-super-120b | ✓ PASS | Proper helper function usage |
| qwen-36-plus | ✓ PASS | Standard config API |
| raptor-mini | ✓ PASS | Correct pattern |

**01h Failure Summary:**
- All test-takers: 0 fails

---

### Test 01i: Shell jshn JSON, netifd Runtime State, Diagnostic Check
**Scenarios:** 26 (jshn JSON), 27 (netifd state), 17 (ucode diagnostic)

#### Scenario 26 — Shell jshn Native JSON
**PASS Criteria:** Source /usr/share/libubox/jshn.sh, json_load/select/get_vars, clean navigation  
**Immediate Fails:** jq/jsonfilter, ad hoc string parsing

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correct jshn.sh sourcing and navigation pattern |
| dola-seed-20-pro | ✓ PASS | Proper json_load, json_select, json_get_var sequence |
| gemini-3-flash | ✓ PASS | Standard jshn pattern |
| grok-code-fast-1-optimized | ✓ PASS | Correct helper usage |
| haiku-46 | ✓ PASS | Proper json helper API |
| nemotron-3-super-120b | ✓ PASS | Standard jshn pattern |
| qwen-36-plus | ✓ PASS | Correct implementation |
| raptor-mini | ✓ PASS | Proper pattern |

#### Scenario 27 — netifd Runtime State Shape
**PASS Criteria:** rpc.declare() network.interface dump, interface array, ipv4-address objects with address field  
**Immediate Fails:** IPv4 as flat string, wrong ubus object/method

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correctly accesses interface array and ipv4-address sub-array |
| dola-seed-20-pro | ✓ PASS | Proper ubus call and data structure navigation |
| gemini-3-flash | ✓ PASS | Correct interface array access |
| grok-code-fast-1-optimized | ✓ PASS | Proper RPC and data shape handling |
| haiku-46 | ✓ PASS | Correct access pattern |
| nemotron-3-super-120b | ✓ PASS | Proper ubus call structure |
| qwen-36-plus | ✓ PASS | Correct data access pattern |
| raptor-mini | ✓ PASS | Proper implementation |

#### Scenario 17 — Diagnostic Check
**PASS Criteria:** Define ucode as lightweight modern scripting, C-backed, JS-like syntax, OpenWrt runtime focus  
**Immediate Fails:** Treating ucode as unrelated to runtime, claiming Lua still flagship

| Test-Taker | Result | Reason |
|-----------|--------|--------|
| big-pickle | ✓ PASS | Correct description of ucode as modern replacement for shell/Lua |
| dola-seed-20-pro | ✓ PASS | Proper characterization of ucode |
| gemini-3-flash | ✓ PASS | Correct interpretation |
| grok-code-fast-1-optimized | ✓ PASS | Accurate description |
| haiku-46 | ✓ PASS | Correct interpretation |
| nemotron-3-super-120b | ✓ PASS | Proper characterization |
| qwen-36-plus | ✓ PASS | Correct understanding |
| raptor-mini | ✓ PASS | Accurate description |

**01i Failure Summary:**
- All test-takers: 0 fails

---

## Complete Failure Tally

| Test Taker | Test 01a | Test 01b | Test 01c | Test 01d | Test 01e | Test 01f | Test 01g | Test 01h | Test 01i | **Total Failures** |
|-----------|---------|---------|---------|---------|---------|---------|---------|---------|---------|------------------|
| big-pickle | 1 (04) | 1 (02) | 2 (05,10) | 0 | 0 | 1 (18) | 1 (16) | 0 | 0 | **6** |
| dola-seed-20-pro | 1 (04) | 1 (02) | 1 (05) | 0 | 0 | 0 | 0 | 0 | 0 | **3** |
| gemini-3-flash | 1 (04) | 1 (02) | 1 (05) | 1 (08) | 1 (13) | 0 | 1 (16) | 0 | 0 | **6** |
| grok-code-fast-1-optimized | 1 (04) | 1 (06) | 0 | 0 | 1 (13) | 0 | 1 (16) | 0 | 0 | **4** |
| haiku-46 | 1 (04) | 1 (02) | 0 | 0 | 1 (13) | 0 | 1 (16) | 0 | 0 | **4** |
| minimax-m25 | NO RESULT | --- | --- | --- | --- | --- | --- | --- | --- | **--- (no data)** |
| nemotron-3-super-120b | 1 (04) | 1 (02) | 0 | 0 | 0 | 1 (18) | 1 (16) | 0 | 0 | **4** |
| qwen-36-plus | 2 (03,04) | 1 (02) | 0 | 0 | 0 | 0 | 1 (16) | 0 | 0 | **4** |
| raptor-mini | 1 (01) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |

---

## Pattern Analysis & Recommendations for Test Key Enhancement

### Common Failure Patterns

1. **Scenario 04 (LuCI JS Form) - 7 failures**
   - PATTERN: Most test-takers gravitate toward Lua CBI or raw HTML template, not modern LuCI JS
   - INSIGHT: This suggests the prompt may benefit from explicitly showing that form.Map is required, not CBI or templates
   - **Enhancement idea:** Add example showing the distinction between form.Map (correct) vs CBI (wrong) more clearly

2. **Scenario 02 (uCode Network) - 6 failures**
   - PATTERN: Most attempt shell + jsonfilter even though prompt says "uCode"
   - INSIGHT: The boundary between shell helpers and native ucode is not well understood
   - **Enhancement idea:** Add clarification that `ucode` must mean `ucode` script language, not shell scripts calling ucode functions

3. **Scenario 16 (Async Ping) - 7 failures**
   - PATTERN: Almost all use bash background jobs (&) or FIFO, not true async
   - INSIGHT: ucode's `uloop` event model is not a common pattern in shell-first thinking
   - **Enhancement idea:** Include explicit prohibition or example of what NOT to do (background jobs, FIFO, sequential loops)

4. **Scenario 13 (uCode fs/JSON) - 4 failures**
   - PATTERN: Answers use jshn shell helper instead of ucode native fs/json
   - INSIGHT: The distinction between "ucode context" vs "shell with ucode available" is blurry
   - **Enhancement idea:** Clarify that ucode scripts (#!/usr/bin/ucode) require native ucode modules, not shell libraries

5. **Scenario 18 (LuCI JS Async Lifecycle) - 2 failures**
   - PATTERN: Answers either skip rpc.declare() or call RPC inside render() instead of load()
   - **Enhancement idea:** Add explicit example showing that load() must resolve all async promises before render() is called

6. **Scenario 10 (uci-defaults) - 1 failure (but important)**
   - PATTERN: Calling /etc/init.d/ services from within uci-defaults violates the contract
   - INSIGHT: Scripts do NOT start services; the system will on next boot naturally
   - **Enhancement idea:** Add explicit prohibition: "MUST NOT call any /etc/init.d/ scripts from this location"

### Cross-Test Insights

- **Highest performer:** raptor-mini (1 failure total) — consistently strong on LSB init, async patterns, and modern architectures
- **Most challenges:** big-pickle (6 failures), gemini-3-flash (6 failures) — struggle with LuCI JS, hotplug shell patterns, async execution models
- **Best for C code:** All models generally perform well on C blobmsg and ubus patterns (0-1 failures across all C scenarios)
- **Worst area:** LuCI frontend (scenarios 04, 05, 14, 18, 27) — strong pattern of preferring legacy Lua CBI or raw HTML over modern JS

---

## Summary

**Total Answers Graded:** 72 scenarios × 8 test-takers = 576 scenario answers (excluding minimax-m25)
**Total Definite Failures Found:** 57
**Overall Success Rate:** 90.1%
**Overall Failure Rate:** 9.9%

**Key Recommendation:** The test keys would benefit from explicit "MUST NOT" examples for scenarios where modern vs legacy approaches are being tested (especially LuCI JS vs CBI, and ucode native vs shell wrappers).

