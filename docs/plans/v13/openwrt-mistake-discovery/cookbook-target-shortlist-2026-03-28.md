# Cookbook Target Shortlist (2026-03-28)

This is the first implementation artifact for turning the processed archive corpus into concrete cookbook targets.

It is intentionally narrower than the raw lesson corpus. The goal here is not to preserve every interesting thread. The goal is to identify the highest-value, transferable, OpenWrt-specific mistake families that can become task-oriented WRONG/CORRECT cookbook pages.

## Keep Rules

- Keep mistake families that recur across subsystems or reveal a durable OpenWrt programming model.
- Keep topics that can be taught with small, source-backed code snippets.
- Keep topics that are useful to both humans and AI agents working in current-era OpenWrt trees.
- Prefer runtime, config, init, IPC, LuCI, and migration patterns over bring-up-only work.

## Drop Rules

- Drop one-off board enablement, DTS-only bring-up, and vendor flash-layout quirks.
- Drop broad kernel debugging topics unless the lesson clearly maps to OpenWrt integration practice.
- Drop generic package-version bumps and toolchain churn unless they expose an OpenWrt-specific boundary.
- Drop topics already substantially covered by the current cookbook set unless the new lesson would materially deepen the page.

## Current Cookbook Overlap

Existing pages already cover the basics of package Makefiles, LuCI form wiring, procd lifecycle, UCI from ucode, and high-level architecture. The shortlist below avoids rewriting those pages from scratch.

The main gaps are still:

- first-boot mutation patterns
- hotplug handler design
- ubus and rpcd service design
- network model migrations
- LuCI and uhttpd auth and HTTPS behavior
- canonical runtime identity and observability surfaces

## Priority Shortlist

| Priority | Mistake family | Why it survives filtering | Evidence seeds | Cookbook destination |
| --- | --- | --- | --- | --- |
| P1 | Ubus-first metrics and state surfaces | Repeated evidence that shelling out from init scripts or LuCI is slow, duplicated, and fragile. The durable lesson is to publish state once through ubus and consume it everywhere. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt (`add ubus support to ltq-[v|a]dsl-app`) and https://lists.openwrt.org/pipermail/openwrt-devel/2021-December.txt (`netifd: add devtype to ubus call`) | New page: `inter-component-communication-map.md` plus a focused pattern page `ubus-observability-pattern.md` |
| P1 | rpcd and ubus contracts must degrade cleanly when optional backends or ACL objects are missing | The archive repeatedly shows runtime breakage from assuming a ubus object, backend field, or ACL surface always exists. This is a strong OpenWrt-specific service-author lesson. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-June.txt (dnsmasq ubus name collision and init failure behavior) and https://lists.openwrt.org/pipermail/openwrt-devel/2025-December.txt (`ufpd: import unetmsg.client conditionally`) | Planned page: `ucode-rpcd-service-pattern.md` |
| P1 | `uci-defaults` is for first-boot state mutation, not early service orchestration | This is a recurring misunderstanding with real user-facing breakage. The durable lesson is sequencing: mutate config first, let boot and procd apply it later. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-March.txt (uhttpd reload from `uci-defaults` called out as wrong) | New page: `firstboot-uci-defaults-pattern.md` |
| P1 | First-boot Wi-Fi enablement is a policy and config problem, not an async probe problem | The thread resolves a common misconception directly: enabling first-boot Wi-Fi only requires mutating config before boot continues. That is cookbook-grade and highly reusable. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-July.txt (`Enabling Wi-Fi on First boot`) | New page: `firstboot-uci-defaults-pattern.md` with a dedicated section or companion page `firstboot-wifi-policy.md` |
| P1 | Hotplug handlers must sanitize inherited environment and handle event taxonomy explicitly | The corpus shows two durable failures: stale shell variables leaking into handlers and scripts assuming only add/remove events exist. This is exactly the kind of low-level OpenWrt trap a cookbook should teach. | https://lists.openwrt.org/pipermail/openwrt-devel/2024-February.txt (`procd, possible hotplug issue?`) and a second seed to confirm from the archive pass around `comgt` USB bind/unbind handling | Planned page: `hotplug-handler-pattern.md` |
| P1 | Bridge model migration from `ifname` to `ports` needs compatibility shims, not silent breakage | This is a clear, teachable example of OpenWrt network model change management. It is specific enough to be useful and broad enough to recur. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt (`bridge: rename "ifname" attribute to "ports"`) | New page: `network-device-model-migrations.md` |
| P1 | swconfig-to-DSA migration should preserve user intent through explicit `uci-defaults` migration scripts | This is a core OpenWrt transition pattern, not a one-off board quirk. It belongs in cookbook form because future migrations will repeat the same shape. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-October.txt (`bcm53xx: switch to the upstream DSA-based b53 driver`) | New page: `network-device-model-migrations.md` |
| P2 | Device-specific switch support belongs in per-device packages, not target-wide kernel defaults | The lesson is small but important: encode support where the device model needs it, do not smear target defaults across unrelated boards. This generalizes well to other optional hardware surfaces. | https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt (`ath79: Push MV88E6060 DSA switch into package`) | Add a focused section to `network-device-model-migrations.md` |
| P2 | LuCI and uhttpd HTTPS behavior has real auth, redirect, and cookie edge cases | This is not generic web advice. The archive shows concrete OpenWrt-specific behavior around `sysauth` cookies, HTTPS availability, and LuCI UX. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt (`Activate https server support in 21.02 by default`) and continuation references in https://lists.openwrt.org/pipermail/openwrt-devel/2021-September.txt | New page: `luci-uhttpd-https-auth.md` |
| P2 | `ubus call system board` is the canonical runtime identity surface | The archive explicitly points to the correct runtime identity source instead of reconstructing target, subtarget, and profile from build-time assumptions. This is ideal cookbook material for tooling and agents. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt (image-selection discussion pointing to `ubus call system board`) | Add a core section to `inter-component-communication-map.md` |
| P2 | Package-owned config bootstrapping should land in `/etc/config` with predictable init logic, not only static conf fragments | The OpenSSL engine series exposes a reusable package pattern: write defaults through package-owned config, then let init and runtime logic apply them. This generalizes beyond OpenSSL. | https://lists.openwrt.org/pipermail/openwrt-devel/2021-April.txt (`Engine configuration series`) | New page: `package-config-bootstrap-pattern.md` |

