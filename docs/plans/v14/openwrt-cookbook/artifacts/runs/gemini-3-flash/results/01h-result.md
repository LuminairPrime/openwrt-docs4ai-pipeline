# Result for 01h.md

## Scenario 22

A C ubus handler that parses a message and returns a nested result:

```c
static int handle_request(struct ubus_context *ctx, struct ubus_object *obj,
                          struct ubus_request_data *req, const char *method,
                          struct blob_attr *msg)
{
    struct blob_attr *tb[__ATTR_MAX];
    struct blob_buf b = {0};
    const char *address;

    blobmsg_parse(my_policy, __ATTR_MAX, tb, blobmsg_data(msg), blobmsg_len(msg));
    if (!tb[ATTR_ADDR]) return UBUS_STATUS_INVALID_ARGUMENT;

    address = blobmsg_get_string(tb[ATTR_ADDR]);

    blob_buf_init(&b, 0);
    
    // Create nested: {"accepted": true, "address": "..."}
    void *c = blobmsg_open_table(&b, "result");
    blobmsg_add_bool(&b, "accepted", true);
    blobmsg_add_string(&b, "address", address);
    blobmsg_close_table(&b, c);

    ubus_send_reply(ctx, req, b.head);
    blob_buf_free(&b);
    return 0;
}
```

## Scenario 24

The rpcd ACL file to grant access to `myservice`:

```json
{
	"my-luci-app": {
		"description": "Grant access to my service methods",
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

**Location:** This file should be installed at `/usr/share/rpcd/acl.d/my-luci-app.json`. After installation, rpcd will automatically load it.

## Scenario 25

A shell snippet to parse UCI correctly using OpenWrt helpers:

```bash
#!/bin/sh

. /lib/functions.sh

# Load the system board/network configuration
config_load network

# Global or sectional read helper
local ifname auto

# 1. Read 'ifname' from 'wan' section
config_get ifname "wan" "device" "eth0"

# 2. Read boolean 'auto' from 'wan' with default '1'
config_get_bool auto "wan" "auto" 1

echo "WAN Device: $ifname (Auto-start: $auto)"

# 3. Iterate through 'dns' list items
handle_dns() {
    local val="$1"
    echo "Found DNS server: $val"
}

# Iterate call for the 'dns' list in the 'wan' section
config_list_foreach "wan" "dns" handle_dns
```
