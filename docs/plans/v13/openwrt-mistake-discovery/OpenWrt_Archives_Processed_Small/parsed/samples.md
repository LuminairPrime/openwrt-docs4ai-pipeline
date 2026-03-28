# QA Samples

Randomly selected records for manual inspection.

## Sample 1

```json
{
  "source_file": "devel/2023-May.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2023-May.txt",
  "byte_offset": 276408,
  "mbox_from_line": "From linus.walleij at linaro.org  Sat May 13 14:21:36 2023",
  "message_id": "<20230513212137.1272012-4-linus.walleij@linaro.org>",
  "in_reply_to": "<20230513212137.1272012-1-linus.walleij@linaro.org>",
  "references": [
    "<20230513212137.1272012-1-linus.walleij@linaro.org>"
  ],
  "from_addr": "linus.walleij@linaro.org",
  "from_name": "",
  "date_raw": "Sat, 13 May 2023 23:21:36 +0200",
  "date_iso": "2023-05-13T23:21:36+02:00",
  "subject": "[PATCH 3/4] bcm53xx: dir885/dir890: Tag both partitions as SEAMA",
  "body_for_scoring": "The newly added D-Link DIR-890L also needs to have a seama\ntag on its partition so that it will be split properly by\nmtdsplit.\n\nSigned-off-by: Linus Walleij <linus.walleij at linaro.org>\n---\n ...-dts-BCM5301X-Describe-partition-formats.patch | 15 +++++++++++++--\n 1 file changed, 13 insertions(+), 2 deletions(-)\n\n[diff: target/linux/bcm53xx/patches-5.15/321-ARM-dts-BCM5301X-Describe-partition-formats.patch]\n-From 7166207bd1d8c46d09d640d46afc685df9bb9083 Mon Sep 17 00:00:00 2001\n+From a054e2fe2d00bd32f308986de654b66f054083d2 Mon Sep 17 00:00:00 2001\n[hunk: It's needed by OpenWrt for custom partitioning.]\n- 1 file changed, 1 insertion(+)\n+ arch/arm/boot/dts/bcm47094-dlink-dir-890l.dts | 1 +\n+ 2 files changed, 2 insertions(+)\n[hunk: Signed-off-by: Rafa? Mi?ecki <rafal at milecki.pl>]\n+@@ -151,6 +151,7 @@\n+ \t\tfirmware at 0 {\n+ \t\t\tlabel = \"firmware\";\n+ \t\t\treg = <0x00000000 0x08000000>;\n+ \t\t};",
  "body_no_diff": "The newly added D-Link DIR-890L also needs to have a seama\ntag on its partition so that it will be split properly by\nmtdsplit.\n\nSigned-off-by: Linus Walleij <linus.walleij at linaro.org>\n---\n ...-dts-BCM5301X-Describe-partition-formats.patch | 15 +++++++++++++--\n 1 file changed, 13 insertions(+), 2 deletions(-)\n\n[diff: target/linux/bcm53xx/patches-5.15/321-ARM-dts-BCM5301X-Describe-partition-formats.patch]\n-From 7166207bd1d8c46d09d640d46afc685df9bb9083 Mon Sep 17 00:00:00 2001\n+From a054e2fe2d00bd32f308986de654b66f054083d2 Mon Sep 17 00:00:00 2001\n[hunk: It's needed by OpenWrt for custom partitioning.]\n- 1 file changed, 1 insertion(+)\n+ arch/arm/boot/dts/bcm47094-dlink-dir-890l.dts | 1 +\n+ 2 files changed, 2 insertions(+)\n[hunk: Signed-off-by: Rafa? Mi?ecki <rafal at milecki.pl>]\n+@@ -151,6 +151,7 @@\n+ \t\tfirmware at 0 {\n+ \t\t\tlabel = \"firmware\";\n+ \t\t\treg = <0x00000000 0x08000000>;\n+ \t\t};",
  "quoted_context_pairs": [],
  "mentioned_files": [
    "target/linux/bcm53xx/patches-5.15/321-ARM-dts-BCM5301X-Describe-partition-formats.patch"
  ],
  "mentioned_commits": [],
  "keyword_matches": [
    "proper(?:ly)?"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "kernel-driver"
  ],
  "has_patch_subject": true,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 2

```json
{
  "source_file": "bugs/2021-October.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-October.txt",
  "byte_offset": 221187,
  "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Wed Oct 20 11:49:18 2021",
  "message_id": "<mailman.8103.1634755764.1923571.openwrt-bugs@lists.openwrt.org>",
  "in_reply_to": "<FS4101@bugs.openwrt.org>",
  "references": [
    "<FS4101@bugs.openwrt.org>"
  ],
  "from_addr": "openwrt-bugs@lists.openwrt.org",
  "from_name": "",
  "date_raw": "Wed, 20 Oct 2021 18:49:18 +0000",
  "date_iso": "2021-10-20T18:49:18+00:00",
  "subject": "[FS#4101] Meraki 5G radio : cannot use high channels (52 upwards)",
  "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nA new Flyspray task has been opened.  Details are below. \n\nUser who did this - Mark Shickell (mash2895) \n\nAttached to Project - OpenWrt/LEDE Project\nSummary - Meraki 5G radio : cannot use high channels (52 upwards)\nTask Type - Bug Report\nCategory - Base system\nStatus - Unconfirmed\nAssigned To - \nOperating System - All\nSeverity - Low\nPriority - Very Low\nReported Version - openwrt-19.07\nDue in Version - Undecided\nDue Date - Undecided\nDetails - Name the tree/revision/version\nOpenWrt 19.07.8 r11364-ef56c85848 / LuCI openwrt-19.07 branch git-21.189.23240-7b931da\n\nName the affected device\nMeraki MR33\n\nWhat does it do that it should not do / what does it not do that it should do\nChannels 36-48 seem ok on the 5G radio but others don't work\n\nSteps to reproduce\nI set radio0 to channel 52 and the radio becomes inactive\n\nWhat you have already done to workaround/fix the problem\nfix to channel 48\n\nAny additional info you think is important\nI can get you one to play with remotely if it helps\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4101\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nA new Flyspray task has been opened.  Details are below. \n\nUser who did this - Mark Shickell (mash2895) \n\nAttached to Project - OpenWrt/LEDE Project\nSummary - Meraki 5G radio : cannot use high channels (52 upwards)\nTask Type - Bug Report\nCategory - Base system\nStatus - Unconfirmed\nAssigned To - \nOperating System - All\nSeverity - Low\nPriority - Very Low\nReported Version - openwrt-19.07\nDue in Version - Undecided\nDue Date - Undecided\nDetails - Name the tree/revision/version\nOpenWrt 19.07.8 r11364-ef56c85848 / LuCI openwrt-19.07 branch git-21.189.23240-7b931da\n\nName the affected device\nMeraki MR33\n\nWhat does it do that it should not do / what does it not do that it should do\nChannels 36-48 seem ok on the 5G radio but others don't work\n\nSteps to reproduce\nI set radio0 to channel 52 and the radio becomes inactive\n\nWhat you have already done to workaround/fix the problem\nfix to channel 48\n\nAny additional info you think is important\nI can get you one to play with remotely if it helps\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4101\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [
    "7b931da",
    "ef56c85848"
  ],
  "keyword_matches": [
    "bug",
    "do\\s+not|don't",
    "luci",
    "uci"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": true,
    "has_patch_revision": false
  },
  "categories": [
    "uci-config",
    "luci-frontend"
  ],
  "has_patch_subject": false,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 3

