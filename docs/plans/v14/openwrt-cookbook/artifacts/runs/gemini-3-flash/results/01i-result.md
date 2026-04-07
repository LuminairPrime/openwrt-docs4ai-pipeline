# Result for 01i.md

## Scenario 26

To parse a JSON string stored in `$payload` using `jsonfilter`:

```bash
#!/bin/sh

# Assume payload is '{"network": {"proto": "dhcp", "device": "eth0"}}'
payload='{"network": {"proto": "dhcp", "device": "eth0"}}'

# Extract multiple fields at once
# This doesn't strictly have an "enter/exit" context like an object oriented parser, 
# but we can query specific sub-paths.
proto=$(echo "$payload" | jsonfilter -e "@.network.proto")
device=$(echo "$payload" | jsonfilter -e "@.network.device")

echo "Protocol: $proto, Device: $device"
```

## Scenario 27

A LuCI JS snippet to extract the IPv4 address from the system bus:

```javascript
'use strict';
'require rpc';

var callNetworkDump = rpc.declare({
	object: 'network.interface',
	method: 'dump',
	expect: { 'interface': [] }
});

return callNetworkDump().then(function(ifaces) {
	// 1. Find the 'lan' interface
	var lan = ifaces.filter(function(i) { return i.interface === 'lan' })[0];
	if (!lan || !lan.up) return null;

	// 2. Extract the first IPv4 address
	var ipv4 = (lan['ipv4-address'] && lan['ipv4-address'][0]) ? 
			   lan['ipv4-address'][0].address : "N/A";

	return ipv4;
});
```

## Scenario 17

**What is OpenWrt ucode?**
ucode is a tiny scripting and templating language developed by the OpenWrt project. It is inspired by Javascript (ECMAScript syntax) but tailored for embedded systems.

**Why was it created?**
It was created primarily to replace the fragmented and often inefficient combination of shell scripting with `jshn`/`jsonfilter` and LuCI's dependence on the Lua language. Lua, while efficient, carried a memory footprint that was sometimes too large for the smallest 4MB flash devices, and shell-based JSON parsing was slow. ucode provides a unified, fast, and very lightweight alternative.

**What is it good for?**
- **Template Rendering**: It is now the primary engine for rendering LuCI views and templates.
- **UCI Manipulation**: It has first-class support for reading and writing OpenWrt's UCI configuration.
- **JSON Processing**: It provides a native scripting environment for complex JSON manipulation without calling external binaries.
- **Initialization**: It is increasingly used in boot sequences and service management for more complex logic than raw shell scripts can handle cleanly.
