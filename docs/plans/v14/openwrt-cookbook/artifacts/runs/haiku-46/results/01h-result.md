# OpenWrt Development Test - Results

Test File: 01h.md
Test Executor: HAIKU Agent
Date: 2026-04-06

---

## Scenario 17

**Question:** What is OpenWrt ucode, why was it created, and what is it good for?

**Answer:**

OpenWrt ucode is a lightweight, embedded scripting language designed specifically for the OpenWrt embedded Linux distribution. It is a modern replacement for shell scripting in certain OpenWrt contexts.

**Why it was created:**
- OpenWrt needed a scripting language that was lighter-weight than traditional shell/bash but more expressive and safer than pure shell operations
- Traditional POSIX shell has limitations in data structures, error handling, and performance
- ucode provides a sandboxed environment for UCI (OpenWrt configuration system) operations and system scripting
- It aims to bridge the gap between shell simplicity and programmatic power while maintaining a small footprint suitable for embedded devices

**What it's good for:**
- Scripting complex configuration logic with better data structures and control flow
- Replacing certain system administration shell scripts with safer, more maintainable code
- System configuration hooks and callbacks that need structured data handling
- Processing JSON and structured data more cleanly than shell would allow
- Writing maintainable, debuggable scripts without the complexity of C or Lua
- Integration with OpenWrt's package management and configuration system
- Provides cleaner syntax for conditional logic, loops, and variable handling compared to shell

ucode features:
- C-like syntax with familiar control structures
- Dynamic typing with type coercion
- Built-in object and array support
- Better error handling with try/catch support
- Smaller memory footprint than Lua or Python
- Native integration with OpenWrt system APIs and tools

---

## Scenario 22

**Question:** For OpenWrt, write a C ubus handler snippet that parses input attributes with `blobmsg_policy` and `blobmsg_parse()`, then replies with a nested result object containing `accepted=true` and the supplied address.

**Answer:**

```c
#include <libubus.h>
#include <libubox/blobmsg.h>
#include <libubox/blobmsg_json.h>

static const struct blobmsg_policy policy[] = {
    [0] = { .name = "address", .type = BLOBMSG_TYPE_STRING },
};

enum {
    INPUT_ADDRESS,
    __INPUT_MAX
};

static int handle_request(struct ubus_context *ctx, struct ubus_object *obj,
                         struct ubus_request_data *req, const char *method,
                         struct blob_attr *msg)
{
    struct blob_attr *tb[__INPUT_MAX];
    struct blob_buf b = {};
    const char *address = NULL;

    blobmsg_parse(policy, __INPUT_MAX, tb, blob_data(msg), blob_len(msg));

    if (!tb[INPUT_ADDRESS]) {
        return UBUS_STATUS_INVALID_ARGUMENT;
    }

    address = blobmsg_get_string(tb[INPUT_ADDRESS]);

    blob_buf_init(&b, 0);
    blobmsg_add_u8(&b, "accepted", 1);
    blobmsg_add_string(&b, "address", address);

    ubus_send_reply(ctx, req, b.head);
    blob_buf_free(&b);

    return 0;
}

static struct ubus_method methods[] = {
    UBUS_METHOD("process", handle_request, policy),
};

static struct ubus_object_type object_type =
    UBUS_OBJECT_TYPE("myservice", methods);

static struct ubus_object object = {
    .name = "myservice",
    .type = &object_type,
    .methods = methods,
    .n_methods = ARRAY_SIZE(methods),
};
```

Key elements:
- `blobmsg_policy` array defines expected input attributes (address string)
- `blobmsg_parse()` parses incoming message according to policy
- Result built with `blob_buf_init()` for output
- Nested fields added with `blobmsg_add_u8()` and `blobmsg_add_string()`
- `ubus_send_reply()` returns the result
- Proper cleanup with `blob_buf_free()`

---

## Scenario 24

**Question:** Your LuCI JS view already uses `rpc.declare()` to call ubus methods on `myservice`, but the framework blocks the call because permission is missing. Write the rpcd ACL JSON file needed to grant the LuCI session read access to `get_config` and write access to `set_config`, and say where the file must be installed.

**Answer:**

**File Content:** `/etc/rpcd/acl.d/myservice.json`

```json
{
    "myservice": {
        "description": "MyService RPC Access Control",
        "read": {
            "ubus": {
                "myservice": [
                    "get_config"
                ]
            }
        },
        "write": {
            "ubus": {
                "myservice": [
                    "set_config"
                ]
            }
        }
    }
}
```

**Installation Location:**
- The file must be installed at: `/etc/rpcd/acl.d/myservice.json`
- rpcd reads all `.json` files in the `/etc/rpcd/acl.d/` directory
- The LuCI session (which typically runs as the `nobody` or `root` user depends on configuration) will be granted permissions according to the ACL rules defined
- After installing the file, rpcd will automatically load it; no service restart required if rpcd is already running, though restarting rpcd is safe
- The top-level key (`myservice`) typically corresponds to the UCI package or service name
- The `read` and `write` sections define ubus object and method access
- When a LuCI RPC call is made via `rpc.declare()`, rpcd checks the ACL to enforce permissions before allowing the ubus call

