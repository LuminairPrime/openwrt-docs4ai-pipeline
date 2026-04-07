## Scenario 26
```sh
. /usr/share/libubox/jshn.sh
load_json "$payload"
enter object network
get_var proto proto
get_var device device
exit
```

## Scenario 27
```js
ubus call network.interface dump '{}', function(result) {
    if (result && result.interface) {
        for (let i = 0; i < result.interface.length; i++) {
            if (result.interface[i].interface === 'lan' && 
                result.interface[i].ipv4_addr && 
                result.interface[i].ipv4_addr.length > 0) {
                console.log(result.interface[i].ipv4_addr[0].address);
                break;
            }
        }
    }
});
```

## Scenario 17
OpenWrt ucode is a lightweight, embeddable JavaScript engine designed specifically for resource-constrained devices like routers running OpenWrt. It was created to provide a safe, sandboxed environment for executing user scripts and configuration logic without compromising system stability or security. Ucode is good for implementing custom network functions, dynamic firewall rules, automated configuration tasks, and lightweight web services directly on OpenWrt devices where traditional JavaScript engines would be too heavy.

## Scenario 22
```c
#include <libubox/blobmsg_json.h>
#include <libubus.h>

static const struct blobmsg_policy policy[] = {
    [ADDRESS] = { .type = BLOBMSG_TYPE_STRING },
};

static int
handle_set_address(struct ubus_context *ctx, struct ubus_object *obj,
                  struct ubus_request_data *req, const char *method,
                  struct blob_attr *msg)
{
    struct blob_attr *tb[__ADDRESS_MAX];
    char *address = NULL;
    
    blobmsg_parse(policy, ARRAY_SIZE(policy), tb, blob_data(msg), blob_len(msg));
    
    if (!tb[ADDRESS]) {
        return UBUS_STATUS_INVALID_ARGUMENT;
    }
    
    address = blobmsg_get_string(tb[ADDRESS]);
    
    /* Process the address here */
    
    /* Reply with success */
    struct blob_buf b;
    blob_buf_init(&b, 0);
    blobmsg_add_bool(&b, "accepted", true);
    if (address) {
        blobmsg_add_string(&b, "address", address);
    }
    ubus_send_reply(ctx, req, b.head);
    
    return 0;
}
```

## Scenario 24
rpcd ACL JSON file (`/etc/rpcd/acd.d/luci-myservice.json`):
```json
{
    "luci-myservice": {
        "description": "Access control for myservice",
        "read": {
            "ubus": {
                "myservice": ["get_config"]
            }
        },
        "write": {
            "ubus": {
                "myservice": ["set_config"]
            }
        }
    }
}
```
The file must be installed in `/etc/rpcd/acd.d/` directory on the OpenWrt device.

## Scenario 25
```sh
. /usr/share/libubox/jshn.sh
. /usr/share/libubox/shconfig.sh
config_load network
config_get ifname wan ifname
config_get_bool auto wan auto 1
config_foreach 'process_dns' wan dns

process_dns() {
    local dns=$1
    echo "DNS server: $dns"
}
```