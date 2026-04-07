# OpenWrt Development Test Results

---

## Scenario 26

```sh
#!/bin/sh
. /usr/share/libubox/jshn.sh

json_init
json_load "$payload"
json_select network
json_get_var proto proto
json_get_var device device
json_select ..
```

---

## Scenario 27

```js
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var data = JSON.parse(this.responseText);
        var lan = data.interface.find(function(i) { return i.name === 'lan'; });
        if (lan && lan.ipaddr) {
            var ipv4 = lan.ipaddr.split('.').length === 4 ? lan.ipaddr : null;
            if (ipv4) console.log(ipv4);
        }
    }
};
xhr.open('GET', '/ubus/luci/network/interface/lan', true);
xhr.send();
```

Or using the LuCI RPC pattern:

```js
new LuCI.rpc.call('network.interface.dump', {}, function(res) {
    var lan = res.interface.filter(function(i) { return i.interface === 'lan'; })[0];
    if (lan) {
        var ipv4 = lan.address.find(function(a) { return a.family === 'ipv4'; });
        if (ipv4) console.log(ipv4.address);
    }
});
```

---

## Scenario 17

OpenWrt **ucode** is a lightweight, C-based scripting language developed as a minimal replacement for Lua in embedded environments. It was created to address memory and storage constraints on resource-limited router hardware while providing a simple, performant runtime for configuration and system automation tasks.

**Why it was created:**
- Lua's runtime overhead was too heavy for devices with <32MB RAM
- Need for a tiny, embeddable language with minimal dependencies
- Faster cold-start performance for system scripts

**What it's good for:**
- Fast, low-memory configuration scripts
- UCI configuration parsing and manipulation
- Network and system automation
- Replacing shell scripts where performance matters
- Embedded JSON processing with built-in JSON support