Alternative more explicit format (also valid):
```json
{
    "luci": {
        "description": "LuCI Access Control",
        "read": {
            "ubus": {
                "myservice": [
                    "get_config"
                ]
            }
        },
        "write": {
            "ubus": {
                "myservice": [
                    "set_config"
                ]
            }
        }
    }
}
```

If using this variant, the top-level key should match the authenticated user/role from LuCI's authentication.

---

## Scenario 25

**Question:** Write an OpenWrt shell snippet that sources the standard config helper library, loads the `network` config, reads the `ifname` option from section `wan`, reads a boolean `auto` option with a default of `1`, and iterates each `dns` list item.

**Answer:**

```bash
#!/bin/sh

# Source the UCI config helper library
. /lib/functions.sh

# Load the network config
config_load network

# Read the ifname option from section wan
config_get ifname wan ifname

# Read a boolean auto option with default of 1
config_get_bool auto wan auto "1"

# Iterate each dns list item
config_list_foreach wan dns handle_dns_item

handle_dns_item() {
    local dns="$1"
    echo "DNS server: $dns"
}
```

**Detailed explanation:**

```bash
#!/bin/sh

# Source the UCI config helper library - provides functions for reading UCI config
. /lib/functions.sh

# Load the network config - reads /etc/config/network into memory
config_load network

# Read the ifname option from section wan
# Syntax: config_get <variable> <section> <option> [<default>]
config_get ifname wan ifname

# Read a boolean auto option with default of 1 (true)
# Syntax: config_get_bool <variable> <section> <option> [<default>]
# Returns 0 or 1 (true/false)
config_get_bool auto wan auto "1"

# Iterate each dns list item in the wan section
# Syntax: config_list_foreach <section> <option> <function>
# Calls handle_dns_item for each list item
config_list_foreach wan dns handle_dns_item

# Handler function called for each dns entry
# The list item value is passed as $1
handle_dns_item() {
    local dns="$1"
    echo "DNS server: $dns"
}
```

**Key functions from /lib/functions.sh:**
- `config_load <config_name>`: Load a UCI config file
- `config_get <var> <section> <option> [<default>]`: Get string value
- `config_get_bool <var> <section> <option> [<default>]`: Get boolean value (0 or 1)
- `config_list_foreach <section> <option> <function>`: Iterate list items, calling function for each
- The function passed to `config_list_foreach` receives each list value as argument `$1`

This pattern is the standard OpenWrt way to read UCI configuration in shell scripts.

---

## Scenario 26

**Question:** Write an OpenWrt shell snippet that sources the native shell JSON helper, loads a JSON string from `$payload`, enters the `network` object, reads the `proto` and `device` fields, then navigates back out cleanly.

**Answer:**

```bash
#!/bin/sh

# Source the JSON helper library
. /usr/share/libubox/jshn.sh

# Sample JSON payload (would come from variable in real usage)
payload='{"network":{"proto":"static","device":"eth0","mode":"nat"}}'

# Load the JSON string into jshn
json_load "$payload"

# Enter the network object
json_select network

# Read the proto field
json_get_var proto proto

# Read the device field
json_get_var device device

# Use the values
echo "Protocol: $proto"
echo "Device: $device"

# Navigate back out to root cleanly
json_select ..

# Or if multiple levels/direct exit:
# json_select ""  # This also returns to root

echo "Exited JSON context"
```

**Extended version with error handling:**

```bash
#!/bin/sh

. /usr/share/libubox/jshn.sh

payload='{"network":{"proto":"static","device":"eth0"}}'

# Safely load JSON with error checking
if ! json_load "$payload"; then
    echo "Error: Invalid JSON payload" >&2
    exit 1
fi

# Enter network object with error checking
if ! json_select network; then
    echo "Error: network object not found" >&2
    exit 1
fi

# Read values safely
json_get_var proto proto
json_get_var device device

if [ -z "$proto" ] || [ -z "$device" ]; then
    echo "Error: Missing required fields" >&2
    json_select ..
    exit 1
fi

echo "Protocol: $proto"
echo "Device: $device"

# Navigate back out cleanly
json_select ..

# Reset jshn state completely if needed
json_cleanup
```

**Key jshn.sh functions:**
- `json_load <json_string>`: Parse JSON string into jshn context
- `json_select <path>`: Navigate into nested objects
  - `json_select network`: Enter network object
  - `json_select ..`: Go back to parent level
  - `json_select ""`: Return to root
- `json_get_var <variable> <field>`: Get field value into variable
- `json_get_type <field>`: Get field data type (object, array, string, number, true, false, null)
- `json_cleanup`: Reset jshn state completely
- `json_dump`: Dump entire parsed JSON structure

The `jshn.sh` library provides a simple way to parse and navigate JSON in shell scripts without external JSON processors.

---

## Scenario 27

