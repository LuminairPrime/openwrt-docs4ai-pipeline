---

### Scenario 22
```c
#include <libubox/blobmsg_json.h>
#include <libubus.h>

static const struct blobmsg_policy my_policy[] = {
    { .name = "address", .type = BLOBMSG_TYPE_STRING },
};

enum {
    MY_ATTR_ADDRESS,
    MY_ATTR_MAX
};

static int my_handler(struct ubus_context *ctx, struct ubus_object *obj,
                      struct ubus_request_data *req, const char *method,
                      struct blob_attr *msg)
{
    struct blob_attr *tb[MY_ATTR_MAX];
    void *c, *r;

    blobmsg_parse(my_policy, MY_ATTR_MAX, tb, blob_data(msg), blob_len(msg));

    if (!tb[MY_ATTR_ADDRESS])
        return UBUS_STATUS_INVALID_ARGUMENT;

    c = blobmsg_open_table(ctx->buf, NULL);
    blobmsg_add_bool(ctx->buf, "accepted", true);
    r = blobmsg_open_table(ctx->buf, "result");
    blobmsg_add_string(ctx->buf, "address", blobmsg_get_string(tb[MY_ATTR_ADDRESS]));
    blobmsg_close_table(ctx->buf, r);
    blobmsg_close_table(ctx->buf, c);

    ubus_send_reply(ctx, req, ctx->buf);
    return 0;
}
```
**Explanation:** This follows OpenWrt ubus conventions: uses standard blobmsg policy array, correctly parses input attributes, constructs properly nested reply objects. Returns standard ubus status codes.

---

### Scenario 24
Create ACL file `/usr/share/rpcd/acl.d/myservice.json`:
```json
{
  "myservice": {
    "description": "Grant access to myservice ubus methods",
    "read": {
      "ubus": {
        "myservice": [ "get_config" ]
      }
    },
    "write": {
      "ubus": {
        "myservice": [ "set_config" ]
      }
    }
  }
}
```
**Installation location:** The file **MUST** be installed at `/usr/share/rpcd/acl.d/myservice.json` with permissions `0644`. No service restart is needed - rpcd automatically watches this directory for changes.

---

### Scenario 25
```sh
#!/bin/sh

# Source OpenWrt standard config library
. /lib/functions.sh

# Load network configuration database
config_load network

# Read values from wan section
config_get ifname wan ifname
config_get_bool auto wan auto 1

echo "Interface name: $ifname"
echo "Auto start: $auto"

# Iterate all dns list entries
config_list_foreach wan dns handle_dns_entry

handle_dns_entry() {
    local dns_server="$1"
    echo "Found DNS server: $dns_server"
}
```
**Explanation:** Uses standard OpenWrt `config.sh` API correctly. `config_get_bool` properly receives the default value as the 4th argument. `config_list_foreach` is the correct iterator for list options.