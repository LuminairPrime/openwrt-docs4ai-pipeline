# Result for 01c.md

## Scenario 07

A C method handler function for a ubus object that returns a JSON status object:

```c
#include <libubus.h>

static int handle_rpc_call(struct ubus_context *ctx, struct ubus_object *obj,
                           struct ubus_request_data *req, const char *method,
                           struct blob_attr *msg)
{
    struct blob_buf b = {0};
    blob_buf_init(&b, 0);

    // Prepare JSON: {"status": "ok"}
    blobmsg_add_string(&b, "status", "ok");

    // Send the reply
    ubus_send_reply(ctx, req, b.head);

    blob_buf_free(&b);
    return 0;
}
```

## Scenario 05

A LuCI Template snippet (`.htm` file) that fetches connected WiFi clients via ubus and displays them:

```html
<%
local ubus = require "ubus"
local conn = ubus.connect()
local wifi = conn:call("iwinfo", "assoclist", { device = "radio0.network1" }) or {}
conn:close()
%>

<table>
    <thead>
        <tr><th>MAC Address</th></tr>
    </thead>
    <tbody>
    <% for _, client in ipairs(wifi.results or {}) do %>
        <tr><td><%=client.mac%></td></tr>
    <% end %>
    </tbody>
</table>
```

## Scenario 10

To set the default timezone to UTC on the first boot:

```bash
#!/bin/sh

# uci-defaults script for setting timezone
uci set system.@system[0].zonename='UTC'
uci set system.@system[0].timezone='UTC'
uci commit system

# Any exit code other than 0 would mean the script stays in uci-defaults.
# On success (exit 0), procd will delete this script from /etc/uci-defaults/
exit 0
```

**Location:** You should place this script at `/etc/uci-defaults/90-timezone-utc`. Procd executes all scripts in this directory once during the first-boot initialization and deletes them on success.
