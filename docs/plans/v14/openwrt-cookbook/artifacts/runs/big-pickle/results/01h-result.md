# OpenWrt Development Test — Results

---

## Scenario 26

Write an OpenWrt shell snippet that sources the native shell JSON helper, loads a JSON string from `$payload`, enters the `network` object, reads the `proto` and `device` fields, then navigates back out cleanly.

```sh
#!/bin/sh
# Source the native shell JSON helper (jshn.sh)
. /usr/share/libubox/jshn.sh

# Start fresh — reset any prior jshn state and load JSON from $payload
json_cleanup
json_load "$payload"

# Enter the "network" object
json_select network

# Read the "proto" field
json_get_var proto proto
# Read the "device" field
json_get_var device device

# Navigate back out to the root
json_select ..
# (optional) call json_cleanup to free jshn state
json_cleanup

echo "proto=$proto device=$device"
```

Key points:
- `jshn.sh` is the standard OpenWrt shell JSON library (part of `libubox`).
- `json_load` parses `$payload` into an internal jshn key-value store.
- `json_select` pushes/pops the current object path; `..` pops back to parent.
- `json_get_var` extracts a scalar field into a shell variable.
- `json_cleanup` resets state when done.

---

## Scenario 27

Write a LuCI/OpenWrt JS snippet that calls the runtime network-interface dump over ubus and extracts the first non-loopback IPv4 address for the `lan` interface from the returned data structure.

```js
'use strict';

var rpc = require('luci.rpc');

var ubus = new rpc.LuCIRPC();

ubus.call('network.interface', 'dump', {}).then(function(data) {
    var lanInterface = null;

    // Find the "lan" interface in the interface list
    for (var i = 0; i < data.interface.length; i++) {
        if (data.interface[i].interface === 'lan') {
            lanInterface = data.interface[i];
            break;
        }
    }

    if (!lanInterface) {
        console.log('lan interface not found');
        return;
    }

    var firstNonLoopbackIPv4 = null;

    // Walk the "ipv4-address" array; skip loopback (127.0.0.0/8)
    var addrs = lanInterface['ipv4-address'] || [];
    for (var j = 0; j < addrs.length; j++) {
        var addr = addrs[j];
        if (addr.address && !addr.address.startsWith('127.')) {
            firstNonLoopbackIPv4 = addr.address + '/' + addr.mask;
            break;
        }
    }

    if (firstNonLoopbackIPv4) {
        console.log('First non-loopback IPv4 on lan: ' + firstNonLoopbackIPv4);
    } else {
        console.log('No non-loopback IPv4 found on lan');
    }
}).catch(function(err) {
    console.log('ubus call failed: ' + err);
});
```

Key points:
- `luci.rpc` exposes `call()` which wraps the underlying ubus RPC protocol.
- `network.interface dump` returns an `interface` array; each entry has an `interface` name field and an `ipv4-address` array.
- The `address` field is a string; loopback detection uses the standard `127.0.0.0/8` prefix.
- In classic LuCI dispatcher JS (旧版 `view.js` context), the same pattern applies with `XHR.get()` / `U.call()`.

---

## Scenario 17

**What is OpenWrt ucode, why was it created, and what is it good for?**

OpenWrt **ucode** (micro-code) is a lightweight, C-embedded scripting language and execution runtime introduced to OpenWrt as a replacement for traditional POSIX shell scripting in high-frequency or performance-sensitive UCI/processing contexts.

**Why it was created:**

- Shell scripts (`/bin/sh`) are slow — every UCI `config_get` or `ubus call` forks a subprocess, which on a resource-constrained router SoC is expensive.
- LuCI's Lua runtime is powerful but carries a full interpreter footprint not always justified for simple tasks.
- There was a gap between "shell is too slow" and "Lua is too heavy" for lightweight daemon helpers, ubus method handlers, and hotplug2/ubox action scripts.

**What it is good for:**

- **UCI config manipulation** — reading/writing network, system, wireless config without shell overhead.
- **ubus RPC method handlers** — writing compact ubus daemon methods in a few lines of ucode rather than C.
- **Hotplug / ubox event scripts** — reacting to device add/remove, network up/down events with low latency.
- **LED trigger / GPIO automation** — simple conditional logic on embedded hardware.
- **Drop-in replacement for shell in `/etc/hotplug.d/`** — faster boot and response times.
- **Embedded-friendly FFI to libubox / ubus** — ucode has built-in JSON, blobmsg, and ubus call bindings via the `ucode` standard library modules (`json`, `ubus`, etc.).

It compiles to a small binary (`ucode`) with a standard library of native modules. Scripts are plain text, interpreted at runtime, and can call into C libraries via simple native-module bindings.

---

## Scenario 22

For OpenWrt, write a C ubus handler snippet that parses input attributes with `blobmsg_policy` and `blobmsg_parse()`, then replies with a nested result object containing `accepted=true` and the supplied address.

