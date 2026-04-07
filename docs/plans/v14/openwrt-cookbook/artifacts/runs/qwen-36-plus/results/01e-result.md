# OpenWrt Development Test Results

---

## Scenario 26

Write an OpenWrt shell snippet that sources the native shell JSON helper, loads a JSON string from `$payload`, enters the `network` object, reads the `proto` and `device` fields, then navigates back out cleanly.

```sh
#!/bin/sh
# Source the native JSON helper for shell
. /usr/share/libubox/jshn.sh

# payload contains JSON string like: {"network": {"proto": "dhcp", "device": "eth0"}}
payload='{"network": {"proto": "dhcp", "device": "eth0"}}'

# Load JSON string into jshn variables
json_load "$payload"

# Enter the "network" object
json_select network

# Read the "proto" field
json_get_var proto "proto"

# Read the "device" field  
json_get_var device "device"

# Cleanly navigate back out to root
json_select ..

# Output the extracted values
echo "Protocol: $proto"
echo "Device: $device"
```

Key functions used:
- `json_load` - Parse a JSON string into jshn shell variables
- `json_select` - Navigate into a JSON object (`.` goes back to root)
- `json_get_var` - Extract a variable value from current object level

---

## Scenario 27

Write a LuCI/OpenWrt JS snippet that calls the runtime network-interface dump over ubus and extracts the first non-loopback IPv4 address for the `lan` interface from the returned data structure.

```javascript
// LuCI JavaScript (typically in /usr/lib/lua/luci/controller/ or view)

var ubus = require("ubus");
var conn = ubus.connect();

if (!conn) {
    throw "Cannot connect to ubus";
}

// Call network.interface dump
var network_dump = conn.call("network.interface", "dump", {});

// Find the lan interface
var lan_interface = null;
for (var i = 0; i < network_dump.interface.length; i++) {
    var iface = network_dump.interface[i];
    if (iface.interface === "lan") {
        lan_interface = iface;
        break;
    }
}

// Extract first non-loopback IPv4 address
var ipv4_address = null;
if (lan_interface && lan_interface["ipv4-address"]) {
    var ipv4_list = lan_interface["ipv4-address"];
    for (var j = 0; j < ipv4_list.length; j++) {
        var addr = ipv4_list[j];
        // Skip loopback addresses (127.0.0.0/8)
        if (addr.address !== "127.0.0.1" && !addr.address.startsWith("127.")) {
            ipv4_address = addr.address + "/" + addr.mask;
            break;
        }
    }
}

if (ipv4_address) {
    print("LAN IPv4 Address: " + ipv4_address);
} else {
    print("No non-loopback IPv4 address found for lan interface");
}
```

The ubus call returns a structure like:
```json
{
  "interface": [
    {
      "interface": "lan",
      "ipv4-address": [
        { "address": "192.168.1.1", "mask": 24, ... }
      ],
      ...
    }
  ]
}
```

---

## Scenario 17

**What is OpenWrt ucode, why was it created, and what is it good for?**

### What is OpenWrt ucode?

**ucode** is a lightweight, embeddable scripting language developed specifically for OpenWrt. It features a JavaScript-like syntax that compiles to compact C data structures, allowing developers to write programs that run with minimal memory overhead on resource-constrained embedded devices.

### Why was it created?

ucode was created to address several pain points in OpenWrt development:

1. **Memory constraints**: Traditional scripting solutions (Python, Lua, full JavaScript engines) consumed too much RAM and flash storage on typical OpenWrt devices.

2. **Shell script limitations**: Complex logic in shell scripts (ash/bash) is fragile, slow, and difficult to maintain. Shell handling of variables and data structures is primitive.

3. **uci configuration complexity**: Interacting with UCI configuration system from shell required awkward parsing and didn't integrate cleanly with JSON data from ubus.

4. **JSON handling**: Shell scripts lacked native JSON support for working with ubus (which uses JSON-RPC).

5. **Replacement for procd scripting**: OpenWrt's procd init system needed a more capable scripting language for service management and hotplug handlers.

### What is it good for?

ucode excels at:

- **UCI configuration management**: Clean API for reading/writing UCI config files
- **ubus RPC interaction**: Simple syntax for calling ubus methods and handling responses
- **JSON processing**: Native JSON parsing and manipulation without external dependencies
- **Hotplug handlers**: More reliable than shell for responding to device events
- **Service initialization**: Init scripts that need conditional logic and external command execution
- **Lightweight daemons**: Writing simple network services with minimal footprint
- **Prototyping**: Quick development cycle since ucode files don't require compilation

