# QA Samples

Randomly selected records for manual inspection.

## Sample 1

```json
{
  "thread_id": "<20210320192839.3962480-1-hauke@hauke-m.de>",
  "subject": "[PATCH uhttpd] client: Always close connection with request body in case of error",
  "messages": [
    {
      "source_file": "devel/2021-March.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-March.txt",
      "byte_offset": 1319889,
      "mbox_from_line": "From hauke at hauke-m.de  Sat Mar 20 19:28:39 2021",
      "message_id": "<20210320192839.3962480-1-hauke@hauke-m.de>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "hauke@hauke-m.de",
      "from_name": "",
      "date_raw": "Sat, 20 Mar 2021 20:28:39 +0100",
      "date_iso": "2021-03-20T20:28:39+01:00",
      "subject": "[PATCH uhttpd] client: Always close connection with request body in case of error",
      "body_for_scoring": "When we run into an error like a 404 Not Found the request body is not\nread and will be parsed as part of the next request. The next Request\nwill then fail because there is unexpected data in it.\nWhen we run into such a problem with a request body close return an\nerror and close the connection. This should be easier than trying to\nrecover the state.\n\nWe saw this problem when /ubus/ was not installed, but the browser tried\nto access it. Then uhttpd returned a 404, but the next request done in\nthis connection also failed with a HTTP 400, bad request.\n\nSigned-off-by: Hauke Mehrtens <hauke at hauke-m.de>\n---\n client.c | 6 ++++++\n 1 file changed, 6 insertions(+)\n\n[diff: client.c]\n[hunk: void uh_request_done(struct client *cl)]\n+\tstruct http_request *r = &cl->request;\n[hunk: uh_client_error(struct client *cl, int code, const char *summary, const char *fm]\n+\tif (r->transfer_chunked || r->content_length > 0) {\n+\t\tcl->state = CLIENT_STATE_CLOSE;\n+\t\tcl->request.connection_close = true;\n+\t}",
      "body_no_diff": "When we run into an error like a 404 Not Found the request body is not\nread and will be parsed as part of the next request. The next Request\nwill then fail because there is unexpected data in it.\nWhen we run into such a problem with a request body close return an\nerror and close the connection. This should be easier than trying to\nrecover the state.\n\nWe saw this problem when /ubus/ was not installed, but the browser tried\nto access it. Then uhttpd returned a 404, but the next request done in\nthis connection also failed with a HTTP 400, bad request.\n\nSigned-off-by: Hauke Mehrtens <hauke at hauke-m.de>\n---\n client.c | 6 ++++++\n 1 file changed, 6 insertions(+)\n\n[diff: client.c]\n[hunk: void uh_request_done(struct client *cl)]\n+\tstruct http_request *r = &cl->request;\n[hunk: uh_client_error(struct client *cl, int code, const char *summary, const char *fm]\n+\tif (r->transfer_chunked || r->content_length > 0) {\n+\t\tcl->state = CLIENT_STATE_CLOSE;\n+\t\tcl->request.connection_close = true;\n+\t}",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "client.c"
      ],
      "mentioned_commits": [],
      "keyword_matches": [
        "const",
        "fail(?:ed|ure|ing)?",
        "should\\s+(?:use|be|have|call)",
        "ubus",
        "uhttpd"
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
        "ubus-ipc",
        "luci-frontend"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    },
    {
      "source_file": "devel/2021-March.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-March.txt",
      "byte_offset": 1321499,
      "mbox_from_line": "From hauke at hauke-m.de  Sat Mar 20 19:37:38 2021",
      "message_id": "<5bdc32ac-525b-b708-5524-f73eb357d039@hauke-m.de>",
      "in_reply_to": "<20210320192839.3962480-1-hauke@hauke-m.de>",
      "references": [
        "<20210320192839.3962480-1-hauke@hauke-m.de>"
      ],
      "from_addr": "hauke@hauke-m.de",
      "from_name": "",
      "date_raw": "Sat, 20 Mar 2021 20:37:38 +0100",
      "date_iso": "2021-03-20T20:37:38+01:00",
      "subject": "[PATCH uhttpd] client: Always close connection with request body in case of error",
      "body_for_scoring": "On 3/20/21 8:28 PM, Hauke Mehrtens wrote:\n\nThis should fix the following bug report:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3378",
      "body_no_diff": "On 3/20/21 8:28 PM, Hauke Mehrtens wrote:\n> When we run into an error like a 404 Not Found the request body is not\n> read and will be parsed as part of the next request. The next Request\n> will then fail because there is unexpected data in it.\n> When we run into such a problem with a request body close return an\n> error and close the connection. This should be easier than trying to\n> recover the state.\n> \n> We saw this problem when /ubus/ was not installed, but the browser tried\n> to access it. Then uhttpd returned a 404, but the next request done in\n> this connection also failed with a HTTP 400, bad request.\n> \n> Signed-off-by: Hauke Mehrtens <hauke at hauke-m.de>\n\nThis should fix the following bug report:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3378\n\n> ---\n>   client.c | 6 ++++++\n>   1 file changed, 6 insertions(+)\n> \n> diff --git a/client.c b/client.c\n> index 6233d01..1d337f3 100644\n> --- a/client.c\n> +++ b/client.c\n> @@ -138,6 +138,7 @@ void uh_request_done(struct client *cl)\n>   void __printf(4, 5)\n>   uh_client_error(struct client *cl, int code, const char *summary, const char *fmt, ...)\n>   {\n> +\tstruct http_request *r = &cl->request;\n>   \tva_list arg;\n>   \n>   \tuh_http_header(cl, code, summary);\n> @@ -151,6 +152,11 @@ uh_client_error(struct client *cl, int code, const char *summary, const char *fm\n>   \t\tva_end(arg);\n>   \t}\n>   \n> +\tif (r->transfer_chunked || r->content_length > 0) {\n> +\t\tcl->state = CLIENT_STATE_CLOSE;\n> +\t\tcl->request.connection_close = true;\n> +\t}\n> +\n>   \tuh_request_done(cl);\n>   }\n>   \n>",
      "quoted_context_pairs": [
        {
          "quoted": "When we run into an error like a 404 Not Found the request body is not\nread and will be parsed as part of the next request. The next Request\nwill then fail because there is unexpected data in it.\nWhen we run into such a problem with a request body close return an\nerror and close the connection. This should be easier than trying to\nrecover the state.\n\nWe saw this problem when /ubus/ was not installed, but the browser tried\nto access it. Then uhttpd returned a 404, but the next request done in\nthis connection also failed with a HTTP 400, bad request.\n\nSigned-off-by: Hauke Mehrtens <hauke at hauke-m.de>",
          "response": "This should fix the following bug report:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3378",
          "line_index": 13
        }
      ],
      "mentioned_files": [],
      "mentioned_commits": [
        "1d337f3",
        "6233d01"
      ],
      "keyword_matches": [
        "bug",
        "uhttpd"
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
        "c-language",
        "ubus-ipc",
        "luci-frontend"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 2,
  "author_count": 1,
  "date_range": [
    "2021-03-20T20:28:39+01:00",
    "2021-03-20T20:37:38+01:00"
  ],
  "all_mentioned_files": [
    "client.c"
  ],
  "all_mentioned_commits": [
    "1d337f3",
    "6233d01"
  ],
  "categories": [
    "c-language",
    "ubus-ipc",
    "luci-frontend"
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
  "source_refs": [
    {
      "source_file": "devel/2021-March.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-March.txt",
      "message_id": "<20210320192839.3962480-1-hauke@hauke-m.de>",
      "byte_offset": 1319889
    },
    {
      "source_file": "devel/2021-March.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-March.txt",
      "message_id": "<5bdc32ac-525b-b708-5524-f73eb357d039@hauke-m.de>",
      "byte_offset": 1321499
    }
  ],
  "score": 0.85
}
```

## Sample 2