**Question:** Write a LuCI/OpenWrt JS snippet that calls the runtime network-interface dump over ubus and extracts the first non-loopback IPv4 address for the `lan` interface from the returned data structure.

**Answer:**

```javascript
// LuCI/OpenWrt JavaScript - requires LuCI RPC framework

// Method 1: Using rpc.declare() and promise-based approach
var getFirstLanIPv4 = function() {
    return rpc.declare({
        object: 'network.interface',
        method: 'dump',
        params: []
    })().then(function(result) {
        if (result && result.interface) {
            // Find the 'lan' interface
            var lanInterface = null;
            for (var i = 0; i < result.interface.length; i++) {
                if (result.interface[i]['interface'] === 'lan') {
                    lanInterface = result.interface[i];
                    break;
                }
            }
            
            if (!lanInterface || !lanInterface.ipv4_address) {
                return null;
            }
            
            // Extract first non-loopback IPv4 address
            var addresses = lanInterface.ipv4_address;
            for (var i = 0; i < addresses.length; i++) {
                var addr = addresses[i].address;
                if (addr && addr !== '127.0.0.1') {
                    return addr;
                }
            }
        }
        return null;
    });
};

// Usage:
getFirstLanIPv4().then(function(ipv4) {
    console.log('LAN IPv4 Address: ' + ipv4);
});
```

**Method 2: Direct ubus call via LuCI's `rpc` object (synchronous style in callback):**

```javascript
// Using LuCI's rpc.call for direct ubus invocation
rpc.declare({
    object: 'network.interface',
    method: 'dump',
    params: []
})().then(function(result) {
    var lanIPv4 = null;
    
    if (result && result.interface) {
        for (var i = 0; i < result.interface.length; i++) {
            var iface = result.interface[i];
            
            // Find lan interface
            if (iface.interface === 'lan' && iface.ipv4_address) {
                // Extract first non-loopback IPv4
                for (var j = 0; j < iface.ipv4_address.length; j++) {
                    var addr = iface.ipv4_address[j].address;
                    if (addr && !addr.startsWith('127.')) {
                        lanIPv4 = addr;
                        break;
                    }
                }
                break;
            }
        }
    }
    
    if (lanIPv4) {
        console.log('First LAN IPv4: ' + lanIPv4);
        document.getElementById('lan-ip').textContent = lanIPv4;
    }
});
```

**Method 3: With error handling and fallback:**

```javascript
function extractFirstLanIPv4() {
    return rpc.declare({
        object: 'network.interface',
        method: 'dump',
        params: []
    })().then(function(result) {
        if (!result || !result.interface || !Array.isArray(result.interface)) {
            console.error('Invalid response structure');
            return null;
        }
        
        // Find lan interface
        var lanIface = result.interface.find(function(iface) {
            return iface.interface === 'lan';
        });
        
        if (!lanIface || !Array.isArray(lanIface.ipv4_address)) {
            console.warn('LAN interface not found or has no IPv4 addresses');
            return null;
        }
        
        // Find first non-loopback IPv4
        var firstIPv4 = lanIface.ipv4_address.find(function(addr) {
            return addr.address && addr.address !== '127.0.0.1' && 
                   !addr.address.startsWith('127.');
        });
        
        return firstIPv4 ? firstIPv4.address : null;
    }).catch(function(error) {
        console.error('ubus call failed:', error);
        return null;
    });
}

// Usage with async/await style (in newer LuCI):
(async function() {
    var ipv4 = await extractFirstLanIPv4();
    console.log('LAN IPv4: ' + ipv4);
})();
```

**Expected ubus response structure from `network.interface dump`:**
```json
{
    "interface": [
        {
            "interface": "lan",
            "proto": "static",
            "ipv4_address": [
                {
                    "address": "192.168.1.1",
                    "mask": 24
                }
            ],
            "ipv6_address": [],
            "uptime": 12345
        },
        {
            "interface": "wan",
            "proto": "dhcp",
            "ipv4_address": [
                {
                    "address": "10.0.0.5",
                    "mask": 24
                }
            ]
        }
    ]
}
```

**Key points:**
- `rpc.declare()` creates an RPC method that calls ubus
- `network.interface` is the ubus object
- `dump` is the method that returns all interface data
- The response structure contains an array of interfaces under `interface` key
- Each interface has `ipv4_address` array containing address objects
- Filter out loopback addresses (127.0.0.1 or starting with 127.)
- Use promises (.then()) or async/await for handling asynchronous ubus calls
- Proper error handling is important for production code

---

## Summary

All 6 scenarios completed:
- ✅ Scenario 17: OpenWrt ucode explanation
- ✅ Scenario 22: C ubus handler with blobmsg
- ✅ Scenario 24: rpcd ACL JSON configuration
- ✅ Scenario 25: OpenWrt shell config helper usage
- ✅ Scenario 26: Shell JSON helper with jshn.sh
- ✅ Scenario 27: LuCI JavaScript ubus network dump

All answers provided with complete code snippets and detailed explanations.
