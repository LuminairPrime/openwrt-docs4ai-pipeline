# Result for 01f.md

## Scenario 15

A C function snippet to allocate and populate a network state structure from a blobmsg:

```c
#include <libubox/blobmsg.h>
#include <libubox/blobmsg_json.h>

struct iface_state {
	char *name;
	int mtu;
	bool up;
};

enum {
	IF_ATTR_NAME,
	IF_ATTR_MTU,
	IF_ATTR_UP,
	__IF_ATTR_MAX
};

static const struct blobmsg_policy if_policy[__IF_ATTR_MAX] = {
	[IF_ATTR_NAME] = { .name = "name", .type = BLOBMSG_TYPE_STRING },
	[IF_ATTR_MTU]  = { .name = "mtu",  .type = BLOBMSG_TYPE_INT32 },
	[IF_ATTR_UP]   = { .name = "up",   .type = BLOBMSG_TYPE_BOOL },
};

struct iface_state *parse_iface_blob(struct blob_attr *msg) {
	struct blob_attr *tb[__IF_ATTR_MAX];
	struct iface_state *state;

	blobmsg_parse(if_policy, __IF_ATTR_MAX, tb, blobmsg_data(msg), blobmsg_len(msg));
	if (!tb[IF_ATTR_NAME]) return NULL;

	state = calloc(1, sizeof(*state));
	if (!state) return NULL;

	state->name = strdup(blobmsg_get_string(tb[IF_ATTR_NAME]));
	state->mtu  = tb[IF_ATTR_MTU] ? blobmsg_get_u32(tb[IF_ATTR_MTU]) : 1500;
	state->up   = tb[IF_ATTR_UP] ? blobmsg_get_bool(tb[IF_ATTR_UP]) : false;

	return state;
}
```

## Scenario 18

A modern LuCI JS view that preloads UCI and ubus data:

```javascript
'use strict';
'require view';
'require rpc';
'require uci';
'require form';

var callStatus = rpc.declare({
	object: 'network.interface',
	method: 'status',
	params: [ 'interface' ],
	expect: { '': {} }
});

return view.extend({
	load: function() {
		return Promise.all([
			uci.load('my_service'),
			callStatus('lan')
		]);
	},

	render: function(data) {
		var uciData = data[0];
		var liveStatus = data[1];

		var m, s, o;

		m = new form.Map('my_service', _('My Service'),
			_('Configure the service and view live status: ' + (liveStatus.up ? 'Active' : 'Inactive')));

		s = m.section(form.TypedSection, 'globals', _('Settings'));
		s.anonymous = true;

		o = s.option(form.Flag, 'enabled', _('Enable Service'));
		o.rmempty = false;

		return m.render();
	}
});
```

## Scenario 20

A first-boot UCI setup script for `/etc/uci-defaults/99-service-enable`:

```bash
#!/bin/sh

# Set the enabled flag for a service (e.g., 'myapp')
uci set myapp.@settings[0].enabled='1'

# Save the changes to flash
if uci commit myapp; then
    logger -t "uci-defaults" "Enabled myapp service on first boot."
    exit 0
else
    logger -t "uci-defaults" "Failed to enable myapp service."
    exit 1
fi
```