### Example advantages over shell:

```sh
# Shell approach - awkward and error-prone
. /usr/share/libubox/jshn.sh
json_load "$(ubus call network.interface.lan status)"
json_select "ipv4-address"
json_get_var addr address

# ucode approach - clean and direct
let ubus = require("ubus");
let conn = ubus.connect();
let status = conn.call("network.interface.lan", "status", {});
let addr = status["ipv4-address"][0].address;
```

---

## Scenario 13

Write an OpenWrt script snippet that safely reads an external JSON file from `/etc/my_app/config.json`, parses the data natively, and prints the value of the `startup_delay` key.

```sh
#!/bin/sh

CONFIG_FILE="/etc/my_app/config.json"

# Check file exists and is readable
if [ ! -f "$CONFIG_FILE" ] || [ ! -r "$CONFIG_FILE" ]; then
    echo "Error: Config file not found or not readable: $CONFIG_FILE" >&2
    exit 1
fi

# Verify it's actually JSON (basic sanity check)
if ! head -c 1 "$CONFIG_FILE" 2>/dev/null | grep -qE '^\[|^\{'; then
    echo "Error: Config file does not appear to be valid JSON" >&2
    exit 1
fi

# Source the JSON helper
. /usr/share/libubox/jshn.sh

# Clear any previous JSON state
json_cleanup 2>/dev/null

# Load the JSON file content
json_load "$(cat "$CONFIG_FILE")"

# Extract the startup_delay value
json_get_var startup_delay "startup_delay"

# Clean up JSON state
json_cleanup

# Print the result
if [ -n "$startup_delay" ]; then
    echo "startup_delay: $startup_delay"
else
    echo "Error: startup_delay key not found in config" >&2
    exit 1
fi
```

### Alternative using jsonfilter (more concise):

```sh
#!/bin/sh

CONFIG_FILE="/etc/my_app/config.json"

if [ ! -f "$CONFIG_FILE" ] || [ ! -r "$CONFIG_FILE" ]; then
    echo "Error: Config file not found" >&2
    exit 1
fi

startup_delay=$(jsonfilter -i "$CONFIG_FILE" -e '@.startup_delay')

if [ -n "$startup_delay" ]; then
    echo "startup_delay: $startup_delay"
else
    echo "Error: startup_delay not found" >&2
    exit 1
fi
```

### Alternative using ucode (modern approach):

```sh
#!/usr/bin/ucode

import "fs";
import "uci";

const config_path = "/etc/my_app/config.json";

let config_content = fs.read(config_path);
if (!config_content) {
    printf("Error: Cannot read config file\n");
    return 1;
}

let config = json_parse(config_content);
if (!config) {
    printf("Error: Invalid JSON in config file\n");
    return 1;
}

if (config.startup_delay !== undefined) {
    printf("startup_delay: %s\n", config.startup_delay);
} else {
    printf("Error: startup_delay key not found\n");
    return 1;
}
```

---

## Scenario 14

Write the modern OpenWrt LuCI menu definition snippet (JSON format) required to register a new menu tab under 'Network' called 'My Tool' that renders a specific Javascript view.

### Menu Definition (in /etc/config/luci or application section):

```json
{
  "network": {
    "title": "Network",
    "order": 30,
    "items": {
      "mytool": {
        "title": "My Tool",
        "order": 10,
        "view": "myapp/mytool"
      }
    }
  }
}
```

### Alternative: Application-driven registration (recommended approach)

Create `/usr/lib/lua/luci/controller/myapp.lua`:
```lua
module("luci.controller.myapp", package.seeall)

function index()
    entry({"admin", "network", "mytool"},
         template("myapp/mytool"),
         "My Tool",
         10)
end
```

Create `/usr/lib/lua/luci/view/myapp/mytool.htm`:
```html
<%+header%>
<div class="cbi-map">
    <h2><%:My Tool%></h2>
    <div id="myapp-content">
        <p>Loading...</p>
    </div>
</div>
<script>
    // Call ubus or perform AJAX actions
    ubus.call('myapp', 'status', {}, function(data) {
        document.getElementById('myapp-content').innerHTML = 
            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    });
</script>
<%+footer%>
```