```json
{
  "thread_id": "<20210803033558.23441-1-ianchang@ieiworld.com>",
  "subject": "[PATCH v6 2/3] mvebu: add dts files for iEi Puzzle-M901/Puzzle-M902",
  "messages": [
    {
      "source_file": "devel/2021-August.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-August.txt",
      "byte_offset": 16105,
      "mbox_from_line": "From eveans2002 at gmail.com  Mon Aug  2 20:35:58 2021",
      "message_id": "<20210803033558.23441-1-ianchang@ieiworld.com>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "eveans2002@gmail.com",
      "from_name": "",
      "date_raw": "Tue, 03 Aug 2021 11:35:58 +0800",
      "date_iso": "2021-08-03T11:35:58+08:00",
      "subject": "[PATCH v6 2/3] mvebu: add dts files for iEi Puzzle-M901/Puzzle-M902",
      "body_for_scoring": "From: Ian Chang <ianchang at ieiworld.com>\n\nSigned-off-by: Ian Chang <ianchang at ieiworld.com>\n---\n .../boot/dts/marvell/cn9131-puzzle-m901.dts   | 319 ++++++++++++\n .../boot/dts/marvell/cn9132-puzzle-m902.dts   | 481 ++++++++++++++++++\n 2 files changed, 800 insertions(+)\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n\n[diff: target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts]\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9131-DB board.\n[diff: target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts]\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9132-DB board.",
      "body_no_diff": "From: Ian Chang <ianchang at ieiworld.com>\n\nSigned-off-by: Ian Chang <ianchang at ieiworld.com>\n---\n .../boot/dts/marvell/cn9131-puzzle-m901.dts   | 319 ++++++++++++\n .../boot/dts/marvell/cn9132-puzzle-m902.dts   | 481 ++++++++++++++++++\n 2 files changed, 800 insertions(+)\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n\n[diff: target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts]\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9131-DB board.\n[diff: target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts]\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9132-DB board.",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts",
        "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts"
      ],
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
        "kernel-driver"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    },
    {
      "source_file": "devel/2021-August.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-August.txt",
      "byte_offset": 248068,
      "mbox_from_line": "From daniel at makrotopia.org  Sun Aug  8 08:30:12 2021",
      "message_id": "<YQ/4hEE7D6i2eZrc@makrotopia.org>",
      "in_reply_to": "<20210803033558.23441-1-ianchang@ieiworld.com>",
      "references": [
        "<20210803033558.23441-1-ianchang@ieiworld.com>"
      ],
      "from_addr": "daniel@makrotopia.org",
      "from_name": "",
      "date_raw": "Sun, 08 Aug 2021 16:30:12 +0100",
      "date_iso": "2021-08-08T16:30:12+01:00",
      "subject": "[PATCH v6 2/3] mvebu: add dts files for iEi Puzzle-M901/Puzzle-M902",
      "body_for_scoring": "On Tue, Aug 03, 2021 at 11:35:58AM +0800, eveans2002 at gmail.com wrote:\n\nIndentation here is wrong and missing one tab. This has already been\na problem in the previous iteration of this series.",
      "body_no_diff": "On Tue, Aug 03, 2021 at 11:35:58AM +0800, eveans2002 at gmail.com wrote:\n> From: Ian Chang <ianchang at ieiworld.com>\n> \n> Signed-off-by: Ian Chang <ianchang at ieiworld.com>\n> ---\n>  .../boot/dts/marvell/cn9131-puzzle-m901.dts   | 319 ++++++++++++\n>  .../boot/dts/marvell/cn9132-puzzle-m902.dts   | 481 ++++++++++++++++++\n>  2 files changed, 800 insertions(+)\n>  create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n>  create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n> \n> diff --git a/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n> new file mode 100644\n> index 0000000000..58e749490a\n> --- /dev/null\n> +++ b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n> @@ -0,0 +1,319 @@\n> +// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n> +/*\n> + * Copyright (C) 2019 Marvell International Ltd.\n> + *\n> + * Device tree for the CN9131-DB board.\n> + */\n> +\n> +#include \"cn9130.dtsi\"\n> +\n> +#include <dt-bindings/gpio/gpio.h>\n> +\n> +/ {\n> +\tmodel = \"iEi Puzzle-M901\";\n> +\tcompatible = \"iei,puzzle-m901\",\n> +\t\t     \"marvell,armada-ap807-quad\", \"marvell,armada-ap807\";\n> +\n> +\tchosen {\n> +\t\tstdout-path = \"serial0:115200n8\";\n> +\t};\n> +\n> +\taliases {\n> +\t\ti2c0 = &cp1_i2c0;\n> +\t\ti2c1 = &cp0_i2c0;\n> +\t\tethernet0 = &cp0_eth0;\n> +\t\tethernet1 = &cp0_eth1;\n> +\t\tethernet2 = &cp0_eth2;\n> +\t\tethernet3 = &cp1_eth0;\n> +\t\tethernet4 = &cp1_eth1;\n> +\t\tethernet5 = &cp1_eth2;\n> +\t\tgpio1 = &cp0_gpio1;\n> +\t\tgpio2 = &cp0_gpio2;\n> +\t\tgpio3 = &cp1_gpio1;\n> +\t\tgpio4 = &cp1_gpio2;\n> +\t};\n> +\n> +\tmemory at 00000000 {\n> +\t\tdevice_type = \"memory\";\n> +\t\treg = <0x0 0x0 0x0 0x80000000>;\n> +\t};\n> +};\n> +\n> +&uart0 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_uart0 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* on-board eMMC - U9 */\n> +&ap_sdhci0 {\n> +\tpinctrl-names = \"default\";\n> +\tbus-width = <8>;\n> +\tstatus = \"okay\";\n> +\tmmc-ddr-1_8v;\n> +\tmmc-hs400-1_8v;\n> +};\n> +\n> +&cp0_crypto {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_xmdio {\n> +\tstatus = \"okay\";\n> +\tcp0_nbaset_phy0: ethernet-phy at 0 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <2>;\n> +\t};\n> +\tcp0_nbaset_phy1: ethernet-phy at 1 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <0>;\n> +\t};\n> +\tcp0_nbaset_phy2: ethernet-phy at 2 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <8>;\n> +\t};\n> +};\n> +\n> +&cp0_ethernet {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* SLM-1521-V2, CON9 */\n> +&cp0_eth0 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp0_comphy2 0>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_eth1 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp0_comphy4 1>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_eth2 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp0_comphy5 2>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_gpio1 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_gpio2 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_i2c0 {\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp0_i2c0_pins>;\n> +\tstatus = \"okay\";\n> +\tclock-frequency = <100000>;\n> +\trtc at 32 {\n> +\t\tcompatible = \"epson,rx8130\";\n> +\t\treg = <0x32>;\n> +\t\twakeup-source;\n> +\t};\n> +};\n> +\n> +/* SLM-1521-V2, CON6 */\n> +&cp0_pcie0 {\n> +\tstatus = \"okay\";\n> +\tnum-lanes = <2>;\n> +\tnum-viewport = <8>;\n> +\tphys = <&cp0_comphy0 0>, <&cp0_comphy1 0>;\n> +};\n> +\n> +/* U55 */\n> +&cp0_spi1 {\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp0_spi0_pins>;\n> +\treg = <0x700680 0x50>,          /* control */\n> +\t      <0x2000000 0x1000000>;    /* CS0 */\n> +\tstatus = \"okay\";\n> +\tspi-flash at 0 {\n> +\t\t#address-cells = <0x1>;\n> +\t\t#size-cells = <0x1>;\n> +\t\tcompatible = \"jedec,spi-nor\";\n> +\t\treg = <0x0>;\n> +\t\tspi-max-frequency = <40000000>;\n> +\t\tpartitions {\n> +\t\t\tcompatible = \"fixed-partitions\";\n> +\t\t\t#address-cells = <1>;\n> +\t\t\t#size-cells = <1>;\n> +\t\t\tpartition at 0 {\n> +\t\t\t\tlabel = \"U-Boot\";\n> +\t\t\t\treg = <0x0 0x1f0000>;\n> +\t\t\t};\n> +\t\t\tpartition at 1f0000 {\n> +\t\t\t\tlabel = \"U-Boot ENV Factory\";\n> +\t\t\t\treg = <0x1f0000 0x10000>;\n> +\t\t\t};\n> +\t\t\tpartition at 200000 {\n> +\t\t\t\tlabel = \"Reserved\";\n> +\t\t\t\treg = <0x200000 0x1f0000>;\n> +\t\t\t};\n> +\t\t\tpartition at 3f0000 {\n> +\t\t\t\tlabel = \"U-Boot ENV\";\n> +\t\t\t\treg = <0x3f0000 0x10000>;\n> +\t\t\t};\n> +\t\t};\n> +\t};\n> +};\n> +\n> +&cp0_syscon0 {\n> +\tcp0_pinctrl: pinctrl {\n> +\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n> +\t\tcp0_i2c0_pins: cp0-i2c-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n> +\t\t\tmarvell,function = \"i2c0\";\n> +\t\t};\n> +\t\tcp0_i2c1_pins: cp0-i2c-pins-1 {\n> +\t\t\tmarvell,pins = \"mpp35\", \"mpp36\";\n> +\t\t\tmarvell,function = \"i2c1\";\n> +\t\t};\n> +\t\tcp0_ge1_rgmii_pins: cp0-ge-rgmii-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp0\", \"mpp1\", \"mpp2\",\n> +\t\t\t\t       \"mpp3\", \"mpp4\", \"mpp5\",\n> +\t\t\t\t       \"mpp6\", \"mpp7\", \"mpp8\",\n> +\t\t\t\t       \"mpp9\", \"mpp10\", \"mpp11\";\n> +\t\t\tmarvell,function = \"ge0\";\n> +\t\t};\n> +\t\tcp0_ge2_rgmii_pins: cp0-ge-rgmii-pins-1 {\n> +\t\t\tmarvell,pins = \"mpp44\", \"mpp45\", \"mpp46\",\n> +\t\t\t\t       \"mpp47\", \"mpp48\", \"mpp49\",\n> +\t\t\t\t       \"mpp50\", \"mpp51\", \"mpp52\",\n> +\t\t\t\t       \"mpp53\", \"mpp54\", \"mpp55\";\n> +\t\t\tmarvell,function = \"ge1\";\n> +\t\t};\n> +\t\tcp0_spi0_pins: cp0-spi-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n> +\t\t\tmarvell,function = \"spi1\";\n> +\t\t};\n> +\t};\n> +};\n> +\n> +/*\n> + * Instantiate the first connected CP115\n> + */\n> +\n> +#define CP11X_NAME\t\tcp1\n> +#define CP11X_BASE\t\tf6000000\n> +#define CP11X_PCIEx_MEM_BASE(iface) (0xe2000000 + (iface * 0x1000000))\n> +#define CP11X_PCIEx_MEM_SIZE(iface) 0xf00000\n> +#define CP11X_PCIE0_BASE\tf6600000\n> +#define CP11X_PCIE1_BASE\tf6620000\n> +#define CP11X_PCIE2_BASE\tf6640000\n> +\n> +#include \"armada-cp115.dtsi\"\n> +\n> +#undef CP11X_NAME\n> +#undef CP11X_BASE\n> +#undef CP11X_PCIEx_MEM_BASE\n> +#undef CP11X_PCIEx_MEM_SIZE\n> +#undef CP11X_PCIE0_BASE\n> +#undef CP11X_PCIE1_BASE\n> +#undef CP11X_PCIE2_BASE\n> +\n> +&cp1_crypto {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_xmdio {\n> +\tstatus = \"okay\";\n> +\tcp1_nbaset_phy0: ethernet-phy at 3 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <2>;\n> +\t};\n> +\tcp1_nbaset_phy1: ethernet-phy at 4 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <0>;\n> +\t};\n> +\tcp1_nbaset_phy2: ethernet-phy at 5 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <8>;\n> +\t};\n> +};\n> +\n> +&cp1_ethernet {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* CON50 */\n> +&cp1_eth0 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp1_comphy2 0>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_eth1 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp1_comphy4 1>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_eth2 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp1_comphy5 2>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_sata0 {\n> +\tstatus = \"okay\";\n> +\tsata-port at 1 {\n> +\t\tstatus = \"okay\";\n> +\t\tphys = <&cp1_comphy0 1>;\n> +\t};\n> +};\n> +\n> +&cp1_gpio1 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_gpio2 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_i2c0 {\n> +\tstatus = \"okay\";\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp1_i2c0_pins>;\n> +\tclock-frequency = <100000>;\n> +};\n> +\n> +&cp1_syscon0 {\n> +\tcp1_pinctrl: pinctrl {\n> +\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n> +\t\tcp1_i2c0_pins: cp1-i2c-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n> +\t\t\tmarvell,function = \"i2c0\";\n> +\t\t};\n> +\t\tcp1_spi0_pins: cp1-spi-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n> +\t\t\tmarvell,function = \"spi1\";\n> +\t\t};\n> +\t\tcp1_xhci0_vbus_pins: cp1-xhci0-vbus-pins {\n> +\t\t\tmarvell,pins = \"mpp3\";\n> +\t\t\tmarvell,function = \"gpio\";\n> +\t\t};\n> +\t\tcp1_sfp_pins: sfp-pins {\n> +\t\t\tmarvell,pins = \"mpp8\", \"mpp9\", \"mpp10\", \"mpp11\";\n> +\t\t\tmarvell,function = \"gpio\";\n> +\t\t};\n> +\t};\n> +};\n> +\n> +&cp1_usb3_1 {\n> +\tstatus = \"okay\";\n> +\tphys = <&cp1_comphy3 1>;\n> +\tphy-names = \"usb\";\n> +};\n> diff --git a/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n> new file mode 100644\n> index 0000000000..0d27cc356e\n> --- /dev/null\n> +++ b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n> @@ -0,0 +1,481 @@\n> +// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n> +/*\n> + * Copyright (C) 2019 Marvell International Ltd.\n> + *\n> + * Device tree for the CN9132-DB board.\n> + */\n> +\n> +#include \"cn9130.dtsi\"\n> +\n> +#include <dt-bindings/gpio/gpio.h>\n> +\n> +/ {\n> +\tmodel = \"iEi Puzzle-M902\";\n> +\tcompatible = \"iei,puzzle-m902\",\n> +\t\t     \"marvell,armada-ap807-quad\", \"marvell,armada-ap807\";\n> +\n> +\tchosen {\n> +\t\tstdout-path = \"serial0:115200n8\";\n> +\t};\n> +\n> +\taliases {\n> +\t\ti2c0 = &cp1_i2c0;\n> +\t\ti2c1 = &cp0_i2c0;\n> +\t\tgpio1 = &cp0_gpio1;\n> +\t\tgpio2 = &cp0_gpio2;\n> +\t\tgpio3 = &cp1_gpio1;\n> +\t\tgpio4 = &cp1_gpio2;\n> +\t\tgpio5 = &cp2_gpio1;\n> +\t\tgpio6 = &cp2_gpio2;\n> +\t\tethernet0 = &cp0_eth0;\n> +\t\tethernet1 = &cp0_eth1;\n> +\t\tethernet2 = &cp0_eth2;\n> +\t\tethernet3 = &cp1_eth0;\n> +\t\tethernet4 = &cp1_eth1;\n> +\t\tethernet5 = &cp1_eth2;\n> +\t\tethernet6 = &cp2_eth0;\n> +\t\tethernet7 = &cp2_eth1;\n> +\t\tethernet8 = &cp2_eth2;\n> +\t\tspi1 = &cp0_spi0;\n> +\t\tspi2 = &cp0_spi1;\n> +\t\tserial1 = &cp0_uart0;\n> +\t};\n> +\n> +\tmemory at 00000000 {\n> +\t\tdevice_type = \"memory\";\n> +\t\treg = <0x0 0x0 0x0 0x80000000>;\n> +\t};\n> +\n> +\tcp2_reg_usb3_vbus0: cp2_usb3_vbus at 0 {\n> +\t\tcompatible = \"regulator-fixed\";\n> +\t\tregulator-name = \"cp2-xhci0-vbus\";\n> +\t\tregulator-min-microvolt = <5000000>;\n> +\t\tregulator-max-microvolt = <5000000>;\n> +\t\tenable-active-high;\n> +\t\tgpio = <&cp2_gpio1 2 GPIO_ACTIVE_HIGH>;\n> +\t};\n> +\n> +\tcp2_usb3_0_phy0: cp2_usb3_phy0 {\n> +\t\tcompatible = \"usb-nop-xceiv\";\n> +\t\tvcc-supply = <&cp2_reg_usb3_vbus0>;\n> +\t};\n> +\n> +\tcp2_reg_usb3_vbus1: cp2_usb3_vbus at 1 {\n> +\t\tcompatible = \"regulator-fixed\";\n> +\t\tregulator-name = \"cp2-xhci1-vbus\";\n> +\t\tregulator-min-microvolt = <5000000>;\n> +\t\tregulator-max-microvolt = <5000000>;\n> +\t\tenable-active-high;\n> +\t\tgpio = <&cp2_gpio1 3 GPIO_ACTIVE_HIGH>;\n> +\t};\n> +\n> +\tcp2_usb3_0_phy1: cp2_usb3_phy1 {\n> +\t\tcompatible = \"usb-nop-xceiv\";\n> +\t\tvcc-supply = <&cp2_reg_usb3_vbus1>;\n> +\t};\n> +\n> +\tcp2_sfp_eth0: sfp-eth0 {\n> +\t\tcompatible = \"sff,sfp\";\n> +\t\ti2c-bus = <&cp2_sfpp0_i2c>;\n> +\t\tlos-gpio = <&cp2_module_expander1 11 GPIO_ACTIVE_HIGH>;\n> +\t\tmod-def0-gpio = <&cp2_module_expander1 10 GPIO_ACTIVE_LOW>;\n> +\t\ttx-disable-gpio = <&cp2_module_expander1 9 GPIO_ACTIVE_HIGH>;\n> +\t\ttx-fault-gpio = <&cp2_module_expander1 8 GPIO_ACTIVE_HIGH>;\n> +\t\tstatus = \"disabled\";\n> +\t};\n> +};\n> +\n> +&uart0 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_uart0 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* on-board eMMC - U9 */\n> +&ap_sdhci0 {\n> +\tpinctrl-names = \"default\";\n> +\tbus-width = <8>;\n> +\tstatus = \"okay\";\n> +\tmmc-ddr-1_8v;\n> +\tmmc-hs400-1_8v;\n> +};\n> +\n> +&cp0_crypto {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_xmdio {\n> +\tstatus = \"okay\";\n> +\tcp0_nbaset_phy0: ethernet-phy at 0 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <2>;\n> +\t};\n> +\tcp0_nbaset_phy1: ethernet-phy at 1 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <0>;\n> +\t};\n> +\tcp0_nbaset_phy2: ethernet-phy at 2 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <8>;\n> +\t};\n> +};\n> +\n> +&cp0_ethernet {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* SLM-1521-V2, CON9 */\n> +&cp0_eth0 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"10gbase-kr\";\n> +\tphys = <&cp0_comphy2 0>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_eth1 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp0_comphy4 1>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_eth2 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp0_comphy1 2>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp0_gpio1 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_gpio2 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp0_i2c0 {\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp0_i2c0_pins>;\n> +\tstatus = \"okay\";\n> +\tclock-frequency = <100000>;\n> +\trtc at 32 {\n> +\t\tcompatible = \"epson,rx8130\";\n> +\t\treg = <0x32>;\n> +\t\twakeup-source;\n> +\t};\n> +};\n> +\n> +&cp0_i2c1 {\n> +\tclock-frequency = <100000>;\n> +};\n> +\n> +/* SLM-1521-V2, CON6 */\n> +&cp0_sata0 {\n> +\tstatus = \"okay\";\n> +\tsata-port at 1 {\n> +\t\tstatus = \"okay\";\n> +\t\tphys = <&cp0_comphy0 1>;\n> +\t};\n> +};\n> +\n> +&cp0_pcie2 {\n> +\tstatus = \"okay\";\n> +\tnum-lanes = <1>;\n> +\tnum-viewport = <8>;\n> +\tphys = <&cp0_comphy5 2>;\n> +};\n> +\n> +/* U55 */\n> +&cp0_spi1 {\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp0_spi0_pins>;\n> +\treg = <0x700680 0x50>,          /* control */\n> +\t      <0x2000000 0x1000000>;    /* CS0 */\n> +\tstatus = \"okay\";\n> +\tspi-flash at 0 {\n> +\t\t#address-cells = <0x1>;\n> +\t\t#size-cells = <0x1>;\n> +\t\tcompatible = \"jedec,spi-nor\";\n> +\t\treg = <0x0>;\n> +\t\tspi-max-frequency = <40000000>;\n> +\t\tpartitions {\n> +\t\t\tcompatible = \"fixed-partitions\";\n> +\t\t\t#address-cells = <1>;\n> +\t\t\t#size-cells = <1>;\n> +\t\t\tpartition at 0 {\n> +\t\t\t\tlabel = \"U-Boot\";\n> +\t\t\t\treg = <0x0 0x1f0000>;\n> +\t\t\t};\n> +\t\tpartition at 1f0000 {\n\nIndentation here is wrong and missing one tab. This has already been\na problem in the previous iteration of this series.\n\n\n> +\t\t\t\tlabel = \"U-Boot ENV Factory\";\n> +\t\t\t\treg = <0x1f0000 0x10000>;\n> +\t\t\t};\n> +\t\tpartition at 200000 {\n> +\t\t\t\tlabel = \"Reserved\";\n> +\t\t\t\treg = <0x200000 0x1f0000>;\n> +\t\t\t};\n> +\t\tpartition at 3f0000 {\n> +\t\t\t\tlabel = \"U-Boot ENV\";\n> +\t\t\t\treg = <0x3f0000 0x10000>;\n> +\t\t\t};\n> +\t\t};\n> +\t};\n> +};\n> +\n> +&cp0_syscon0 {\n> +\tcp0_pinctrl: pinctrl {\n> +\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n> +\t\tcp0_i2c0_pins: cp0-i2c-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n> +\t\t\tmarvell,function = \"i2c0\";\n> +\t\t};\n> +\t\tcp0_i2c1_pins: cp0-i2c-pins-1 {\n> +\t\t\tmarvell,pins = \"mpp35\", \"mpp36\";\n> +\t\t\tmarvell,function = \"i2c1\";\n> +\t\t};\n> +\t\tcp0_ge1_rgmii_pins: cp0-ge-rgmii-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp0\", \"mpp1\", \"mpp2\",\n> +\t\t\t\t       \"mpp3\", \"mpp4\", \"mpp5\",\n> +\t\t\t\t       \"mpp6\", \"mpp7\", \"mpp8\",\n> +\t\t\t\t       \"mpp9\", \"mpp10\", \"mpp11\";\n> +\t\t\tmarvell,function = \"ge0\";\n> +\t\t};\n> +\t\tcp0_ge2_rgmii_pins: cp0-ge-rgmii-pins-1 {\n> +\t\t\tmarvell,pins = \"mpp44\", \"mpp45\", \"mpp46\",\n> +\t\t\t\t       \"mpp47\", \"mpp48\", \"mpp49\",\n> +\t\t\t\t       \"mpp50\", \"mpp51\", \"mpp52\",\n> +\t\t\t\t       \"mpp53\", \"mpp54\", \"mpp55\";\n> +\t\t\tmarvell,function = \"ge1\";\n> +\t\t};\n> +\t\tcp0_spi0_pins: cp0-spi-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n> +\t\t\tmarvell,function = \"spi1\";\n> +\t\t};\n> +\t};\n> +};\n> +\n> +&cp0_usb3_1 {\n> +\tstatus = \"okay\";\n> +\tphys = <&cp0_comphy3 1>;\n> +\tphy-names = \"usb\";\n> +};\n> +\n> +/*\n> + * Instantiate the first connected CP115\n> + */\n> +\n> +#define CP11X_NAME\t\tcp1\n> +#define CP11X_BASE\t\tf4000000\n> +#define CP11X_PCIEx_MEM_BASE(iface) (0xe2000000 + (iface * 0x1000000))\n> +#define CP11X_PCIEx_MEM_SIZE(iface) 0xf00000\n> +#define CP11X_PCIE0_BASE\tf4600000\n> +#define CP11X_PCIE1_BASE\tf4620000\n> +#define CP11X_PCIE2_BASE\tf4640000\n> +\n> +#include \"armada-cp115.dtsi\"\n> +\n> +#undef CP11X_NAME\n> +#undef CP11X_BASE\n> +#undef CP11X_PCIEx_MEM_BASE\n> +#undef CP11X_PCIEx_MEM_SIZE\n> +#undef CP11X_PCIE0_BASE\n> +#undef CP11X_PCIE1_BASE\n> +#undef CP11X_PCIE2_BASE\n> +\n> +&cp1_crypto {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_xmdio {\n> +\tstatus = \"okay\";\n> +\tcp1_nbaset_phy0: ethernet-phy at 3 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <2>;\n> +\t};\n> +\tcp1_nbaset_phy1: ethernet-phy at 4 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <0>;\n> +\t};\n> +\tcp1_nbaset_phy2: ethernet-phy at 5 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <8>;\n> +\t};\n> +};\n> +\n> +&cp1_ethernet {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +/* CON50 */\n> +&cp1_eth0 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"10gbase-kr\";\n> +\tphys = <&cp1_comphy2 0>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_eth1 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp1_comphy4 1>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_eth2 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp1_comphy1 2>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp1_gpio1 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_gpio2 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp1_i2c0 {\n> +\tstatus = \"okay\";\n> +\tpinctrl-names = \"default\";\n> +\tpinctrl-0 = <&cp1_i2c0_pins>;\n> +\tclock-frequency = <100000>;\n> +};\n> +\n> +&cp1_syscon0 {\n> +\tcp1_pinctrl: pinctrl {\n> +\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n> +\t\tcp1_i2c0_pins: cp1-i2c-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n> +\t\t\tmarvell,function = \"i2c0\";\n> +\t\t};\n> +\t\tcp1_spi0_pins: cp1-spi-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n> +\t\t\tmarvell,function = \"spi1\";\n> +\t\t};\n> +\t\tcp1_xhci0_vbus_pins: cp1-xhci0-vbus-pins {\n> +\t\t\tmarvell,pins = \"mpp3\";\n> +\t\t\tmarvell,function = \"gpio\";\n> +\t\t};\n> +\t};\n> +};\n> +\n> +/*\n> + * Instantiate the second connected CP115\n> + */\n> +\n> +#define CP11X_NAME\t\tcp2\n> +#define CP11X_BASE\t\tf6000000\n> +#define CP11X_PCIEx_MEM_BASE(iface) (0xe5000000 + (iface * 0x1000000))\n> +#define CP11X_PCIEx_MEM_SIZE(iface) 0xf00000\n> +#define CP11X_PCIE0_BASE\tf6600000\n> +#define CP11X_PCIE1_BASE\tf6620000\n> +#define CP11X_PCIE2_BASE\tf6640000\n> +\n> +#include \"armada-cp115.dtsi\"\n> +\n> +#undef CP11X_NAME\n> +#undef CP11X_BASE\n> +#undef CP11X_PCIEx_MEM_BASE\n> +#undef CP11X_PCIEx_MEM_SIZE\n> +#undef CP11X_PCIE0_BASE\n> +#undef CP11X_PCIE1_BASE\n> +#undef CP11X_PCIE2_BASE\n> +\n> +&cp2_crypto {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp2_ethernet {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp2_xmdio {\n> +\tstatus = \"okay\";\n> +\tcp2_nbaset_phy0: ethernet-phy at 6 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <2>;\n> +\t};\n> +\tcp2_nbaset_phy1: ethernet-phy at 7 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <0>;\n> +\t};\n> +\tcp2_nbaset_phy2: ethernet-phy at 8 {\n> +\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n> +\t\treg = <8>;\n> +\t};\n> +};\n> +\n> +/* SLM-1521-V2, CON9 */\n> +&cp2_eth0 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"10gbase-kr\";\n> +\tphys = <&cp2_comphy2 0>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp2_eth1 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp2_comphy4 1>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp2_eth2 {\n> +\tstatus = \"okay\";\n> +\tphy-mode = \"2500base-x\";\n> +\tphys = <&cp2_comphy1 2>;\n> +\tmanaged = \"in-band-status\";\n> +};\n> +\n> +&cp2_gpio1 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp2_gpio2 {\n> +\tstatus = \"okay\";\n> +};\n> +\n> +&cp2_i2c0 {\n> +\tclock-frequency = <100000>;\n> +\t/* SLM-1521-V2 - U3 */\n> +\ti2c-mux at 72 {\n> +\t\tcompatible = \"nxp,pca9544\";\n> +\t\t#address-cells = <1>;\n> +\t\t#size-cells = <0>;\n> +\t\treg = <0x72>;\n> +\t\tcp2_sfpp0_i2c: i2c at 0 {\n> +\t\t\t#address-cells = <1>;\n> +\t\t\t#size-cells = <0>;\n> +\t\t\treg = <0>;\n> +\t\t};\n> +\n> +\t\ti2c at 1 {\n> +\t\t\t#address-cells = <1>;\n> +\t\t\t#size-cells = <0>;\n> +\t\t\treg = <1>;\n> +\t\t\t/* U12 */\n> +\t\t\tcp2_module_expander1: pca9555 at 21 {\n> +\t\t\t\tcompatible = \"nxp,pca9555\";\n> +\t\t\t\tpinctrl-names = \"default\";\n> +\t\t\t\tgpio-controller;\n> +\t\t\t\t#gpio-cells = <2>;\n> +\t\t\t\treg = <0x21>;\n> +\t\t\t};\n> +\t\t};\n> +\t};\n> +};\n> +\n> +&cp2_syscon0 {\n> +\tcp2_pinctrl: pinctrl {\n> +\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n> +\t\tcp2_i2c0_pins: cp2-i2c-pins-0 {\n> +\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n> +\t\t\tmarvell,function = \"i2c0\";\n> +\t\t};\n> +\t};\n> +};\n> -- \n> 2.17.1\n> \n> \n> _______________________________________________\n> openwrt-devel mailing list\n> openwrt-devel at lists.openwrt.org\n> https://lists.openwrt.org/mailman/listinfo/openwrt-devel",
      "quoted_context_pairs": [
        {
          "quoted": "From: Ian Chang <ianchang at ieiworld.com>\n\nSigned-off-by: Ian Chang <ianchang at ieiworld.com>\n---\n .../boot/dts/marvell/cn9131-puzzle-m901.dts   | 319 ++++++++++++\n .../boot/dts/marvell/cn9132-puzzle-m902.dts   | 481 ++++++++++++++++++\n 2 files changed, 800 insertions(+)\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n create mode 100644 target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n\ndiff --git a/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\nnew file mode 100644\nindex 0000000000..58e749490a\n--- /dev/null\n+++ b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts\n@@ -0,0 +1,319 @@\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9131-DB board.\n+ */\n+\n+#include \"cn9130.dtsi\"\n+\n+#include <dt-bindings/gpio/gpio.h>\n+\n+/ {\n+\tmodel = \"iEi Puzzle-M901\";\n+\tcompatible = \"iei,puzzle-m901\",\n+\t\t     \"marvell,armada-ap807-quad\", \"marvell,armada-ap807\";\n+\n+\tchosen {\n+\t\tstdout-path = \"serial0:115200n8\";\n+\t};\n+\n+\taliases {\n+\t\ti2c0 = &cp1_i2c0;\n+\t\ti2c1 = &cp0_i2c0;\n+\t\tethernet0 = &cp0_eth0;\n+\t\tethernet1 = &cp0_eth1;\n+\t\tethernet2 = &cp0_eth2;\n+\t\tethernet3 = &cp1_eth0;\n+\t\tethernet4 = &cp1_eth1;\n+\t\tethernet5 = &cp1_eth2;\n+\t\tgpio1 = &cp0_gpio1;\n+\t\tgpio2 = &cp0_gpio2;\n+\t\tgpio3 = &cp1_gpio1;\n+\t\tgpio4 = &cp1_gpio2;\n+\t};\n+\n+\tmemory at 00000000 {\n+\t\tdevice_type = \"memory\";\n+\t\treg = <0x0 0x0 0x0 0x80000000>;\n+\t};\n+};\n+\n+&uart0 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_uart0 {\n+\tstatus = \"okay\";\n+};\n+\n+/* on-board eMMC - U9 */\n+&ap_sdhci0 {\n+\tpinctrl-names = \"default\";\n+\tbus-width = <8>;\n+\tstatus = \"okay\";\n+\tmmc-ddr-1_8v;\n+\tmmc-hs400-1_8v;\n+};\n+\n+&cp0_crypto {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_xmdio {\n+\tstatus = \"okay\";\n+\tcp0_nbaset_phy0: ethernet-phy at 0 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <2>;\n+\t};\n+\tcp0_nbaset_phy1: ethernet-phy at 1 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <0>;\n+\t};\n+\tcp0_nbaset_phy2: ethernet-phy at 2 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <8>;\n+\t};\n+};\n+\n+&cp0_ethernet {\n+\tstatus = \"okay\";\n+};\n+\n+/* SLM-1521-V2, CON9 */\n+&cp0_eth0 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp0_comphy2 0>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_eth1 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp0_comphy4 1>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_eth2 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp0_comphy5 2>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_gpio1 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_gpio2 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_i2c0 {\n+\tpinctrl-names = \"default\";\n+\tpinctrl-0 = <&cp0_i2c0_pins>;\n+\tstatus = \"okay\";\n+\tclock-frequency = <100000>;\n+\trtc at 32 {\n+\t\tcompatible = \"epson,rx8130\";\n+\t\treg = <0x32>;\n+\t\twakeup-source;\n+\t};\n+};\n+\n+/* SLM-1521-V2, CON6 */\n+&cp0_pcie0 {\n+\tstatus = \"okay\";\n+\tnum-lanes = <2>;\n+\tnum-viewport = <8>;\n+\tphys = <&cp0_comphy0 0>, <&cp0_comphy1 0>;\n+};\n+\n+/* U55 */\n+&cp0_spi1 {\n+\tpinctrl-names = \"default\";\n+\tpinctrl-0 = <&cp0_spi0_pins>;\n+\treg = <0x700680 0x50>,          /* control */\n+\t      <0x2000000 0x1000000>;    /* CS0 */\n+\tstatus = \"okay\";\n+\tspi-flash at 0 {\n+\t\t#address-cells = <0x1>;\n+\t\t#size-cells = <0x1>;\n+\t\tcompatible = \"jedec,spi-nor\";\n+\t\treg = <0x0>;\n+\t\tspi-max-frequency = <40000000>;\n+\t\tpartitions {\n+\t\t\tcompatible = \"fixed-partitions\";\n+\t\t\t#address-cells = <1>;\n+\t\t\t#size-cells = <1>;\n+\t\t\tpartition at 0 {\n+\t\t\t\tlabel = \"U-Boot\";\n+\t\t\t\treg = <0x0 0x1f0000>;\n+\t\t\t};\n+\t\t\tpartition at 1f0000 {\n+\t\t\t\tlabel = \"U-Boot ENV Factory\";\n+\t\t\t\treg = <0x1f0000 0x10000>;\n+\t\t\t};\n+\t\t\tpartition at 200000 {\n+\t\t\t\tlabel = \"Reserved\";\n+\t\t\t\treg = <0x200000 0x1f0000>;\n+\t\t\t};\n+\t\t\tpartition at 3f0000 {\n+\t\t\t\tlabel = \"U-Boot ENV\";\n+\t\t\t\treg = <0x3f0000 0x10000>;\n+\t\t\t};\n+\t\t};\n+\t};\n+};\n+\n+&cp0_syscon0 {\n+\tcp0_pinctrl: pinctrl {\n+\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n+\t\tcp0_i2c0_pins: cp0-i2c-pins-0 {\n+\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n+\t\t\tmarvell,function = \"i2c0\";\n+\t\t};\n+\t\tcp0_i2c1_pins: cp0-i2c-pins-1 {\n+\t\t\tmarvell,pins = \"mpp35\", \"mpp36\";\n+\t\t\tmarvell,function = \"i2c1\";\n+\t\t};\n+\t\tcp0_ge1_rgmii_pins: cp0-ge-rgmii-pins-0 {\n+\t\t\tmarvell,pins = \"mpp0\", \"mpp1\", \"mpp2\",\n+\t\t\t\t       \"mpp3\", \"mpp4\", \"mpp5\",\n+\t\t\t\t       \"mpp6\", \"mpp7\", \"mpp8\",\n+\t\t\t\t       \"mpp9\", \"mpp10\", \"mpp11\";\n+\t\t\tmarvell,function = \"ge0\";\n+\t\t};\n+\t\tcp0_ge2_rgmii_pins: cp0-ge-rgmii-pins-1 {\n+\t\t\tmarvell,pins = \"mpp44\", \"mpp45\", \"mpp46\",\n+\t\t\t\t       \"mpp47\", \"mpp48\", \"mpp49\",\n+\t\t\t\t       \"mpp50\", \"mpp51\", \"mpp52\",\n+\t\t\t\t       \"mpp53\", \"mpp54\", \"mpp55\";\n+\t\t\tmarvell,function = \"ge1\";\n+\t\t};\n+\t\tcp0_spi0_pins: cp0-spi-pins-0 {\n+\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n+\t\t\tmarvell,function = \"spi1\";\n+\t\t};\n+\t};\n+};\n+\n+/*\n+ * Instantiate the first connected CP115\n+ */\n+\n+#define CP11X_NAME\t\tcp1\n+#define CP11X_BASE\t\tf6000000\n+#define CP11X_PCIEx_MEM_BASE(iface) (0xe2000000 + (iface * 0x1000000))\n+#define CP11X_PCIEx_MEM_SIZE(iface) 0xf00000\n+#define CP11X_PCIE0_BASE\tf6600000\n+#define CP11X_PCIE1_BASE\tf6620000\n+#define CP11X_PCIE2_BASE\tf6640000\n+\n+#include \"armada-cp115.dtsi\"\n+\n+#undef CP11X_NAME\n+#undef CP11X_BASE\n+#undef CP11X_PCIEx_MEM_BASE\n+#undef CP11X_PCIEx_MEM_SIZE\n+#undef CP11X_PCIE0_BASE\n+#undef CP11X_PCIE1_BASE\n+#undef CP11X_PCIE2_BASE\n+\n+&cp1_crypto {\n+\tstatus = \"okay\";\n+};\n+\n+&cp1_xmdio {\n+\tstatus = \"okay\";\n+\tcp1_nbaset_phy0: ethernet-phy at 3 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <2>;\n+\t};\n+\tcp1_nbaset_phy1: ethernet-phy at 4 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <0>;\n+\t};\n+\tcp1_nbaset_phy2: ethernet-phy at 5 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <8>;\n+\t};\n+};\n+\n+&cp1_ethernet {\n+\tstatus = \"okay\";\n+};\n+\n+/* CON50 */\n+&cp1_eth0 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp1_comphy2 0>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp1_eth1 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp1_comphy4 1>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp1_eth2 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp1_comphy5 2>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp1_sata0 {\n+\tstatus = \"okay\";\n+\tsata-port at 1 {\n+\t\tstatus = \"okay\";\n+\t\tphys = <&cp1_comphy0 1>;\n+\t};\n+};\n+\n+&cp1_gpio1 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp1_gpio2 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp1_i2c0 {\n+\tstatus = \"okay\";\n+\tpinctrl-names = \"default\";\n+\tpinctrl-0 = <&cp1_i2c0_pins>;\n+\tclock-frequency = <100000>;\n+};\n+\n+&cp1_syscon0 {\n+\tcp1_pinctrl: pinctrl {\n+\t\tcompatible = \"marvell,cp115-standalone-pinctrl\";\n+\t\tcp1_i2c0_pins: cp1-i2c-pins-0 {\n+\t\t\tmarvell,pins = \"mpp37\", \"mpp38\";\n+\t\t\tmarvell,function = \"i2c0\";\n+\t\t};\n+\t\tcp1_spi0_pins: cp1-spi-pins-0 {\n+\t\t\tmarvell,pins = \"mpp13\", \"mpp14\", \"mpp15\", \"mpp16\";\n+\t\t\tmarvell,function = \"spi1\";\n+\t\t};\n+\t\tcp1_xhci0_vbus_pins: cp1-xhci0-vbus-pins {\n+\t\t\tmarvell,pins = \"mpp3\";\n+\t\t\tmarvell,function = \"gpio\";\n+\t\t};\n+\t\tcp1_sfp_pins: sfp-pins {\n+\t\t\tmarvell,pins = \"mpp8\", \"mpp9\", \"mpp10\", \"mpp11\";\n+\t\t\tmarvell,function = \"gpio\";\n+\t\t};\n+\t};\n+};\n+\n+&cp1_usb3_1 {\n+\tstatus = \"okay\";\n+\tphys = <&cp1_comphy3 1>;\n+\tphy-names = \"usb\";\n+};\ndiff --git a/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\nnew file mode 100644\nindex 0000000000..0d27cc356e\n--- /dev/null\n+++ b/target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts\n@@ -0,0 +1,481 @@\n+// SPDX-License-Identifier: (GPL-2.0-or-later OR MIT)\n+/*\n+ * Copyright (C) 2019 Marvell International Ltd.\n+ *\n+ * Device tree for the CN9132-DB board.\n+ */\n+\n+#include \"cn9130.dtsi\"\n+\n+#include <dt-bindings/gpio/gpio.h>\n+\n+/ {\n+\tmodel = \"iEi Puzzle-M902\";\n+\tcompatible = \"iei,puzzle-m902\",\n+\t\t     \"marvell,armada-ap807-quad\", \"marvell,armada-ap807\";\n+\n+\tchosen {\n+\t\tstdout-path = \"serial0:115200n8\";\n+\t};\n+\n+\taliases {\n+\t\ti2c0 = &cp1_i2c0;\n+\t\ti2c1 = &cp0_i2c0;\n+\t\tgpio1 = &cp0_gpio1;\n+\t\tgpio2 = &cp0_gpio2;\n+\t\tgpio3 = &cp1_gpio1;\n+\t\tgpio4 = &cp1_gpio2;\n+\t\tgpio5 = &cp2_gpio1;\n+\t\tgpio6 = &cp2_gpio2;\n+\t\tethernet0 = &cp0_eth0;\n+\t\tethernet1 = &cp0_eth1;\n+\t\tethernet2 = &cp0_eth2;\n+\t\tethernet3 = &cp1_eth0;\n+\t\tethernet4 = &cp1_eth1;\n+\t\tethernet5 = &cp1_eth2;\n+\t\tethernet6 = &cp2_eth0;\n+\t\tethernet7 = &cp2_eth1;\n+\t\tethernet8 = &cp2_eth2;\n+\t\tspi1 = &cp0_spi0;\n+\t\tspi2 = &cp0_spi1;\n+\t\tserial1 = &cp0_uart0;\n+\t};\n+\n+\tmemory at 00000000 {\n+\t\tdevice_type = \"memory\";\n+\t\treg = <0x0 0x0 0x0 0x80000000>;\n+\t};\n+\n+\tcp2_reg_usb3_vbus0: cp2_usb3_vbus at 0 {\n+\t\tcompatible = \"regulator-fixed\";\n+\t\tregulator-name = \"cp2-xhci0-vbus\";\n+\t\tregulator-min-microvolt = <5000000>;\n+\t\tregulator-max-microvolt = <5000000>;\n+\t\tenable-active-high;\n+\t\tgpio = <&cp2_gpio1 2 GPIO_ACTIVE_HIGH>;\n+\t};\n+\n+\tcp2_usb3_0_phy0: cp2_usb3_phy0 {\n+\t\tcompatible = \"usb-nop-xceiv\";\n+\t\tvcc-supply = <&cp2_reg_usb3_vbus0>;\n+\t};\n+\n+\tcp2_reg_usb3_vbus1: cp2_usb3_vbus at 1 {\n+\t\tcompatible = \"regulator-fixed\";\n+\t\tregulator-name = \"cp2-xhci1-vbus\";\n+\t\tregulator-min-microvolt = <5000000>;\n+\t\tregulator-max-microvolt = <5000000>;\n+\t\tenable-active-high;\n+\t\tgpio = <&cp2_gpio1 3 GPIO_ACTIVE_HIGH>;\n+\t};\n+\n+\tcp2_usb3_0_phy1: cp2_usb3_phy1 {\n+\t\tcompatible = \"usb-nop-xceiv\";\n+\t\tvcc-supply = <&cp2_reg_usb3_vbus1>;\n+\t};\n+\n+\tcp2_sfp_eth0: sfp-eth0 {\n+\t\tcompatible = \"sff,sfp\";\n+\t\ti2c-bus = <&cp2_sfpp0_i2c>;\n+\t\tlos-gpio = <&cp2_module_expander1 11 GPIO_ACTIVE_HIGH>;\n+\t\tmod-def0-gpio = <&cp2_module_expander1 10 GPIO_ACTIVE_LOW>;\n+\t\ttx-disable-gpio = <&cp2_module_expander1 9 GPIO_ACTIVE_HIGH>;\n+\t\ttx-fault-gpio = <&cp2_module_expander1 8 GPIO_ACTIVE_HIGH>;\n+\t\tstatus = \"disabled\";\n+\t};\n+};\n+\n+&uart0 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_uart0 {\n+\tstatus = \"okay\";\n+};\n+\n+/* on-board eMMC - U9 */\n+&ap_sdhci0 {\n+\tpinctrl-names = \"default\";\n+\tbus-width = <8>;\n+\tstatus = \"okay\";\n+\tmmc-ddr-1_8v;\n+\tmmc-hs400-1_8v;\n+};\n+\n+&cp0_crypto {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_xmdio {\n+\tstatus = \"okay\";\n+\tcp0_nbaset_phy0: ethernet-phy at 0 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <2>;\n+\t};\n+\tcp0_nbaset_phy1: ethernet-phy at 1 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <0>;\n+\t};\n+\tcp0_nbaset_phy2: ethernet-phy at 2 {\n+\t\tcompatible = \"ethernet-phy-ieee802.3-c45\";\n+\t\treg = <8>;\n+\t};\n+};\n+\n+&cp0_ethernet {\n+\tstatus = \"okay\";\n+};\n+\n+/* SLM-1521-V2, CON9 */\n+&cp0_eth0 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"10gbase-kr\";\n+\tphys = <&cp0_comphy2 0>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_eth1 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp0_comphy4 1>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_eth2 {\n+\tstatus = \"okay\";\n+\tphy-mode = \"2500base-x\";\n+\tphys = <&cp0_comphy1 2>;\n+\tmanaged = \"in-band-status\";\n+};\n+\n+&cp0_gpio1 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_gpio2 {\n+\tstatus = \"okay\";\n+};\n+\n+&cp0_i2c0 {\n+\tpinctrl-names = \"default\";\n+\tpinctrl-0 = <&cp0_i2c0_pins>;\n+\tstatus = \"okay\";\n+\tclock-frequency = <100000>;\n+\trtc at 32 {\n+\t\tcompatible = \"epson,rx8130\";\n+\t\treg = <0x32>;\n+\t\twakeup-source;\n+\t};\n+};\n+\n+&cp0_i2c1 {\n+\tclock-frequency = <100000>;\n+};\n+\n+/* SLM-1521-V2, CON6 */\n+&cp0_sata0 {\n+\tstatus = \"okay\";\n+\tsata-port at 1 {\n+\t\tstatus = \"okay\";\n+\t\tphys = <&cp0_comphy0 1>;\n+\t};\n+};\n+\n+&cp0_pcie2 {\n+\tstatus = \"okay\";\n+\tnum-lanes = <1>;\n+\tnum-viewport = <8>;\n+\tphys = <&cp0_comphy5 2>;\n+};\n+\n+/* U55 */\n+&cp0_spi1 {\n+\tpinctrl-names = \"default\";\n+\tpinctrl-0 = <&cp0_spi0_pins>;\n+\treg = <0x700680 0x50>,          /* control */\n+\t      <0x2000000 0x1000000>;    /* CS0 */\n+\tstatus = \"okay\";\n+\tspi-flash at 0 {\n+\t\t#address-cells = <0x1>;\n+\t\t#size-cells = <0x1>;\n+\t\tcompatible = \"jedec,spi-nor\";\n+\t\treg = <0x0>;\n+\t\tspi-max-frequency = <40000000>;\n+\t\tpartitions {\n+\t\t\tcompatible = \"fixed-partitions\";\n+\t\t\t#address-cells = <1>;\n+\t\t\t#size-cells = <1>;\n+\t\t\tpartition at 0 {\n+\t\t\t\tlabel = \"U-Boot\";\n+\t\t\t\treg = <0x0 0x1f0000>;\n+\t\t\t};\n+\t\tpartition at 1f0000 {",
          "response": "Indentation here is wrong and missing one tab. This has already been\na problem in the previous iteration of this series.",
          "line_index": 554
        }
      ],
      "mentioned_files": [
        "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts",
        "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts"
      ],
      "mentioned_commits": [
        "00000000",
        "0000000000",
        "0d27cc356e",
        "40000000",
        "5000000",
        "58e749490a",
        "f4000000",
        "f4600000",
        "f4620000",
        "f4640000",
        "f6000000",
        "f6600000",
        "f6620000",
        "f6640000"
      ],
      "keyword_matches": [
        "\\[PATCH\\s+v[2-9]",
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
        "concurrency",
        "kernel-driver"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 2,
  "author_count": 2,
  "date_range": [
    "2021-08-03T11:35:58+08:00",
    "2021-08-08T16:30:12+01:00"
  ],
  "all_mentioned_files": [
    "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9131-puzzle-m901.dts",
    "target/linux/mvebu/files/arch/arm64/boot/dts/marvell/cn9132-puzzle-m902.dts"
  ],
  "all_mentioned_commits": [
    "00000000",
    "0000000000",
    "0d27cc356e",
    "40000000",
    "5000000",
    "58e749490a",
    "f4000000",
    "f4600000",
    "f4620000",
    "f4640000",
    "f6000000",
    "f6600000",
    "f6620000",
    "f6640000"
  ],
  "categories": [
    "kernel-driver",
    "concurrency"
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
  "source_refs": [
    {
      "source_file": "devel/2021-August.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-August.txt",
      "message_id": "<20210803033558.23441-1-ianchang@ieiworld.com>",
      "byte_offset": 16105
    },
    {
      "source_file": "devel/2021-August.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-August.txt",
      "message_id": "<YQ/4hEE7D6i2eZrc@makrotopia.org>",
      "byte_offset": 248068
    }
  ],
  "score": 1.0
}
```

