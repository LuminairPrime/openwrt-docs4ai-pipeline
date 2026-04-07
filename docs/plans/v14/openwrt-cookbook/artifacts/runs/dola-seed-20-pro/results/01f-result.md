---

### Scenario 15
```c
#include <libubox/blobmsg.h>
#include <libubox/uloop.h>
#include "netifd/interface.h"

struct interface *interface_alloc_from_blob(struct blob_attr *msg)
{
    enum {
        IF_ATTR_NAME,
        IF_ATTR_IFNAME,
        IF_ATTR_MTU,
        IF_ATTR_FLAGS,
        __IF_ATTR_MAX
    };

    static const struct blobmsg_policy if_policy[__IF_ATTR_MAX] = {
        [IF_ATTR_NAME] = { .name = "name", .type = BLOBMSG_TYPE_STRING },
        [IF_ATTR_IFNAME] = { .name = "ifname", .type = BLOBMSG_TYPE_STRING },
        [IF_ATTR_MTU] = { .name = "mtu", .type = BLOBMSG_TYPE_INT32 },
        [IF_ATTR_FLAGS] = { .name = "flags", .type = BLOBMSG_TYPE_INT32 },
    };

    struct blob_attr *tb[__IF_ATTR_MAX];
    struct interface *iface;

    if (blobmsg_parse(if_policy, __IF_ATTR_MAX, tb, blobmsg_data(msg), blobmsg_len(msg)) < 0)
        return NULL;

    if (!tb[IF_ATTR_NAME] || !tb[IF_ATTR_IFNAME])
        return NULL;

    iface = calloc(1, sizeof(*iface));
    if (!iface)
        return NULL;

    iface->name = strdup(blobmsg_get_string(tb[IF_ATTR_NAME]));
    iface->ifname = strdup(blobmsg_get_string(tb[IF_ATTR_IFNAME]));
    iface->mtu = tb[IF_ATTR_MTU] ? blobmsg_get_u32(tb[IF_ATTR_MTU]) : 1500;
    iface->flags = tb[IF_ATTR_FLAGS] ? blobmsg_get_u32(tb[IF_ATTR_FLAGS]) : 0;

    return iface;
}
```
**Explanation:** Follows standard OpenWrt `blobmsg` parsing pattern used throughout netifd, ubus, and all core daemons. Uses correct policy table parsing, proper null checks, and safe default values.

---

### Scenario 18
```javascript
'use strict';
'require view';
'require form';
'require rpc';

return view.extend({
    load: function() {
        const getStatus = rpc.declare({
            object: 'luci.status',
            method: 'getInterfaceStatus',
            params: [ 'ifname' ]
        });

        return Promise.all([
            getStatus('wan'),
            uci.load('network')
        ]);
    },

    render: function(data) {
        const [ status, networkConfig ] = data;
        const m = new form.Map('network', _('WAN Interface Status'));

        const s = m.section(form.NamedSection, 'wan', 'interface');
        s.option(form.Value, 'ifname', _('Device')).readonly = true;
        s.option(form.Value, 'address', _('IP Address')).value = status.address;
        s.option(form.Value, 'uptime', _('Uptime')).value = status.uptime;

        return m.render();
    }
});
```
**Explanation:** Correct modern LuCI 2020+ view pattern: all RPC/UCI operations run exclusively inside the `load()` lifecycle hook, resolved data is passed cleanly to `render()`. Uses official `rpc.declare()` contract binding not raw `rpc.call()`.

---

### Scenario 20
```sh
#!/bin/sh

[ -n "$IPKG_INSTROOT" ] && exit 0

. /lib/functions.sh

uci set myservice.@main[0].enabled='1'
uci commit myservice

exit 0
```
**Explanation:**
- Standard OpenWrt uci-defaults script header
- Correct `IPKG_INSTROOT` skip check (prevents running at package install time instead of first boot)
- Uses official uci batch syntax, correct exit codes
- Does NOT restart/reload the service as requested; system will apply the change automatically at next normal service startup
- Placed with executable mode at `/etc/uci-defaults/90-enable-myservice`