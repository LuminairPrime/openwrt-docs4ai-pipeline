# OpenWrt Development Test Results

## Scenario 22: C ubus handler with blobmsg_policy

```c
#include <libubus.h>
#include <blobmsg.h>

static int
my_handler(struct ubus_context *ctx, struct ubus_object *obj,
           struct ubus_request_data *req, const char *method,
           struct blob_attr *msg)
{
    struct blob_attr *tb[2];
    struct blob_buf b = { 0 };

    static const struct blobmsg_policy policy[] = {
        [0] = { .name = "address", .type = BLOBMSG_TYPE_STRING },
    };

    blobmsg_parse(policy, 1, tb, blob_data(msg), blob_len(msg));

    blob_buf_init(&b, 0);
    blobmsg_add_string(&b, "accepted", "true");
    if (tb[0])
        blobmsg_add_string(&b, "address", blobmsg_get_string(tb[0]));

    ubus_send_reply(ctx, req, b.head);
    blob_buf_free(&b);

    return 0;
}
```

---

## Scenario 24: rpcd ACL JSON for LuCI ubus access

```json
{
    "myservice": {
        "description": "Access to myservice ubus methods",
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

**Installation location:** `/etc/rpcd/acl.d/myservice-acl.json` or `/etc/config/rpcd` (if using UCI config format)

---

## Scenario 25: OpenWrt shell snippet for config parsing

```sh
#!/bin/sh
. /lib/functions.sh
. /lib/functions/network.sh

config_load network

config_get ifname wan ifname
config_get_bool auto wan auto 1

config_list_foreach wan dns echo_dns

echo_dns() {
    echo "DNS server: $1"
}
```
