# Result for 01g.md

## Scenario 16

To run two simultaneous pinks and prefix their output in an OpenWrt shell:

```bash
#!/bin/sh

# Launch both pings in the background, piping each to sed for prefixing
ping 10.10.10.2 | sed "s/^/10.10.10.2: /" &
ping 10.10.10.3 | sed "s/^/10.10.10.3: /" &

# Wait for both background processes to complete (which is never, unless interrupted)
wait
```

## Scenario 21

To use the board-defaults helpers from `/lib/functions/uci-defaults.sh` to define the WAN interface:

```bash
# In board-defaults script: /etc/board.d/01-network
. /lib/functions/uci-defaults.sh

# This helper will automatically handle the network configuration for us
# Arguments: interface, device, protocol
ucidef_set_interface_wan "dsl0" "pppoe"

# Note: This is usually used for board-specific initial network layout
# rather than runtime configuration.
```

## Scenario 23

The `Package/install` snippet for an OpenWrt Makefile to handle different assets correctly:

```makefile
define Package/my-luci-app/install
	# 1. LuCI JS View
	$(INSTALL_DIR) $(1)/www/luci-static/resources/view/my_app
	$(INSTALL_DATA) ./files/view/my_app_view.js $(1)/www/luci-static/resources/view/my_app/

	# 2. ACL File for rpcd/LuCI
	$(INSTALL_DIR) $(1)/usr/share/rpcd/acl.d
	$(INSTALL_DATA) ./files/my_app_acl.json $(1)/usr/share/rpcd/acl.d/

	# 3. rpcd Helper Script
	$(INSTALL_DIR) $(1)/usr/libexec/rpcd
	$(INSTALL_BIN) ./files/my_app_helper $(1)/usr/libexec/rpcd/

	# 4. UCI Config File
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./files/my_app.config $(1)/etc/config/my_app

	# 5. uci-defaults Bootstrap Script
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/my_app_setup $(1)/etc/uci-defaults/99-my_app
end define
```
