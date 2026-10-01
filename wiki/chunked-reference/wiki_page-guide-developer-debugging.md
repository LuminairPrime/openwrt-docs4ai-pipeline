---
title: Debugging
module: wiki
origin_type: wiki_page
token_count: 1962
source_file: L1-raw/wiki/wiki_page-guide-developer-debugging.md
last_pipeline_run: '2026-10-01T18:43:26.586825+00:00'
source_url: https://openwrt.org/docs/guide-developer/debugging
language: text
ai_summary: The Debugging module in OpenWrt provides essential tools and techniques for diagnosing issues related to hardware, kernel, and driver development. It covers methods such as adding a serial console, utilizing JTAG for debugging, and employing GDB for code analysis. Additionally, it offers guidance on capturing wireless management traffic using tools like tcpdump and iwcap, as well as adjusting the logging level for hostapd to facilitate troubleshooting. These resources are crucial for developers working on embedded network devices to effectively identify and resolve issues.
ai_when_to_use: Use this module when developing or debugging drivers and kernel code on OpenWrt devices, especially when dealing with wireless connectivity issues.
ai_related_topics:
- port.serial
- port.jtag
- gdb
---

> **Source:** [https://openwrt.org/docs/guide-developer/debugging](https://openwrt.org/docs/guide-developer/debugging)
> **Kind:** wiki_page | **Method:** scraped
> **Normalized:** 2026-10-01

# Debugging

Debugging hardware can be tricky especially when doing kernel and driver development. It might become handy for you to add serial console to your device as well as using JTAG to debug your code.

## Serial Port

-\> [port.serial](/docs/techref/hardware/port.serial)

## JTAG

-\> [port.jtag](/docs/techref/hardware/port.jtag)

## GDB

:!: -\> [gdb](/docs/guide-developer/gdb) a very short introduction on the GNU Debugger

## CPU Profiling perf/oprofile

-\> <http://false.ekta.is/2012/11/cpu-profiling-applications-on-openwrt-with-perf-or-oprofile/>

## Wireless

When encountering wireless bugs, such as connection drop or WPA rekeying issues, it is possible to remotely run `tcpdump` in order to capture wireless management traffic for later analysis of the communication leading to the problem.

### Capture Management Traffic

The command below will spawn a monitor interface with a mac80211 based driver, start `tcpdump` and save the captured data locally into `/tmp`:

``` bash
ssh root@192.168.1.1 'grep -q mon0 /proc/net/dev || /usr/sbin/iw phy phy0 interface add mon0 type monitor;
    /sbin/ifconfig mon0 up; /usr/sbin/tcpdump -s 0 -i mon0 -y IEEE802_11_RADIO -w -' > /tmp/wifi.pcap
```

A smaller alternative to `tcpdump` is the `iwcap` utility. It's a MIPS binary only ~5KB and does not require `libpcap` to function. It also supports the filtering of data frames through the `-D` switch to cut down the amount of captured traffic.

``` bash
ssh root@192.168.1.1 'grep -q mon0 /proc/net/dev || /usr/sbin/iw phy phy0 interface add mon0 type monitor;
    /sbin/ifconfig mon0 up; /usr/sbin/iwcap -i mon0 -s' > /tmp/wifi.pcap
```

### Logging hostapd behaviour

OpenWrt ships with a version of hostapd which has verbose debug messages disabled in order to save space (see <https://dev.openwrt.org/ticket/15658>). Set "minimum debug message priority" in menuconfig to 0 to have all log levels available for debugging.

To enable debug, first remove the cut-down version, then install the debug build of hostapd which is contained in the wpad package:

``` bash
apk del wpad-mini
apk -U add wpad
```

Below are the common logging levels.

``` bash
Levels (minimum value for logged events):
0 = verbose debugging
1 = debugging
2 = informational messages
3 = notification
4 = warning
```

The default is 2 for "informational messages". The example below shows you how to change check this and change it to "debugging".

Check the log level currently being used:

``` bash
root@OpenWrt:~# ps | grep hostapd
 6948 root      1784 S    /usr/sbin/hostapd -P /var/run/wifi-phy1.pid -B /var/run/hostapd-phy1.conf
 6987 root      1784 S    /usr/sbin/hostapd -P /var/run/wifi-phy0.pid -B /var/run/hostapd-phy0.conf
 7019 root      1448 S    grep hostapd
```

Lets say you're interested in addressing a problem with the phy0 hostapd. First check the current level for this hostapd:

``` bash
root@OpenWrt:~# grep _level /var/run/hostapd-phy0.conf
logger_syslog_level=2
logger_stdout_level=2
```

Here we see that log level 2 is selected. Let's change this to 1 which is debug:

``` bash
root@OpenWrt:~# uci set wireless.radio0.log_level=1
root@OpenWrt:~# uci commit wireless
root@OpenWrt:~# wifi up
root@OpenWrt:~# grep _level /var/run/hostapd-phy0.conf
logger_syslog_level=1
logger_stdout_level=1
```

Now the level has been changed. Enter `logread -f` command to monitor debug messages on the console like those below:

``` bash
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 MLME: MLME-REASSOCIATE.indication(20:16:d8:db:aa:56)
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 MLME: MLME-DELETEKEYS.request(20:16:d8:db:aa:56)
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: event 1 notification
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: start authentication
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 IEEE 802.1X: unauthorizing port
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: sending 1/4 msg of 4-Way Handshake
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: received EAPOL-Key frame (2/4 Pairwise)
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: sending 3/4 msg of 4-Way Handshake
Tue Apr 22 11:35:41 2014 daemon.debug hostapd: wlan0: STA 20:16:d8:db:aa:56 WPA: received EAPOL-Key frame (4/4 Pairwise)
```

See [log.essentials](/docs/guide-user/base-system/log.essentials) for more information about logging.

You may want to setup remote logging via syslog to another computer by setting a logfile (warning: this won't be auto-rotated, so make sure it doesn't fill up a vital filesystem).

``` bash
uci set system.@system[0].log_file=[path-to-my-logfile]
uci commit
[reboot required]
```

Or alternatively, it might be better to use system.@system\[0\].log_ip to log to a remote machine (which must be running an appropriate listener e.g. rsyslogd - see <https://forum.openwrt.org/viewtopic.php?id=11912>).

If you wish to debug on the command line instead, you may use a command like this:

``` bash
kill `cat /var/run/wifi-phy0.pid` ; /usr/sbin/hostapd -dd -P /var/run/wifi-phy0.pid  /var/run/hostapd-phy0.conf
```

Use the output of `ps` above to create the necessary command line, remove the '-B' argument to stop hostapd forking into the background, and add '-dd' to verbose debug to stdout.

Depending on your hardware and interface state, it may be necessary to create or re-create the relevant wlan device before starting hostapd:

``` bash
iw dev wlan0 del
iw phy phy0 interface add wlan0 type managed
```

## Add and modify compiler debug flags

The "Compile with debug" entry in advanced developer menu enables "-g3" compile option.

You have to disable \_sstrip\_ to keep debug information.

If you just want to build a single package unstripped, try, "make package/foo/compile STRIP=true". Unstripped binaries are placed in "staging_dir/target-\*/root-\*/" where your host side tools can use them. Remember, gdbserver can attach to the stripped binary, while gdb loads the unstripped binary. See [gdb](/docs/guide-developer/gdb).

Alternatively you can add or modify "Custom Target Options" like add "-g3 -ggdb3".

Be aware there are default compiler options defined in include/[target.mk](../../openwrt-core/chunked-reference/makefile_meta-include-mk.md) for example ("-Os -pipe").

Some packets might overwrite or not use the flags. Check your compile log.

Additional tips:

- Check with different GCC versions
- There is "-O0" to disable compiler optimizations
- "-Wall -Wextra" might provide useful warnings
- See <https://gcc.gnu.org/bugs/>
