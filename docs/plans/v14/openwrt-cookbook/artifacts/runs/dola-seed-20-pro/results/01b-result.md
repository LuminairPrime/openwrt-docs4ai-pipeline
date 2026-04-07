---

### Scenario 02
```sh
#!/bin/sh
# OpenWrt standard network interface enumeration using official ubus API

. /lib/functions.sh
. /usr/share/libubox/jshn.sh

json_init
json_add_string "timestamp" "$(date -Iseconds)"
json_add_string "system" "$(ubus call system board | jsonfilter -e '@.release.description')"
json_add_array "interfaces"

for iface in $(ubus list network.interface.* | cut -d. -f3); do
    status=$(ubus call network.interface."$iface" status)
    if [ "$(jsonfilter -s "$status" -e '@.up')" = "true" ]; then
        json_add_object
        json_add_string "interface" "$iface"
        json_add_string "device" "$(jsonfilter -s "$status" -e '@.device')"
        json_add_string "ipv4_address" "$(jsonfilter -s "$status" -e '@.ipv4-address[0].address')"
        json_add_string "ipv4_netmask" "$(jsonfilter -s "$status" -e '@.ipv4-address[0].mask')"
        json_add_string "mac" "$(jsonfilter -s "$status" -e '@.macaddr')"
        json_close_object
    fi
done

json_close_array
json_dump
```

**Explanation:** Uses native OpenWrt ubus, libubox jshn and jsonfilter utilities which are present on all standard installations. Avoids parsing legacy `ifconfig`/`ip` output which is unreliable across OpenWrt versions.

---

### Scenario 06
```sh
validate_loglevel() {
    local loglevel

    # Read uci config properly using OpenWrt config API
    config_load myservice
    config_get loglevel general loglevel 3

    # Validate integer range 0-7 (standard syslog levels)
    if ! [ "$loglevel" -eq "$loglevel" ] 2>/dev/null; then
        echo "ERROR: loglevel must be an integer" >&2
        return 1
    fi

    if [ "$loglevel" -lt 0 ] || [ "$loglevel" -gt 7 ]; then
        echo "ERROR: loglevel must be between 0 and 7" >&2
        return 1
    fi

    return 0
}

# Usage in init script start routine
start() {
    validate_loglevel || exit 1
    service_start /usr/sbin/myservice -l "$loglevel"
}
```

**Explanation:** Follows OpenWrt init script conventions using the official `config_load` / `config_get` API. Uses arithmetic comparison to safely validate integer type, checks valid syslog level range as used system-wide in OpenWrt.

---

### Scenario 09
```sh
#!/bin/sh
# Place this file at: /etc/hotplug.d/iface/99-restart-firewall-wan-up

[ "$ACTION" = "ifup" ] || exit 0
[ "$INTERFACE" = "wan" ] || exit 0

logger -t hotplug "WAN interface came up, restarting firewall service"

# Use official service control, never call init scripts directly
service firewall restart

exit 0
```

**Explanation:** This is an OpenWrt hotplug script, the official supported mechanism for system interface events. Hotplug executes all scripts in this directory automatically on interface state changes with standard environment variables. Uses the `service` wrapper for correct service lifecycle management.