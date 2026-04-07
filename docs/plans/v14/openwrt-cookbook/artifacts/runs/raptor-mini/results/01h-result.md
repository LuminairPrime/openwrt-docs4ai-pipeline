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
OpenWrt ucode is a compact embedded scripting language for the OpenWrt platform. It was created to let system maintainers express automation and configuration changes safely and with predictable structure. It is good for handling runtime device logic, config commits, and simple automation tasks in a more robust way than raw shell code.

## Scenario 22
```c
static const struct blobmsg_policy policy[] = {
    { .name = "address", .type = BLOBMSG_TYPE_STRING },
};

static int my_handler(struct ubus_context *ctx, struct ubus_object *obj,
                      struct ubus_request_data *req, const char *method,
                      struct blob_attr *msg)
{
    struct blob_attr *tb[ARRAY_SIZE(policy)];
    struct blob_buf buf;
    const char *address;

    blobmsg_parse(policy, ARRAY_SIZE(policy), tb, blobmsg_data(msg), blobmsg_len(msg));
    if (!tb[0])
        return UBUS_STATUS_INVALID_ARGUMENT;

    address = blobmsg_get_string(tb[0]);
    blob_buf_init(&buf, 0);
    blobmsg_add_bool(&buf, "accepted", true);
    blobmsg_add_string(&buf, "address", address);
    ubus_send_reply(ctx, req, buf.head);
    return 0;
}
```

## Scenario 24
```json
{
  "name": "myservice",
  "description": "Grant LuCI session access to myservice RPC methods",
  "policy": [
    {
      "user": "@luci",
      "allow": [
        { "method": "get_config", "access": "read" },
        { "method": "set_config", "access": "write" }
      ]
    }
  ]
}
```

Install this file under `/etc/rpcd.d/`, for example `/etc/rpcd.d/myservice_acl.json`.

## Scenario 25
```sh
#!/bin/sh
. /lib/functions.sh

config_load network
config_get ifname wan ifname ""
config_get_bool auto wan auto 1
config_get_list dns wan dns

json_init
json_add_object "network"
json_add_string "ifname" "$ifname"
json_add_bool "auto" "$auto"
json_add_array "dns"
for entry in "${dns[@]}"; do
    json_add_string "" "$entry"
done
json_close_array
json_close_object
json_dump
```