## Sample 3

```json
{
  "thread_id": "<mailman.52.1613626480.962.openwrt-bugs@lists.openwrt.org>",
  "subject": "[FS#3607] fakeroot fails to build from source with glibc 2.33",
  "messages": [
    {
      "source_file": "bugs/2021-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-February.txt",
      "byte_offset": 161407,
      "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Thu Feb 18 00:34:22 2021",
      "message_id": "<mailman.52.1613626480.962.openwrt-bugs@lists.openwrt.org>",
      "in_reply_to": "<FS3607@bugs.openwrt.org>",
      "references": [
        "<FS3607@bugs.openwrt.org>"
      ],
      "from_addr": "openwrt-bugs@lists.openwrt.org",
      "from_name": "",
      "date_raw": "Thu, 18 Feb 2021 05:34:22 +0000",
      "date_iso": "2021-02-18T05:34:22+00:00",
      "subject": "[FS#3607] fakeroot fails to build from source with glibc 2.33",
      "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3607 - fakeroot fails to build from source with glibc 2.33\nUser who did this - plunder (cascadingstyletrees)\n\n----------\nI was able to build in Arch today.\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3607#comment9377\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3607 - fakeroot fails to build from source with glibc 2.33\nUser who did this - plunder (cascadingstyletrees)\n\n----------\nI was able to build in Arch today.\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3607#comment9377\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "quoted_context_pairs": [],
      "mentioned_files": [],
      "mentioned_commits": [],
      "keyword_matches": [
        "bug",
        "do\\s+not|don't",
        "fail(?:ed|ure|ing)?"
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
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2021-02-18T05:34:22+00:00",
    "2021-02-18T05:34:22+00:00"
  ],
  "all_mentioned_files": [],
  "all_mentioned_commits": [],
  "categories": [
    "uncategorized"
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
  "source_refs": [
    {
      "source_file": "bugs/2021-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-February.txt",
      "message_id": "<mailman.52.1613626480.962.openwrt-bugs@lists.openwrt.org>",
      "byte_offset": 161407
    }
  ],
  "score": 0.65
}
```

