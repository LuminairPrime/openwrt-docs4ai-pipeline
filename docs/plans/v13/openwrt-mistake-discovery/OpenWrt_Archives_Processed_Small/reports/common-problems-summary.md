# Common Problems Summary

This file condenses the larger lesson report into recurring problem families that can later be paired with positive examples from the OpenWrt source tree.

## Overview

- Total lesson candidates: 4822
- Categories represented: 13
- Each section below shows high-frequency keyword signals and representative referenced threads.

## build-system

- Lesson candidates: 1010
- Completeness: complete=529, fragmentary=253, problem-only=32, searchable=196
- Common signals: linux, target, package, build-system, hunk:, diff:, struct, set, openwrt, kernel, mode, kernel-driver

Representative referenced problems:

### Add GS1900-8HP v1/v2 support and GS1900 DTSI: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt
- Root message ID: <20210108133248.13606-1-foss@volatilesystems.org>
- Problem excerpt: Create a common DTSI in preparation for
GS1900-8HP support, and switch to the macros defined in rtl838x.dtsi.. Signed-off-by: Stijn Segers <foss at volatilesystems.org>
---
 .../realtek/dts/rtl8380_zyxel_gs1900-10hp.dts | 233 +-----------------
 .../realtek/dts/rtl8380_zyxel_gs1900.dtsi     | 146 +++++++++++
 2 files changed, 151 insertions(+), 228 deletions(-)
 create mode 100644 target/linux/realtek/dts/rtl8380_zyxel_gs1900.dtsi.