```json
{
  "source_file": "bugs/2021-February.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-February.txt",
  "byte_offset": 112963,
  "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Mon Feb 15 05:11:58 2021",
  "message_id": "<mailman.1472.1613383922.929.openwrt-bugs@lists.openwrt.org>",
  "in_reply_to": "<FS1170@bugs.openwrt.org>",
  "references": [
    "<FS1170@bugs.openwrt.org>"
  ],
  "from_addr": "openwrt-bugs@lists.openwrt.org",
  "from_name": "",
  "date_raw": "Mon, 15 Feb 2021 10:11:58 +0000",
  "date_iso": "2021-02-15T10:11:58+00:00",
  "subject": "[FS#1170] mt7621: kernel errors - rcu_sched detected stalls on CPUs/tasks - again",
  "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task is now closed:\n\nFS#1170 - mt7621: kernel errors - rcu_sched detected stalls on CPUs/tasks - again\nUser who did this - Baptiste Jonglez (bjonglez)\n\nReason for closing: Won't fix\nAdditional comments about closing: Closing as there have been many changes since then. Might be related to FS#2628.\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=1170\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task is now closed:\n\nFS#1170 - mt7621: kernel errors - rcu_sched detected stalls on CPUs/tasks - again\nUser who did this - Baptiste Jonglez (bjonglez)\n\nReason for closing: Won't fix\nAdditional comments about closing: Closing as there have been many changes since then. Might be related to FS#2628.\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=1170\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [],
  "keyword_matches": [
    "bug",
    "do\\s+not|don't"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": true,
    "has_patch_revision": false
  },
  "categories": [
    "kernel-driver"
  ],
  "has_patch_subject": false,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 4

```json
{
  "source_file": "devel/2024-November.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2024-November.txt",
  "byte_offset": 302883,
  "mbox_from_line": "From christoph.hartmann at posteo.de  Wed Nov 20 23:52:55 2024",
  "message_id": "<d440834b-c9c0-4d3e-89f9-7d5a0fbdcdd6@posteo.de>",
  "in_reply_to": "<ec2dca0e-d576-4bf3-af31-bf8f7c2c9527@gmail.com>",
  "references": [
    "<fc615532-dd48-47f2-9cf1-23eccfd3d6a9@posteo.mx>",
    "<ec2dca0e-d576-4bf3-af31-bf8f7c2c9527@gmail.com>"
  ],
  "from_addr": "christoph.hartmann@posteo.de",
  "from_name": "",
  "date_raw": "Thu, 21 Nov 2024 07:52:55 +0000",
  "date_iso": "2024-11-21T07:52:55+00:00",
  "subject": "ULA prefix lifetime",
  "body_for_scoring": "This patch of your would allow to specify a lifetime per prefix on all \ninterfaces?\n\nThis would be nice as it would solve my problem. My idea for a patch \nwould just set have set a custom lifetime for the ULA prefix to keep the \nconfiguration simple.\n\n\nI'm new to the list - is there some kind of \" voting system\" to express \ninterest to get a patch merged or looked into by the main developer?\n\n//chriss\n\nOn 11/20/24 22:34, Paul D wrote:",
  "body_no_diff": "This patch of your would allow to specify a lifetime per prefix on all \ninterfaces?\n\nThis would be nice as it would solve my problem. My idea for a patch \nwould just set have set a custom lifetime for the ULA prefix to keep the \nconfiguration simple.\n\n\nI'm new to the list - is there some kind of \" voting system\" to express \ninterest to get a patch merged or looked into by the main developer?\n\n//chriss\n\nOn 11/20/24 22:34, Paul D wrote:\n> I proposed a 'fix' or, at least, a new feature to specify prefix lifetimes about a half-year ago which @Ansuel just reviewed a few days ago.\n>\n> See\n>\n> [RFC PATCH 08/14] router: clamp prefix valid_lt to interface valid_lifetime\n>\n> which... ideally should go in a separate patch (but this version depended on changes in the named patch-set)\n>\n> It's in his inbox for further review/merge.\n>\n> Otherwise prefixes stick around forever and start fucking shit up in your environment. I triggered a DoS in some systems which I won't name because of this >:)\n>\n>\n>\n>\n> On 2024-11-20 16:54, chriss wrote:\n>> Hi\n>>\n>> I have the following scenario:\n>>\n>> - a router with openwrt\n>>\n>> - a (german) VDSL connection with IPv4 and IPv6\n>>\n>> - a delegated IPv6 prefix (/56) that I use in my internal LAN segments\n>>\n>> My problem:\n>>\n>> I happens that I have to reconnect my VDSL (update of router, tripped over cable, whatever) - with that I get a new IPv6 prefix delegated. Now my clients have 2 prefixes/addresses. The old one (before the router reboot/reconnect) and a new one. That's bad because the old one won't route anymore. simple solution: set the lifetime to sth like 5min or so and the old addresses gets deprecated fast enough.\n>>\n>> Now my ULA addresses have also?a lifetime of 5min - which is bad because after 5 min of router downtime (update) I lose my local delivery between clients.\n>>\n>> My solution (to this very specific and edge case problem) would be to set a large lifetime for ULA prefixes and use a short one for WAN delegated.\n>>\n>> My idea would be to allow the user to set (optional) a ULA lifetime where one can specify the ULA prefix. The odhcpd process would then use this config entry and send RA with the respective lifetime.\n>>\n>>\n>> I write to gather feedback and maybe alternative solutions and if a path / PR for my solution would be accepted.\n>>\n>>\n>>\n>> kind regards\n>>\n>> //chriss\n>>\n>>\n>> _______________________________________________\n>> openwrt-devel mailing list\n>> openwrt-devel at lists.openwrt.org\n>> https://lists.openwrt.org/mailman/listinfo/openwrt-devel\n>\n> _______________________________________________\n> openwrt-devel mailing list\n> openwrt-devel at lists.openwrt.org\n> https://lists.openwrt.org/mailman/listinfo/openwrt-devel",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [],
  "keyword_matches": [],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "uci-config",
    "networking",
    "package-packaging"
  ],
  "has_patch_subject": false,
  "has_keyword_match": false,
  "disposition": "primary"
}
```

## Sample 5

```json
{
  "source_file": "devel/2021-June.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-June.txt",
  "byte_offset": 151123,
  "mbox_from_line": "From e9hack at gmail.com  Fri Jun  4 06:22:57 2021",
  "message_id": "<e3201d01-258f-780c-448e-b336bde7f9e2@gmail.com>",
  "in_reply_to": null,
  "references": [],
  "from_addr": "e9hack@gmail.com",
  "from_name": "",
  "date_raw": "Fri, 04 Jun 2021 15:22:57 +0200",
  "date_iso": "2021-06-04T15:22:57+02:00",
  "subject": "wrong activation of internal radius server",
  "body_for_scoring": "Hi,\n\nOpenWrt has been supporting hostapd's internal radius server for a few days. For several years there has been a line in the init-script that activates the internal radius server too. I think this is wrong (from hostapd.sh):\n\n\t[ -n \"$wps_possible\" -a -n \"$config_methods\" ] && {\n\t\tset_default ext_registrar 0\n\t\tset_default wps_device_type \"6-0050F204-1\"\n\t\tset_default wps_device_name \"OpenWrt AP\"\n\t\tset_default wps_manufacturer \"www.openwrt.org\"\n\t\tset_default wps_independent 1\n\n\t\twps_state=2\n\t\t[ -n \"$wps_not_configured\" ] && wps_state=1\n\n\t\t[ \"$ext_registrar\" -gt 0 -a -n \"$network_bridge\" ] && append bss_conf \"upnp_iface=$network_bridge\" \"$N\"\n\n===>\t\tappend bss_conf \"eap_server=1\" \"$N\"\n\t\t[ -n \"$wps_pin\" ] && append bss_conf \"ap_pin=$wps_pin\" \"$N\"\n\n\nRegards,\nHartmut",
  "body_no_diff": "Hi,\n\nOpenWrt has been supporting hostapd's internal radius server for a few days. For several years there has been a line in the init-script that activates the internal radius server too. I think this is wrong (from hostapd.sh):\n\n\t[ -n \"$wps_possible\" -a -n \"$config_methods\" ] && {\n\t\tset_default ext_registrar 0\n\t\tset_default wps_device_type \"6-0050F204-1\"\n\t\tset_default wps_device_name \"OpenWrt AP\"\n\t\tset_default wps_manufacturer \"www.openwrt.org\"\n\t\tset_default wps_independent 1\n\n\t\twps_state=2\n\t\t[ -n \"$wps_not_configured\" ] && wps_state=1\n\n\t\t[ \"$ext_registrar\" -gt 0 -a -n \"$network_bridge\" ] && append bss_conf \"upnp_iface=$network_bridge\" \"$N\"\n\n===>\t\tappend bss_conf \"eap_server=1\" \"$N\"\n\t\t[ -n \"$wps_pin\" ] && append bss_conf \"ap_pin=$wps_pin\" \"$N\"\n\n\nRegards,\nHartmut",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [
    "0050f204"
  ],
  "keyword_matches": [
    "wrong"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "build-system",
    "networking"
  ],
  "has_patch_subject": false,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 6

```json
{
  "source_file": "devel/2021-January.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt",
  "byte_offset": 1692513,
  "mbox_from_line": "From zajec5 at gmail.com  Wed Jan 20 10:16:06 2021",
  "message_id": "<7421f91e-88ba-c52d-bcf8-e3bdc0c65b0c@gmail.com>",
  "in_reply_to": "<20210120143527.14434-2-bjorn@mork.no>",
  "references": [
    "<20210120143527.14434-1-bjorn@mork.no>",
    "<20210120143527.14434-2-bjorn@mork.no>"
  ],
  "from_addr": "zajec5@gmail.com",
  "from_name": "",
  "date_raw": "Wed, 20 Jan 2021 16:16:06 +0100",
  "date_iso": "2021-01-20T16:16:06+01:00",
  "subject": "[PATCH v3 01/10] dt-bindings: mtd: partitions: add OpenWrt defined U-Boot Image",
  "body_for_scoring": "On 20.01.2021 15:35, Bj?rn Mork wrote:\n\nDid you check that binding with the dt_binding_check?\n\nSomething like:\nmake dt_binding_check DT_SCHEMA_FILES=Documentation/devicetree/bindings/mtd/partitions/openwrt,uimage.yaml\n(you may need arch too, e.g. ARCH=arm64)\n\nI think preferred license for yaml (that dt_binding_check checks for) is\n# SPDX-License-Identifier: GPL-2.0-only OR BSD-2-Clause",
  "body_no_diff": "On 20.01.2021 15:35, Bj?rn Mork wrote:\n> @@ -0,0 +1,91 @@\n> +# SPDX-License-Identifier: GPL-2.0\n> +%YAML 1.2\n> +---\n> +$id: http://devicetree.org/schemas/mtd/partitions/openwrt,uimage.yaml#\n> +$schema: http://devicetree.org/meta-schemas/core.yaml#\n> +\n> +title: OpenWrt variations of U-Boot Image partitions\n> +\n> +maintainers:\n> +  - Bj?rn Mork <bjorn at mork.no>\n> +\n> +description: |\n> +  The image format defined by the boot loader \"Das U-Boot\" is often\n> +  modified or extended by device vendors. This defines a few optional\n> +  properties which can be used to describe such modifications.\n> +\n> +# partition.txt defines common properties, but has not yet been\n> +# converted to YAML\n> +#allOf:\n> +#  - $ref: ../partition.yaml#\n> +\n> +properties:\n> +  compatible:\n> +    items:\n> +      - enum:\n> +          - openwrt,uimage\n> +      - const: denx,uimage\n> +\n> +  openwrt,padding:\n> +    description: Number of padding bytes between header and data\n> +    $ref: /schemas/types.yaml#/definitions/uint32\n> +    default: 0\n> +\n> +  openwrt,ih-magic:\n> +    description: U-Boot Image Header magic number.\n> +    $ref: /schemas/types.yaml#/definitions/uint32\n> +    default: 0x27051956 # IH_MAGIC\n> +\n> +  openwrt,ih-type:\n> +    description: U-Boot Image type\n> +    $ref: /schemas/types.yaml#/definitions/uint32\n> +    default: 2 # IH_TYPE_KERNEL\n> +\n> +  openwrt,offset:\n> +    description:\n> +      Offset between partition start and U-Boot Image in bytes\n> +    $ref: /schemas/types.yaml#/definitions/uint32\n> +    default: 0\n> +\n> +  openwrt,partition-magic:\n> +    description:\n> +      Magic number found at the start of the partition. Will only be\n> +      validated if both this property and openwrt,offset is non-zero\n> +    $ref: /schemas/types.yaml#/definitions/uint32\n> +    default: 0\n> +\n> +required:\n> +  - compatible\n> +  - reg\n> +\n> +#unevaluatedProperties: false\n> +additionalProperties: false\n> +\n> +examples:\n> +  - |\n> +    // device with non-default magic\n> +    partition at 300000 {\n> +          compatible = \"openwrt,uimage\", \"denx,uimage\";\n> +          reg = <0x00300000 0xe80000>;\n> +          label = \"firmware\";\n> +          openwrt,ih-magic = <0x4e474520>;\n> +    };\n> +  - |\n> +    // device with U-Boot Image at an offset, with a partition magic value\n> +    partition at 70000 {\n> +          compatible = \"openwrt,uimage\", \"denx,uimage\";\n> +          reg = <0x00070000 0x00790000>;\n> +          label = \"firmware\";\n> +          openwrt,offset = <20>;\n> +          openwrt,partition-magic = <0x43535953>;\n> +    };\n> +  - |\n> +    // device using a non-default image type\n> +    #include \"dt-bindings/mtd/partitions/uimage.h\"\n> +    partition at 6c0000 {\n> +          compatible = \"openwrt,uimage\", \"denx,uimage\";\n> +          reg = <0x6c0000 0x1900000>;\n> +          label = \"firmware\";\n> +          openwrt,ih-magic = <0x33373033>;\n> +          openwrt,ih-type = <IH_TYPE_FILESYSTEM>;\n> +    };\n\nDid you check that binding with the dt_binding_check?\n\nSomething like:\nmake dt_binding_check DT_SCHEMA_FILES=Documentation/devicetree/bindings/mtd/partitions/openwrt,uimage.yaml\n(you may need arch too, e.g. ARCH=arm64)\n\nI think preferred license for yaml (that dt_binding_check checks for) is\n# SPDX-License-Identifier: GPL-2.0-only OR BSD-2-Clause",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [],
  "keyword_matches": [
    "\\[PATCH\\s+v[2-9]"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "c-language",
    "uci-config",
    "kernel-driver"
  ],
  "has_patch_subject": true,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 7

```json
{
  "source_file": "devel/2021-January.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-January.txt",
  "byte_offset": 239387,
  "mbox_from_line": "From mail at adrianschmutzler.de  Sun Jan  3 07:21:51 2021",
  "message_id": "<002e01d6e1cb$05dd7ae0$119870a0$@adrianschmutzler.de>",
  "in_reply_to": "<20210103003307.1211324-1-rsalvaterra@gmail.com>",
  "references": [
    "<20210103003307.1211324-1-rsalvaterra@gmail.com>"
  ],
  "from_addr": "mail@adrianschmutzler.de",
  "from_name": "",
  "date_raw": "Sun, 03 Jan 2021 13:21:51 +0100",
  "date_iso": "2021-01-03T13:21:51+01:00",
  "subject": "[PATCH] kernel/pending-5.4: enable DCDE for x86(-64)",
  "body_for_scoring": "Hi,\n\n\nShouldn't it be in target/linux/x86 then?\n\nBest\n\nAdrian\n\n-------------- next part --------------\nA non-text attachment was scrubbed...\nName: openpgp-digital-signature.asc\nType: application/pgp-signature\nSize: 834 bytes\nDesc: not available\nURL: <http://lists.openwrt.org/pipermail/openwrt-devel/attachments/20210103/96afa6fd/attachment.sig>",
  "body_no_diff": "Hi,\n\n> -----Original Message-----\n> From: openwrt-devel [mailto:openwrt-devel-bounces at lists.openwrt.org]\n> On Behalf Of Rui Salvaterra\n> Sent: Sonntag, 3. Januar 2021 01:33\n> To: openwrt-devel at lists.openwrt.org\n> Cc: hauke at hauke-m.de; daniel at makrotopia.org; Rui Salvaterra\n> <rsalvaterra at gmail.com>\n> Subject: [PATCH] kernel/pending-5.4: enable DCDE for x86(-64)\n> \n> Port and adapt Nick Piggin's original patch [1]. This enables dead code and\n> data elimination at linking time (gc-sections) on x86(-64).\n\nShouldn't it be in target/linux/x86 then?\n\nBest\n\nAdrian\n\n> \n> openwrt-x86-64-generic-kernel.bin size, with my config:\n> \n> Before:\t3138048 bytes\n> After:\t2937344 bytes\n> \n> In other words, we save about 100 kB.\n> \n> [1] https://lore.kernel.org/lkml/20170709031333.29443-1-\n> npiggin at gmail.com/\n> \n> Signed-off-by: Rui Salvaterra <rsalvaterra at gmail.com>\n> ---\n>  ...nable-dead-code-and-data-elimination.patch | 127\n> ++++++++++++++++++\n>  1 file changed, 127 insertions(+)\n>  create mode 100644 target/linux/generic/pending-5.4/350-x86-enable-\n> dead-code-and-data-elimination.patch\n> \n> diff --git a/target/linux/generic/pending-5.4/350-x86-enable-dead-code-\n> and-data-elimination.patch b/target/linux/generic/pending-5.4/350-x86-\n> enable-dead-code-and-data-elimination.patch\n> new file mode 100644\n> index 0000000000..392ddd71ce\n> --- /dev/null\n> +++ b/target/linux/generic/pending-5.4/350-x86-enable-dead-code-and-\n> data\n> +++ -elimination.patch\n> @@ -0,0 +1,127 @@\n> +From f08a0e4e59f92b4a88501653761cbca08935b9b6 Mon Sep 17 00:00:00\n> 2001\n> +From: Rui Salvaterra <rsalvaterra at gmail.com>\n> +Date: Wed, 4 Nov 2020 19:45:04 +0000\n> +Subject: [PATCH] x86: enable dead code and data elimination\n> +\n> +Adapt Nick Piggin's original patch [1]. This saves nearly 300 kiB on\n> +the final vmlinuz (zstd-compressed).\n> +\n> +[1]\n> +https://lore.kernel.org/lkml/20170709031333.29443-1-npiggin at gmail.com/\n> +\n> +Signed-off-by: Rui Salvaterra <rsalvaterra at gmail.com>\n> +---\n> + arch/x86/Kconfig              |  1 +\n> + arch/x86/kernel/vmlinux.lds.S | 24 ++++++++++++------------\n> + 2 files changed, 13 insertions(+), 12 deletions(-)\n> +\n> +--- a/arch/x86/Kconfig\n> ++++ b/arch/x86/Kconfig\n> +@@ -184,6 +184,7 @@ config X86\n> + \tselect HAVE_FUNCTION_ERROR_INJECTION\n> + \tselect HAVE_KRETPROBES\n> + \tselect HAVE_KVM\n> ++\tselect HAVE_LD_DEAD_CODE_DATA_ELIMINATION\n> + \tselect HAVE_LIVEPATCH\t\t\tif X86_64\n> + \tselect HAVE_MEMBLOCK_NODE_MAP\n> + \tselect HAVE_MIXED_BREAKPOINTS_REGS\n> +--- a/arch/x86/kernel/vmlinux.lds.S\n> ++++ b/arch/x86/kernel/vmlinux.lds.S\n> +@@ -242,14 +242,14 @@ SECTIONS\n> + \t * See static_cpu_has() for an example.\n> + \t */\n> + \t.altinstr_aux : AT(ADDR(.altinstr_aux) - LOAD_OFFSET) {\n> +-\t\t*(.altinstr_aux)\n> ++\t\tKEEP(*(.altinstr_aux))\n> + \t}\n> +\n> + \tINIT_DATA_SECTION(16)\n> +\n> + \t.x86_cpu_dev.init : AT(ADDR(.x86_cpu_dev.init) - LOAD_OFFSET) {\n> + \t\t__x86_cpu_dev_start = .;\n> +-\t\t*(.x86_cpu_dev.init)\n> ++\t\tKEEP(*(.x86_cpu_dev.init))\n> + \t\t__x86_cpu_dev_end = .;\n> + \t}\n> +\n> +@@ -257,7 +257,7 @@ SECTIONS\n> + \t.x86_intel_mid_dev.init : AT(ADDR(.x86_intel_mid_dev.init) - \\\n> + \t\t\t\t\t\t\t\tLOAD_OFFSET)\n> {\n> + \t\t__x86_intel_mid_dev_start = .;\n> +-\t\t*(.x86_intel_mid_dev.init)\n> ++\t\tKEEP(*(.x86_intel_mid_dev.init))\n> + \t\t__x86_intel_mid_dev_end = .;\n> + \t}\n> + #endif\n> +@@ -271,7 +271,7 @@ SECTIONS\n> + \t. = ALIGN(8);\n> + \t.parainstructions : AT(ADDR(.parainstructions) - LOAD_OFFSET) {\n> + \t\t__parainstructions = .;\n> +-\t\t*(.parainstructions)\n> ++\t\tKEEP(*(.parainstructions))\n> + \t\t__parainstructions_end = .;\n> + \t}\n> +\n> +@@ -283,7 +283,7 @@ SECTIONS\n> + \t. = ALIGN(8);\n> + \t.altinstructions : AT(ADDR(.altinstructions) - LOAD_OFFSET) {\n> + \t\t__alt_instructions = .;\n> +-\t\t*(.altinstructions)\n> ++\t\tKEEP(*(.altinstructions))\n> + \t\t__alt_instructions_end = .;\n> + \t}\n> +\n> +@@ -293,7 +293,7 @@ SECTIONS\n> + \t * get the address and the length of them to patch the kernel safely.\n> + \t */\n> + \t.altinstr_replacement : AT(ADDR(.altinstr_replacement) -\n> LOAD_OFFSET) {\n> +-\t\t*(.altinstr_replacement)\n> ++\t\tKEEP(*(.altinstr_replacement))\n> + \t}\n> +\n> + \t/*\n> +@@ -304,14 +304,14 @@ SECTIONS\n> + \t */\n> + \t.iommu_table : AT(ADDR(.iommu_table) - LOAD_OFFSET) {\n> + \t\t__iommu_table = .;\n> +-\t\t*(.iommu_table)\n> ++\t\tKEEP(*(.iommu_table))\n> + \t\t__iommu_table_end = .;\n> + \t}\n> +\n> + \t. = ALIGN(8);\n> + \t.apicdrivers : AT(ADDR(.apicdrivers) - LOAD_OFFSET) {\n> + \t\t__apicdrivers = .;\n> +-\t\t*(.apicdrivers);\n> ++\t\tKEEP(*(.apicdrivers))\n> + \t\t__apicdrivers_end = .;\n> + \t}\n> +\n> +@@ -346,7 +346,7 @@ SECTIONS\n> + \t. = ALIGN(PAGE_SIZE);\n> + \t.smp_locks : AT(ADDR(.smp_locks) - LOAD_OFFSET) {\n> + \t\t__smp_locks = .;\n> +-\t\t*(.smp_locks)\n> ++\t\tKEEP(*(.smp_locks))\n> + \t\t. = ALIGN(PAGE_SIZE);\n> + \t\t__smp_locks_end = .;\n> + \t}\n> +@@ -380,8 +380,8 @@ SECTIONS\n> + \t. = ALIGN(PAGE_SIZE);\n> + \t.brk : AT(ADDR(.brk) - LOAD_OFFSET) {\n> + \t\t__brk_base = .;\n> +-\t\t. += 64 * 1024;\t\t/* 64k alignment slop space */\n> +-\t\t*(.brk_reservation)\t/* areas brk users have reserved */\n> ++\t\t. += 64 * 1024;\t\t\t/* 64k alignment slop space */\n> ++\t\tKEEP(*(.brk_reservation))\t/* areas brk users have\n> reserved */\n> + \t\t__brk_limit = .;\n> + \t}\n> +\n> +@@ -407,7 +407,7 @@ SECTIONS\n> + \t. = ALIGN(HPAGE_SIZE);\n> + \t.init.scratch : AT(ADDR(.init.scratch) - LOAD_OFFSET) {\n> + \t\t__init_scratch_begin = .;\n> +-\t\t*(.init.scratch)\n> ++\t\tKEEP(*(.init.scratch))\n> + \t\t. = ALIGN(HPAGE_SIZE);\n> + \t\t__init_scratch_end = .;\n> + \t}\n> --\n> 2.30.0\n> \n> \n> _______________________________________________\n> openwrt-devel mailing list\n> openwrt-devel at lists.openwrt.org\n> https://lists.openwrt.org/mailman/listinfo/openwrt-devel\n-------------- next part --------------\nA non-text attachment was scrubbed...\nName: openpgp-digital-signature.asc\nType: application/pgp-signature\nSize: 834 bytes\nDesc: not available\nURL: <http://lists.openwrt.org/pipermail/openwrt-devel/attachments/20210103/96afa6fd/attachment.sig>",
  "quoted_context_pairs": [
    {
      "quoted": "-----Original Message-----\nFrom: openwrt-devel [mailto:openwrt-devel-bounces at lists.openwrt.org]\nOn Behalf Of Rui Salvaterra\nSent: Sonntag, 3. Januar 2021 01:33\nTo: openwrt-devel at lists.openwrt.org\nCc: hauke at hauke-m.de; daniel at makrotopia.org; Rui Salvaterra\n<rsalvaterra at gmail.com>\nSubject: [PATCH] kernel/pending-5.4: enable DCDE for x86(-64)\n\nPort and adapt Nick Piggin's original patch [1]. This enables dead code and\ndata elimination at linking time (gc-sections) on x86(-64).",
      "response": "Shouldn't it be in target/linux/x86 then?\n\nBest",
      "line_index": 13
    }
  ],
  "mentioned_files": [],
  "mentioned_commits": [
    "0000000000",
    "20210103",
    "2937344",
    "3138048",
    "392ddd71ce",
    "96afa6fd"
  ],
  "keyword_matches": [],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "concurrency",
    "uci-config",
    "kernel-driver"
  ],
  "has_patch_subject": true,
  "has_keyword_match": false,
  "disposition": "primary"
}
```

## Sample 8

```json
{
  "source_file": "devel/2021-April.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-April.txt",
  "byte_offset": 54253,
  "mbox_from_line": "From oskari at lemmela.net  Mon Apr  5 18:53:14 2021",
  "message_id": "<20210405175317.648566-2-oskari@lemmela.net>",
  "in_reply_to": "<20210405175317.648566-1-oskari@lemmela.net>",
  "references": [
    "<20210405175317.648566-1-oskari@lemmela.net>"
  ],
  "from_addr": "oskari@lemmela.net",
  "from_name": "",
  "date_raw": "Mon, 05 Apr 2021 20:53:14 +0300",
  "date_iso": "2021-04-05T20:53:14+03:00",
  "subject": "[PATCH 1/4] mediatek: bpi-r64: use separate partition for emmc bootloader",
  "body_for_scoring": "emmc booloader is stored to separate partition.\nfip size is increased to 2MB.\n\nSigned-off-by: Oskari Lemmela <oskari at lemmela.net>\n---\n .../403-add-bananapi_bpi-r64_defconfigs.patch       |  8 ++++----\n target/linux/mediatek/image/mt7622.mk               | 13 +++++++------\n 2 files changed, 11 insertions(+), 10 deletions(-)\n\n[diff: package/boot/uboot-mediatek/patches/403-add-bananapi_bpi-r64_defconfigs.patch]\n[diff: target/linux/mediatek/image/mt7622.mk]\n[hunk: define Build/mt7622-gpt]\n-\t\t\t-t 0xef\t-N fip\t\t-r\t-p 1M at 2M \\\n+\t\t\t-t 0xef\t-N fip\t\t-r\t-p 2M at 2M \\\n-\t\t\t-t 0x2e -N production\t\t-p 216M at 40M \\\n+\t\t\t\t-N install\t-r\t-p 7M at 38M \\\n+\t\t\t-t 0x2e -N production\t\t-p 211M at 45M \\\n[hunk: define Device/bananapi_bpi-r64]\n-\t\t\t\t   pad-to 128k | mt7622-gpt emmc |\\\n-\t\t\t\t   pad-to 256k | bl2 emmc-2ddr |\\\n-\t\t\t\t   pad-to 1024k | bl31-uboot bananapi_bpi-r64-emmc |\\\n-\t\t\t\t   pad-to 40960k | append-image squashfs-sysupgrade.itb | gzip\n+\t\t\t\t   pad-to 38912k | mt7622-gpt emmc |\\",
  "body_no_diff": "emmc booloader is stored to separate partition.\nfip size is increased to 2MB.\n\nSigned-off-by: Oskari Lemmela <oskari at lemmela.net>\n---\n .../403-add-bananapi_bpi-r64_defconfigs.patch       |  8 ++++----\n target/linux/mediatek/image/mt7622.mk               | 13 +++++++------\n 2 files changed, 11 insertions(+), 10 deletions(-)\n\n[diff: package/boot/uboot-mediatek/patches/403-add-bananapi_bpi-r64_defconfigs.patch]\n[diff: target/linux/mediatek/image/mt7622.mk]\n[hunk: define Build/mt7622-gpt]\n-\t\t\t-t 0xef\t-N fip\t\t-r\t-p 1M at 2M \\\n+\t\t\t-t 0xef\t-N fip\t\t-r\t-p 2M at 2M \\\n-\t\t\t-t 0x2e -N production\t\t-p 216M at 40M \\\n+\t\t\t\t-N install\t-r\t-p 7M at 38M \\\n+\t\t\t-t 0x2e -N production\t\t-p 211M at 45M \\\n[hunk: define Device/bananapi_bpi-r64]\n-\t\t\t\t   pad-to 128k | mt7622-gpt emmc |\\\n-\t\t\t\t   pad-to 256k | bl2 emmc-2ddr |\\\n-\t\t\t\t   pad-to 1024k | bl31-uboot bananapi_bpi-r64-emmc |\\\n-\t\t\t\t   pad-to 40960k | append-image squashfs-sysupgrade.itb | gzip\n+\t\t\t\t   pad-to 38912k | mt7622-gpt emmc |\\",
  "quoted_context_pairs": [],
  "mentioned_files": [
    "package/boot/uboot-mediatek/patches/403-add-bananapi_bpi-r64_defconfigs.patch",
    "target/linux/mediatek/image/mt7622.mk"
  ],
  "mentioned_commits": [],
  "keyword_matches": [],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "uncategorized"
  ],
  "has_patch_subject": true,
  "has_keyword_match": false,
  "disposition": "primary"
}
```

## Sample 9

```json
{
  "source_file": "devel/2024-May.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2024-May.txt",
  "byte_offset": 511304,
  "mbox_from_line": "From tmn505 at terefe.re  Wed May 29 07:24:11 2024",
  "message_id": "<20240529143825.5472-9-tmn505@terefe.re>",
  "in_reply_to": "<20240529143825.5472-1-tmn505@terefe.re>",
  "references": [
    "<20240529143825.5472-1-tmn505@terefe.re>"
  ],
  "from_addr": "tmn505@terefe.re",
  "from_name": "",
  "date_raw": "Wed, 29 May 2024 16:24:11 +0200",
  "date_iso": "2024-05-29T16:24:11+02:00",
  "subject": "[PATCH v2 8/8] tegra: trimslice: adjust LED patch to upstream changes",
  "body_for_scoring": "From: Tomasz Maciej Nowak <tmn505 at gmail.com>\n\nLED subsystem has undergone changes how the function and color of LEDs\nshould be specified, so use that, while still keeping the old label.\n\nSigned-off-by: Tomasz Maciej Nowak <tmn505 at gmail.com>\n---\n ...enable-front-panel-leds-in-TrimSlice.patch | 28 ++++++++++++++-----\n 1 file changed, 21 insertions(+), 7 deletions(-)\n\n[diff: target/linux/tegra/patches-6.6/101-ARM-dtc-tegra-enable-front-panel-leds-in-TrimSlice.patch]\n-@@ -201,16 +201,17 @@\n+@@ -2,6 +2,7 @@\n+ /dts-v1/;\n+ \n+ #include <dt-bindings/input/input.h>\n-@@ -408,6 +409,20 @@\n+@@ -408,6 +410,26 @@",
  "body_no_diff": "From: Tomasz Maciej Nowak <tmn505 at gmail.com>\n\nLED subsystem has undergone changes how the function and color of LEDs\nshould be specified, so use that, while still keeping the old label.\n\nSigned-off-by: Tomasz Maciej Nowak <tmn505 at gmail.com>\n---\n ...enable-front-panel-leds-in-TrimSlice.patch | 28 ++++++++++++++-----\n 1 file changed, 21 insertions(+), 7 deletions(-)\n\n[diff: target/linux/tegra/patches-6.6/101-ARM-dtc-tegra-enable-front-panel-leds-in-TrimSlice.patch]\n-@@ -201,16 +201,17 @@\n+@@ -2,6 +2,7 @@\n+ /dts-v1/;\n+ \n+ #include <dt-bindings/input/input.h>\n-@@ -408,6 +409,20 @@\n+@@ -408,6 +410,26 @@",
  "quoted_context_pairs": [],
  "mentioned_files": [
    "target/linux/tegra/patches-6.6/101-ARM-dtc-tegra-enable-front-panel-leds-in-TrimSlice.patch"
  ],
  "mentioned_commits": [],
  "keyword_matches": [
    "\\[PATCH\\s+v[2-9]",
    "should\\s+(?:use|be|have|call)"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": false,
    "has_patch_revision": false
  },
  "categories": [
    "kernel-driver",
    "patch-maintenance"
  ],
  "has_patch_subject": true,
  "has_keyword_match": true,
  "disposition": "primary"
}
```

## Sample 10

```json
{
  "source_file": "bugs/2021-November.txt",
  "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-November.txt",
  "byte_offset": 287702,
  "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Sat Nov 27 12:44:13 2021",
  "message_id": "<mailman.17884.1638045856.1923571.openwrt-bugs@lists.openwrt.org>",
  "in_reply_to": "<FS4160@bugs.openwrt.org>",
  "references": [
    "<FS4160@bugs.openwrt.org>"
  ],
  "from_addr": "openwrt-bugs@lists.openwrt.org",
  "from_name": "",
  "date_raw": "Sat, 27 Nov 2021 20:44:13 +0000",
  "date_iso": "2021-11-27T20:44:13+00:00",
  "subject": "[FS#4160] Leaking host IP addresses to unrelated dnsmasq instances",
  "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#4160 - Leaking host IP addresses to unrelated dnsmasq instances\nUser who did this - Robert Klauco (sanchosk)\n\n----------\nThis is the pull request\nhttps://github.com/openwrt/openwrt/pull/4798\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4160#comment10350\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#4160 - Leaking host IP addresses to unrelated dnsmasq instances\nUser who did this - Robert Klauco (sanchosk)\n\n----------\nThis is the pull request\nhttps://github.com/openwrt/openwrt/pull/4798\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4160#comment10350\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
  "quoted_context_pairs": [],
  "mentioned_files": [],
  "mentioned_commits": [],
  "keyword_matches": [
    "bug",
    "do\\s+not|don't"
  ],
  "structural_signals": {
    "has_compiler_error": false,
    "has_stack_trace": false,
    "has_shell_error": false,
    "has_build_error": false,
    "has_code_block": false,
    "has_reference_urls": true,
    "has_patch_revision": false
  },
  "categories": [
    "uncategorized"
  ],
  "has_patch_subject": false,
  "has_keyword_match": true,
  "disposition": "primary"
}
```