## Mapping To Existing Cookbook Pages

| Existing page | Recommendation |
| --- | --- |
| `procd-service-lifecycle.md` | Extend with a short boundary section that explains when a problem belongs in procd, when it belongs in hotplug, and when the better answer is ubus. |
| `luci-form-with-uci.md` | Keep focused on form wiring. Do not overload it with HTTPS, cookie, or auth-sequencing behavior. |
| `uci-read-write-from-ucode.md` | Keep focused on ucode mutation mechanics. First-boot shell-based mutation belongs in a separate page. |
| `common-ai-mistakes.md` | Turn this into a link hub for the new pages once they exist. Do not let it absorb the implementation detail itself. |

## Deferred Or Backlog Families

These showed up in the archive but should not be first-wave cookbook targets:

- extroot, NAND, UBI, and factory-flash preservation threads that depend on device-specific storage layouts
- calibration and MAC-fix hotplug snippets tied to a single board family
- large kernel backport or toolchain series with only incidental OpenWrt lessons
- modem bring-up threads that still need a stronger separation between generic netifd or ModemManager patterns and board-specific logs
- pure packaging or licensing disputes that do not teach a reusable programming model

## Authoring Order

Suggested order for the next cookbook-writing pass:

1. `firstboot-uci-defaults-pattern.md`
2. `hotplug-handler-pattern.md`
3. `ucode-rpcd-service-pattern.md`
4. `network-device-model-migrations.md`
5. `inter-component-communication-map.md`
6. `luci-uhttpd-https-auth.md`

This order starts with the smallest, least device-specific boundaries first, then moves outward into network migration and LuCI behavior.

## Notes For The Next Pass

- For every shortlisted family, collect one current upstream example from `openwrt`, `packages`, or `luci` before authoring prose.
- Prefer examples that still exist on `main`, even if the triggering mistake came from an older thread.
- Keep future cookbook pages task-oriented. The archive evidence explains why the lesson matters; the code example must show how to do it correctly now.