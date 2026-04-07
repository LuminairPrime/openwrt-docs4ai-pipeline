---

### Scenario 01: OpenWrt Procd Startup Script
This is the standard official OpenWrt init script format using `procd` (OpenWrt native process supervisor).

```bash
#!/bin/sh /etc/rc.common

USE_PROCD=1
START=99
STOP=10

CONFIG_FILE=/etc/config/my_daemon
DAEMON=/usr/sbin/my_daemon

start_service() {
    local hostname

    config_load my_daemon
    config_get hostname general hostname

    # Apply hostname from config
    [ -n "$hostname" ] && uci set system.@system[0].hostname="$hostname" && uci commit system

    procd_open_instance
    procd_set_param command "$DAEMON"
    procd_set_param respawn  # Auto restart on crash
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_close_instance
}

service_triggers() {
    # Auto restart service when config changes
    procd_add_config_trigger "config.change" "my_daemon" /etc/init.d/my_daemon reload
}
```

**Explanation:**
- Install this file at `/etc/init.d/my_daemon` with executable permissions
- `procd` provides native crash restart, process supervision and lifecycle management
- Configuration is read from standard UCI config path `/etc/config/my_daemon`
- Uses OpenWrt native `config_load` / `config_get` UCI API
- Automatically restarts when configuration is modified

---

### Scenario 03: OpenWrt Ubus System API Module
This uses `ubus` - the official OpenWrt system IPC and API bus used by all core system services.

```c
#include <libubus.h>

static struct ubus_context *ctx;

static int my_plugin_get_status(struct ubus_context *ctx,
                                struct ubus_object *obj,
                                struct ubus_request_data *req,
                                const char *method,
                                struct blob_attr *msg)
{
    struct blob_buf buf = {};

    blob_buf_init(&buf, 0);
    blobmsg_add_string(&buf, "status", "running");
    blobmsg_add_u32(&buf, "uptime", uptime());

    ubus_send_reply(ctx, req, buf.head);
    blob_buf_free(&buf);

    return UBUS_STATUS_OK;
}

static const struct ubus_method my_plugin_methods[] = {
    UBUS_METHOD("getStatus", my_plugin_get_status, {}),
};

static struct ubus_object_type my_plugin_object_type =
    UBUS_OBJECT_TYPE("my_plugin", my_plugin_methods);

static struct ubus_object my_plugin_object = {
    .name = "my_plugin",
    .type = &my_plugin_object_type,
    .methods = my_plugin_methods,
    .n_methods = ARRAY_SIZE(my_plugin_methods),
};

// Call this at daemon initialization
int my_plugin_register_api(void) {
    ctx = ubus_connect(NULL);
    return ubus_add_object(ctx, &my_plugin_object);
}
```

**Explanation:**
- This is the exact registration pattern used by all native OpenWrt system daemons
- Registered methods are automatically available via `ubus call` CLI, LuCI, and all system services
- All method arguments and return values use OpenWrt standard `blobmsg` serialization format
- API is automatically discoverable by all system components

---

### Scenario 04: LuCI Admin Panel Firewall Zone Form
This uses the official LuCI CBI (Configuration Binding Interface) framework that all standard OpenWrt admin pages use.

```lua
local m, s, o
m = Map("firewall", translate("Firewall Zone Settings"))

s = m:section(NamedSection, "wan", "zone", translate("WAN Zone Configuration"))

-- Dynamic interface dropdown automatically populated from system network config
o = s:option(ListValue, "network", translate("Associated Interfaces"))
o:value("*", translate("All interfaces"))
o:multi(true)

-- Automatically fetch and populate all configured network interfaces
for _, iface in ipairs(luci.model.network.get_networks()) do
    o:value(iface:name(), iface:get_i18n())
end

o = s:option(Flag, "input", translate("Allow input traffic"))
o = s:option(Flag, "forward", translate("Allow forwarding"))
o = s:option(Flag, "output", translate("Allow output traffic"))
o = s:option(Flag, "masq", translate("Enable NAT masquerading"))

return m
```

**Explanation:**
- This is the standard LuCI page format used for all official OpenWrt configuration pages
- Interfaces are dynamically fetched from running system configuration using native LuCI network API
- Form validation, saving, error handling, and commit are all automatically handled by the CBI framework
- Automatically integrates with the rest of the OpenWrt admin panel theme, navigation and permissions system
- Install this file at `/usr/lib/lua/luci/model/cbi/firewall/my_zone.lua`