```c
#include <blobmsg.h>
#include <json_script.h>
#include <libubus.h>

enum {
    EXAMPLE_ATTR_ADDRESS,
    EXAMPLE_ATTR_COUNT,
    __EXAMPLE_ATTR_MAX,
};

static const struct blobmsg_policy example_policy[] = {
    [EXAMPLE_ATTR_ADDRESS] = {
        .name = "address",
        .type = BLOBMSG_TYPE_STRING,
    },
    [EXAMPLE_ATTR_COUNT] = {
        .name = "count",
        .type = BLOBMSG_TYPE_INT32,
    },
};

static int
example_handler(struct ubus_context *ctx, struct ubus_object *obj,
                struct ubus_request_data *req,
                const char *method,
                struct blob_attr *msg)
{
    struct blob_attr *tb[__EXAMPLE_ATTR_MAX];

    /* Parse incoming blobmsg attributes into table */
    blobmsg_parse(example_policy, ARRAY_SIZE(example_policy),
                  tb, blob_data(msg), blob_len(msg));

    /* Read the address field if present */
    char *address = NULL;
    if (tb[EXAMPLE_ATTR_ADDRESS]) {
        address = blobmsg_get_string(tb[EXAMPLE_ATTR_ADDRESS]);
    }

    /* Build the reply — nested result object */
    void *reply = ubus_reply_create(ctx, req, 0);
    if (!reply)
        return UBUS_STATUS_NO_MEMORY;

    void *result = blobmsg_open_table(reply, NULL);
    blobmsg_add_string(reply, "accepted", "true");

    if (address) {
        void *net_obj = blobmsg_open_table(reply, "network");
        blobmsg_add_string(reply, "address", address);
        blobmsg_close_table(reply, net_obj);
    }

    blobmsg_close_table(reply, result);

    ubus_reply_send(ctx, req, reply);
    return 0;
}

/* method declaration for ubus_add_obj */
static const struct ubus_method example_methods[] = {
    UBUS_METHOD("submit", example_handler, example_policy),
};
```

Key points:
- `blobmsg_parse()` maps raw `blob_attr*` into a typed `tb[]` table using the policy array.
- `blobmsg_get_string()` / `blobmsg_get_u32()` / etc. extract typed values from each slot.
- Replies are built by opening a table (`blobmsg_open_table`), adding fields, then closing it.
- The nested `network` object is opened as a sub-table inside the top-level result.
- The handler returns a `ubus_status_t`; `0` (or `UBUS_STATUS_OK`) means success.

---

## Scenario 24

Your LuCI JS view already uses `rpc.declare()` to call ubus methods on `myservice`, but the framework blocks the call because permission is missing. Write the rpcd ACL JSON file needed to grant the LuCI session read access to `get_config` and write access to `set_config`, and say where the file must be installed.

**rpcd ACL JSON file** (`myservice-acl.json`):

```json
{
  "myservice": {
    "description": "Grant LuCI session access to myservice",
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

**Installation path:**

```
/usr/share/rpcd/acl.d/myservice-acl.json
```

Then restart rpcd or reload ACLs (no full reboot required — `ubus call session reload` or `service rpcd restart`).

**Explanation:**

- `ubus` ACL keys list ubus object names; each value is an array of method names granted to that session type.
- `read` grants the LuCI session's default read identity (typically `077577` / "cgi-io") permission to call `get_config`.
- `write` grants write permission (required when the JS calls `set_config` as a non-notification, mutating method).
- The filename is arbitrary but conventionally matches the service name; what matters is placement in `/usr/share/rpcd/acl.d/`.
- After installation, the next new LuCI session that loads will pick up the ACL automatically; existing sessions may need a refresh.

---

## Scenario 25

Write an OpenWrt shell snippet that sources the standard config helper library, loads the `network` config, reads the `ifname` option from section `wan`, reads a boolean `auto` option with a default of `1`, and iterates each `dns` list item.

```sh
#!/bin/sh
. /lib/functions.sh
. /lib/functions/network.sh

# Load /etc/config/network into UCI shell-var context
config_load network

# Read the "ifname" option from section "wan"
# config_get <var> <section> <option> [<default>]
config_get ifname wan ifname
echo "wan ifname: $ifname"

# Read a boolean "auto" option with default of 1
# config_get_bool <var> <section> <option> <default>
config_get_bool auto wan auto 1
echo "wan auto: $auto"

# Iterate each DNS server in the "dns" list on section "wan"
# config_list_foreach <section> <option> <function> [<args...>]
config_list_foreach wan dns echo_dns_item

# The callback function receives each list item as "$1"
echo_dns_item() {
    echo "  DNS server: $1"
}
```

Key points:
- `/lib/functions.sh` provides `config_load`, `config_get`, `config_get_bool`, `config_list_foreach`.
- `/lib/functions/network.sh` adds network helpers like `network_find_wan`, `network_get_device`, etc. (imported here for completeness; not strictly required for this snippet).
- `config_get_bool` interprets UCI values `1`, `yes`, `on`, `true` as boolean `1`; `0`, `no`, `off`, `false` as `0`; any other value falls back to the provided default (`1` in this case).
- `config_list_foreach` takes a callback function name; each list element is passed as `$1` to the callback.
- UCI `list` types are space-separated values in the UCI config file but are automatically split by `config_list_foreach`.