### Combined JSON menu entry format:

```json
{
  "admin": {
    "Network": [
      {
        "id": "admin-network-mytool",
        "title": "My Tool",
        "action": {
          "type": "view",
          "path": "myapp/mytool"
        },
        "order": 50,
        "depends": {
          "acl": ["luci-app-myapp"]
        }
      }
    ]
  }
}
```

The key components are:
- `admin` - Top-level admin section
- `Network` - Parent menu (creates "Network" tab)
- `id` - Unique identifier for the menu entry
- `title` - Display text shown in menu
- `action.path` - Points to the view file in `/usr/lib/lua/luci/view/`
- `order` - Position within parent menu

---

## Scenario 19

Write an OpenWrt hotplug script snippet that reacts only when the `wan` interface comes up, builds a structured JSON payload from the hotplug environment, and forwards it to a ubus method.

### Hotplug script location and format:

Create `/etc/hotplug.d/iface/30-wan-notify`:
```sh
#!/bin/sh

# Only react to wan interface coming up
if [ "$ACTION" != "ifup" ] || [ "$INTERFACE" != "wan" ]; then
    exit 0
fi

# Source the JSON helper
. /usr/share/libubox/jshn.sh

# Build structured JSON payload from hotplug environment
json_init
json_add_string "action" "$ACTION"
json_add_string "interface" "$INTERFACE"
json_add_string "device" "$DEVICE"
json_add_string "logical_device" "$LOGICALDEVICE"
json_add_string "proto" "$PROTO"

# Add timestamp
json_add_string "timestamp" "$(date -Iseconds)"

# Add IP information if available
if [ -n "$IPADDR" ]; then
    json_add_string "ipaddr" "$IPADDR"
fi
if [ -n "$SUBNET" ]; then
    json_add_string "subnet" "$SUBNET"
fi
if [ -n "$GATEWAY" ]; then
    json_add_string "gateway" "$GATEWAY"
fi

# Get the generated JSON string
NOTIFY_JSON=$(json_dump)

# Forward to ubus method
ubus call myapp wan_event "${NOTIFY_JSON}"

# Cleanup
json_cleanup

# Log for debugging
logger -t hotplug-wan "Forwarded wan up event to ubus: $NOTIFY_JSON"
```

### Alternative using ucode (cleaner approach):

Create `/etc/hotplug.d/iface/30-wan-notify.ucode`:
```sh
#!/usr/bin/ucode

// Only react to wan interface coming up
if (ENV.ACTION !== "ifup" || ENV.INTERFACE !== "wan") {
    return 0;
}

import "ubus";

let conn = ubus.connect();
if (!conn) {
    warn("Cannot connect to ubus\n");
    return 1;
}

// Build structured payload from hotplug environment
let payload = {
    action: ENV.ACTION,
    interface: ENV.INTERFACE,
    device: ENV.DEVICE,
    logical_device: ENV.LOGICALDEVICE,
    proto: ENV.PROTO,
    timestamp: date('%Y-%m-%dT%H:%M:%S%z'),
};

// Add IP info if available
if (ENV.IPADDR) {
    payload.ipaddr = ENV.IPADDR;
}
if (ENV.GATEWAY) {
    payload.gateway = ENV.GATEWAY;
}

// Forward to ubus method
try {
    conn.call("myapp", "wan_event", payload);
    printf("Forwarded wan event to myapp.wan_event\n");
} catch (err) {
    warn(`Failed to call ubus: ${err}\n`);
}

conn.close();
```

### Hotplug environment variables available:

| Variable | Description |
|----------|-------------|
| `ACTION` | Event type (ifup, ifdown, update) |
| `INTERFACE` | Interface name from UCI (e.g., "wan") |
| `DEVICE` | Physical device (e.g., "eth1") |
| `LOGICALDEVICE` | Logical device name |
| `PROTO` | Protocol (dhcp, static, pppoe) |
| `IPADDR` | Assigned IP address |
| `SUBNET` | Subnet mask |
| `GATEWAY` | Default gateway |
| `INTERFACE` | Interface name |

The script ensures:
1. Only runs for `wan` interface `ifup` events
2. Builds clean JSON from environment variables
3. Forwards to custom ubus method `myapp.wan_event`
4. Proper cleanup and logging