[diff: target/linux/realtek/dts/rtl8380_zyxel_gs1900-10hp.dts]
-#include "rtl838x.dtsi"
+#include "rtl8380_zyxel_gs1900.dtsi"
-	aliases {
-		led-boot = &led_sys;
-		led-failsafe = &led_sys;
-		led-running = &led_sys;
-		led-upgrade = &led_sys;
-};
-&spi0 {
-	status = "okay";
-	flash at 0 {
-		compatible = "jedec,spi-nor";
[diff: target/linux/realtek/dts/rtl8380_zyxel_gs1900.dtsi]
+// SPDX-License-Identifier: GPL-2.0-or-later
+#include "rtl838x.dtsi"
+#include <dt-bindings/input/input.h>
+#include <dt-bindings/gpio/gpio.h>
+/ {
- Mentioned files: target/linux/realtek/base-files/etc/board.d/02_network, target/linux/realtek/dts/rtl8380_zyxel_gs1900-10hp.dts, target/linux/realtek/dts/rtl8380_zyxel_gs1900-8hp-v1.dts, target/linux/realtek/dts/rtl8380_zyxel_gs1900-8hp-v2.dts, target/linux/realtek/dts/rtl8380_zyxel_gs1900.dtsi

### Add support for Chromium OS and Google WiFi: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt
- Root message ID: <20210117030707.1251501-1-computersforpeace@gmail.com>
- Problem excerpt: The GUID is also recognized in fdisk, and likely other utilities, but
creation/manipulation is typically done via the 'cgpt' utility, provided
as part of the vboot_reference project.. Signed-off-by: Brian Norris <computersforpeace at gmail.com>
---
 tools/firmware-utils/src/ptgen.c | 39 +++++++++++++++++++++++++++++---
 1 file changed, 36 insertions(+), 3 deletions(-).
[diff: tools/firmware-utils/src/ptgen.c]
[hunk: typedef struct {]
+#define GUID_PARTITION_CHROME_OS_KERNEL \
+	GUID_INIT( 0xFE3A2A5D, 0x4F32, 0x41A7, \
+			0xB7, 0x25, 0xAC, 0xCC, 0x32, 0x85, 0xA3, 0x09)
[hunk: struct partinfo {]
+	bool has_gtype;
+	guid_t gtype;  /* GPT partition type */
+	uint64_t gattr;  /* GPT partition attributes */
[hunk: static inline int guid_parse(char *buf, guid_t *guid)]
+/* Map GPT partition types to partition GUIDs. */
+static inline bool parse_gpt_parttype(const char *type, struct partinfo *part)
+{
+	if (!strcmp(type, "cros_kernel")) {
+		part->has_gtype = true;
[hunk: static int gen_gptable(uint32_t signature, guid_t guid, unsigned nr)]
-		if (parts[i].type == 0xEF || (i + 1) == (unsigned)active) {
+		if (parts[i].has_gtype) {
+			gpte[i].type = parts[i].gtype;
+		} else if (parts[i].type == 0xEF || (i + 1) == (unsigned)active) {
+		gpte[i].attr = parts[i].gattr;
[hunk: fail:]
-	fprintf(stderr, "Usage: %s [-v] [-n] [-g] -h <heads> -s <sectors> -o <outputfile> [-a 0..4] [-l <align kB>] [-G <guid>] [[-t <type>] -p <size>[@<start>]...] \n", prog);
+	fprintf(stderr, "Usage: %s [-v] [-n] [-g] -h <heads> -s <sectors> -o <outputfile>\n"
+			"          [-a 0..4] [-l <align kB>] [-G <guid>]\n"
+			"          [[-t <type> | -T <GPT part type>] -p <size>[@<start>]...] \n", prog);
[hunk: int main (int argc, char **argv)]
-	while ((ch = getopt(argc, argv, "h:s:p:a:t:o:vngl:S:G:")) != -1) {
+	while ((ch = getopt(argc, argv, "h:s:p:a:t:T:o:vngl:S:G:")) != -1) {
[hunk: int main (int argc, char **argv)]
+		case 'T':
+			if (!parse_gpt_parttype(optarg, &parts[part])) {
+				fprintf(stderr,
+					"Invalid GPT partition type \"%s\"\n",
+					optarg);
- Mentioned files: include/gpt.h, include/image-commands.mk, lib/cgptlib/include/cgptlib_internal.h, lib/upgrade/common.sh, lib/upgrade/platform.sh

### add ubus support to ltq-[v|a]dsl-app: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt
- Root message ID: <20210126080052.750121-1-a.heider@gmail.com>
- Problem excerpt: v3:
- copy dsl_cpe_ubus.c from ltq-adsl-app to ltq-vdsl-app instead of using
  a symlink
- squash PKG_RELEASE patches
- move feed patches to PRs:
  https://github.com/openwrt/packages/pull/14572
  https://github.com/openwrt/luci/pull/4749.
v2:
- drop 0002-ltq-vdsl-app-fix-Wundef-warnings.patch
- use "/dev/dsl_cpe_api" without the "0" suffix for the adsl daemon:
  package/kernel/lantiq/ltq-adsl/patches/100-dsl_compat.patch:+   device_create(dsl_class, NULL, MKDEV(DRV_DSL_CPE_API_DEV_MAJOR, 0), NULL, "dsl_cpe_api");
  package/kernel/lantiq/ltq-vdsl/patches/100-compat.patch:+   device_create(dsl_class, NULL, dsl_devt, NULL, "dsl_cpe_api0");
- use callDSLMetrics() for luci, per jo
- add Tested-by tags. This is to significantly speed up the generation of the metrics.. The motivation comes from the fact that ~2.6s is just way too
ineffcient for interval based metric collectors like prometheus or
collectd..
- Mentioned files: lib/functions/lantiq_dsl.sh, package/kernel/lantiq/ltq-adsl/patches/100-dsl_compat.patch, package/kernel/lantiq/ltq-vdsl/patches/100-compat.patch, package/network/config/ltq-adsl-app/Makefile, package/network/config/ltq-adsl-app/files/dsl_control

### Advice re auto-extroot for EcoNet platform: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2025-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2025-September.txt
- Root message ID: <13146.1757878583@obiwan.sandelman.ca>
- Problem excerpt: If it exists at the
    > time the extroot is first mounted, we can copy files over, but if we boot
    > with the extroot removed, data will be stored there again and it will go out
    > of sync. We can imagine creating an init script which prints a warning in
    > this case, but the risk will always be present. My preference, because
    > I. Panic, flash available LEDs?
extroot seems like an "us" problem, not a user problem.

### aquantia-firmware: package MediaTek's Aquantia AQR113C firmware: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2024-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2024-February.txt
- Root message ID: <ZcDu8x0L5qzhZC25@makrotopia.org>
- Problem excerpt: Change-Id: Iddc29f5e1c73c772bcea9313938b6daccc10025a
     Reviewed-on: https://gerrit.mediatek.inc/c/openwrt/feeds/mtk_openwrt_feeds/+/6781059.
with not licensing details.. Later there was a firmware update update handled by adding file:
Rhe-05.06-Candidate9-AQR_Mediatek_23B_P5_ID45824_LCLVER1.cld in the commit:.
commit 405b1e31f924b97d379719fb39f0d28c0fac43a9
Author: developer <developer at mediatek.com>
Date:   Tue Mar 28 17:00:41 2023 +0800.
     [][kernel][mt7988][eth][Fix AQR113C 5GBASE-T compliance test mode4 tone1 fail issue].
     [Description]
     Fix AQR113C 5GBASE-T compliance test mode4 tone1 fail issue by
     updating firmware version to
     Rhe-05.06-Candidate9-AQR_Mediatek_23B_P5_ID45824_LCLVER1.cld.. If without this patch, AQR113C might not pass the 5GBASE-T mode4 tone1
     items for the compliance test..
     [Release-log]
     N/A. Change-Id: I3b2c6e6cf1a6ba8183daa7e30110ff2c839c5989
     Reviewed-on: https://gerrit.mediatek.inc/c/openwrt/feeds/mtk_openwrt_feeds/+/7305781.
but again with not licensing info..
- Mentioned files: package/firmware/aquantia-firmware/Makefile

---

## c-language

- Lesson candidates: 297
- Completeness: complete=175, fragmentary=73, problem-only=7, searchable=42
- Common signals: c-language, int, struct, hunk:, static, option, char, you, const, https:, openwrt, can

Representative referenced problems:

### ath79 / TP-Link CPE510 / tftp: recovery.bin: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-November.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt
- Root message ID: <20211112080952.hm6tegdqwx5533a6@email>
- Problem excerpt: The bootloader says:
Incorrect File. Writting error.. Anyway: does somebody know how to access the bootloader? The password 'admin' or 'tpl' is not accepted and
images are also not accepted..

### Backports b43 fix No 2GHz EPA gain table available for this device on phy rev 17 (bcm43217): mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-July.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-July.txt
- Root message ID: <PR2PR09MB31808894FCD0106C17A95EF0CB8E9@PR2PR09MB3180.eurprd09.prod.outlook.com>
- Problem excerpt: Gain table is missing for rev 17 phy causing error:
b43-phy0 ERROR: No 2GHz EPA gain table available for this device. Table taken from wl driver with version string 6.37.14.4803.cpe4.14L04.0. This chip (bcm43217) only seems to be used in routers so I don't see much point sending the patch to linux-wireless.
- Mentioned files: package/kernel/mac80211/patches/brcm/1001-add-tx-gain-epa-phy-rev17-table.patch

### devices: add support for declaring compatible matched devices: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-January.txt
- Root message ID: <20230109172812.28488-1-ansuelsmth@gmail.com>
- Problem excerpt: When a device is matched using compatible in iwinfo the hardware will be
flagged as embedded and won't print empty ids.. Tested-by: Christian Marangi <ansuelsmth at gmail.com>
Co-developed-by: Christian Marangi <ansuelsmth at gmail.com>
Signed-off-by: Jo-Philipp Wich <jo at mein.io>
Signed-off-by: Christian Marangi <ansuelsmth at gmail.com>
---
 devices.txt      | 13 +++++++++
 include/iwinfo.h |  2 ++
 iwinfo_cli.c     |  9 ++++--
 iwinfo_nl80211.c | 71 ++++++------------------------------------------
 iwinfo_utils.c   |  8 +++++-
 5 files changed, 36 insertions(+), 67 deletions(-).
[diff: devices.txt]
+# FDT compatible strings
+# "compatible" | txpower offset | frequency offset | ...
+"qca,ar9130-wmac"       0      0  "Atheros"  "AR9130"
+"qca,ar9330-wmac"       0      0  "Atheros"  "AR9330"
+"qca,ar9340-wmac"       0      0  "Atheros"  "AR9340"
[diff: include/iwinfo.h]
[hunk: struct iwinfo_hardware_id {]
+	char compatible[128];
[hunk: struct iwinfo_hardware_entry {]
+	char compatible[128];
[diff: iwinfo_cli.c]
[hunk: static char * print_hardware_id(const struct iwinfo_ops *iw, const char *ifname)]
-		snprintf(buf, sizeof(buf), "%04X:%04X %04X:%04X",
-			ids.vendor_id, ids.device_id,
-			ids.subsystem_vendor_id, ids.subsystem_device_id);
+		if (strlen(ids.compatible) > 0)
+			snprintf(buf, sizeof(buf), "embedded");
[diff: iwinfo_nl80211.c]
[hunk: static int nl80211_get_mbssid_support(const char *ifname, int *buf)]
-	char *phy, compat[64], path[PATH_MAX];
+	char *phy, path[PATH_MAX];
[hunk: static int nl80211_hardware_id_from_fdt(struct iwinfo_hardware_id *id, const cha]
-	if (nl80211_readstr(path, compat, sizeof(compat)) <= 0)
+	if (nl80211_readstr(path, id->compatible, sizeof(id->compatible)) <= 0)
-	if (!strcmp(compat, "qca,ar9130-wmac")) {
-		id->vendor_id = 0x168c;
-		id->device_id = 0x0029;
[hunk: static int nl80211_get_hardware_id(const char *ifname, char *buf)]
-	/* Failed to obtain hardware IDs, try FDT */
-	if (id->vendor_id == 0 && id->device_id == 0 &&
-	    id->subsystem_vendor_id == 0 && id->subsystem_device_id == 0)
-		if (!nl80211_hardware_id_from_fdt(id, ifname))
-			return 0;
[diff: iwinfo_utils.c]
[hunk: struct iwinfo_hardware_entry * iwinfo_hardware(struct iwinfo_hardware_id *id)]
-			       e.vendor_name, e.device_name) < 8)
+			       e.vendor_name, e.device_name) != 8 &&
+			sscanf(buf, "\"%127[^\"]\" %hd %hd \"%63[^\"]\" \"%63[^\"]\"",
+			       e.compatible, &e.txpower_offset, &e.frequency_offset,
+			       e.vendor_name, e.device_name) != 5)
[hunk: struct iwinfo_hardware_entry * iwinfo_hardware(struct iwinfo_hardware_id *id)]
+		if (strcmp(e.compatible, id->compatible))
+			continue;
- Mentioned files: devices.txt, include/iwinfo.h, iwinfo_cli.c, iwinfo_nl80211.c, iwinfo_utils.c

### dms: add --get-operating-mode: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-December.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-December.txt
- Root message ID: <CAEJWX3E5BAws5t21SzMvvFoGP=0AYgidAHhcHSo7nzyCKnOfWQ@mail.gmail.com>
- Problem excerpt: This is for all LTE terminals.. I have a local uqmi version with commands for checking and modifying
the APN settings..
>
> > To make it possible to automate change of APN setting --get-operating-mode is
> > needed.
> >
> > Signed-off-by: Henrik Ginstmark <henrik at ginstmark.se>
>
> Your patch seems broken. Consider using git-format-patch and
> git-send-email to prepare and submit the patch, please.. Sorry, I?m new to this.

### fakeroot: fix to work with glibc 2.33: recurring problem pattern

- Score: 1.0
- Completeness: searchable
- Source file: devel/2021-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-February.txt
- Root message ID: <20210211031441.628215-1-ilya.lipnitskiy@gmail.com>
- Problem excerpt: The following commit removed _STAT_VER definitions from glibc:
https://sourceware.org/git/?p=glibc.git;a=commitdiff;h=8ed005daf0ab03e142500324a34087ce179ae78e. That subsequently broke fakeroot:
https://bugs.archlinux.org/task/69572
https://bugzilla.redhat.com/show_bug.cgi?id=1889862#c13
https://forum.openwrt.org/t/unable-to-build-toolchain-fakeroot-fails-perhaps-others-after-it/87966. Make the patch based on Jan Pazdziora's suggestion from here:
https://lists.fedoraproject.org/archives/list/devel at lists.fedoraproject.org/message/SMQ3RYXEYTVZH6PLQMKNB3NM4XLPMNZO/. Tested on my x86_64 Arch Linux machine, fakeroot unit tests pass..
- Mentioned files: tools/fakeroot/patches/100-portability.patch, tools/fakeroot/patches/300-glibc-2.33-compatibility.patch

---

## concurrency

- Lesson candidates: 575
- Completeness: complete=407, fragmentary=96, problem-only=20, searchable=52
- Common signals: linux, struct, target, hunk:, openwrt, mode, kernel:, static, signed-off-by:, package, concurrency, config

Representative referenced problems:

### add dlink-sge-image for D-Link devices by SGE: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-June.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-June.txt
- Root message ID: <20230623120600.16663-1-openwrt@sebastianschaper.net>
- Problem excerpt: A1 [3].. Further scripts (e.g. /lib/upgrade/) and keys were found in the GPL tarball
and/or rootfs of COVR-C1200 (the devices are based on OpenWrt Chaos Calmer
and failsafe can be entered by pressing 'f' on the serial console during
boot, allowing to access the file system of the running device).. For newer devices like COVR-X1860 and DIR-X3260, an updated method of
vendor key derivation is implemented based on enk.txt from the GPL release..
[1] https://0x00sec.org/t/breaking-the-d-link-dir3060-firmware-encryption-recon-part-1/21943
[2] https://github.com/0xricksanchez/dlink-decrypt
[3] https://tsd.dlink.com.tw/GPL.asp. Signed-off-by: Sebastian Schaper <openwrt at sebastianschaper.net>
Tested-By: Alan Luck <luckyhome2008 at gmail.com>
---.
- Mentioned files: CMakeLists.txt, src/dlink-sge-image.c, src/dlink-sge-image.h

### ARM BCM53573 SoC hangs/lockups caused by locks/clock/random changes: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-September.txt
- Root message ID: <a03a6e1d-e99c-40a3-bdac-0075b5339beb@gmail.com>
- Problem excerpt: I made a second attempt on debugging some longstanding stability issues
affecting BCM53753 SoCs. Those are single CPU core ARM Cortex-A7 boards
with a pretty slow arch timer running at 36,8 kHz.. After 0 to 20 minutes of close to zero activity I experience hangs and I
need to wait a minute for watchdog to kick in and reboot device..

### ARM board lockups/hangs triggered by locks and mutexes: recurring problem pattern

- Score: 1.0
- Completeness: searchable
- Source file: devel/2023-August.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-August.txt
- Root message ID: <CACna6rxpzDWE5-gnmpgMgfzPmmHvEGTZk4GJvJ8jLSMazh2bVA@mail.gmail.com>
- Problem excerpt: We released
firmwares based on Linux 4.4 (and later on 4.14) that worked almost
fine. There was one little issue we couldn't debug or fix: random hangs
and reboots. They were too rare to deal with (most devices worked fine
for weeks or months).. Recently I updated my stable kernel 5.4 and I started experiencing
stability issues on my own!
- Mentioned files: drivers/mtd/mtdchar.c, drivers/mtd/mtdcore.c, kernel/locking/mutex-debug.c

### arm-trusted-firmware-mvebu: CZ.NIC's Secure Firmware bump to v2021.09.07: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-September.txt
- Root message ID: <MEAPR01MB3574140E649A556BE964A3BEC0DA9@MEAPR01MB3574.ausprd01.prod.outlook.com>
- Problem excerpt: bump version and remove patches that have been applied. 176d701 wtmi: Wait 1s after putting PHYs INTn pin low
2eeccfe wtmi: Change comment describing reset workaround
e8c94a5 wtmi: Count RAM size from both CS0 and CS1
995979e wtmi: Rename macro
e29eb29 wtmi: soc: Fix start_ap_workaround() for TF-A with debug
81245ed wtmi: Use constant name PLAT_MARVELL_MAILBOX_BASE
18ccb83 wtmi: Do a proper UART reset with clock change as described in spec
15ff106 avs: Validate VDD value from OTP
3f33626 fix: clock: a3700: change pwm clock for 600/600 and 1200/750 preset
fb5e436 wtmi: uart: fix UART baudrate divisor calculation. Signed-off-by: sean lee <ilf at live.com>
---
 .../boot/arm-trusted-firmware-mvebu/Makefile  |  4 +-
 ...ix-UART-baudrate-divisor-calculation.patch | 66 -------------------
 ...change-pwm-clock-for-600-600-and-120.patch | 48 --------------
 .../102-avs-Validate-VDD-value-from-OTP.patch | 52 ---------------
 4 files changed, 2 insertions(+), 168 deletions(-)
 delete mode 100644 package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/100-wtmi-uart-fix-UART-baudrate-divisor-calculation.patch
 delete mode 100644 package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/101-fix-clock-a3700-change-pwm-clock-for-600-600-and-120.patch
 delete mode 100644 package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/102-avs-Validate-VDD-value-from-OTP.patch.
[diff: package/boot/arm-trusted-firmware-mvebu/Makefile]
[hunk: define Download/mv-ddr-marvell]
-MOX_BB_RELEASE:=v2021.04.09
+MOX_BB_RELEASE:=v2021.09.07
-  HASH:=f0ed4fa25006e36a07d4256f633e3f25d6f8898dbe2e081e578251a182885520
+  HASH:=fd5fe276a3b0dee3177d61c017907a8eb23cd2169478fa78e9a3a836cfe3a4a8
[diff: package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/100-wtmi-uart-fix-UART-baudrate-divisor-calculation.patch]
-From fb5e436843614f93b30aec0a2a00e5e59a133aab Mon Sep 17 00:00:00 2001
-From: =?UTF-8?q?Marek=20Beh=C3=BAn?= <marek.behun at nic.cz>
-Date: Sat, 15 May 2021 17:44:24 +0200
-Subject: [PATCH] wtmi: uart: fix UART baudrate divisor calculation
-MIME-Version: 1.0
- Mentioned files: package/boot/arm-trusted-firmware-mvebu/Makefile, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/100-wtmi-uart-fix-UART-baudrate-divisor-calculation.patch, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/101-fix-clock-a3700-change-pwm-clock-for-600-600-and-120.patch, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/102-avs-Validate-VDD-value-from-OTP.patch, package/boot/arm-trusted-firmware-mvebu/patches/001-imagetool.patch

### arm-trusted-firmware-mvebu: CZ.NIC's Secure Firmware bump to v2021.09.07: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-September.txt
- Root message ID: <MEAPR01MB3574E3F34BA95DC3E8802A9DC0D99@MEAPR01MB3574.ausprd01.prod.outlook.com>
- Problem excerpt: bump version and remove patches that have been applied. 176d701 wtmi: Wait 1s after putting PHYs INTn pin low
2eeccfe wtmi: Change comment describing reset workaround
e8c94a5 wtmi: Count RAM size from both CS0 and CS1
995979e wtmi: Rename macro
e29eb29 wtmi: soc: Fix start_ap_workaround() for TF-A with debug
81245ed wtmi: Use constant name PLAT_MARVELL_MAILBOX_BASE
18ccb83 wtmi: Do a proper UART reset with clock change as described in spec
15ff106 avs: Validate VDD value from OTP
3f33626 fix: clock: a3700: change pwm clock for 600/600 and 1200/750 preset
fb5e436 wtmi: uart: fix UART baudrate divisor calculation. Signed-off-by: sean lee <ilf at live.com>
---
  .../boot/arm-trusted-firmware-mvebu/Makefile  |  4 +-
  ...ix-UART-baudrate-divisor-calculation.patch | 66 -------------------
  ...change-pwm-clock-for-600-600-and-120.patch | 48 --------------
  .../102-avs-Validate-VDD-value-from-OTP.patch | 52 ---------------
  4 files changed, 2 insertions(+), 168 deletions(-)
  delete mode 100644 
package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/100-wtmi-uart-fix-UART-baudrate-divisor-calculation.patch
  delete mode 100644 
package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/101-fix-clock-a3700-change-pwm-clock-for-600-600-and-120.patch
  delete mode 100644 
package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/102-avs-Validate-VDD-value-from-OTP.patch.
[diff: package/boot/arm-trusted-firmware-mvebu/Makefile]
[hunk: define Download/mv-ddr-marvell]
-MOX_BB_RELEASE:=v2021.04.09
+MOX_BB_RELEASE:=v2021.09.07
-  HASH:=f0ed4fa25006e36a07d4256f633e3f25d6f8898dbe2e081e578251a182885520
+  HASH:=fd5fe276a3b0dee3177d61c017907a8eb23cd2169478fa78e9a3a836cfe3a4a8
-From fb5e436843614f93b30aec0a2a00e5e59a133aab Mon Sep 17 00:00:00 2001
-From: =?UTF-8?q?Marek=20Beh=C3=BAn?= <marek.behun at nic.cz>
-Date: Sat, 15 May 2021 17:44:24 +0200
-Subject: [PATCH] wtmi: uart: fix UART baudrate divisor calculation
-MIME-Version: 1.0
- Mentioned files: package/boot/arm-trusted-firmware-mvebu/Makefile, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/100-wtmi-uart-fix-UART-baudrate-divisor-calculation.patch, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/101-fix-clock-a3700-change-pwm-clock-for-600-600-and-120.patch, package/boot/arm-trusted-firmware-mvebu/patches-mox-boot-builder/102-avs-Validate-VDD-value-from-OTP.patch

---

## kernel-driver

- Lesson candidates: 399
- Completeness: complete=262, fragmentary=95, problem-only=18, searchable=24
- Common signals: kernel-driver, linux, you, target, kernel, can, https:, following, did, dts, openwrt, details

Representative referenced problems:

### Add package version dependency for point releases: recurring problem pattern

- Score: 1.0
- Completeness: problem-only
- Source file: devel/2021-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt
- Root message ID: <ccbfe5674a2def7208d3eaace8652a1f@dev.tdt.de>
- Problem excerpt: I just realized (thanks to @brianjmurrell [1]) that in a stable release, 
this is quite important.. The problem is, that a bug fix has been added to the kernel, which makes 
a workaround in mwan3 superfluous. This workaround in the mwan3 I have now reverted. Since this is no 
longer needed.

### ath79/zyxel_nbg6716: resize kernel partition to 6MiB and reenable again: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210522150035.19310-1-avalentin@marcant.net>
- Problem excerpt: Alternatively, you can flash sysupgrade-6M-Kernel.bin with
 zcat sysupgrade-6M-Kernel.bin | mtd -r -e /dev/mtd 3 write - /dev/mtd3. This may thow an error, because it is a 256M image. There are
devices out there with this flash size.. Notice that you will always loose configuration..
- Mentioned files: target/linux/ath79/dts/qca9558_zyxel_nbg6716.dts, target/linux/ath79/image/nand.mk

### ath79: add support for Mikrotik RouterBoard 912G: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210521110503.5568-1-denis281089@gmail.com>
- Problem excerpt: But only one can be used.
* LEDs: 5 general purpose LEDs (led1..led5), power LED, user LED,
  Ethernet phy LED,
* Button,
* Beeper.. Not working:
* Button: it shares gpio line 15 with NAND ALE and NAND IO7,
  and current drivers doesn't easily support this configuration,
* Beeper: it is connected to bit 5 of a serial shift register
  (tested with sysfs led trigger timer). But kmod-gpio-beeper
  doesn't work -- we left this as is for now.. You can flash image by sysupgrade utility or load it by net
(by DHCP/TFTP, hold the button while booting)..
- Mentioned files: lib/upgrade/platform.sh, target/linux/ath79/dts/ar9342_mikrotik_routerboard-912g.dts, target/linux/ath79/files/drivers/gpio/gpio-latch.c, target/linux/ath79/files/drivers/mtd/nand/raw/rb91x_nand.c, target/linux/ath79/image/mikrotik.mk

### ath79: add support for reset key on MikroTik RB912UAG-2HPnD: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-January.txt
- Root message ID: <51a65989-f39e-f7d5-cdfe-e673b1e0f7ae@citymesh.com>
- Problem excerpt: On 19.01.22 11:25, Denis Kalashnikov wrote:
> On MikroTik RB91x board series a reset key shares SoC gpio
> line #15 with NAND ALE and NAND IO7. So we need a custom
> gpio driver to manage this non-trivial connection schema.
> Also rb91x-nand needs to have an ability to disable a polling
> of the key while it works with NAND.
>
> While we've been integrating rb91x-key into a firmware, we've
> figured out that:
> * In the gpio-latch driver we need to add a "cansleep" suffix to
> several gpiolib calls,
> * When gpio-latch and rb91x-nand fail to get a gpio and an error
> is -EPROBE_DEFER, they shouldn't report about this, since this
> actually is not an error and occurs when the gpio-latch probe
> function is called before the rb91x-key probe.
> We fix these related things here too.
>
> Signed-off-by: Denis Kalashnikov <denis281089 at gmail.com>
> ---
>
> Changelog:
>
> v1 --> v2:
> * Remove support for kernel 5.4,
> * gpio-latch and rb91x-nand don't report about -EPROBE_DEFER.
>
This one is actually v3 :-). No worries :y. Koen
- Mentioned files: target/linux/ath79/config-5.10, target/linux/ath79/dts/ar9342_mikrotik_routerboard-912uag-2hpnd.dts, target/linux/ath79/files/drivers/gpio/gpio-latch.c, target/linux/ath79/files/drivers/gpio/gpio-rb91x-key.c, target/linux/ath79/files/drivers/mtd/nand/raw/rb91x_nand.c

### ath79: convert QCA955x-based D-Link DAP-2xxx to nvmem: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-June.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-June.txt
- Root message ID: <cover.1655151247.git.sander@svanheule.net>
- Problem excerpt: 15.751865] ath10k_pci 0000:00:00.0: qca9984/qca9994 hw1.0 target 
0x01000000 chip_id 0x00000000 sub 168c:cafe
[?? 15.761962] ath10k_pci 0000:00:00.0: kconfig debug 0 debugfs 1 
tracing 0 dfs 1 testmode 0
[?? 15.781211] ath10k_pci 0000:00:00.0: firmware ver 
10.4b-ct-9984-fW-13-5ae337bb1 api 5 features 
mfp,peer-flow-ctrl,txstatus-noack,wmi-10.x-CT,ratemask-CT,regdump-CT,txrate-CT,flush-all-CT,pingpong-CT,ch-regs-CT,nop-CT,set-special-CT,tx-rc-CT,cust-stats-CT,txrate2-CT,beacon-cb-CT,wmi-block-ack-CT,wmi-bcn-rc-CT 
crc32 7ea63dc5
[?? 18.114113] ath10k_pci 0000:00:00.0: Loading BDF type 0
[??
- Mentioned files: target/linux/ath79/dts/qca9557_dlink_dap-2660-a1.dts, target/linux/ath79/dts/qca9558_dlink_dap-2680-a1.dts, target/linux/ath79/dts/qca9558_dlink_dap-2695-a1.dts, target/linux/ath79/dts/qca9558_dlink_dap-3662-a1.dts, target/linux/ath79/dts/qca955x_dlink_dap-2xxx.dtsi

---

## luci-frontend

- Lesson candidates: 41
- Completeness: complete=27, fragmentary=8, problem-only=3, searchable=3
- Common signals: https:, openwrt, luci-frontend, you, include, type, can, home, feckert, target.mk:256:, cpu_type, doesn

Representative referenced problems:

### comgt-ncm: add support for quectel modem EC200T-EU: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-November.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-November.txt
- Root message ID: <20221130093343.2796646-1-git@aiyionpri.me>
- Problem excerpt: On 11/30/22 10:41, Ar?n? ?NAL wrote:
> On 30.11.2022 12:33, Jan-Niklas Burfeind wrote:
>> Wavlink WS-WN572HP3 4G is an 802.11ac
>> dual-band outdoor router with LTE support.
>>
>> Specifications;
>> * Soc: MT7621DAT
>> * RAM: 128MiB
>> * Flash: NOR 16MiB GD-25Q128ESIG3
>> * Wi-Fi:
>> ?? * MT7613BEN: 5GHz
>> ?? * MT7603EN: 2.4GHz
>> * Ethernet: 2x 1GbE
>> * USB: None - only used internally
>> * LTE Modem: Quectel EC200T-EU
>> * UART: 115200 baud
>> * LEDs:
>> ?? * 7 blue at the front
>> ???? * 1 Power
>> ???? * 2 LAN / WAN
>> ???? * 1 Status
>> ???? * 3 RSSI (annotated 4G)
>> ?? * 1 green at the bottom (4G LED)
>> * Buttons: 1 reset button
>>
>> Installation:
>> * press and hold the reset button while powering on the device
>> * keep it pressed for ten seconds
>> * connect to 192.168.10.1 via webbrowser (chromium/chrome works, at
>> ?? least Firefox 106.0.3 does not)
>> * upload the sysupgrade image, confirm the checksum, wait 2 minutes
>> ?? until the device reboots
>>
>> Revert to stock firmware:
>> * same as installation but use the recovery image for WL-WN572HP3
>>
>> Signed-off-by: Jan-Niklas Burfeind <git at aiyionpri.me>
> 
> Acked-by: Ar?n? ?NAL <arinc.unal at arinc9.com>
> 
> Ar?n?
> . Something must've gone wrong. Connecting the lan port does not trigger a log message anymore. WAN still does:
982.295568] mtk_soc_eth 1e100000.ethernet wan: Link is Up - 1Gbps/Full - 
flow control rx/tx.
- Mentioned files: package/network/utils/comgt/files/ncm.json, package/network/utils/comgt/files/ncm.sh, target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts, target/linux/ramips/image/mt7621.mk, target/linux/ramips/mt7621/base-files/etc/board.d/02_network

### comgt-ncm: add support for quectel modem EC200T-EU: recurring problem pattern

- Score: 1.0
- Completeness: searchable
- Source file: devel/2022-November.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-November.txt
- Root message ID: <20221130164446.2876317-1-git@aiyionpri.me>
- Problem excerpt: s-2 made me aware of an LED rssi issue; this is not ready to merge yet.. On 11/30/22 17:44, Jan-Niklas Burfeind wrote:
> Wavlink WS-WN572HP3 4G is an 802.11ac
> dual-band outdoor router with LTE support.
> 
> Specifications;
> * Soc: MT7621DAT
> * RAM: 128MiB
> * Flash: NOR 16MiB GD-25Q128ESIG3
> * Wi-Fi:
>    * MT7613BEN: 5GHz
>    * MT7603EN: 2.4GHz
> * Ethernet: 2x 1GbE
> * USB: None - only used internally
> * LTE Modem: Quectel EC200T-EU
> * UART: 115200 baud
> * LEDs:
>    * 7 blue at the front
>      * 1 Power
>      * 2 LAN / WAN
>      * 1 Status
>      * 3 RSSI (annotated 4G)
>    * 1 green at the bottom (4G LED)
> * Buttons: 1 reset button
> 
> Installation:
> * press and hold the reset button while powering on the device
> * keep it pressed for ten seconds
> * connect to 192.168.10.1 via webbrowser (chromium/chrome works, at
>    least Firefox 106.0.3 does not)
> * upload the sysupgrade image, confirm the checksum, wait 2 minutes
>    until the device reboots
> 
> Revert to stock firmware:
> * same as installation but use the recovery image for WL-WN572HP3
> 
> Signed-off-by: Jan-Niklas Burfeind <git at aiyionpri.me>
> ---
>   .../dts/mt7621_wavlink_ws-wn572hp3-4g.dts     | 183 ++++++++++++++++++
>   target/linux/ramips/image/mt7621.mk           |  17 ++
>   .../mt7621/base-files/etc/board.d/02_network  |   1 +
>   3 files changed, 201 insertions(+)
>   create mode 100644 target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts
> 
> diff --git a/target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts b/target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts
> new file mode 100644
> index 0000000000..a9b6b7a0df
> --- /dev/null
> +++ b/target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts
> @@ -0,0 +1,183 @@
> +// SPDX-License-Identifier: GPL-2.0-or-later OR MIT
> +
> +#include "mt7621.dtsi"
> +
> +#include <dt-bindings/gpio/gpio.h>
> +#include <dt-bindings/input/input.h>
> +
> +/ {
> +	compatible = "wavlink,ws-wn572hp3-4g", "mediatek,mt7621-soc";
> +	model = "Wavlink WS-WN572HP3 4G";
> +
> +	chosen {
> +		bootargs = "console=ttyS0,115200";
> +	};
> +
> +	aliases {
> +		led-boot = &led_status_blue;
> +		led-failsafe = &led_status_blue;
> +		led-running = &led_status_blue;
> +		led-upgrade = &led_status_blue;
> +	};
> +
> +	keys {
> +		compatible = "gpio-keys";
> +
> +		reset {
> +			label = "Reset Button";
> +			gpios = <&gpio 18 GPIO_ACTIVE_LOW>;
> +			linux,code = <KEY_RESTART>;
> +		};
> +	};
> +
> +	leds {
> +		compatible = "gpio-leds";
> +
> +		rssihigh {
> +			label = "blue:rssihigh";
> +			gpios = <&gpio 68 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		rssimedium {
> +			label = "blue:rssimedium";
> +			gpios = <&gpio 81 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		rssilow {
> +			label = "blue:rssilow";
> +			gpios = <&gpio 80 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		led_status_blue: status_blue {
> +			label = "blue:status";
> +			gpios = <&gpio 67 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		// gpio 79 would be Quectels PWRKEY if used
> +	};
> +};
> +
> +&spi0 {
> +	status = "okay";
> +
> +	flash at 0 {
> +		compatible = "jedec,spi-nor";
> +		reg = <0>;
> +		spi-max-frequency = <40000000>;
> +
> +		partitions {
> +			compatible = "fixed-partitions";
> +			#address-cells = <1>;
> +			#size-cells = <1>;
> +
> +			partition at 0 {
> +				label = "u-boot";
> +				reg = <0x0 0x30000>;
> +				read-only;
> +			};
> +
> +			partition at 30000 {
> +				label = "config";
> +				reg = <0x30000 0x10000>;
> +				read-only;
> +			};
> +
> +			factory: partition at 40000 {
> +				label = "factory";
> +				reg = <0x40000 0x10000>;
> +				read-only;
> +			};
> +
> +			partition at 50000 {
> +				compatible = "denx,fit";
> +				label = "firmware";
> +				reg = <0x50000 0xf30000>;
> +			};
> +
> +			partition at f00000 {
> +				label = "vendor";
> +				reg = <0xf80000 0x80000>;
> +				read-only;
> +			};
> +		};
> +	};
> +};
> +
> +&pcie {
> +	status = "okay";
> +};
> +
> +&pcie0 {
> +	wifi0: mt76 at 0,0 {
> +		compatible = "mediatek,mt76";
> +		reg = <0x0000 0 0 0 0>;
> +		mediatek,mtd-eeprom = <&factory 0x0>;
> +	};
> +};
> +
> +&pcie1 {
> +	wifi1: mt76 at 0,0 {
> +		compatible = "mediatek,mt76";
> +		reg = <0x0000 0 0 0 0>;
> +		mediatek,mtd-eeprom = <&factory 0x8000>;
> +	};
> +};
> +
> +&gmac0 {
> +	nvmem-cells = <&macaddr_factory_e000>;
> +	nvmem-cell-names = "mac-address";
> +};
> +
> +&gmac1 {
> +	status = "okay";
> +	label = "wan";
> +	phy-handle = <&ethphy4>;
> +
> +	nvmem-cells = <&macaddr_factory_e006>;
> +	nvmem-cell-names = "mac-address";
> +};
> +
> +&mdio {
> +	ethphy4: ethernet-phy at 4 {
> +		reg = <4>;
> +	};
> +};
> +
> +&switch0 {
> +	ports {
> +		port at 1 {
> +			status = "okay";
> +			label = "lan";
> +		};
> +	};
> +};
> +
> +&state_default {
> +	gpio {
> +		groups = "wdt";
> +		function = "gpio";
> +	};
> +};
> +
> +&factory {
> +	compatible = "nvmem-cells";
> +	#address-cells = <1>;
> +	#size-cells = <1>;
> +
> +	macaddr_factory_e000: macaddr at e000 {
> +		reg = <0xe000 0x6>;
> +	};
> +
> +	macaddr_factory_e006: macaddr at e006 {
> +		reg = <0xe006 0x6>;
> +	};
> +};
> +
> +&wifi0{
> +	ieee80211-freq-limit = <2400000 2500000>;
> +};
> +
> +&wifi1{
> +	ieee80211-freq-limit = <5000000 6000000>;
> +};
> +
> diff --git a/target/linux/ramips/image/mt7621.mk b/target/linux/ramips/image/mt7621.mk
> index 943fc62ecd..4028e43e39 100644
> --- a/target/linux/ramips/image/mt7621.mk
> +++ b/target/linux/ramips/image/mt7621.mk
> @@ -2158,6 +2158,23 @@ define Device/wavlink_wl-wn533a8
>   endef
>   TARGET_DEVICES += wavlink_wl-wn533a8
>   
> +define Device/wavlink_ws-wn572hp3-4g
> +  $(Device/dsa-migration)
> +  BLOCKSIZE := 64k
> +  DEVICE_VENDOR := Wavlink
> +  DEVICE_MODEL := WS-WN572HP3
> +  DEVICE_VARIANT := 4G
> +  IMAGE_SIZE := 15040k
> +  KERNEL_LOADADDR := 0x82000000
> +  KERNEL := kernel-bin | relocate-kernel 0x80001000 | lzma | \
> +	fit lzma $$(KDIR)/image-$$(firstword $$(DEVICE_DTS)).dtb
> +  IMAGE/sysupgrade.bin := append-kernel | pad-to $$$$(BLOCKSIZE) | \
> +	append-rootfs | pad-rootfs | check-size | append-metadata
> +  DEVICE_PACKAGES := kmod-mt7603 kmod-mt7615e kmod-mt7663-firmware-ap \
> +	kmod-usb3 kmod-usb-net-rndis comgt-ncm
> +endef
> +TARGET_DEVICES += wavlink_ws-wn572hp3-4g
> +
>   define Device/wevo_11acnas
>     $(Device/dsa-migration)
>     $(Device/uimage-lzma-loader)
> diff --git a/target/linux/ramips/mt7621/base-files/etc/board.d/02_network b/target/linux/ramips/mt7621/base-files/etc/board.d/02_network
> index c4fe2153ac..b7121db64f 100644
> --- a/target/linux/ramips/mt7621/base-files/etc/board.d/02_network
> +++ b/target/linux/ramips/mt7621/base-files/etc/board.d/02_network
> @@ -50,6 +50,7 @@ ramips_setup_interfaces()
>   		;;
>   	asiarf,ap7621-001|\
>   	humax,e10|\
> +	wavlink,ws-wn572hp3-4g|\
>   	winstars,ws-wn583a6)
>   		ucidef_set_interfaces_lan_wan "lan" "wan"
>   		;;
- Mentioned files: package/network/utils/comgt/files/ncm.json, package/network/utils/comgt/files/ncm.sh, target/linux/ramips/dts/mt7621_wavlink_ws-wn572hp3-4g.dts, target/linux/ramips/image/mt7621.mk, target/linux/ramips/mt7621/base-files/etc/board.d/02_network

### lua 5.1.5 CVEs: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-October.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-October.txt
- Root message ID: <5f9494a4-7bae-b973-0db8-ad3f2695fbe9@chocky.org>
- Problem excerpt: Lua 5.1.5 would appear to have CVEs below against it.. The patches to this in OpenWrt are significant, but dated, with the
last bug fix seeming to be from 2019, so it's hard to say if
these are addressed:.
https://github.com/openwrt/openwrt/tree/openwrt-22.03/package/utils/lua/patches.
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15888.
https://github.com/lua/lua/commit/6298903e35217ab69c279056f925fb72900ce0b7
https://github.com/lua/lua/commit/eb41999461b6f428186c55abd95f4ce1a76217d5. I can't see that these have been applied - correct me here please..
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43519. This appears to be the fix:.
https://github.com/lua/lua/commit/6298903e35217ab69c279056f925fb72900ce0b7.
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15945.

### OpenWrt 24.10 release status: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2025-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt
- Root message ID: <da710280-e3e2-46ea-8e8e-2c44cb1d2e70@hauke-m.de>
- Problem excerpt: Feel free to backport 
stuff if needed.. There are still some regression compared to 23.05. These are the big regressions affecting multiple people I am aware of..
ath10k: 5 GHz radio not detected:
https://github.com/openwrt/openwrt/issues/14541
	This affects multiple devices with ath10k radio..
mt7621: Periodic link down+up since 24.10.0-rc*
https://github.com/openwrt/openwrt/issues/17351
	It looks like there is a regression in the PHY driver for
	mt7621. When people deactivate EEE it works more stable..
- Mentioned files: feeds/mtk-openwrt-feeds/+/refs/heads/master/autobuild/unified/global/24.10/files/target/linux/mediatek/patches-6.6/999-2700-net-ethernet-mtk_eth_soc-add-mdio-reset-delay.patch, target/linux/mediatek/dts/mt7622-netgear-wax206.dts

### build: add explicit timezone in CycloneDX SBOM: mistake and correction

- Score: 0.95
- Completeness: complete
- Source file: devel/2024-June.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2024-June.txt
- Root message ID: <20240604160003.1178243-1-roman.azarenko@iopsys.eu>
- Problem excerpt: This is causing problems with OWASP Dependency-Track version 4.11.0 or
newer, where it now validates submitted SBOMs against the JSON schema
by default [4]. SBOMs with incorrect timestamp values are rejected with
the following error:.
	{
	    "detail": "Schema validation failed",
	    "errors": [
	        "$.metadata.timestamp: 2024-06-03T15:51:10 is an invalid date-time"
	    ],
	    "status": 400,
	    "title": "The uploaded BOM is invalid"
	}. Add explicit `Z` (UTC) timezone offset in the `timestamp` field
to satisfy the CycloneDX schema..
[1]: https://github.com/CycloneDX/specification/blob/1.4/schema/bom-1.4.schema.json#L116-L121
[2]: https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01#rfc.section.7.3.1
[3]: https://datatracker.ietf.org/doc/html/rfc3339#section-5.6
[4]: https://github.com/DependencyTrack/dependency-track/pull/3522. Signed-off-by: Roman Azarenko <roman.azarenko at iopsys.eu>
---
 scripts/package-metadata.pl | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-).
[diff: scripts/package-metadata.pl]
[hunk: sub dump_cyclonedxsbom_json {]
-			timestamp => gmtime->datetime,
+			timestamp => gmtime->datetime . 'Z',
- Mentioned files: scripts/package-metadata.pl

---

## memory-management

- Lesson candidates: 148
- Completeness: complete=97, fragmentary=11, problem-only=17, searchable=23
- Common signals: set, linux, target, struct, generic, backport-5.4, int, static, pci, void, diff:, memory-management

Representative referenced problems:

### Adds pcre2 to base: recurring problem pattern

- Score: 1.0
- Completeness: searchable
- Source file: devel/2022-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-May.txt
- Root message ID: <20220519130333.159011-1-dominick.grift@defensec.nl>
- Problem excerpt: 50a51cb Fixed a unicode properrty matching issue in JIT
f7a7341 Update ucd.c generation script for overlong initializer
eef5740 Remove overlooked excess initializer
dea56d2 JIT compiler update. 111cd47 Fix typo `with-match-limit_depth` -> `with-match-limit-depth` (#83)
fdd9479 Fix incorrect compiling when [Aa] etc. are quantified
419e3c6 Tidy comments
e21345d Extend unicode boolean property bitset index to 12 bit (#81)
e85a81e Correct CMakeLists.txt for MSVC debugger file names
504ff06 Fix overrun bug in recent property name parsing change
360a84e Update descriptive comments in UCD generation. 061e576 Merge scriptx and bidi fields (#78)
7f7d3e8 Documentation update for binary property support
bf35c05 Add -LP and -LS (list properties, list scripts) features to pcre2test. 68fbc19 Support boolean properties in JIT (#76)
06d3a66 Fix bug in modifier listing
87571b5 Update documentation and comments for UCD generation
838cdac Remove vestiges of previous Bidi_Class coding
628a804 Tests for new Boolean properties
ec091e2 Restore lost de-duplication
636569a Initial code for Boolean property support
81d3729 Temporary note in maint/README and update ucptestdata for changes to script numbers
f90542a Improve unicode property abbreviation support (#74)
14dbc6e jit: use correct type when checking for max value (#73)
80205ee ChangeLog entry for PR#72
04ecb26 match: Properly align heapframes for CHERI/Arm's Morello prototype (#72)
534b476 RunGrepTest: Fix tests 132 and 133 when srcdir is relative (#71)
31fb2e5 Suppress compiler fall-through warnings
435140a Fix script extension support on jit (#69)
c24047f Documentation update
e745700 Auto generate unicode property tests. (#67)
d888d36 Update script run code to work with new script extensions coding
6614b28 Implement script extension support in JIT. (#66)
afa4756 Rework script extension handling (#64)
7713f33 Add support for 4-character script abbreviations
af2637e Fix parameter types in the pcre2serialize man page (#63)
98e7d70 Refactor Python scripts for generating Unicode property data
321b559 Ignore Python cache
16c8a84 Arrange to distribute pcre2_ucptables.c
4514ddd Split generated tables from fixed tables
944f0e1 Documentation for script handling update
b297320 Revised script handling (see ChangeLog)
92d7cf1 Very minor code speed up for maximizing character property matches
1d432ee Do bidi synonyms properly
194a153 Correct comment in test
1c41a5b Fix minor issues raised by Clang sanitize
4243515 JIT support for Bidi_Control and Bidi_Class
49b29f8 Add short synonyms for Bidi_Control and Bidi_Class
30abd0a Documentation for Bidi_Control and Bidi_Class
0246c6b Add support for Bidi_Control and Bidi_Class properties
823d4ac Add bidi class and control information to Unicode property data
ba3d0ed Documentation update
4ef0c51 Interpret NULL pointer, zero length as an empty string for subjects and replacements.
- Mentioned files: include/pcre2*.h, package/libs/pcre2/Config.in, package/libs/pcre2/Makefile

### ARM board lockups/hangs triggered by locks and mutexes: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-August.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-August.txt
- Root message ID: <60a553a2-85f3-d8c6-b070-ecd3089c3c5e@gmail.com>
- Problem excerpt: We released
>> firmwares based on Linux 4.4 (and later on 4.14) that worked almost
>> fine. There was one little issue we couldn't debug or fix: random hangs
>> and reboots. They were too rare to deal with (most devices worked fine
>> for weeks or months).
>>
>> Recently I updated my stable kernel 5.4 and I started experiencing
>> stability issues on my own! After some uptime (usually from 0 to 20
>> minutes of close to zero activity) serial console hangs.

### bug in busybox lock: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-March.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-March.txt
- Root message ID: <f06ae46c-71a9-7f0d-d318-f2c80bbf99b5@gmail.com>
- Problem excerpt: Hi,.
commit.
busybox: fix busybox lock applet pidstr buffer overflow.
looks wrong for me:.
--- a/package/utils/busybox/patches/220-add_lock_util.patch
+++ b/package/utils/busybox/patches/220-add_lock_util.patch
@@ -109,7 +109,7 @@
  +              if (!waitonly) {
  +                      lseek(fd, 0, SEEK_SET);
  +                      ftruncate(fd, 0);
-+                      sprintf(pidstr, "%d\n", pid);
++                      snprintf(sizeof(pidstr), pidstr, "%d\n", pid);
  +                      write(fd, pidstr, strlen(pidstr));
  +                      close(fd);
  +              }. The first parameter in snprintf() must be the buffer and the second the length.. Regards,
Hartmut
- Mentioned files: package/utils/busybox/patches/220-add_lock_util.patch

### Build problems with packages which are using openssl: recurring problem pattern

- Score: 1.0
- Completeness: problem-only
- Source file: devel/2023-April.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-April.txt
- Root message ID: <5CF95643-2177-4B34-A0ED-7F1DB1349C67@redfish-solutions.com>
- Problem excerpt: I don't know if it's related, but syslog-ng-3.38.1 and now -4.1.1 keep crashing in libssl.so..
[ 7263.710130] syslog-ng[6648]: segfault at 180 ip 00007fe55725dd43 sp 00007ffffde33ed8 error 6 in libssl.so.3[7fe557252000+45000]
[ 7263.715174] Code: e8 03 00 ff 15 8e dc 05 00 31 d2 31 c0 be 11 01 00 00 bf 14 00 00 00 ff 15 f2 d8 05 00 31 c0 5a c3 89 d1 48 8d 87 88 01 00 00 <48> 89 8f 80 01 00 00 48 39 f0 73 09 48 8d 14 08 48 39 d6 eb 0c 48
[ 7296.292439] syslog-ng[6767]: segfault at 180 ip 00007fa446859d43 sp 00007ffcb4e2dac8 error 6 in libssl.so.3[7fa44684e000+45000]
[ 7296.297398] Code: e8 03 00 ff 15 8e dc 05 00 31 d2 31 c0 be 11 01 00 00 bf 14 00 00 00 ff 15 f2 d8 05 00 31 c0 5a c3 89 d1 48 8d 87 88 01 00 00 <48> 89 8f 80 01 00 00 48 39 f0 73 09 48 8d 14 08 48 39 d6 eb 0c 48
[ 7313.742858] syslog-ng[6832]: segfault at 180 ip 00007f81280f0d43 sp 00007fffcebbf898 error 6 in libssl.so.3[7f81280e5000+45000]
[ 7313.747486] Code: e8 03 00 ff 15 8e dc 05 00 31 d2 31 c0 be 11 01 00 00 bf 14 00 00 00 ff 15 f2 d8 05 00 31 c0 5a c3 89 d1 48 8d 87 88 01 00 00 <48> 89 8f 80 01 00 00 48 39 f0 73 09 48 8d 14 08 48 39 d6 eb 0c 48
[ 7378.425765] syslog-ng[6916]: segfault at 180 ip 00007f3c036a7d43 sp 00007ffc825fd898 error 6 in libssl.so.3[7f3c0369c000+45000]
[ 7378.430827] Code: e8 03 00 ff 15 8e dc 05 00 31 d2 31 c0 be 11 01 00 00 bf 14 00 00 00 ff 15 f2 d8 05 00 31 c0 5a c3 89 d1 48 8d 87 88 01 00 00 <48> 89 8f 80 01 00 00 48 39 f0 73 09 48 8d 14 08 48 39 d6 eb 0c 48. I'm having to switch over to rsyslog until we get this figured out..
> On Apr 23, 2023, at 3:56 PM, e9hack <e9hack at gmail.com> wrote:
> 
> Hi,
> 
> in the past, it was possible to build packages, which are using crypto libraries like openssl, wolfssl or mbedtls, in parallel. One was build for the image, selected as <y>, the others were build as module selected as <m>.
> 
> This doesn't work any more, if a package is selected for usage of openssl with <m> and any other crypto library is selected with <y>.
> 
> Compiling is successful, but installation complains about to install a binary twice from two different packages.
> 
> I'm not sure, since when this does occur, but I assume, it was introduced with the openssl update to 3.0.x.
> 
> Regards,
> Hartmut
> 
> _______________________________________________
> openwrt-devel mailing list
> openwrt-devel at lists.openwrt.org
> https://lists.openwrt.org/mailman/listinfo/openwrt-devel

### gemini: Add kernel v6.1 patches: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-May.txt
- Root message ID: <20230531212108.3252356-1-linus.walleij@linaro.org>
- Problem excerpt: D-Link DNS-313.. Signed-off-by: Linus Walleij <linus.walleij at linaro.org>
---
 ...pio-vbus-usb-Add-device-tree-probing.patch |    71 +
 ...llect-pieces-of-dual-mode-controller.patch | 16029 ++++++++++++++++
 ...-usb-fotg210-Compile-into-one-module.patch |   342 +
 ...usb-fotg210-Select-subdriver-by-mode.patch |    71 +
 ...b-fotg2-add-Gemini-specific-handling.patch |   139 +
 ...210-Fix-Kconfig-for-USB-host-modules.patch |    54 +
 ...FOTG210-should-depend-on-ARCH_GEMINI.patch |    29 +
 ...dev-pointer-in-probe-and-dev_message.patch |    64 +
 ...10-udc-Support-optional-external-PHY.patch |   162 +
 .../0010-fotg210-udc-Handle-PCLK.patch        |    94 +
 ...0-udc-Get-IRQ-using-platform_get_irq.patch |    72 +
 ...g210-udc-Remove-a-useless-assignment.patch |    42 +
 ...fix-potential-memory-leak-in-fotg210.patch |    61 +
 .../0014-usb-fotg210-fix-OTG-only-build.patch |    42 +
 ...fix-error-return-code-in-fotg210_udc.patch |    31 +
 ...-usb-fotg210-List-different-variants.patch |    28 +
 ...g210-Acquire-memory-resource-in-core.patch |   253 +
 ...-fotg210-Move-clock-handling-to-core.patch |   203 +
 ...-fotg210-Check-role-register-in-core.patch |    57 +
 ...dc-Assign-of_node-and-speed-on-start.patch |    37 +
 ...b-fotg210-udc-Implement-VBUS-session.patch |   101 +
 ...oduce-and-use-a-fotg210_ack_int-func.patch |   137 +
 ...10-udc-Improve-device-initialization.patch |    66 +
 ...use-sysfs_emit-to-instead-of-scnprin.patch |    35 +
 ...i-Push-down-flash-address-size-cells.patch |    68 +
 ...ni-wbd111-Use-RedBoot-partion-parser.patch |    57 +
 ...ni-wbd222-Use-RedBoot-partion-parser.patch |    57 +
 ...ARM-dts-gemini-Fix-USB-block-version.patch |    34 +
 ...mini-Enable-DNS313-FOTG210-as-periph.patch |    58 +
 ...-DIR-685-partition-table-for-OpenWrt.patch |    37 +
 30 files changed, 18531 insertions(+)
 create mode 100644 target/linux/gemini/patches-6.1/0001-usb-phy-phy-gpio-vbus-usb-Add-device-tree-probing.patch
 create mode 100644 target/linux/gemini/patches-6.1/0002-usb-fotg210-Collect-pieces-of-dual-mode-controller.patch
 create mode 100644 target/linux/gemini/patches-6.1/0003-usb-fotg210-Compile-into-one-module.patch
 create mode 100644 target/linux/gemini/patches-6.1/0004-usb-fotg210-Select-subdriver-by-mode.patch
 create mode 100644 target/linux/gemini/patches-6.1/0005-usb-fotg2-add-Gemini-specific-handling.patch
 create mode 100644 target/linux/gemini/patches-6.1/0006-usb-fotg210-Fix-Kconfig-for-USB-host-modules.patch
 create mode 100644 target/linux/gemini/patches-6.1/0007-usb-USB_FOTG210-should-depend-on-ARCH_GEMINI.patch
 create mode 100644 target/linux/gemini/patches-6.1/0008-fotg210-udc-Use-dev-pointer-in-probe-and-dev_message.patch
 create mode 100644 target/linux/gemini/patches-6.1/0009-fotg210-udc-Support-optional-external-PHY.patch
 create mode 100644 target/linux/gemini/patches-6.1/0010-fotg210-udc-Handle-PCLK.patch
 create mode 100644 target/linux/gemini/patches-6.1/0011-fotg210-udc-Get-IRQ-using-platform_get_irq.patch
 create mode 100644 target/linux/gemini/patches-6.1/0012-usb-fotg210-udc-Remove-a-useless-assignment.patch
 create mode 100644 target/linux/gemini/patches-6.1/0013-usb-fotg210-udc-fix-potential-memory-leak-in-fotg210.patch
 create mode 100644 target/linux/gemini/patches-6.1/0014-usb-fotg210-fix-OTG-only-build.patch
 create mode 100644 target/linux/gemini/patches-6.1/0015-usb-fotg210-udc-fix-error-return-code-in-fotg210_udc.patch
 create mode 100644 target/linux/gemini/patches-6.1/0016-usb-fotg210-List-different-variants.patch
 create mode 100644 target/linux/gemini/patches-6.1/0017-usb-fotg210-Acquire-memory-resource-in-core.patch
 create mode 100644 target/linux/gemini/patches-6.1/0018-usb-fotg210-Move-clock-handling-to-core.patch
 create mode 100644 target/linux/gemini/patches-6.1/0019-usb-fotg210-Check-role-register-in-core.patch
 create mode 100644 target/linux/gemini/patches-6.1/0020-usb-fotg210-udc-Assign-of_node-and-speed-on-start.patch
 create mode 100644 target/linux/gemini/patches-6.1/0021-usb-fotg210-udc-Implement-VBUS-session.patch
 create mode 100644 target/linux/gemini/patches-6.1/0022-fotg210-udc-Introduce-and-use-a-fotg210_ack_int-func.patch
 create mode 100644 target/linux/gemini/patches-6.1/0023-fotg210-udc-Improve-device-initialization.patch
 create mode 100644 target/linux/gemini/patches-6.1/0024-usb-fotg210-hcd-use-sysfs_emit-to-instead-of-scnprin.patch
 create mode 100644 target/linux/gemini/patches-6.1/0025-ARM-dts-gemini-Push-down-flash-address-size-cells.patch
 create mode 100644 target/linux/gemini/patches-6.1/0026-ARM-dts-gemini-wbd111-Use-RedBoot-partion-parser.patch
 create mode 100644 target/linux/gemini/patches-6.1/0027-ARM-dts-gemini-wbd222-Use-RedBoot-partion-parser.patch
 create mode 100644 target/linux/gemini/patches-6.1/0028-ARM-dts-gemini-Fix-USB-block-version.patch
 create mode 100644 target/linux/gemini/patches-6.1/0029-ARM-dts-gemini-Enable-DNS313-FOTG210-as-periph.patch
 create mode 100644 target/linux/gemini/patches-6.1/300-ARM-dts-Augment-DIR-685-partition-table-for-OpenWrt.patch.
[diff: target/linux/gemini/patches-6.1/0001-usb-phy-phy-gpio-vbus-usb-Add-device-tree-probing.patch]
+From d5a026cc8306ccd3e99e1455c87e38f8e6fa18df Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 7 Nov 2022 00:05:06 +0100
+Subject: [PATCH 01/29] usb: phy: phy-gpio-vbus-usb: Add device tree probing
+Make it possible to probe the GPIO VBUS detection driver
[diff: target/linux/gemini/patches-6.1/0002-usb-fotg210-Collect-pieces-of-dual-mode-controller.patch]
+From 30367636930864f71b2bd462adedcf8484313864 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 23 Oct 2022 16:47:06 +0200
+Subject: [PATCH 02/29] usb: fotg210: Collect pieces of dual mode controller
+The Faraday FOTG210 is a dual-mode OTG USB controller that can
[diff: target/linux/gemini/patches-6.1/0003-usb-fotg210-Compile-into-one-module.patch]
+From 0dbc77a99267a5efef0603a4b49ac02ece6a3f23 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 23 Oct 2022 16:47:07 +0200
+Subject: [PATCH 03/29] usb: fotg210: Compile into one module
+It is since ages perfectly possible to compile both of these
[diff: target/linux/gemini/patches-6.1/0004-usb-fotg210-Select-subdriver-by-mode.patch]
+From 7c0b661926097e935f2711857596fc2277b2304a Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 23 Oct 2022 16:47:08 +0200
+Subject: [PATCH 04/29] usb: fotg210: Select subdriver by mode
+Check which mode the hardware is in, and selecte the peripheral
[diff: target/linux/gemini/patches-6.1/0005-usb-fotg2-add-Gemini-specific-handling.patch]
+From f7f6c8aca91093e2f886ec97910b1a7d9a69bf9b Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 9 Nov 2022 21:05:54 +0100
+Subject: [PATCH 05/29] usb: fotg2: add Gemini-specific handling
+The Cortina Systems Gemini has bolted on a PHY inside the
[diff: target/linux/gemini/patches-6.1/0006-usb-fotg210-Fix-Kconfig-for-USB-host-modules.patch]
+From 6e002d41889bc52213a26ff91338d340505e0336 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Fri, 11 Nov 2022 15:48:21 +0100
+Subject: [PATCH 06/29] usb: fotg210: Fix Kconfig for USB host modules
+The kernel robot reports a link failure when activating the
[diff: target/linux/gemini/patches-6.1/0007-usb-USB_FOTG210-should-depend-on-ARCH_GEMINI.patch]
+From 466b10510add46afd21ca19505b29d35ad853370 Mon Sep 17 00:00:00 2001
+From: Geert Uytterhoeven <geert+renesas at glider.be>
+Date: Mon, 21 Nov 2022 16:22:19 +0100
+Subject: [PATCH 07/29] usb: USB_FOTG210 should depend on ARCH_GEMINI
+The Faraday Technology FOTG210 USB2 Dual Role Controller is only present
[diff: target/linux/gemini/patches-6.1/0008-fotg210-udc-Use-dev-pointer-in-probe-and-dev_message.patch]
+From 27cd321a365fecac857e41ad1681062994142e4a Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 14 Nov 2022 12:51:58 +0100
+Subject: [PATCH 08/29] fotg210-udc: Use dev pointer in probe and dev_messages
+Add a local struct device *dev pointer and use dev_err()
[diff: target/linux/gemini/patches-6.1/0009-fotg210-udc-Support-optional-external-PHY.patch]
+From 03e4b585ac947e2d422bedf03179bbfec3aca3cf Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 14 Nov 2022 12:51:59 +0100
+Subject: [PATCH 09/29] fotg210-udc: Support optional external PHY
+This adds support for an optional external PHY to the FOTG210
[diff: target/linux/gemini/patches-6.1/0010-fotg210-udc-Handle-PCLK.patch]
+From 772ea3ec2b9363b45ef9a4768ea205f758c3debc Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 14 Nov 2022 12:52:00 +0100
+Subject: [PATCH 10/29] fotg210-udc: Handle PCLK
+This adds optional handling of the peripheral clock PCLK.
[diff: target/linux/gemini/patches-6.1/0011-fotg210-udc-Get-IRQ-using-platform_get_irq.patch]
+From eda686d41e298a9d16708d2ec8d12d8e682dd7ca Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 14 Nov 2022 12:52:01 +0100
+Subject: [PATCH 11/29] fotg210-udc: Get IRQ using platform_get_irq()
+The platform_get_irq() is necessary to use to get dynamic
[diff: target/linux/gemini/patches-6.1/0012-usb-fotg210-udc-Remove-a-useless-assignment.patch]
+From 7889a2f0256c55e0184dffd0001d0782f9e4cb83 Mon Sep 17 00:00:00 2001
+From: Christophe JAILLET <christophe.jaillet at wanadoo.fr>
+Date: Mon, 14 Nov 2022 21:38:04 +0100
+Subject: [PATCH 12/29] usb: fotg210-udc: Remove a useless assignment
+There is no need to use an intermediate array for these memory allocations,
[diff: target/linux/gemini/patches-6.1/0013-usb-fotg210-udc-fix-potential-memory-leak-in-fotg210.patch]
+From 7b95ade85ac18eec63e81ac58a482b3e88361ffd Mon Sep 17 00:00:00 2001
+From: Yi Yang <yiyang13 at huawei.com>
+Date: Fri, 2 Dec 2022 09:21:26 +0800
+Subject: [PATCH 13/29] usb: fotg210-udc: fix potential memory leak in
+ fotg210_udc_probe()
[diff: target/linux/gemini/patches-6.1/0014-usb-fotg210-fix-OTG-only-build.patch]
+From d8eed400495029ba551704ff0fae1dad87332291 Mon Sep 17 00:00:00 2001
+From: Arnd Bergmann <arnd at arndb.de>
+Date: Thu, 15 Dec 2022 17:57:20 +0100
+Subject: [PATCH 14/29] usb: fotg210: fix OTG-only build
+The fotg210 module combines the HCD and OTG drivers, which then
[diff: target/linux/gemini/patches-6.1/0015-usb-fotg210-udc-fix-error-return-code-in-fotg210_udc.patch]
+From eaaa85d907fe27852dd960b2bc5d7bcf11bc3ebd Mon Sep 17 00:00:00 2001
+From: Yang Yingliang <yangyingliang at huawei.com>
+Date: Fri, 30 Dec 2022 14:54:27 +0800
+Subject: [PATCH 15/29] usb: fotg210-udc: fix error return code in
+ fotg210_udc_probe()
[diff: target/linux/gemini/patches-6.1/0016-usb-fotg210-List-different-variants.patch]
+From 407577548b2fcd41cc72ee05df1f05a430ed30a0 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:16 +0100
+Subject: [PATCH 16/29] usb: fotg210: List different variants
+There are at least two variants of the FOTG: FOTG200 and
[diff: target/linux/gemini/patches-6.1/0017-usb-fotg210-Acquire-memory-resource-in-core.patch]
+From fa735ad1afeb5791d5562617b9bbed74574d3e81 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:17 +0100
+Subject: [PATCH 17/29] usb: fotg210: Acquire memory resource in core
+The subdrivers are obtaining and mapping the memory resource
[diff: target/linux/gemini/patches-6.1/0018-usb-fotg210-Move-clock-handling-to-core.patch]
+From fb8e1e8dbc47e7aff7624b47adaa0a84d2983802 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:18 +0100
+Subject: [PATCH 18/29] usb: fotg210: Move clock handling to core
+Grab the optional silicon block clock, prepare and enable it in
[diff: target/linux/gemini/patches-6.1/0019-usb-fotg210-Check-role-register-in-core.patch]
+From b1b07abb598211de3ce7f52abdf8dcb24384341e Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:19 +0100
+Subject: [PATCH 19/29] usb: fotg210: Check role register in core
+Read the role register and check that we are in host/peripheral
[diff: target/linux/gemini/patches-6.1/0020-usb-fotg210-udc-Assign-of_node-and-speed-on-start.patch]
+From d7c2b0b6da75b86cf5ddbcd51a74d74e19bbf178 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:20 +0100
+Subject: [PATCH 20/29] usb: fotg210-udc: Assign of_node and speed on start
+Follow the example set by other drivers to assign of_node
[diff: target/linux/gemini/patches-6.1/0021-usb-fotg210-udc-Implement-VBUS-session.patch]
+From 2fbbfb2c556944945639b17b13fcb1e05272b646 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Wed, 18 Jan 2023 08:09:21 +0100
+Subject: [PATCH 21/29] usb: fotg210-udc: Implement VBUS session
+Implement VBUS session handling for FOTG210. This is
[diff: target/linux/gemini/patches-6.1/0022-fotg210-udc-Introduce-and-use-a-fotg210_ack_int-func.patch]
+From f011d1eab23f4c063c5441c0d5a22898adf9145c Mon Sep 17 00:00:00 2001
+From: Fabian Vogt <fabian at ritter-vogt.de>
+Date: Mon, 23 Jan 2023 08:35:07 +0100
+Subject: [PATCH 22/29] fotg210-udc: Introduce and use a fotg210_ack_int
+ function
[diff: target/linux/gemini/patches-6.1/0023-fotg210-udc-Improve-device-initialization.patch]
+From 367747c7813cecf19b46ef7134691f903ab76dc9 Mon Sep 17 00:00:00 2001
+From: Fabian Vogt <fabian at ritter-vogt.de>
+Date: Mon, 23 Jan 2023 08:35:08 +0100
+Subject: [PATCH 23/29] fotg210-udc: Improve device initialization
+Reset the device explicitly to get into a known state and also set the chip
[diff: target/linux/gemini/patches-6.1/0024-usb-fotg210-hcd-use-sysfs_emit-to-instead-of-scnprin.patch]
+From 482830a70408a5d30af264b3d6706f818c78b2b2 Mon Sep 17 00:00:00 2001
+From: Andy Shevchenko <andriy.shevchenko at linux.intel.com>
+Date: Fri, 20 Jan 2023 17:44:33 +0200
+Subject: [PATCH 24/29] usb: fotg210-hcd: use sysfs_emit() to instead of
+ scnprintf()
[diff: target/linux/gemini/patches-6.1/0025-ARM-dts-gemini-Push-down-flash-address-size-cells.patch]
+From 6b84aa39a063eec883d410a9893cec70fce56163 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 4 Dec 2022 20:02:28 +0100
+Subject: [PATCH 25/29] ARM: dts: gemini: Push down flash address/size cells
+The platforms not defining any OF partions complain like
[diff: target/linux/gemini/patches-6.1/0026-ARM-dts-gemini-wbd111-Use-RedBoot-partion-parser.patch]
+From 0e733f5af628210f372585e431504a7024e7b571 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 4 Dec 2022 20:02:29 +0100
+Subject: [PATCH 26/29] ARM: dts: gemini: wbd111: Use RedBoot partion parser
+This is clearly a RedBoot partitioned device with 0x20000
[diff: target/linux/gemini/patches-6.1/0027-ARM-dts-gemini-wbd222-Use-RedBoot-partion-parser.patch]
+From 8558e2e1110a5daa4ac9e1c5b5c15e1651a8fb94 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Sun, 4 Dec 2022 20:02:30 +0100
+Subject: [PATCH 27/29] ARM: dts: gemini: wbd222: Use RedBoot partion parser
+This is clearly a RedBoot partitioned device with 0x20000
[diff: target/linux/gemini/patches-6.1/0028-ARM-dts-gemini-Fix-USB-block-version.patch]
+From d5c01ce4a1016507c69682894cf6b66301abca3d Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 23 Jan 2023 08:39:15 +0100
+Subject: [PATCH 28/29] ARM: dts: gemini: Fix USB block version
+The FOTG version in the Gemini is the FOTG200, fix this
[diff: target/linux/gemini/patches-6.1/0029-ARM-dts-gemini-Enable-DNS313-FOTG210-as-periph.patch]
+From 296184694ae7a4e388603c95499e98d30b21cc09 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 23 Jan 2023 08:39:16 +0100
+Subject: [PATCH 29/29] ARM: dts: gemini: Enable DNS313 FOTG210 as periph
+Add the GPIO-based VBUS phy, and enable the FOTG210
[diff: target/linux/gemini/patches-6.1/300-ARM-dts-Augment-DIR-685-partition-table-for-OpenWrt.patch]
+From 36ee838bf83c01cff7cb47c7b07be278d2950ac0 Mon Sep 17 00:00:00 2001
+From: Linus Walleij <linus.walleij at linaro.org>
+Date: Mon, 11 Mar 2019 15:44:29 +0100
+Subject: [PATCH 2/2] ARM: dts: Augment DIR-685 partition table for OpenWrt
+Rename the firmware partition so that the firmware MTD
- Mentioned files: package/kernel/linux/modules/usb.mk, target/linux/gemini/Makefile, target/linux/gemini/config-6.1, target/linux/gemini/modules.mk, target/linux/gemini/patches-6.1/0001-usb-phy-phy-gpio-vbus-usb-Add-device-tree-probing.patch

---

## networking

- Lesson candidates: 366
- Completeness: complete=284, fragmentary=59, problem-only=7, searchable=16
- Common signals: you, networking, can, following, did, https:, comment, message, details, user, found, who

Representative referenced problems:

### add support mikrotik routerboard hex poe: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-December.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-December.txt
- Root message ID: <20211226184126.3186364-1-oskari@lemmela.net>
- Problem excerpt: RFC patchset because of following open questions:.
---
Since the QCA8337 DSA driver does not work properly with the current
5.4 kernel, should new boards wait until ath79 5.10 kernel and DSA change
is made?.
---
Mikrotik bootloader does not print anything to the serial console. Debugging the bootloader is quite time consuming. While testing,
I found that it is impossible to start an initramfs image larger
than 0x580000 (5.7 MB) via tftp.. Is there any way to limit the size of the initramfs image when the 
sysupgrade image exceeds the tftp size limit?.
---
POE driver is implemented as a kernel module.
- Mentioned files: lib/functions.sh, lib/preinit/10_rename_interfaces.sh, target/linux/ath79/dts/qca9557_mikrotik_routerboard-960pgs.dts, target/linux/ath79/files/drivers/hwmon/rbpoe.c, target/linux/ath79/files/drivers/hwmon/rbpoe.h

### ath79: add support for Ubiquiti PowerBeam M (XW): mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210523115946.711907-1-russell@personaltelco.net>
- Problem excerpt: Specifications:
 - Atheros AR9342 SoC
 - 64 MB RAM
 - 8 MB SPI flash
 - 1x 10/100 Mbps Ethernet port, 24 Vdc PoE-in
 - Power and LAN green LEDs
 - 4x RSSI LEDs (red, orange, green, green)
 - UART (115200 8N1). Flashing via stock GUI:
 - WARNING: flashing OpenWrt from AirOS v5.6 or newer will brick your
   device! Read the wiki for more info.
 - Downgrade to AirOS v5.5.x (latest available is 5.5.10-u2) first.
 - Upload the factory image via AirOS web GUI.. Flashing via TFTP:
 - WARNING: flashing OpenWrt from AirOS v5.6 or newer will brick your
   device!
- Mentioned files: target/linux/ath79/dts/ar9342_ubnt_powerbeam-m-xw.dts, target/linux/ath79/generic/base-files/etc/board.d/01_leds, target/linux/ath79/generic/base-files/etc/board.d/02_network, target/linux/ath79/image/generic-ubnt.mk

### ath79: add support for Ubiquiti PowerBeam M (XW): mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210523052405.615472-1-russell@personaltelco.net>
- Problem excerpt: Specifications:
 - Atheros AR9342 SoC
 - 64 MB RAM
 - 8 MB SPI flash
 - 1x 10/100 Mbps Ethernet port, 24 Vdc PoE-in
 - Power and LAN green LEDs
 - 4x RSSI LEDs (red, orange, green, green)
 - UART (115200 8N1). Flashing via stock GUI:
 - WARNING: flashing OpenWrt from AirOS v5.6 or newer will brick your
   device! Read the wiki for more info.
 - Downgrade to AirOS v5.5.x (latest available is 5.5.10-u2) first.
 - Upload the factory image via AirOS web GUI.. Flashing via TFTP:
 - WARNING: flashing OpenWrt from AirOS v5.6 or newer will brick your
   device!
- Mentioned files: target/linux/ath79/dts/ar9342_ubnt_powerbeam-m.dts, target/linux/ath79/generic/base-files/etc/board.d/01_leds, target/linux/ath79/generic/base-files/etc/board.d/02_network, target/linux/ath79/image/generic-ubnt.mk

### backport fixes and improvements for MT7530: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-February.txt
- Root message ID: <20220203120705.3532684-1-dqfext@gmail.com>
- Problem excerpt: Fix FDB learning bugs when VLAN filtering is enabled.. Signed-off-by: DENG Qingfang <dqfext at gmail.com>
---
 ...disable-learning-on-standalone-ports.patch |  65 +++++
 ...enable-assisted-learning-on-CPU-port.patch | 102 +++++++
 ...se-independent-VLAN-learning-on-VLAN.patch | 262 ++++++++++++++++++
 ...-mt7530-set-STP-state-on-filter-ID-1.patch |  40 +++
 ...lways-install-FDB-entries-with-IVL-a.patch |  54 ++++
 5 files changed, 523 insertions(+)
 create mode 100644 target/linux/generic/backport-5.10/765-v5.15-net-dsa-mt7530-disable-learning-on-standalone-ports.patch
 create mode 100644 target/linux/generic/backport-5.10/766-v5.15-net-dsa-mt7530-enable-assisted-learning-on-CPU-port.patch
 create mode 100644 target/linux/generic/backport-5.10/767-v5.15-net-dsa-mt7530-use-independent-VLAN-learning-on-VLAN.patch
 create mode 100644 target/linux/generic/backport-5.10/768-v5.15-net-dsa-mt7530-set-STP-state-on-filter-ID-1.patch
 create mode 100644 target/linux/generic/backport-5.10/769-v5.15-net-dsa-mt7530-always-install-FDB-entries-with-IVL-a.patch.
[diff: target/linux/generic/backport-5.10/765-v5.15-net-dsa-mt7530-disable-learning-on-standalone-ports.patch]
+From ba2203f36b981235556504fb7b62baee28512a40 Mon Sep 17 00:00:00 2001
+From: DENG Qingfang <dqfext at gmail.com>
+Date: Tue, 24 Aug 2021 11:37:50 +0800
+Subject: [PATCH] net: dsa: mt7530: disable learning on standalone ports
+This is a partial backport of commit 5a30833b9a16f8d1aa15de06636f9317ca51f9df
[diff: target/linux/generic/backport-5.10/766-v5.15-net-dsa-mt7530-enable-assisted-learning-on-CPU-port.patch]
+From 59c8adbc8e2c7f6b46385f36962eadaad3ea2daa Mon Sep 17 00:00:00 2001
+From: DENG Qingfang <dqfext at gmail.com>
+Date: Wed, 4 Aug 2021 00:04:01 +0800
+Subject: [PATCH] net: dsa: mt7530: enable assisted learning on CPU port
+Consider the following bridge configuration, where bond0 is not
[diff: target/linux/generic/backport-5.10/767-v5.15-net-dsa-mt7530-use-independent-VLAN-learning-on-VLAN.patch]
+From e3a402764c5753698e7a9e45d4d21f093faa7852 Mon Sep 17 00:00:00 2001
+From: DENG Qingfang <dqfext at gmail.com>
+Date: Wed, 4 Aug 2021 00:04:02 +0800
+Subject: [PATCH] net: dsa: mt7530: use independent VLAN learning on
+ VLAN-unaware bridges
[diff: target/linux/generic/backport-5.10/768-v5.15-net-dsa-mt7530-set-STP-state-on-filter-ID-1.patch]
+From c5ffcefcb40420528d04c63e7dfc88f2845c9831 Mon Sep 17 00:00:00 2001
+From: DENG Qingfang <dqfext at gmail.com>
+Date: Wed, 4 Aug 2021 00:04:03 +0800
+Subject: [PATCH] net: dsa: mt7530: set STP state on filter ID 1
+As filter ID 1 is the only one used for bridges, set STP state on it.
[diff: target/linux/generic/backport-5.10/769-v5.15-net-dsa-mt7530-always-install-FDB-entries-with-IVL-a.patch]
+From 138c126a33f7564edb66b1da5b847e4a60740bfc Mon Sep 17 00:00:00 2001
+From: DENG Qingfang <dqfext at gmail.com>
+Date: Wed, 4 Aug 2021 00:04:04 +0800
+Subject: [PATCH] net: dsa: mt7530: always install FDB entries with IVL and FID
+ 1
- Mentioned files: target/linux/generic/backport-5.10/611-v5.12-net-ethernet-mediatek-support-setting-MTU.patch, target/linux/generic/backport-5.10/762-v5.11-net-dsa-mt7530-support-setting-MTU.patch, target/linux/generic/backport-5.10/763-v5.11-net-dsa-mt7530-enable-MTU-normalization.patch, target/linux/generic/backport-5.10/764-v5.11-net-dsa-mt7530-support-setting-ageing-time.patch, target/linux/generic/backport-5.10/765-v5.15-net-dsa-mt7530-disable-learning-on-standalone-ports.patch

### bmips: bcm6368-enetsw: Bump max MTU: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-October.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-October.txt
- Root message ID: <20231001222553.3005147-1-linus.walleij@linaro.org>
- Problem excerpt: The available overhead is needed when using the DSA
switch with a cascaded Marvell DSA switch, which is something that exist
in real products, in this case the Inteno XG6846.. Before this patch (on the lan1 DSA port in this case):
dsa_slave_change_mtu: master->max_mtu = 9724, dev->max_mtu = 10218, DSA overhead = 8
dsa_slave_change_mtu: master = extsw, dev = lan1
dsa_slave_change_mtu: master->max_mtu = 1510, dev->max_mtu = 9724, DSA overhead = 6
dsa_slave_change_mtu: master = eth0, dev = extsw
dsa_slave_change_mtu new_master_mtu 1514 > mtu_limit 1510
mdio_mux-0.1:00: nonfatal error -34 setting MTU to 1500 on port 0. My added debug prints before the nonfatal error: the first switch from the top
is the Marvell switch, the second in the bcm6368-enetsw with its 1510 limit.. After this patch the error is gone..
- Mentioned files: target/linux/bmips/files/drivers/net/ethernet/broadcom/bcm6368-enetsw.c

---

## package-packaging

- Lesson candidates: 50
- Completeness: complete=39, fragmentary=7, problem-only=2, searchable=2
- Common signals: you, package-packaging, can, did, https:, message, details, following, opkg, found, are, more

Representative referenced problems:

### Brokenness of the OpenWrt "packages" repo (was: Re: [PATCH] Revert "dbus: update to 1.13.18"): mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-April.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-April.txt
- Root message ID: <87pmyi5v70.fsf_-_@miraculix.mork.no>
- Problem excerpt: There
is no reason to skip run testing in the first place. This buggy change
would never have been commited by any qualified developer.. And you got a report 19 days ago that the package was uninstallable:
https://github.com/openwrt/packages/commit/0fb5d3ed2cb31a0a6076d36fb7a668cfe5328c92#commitcomment-49147445
The only logical thing to do would be an immediate revert. But no, the
package is still broken.

### comgt: Move to community packages repo: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-June.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-June.txt
- Root message ID: <7cd7992b-6e7c-74e0-c4ea-e479311c4c3b@aparcar.org>
- Problem excerpt: On 6/28/21 8:53 AM, Piotr Dymacz wrote:
> Hi John,
>
> On 28.06.2021 20:32, John Crispin wrote:
>>
>> On 28.06.21 19:26, Piotr Dymacz wrote:
>>> I might be wrong here but I think we don't include packages from 
>>> external feeds inside 'DEVICE_PACKAGES' (not sure/don't remember why). 
>>
>> I am in favour of moving all none-core packages to the feeds. the
>> dependency should be removed and a note should be added to the wiki
>> indicating that if a release/snapshot image is installed an opkg call
>> shall be issued
I'm in favor of this too but if it's a core feature (i.e. SIM card 
support) we should provide the package by default to, not?
>
> Sounds good to me, just wanted to warn about the existing dependency.
>
- Mentioned files: lib/functions.sh, lib/netifd/netifd-proto.sh, lib/netifd/proto/3g.sh, lib/netifd/proto/directip.sh, lib/netifd/proto/ncm.sh

### ca-certificates doesn't include Lets Encrypt CA, preventing package installations through opkg: mistake and correction

- Score: 0.95
- Completeness: complete
- Source file: bugs/2021-October.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-bugs/2021-October.txt
- Root message ID: <mailman.2892.1633288426.1923571.openwrt-bugs@lists.openwrt.org>
- Problem excerpt: The following task has a new comment added:. FS#4059 - ca-certificates doesn't include Lets Encrypt CA, preventing package installations through opkg
User who did this - Vladim?r N?vrat (vlna).
----------
OpenWrt 21.02.0, r16279-5cc0535800 on TP-LINK WDR3600.
wget http://oleole.pl -O -
Downloading 'http://oleole.pl'
Connecting to 155.133.76.33:80
Redirected to / on www.oleole.pl
Redirected to / on www.oleole.pl
Connection error: Invalid SSL certificate. It started after 2021-09-30 13:05 and before 2021-09-30 16:05 CEST.. No problem with update/install.
----------.

### Check on 'which' in include/prereq-build.mk fails for Fedora 34 since recently, how to fix?: recurring problem pattern

- Score: 0.95
- Completeness: searchable
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <7d7b4e92-d26e-2943-9973-5ec8a672f20d@basmevissen.nl>
- Problem excerpt: I ran into the following:.
$ ./scripst/feeds update -a
(...)
Checking 'rsync'... ok. Checking 'which'... failed. Checking 'ldconfig-stub'... ok.. Build dependency: Please install 'which'
(...).
$ rpm -qa which
which-2.21-26.fc34.x86_64.
- Mentioned files: include/prereq-build.mk

### Add SoB tag to hack patches on generic target

- Score: 0.85
- Completeness: fragmentary
- Source file: devel/2022-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-September.txt
- Root message ID: <CA+_ehUxVUSJc+nxJFPit_bcxXNZ6=uD6r9P3M+SoJNWYFqf1wg@mail.gmail.com>

---

## patch-maintenance

- Lesson candidates: 88
- Completeness: complete=57, fragmentary=22, problem-only=2, searchable=7
- Common signals: format, name, libsepol, cil:, you, patch-maintenance, struct, https:, array, field, can, following

Representative referenced problems:

### build: prereq: drop support for Python 3.5: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-February.txt
- Root message ID: <20210216072108.26107-1-a.heider@gmail.com>
- Problem excerpt: This patch ensures that OpenWrt can update meson while still
> relying on the host python.. Current buildbot images are based on Debian 9, which uses Python 3.5 so merging this
would result in broken buildbots.. Cheers,. Petr
- Mentioned files: include/prereq-build.mk

### feeds.conf.default: remove freifunk feed: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-February.txt
- Root message ID: <20220227111247.7677-1-ynezz@true.cz>
- Problem excerpt: Since that didn?t work out I?m fine that it was dropped later on.. Being part of the OpenWrt project I learn every other day that ?legacy? shouldn?t be broken. By removing the Freifunk feed we may break whatever special setup some community somewhere figured out, glued into some CI and scripts which silently produces images for whatever use case.. Anyway, if the Freifunk community itself finds it to be useless, let?s drop it.
- Mentioned files: feeds.conf.default

### OpenWrt 21.02 and 19.07 minor release: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-January.txt
- Root message ID: <57937806-1129-9d16-eb2c-e001c3d001fa@hauke-m.de>
- Problem excerpt: I am not aware of a severe security problem, it was just some time 
since the last release.. Are there any known regressions in the current stable branches compared 
to the last release and should we fix them?. If we should backport some changes from master please just answer to 
this mail with the commit and a reason why you need it.. There are already some pull requests on github:
https://github.com/openwrt/openwrt/pulls?q=is%3Apr+is%3Aopen+label%3Arelease%2F21.02 .
https://github.com/openwrt/openwrt/pulls?q=is%3Apr+is%3Aopen+label%3Arelease%2F19.07.

### OpenWrt 25.12 release plan: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2026-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2026-February.txt
- Root message ID: <9cb1c119-258b-49d1-ac7b-51aaaba21fb5@hauke-m.de>
- Problem excerpt: I plan to tag OpenWrt 25.12.0-rc5 next weekend and then the final 
version about 1 week later.. Between rc5 and the final version only small changes should get in to 
reduce the risk of adding new regressions..
@Felix: Could you please have a look at the changes you did in the main 
branch and cherry pick bugfixes needed for 25.12.
@Linus: Please have a look at the fixes you pushed to the main branch in 
the last few weeks and check which should get backported to 25.12.. Hauke

### ramips: move mt7621_nand driver to files: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-January.txt
- Root message ID: <20220127225350.2932004-1-stijn@linux-ipv6.be>
- Problem excerpt: The mtk_nand driver should be
modified to support the mt7621 flash controller instead. As there is no
newer version to backport, or no upstream version to fix bugs, let's
move the driver to the files dir under the ramips target. This makes it
easier to make changes to the driver while waiting for mt7621 support to
land in mtk_nand.. Signed-off-by: Stijn Tintel <stijn at linux-ipv6.be>
---
 .../files/drivers/mtd/nand/raw/mt7621_nand.c  | 1353 ++++++++++++++++
 ...driver-support-for-MT7621-nand-flash.patch | 1356 -----------------
 2 files changed, 1353 insertions(+), 1356 deletions(-)
 create mode 100644 target/linux/ramips/files/drivers/mtd/nand/raw/mt7621_nand.c.
[diff: target/linux/ramips/files/drivers/mtd/nand/raw/mt7621_nand.c]
+// SPDX-License-Identifier: GPL-2.0
+/*
+ * MediaTek MT7621 NAND Flash Controller driver
+ *
+ * Copyright (C) 2020 MediaTek Inc.
- Mentioned files: target/linux/ramips/files/drivers/mtd/nand/raw/mt7621_nand.c, target/linux/ramips/patches-5.10/410-mtd-rawnand-add-driver-support-for-MT7621-nand-flash.patch

---

## procd-init

- Lesson candidates: 120
- Completeness: complete=79, fragmentary=26, problem-only=6, searchable=9
- Common signals: https:, procd-init, you, dridainfotec.com, openwrt, etc, did, details, can, version, system, user

Representative referenced problems:

### Add support for ZyXEL LTE3301-Plus: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210515001130.20654-1-avalentin@marcant.net>
- Problem excerpt: Mai 2021 02:12
> To: openwrt-devel at lists.openwrt.org
> Cc: avalentin at marcant.net
> Subject: [PATCH 2/2] ramips: mt7621: Add support for ZyXEL LTE3301-Plus
> 
> The ZyXEL LTE3301-Plus is an 4G indoor CPE with 2 external LTE antennas.
> 
> Specifications:
> 
>  - SoC: MediaTek MT7621AT
>  - RAM: 256 MB
>  - Flash: 128 MB MB NAND (MX30LF1G18AC)
>  - WiFi: MediaTek MT7615E
>  - Switch: 4 LAN ports (Gigabit)
>  - LTE: Quectel EG506 connected by USB3 to SoC
>  - SIM: 1 micro-SIM slot
>  - USB: USB3 port
>  - Buttons: Reset, WPS
>  - LEDs: Multicolour power, internet, LTE, signal, Wifi, USB
>  - Power: 12V, 1.5A
> 
> The device is built as an indoor ethernet to LTE bridge or router with Wifi.
> 
> UART Serial:
> 
> 57600N1
> Located on populated 5 pin header J5:
> 
>  [o] GND
>  [ ] key - no pin
>  [o] 3.3V Vcc
>  [o] RX
>  [o] TX
> 
> For more details about flashing see commit
> 2449a632084b29632605e5a79ce5d73028eb15dd .
> 
> Signed-off-by: Andr? Valentin <avalentin at marcant.net>
> ---
>  .../ramips/dts/mt7621_zyxel_lte3301-plus.dts  | 213 ++++++++++++++++++
>  target/linux/ramips/image/mt7621.mk           |  16 ++
>  .../mt7621/base-files/etc/board.d/01_leds     |   4 +
>  .../mt7621/base-files/etc/board.d/02_network  |   3 +
>  .../base-files/etc/board.d/03_gpio_switches   |   3 +
>  .../mt7621/base-files/etc/init.d/bootcount    |   1 +
>  .../mt7621/base-files/lib/upgrade/platform.sh |   1 +
>  7 files changed, 241 insertions(+)
>  create mode 100644 target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> 
> diff --git a/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> b/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> new file mode 100644
> index 0000000000..9f2939bb2b
> --- /dev/null
> +++ b/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> @@ -0,0 +1,213 @@
> +// SPDX-License-Identifier: GPL-2.0-or-later OR MIT
> +
> +#include "mt7621.dtsi"
> +
> +#include <dt-bindings/gpio/gpio.h>
> +#include <dt-bindings/input/input.h>
> +
> +/ {
> +	compatible = "zyxel,lte3301-plus", "mediatek,mt7621-soc";
> +	model = "ZyXEL LTE3301-Plus";
> +
> +	aliases {
> +		label-mac-device = &gmac0;
> +		led-boot = &led_power;
> +		led-failsafe = &led_power;
> +		led-running = &led_power;
> +		led-upgrade = &led_power;
> +	};
> +
> +	chosen {
> +		bootargs = "console=ttyS0,57600";
> +	};. IIRC, this is already in the DTSI and can be dropped..
> +
> +	leds {
> +		compatible = "gpio-leds";
> +
> +		led_power: power {
> +			label = "lte3301-plus:white:power";.
drop model from LED labels, keeping just "white:power" etc..
> +			gpios = <&gpio 5 GPIO_ACTIVE_HIGH>;
> +		};
> +
> +		wifi {
> +			label = "lte3301-plus:white:wifi";
> +			gpios = <&gpio 13 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		internet {
> +			label = "lte3301-plus:white:internet";
> +			gpios = <&gpio 23 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		usb {
> +			label = "lte3301-plus:white:usb";
> +			gpios = <&gpio 24 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		lte {
> +			label = "lte3301-plus:white:lte";
> +			gpios = <&gpio 26 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		mobile_green {
> +			label = "lte3301-plus:green:mobile";
> +			gpios = <&gpio 31 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		mobile_orange {
> +			label = "lte3301-plus:orange:mobile";
> +			gpios = <&gpio 22 GPIO_ACTIVE_LOW>;
> +		};. Missing empty line between nodes..
> +		mobile_red {
> +			label = "lte3301-plus:red:mobile";
> +			gpios = <&gpio 14 GPIO_ACTIVE_LOW>;
> +		};
> +	};
> +
> +	keys {
> +		compatible = "gpio-keys";
> +
> +		reset {
> +			label = "reset";
> +			gpios = <&gpio 18 GPIO_ACTIVE_LOW>;
> +			linux,code = <KEY_RESTART>;
> +		};
> +
> +		wps {
> +			label = "wps";
> +			gpios = <&gpio 6 GPIO_ACTIVE_LOW>;
> +			linux,code = <KEY_WPS_BUTTON>;
> +		};
> +	};
> +};
> +
> +&gpio {
> +	status = "okay";
> +
> +	lte_power {
> +		gpio-hog;
> +		gpios = <27 GPIO_ACTIVE_LOW>;
> +		output-high;
> +		line-name = "lte-power";
> +	};
> +
> +	usb_power {
> +		gpio-hog;
> +		gpios = <7 GPIO_ACTIVE_HIGH>;
> +		output-high;
> +		line-name = "usb-power";
> +	};
> +};
> +
> +&nand {
> +	status = "okay";
> +
> +	partitions {
> +		compatible = "fixed-partitions";
> +		#address-cells = <1>;
> +		#size-cells = <1>;
> +
> +		partition at 0 {
> +			label = "Bootloader";
> +			reg = <0x0 0x80000>;
> +			read-only;
> +		};
> +
> +		partition at 80000 {
> +			label = "Config";
> +			reg = <0x80000 0x80000>;
> +		};
> +
> +		factory: partition at 100000 {
> +			label = "Factory";
> +			reg = <0x100000 0x40000>;
> +			read-only;
> +		};
> +
> +		partition at 140000 {
> +			label = "Kernel";
> +			reg = <0x140000 0x1ec0000>;
> +		};.
"ubi" is part of kernel?.
> +
> +		partition at 540000 {
> +			label = "ubi";
> +			reg = <0x540000 0x1ac0000>;
> +		};
> +
> +		partition at 2140000 {
> +			label = "Kernel2";
> +			reg = <0x2140000 0x1ec0000>;
> +		};.
- Mentioned files: lib/upgrade/platform.sh, target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts, target/linux/ramips/image/mt7621.mk, target/linux/ramips/mt7621/base-files/etc/board.d/01_leds, target/linux/ramips/mt7621/base-files/etc/board.d/02_network

### Add support for ZyXEL LTE3301-Plus: recurring problem pattern

- Score: 1.0
- Completeness: searchable
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <20210518204455.10087-1-avalentin@marcant.net>
- Problem excerpt: But the user should get a general idea about flashing without following any links (you may choose whether you prefer just providing one method and then use the link for the other, or just give an overview of available methods etc.)..
> 
> Signed-off-by: Andr? Valentin <avalentin at marcant.net>
> ---
>  package/boot/uboot-envtools/files/ramips      |   1 +
>  .../ramips/dts/mt7621_zyxel_lte3301-plus.dts  | 213 ++++++++++++++++++
>  target/linux/ramips/image/mt7621.mk           |  19 ++
>  .../mt7621/base-files/etc/board.d/01_leds     |   3 +
>  .../mt7621/base-files/etc/board.d/02_network  |   3 +-
>  .../base-files/etc/board.d/03_gpio_switches   |   4 +
>  .../mt7621/base-files/etc/init.d/bootcount    |   1 +
>  .../mt7621/base-files/lib/upgrade/platform.sh |   1 +
>  8 files changed, 244 insertions(+), 1 deletion(-)  create mode 100644
> target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> 
> diff --git a/package/boot/uboot-envtools/files/ramips
> b/package/boot/uboot-envtools/files/ramips
> index bce2e5f0fb..4d0e608911 100644
> --- a/package/boot/uboot-envtools/files/ramips
> +++ b/package/boot/uboot-envtools/files/ramips
> @@ -53,6 +53,7 @@ xiaomi,mi-router-ac2100|\
>  xiaomi,redmi-router-ac2100)
>  	ubootenv_add_uci_config "/dev/mtd1" "0x0" "0x1000" "0x20000"
>  	;;
> +zyxel,lte3301-plus|\
>  zyxel,nr7101)
>  	idx="$(find_mtd_index Config)"
>  	[ -n "$idx" ] && \
> diff --git a/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> b/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> new file mode 100644
> index 0000000000..af2e792cb8
> --- /dev/null
> +++ b/target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts
> @@ -0,0 +1,213 @@
> +// SPDX-License-Identifier: GPL-2.0-or-later OR MIT
> +
> +#include "mt7621.dtsi"
> +
> +#include <dt-bindings/gpio/gpio.h>
> +#include <dt-bindings/input/input.h>
> +
> +/ {
> +	compatible = "zyxel,lte3301-plus", "mediatek,mt7621-soc";
> +	model = "ZyXEL LTE3301-PLUS";
> +
> +	aliases {
> +		label-mac-device = &gmac0;
> +		led-boot = &led_power;
> +		led-failsafe = &led_power;
> +		led-running = &led_power;
> +		led-upgrade = &led_power;
> +	};
> +
> +	gpio_export {
> +		compatible = "gpio-export";
> +
> +		lte_power {
> +			gpio-export,name = "lte_power";
> +			gpio-export,output = <1>;
> +			gpios = <&gpio 27 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		usb_power {
> +			gpio-export,name = "usb_power";
> +			gpio-export,output = <1>;
> +			gpios = <&gpio 7 GPIO_ACTIVE_HIGH>;
> +		};
> +	};
> +
> +	leds {
> +		compatible = "gpio-leds";
> +
> +		led_power: power {
> +			label = "white:power";
> +			gpios = <&gpio 5 GPIO_ACTIVE_HIGH>;
> +		};
> +
> +		wifi {
> +			label = "white:wifi";
> +			gpios = <&gpio 13 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		internet {
> +			label = "white:internet";
> +			gpios = <&gpio 23 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		usb {
> +			label = "white:usb";
> +			gpios = <&gpio 24 GPIO_ACTIVE_LOW>;
> +			trigger-sources = <&xhci_ehci_port1>,
> <&ehci_port2>;
> +			linux,default-trigger = "usbport";
> +		};
> +
> +		lte {
> +			label = "white:lte";
> +			gpios = <&gpio 26 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		mobile_green {
> +			label = "green:mobile";
> +			gpios = <&gpio 31 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		mobile_orange {
> +			label = "orange:mobile";
> +			gpios = <&gpio 22 GPIO_ACTIVE_LOW>;
> +		};
> +
> +		mobile_red {
> +			label = "red:mobile";
> +			gpios = <&gpio 14 GPIO_ACTIVE_LOW>;
> +		};
> +	};
> +
> +	keys {
> +		compatible = "gpio-keys";
> +
> +		reset {
> +			label = "reset";
> +			gpios = <&gpio 18 GPIO_ACTIVE_LOW>;
> +			linux,code = <KEY_RESTART>;
> +		};
> +
> +		wps {
> +			label = "wps";
> +			gpios = <&gpio 6 GPIO_ACTIVE_LOW>;
> +			linux,code = <KEY_WPS_BUTTON>;
> +		};
> +	};
> +};
> +
> +&nand {
> +	status = "okay";
> +
> +	partitions {
> +		compatible = "fixed-partitions";
> +		#address-cells = <1>;
> +		#size-cells = <1>;
> +
> +		/* There is blank space between the partitions, this has been
> +		   adopted from the manufacturer.
> +		 */. I'd prefer to have a specific comment at the specific position in the partition table, i.e. name the position/offset or start/end and put the comment where the gap is. Otherwise, if you did a mistake somewhere, people will never know if it's a mistake or the expected blank space..
> +		partition at 0 {
> +			label = "Bootloader";
> +			reg = <0x0 0x80000>;
> +			read-only;
> +		};
> +
> +		partition at 80000 {
> +			label = "Config";
> +			reg = <0x80000 0x80000>;
> +		};
> +
> +		factory: partition at 100000 {
> +			label = "Factory";
> +			reg = <0x100000 0x40000>;
> +			read-only;
> +		};
> +
> +		partition at 140000 {
> +			label = "Kernel";
> +			reg = <0x140000 0x1ec0000>;
> +		};
> +
> +		partition at 540000 {
> +			label = "ubi";
> +			reg = <0x540000 0x1ac0000>;
> +		};
> +
> +		partition at 2140000 {
> +			label = "Kernel2";
> +			reg = <0x2140000 0x1ec0000>;
> +		};
> +
> +		partition at 4000000 {
> +			label = "wwan";
> +			reg = <0x4000000 0x100000>;
> +		};
> +
> +		partition at 4100000 {
> +			label = "data";
> +			reg = <0x4100000 0x1000000>;
> +		};
> +
> +		partition at 5100000 {
> +			label = "rom-d";
> +			reg = <0x5100000 0x100000>;
> +			read-only;
> +		};
> +
> +		partition at 5200000 {
> +			label = "reserve";
> +			reg = <0x5200000 0x80000>;
> +		};
> +	};
> +};
> +
> +&pcie {
> +       status = "okay";
> +
> +};
> +
> +&pcie0 {
> +       status = "okay";
> +
> +       mt7615d at 1,0 {.
wifi at 1,0.
> +               compatible = "pci14c3,7615";
> +               reg = <0x0000 0 0 0 0>;
> +               mediatek,firmware-eeprom = "mt7615e_eeprom.bin";
> +               mediatek,mtd-eeprom = <&factory 0x0000>;
> +               mtd-mac-address = <&factory 0xfe6e>;
> +	       mtd-mac-address-increment = <1>;.
- Mentioned files: lib/upgrade/platform.sh, package/boot/uboot-envtools/files/ramips, scripts/checkpatch.pl, target/linux/ramips/dts/mt7621_zyxel_lte3301-plus.dts, target/linux/ramips/image/mt7621.mk

### base-files: fix zoneinfo support: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-April.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-April.txt
- Root message ID: <20210410002248.727974-1-rosenp@gmail.com>
- Problem excerpt: This made the if condition never return true.. Example failure when removing the if condition:.
/tmp/localtime -> /usr/share/zoneinfo/America/Los Angeles. This file does not exist. America/Los_Angeles does..
- Mentioned files: package/base-files/files/etc/init.d/system

### base-files: update min_free_kbytes configuration: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2024-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2024-January.txt
- Root message ID: <20240103023218.274699-1-quic_shoudil@quicinc.com>
- Problem excerpt: Some network drivers allocate memory in atomic context. This limit was set to prevent memory allocation failure in these cases.. What devices/scenarios have you tested this change on? How did you determine what's the proper value for this property?.
>
> Signed-off-by: shoudil <quic_shoudil at quicinc.com>.
- Mentioned files: package/base-files/files/etc/init.d/sysctl

### Moving git.openwrt.org behind Fastly CDN: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2024-December.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2024-December.txt
- Root message ID: <20241204130708.GB56964@meh.true.cz>
- Problem excerpt: Hi,.
git.openwrt.org is currently served by a single VPS server, which is no longer
suitable in this age of AI scraping. That server is being overloaded on daily
basis with spikes of requests, leading quite often to 500s, causing build
failures on our buildbots during feed syncs.. As a first quick fix attempt, I've prepared git.cdn.openwrt.org, which is a
Fastly CDN-backed mirror of git.openwrt.org and would like to serve all the
traffic via Fastly CDN which I hope should alleviate the gitweb based load on
the server as it could be served from the CDN cache.. The CDN is generously provided by Fastly, without any cost to us.
- Mentioned files: include/download.mk

---

## ubus-ipc

- Lesson candidates: 31
- Completeness: complete=20, fragmentary=9, searchable=2
- Common signals: you, ubus-ipc, can, https:, did, following, more, found, details, message, struct, information

Representative referenced problems:

### add compatibility for wolfssl >= 5.0: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-January.txt
- Root message ID: <20220101192846.95891-1-sergey@lobanov.in>
- Problem excerpt: Signed-off-by: Sergey V. Lobanov <sergey at lobanov.in>
---
 ustream-openssl.c | 2 ++
 1 file changed, 2 insertions(+).
[diff: ustream-openssl.c]
[hunk: static bool handle_wolfssl_asn_error(struct ustream_ssl *us, int r)]
+#if LIBWOLFSSL_VERSION_HEX < 0x05000000
+#endif
- Mentioned files: ustream-openssl.c

### Should ubus be marked as target-specific "nonshared"? (broken 21.02 rc2 imagebuilder): mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-June.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-June.txt
- Root message ID: <e775b5d7-6193-856e-93aa-c7928677b03c@aparcar.org>
- Problem excerpt: I think that it might be wise to mark ubus as target-specific "nonshared" 
(PKG_FLAGS:=nonshared). Based on forum discussion, we have currently a broken 21.02.0-rc2 
imagebuilder, as libiwinfo can't find the correct libubus version..
https://forum.openwrt.org/t/21-02-0-rc2-build-error-on-libubus20210215/98373. My reasoning:.
* ubus is a normal (shared) package in the packages/ downloads dir.
* the nonshared libiwinfo depends on libubus with ABI specification..
* ubus has been updated since rc2, so new ubus and libubus versions are now 
offered for download.
* The nonshared libiwinfo is located in the target/ download directory of 
rc2, and it still depends on the older libubus with the old ABI version. And 
that old libubus version has already been replaced by the newer libubus 
version in the normal packages download dir..

### Adding support for Zyxel GS1900-48HPv2: mistake and correction

- Score: 0.95
- Completeness: complete
- Source file: devel/2025-November.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2025-November.txt
- Root message ID: <CAMrSqm+dUeL+DmKO5=9f_yRLOKg3rigdEGc=4BvKw+L=006CYQ@mail.gmail.com>
- Problem excerpt: I
am willing to help in any way I can.. I am ready to test new firmware builds and provide any additional
data, outputs from dmesg, logread, or information from ubus that might
be helpful for debugging the PoE control issue.. The DTS file is attached to this email. Thank you for your time and
for the great work you do on OpenWrt..

### cli: improve error logging for call command: mistake and correction

- Score: 0.95
- Completeness: complete
- Source file: devel/2022-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-February.txt
- Root message ID: <20220218095605.GG56700@meh.true.cz>
- Problem excerpt: Hi,.
> These messages contain absolutely no info that explains where they come
> from; it's not even clear they are coming from ubus. This makes tracking
> down what's causing them virtually impossible..
+1.
> -	return ubus_invoke(ctx, id, argv[1], b.head, receive_call_result_data, NULL, timeout * 1000);
> +	ret = ubus_invoke(ctx, id, argv[1], b.head, receive_call_result_data, NULL, timeout * 1000);
> +	if (ret && !simple_output && !isatty(fileno(stderr) == ENOTTY)) {.
can't you move that !simple and !isatty checks into common place like
print_error() in order to simplify such common use cases?. Other then that, feel free to add my Acked-by:. Cheers,.
- Mentioned files: cli.c

### ath10k-ct iw missing rx stats: mistake and correction

- Score: 0.85
- Completeness: complete
- Source file: devel/2021-February.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-February.txt
- Root message ID: <CA+_ehUyCfg2k2t=8HmE8ndpacgRBCN-jAFVWpJBeUfQne==2+Q@mail.gmail.com>
- Problem excerpt: On 2021-02-14 18:28, Ansuel Smith wrote:
> With recent mac80211 bump I notice that rx stats
> are no longer displayed.
> I ported the atk10-ct patches to the version 5.10
> and I noticed this. It's only me?
> Also this is only to report that ath10k-ct patches can
> be ported with minimal changes and works normally
> (except this problem with ubus not reporting rx stats)
It was an upstream regression. I backported the fix for it and it should
work now..
- Felix

---

## uci-config

- Lesson candidates: 557
- Completeness: complete=414, fragmentary=84, problem-only=22, searchable=37
- Common signals: option, uci-config, you, openwrt, device, did, version, can, config, details, system, due

Representative referenced problems:

### Activate https server support in 21.02 by default: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-May.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-May.txt
- Root message ID: <44535424-df8a-28b3-5f11-d65fe3f1ac95@gmail.com>
- Problem excerpt: 05:00, Petr ?tetiar <ynezz at true.cz> a ?crit :
>
> Fernando Frediani <fhfrediani at gmail.com> [2021-05-11 20:13:18]:
>
> Hi,
>
> > I am no sure https support should still be something by default in the
> > images as it's not something really essential
>
> to me it's like discussion about telnet versus SSH. (Puting aside, that one
> shouldn't be using password at all) If it's fine with you to send your root
> password over telnet, then SSH is not essential, I agree.
>
> FYI HTTPS wouldn't be enabled by default, it would be *available* by default,
> giving users of default release images choice for management of their devices
> over HTTPS, by doing so *explicitly*.. I'm all for HTTPS to be shipped by default
One painfull "bug" that some people might face having both HTTP and HTTPS,
when you login using HTTPS, the sysauth cookie has secure=true,
so you can't login via HTTP anymore because it's trying to modify the
secure=true sysauth cookie :(. Etienne.
> OpenWrt has quite huge community, so I hope, that having HTTPS available in
> default images would bring the currently horrible UX of self-signed
> certificates to wider audience which in turn might foster improvements.
>
> -- ynezz
- Mentioned files: inventories/prod/group_vars/all/02-openwrt-prod.yml

### ath79: add a support for reset key on MikroTik RB912: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-November.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt
- Root message ID: <20211109144607.7571-1-denis281089@gmail.com>
- Problem excerpt: A new key module registers a gpio controller that exports 3 virtual gpio lines:
one output-capable-only for NAND, one input-capable-only for key and one
output-capable-only for NAND to ban a key polling.. While we were implementing a key, we realized that somehow we broke a Wi-Fi:
a kernel started to invoke init function of routerboot partition parser module
too early: when a SPI flash with routerboot partitions hadn't been found yet,
and ath9k failed to load calibration data from hard_config partition.. All seems to be working on my RB912UAG-2HPnD. Tested kernels 5.4 and 5.10..
- Mentioned files: target/linux/ath79/config-5.10, target/linux/ath79/config-5.4, target/linux/ath79/dts/ar9342_mikrotik_routerboard-912uag-2hpnd.dts, target/linux/ath79/files/drivers/gpio/gpio-latch.c, target/linux/ath79/files/drivers/gpio/gpio-rb91x-key.c

### ath79: add support for onion omega: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-August.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-August.txt
- Root message ID: <20210811165437.2280760-1-git@aiyionpri.me>
- Problem excerpt: Hi Jan-Niklas,. On 8/11/21 6:54 PM, Jan-Niklas Burfeind wrote:
> The Onion Omega is a hardware development platform with built-in WiFi.
> 
> https://onioniot.github.io/wiki/
> 
> Specifications:
>  - QCA9331 @ 400 MHz (MIPS 24Kc Big-Endian Processor)
>  - 64MB of DDR2 RAM running at 400 MHz
>  - 16MB of on-board flash storage
>  - Support for USB 2.0
>  - Support for Ethernet at 100 Mbps
>  - 802.11b/g/n WiFi at 150 Mbps
>  - 18 digital GPIOs
>  - A single Serial UART
>  - Support for SPI
>  - Support for I2S
> 
> Flash instructions:
> The device is running OpenWrt upon release using the ar71xx target.
> Both a sysupgrade
> and uploading the factory image using u-boots web-UI do work fine.
> 
> Depending on the ssh client, it might be necessary to enable outdated
> KeyExchange methods e.g. in the clients ssh-config:
> 
> Host 192.168.1.1
>         KexAlgorithms +diffie-hellman-group1-sha1
> 
> The stock credentials are: root onioneer
> 
> For u-boots web-UI manually configure `192.168.1.2/24` on your computer,
> connect to `192.168.1.1`.
> 
> MAC addresses as verified by OEM firmware:
> 2G       phy0      label
> LAN      eth0      label - 1
> 
> LAN is only available in combination with an optional expansion dock.
> 
> Based on vendor acked commit:
> commit 5cd49bb067ca ("ar71xx: add support for Onion Omega")
> 
> Partly reverts:
> commit fc553c7e4c8e ("ath79: drop unused/incomplete dts")
> 
> Signed-off-by: Jan-Niklas Burfeind <git at aiyionpri.me>
> ---
>  target/linux/ath79/dts/ar9331_onion_omega.dts | 138 ++++++++++++++++++
>  .../generic/base-files/etc/board.d/02_network |   1 +
>  target/linux/ath79/image/generic.mk           |  14 ++
>  3 files changed, 153 insertions(+)
>  create mode 100644 target/linux/ath79/dts/ar9331_onion_omega.dts
> 
> diff --git a/target/linux/ath79/dts/ar9331_onion_omega.dts b/target/linux/ath79/dts/ar9331_onion_omega.dts
> new file mode 100644
> index 0000000000..3b72a293b4
> --- /dev/null
> +++ b/target/linux/ath79/dts/ar9331_onion_omega.dts
> @@ -0,0 +1,138 @@
> +// SPDX-License-Identifier: GPL-2.0-or-later OR MIT
> +/dts-v1/;
> +
> +#include <dt-bindings/gpio/gpio.h>
> +#include <dt-bindings/input/input.h>
> +
> +#include "ar9331.dtsi"
> +
> +/ {
> +	model = "Onion Omega";
> +	compatible = "onion,omega", "qca,ar9331";
> +
> +	aliases {
> +		serial0 = &uart;
> +		led-boot = &led_system;
> +		led-failsafe = &led_system;
> +		led-running = &led_system;
> +		led-upgrade = &led_system;
> +	};
> +
> +	leds {
> +		compatible = "gpio-leds";
> +
> +		led_system: system {
> +			label = "onion:amber:system";. Remove the model name from the LED name..
> +			gpios = <&gpio 27 GPIO_ACTIVE_LOW>;
> +		};
> +	};
> +
> +	keys {
> +		compatible = "gpio-keys-polled";
> +		poll-interval = <100>;
> +
> +		button0 {
> +			label = "reset";
> +			linux,code = <KEY_RESTART>;
> +			gpios = <&gpio 11 GPIO_ACTIVE_HIGH>;
> +		};
> +	};
> +};
> +
> +&ref {
> +	clock-frequency = <25000000>;
> +};
> +
> +&uart {
> +	status = "okay";
> +};
> +
> +&gpio {
> +	status = "okay";
> +};
> +
> +&usb {
> +	status = "okay";
> +
> +	dr_mode = "host";
> +};
> +
> +&usb_phy {
> +	status = "okay";
> +};
> +
> +&eth0 {
> +	status = "okay";
> +
> +	compatible = "syscon", "simple-mfd";
> +};
> +
> +&eth1 {
> +	status = "okay";
> +
> +	nvmem-cells = <&macaddr_uboot_1fc00>;
> +	nvmem-cell-names = "mac-address";
> +	mac-address-increment = <(-1)>;
> +
> +	gmac-config {
> +		device = <&gmac>;
> +		switch-phy-addr-swap = <4>;
> +		switch-phy-swap = <4>;
> +	};
> +};
> +
> +
> +&spi {
> +	status = "okay";
> +
> +	num-chipselects = <1>;
> +
> +	/* Winbond 25Q128FVSG SPI flash */
> +	flash at 0 {
> +		compatible = "winbond,w25q128", "jedec,spi-nor";. Drop the winbond compatible - defining model-specific compatible is considered legacy
in case it is not required for Flash-ID duplicates..
> +		spi-max-frequency = <25000000>;
> +		reg = <0>;
> +
> +		partitions {
> +			compatible = "fixed-partitions";
> +			#address-cells = <1>;
> +			#size-cells = <1>;
> +
> +			uboot: partition at 0 {
> +				label = "u-boot";
> +				reg = <0x000000 0x020000>;
> +				read-only;
> +			};
> +
> +			partition at 20000 {
> +				compatible = "tplink,firmware";
> +				label = "firmware";
> +				reg = <0x020000 0xfd0000>;
> +			};
> +
> +			art: partition at ff0000 {
> +				label = "art";
> +				reg = <0xff0000 0x010000>;
> +				read-only;
> +			};
> +		};
> +	};
> +};
> +
> +&wmac {
> +	status = "okay";
> +
> +	mtd-cal-data = <&art 0x1000>;
> +	nvmem-cells = <&macaddr_uboot_1fc00>;
> +	nvmem-cell-names = "mac-address";
> +};
> +
> +&uboot {
> +	compatible = "nvmem-cells";
> +	#address-cells = <1>;
> +	#size-cells = <1>;
> +
> +	macaddr_uboot_1fc00: macaddr at 1fc00 {
> +		reg = <0x1fc00 0x6>;
> +	};
> +};.
- Mentioned files: target/linux/ath79/dts/ar9331_onion_omega.dts, target/linux/ath79/generic/base-files/etc/board.d/02_network, target/linux/ath79/image/generic.mk

### ath79: MikroTik RB912UAG: not working Wi-Fi card in mPCIe slot: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-December.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-December.txt
- Root message ID: <CAKoLU8Nj0zpZx076Av58fhEoxz-wAqmenaXintYw5UUkymbohg@mail.gmail.com>
- Problem excerpt: > Thomas H?hn <thomas.huehn at hs-nordhausen.de> wrote:
>
> We have 5 Mikrotik 912UAG in our Freifunk Network and just build and updated
> them today with latest tunk .. we moved vom ar71xx to ath79 successfully,
> so far so good .. thx for your upstream work!
>
> The only thing that is not working: we can not get your 2nd wifi card in the
> mPCIe port up and running. Only the USB Port is working. We have tried
> several things to switch from USB to mPCIe .. without success:
>
> * change the dts file ar9342_mikrotik_routerboard-912uag-2hpnd.dts in
>   the gpio-export section to have usb_power output = 0 and pcie_power = 1
>   mPCIe port is powered with 3,3V (measured on in 2 & 4) but mPCIe WiFi
>   cards (ath9k - mikrotik) are not detected, tried to rescan the PCI bus
>   as well
> * change on a running 912UAG i the /sys/class/gpio/power_usb
>   ../power-pcie/values ... not WiFi Card detection
> * compare the running und working mPCIe port ar71xx image on the router ...
>   found out there is gpio52 used, but different latch setup .. our good
>   gues was that GPIO20 could be responsible for the usb switch for the mPCIe
>   port .. add gpio20 to the export folder and set it to 1.. but no WiFi card
>   detection
>
> Who has some troubleshooting tips for how to disable the usb port and enable
> the mPCIe port?.
- Mentioned files: target/linux/ath79/dts/ar9342_mikrotik_routerboard-912uag-2hpnd.dts, target/linux/ath79/patches-5.10/451-gpio-74x164-init-val-support.patch

### base-files: Don't enable ULA IPv6 addresses by default in new config: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2022-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2022-September.txt
- Root message ID: <ebb3729e-20a9-a91d-af7b-e7f743437985@gmail.com>
- Problem excerpt: Discovery protocols based on IPv6 multicast and link-local addresses are
  becoming more common (e.g. syncthing) and don't need ULA to work..
- users might be confused to see multiple unrelated IPv6 addresses on
  their devices. Or they might wrongly conclude that they have IPv6
  connectivity thanks to ULA addresses, while in fact ULA addresses are
  not globally routable..
- there have been various bug reports [1, 2, 3] in 19.07 and 21.02 where
  ULA addresses basically break global IPv6 connectivity. These bugs have
  not been solved in several years, indicating a probable lack of interest
  for ULA from the OpenWrt developer community.. ULA addresses are still supported, e.g. by setting
network.globals.ula_prefix='auto' in a uci-defaults script that runs
before "12_network-generate-ula", or by directly setting
network.globals.ula_prefix to a /48 prefix..
[1] https://github.com/openwrt/openwrt/issues/5082
[2] https://forum.openwrt.org/t/router-can-use-ipv6-ok-but-clients-in-lan-cannot/57587
[3] https://lafibre.info/ipv6/saison-2-openwrt-slaac-problemes/.
- Mentioned files: package/base-files/files/bin/config_generate

---

## uncategorized

- Lesson candidates: 1140
- Completeness: complete=938, fragmentary=138, problem-only=30, searchable=34
- Common signals: you, uncategorized, can, https:, did, following, message, details, more, bugs.openwrt.org, index.php, task_id

Representative referenced problems:

### 802.11v: hostapd: time_zone: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2021-December.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2021-December.txt
- Root message ID: <b344424d-ef99-570f-e9e1-2a25bf31a945@gmail.com>
- Problem excerpt: Time appears in beacon frames. e.g.. Tag: Time Advertisement
     Tag Number: Time Advertisement (69)
     Tag length: 17
     Timing capabilities: UTC time at which the TSF timer is 0 (2)
     Time Value: e5070c07022b24000000: current time=2021-12-07 02:44:10
     Time Error: 0000000000
     Time Update Counter: 0.
== time_zone ==
(set as CET-1CEST,M3.5.0,M10.5.0/3). Result: NOK. Time Zone never appears in beacon frames..

### Adding a new x86 image or related packages to the default x86 image: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-September.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-September.txt
- Root message ID: <8682698C-4740-430A-906D-B8DE1AA93C1A@aparcar.org>
- Problem excerpt: Furthermore, x86 devices have often no device identity like other devices using device tree do. With the current implementation, the attended sysupgrade service would be broken since on x86 always use the ?generic? image..
@David since you pulled the PR[1] to your staging tree[2], do you mind modifying the commits (for now) that the new packages are added to the default image?. Best,
Paul.
[1]: https://github.com/openwrt/openwrt/pull/13418
[2]: https://git.openwrt.org/?p=openwrt/staging/blocktrron.git;a=summary

### base-files: Remove nand.sh dependency from emmc upgrade: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-January.txt
- Root message ID: <20230102232534.592501-1-computersforpeace@gmail.com>
- Problem excerpt: Normalize = `make kernel_menuconfig`, save.. Signed-off-by: Brian Norris <computersforpeace at gmail.com>
---.
 target/linux/ipq806x/config-5.15 | 20 +++++++++++---------
 1 file changed, 11 insertions(+), 9 deletions(-).
[diff: target/linux/ipq806x/config-5.15]
[hunk: CONFIG_ARM_CPU_SUSPEND=y]
+# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
+# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-CONFIG_ARM_QCOM_CPUFREQ_KRAIT=y
[hunk: CONFIG_CRC16=y]
-CONFIG_CRYPTO_BLAKE2S=y
-CONFIG_CRYPTO_GF128MUL=y
[hunk: CONFIG_CRYPTO_JITTERENTROPY=y]
-CONFIG_CRYPTO_NULL2=y
[hunk: CONFIG_DEVFREQ_GOV_PASSIVE=y]
-# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
[hunk: CONFIG_DWMAC_IPQ806X=y]
+CONFIG_ETHERNET_PACKET_MANGLE=y
[hunk: CONFIG_GENERIC_BUG=y]
+CONFIG_GENERIC_CPU_VULNERABILITIES=y
+CONFIG_GENERIC_IRQ_MIGRATION=y
[hunk: CONFIG_GENERIC_STRNCPY_FROM_USER=y]
+CONFIG_GLOB=y
[hunk: CONFIG_HAS_IOPORT_MAP=y]
+CONFIG_HOTPLUG_CPU=y
[hunk: CONFIG_IRQ_FASTEOI_HIERARCHY_HANDLERS=y]
+CONFIG_KMAP_LOCAL_NON_LINEAR_PTE_ARRAY=y
-CONFIG_LLD_VERSION=0
[hunk: CONFIG_NO_HZ_IDLE=y]
+CONFIG_NVMEM_SYSFS=y
[hunk: CONFIG_OF_GPIO=y]
-CONFIG_OF_NET=y
[hunk: CONFIG_QCOM_SCM=y]
-# CONFIG_QCOM_SOCINFO is not set
+CONFIG_QCOM_SOCINFO=y
[hunk: CONFIG_SMP_ON_UP=y]
+CONFIG_SOC_BUS=y
- Mentioned files: lib/upgrade/common.sh, lib/upgrade/platform.sh, package/base-files/files/lib/upgrade/common.sh, package/base-files/files/lib/upgrade/emmc.sh, package/base-files/files/lib/upgrade/nand.sh

### base-files: Remove nand.sh dependency from emmc upgrade: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-January.txt
- Root message ID: <20230107074945.2140362-1-computersforpeace@gmail.com>
- Problem excerpt: Signed-off-by: Brian Norris <computersforpeace at gmail.com>
---. Changes in v2:
 * Improve description.
 target/linux/ipq806x/config-5.15 | 20 +++++++++++---------
 1 file changed, 11 insertions(+), 9 deletions(-).
[diff: target/linux/ipq806x/config-5.15]
[hunk: CONFIG_ARM_CPU_SUSPEND=y]
+# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
+# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-CONFIG_ARM_QCOM_CPUFREQ_KRAIT=y
[hunk: CONFIG_CRC16=y]
-CONFIG_CRYPTO_BLAKE2S=y
-CONFIG_CRYPTO_GF128MUL=y
[hunk: CONFIG_CRYPTO_JITTERENTROPY=y]
-CONFIG_CRYPTO_NULL2=y
[hunk: CONFIG_DEVFREQ_GOV_PASSIVE=y]
-# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
[hunk: CONFIG_DWMAC_IPQ806X=y]
+CONFIG_ETHERNET_PACKET_MANGLE=y
[hunk: CONFIG_GENERIC_BUG=y]
+CONFIG_GENERIC_CPU_VULNERABILITIES=y
+CONFIG_GENERIC_IRQ_MIGRATION=y
[hunk: CONFIG_GENERIC_STRNCPY_FROM_USER=y]
+CONFIG_GLOB=y
[hunk: CONFIG_HAS_IOPORT_MAP=y]
+CONFIG_HOTPLUG_CPU=y
[hunk: CONFIG_IRQ_FASTEOI_HIERARCHY_HANDLERS=y]
+CONFIG_KMAP_LOCAL_NON_LINEAR_PTE_ARRAY=y
-CONFIG_LLD_VERSION=0
[hunk: CONFIG_NR_CPUS=2]
+CONFIG_NVMEM_SYSFS=y
[hunk: CONFIG_OF_GPIO=y]
-CONFIG_OF_NET=y
[hunk: CONFIG_QCOM_SCM=y]
-# CONFIG_QCOM_SOCINFO is not set
+CONFIG_QCOM_SOCINFO=y
[hunk: CONFIG_SMP_ON_UP=y]
+CONFIG_SOC_BUS=y
- Mentioned files: lib/alloca.c, lib/gnulib.mk, lib/local.mk, lib/upgrade/common.sh, lib/upgrade/platform.sh

### base-files: Remove nand.sh dependency from emmc upgrade: mistake and correction

- Score: 1.0
- Completeness: complete
- Source file: devel/2023-January.txt
- Archive URL: https://lists.openwrt.org/pipermail/openwrt-devel/2023-January.txt
- Root message ID: <20230111070652.1200657-1-computersforpeace@gmail.com>
- Problem excerpt: Signed-off-by: Brian Norris <computersforpeace at gmail.com>
---.
(no changes since v2). Changes in v2:
 * Improve description.
 target/linux/ipq806x/config-5.15 | 20 +++++++++++---------
 1 file changed, 11 insertions(+), 9 deletions(-).
[diff: target/linux/ipq806x/config-5.15]
[hunk: CONFIG_ARM_CPU_SUSPEND=y]
+# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
+# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-CONFIG_ARM_QCOM_CPUFREQ_KRAIT=y
[hunk: CONFIG_CRC16=y]
-CONFIG_CRYPTO_BLAKE2S=y
-CONFIG_CRYPTO_GF128MUL=y
[hunk: CONFIG_CRYPTO_JITTERENTROPY=y]
-CONFIG_CRYPTO_NULL2=y
[hunk: CONFIG_DEVFREQ_GOV_PASSIVE=y]
-# CONFIG_ARM_KRAIT_CACHE_DEVFREQ is not set
-# CONFIG_ARM_IPQ806X_FAB_DEVFREQ is not set
[hunk: CONFIG_DWMAC_IPQ806X=y]
+CONFIG_ETHERNET_PACKET_MANGLE=y
[hunk: CONFIG_GENERIC_BUG=y]
+CONFIG_GENERIC_CPU_VULNERABILITIES=y
+CONFIG_GENERIC_IRQ_MIGRATION=y
[hunk: CONFIG_GENERIC_STRNCPY_FROM_USER=y]
+CONFIG_GLOB=y
[hunk: CONFIG_HAS_IOPORT_MAP=y]
+CONFIG_HOTPLUG_CPU=y
[hunk: CONFIG_IRQ_FASTEOI_HIERARCHY_HANDLERS=y]
+CONFIG_KMAP_LOCAL_NON_LINEAR_PTE_ARRAY=y
-CONFIG_LLD_VERSION=0
[hunk: CONFIG_NR_CPUS=2]
+CONFIG_NVMEM_SYSFS=y
[hunk: CONFIG_OF_GPIO=y]
-CONFIG_OF_NET=y
[hunk: CONFIG_QCOM_SCM=y]
-# CONFIG_QCOM_SOCINFO is not set
+CONFIG_QCOM_SOCINFO=y
[hunk: CONFIG_SMP_ON_UP=y]
+CONFIG_SOC_BUS=y
- Mentioned files: include/dt-bindings/leds/common.h, lib/upgrade/common.sh, lib/upgrade/platform.sh, package/base-files/files/lib/upgrade/common.sh, package/base-files/files/lib/upgrade/emmc.sh

---