## Sample 4

```json
{
  "thread_id": "<mailman.859.1614506787.959.openwrt-bugs@lists.openwrt.org>",
  "subject": "[FS#3090] dnsmasq:  daemon.err dnsmasq[6363]: failed to load names from /tmp/hosts/dhcp.cfg01411c: Permission ",
  "messages": [
    {
      "source_file": "bugs/2021-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-February.txt",
      "byte_offset": 374043,
      "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Sun Feb 28 05:06:22 2021",
      "message_id": "<mailman.859.1614506787.959.openwrt-bugs@lists.openwrt.org>",
      "in_reply_to": "<FS3090@bugs.openwrt.org>",
      "references": [
        "<FS3090@bugs.openwrt.org>"
      ],
      "from_addr": "openwrt-bugs@lists.openwrt.org",
      "from_name": "",
      "date_raw": "Sun, 28 Feb 2021 10:06:22 +0000",
      "date_iso": "2021-02-28T10:06:22+00:00",
      "subject": "[FS#3090] dnsmasq:  daemon.err dnsmasq[6363]: failed to load names from /tmp/hosts/dhcp.cfg01411c: Permission ",
      "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3090 - dnsmasq:  daemon.err dnsmasq[6363]: failed to load names from /tmp/hosts/dhcp.cfg01411c: Permission \nUser who did this - pgaufillet (pgaufillet)\n\n----------\nConfirmed also in master (r15225), but on specific cases only:\n* Running manually /etc/init.d/dnsmasq start/restart creates /tmp/host/dhcp.cfg01411c with 644 root:root access rights.\n* Running manually /etc/init.d/network restart creates /tmp/host/dhcp.cfg01411c with 600 root:root access rights.\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3090#comment9428\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3090 - dnsmasq:  daemon.err dnsmasq[6363]: failed to load names from /tmp/hosts/dhcp.cfg01411c: Permission \nUser who did this - pgaufillet (pgaufillet)\n\n----------\nConfirmed also in master (r15225), but on specific cases only:\n* Running manually /etc/init.d/dnsmasq start/restart creates /tmp/host/dhcp.cfg01411c with 644 root:root access rights.\n* Running manually /etc/init.d/network restart creates /tmp/host/dhcp.cfg01411c with 600 root:root access rights.\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3090#comment9428\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "quoted_context_pairs": [],
      "mentioned_files": [],
      "mentioned_commits": [],
      "keyword_matches": [
        "bug",
        "do\\s+not|don't",
        "fail(?:ed|ure|ing)?",
        "init\\.d"
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
        "procd-init"
      ],
      "has_patch_subject": false,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2021-02-28T10:06:22+00:00",
    "2021-02-28T10:06:22+00:00"
  ],
  "all_mentioned_files": [],
  "all_mentioned_commits": [],
  "categories": [
    "procd-init"
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
  "source_refs": [
    {
      "source_file": "bugs/2021-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-February.txt",
      "message_id": "<mailman.859.1614506787.959.openwrt-bugs@lists.openwrt.org>",
      "byte_offset": 374043
    }
  ],
  "score": 0.65
}
```

