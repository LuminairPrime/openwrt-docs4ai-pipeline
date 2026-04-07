---

### Scenario 26
```sh
#!/bin/sh

# Source official OpenWrt libubox JSON shell helper
. /usr/share/libubox/jshn.sh

# Load payload JSON into the parser
json_load "$payload"

# Navigate into network object
json_select network

# Read required fields
json_get_var proto proto
json_get_var device device

# Cleanly exit parser context (always required!)
json_select ..
json_cleanup

# Values are now available in $proto and $device variables
```
This uses the official `jshn.sh` shell helper from libubox which is present on all standard OpenWrt installations. Always call `json_select ..` to exit nested contexts and `json_cleanup` to avoid parser state leaks.

---

### Scenario 27
```javascript
// LuCI native ubus runtime call
ubus.call('network.interface', 'dump', {}, function(result) {
    const lanInterface = result.interface.find(iface => iface.interface === 'lan');
    const firstNonLoopbackIpv4 = lanInterface['ipv4-address']
        .find(addr => !addr.address.startsWith('127.'))
        .address;

    console.log('LAN IPv4:', firstNonLoopbackIpv4);
});
```
This uses LuCI's built-in ubus bridge API. The `network.interface.dump` ubus call is the standard supported runtime interface for network state, it returns the live kernel state not just UCI configuration.

---

### Scenario 17
OpenWrt ucode is a lightweight, embeddable bytecode VM and runtime purpose-built for OpenWrt.

It was created to replace Lua as the primary embedded scripting runtime for OpenWrt:
1.  Lua 5.1 had security issues, poor memory efficiency, and lacked first-class asynchronous operation support
2.  Existing runtimes had too large footprint for 16MB / 32MB embedded devices
3.  No existing runtime properly integrated with libubox, ubus, uloop, and OpenWrt's event model

Ucode is optimized for:
-  Minimal RAM usage (<100KB base footprint)
-  Native zero-copy integration with ubus RPC
-  First-class coroutines and async I/O
-  Fast startup time for short-lived scripts
-  Safe execution sandboxing for LuCI and user applications
-  C ABI compatibility with existing OpenWrt libraries

It is now the standard runtime for LuCI, OpenWrt system services, and third-party package scripting on modern OpenWrt releases.