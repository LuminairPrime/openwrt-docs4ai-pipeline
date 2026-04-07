# Result for 01e.md

## Scenario 13

To safely read and parse a JSON file using `jsonfilter` in an OpenWrt shell script:

```bash
#!/bin/sh

# Safely read and parse the startup_delay from a JSON file
config_file="/etc/my_app/config.json"

if [ -f "$config_file" ]; then
    startup_delay=$(jsonfilter -i "$config_file" -e "@.startup_delay")
    if [ -n "$startup_delay" ]; then
        echo "The startup_delay is: $startup_delay"
    else
        echo "Key 'startup_delay' not found in $config_file"
    fi
else
    echo "Config file not found."
fi
```

## Scenario 14

The modern LuCI menu definition in JSON format to be placed in `/usr/share/luci/menu.d/my_tool.json`:

```json
{
	"admin/network/my_tool": {
		"title": "My Tool",
		"order": 90,
		"action": {
			"type": "view",
			"path": "my_package/my_tool_view"
		}
	}
}
```

## Scenario 19

A hotplug script that builds a JSON payload and forwards it to ubus:

```bash
#!/bin/sh

# Hotplug script: /etc/hotplug.d/iface/90-wan-notify
# React only to 'wan' coming up
[ "$INTERFACE" = "wan" ] || exit 0
[ "$ACTION" = "ifup" ] || exit 0

# Build a JSON payload using the environment variables provided by hotplug
payload=$(printf '{"interface":"%s", "device":"%s", "action":"%s", "timestamp":"%s"}' \
    "$INTERFACE" "$DEVICE" "$ACTION" "$(date +%s)")

# Forward the payload to a specific ubus method
ubus call my_service report_event "$payload"
```
