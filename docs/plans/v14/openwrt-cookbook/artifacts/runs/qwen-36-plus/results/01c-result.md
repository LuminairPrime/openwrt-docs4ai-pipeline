## Scenario 26
```sh
# Source the native shell JSON helper
. /usr/share/libubox/jshn.sh

# Load JSON string from $payload
loadjson "$payload"

# Enter the network object
json_select network

# Read the proto and device fields
json_get_var proto proto
json_get_var device device

# Navigate back out cleanly
json_select ..
json_select ..
```

## Scenario 27
```javascript
// Assuming this runs in a LuCI context with ubus available
function getLanIPv4() {
    // Call runtime network-interface dump over ubus
    ubus.call("network.interface", "dump", {}, function(data) {
        // Extract the first non-loopback IPv4 address for the lan interface
        if (data && data.interfaces) {
            for (let i = 0; i < data.interfaces.length; i++) {
                const iface = data.interfaces[i];
                if (iface.interface === "lan" && iface.ipv4_addr) {
                    // Check if it's non-loopback (not 127.0.0.1/8)
                    const ip = iface.ipv4_addr[0].address;
                    if (!ip.startsWith("127.")) {
                        return ip;
                    }
                }
            }
        }
        return null; // No suitable address found
    });
}
```

## Scenario 17
OpenWrt ucode is an embedded interpreter designed for OpenWrt that implements a subset of C and JavaScript-like syntax. It was created to provide a lightweight, safe, and efficient way to write system scripts and configuration handlers directly on embedded routers with limited resources. Ucode is good for writing system daemons, network configuration scripts, and event handlers that need to interact with OpenWrt's ubus system and configuration files, offering better performance than traditional shell scripts while being safer than executing arbitrary code.

## Scenario 07
```c
#include <libubox/blobmsg_json.h>
#include <ubus.h>

static int
handle_status(struct ubus_context *ctx, struct ubus_object *obj,
              struct ubus_request_data *req, const char *method,
              struct blob_attr *msg)
{
    struct blob_buf b = {};
    blob_buf_init(&b, 0);
    blobmsg_add_json_from_string(&b, '{"status": "ok"}');
    ubus_send_reply(ctx, req, b.head);
    return 0;
}

// In your object definition:
// { "status", handle_status, NULL },
```

## Scenario 05
```lua
-- Assuming this is a LuCI view file (.htm or .lua)
<html>
<body>
<h2>Connected WiFi Clients</h2>
<table border="1">
<tr><th>MAC Address</th></tr>
<% 
local ubus = require "ubus"
local conn = ubus.connect()
if not conn then
    print("<tr><td>Failed to connect to ubus</td></tr>")
else
    local function get_wifi_clients()
        local clients = {}
        conn:call("hostapd", "get_clients", {}, function(code, data)
            if code == 0 and data then
                for mac, info in pairs(data) do
                    table.insert(clients, mac)
                end
            end
        end)
        ubus.complete(conn, 1000) -- Wait 1 second for response
        return clients
    end
    
    local clients = get_wifi_clients()
    for _, mac in ipairs(clients) do
        print(string.format("<tr><td>%s</td></tr>", mac))
    end
    conn:close()
end
%>
</table>
</body>
</html>
```

## Scenario 10
```sh
#!/bin/sh
# OpenWrt first boot script to set timezone to UTC

# Set timezone to UTC
uci set system.@system[0].timezone='UTC'

# Commit the change to make it permanent
uci commit system

# Optional: Apply the change immediately
/etc/init.d/system restart
```
Place this script in `/etc/uci-defaults/99-set-timezone-utc` to ensure it runs exactly once on the first boot. The uci-defaults directory is processed during first-boot initialization, and scripts are executed in lexicographical order.