## Sample 5

```json
{
  "thread_id": "<87h67oka59.fsf@miraculix.mork.no>",
  "subject": "fun with git log",
  "messages": [
    {
      "source_file": "devel/2024-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2024-November.txt",
      "byte_offset": 428164,
      "mbox_from_line": "From bjorn at mork.no  Sat Nov 30 07:34:58 2024",
      "message_id": "<87h67oka59.fsf@miraculix.mork.no>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "bjorn@mork.no",
      "from_name": "",
      "date_raw": "Sat, 30 Nov 2024 16:34:58 +0100",
      "date_iso": "2024-11-30T16:34:58+01:00",
      "subject": "fun with git log",
      "body_for_scoring": "tl; dr; \"git log --format=...\" may print much more than expected\n\nJust had an exciting experience trying to buold an image from master.\nThe build would just hang at one specific package, which happend to be a\nslightly modified one (I have been planning to cleanup and submit the\nchanges for a few years  - still on the todo list).\n\nLooking closer, it seemed that autotools never completed configuring the\npackage.  It would just loop over\n\nconfigure.ac:8: the top level\nconfigure.ac:25: warning: The macro `AC_HEADER_STDC' is obsolete.\nconfigure.ac:25: You should run autoupdate.\n./lib/autoconf/headers.m4:704: AC_HEADER_STDC is expanded from...\nconfigure.ac:25: the top level\n cd . && /bin/bash ./config.status Makefile depfiles\nconfig.status: creating Makefile\nconfig.status: executing depfiles commands\nmake[3]: Makefile.am: Timestamp out of range; substituting 2514-05-30 01:53:03.999999999\nmake[3]: Warning: File 'Makefile.am' has modification time 15446890191 s in the future\nmake[3]: configure.ac: Timestamp out of range; substituting 2514-05-30 01:53:03.999999999\nCDPATH=\"${ZSH_VERSION+.}:\" && cd . && /bin/bash '/home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing' aclocal-1.16 \n cd . && /bin/bash /home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing automake-1.16 --foreign\nCDPATH=\"${ZSH_VERSION+.}:\" && cd . && /bin/bash '/home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing' autoconf\nconfigure.ac:8: warning: The macro `AC_CONFIG_HEADER' is obsolete.\nconfigure.ac:8: You should run autoupdate.\n./lib/autoconf/status.m4:719: AC_CONFIG_HEADER is expanded from...\nconfigure.ac:8: the top level\n\n\n\nagain and again.  Yes, and those files in the build directory really had\nunexpcted timestamps.  They might be old, but not from 1901 :-)\n\nLooking at the cached tar file revealed the source of confusion:\n\nbjorn at canardo:/usr/local/src/openwrt$ zstdcat dl/mini-snmpd-1.6.tar.zst|tar tvf - \ndrwxr-xr-x 0/0               0 -9223372036854775808 mini-snmpd-1.6/\n-rw-r--r-- 0/0             504 -9223372036854775808 mini-snmpd-1.6/.clang-format\n-rw-r--r-- 0/0             258 -9223372036854775808 mini-snmpd-1.6/.gitignore\n-rw-r--r-- 0/0            1885 -9223372036854775808 mini-snmpd-1.6/.travis.yml\n-rw-r--r-- 0/0             573 -9223372036854775808 mini-snmpd-1.6/AUTHORS\n-rw-r--r-- 0/0            3501 -9223372036854775808 mini-snmpd-1.6/CONTRIBUTING.md\n-rw-r--r-- 0/0           17989 -9223372036854775808 mini-snmpd-1.6/COPYING\n-rw-r--r-- 0/0            6422 -9223372036854775808 mini-snmpd-1.6/ChangeLog.md\n-rw-r--r-- 0/0            2398 -9223372036854775808 mini-snmpd-1.6/Makefile.am\n-rw-r--r-- 0/0            2608 -9223372036854775808 mini-snmpd-1.6/README.develop\n[snip]\n\nThose timestamps do not look good. But where did that come from? I host\nmy forked source on github, so there shouldn't be any difference from\nany other github hosted package.  But the bug only seemed to affect this\npackage (of the subset I built).  All the other generated tar archives\nhad sane timestamps.\n\nLooking at include/download.mk I found that the timestamp is taken from\na TAR_TIMESTAMP variable, with rules to set that to a stable and\nreasonable value for different version control systems.  But there were\nno relevant changes to any of that code since the last time I built\nthis.  The git rule was\n\n export TAR_TIMESTAMP=`cd $(SUBDIR) && git log -1 --format='@%ct'`\n\nwhich looked fine to me.  But just to be sure, I tested it in my openwrt\nsource tree.  And that's a \"Doh!\" moment:\n\nbjorn at canardo:/usr/local/src/openwrt$ git log -1 --format='@%ct'\ngpg: Signature made Sat Nov 30 14:24:36 2024 CET\ngpg:                using EDDSA key 687BE08049F161EDA67AB21222044ECBBFA4615D\ngpg: please do a --check-trustdb\ngpg: Good signature from \"Bj?rn Mork <bmork at telenor.net>\" [ultimate]\ngpg:                 aka \"Bj?rn Mork <bjorn at mork.no>\" [ultimate]\nPrimary key fingerprint: F461 6F51 2B11 3B3C 1827  3C21 E197 FC12 EFF0 5ECD\n     Subkey fingerprint: 687B E080 49F1 61ED A67A  B212 2204 4ECB BFA4 615D\n@1732973075\n\n\nSo, what happened here?  I can tell you: I recently set\n\n log.showSignature = true\n\nin my global git config.  The special problem with the package source\nwas the top commit was signed.\n\nI assume the reason this specific trigger qhasn't come up earlier is\nthat signed top commits still are relatively rare, and there are\nprobably very few people having set \"log.showSignature = true\" globally\non their OpenWrt build machine.\n\nJust don't to that?  Or maybe make sure the output from \"git log\" is\nconsistent?  It is affected by several config settings.  You should\nprobably disable all global configuration in any script parsing git log\noutput.  I believe something like\n\n export GIT_CONFIG_NOSYSTEM=true\n export GIT_CONFIG_GLOBAL=/dev/null\n\nwill do.\n\n\n\nBj?rn",
      "body_no_diff": "tl; dr; \"git log --format=...\" may print much more than expected\n\nJust had an exciting experience trying to buold an image from master.\nThe build would just hang at one specific package, which happend to be a\nslightly modified one (I have been planning to cleanup and submit the\nchanges for a few years  - still on the todo list).\n\nLooking closer, it seemed that autotools never completed configuring the\npackage.  It would just loop over\n\nconfigure.ac:8: the top level\nconfigure.ac:25: warning: The macro `AC_HEADER_STDC' is obsolete.\nconfigure.ac:25: You should run autoupdate.\n./lib/autoconf/headers.m4:704: AC_HEADER_STDC is expanded from...\nconfigure.ac:25: the top level\n cd . && /bin/bash ./config.status Makefile depfiles\nconfig.status: creating Makefile\nconfig.status: executing depfiles commands\nmake[3]: Makefile.am: Timestamp out of range; substituting 2514-05-30 01:53:03.999999999\nmake[3]: Warning: File 'Makefile.am' has modification time 15446890191 s in the future\nmake[3]: configure.ac: Timestamp out of range; substituting 2514-05-30 01:53:03.999999999\nCDPATH=\"${ZSH_VERSION+.}:\" && cd . && /bin/bash '/home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing' aclocal-1.16 \n cd . && /bin/bash /home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing automake-1.16 --foreign\nCDPATH=\"${ZSH_VERSION+.}:\" && cd . && /bin/bash '/home/bjorn/tmp/tmp-openwrt/build_dir/target-mips_4kec_musl/mini-snmpd-1.6/aux/missing' autoconf\nconfigure.ac:8: warning: The macro `AC_CONFIG_HEADER' is obsolete.\nconfigure.ac:8: You should run autoupdate.\n./lib/autoconf/status.m4:719: AC_CONFIG_HEADER is expanded from...\nconfigure.ac:8: the top level\n\n\n\nagain and again.  Yes, and those files in the build directory really had\nunexpcted timestamps.  They might be old, but not from 1901 :-)\n\nLooking at the cached tar file revealed the source of confusion:\n\nbjorn at canardo:/usr/local/src/openwrt$ zstdcat dl/mini-snmpd-1.6.tar.zst|tar tvf - \ndrwxr-xr-x 0/0               0 -9223372036854775808 mini-snmpd-1.6/\n-rw-r--r-- 0/0             504 -9223372036854775808 mini-snmpd-1.6/.clang-format\n-rw-r--r-- 0/0             258 -9223372036854775808 mini-snmpd-1.6/.gitignore\n-rw-r--r-- 0/0            1885 -9223372036854775808 mini-snmpd-1.6/.travis.yml\n-rw-r--r-- 0/0             573 -9223372036854775808 mini-snmpd-1.6/AUTHORS\n-rw-r--r-- 0/0            3501 -9223372036854775808 mini-snmpd-1.6/CONTRIBUTING.md\n-rw-r--r-- 0/0           17989 -9223372036854775808 mini-snmpd-1.6/COPYING\n-rw-r--r-- 0/0            6422 -9223372036854775808 mini-snmpd-1.6/ChangeLog.md\n-rw-r--r-- 0/0            2398 -9223372036854775808 mini-snmpd-1.6/Makefile.am\n-rw-r--r-- 0/0            2608 -9223372036854775808 mini-snmpd-1.6/README.develop\n[snip]\n\nThose timestamps do not look good. But where did that come from? I host\nmy forked source on github, so there shouldn't be any difference from\nany other github hosted package.  But the bug only seemed to affect this\npackage (of the subset I built).  All the other generated tar archives\nhad sane timestamps.\n\nLooking at include/download.mk I found that the timestamp is taken from\na TAR_TIMESTAMP variable, with rules to set that to a stable and\nreasonable value for different version control systems.  But there were\nno relevant changes to any of that code since the last time I built\nthis.  The git rule was\n\n export TAR_TIMESTAMP=`cd $(SUBDIR) && git log -1 --format='@%ct'`\n\nwhich looked fine to me.  But just to be sure, I tested it in my openwrt\nsource tree.  And that's a \"Doh!\" moment:\n\nbjorn at canardo:/usr/local/src/openwrt$ git log -1 --format='@%ct'\ngpg: Signature made Sat Nov 30 14:24:36 2024 CET\ngpg:                using EDDSA key 687BE08049F161EDA67AB21222044ECBBFA4615D\ngpg: please do a --check-trustdb\ngpg: Good signature from \"Bj?rn Mork <bmork at telenor.net>\" [ultimate]\ngpg:                 aka \"Bj?rn Mork <bjorn at mork.no>\" [ultimate]\nPrimary key fingerprint: F461 6F51 2B11 3B3C 1827  3C21 E197 FC12 EFF0 5ECD\n     Subkey fingerprint: 687B E080 49F1 61ED A67A  B212 2204 4ECB BFA4 615D\n@1732973075\n\n\nSo, what happened here?  I can tell you: I recently set\n\n log.showSignature = true\n\nin my global git config.  The special problem with the package source\nwas the top commit was signed.\n\nI assume the reason this specific trigger qhasn't come up earlier is\nthat signed top commits still are relatively rare, and there are\nprobably very few people having set \"log.showSignature = true\" globally\non their OpenWrt build machine.\n\nJust don't to that?  Or maybe make sure the output from \"git log\" is\nconsistent?  It is affected by several config settings.  You should\nprobably disable all global configuration in any script parsing git log\noutput.  I believe something like\n\n export GIT_CONFIG_NOSYSTEM=true\n export GIT_CONFIG_GLOBAL=/dev/null\n\nwill do.\n\n\n\nBj?rn",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "include/download.mk"
      ],
      "mentioned_commits": [
        "15446890191",
        "1732973075",
        "999999999"
      ],
      "keyword_matches": [
        "Makefile",
        "bug",
        "do\\s+not|don't",
        "warning:"
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
        "c-language",
        "uci-config",
        "patch-maintenance"
      ],
      "has_patch_subject": false,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2024-11-30T16:34:58+01:00",
    "2024-11-30T16:34:58+01:00"
  ],
  "all_mentioned_files": [
    "include/download.mk"
  ],
  "all_mentioned_commits": [
    "15446890191",
    "1732973075",
    "999999999"
  ],
  "categories": [
    "build-system",
    "c-language",
    "uci-config",
    "patch-maintenance"
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
  "source_refs": [
    {
      "source_file": "devel/2024-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2024-November.txt",
      "message_id": "<87h67oka59.fsf@miraculix.mork.no>",
      "byte_offset": 428164
    }
  ],
  "score": 0.7
}
```

## Sample 6

```json
{
  "thread_id": "<mailman.1305.1609501095.939.openwrt-bugs@lists.openwrt.org>",
  "subject": "[FS#3540] ip6806x serial console is mute once kernel takes control (r15355-19d7e73ecc)",
  "messages": [
    {
      "source_file": "bugs/2021-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-January.txt",
      "byte_offset": 1159,
      "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Fri Jan  1 06:37:58 2021",
      "message_id": "<mailman.1305.1609501095.939.openwrt-bugs@lists.openwrt.org>",
      "in_reply_to": "<FS3540@bugs.openwrt.org>",
      "references": [
        "<FS3540@bugs.openwrt.org>"
      ],
      "from_addr": "openwrt-bugs@lists.openwrt.org",
      "from_name": "",
      "date_raw": "Fri, 01 Jan 2021 11:37:58 +0000",
      "date_iso": "2021-01-01T11:37:58+00:00",
      "subject": "[FS#3540] ip6806x serial console is mute once kernel takes control (r15355-19d7e73ecc)",
      "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3540 - ip6806x serial console is mute once kernel takes control (r15355-19d7e73ecc)\nUser who did this - Pawe? Dembicki (CHKDSK88)\n\n----------\nGuys with the problem, please test my PR with fix:\n\nhttps://github.com/openwrt/openwrt/pull/3740\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3540#comment9247\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#3540 - ip6806x serial console is mute once kernel takes control (r15355-19d7e73ecc)\nUser who did this - Pawe? Dembicki (CHKDSK88)\n\n----------\nGuys with the problem, please test my PR with fix:\n\nhttps://github.com/openwrt/openwrt/pull/3740\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=3540#comment9247\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "quoted_context_pairs": [],
      "mentioned_files": [],
      "mentioned_commits": [
        "19d7e73ecc"
      ],
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
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2021-01-01T11:37:58+00:00",
    "2021-01-01T11:37:58+00:00"
  ],
  "all_mentioned_files": [],
  "all_mentioned_commits": [
    "19d7e73ecc"
  ],
  "categories": [
    "kernel-driver"
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
  "source_refs": [
    {
      "source_file": "bugs/2021-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2021-January.txt",
      "message_id": "<mailman.1305.1609501095.939.openwrt-bugs@lists.openwrt.org>",
      "byte_offset": 1159
    }
  ],
  "score": 0.75
}
```

## Sample 7

```json
{
  "thread_id": "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>",
  "subject": "out-of-tree mac80211 driver in a package feed; how to determine mac80211 version",
  "messages": [
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "byte_offset": 517205,
      "mbox_from_line": "From tharvey at gateworks.com  Tue Jan 28 16:37:35 2025",
      "message_id": "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "tharvey@gateworks.com",
      "from_name": "",
      "date_raw": "Tue, 28 Jan 2025 16:37:35 -0800",
      "date_iso": "2025-01-28T16:37:35-08:00",
      "subject": "out-of-tree mac80211 driver in a package feed; how to determine mac80211 version",
      "body_for_scoring": "Greetings,\n\nI've got an out-of-tree mac80211 driver [1] that I built in a package\nfeed. The driver has a lot of kernel compatibility defines using\nKERNEL_VERSION(x,y,z) and LINUX_VERSION_CODE to support various\nkernels from fairly old up to 6.12. I'm finding that this doesn't\nquite work for an OpenWrt package as its the mac80211 version that\nneeds to be used for LINUX_VERSION_CODE instead of the kernel being\nused.\n\nIs there a recommendation of how to handle this?\n\nBest Regards,\n\nTim\n[1] https://github.com/Gateworks/gw-openwrt-packages/blob/master/gateworks/nrc7292/Makefile",
      "body_no_diff": "Greetings,\n\nI've got an out-of-tree mac80211 driver [1] that I built in a package\nfeed. The driver has a lot of kernel compatibility defines using\nKERNEL_VERSION(x,y,z) and LINUX_VERSION_CODE to support various\nkernels from fairly old up to 6.12. I'm finding that this doesn't\nquite work for an OpenWrt package as its the mac80211 version that\nneeds to be used for LINUX_VERSION_CODE instead of the kernel being\nused.\n\nIs there a recommendation of how to handle this?\n\nBest Regards,\n\nTim\n[1] https://github.com/Gateworks/gw-openwrt-packages/blob/master/gateworks/nrc7292/Makefile",
      "quoted_context_pairs": [],
      "mentioned_files": [],
      "mentioned_commits": [],
      "keyword_matches": [
        "Makefile",
        "instead\\s+of",
        "out[-.\\s]of[-.\\s]tree"
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
        "build-system",
        "kernel-driver",
        "package-packaging"
      ],
      "has_patch_subject": false,
      "has_keyword_match": true,
      "disposition": "primary"
    },
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "byte_offset": 526978,
      "mbox_from_line": "From ansuelsmth at gmail.com  Wed Jan 29 00:13:49 2025",
      "message_id": "<CA+_ehUwNTa7_EaFJDynRTPyNvuJ0cTaNk5o1+HP=q0G+N31H4w@mail.gmail.com>",
      "in_reply_to": "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>",
      "references": [
        "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>"
      ],
      "from_addr": "ansuelsmth@gmail.com",
      "from_name": "",
      "date_raw": "Wed, 29 Jan 2025 09:13:49 +0100",
      "date_iso": "2025-01-29T09:13:49+01:00",
      "subject": "out-of-tree mac80211 driver in a package feed; how to determine mac80211 version",
      "body_for_scoring": "Il giorno mer 29 gen 2025 alle ore 01:39 Tim Harvey\n<tharvey at gateworks.com> ha scritto:\n\nHi Tim,\n\nfor mac80211, we use the backports project and that follows a\ndifferent version than\nwhat is used for linux.\nIf your intention is to propose this in OpenWrt, ideally all the\ndefine flag should\nbe dropped and produce a more up-to-date driver with maybe 6.12 and 6.6 max.\n\nBut it really doesn't make sense to have IFDEF to support 2.x or 3.x...\n\nAlso consider that mac80211 backports define have different config flag to\ndifferentiate from kernel config (CPTCFG prefix)",
      "body_no_diff": "Il giorno mer 29 gen 2025 alle ore 01:39 Tim Harvey\n<tharvey at gateworks.com> ha scritto:\n>\n> Greetings,\n>\n> I've got an out-of-tree mac80211 driver [1] that I built in a package\n> feed. The driver has a lot of kernel compatibility defines using\n> KERNEL_VERSION(x,y,z) and LINUX_VERSION_CODE to support various\n> kernels from fairly old up to 6.12. I'm finding that this doesn't\n> quite work for an OpenWrt package as its the mac80211 version that\n> needs to be used for LINUX_VERSION_CODE instead of the kernel being\n> used.\n>\n> Is there a recommendation of how to handle this?\n>\n> Best Regards,\n>\n> Tim\n> [1] https://github.com/Gateworks/gw-openwrt-packages/blob/master/gateworks/nrc7292/Makefile\n>\n\nHi Tim,\n\nfor mac80211, we use the backports project and that follows a\ndifferent version than\nwhat is used for linux.\nIf your intention is to propose this in OpenWrt, ideally all the\ndefine flag should\nbe dropped and produce a more up-to-date driver with maybe 6.12 and 6.6 max.\n\nBut it really doesn't make sense to have IFDEF to support 2.x or 3.x...\n\nAlso consider that mac80211 backports define have different config flag to\ndifferentiate from kernel config (CPTCFG prefix)",
      "quoted_context_pairs": [],
      "mentioned_files": [],
      "mentioned_commits": [],
      "keyword_matches": [
        "out[-.\\s]of[-.\\s]tree",
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
        "build-system",
        "uci-config",
        "kernel-driver",
        "patch-maintenance",
        "package-packaging"
      ],
      "has_patch_subject": false,
      "has_keyword_match": true,
      "disposition": "primary"
    },
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "byte_offset": 537622,
      "mbox_from_line": "From tharvey at gateworks.com  Fri Jan 31 11:56:01 2025",
      "message_id": "<CAJ+vNU1f2uh2733DzowG9ZgjjYNrk+KF6t9v3YUDuqypHu0+uA@mail.gmail.com>",
      "in_reply_to": "<CA+_ehUwNTa7_EaFJDynRTPyNvuJ0cTaNk5o1+HP=q0G+N31H4w@mail.gmail.com>",
      "references": [
        "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>",
        "<CA+_ehUwNTa7_EaFJDynRTPyNvuJ0cTaNk5o1+HP=q0G+N31H4w@mail.gmail.com>"
      ],
      "from_addr": "tharvey@gateworks.com",
      "from_name": "",
      "date_raw": "Fri, 31 Jan 2025 11:56:01 -0800",
      "date_iso": "2025-01-31T11:56:01-08:00",
      "subject": "out-of-tree mac80211 driver in a package feed; how to determine mac80211 version",
      "body_for_scoring": "On Wed, Jan 29, 2025 at 12:14?AM Christian Marangi (Ansuel)\n<ansuelsmth at gmail.com> wrote:\n\nHi Ansuel,\n\nWhy 6.6? If main is using mac80211 linux-backports of 6.12 wouldn't I\nonly need to make sure its compatible with 6.12?\n\nThe out-of-tree driver I use is used for other kernels not just\nOpenWrt so my openwrt package is just a Makefile to build that shared\ndriver source against OpenWrt. Therefor there are lots of\ncompatibility defs to handle changes in mac80211 such as:\n#if KERNEL_VERSION(6, 7, 0) <= LINUX_VERSION_CODE\nstatic int nrc_post_channel_switch(struct ieee80211_hw *hw, struct\nieee80211_vif *vif, struct ieee80211_bss_conf *conf)\n#else\nstatic int nrc_post_channel_switch(struct ieee80211_hw *hw, struct\nieee80211_vif *vif)\n#endif\n\nThis allows the driver source to be compatible with a range of kernels\nas is done in many out-of-tree kernel drivers.\n\nSo what I'm trying to do is to understand how to use the same\nout-of-tree driver source with OpenWrt but the 'LINUX_VERSION_CODE' is\nthe kernel version (6.6) which is wrong and needs to be the version of\nthe mac80211 backport (6.12).\n\n\nWhat do you mean by 2.x or 3.x or are you saying it doesn't make sense\nto use ifdef's at all? It does require compat ifdefs if I'm not trying\nto create multiple driver sources for different kernels.\n\n\nInteresting... but unfortunately I see nothing in the backports\n.config that shows the kernel version the backport is from.\n\nBest Regards,\n\nTim",
      "body_no_diff": "On Wed, Jan 29, 2025 at 12:14?AM Christian Marangi (Ansuel)\n<ansuelsmth at gmail.com> wrote:\n>\n> Il giorno mer 29 gen 2025 alle ore 01:39 Tim Harvey\n> <tharvey at gateworks.com> ha scritto:\n> >\n> > Greetings,\n> >\n> > I've got an out-of-tree mac80211 driver [1] that I built in a package\n> > feed. The driver has a lot of kernel compatibility defines using\n> > KERNEL_VERSION(x,y,z) and LINUX_VERSION_CODE to support various\n> > kernels from fairly old up to 6.12. I'm finding that this doesn't\n> > quite work for an OpenWrt package as its the mac80211 version that\n> > needs to be used for LINUX_VERSION_CODE instead of the kernel being\n> > used.\n> >\n> > Is there a recommendation of how to handle this?\n> >\n> > Best Regards,\n> >\n> > Tim\n> > [1] https://github.com/Gateworks/gw-openwrt-packages/blob/master/gateworks/nrc7292/Makefile\n> >\n>\n> Hi Tim,\n>\n> for mac80211, we use the backports project and that follows a\n> different version than\n> what is used for linux.\n> If your intention is to propose this in OpenWrt, ideally all the\n> define flag should\n> be dropped and produce a more up-to-date driver with maybe 6.12 and 6.6 max.\n\nHi Ansuel,\n\nWhy 6.6? If main is using mac80211 linux-backports of 6.12 wouldn't I\nonly need to make sure its compatible with 6.12?\n\nThe out-of-tree driver I use is used for other kernels not just\nOpenWrt so my openwrt package is just a Makefile to build that shared\ndriver source against OpenWrt. Therefor there are lots of\ncompatibility defs to handle changes in mac80211 such as:\n#if KERNEL_VERSION(6, 7, 0) <= LINUX_VERSION_CODE\nstatic int nrc_post_channel_switch(struct ieee80211_hw *hw, struct\nieee80211_vif *vif, struct ieee80211_bss_conf *conf)\n#else\nstatic int nrc_post_channel_switch(struct ieee80211_hw *hw, struct\nieee80211_vif *vif)\n#endif\n\nThis allows the driver source to be compatible with a range of kernels\nas is done in many out-of-tree kernel drivers.\n\nSo what I'm trying to do is to understand how to use the same\nout-of-tree driver source with OpenWrt but the 'LINUX_VERSION_CODE' is\nthe kernel version (6.6) which is wrong and needs to be the version of\nthe mac80211 backport (6.12).\n\n>\n> But it really doesn't make sense to have IFDEF to support 2.x or 3.x...\n\nWhat do you mean by 2.x or 3.x or are you saying it doesn't make sense\nto use ifdef's at all? It does require compat ifdefs if I'm not trying\nto create multiple driver sources for different kernels.\n\n>\n> Also consider that mac80211 backports define have different config flag to\n> differentiate from kernel config (CPTCFG prefix)\n\nInteresting... but unfortunately I see nothing in the backports\n.config that shows the kernel version the backport is from.\n\nBest Regards,\n\nTim",
      "quoted_context_pairs": [
        {
          "quoted": "But it really doesn't make sense to have IFDEF to support 2.x or 3.x...",
          "response": "What do you mean by 2.x or 3.x or are you saying it doesn't make sense\nto use ifdef's at all? It does require compat ifdefs if I'm not trying\nto create multiple driver sources for different kernels.",
          "line_index": 60
        }
      ],
      "mentioned_files": [],
      "mentioned_commits": [],
      "keyword_matches": [
        "Makefile",
        "out[-.\\s]of[-.\\s]tree",
        "static",
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
        "uci-config",
        "kernel-driver",
        "patch-maintenance",
        "package-packaging"
      ],
      "has_patch_subject": false,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 3,
  "author_count": 2,
  "date_range": [
    "2025-01-28T16:37:35-08:00",
    "2025-01-31T11:56:01-08:00"
  ],
  "all_mentioned_files": [],
  "all_mentioned_commits": [],
  "categories": [
    "build-system",
    "kernel-driver",
    "package-packaging",
    "uci-config",
    "patch-maintenance"
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
  "source_refs": [
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "message_id": "<CAJ+vNU1wTQ=3KL54WgSyqEGMgXB12xMQ3VGCk1sSzOwxQq=xqQ@mail.gmail.com>",
      "byte_offset": 517205
    },
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "message_id": "<CA+_ehUwNTa7_EaFJDynRTPyNvuJ0cTaNk5o1+HP=q0G+N31H4w@mail.gmail.com>",
      "byte_offset": 526978
    },
    {
      "source_file": "devel/2025-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2025-January.txt",
      "message_id": "<CAJ+vNU1f2uh2733DzowG9ZgjjYNrk+KF6t9v3YUDuqypHu0+uA@mail.gmail.com>",
      "byte_offset": 537622
    }
  ],
  "score": 0.9
}
```

## Sample 8

```json
{
  "thread_id": "<20220208132830.914-1-rsalvaterra@gmail.com>",
  "subject": "[PATCH] update_kernel.sh: fix unified version file updates",
  "messages": [
    {
      "source_file": "devel/2022-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2022-February.txt",
      "byte_offset": 416498,
      "mbox_from_line": "From rsalvaterra at gmail.com  Tue Feb  8 05:28:30 2022",
      "message_id": "<20220208132830.914-1-rsalvaterra@gmail.com>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "rsalvaterra@gmail.com",
      "from_name": "",
      "date_raw": "Tue, 08 Feb 2022 13:28:30 +0000",
      "date_iso": "2022-02-08T13:28:30+00:00",
      "subject": "[PATCH] update_kernel.sh: fix unified version file updates",
      "body_for_scoring": "The previous commit broke the kernel-version.mk automated update, since the\nkernel version files are now split. However, older branches still use the\nunified file, so compatibility must be kept.\n\nCheck for the presence of the kernel version-specific file. If it doesn't exist,\nassume we're using the unified file and do the version update accordingly.\n\nFixes: cbb9d08 (\"update_kernel.sh: update it to new kernel hash/version file way\")\n\nSigned-off-by: Rui Salvaterra <rsalvaterra at gmail.com>\n---\n update_kernel.sh | 10 +++++++++-\n 1 file changed, 9 insertions(+), 1 deletion(-)\n\n[diff: update_kernel.sh]\n[hunk: if [ \"$UPDATE\" -eq 1 ]; then]\n-\t$CMD ./staging_dir/host/bin/sed -i include/kernel-${KERNEL} \\\n+\tif [ -f include/kernel-${KERNEL} ]; then\n+\t\t# split version files\n+\t\tKERNEL_VERSION_FILE=include/kernel-${KERNEL}\n+\telse",
      "body_no_diff": "The previous commit broke the kernel-version.mk automated update, since the\nkernel version files are now split. However, older branches still use the\nunified file, so compatibility must be kept.\n\nCheck for the presence of the kernel version-specific file. If it doesn't exist,\nassume we're using the unified file and do the version update accordingly.\n\nFixes: cbb9d08 (\"update_kernel.sh: update it to new kernel hash/version file way\")\n\nSigned-off-by: Rui Salvaterra <rsalvaterra at gmail.com>\n---\n update_kernel.sh | 10 +++++++++-\n 1 file changed, 9 insertions(+), 1 deletion(-)\n\n[diff: update_kernel.sh]\n[hunk: if [ \"$UPDATE\" -eq 1 ]; then]\n-\t$CMD ./staging_dir/host/bin/sed -i include/kernel-${KERNEL} \\\n+\tif [ -f include/kernel-${KERNEL} ]; then\n+\t\t# split version files\n+\t\tKERNEL_VERSION_FILE=include/kernel-${KERNEL}\n+\telse",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "update_kernel.sh"
      ],
      "mentioned_commits": [
        "cbb9d08"
      ],
      "keyword_matches": [
        "Fixes:"
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
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2022-02-08T13:28:30+00:00",
    "2022-02-08T13:28:30+00:00"
  ],
  "all_mentioned_files": [
    "update_kernel.sh"
  ],
  "all_mentioned_commits": [
    "cbb9d08"
  ],
  "categories": [
    "kernel-driver"
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
  "source_refs": [
    {
      "source_file": "devel/2022-February.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2022-February.txt",
      "message_id": "<20220208132830.914-1-rsalvaterra@gmail.com>",
      "byte_offset": 416498
    }
  ],
  "score": 0.4
}
```

## Sample 9

```json
{
  "thread_id": "<20211102223532.3279626-1-dev@kresin.me>",
  "subject": "[PATCH] uboot-lantiq: danube: fix SPL boot",
  "messages": [
    {
      "source_file": "devel/2021-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt",
      "byte_offset": 72165,
      "mbox_from_line": "From dev at kresin.me  Tue Nov  2 15:35:32 2021",
      "message_id": "<20211102223532.3279626-1-dev@kresin.me>",
      "in_reply_to": null,
      "references": [],
      "from_addr": "dev@kresin.me",
      "from_name": "",
      "date_raw": "Tue, 02 Nov 2021 23:35:32 +0100",
      "date_iso": "2021-11-02T23:35:32+01:00",
      "subject": "[PATCH] uboot-lantiq: danube: fix SPL boot",
      "body_for_scoring": "On danube we only have 0x6800 bytes of usable SRAM. Everything behind\ncan't be written to and a SPL u-boot locks up during boot.\n\nSince it's a hard to debug issue and took me more than two years to fix\nit, I consider it worth to include fix albeit SPL u-boots are not build\nin OpenWrt.\n\nI faced the issue while trying to shrink the u-boot to 64K since some\nboard only have an u-boot partition of that size from the days ifx-uboot\nwas used.\n\nSigned-off-by: Mathias Kresin <dev at kresin.me>\n---\n ...0032-MIPS-lantiq-danube-fix-SPL-boot.patch | 33 +++++++++++++++++++\n 1 file changed, 33 insertions(+)\n create mode 100644 package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch\n\n[diff: package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch]\n+From 65f1f160139c2bac83650c9c7c4aee4e5fd74c7c Mon Sep 17 00:00:00 2001\n+From: Mathias Kresin <dev at kresin.me>\n+Date: Sun, 2 May 2021 02:03:05 +0200\n+Subject: [PATCH] MIPS: lantiq: danube: fix SPL boot\n+On danube we only have 0x6800 bytes of usable SRAM. Everything behind",
      "body_no_diff": "On danube we only have 0x6800 bytes of usable SRAM. Everything behind\ncan't be written to and a SPL u-boot locks up during boot.\n\nSince it's a hard to debug issue and took me more than two years to fix\nit, I consider it worth to include fix albeit SPL u-boots are not build\nin OpenWrt.\n\nI faced the issue while trying to shrink the u-boot to 64K since some\nboard only have an u-boot partition of that size from the days ifx-uboot\nwas used.\n\nSigned-off-by: Mathias Kresin <dev at kresin.me>\n---\n ...0032-MIPS-lantiq-danube-fix-SPL-boot.patch | 33 +++++++++++++++++++\n 1 file changed, 33 insertions(+)\n create mode 100644 package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch\n\n[diff: package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch]\n+From 65f1f160139c2bac83650c9c7c4aee4e5fd74c7c Mon Sep 17 00:00:00 2001\n+From: Mathias Kresin <dev at kresin.me>\n+Date: Sun, 2 May 2021 02:03:05 +0200\n+Subject: [PATCH] MIPS: lantiq: danube: fix SPL boot\n+On danube we only have 0x6800 bytes of usable SRAM. Everything behind",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch"
      ],
      "mentioned_commits": [],
      "keyword_matches": [
        "bug",
        "lock(?:ing)?"
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
        "concurrency"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    },
    {
      "source_file": "devel/2021-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt",
      "byte_offset": 93732,
      "mbox_from_line": "From daniel.schwierzeck at gmail.com  Wed Nov  3 06:54:58 2021",
      "message_id": "<d817a1b6342628478c0bac4844beb991d241d6c3.camel@gmail.com>",
      "in_reply_to": "<20211102223532.3279626-1-dev@kresin.me>",
      "references": [
        "<20211102223532.3279626-1-dev@kresin.me>"
      ],
      "from_addr": "daniel.schwierzeck@gmail.com",
      "from_name": "",
      "date_raw": "Wed, 03 Nov 2021 14:54:58 +0100",
      "date_iso": "2021-11-03T14:54:58+01:00",
      "subject": "[PATCH] uboot-lantiq: danube: fix SPL boot",
      "body_for_scoring": "Am Dienstag, dem 02.11.2021 um 23:35 +0100 schrieb Mathias Kresin:\n\nthis is not really documented in the datasheets, but 0x6800 would\ncorrespond to the PPE Shared Buffer size and seems to be correct.\n\n\nReviewed-by: Daniel Schwierzeck <daniel.schwierzeck at gmail.com>",
      "body_no_diff": "Am Dienstag, dem 02.11.2021 um 23:35 +0100 schrieb Mathias Kresin:\n> On danube we only have 0x6800 bytes of usable SRAM. Everything behind\n> can't be written to and a SPL u-boot locks up during boot.\n> \n> Since it's a hard to debug issue and took me more than two years to\n> fix\n> it, I consider it worth to include fix albeit SPL u-boots are not\n> build\n> in OpenWrt.\n> \n> I faced the issue while trying to shrink the u-boot to 64K since some\n> board only have an u-boot partition of that size from the days ifx-\n> uboot\n> was used.\n> \n> Signed-off-by: Mathias Kresin <dev at kresin.me>\n> ---\n>  ...0032-MIPS-lantiq-danube-fix-SPL-boot.patch | 33\n> +++++++++++++++++++\n>  1 file changed, 33 insertions(+)\n>  create mode 100644 package/boot/uboot-lantiq/patches/0032-MIPS-\n> lantiq-danube-fix-SPL-boot.patch\n> \n> diff --git a/package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-\n> danube-fix-SPL-boot.patch b/package/boot/uboot-lantiq/patches/0032-\n> MIPS-lantiq-danube-fix-SPL-boot.patch\n> new file mode 100644\n> index 0000000000..794fd8cc2a\n> --- /dev/null\n> +++ b/package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-\n> SPL-boot.patch\n> @@ -0,0 +1,33 @@\n> +From 65f1f160139c2bac83650c9c7c4aee4e5fd74c7c Mon Sep 17 00:00:00\n> 2001\n> +From: Mathias Kresin <dev at kresin.me>\n> +Date: Sun, 2 May 2021 02:03:05 +0200\n> +Subject: [PATCH] MIPS: lantiq: danube: fix SPL boot\n> +\n> +On danube we only have 0x6800 bytes of usable SRAM. Everything\n> behind\n> +can't be written to and a SPL u-boot locks up during boot.\n> +\n> +Signed-off-by: Mathias Kresin <dev at kresin.me>\n> +---\n> + arch/mips/include/asm/arch-danube/config.h | 4 ++--\n> + 1 file changed, 2 insertions(+), 2 deletions(-)\n> +\n> +--- a/arch/mips/include/asm/arch-danube/config.h\n> ++++ b/arch/mips/include/asm/arch-danube/config.h\n> +@@ -61,7 +61,7 @@\n> + \n> + /* SRAM */\n> + #define CONFIG_SYS_SRAM_BASE\t\t0xBE1A0000\n> +-#define CONFIG_SYS_SRAM_SIZE\t\t0x10000\n> ++#define CONFIG_SYS_SRAM_SIZE\t\t0x6800\n\nthis is not really documented in the datasheets, but 0x6800 would\ncorrespond to the PPE Shared Buffer size and seems to be correct.\n\n> + \n> + /* ASC/UART driver and console */\n> + #define CONFIG_LANTIQ_SERIAL\n> +@@ -117,7 +117,7 @@\n> + #define CONFIG_CMD_NET\n> + #endif\n> + \n> +-#define CONFIG_SPL_MAX_SIZE\t\t(32 * 1024)\n> ++#define CONFIG_SPL_MAX_SIZE\t\t(18 * 1024)\n> + #define CONFIG_SPL_BSS_MAX_SIZE\t\t(8 * 1024)\n> + #define CONFIG_SPL_STACK_MAX_SIZE\t(8 * 1024)\n> + #define CONFIG_SPL_MALLOC_MAX_SIZE\t(32 * 1024)\n\nReviewed-by: Daniel Schwierzeck <daniel.schwierzeck at gmail.com>",
      "quoted_context_pairs": [],
      "mentioned_files": [
        "include/asm/arch-danube/config.h"
      ],
      "mentioned_commits": [
        "0000000000",
        "794fd8cc2a"
      ],
      "keyword_matches": [
        "correct(?:ly)?"
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
        "memory-management",
        "concurrency",
        "build-system"
      ],
      "has_patch_subject": true,
      "has_keyword_match": true,
      "disposition": "primary"
    }
  ],
  "message_count": 2,
  "author_count": 2,
  "date_range": [
    "2021-11-02T23:35:32+01:00",
    "2021-11-03T14:54:58+01:00"
  ],
  "all_mentioned_files": [
    "include/asm/arch-danube/config.h",
    "package/boot/uboot-lantiq/patches/0032-MIPS-lantiq-danube-fix-SPL-boot.patch"
  ],
  "all_mentioned_commits": [
    "0000000000",
    "794fd8cc2a"
  ],
  "categories": [
    "concurrency",
    "memory-management",
    "build-system"
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
  "source_refs": [
    {
      "source_file": "devel/2021-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt",
      "message_id": "<20211102223532.3279626-1-dev@kresin.me>",
      "byte_offset": 72165
    },
    {
      "source_file": "devel/2021-November.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-devel/2021-November.txt",
      "message_id": "<d817a1b6342628478c0bac4844beb991d241d6c3.camel@gmail.com>",
      "byte_offset": 93732
    }
  ],
  "score": 0.95
}
```

## Sample 10

```json
{
  "thread_id": "<mailman.32539.1642932557.1923571.openwrt-bugs@lists.openwrt.org>",
  "subject": "[FS#4229] MT7621 Wireless default error",
  "messages": [
    {
      "source_file": "bugs/2022-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2022-January.txt",
      "byte_offset": 164407,
      "mbox_from_line": "From openwrt-bugs at lists.openwrt.org  Sun Jan 23 02:09:10 2022",
      "message_id": "<mailman.32539.1642932557.1923571.openwrt-bugs@lists.openwrt.org>",
      "in_reply_to": "<FS4229@bugs.openwrt.org>",
      "references": [
        "<FS4229@bugs.openwrt.org>"
      ],
      "from_addr": "openwrt-bugs@lists.openwrt.org",
      "from_name": "",
      "date_raw": "Sun, 23 Jan 2022 10:09:10 +0000",
      "date_iso": "2022-01-23T10:09:10+00:00",
      "subject": "[FS#4229] MT7621 Wireless default error",
      "body_for_scoring": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#4229 - MT7621 Wireless default error\nUser who did this - nicefile (nicefile)\n\n----------\nplease post output from command\niw phy\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4229#comment10474\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
      "body_no_diff": "THIS IS AN AUTOMATED MESSAGE, DO NOT REPLY.\n\nThe following task has a new comment added:\n\nFS#4229 - MT7621 Wireless default error\nUser who did this - nicefile (nicefile)\n\n----------\nplease post output from command\niw phy\n----------\n\nMore information can be found at the following URL:\nhttps://bugs.openwrt.org/index.php?do=details&task_id=4229#comment10474\n\nYou are receiving this message because you have requested it from the Flyspray bugtracking system.  If you did not expect this message or don't want to receive mails in future, you can change your notification settings at the URL shown above.",
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
  ],
  "message_count": 1,
  "author_count": 1,
  "date_range": [
    "2022-01-23T10:09:10+00:00",
    "2022-01-23T10:09:10+00:00"
  ],
  "all_mentioned_files": [],
  "all_mentioned_commits": [],
  "categories": [
    "uncategorized"
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
  "source_refs": [
    {
      "source_file": "bugs/2022-January.txt",
      "archive_url": "https://lists.openwrt.org/pipermail/openwrt-bugs/2022-January.txt",
      "message_id": "<mailman.32539.1642932557.1923571.openwrt-bugs@lists.openwrt.org>",
      "byte_offset": 164407
    }
  ],
  "score": 0.65
}
```
