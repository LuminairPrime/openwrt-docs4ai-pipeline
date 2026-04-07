---

### Scenario 13
```sh
#!/bin/sh
. /usr/share/libubox/jshn.sh

CONFIG_FILE="/etc/my_app/config.json"

[ -f "$CONFIG_FILE" ] || exit 1

json_init
json_load "$(cat "$CONFIG_FILE")"

if json_get_var delay startup_delay; then
    printf "%s\n" "$delay"
else
    exit 1
fi
```
Uses the native `jshn` library shipped by default on all OpenWrt systems. No external dependencies, properly validates file existence and key presence. This is the standard supported method - avoid `jq` or external parsers for base system scripts.

---

### Scenario 14
File location: `/usr/share/luci/menu.d/99-mytool.json`
```json
{
  "admin/network/mytool": {
    "title": "My Tool",
    "order": 75,
    "action": {
      "type": "view",
      "path": "mytool/overview"
    },
    "depends": {
      "acl": [ "luci-app-mytool" ]
    }
  }
}
```
This is the modern LuCI menu definition format introduced in OpenWrt 21.02, replacing the legacy Lua menu API. Order 75 places the entry after Firewall / before Diagnostics in the standard Network menu.

---

### Scenario 19
File location: `/etc/hotplug.d/iface/99-my-wan-monitor`
```sh
#!/bin/sh
. /usr/share/libubox/jshn.sh

[ "$ACTION" = "ifup" ] || exit 0
[ "$INTERFACE" = "wan" ] || exit 0

json_init
json_add_string "action" "$ACTION"
json_add_string "interface" "$INTERFACE"
json_add_string "device" "$DEVICE"
json_add_string "ip4_address" "$IPADDR"
json_add_string "ip4_gateway" "$GATEWAY"

ubus call my.app notify_wan_up "$(json_dump)"
```
Proper hotplug filtering, uses native jshn for safe JSON construction (avoids escaping bugs), correctly forwards structured data over ubus. All environment variables shown are standard hotplug interface variables.