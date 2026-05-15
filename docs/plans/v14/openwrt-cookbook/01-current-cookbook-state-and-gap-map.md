# Current Cookbook State And Gap Map

**Purpose:** Factual inventory of the live cookbook corpus and the most important known gaps or blockers. This file is intentionally descriptive, not argumentative.

---

## 1. Current Live Authored Corpus

The live authored cookbook source set is under `static/cookbook-source/`.

### 1.1 Foundation and orientation

| Page | Current role |
| --- | --- |
| `architecture-overview.md` | Cross-component orientation for service/config/UI/system interactions |
| `common-ai-mistakes.md` | Hub page for known AI/OpenWrt failure categories |
| `openwrt-era-guide.md` | Current vs transitional vs legacy pattern framing |

### 1.2 Service, boot, and policy boundaries

| Page | Current role |
| --- | --- |
| `procd-service-lifecycle.md` | procd lifecycle and init-script boundaries |
| `firstboot-uci-defaults-pattern.md` | first-boot config mutation boundary |
| `firstboot-wifi-policy.md` | first-boot Wi-Fi policy decisions |
| `hotplug-handler-pattern.md` | hotplug event handling discipline |
| `package-config-bootstrap-pattern.md` | package-owned config bootstrap and upgrade logic |

### 1.3 Runtime state, IPC, and architecture placement

| Page | Current role |
| --- | --- |
| `inter-component-communication-map.md` | placement of logic across browser, uhttpd, rpcd, ubus, daemons |
| `ubus-observability-pattern.md` | ubus-first state and metrics publication |
| `runtime-device-identity-via-ubus.md` | canonical runtime identity surface |
| `ucode-rpcd-service-pattern.md` | privileged backend service pattern in ucode/rpcd |
| `c-libubus-daemon-runtime-pattern.md` | minimal current-era C daemon startup contract around `uloop_init()`, `ubus_connect()`, `ubus_add_uloop()`, and `uloop_run()` |

### 1.4 Configuration, UI, and build surfaces

| Page | Current role |
| --- | --- |
| `uci-read-write-from-ucode.md` | UCI mutation and persistence from ucode |
| `ucode-native-file-io-and-json.md` | native non-UCI file I/O plus JSON parsing boundary inside ucode |
| `luci-form-with-uci.md` | modern LuCI JS form wiring with UCI |
| `luci-uhttpd-https-auth.md` | LuCI, uhttpd, HTTPS, auth, and cookie behavior |
| `minimal-openwrt-package-makefile.md` | OpenWrt package Makefile contract |
| `network-device-model-migrations.md` | ifname/ports, swconfig/DSA, and migration logic |

### 1.5 Native ucode and async execution surfaces

| Page | Current role |
| --- | --- |
| `ucode-async-process-pattern.md` | async subprocess handling with `fs.popen()` and `uloop.handle(..., uloop.ULOOP_READ)` |

### 1.6 Supporting note

| File | Role |
| --- | --- |
| `era-guide-evidence-needed.md` | explicit evidence debt tracker for `openwrt-era-guide.md` |

---

## 2. Current Strengths

The live corpus already covers most of the durable OpenWrt boundaries that generic Linux reasoning tends to miss:

- procd instead of generic init habits
- first-boot sequencing via `uci-defaults`
- hotplug environment and event taxonomy
- modern LuCI JS form architecture
- UCI mutation from ucode
- ubus-first state surfaces
- package/bootstrap configuration patterns
- network migration boundaries

This means v14 should begin by tightening selection and verification, not by assuming the corpus is empty.

---

## 3. Highest-Value Remaining Or Weakly Surfaced Gaps

These are the strongest remaining gaps relative to the known blind spots documented in the v13 defect-discovery work.

| Gap | Why it still matters | Likely outcome |
| --- | --- | --- |
| Retroactive staged backfill for early promoted pages | Several cookbook pages now exist, but some were promoted before the staged draft/log/review workflow was formalized | Draft, creation log, and human review reconciliation packets |
| Complete `uci_load_validate` reference treatment | The current service lifecycle coverage may not be enough if this continues to be a repeated structural miss | Extend `procd-service-lifecycle.md` or create a focused companion page |

---

## 4. Current Promotion Blockers

These are real blockers to declaring the cookbook corpus settled.

### 4.1 Reviewer ownership placeholders

The active cookbook pages currently use `reviewed_by: placeholder` in frontmatter.

This means the pages are authored and dated, but final accountable reviewer ownership is not yet complete.

### 4.2 Era guide evidence debt

`era-guide-evidence-needed.md` explicitly records unresolved external evidence needed to fully verify era boundary claims in `openwrt-era-guide.md`.

### 4.3 Path wording drift resolved

The durable cookbook authoring spec was realigned on 2026-04-05 to use the active
filesystem contract: `static/cookbook-source/`.

Any remaining `content/cookbook-source/` mentions should now be treated as archived
historical wording rather than live path truth.

### 4.4 Coverage does not yet imply explicit remediation proof

The corpus is broad, but not every page has an explicit documented before/after remediation relationship to the scenarios that originally justified it.

### 4.5 Retroactive backfill still in progress

`ucode-native-file-io-and-json.md` is now being backfilled into the staged lifecycle using imported
Scenario 13 evidence, but final human review and accountable reviewer ownership are still pending.

---

## 5. Current Recommended Direction

Based on current state, v14 should prioritize:

1. formal scenario admission and retirement rules
2. a failure-family deduplication layer
3. promotion rules for new page versus page extension
4. reviewer ownership cleanup
5. explicit remediation verification on the strongest remaining blind spots

It should **not** begin by launching a new large topic-mining wave without first tightening those controls.
