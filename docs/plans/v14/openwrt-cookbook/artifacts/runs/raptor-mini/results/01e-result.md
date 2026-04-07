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
json_dump
```

## Scenario 27
```js
'use strict';

return L.view.extend({
  load: function() {
    return rpc.declare({
      object: 'network.interface',
      method: 'dump',
      params: []
    })();
  },

  render: function(data) {
    var address = null;
    if (data && data.interface) {
      data.interface.forEach(function(iface) {
        if (iface['.name'] === 'lan' && iface.name !== 'lo') {
          (iface.ipaddr || []).some(function(entry) {
            if (entry.family === 'ipv4' && entry.address) {
              address = entry.address;
              return true;
            }
          });
        }
      });
    }
    return E('div', {}, address || 'No LAN IPv4 address found');
  }
});
```

## Scenario 17
OpenWrt ucode is a compact scripting/configuration language used by OpenWrt to express system automation and config logic. It was created to reduce the fragility of raw shell scripting and to make device-local automation safer and more declarative. It is good for config modifications, runtime hooks, and simple automation tasks.

## Scenario 13
```sh
#!/bin/sh
payload=$(cat /etc/my_app/config.json)
startup_delay=$(jsonfilter -e '@.startup_delay' <<EOF
$payload
EOF
)
echo "$startup_delay"
```

## Scenario 14
```json
{
  "menu": [
    {
      "id": "my_tool",
      "title": "My Tool",
      "parent": "network",
      "uri": "admin/network/my_tool",
      "view": "my_tool"
    }
  ]
}
```

## Scenario 19
```sh
#!/bin/sh
[ "$INTERFACE" != "wan" ] && exit 0
[ "$ACTION" != "ifup" ] && exit 0
payload="{\"interface\":\"$INTERFACE\",\"proto\":\"$PROTO\",\"device\":\"$DEVICE\"}"
ubus call my.service handle_event "$payload"
```
