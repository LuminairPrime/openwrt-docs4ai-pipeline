---

### Scenario 16
```sh
#!/bin/sh
# OpenWrt parallel ping monitor with tagged output

PING1_TARGET=10.10.10.2
PING2_TARGET=10.10.10.3

# Run pings in background with line-buffered output, prefix each line
ping "$PING1_TARGET" | stdbuf -oL sed "s/^/$PING1_TARGET: /" &
PING1_PID=$!

ping "$PING2_TARGET" | stdbuf -oL sed "s/^/$PING2_TARGET: /" &
PING2_PID=$!

# Cleanup handler
trap 'kill $PING1_PID $PING2_PID 2>/dev/null; exit 0' INT TERM

# Wait for both processes
wait
```

This uses `stdbuf -oL` to force line buffering which fixes the standard pipe buffering delay issue on BusyBox. Both ping processes run fully in parallel. The trap ensures background processes are properly terminated on Ctrl+C. This works natively on all standard OpenWrt base images with no extra packages required.

---

### Scenario 21
```sh
#!/bin/sh
. /lib/functions/uci-defaults.sh

board_config_update

# Declare WAN interface using official uci-defaults API
ucidef_set_interface_wan 'dsl0' 'pppoe'

board_config_flush

exit 0
```

Explanation:
- `ucidef_set_interface_wan()` is the official helper provided by `/lib/functions/uci-defaults.sh` for exactly this purpose
- This correctly registers the interface, sets protocol, initializes proper default firewall zones, and applies standard system defaults that raw `uci set` misses
- Always wrap board config changes with `board_config_update` and `board_config_flush` as required by the API contract
- This is the standard pattern used in all official OpenWrt target board definitions

---

### Scenario 23
```makefile
define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/lib/lua/luci/view
	$(INSTALL_DATA) ./files/luci/view/*.htm $(1)/usr/lib/lua/luci/view/

	$(INSTALL_DIR) $(1)/usr/share/rpcd/acl.d
	$(INSTALL_DATA) ./files/rpcd/acl.json $(1)/usr/share/rpcd/acl.d/$(PKG_NAME).json

	$(INSTALL_DIR) $(1)/usr/libexec/rpcd
	$(INSTALL_BIN) ./files/rpcd/helper $(1)/usr/libexec/rpcd/$(PKG_NAME)

	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./files/config/$(PKG_NAME) $(1)/etc/config/

	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/uci-defaults/* $(1)/etc/uci-defaults/
endef
```

This follows standard OpenWrt packaging conventions:
- Use correct official install macros: `INSTALL_DIR`, `INSTALL_DATA`, `INSTALL_BIN`, `INSTALL_CONF`
- Files are placed at the exact standard filesystem paths used by LuCI, rpcd, and UCI
- `INSTALL_CONF` ensures the config file gets proper conffile handling during upgrades
- All components are installed in the standard order used across official OpenWrt packages