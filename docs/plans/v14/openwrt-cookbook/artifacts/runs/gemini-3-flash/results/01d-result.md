# Result for 01d.md

## Scenario 08

To modify the `network.lan.ipaddr` using a `ucode` script:

```javascript
/* Standard ucode script for UCI modification */
const uci = require("uci");

let cursor = uci.cursor();
cursor.set("network", "lan", "ipaddr", "10.10.10.1");

// Commit specifically the network configuration to flash
if (cursor.commit("network")) {
    print("Successfully updated network.lan.ipaddr to 10.10.10.1 and committed changes.\n");
} else {
    print("Failed to commit network changes.\n");
}
```

## Scenario 11

A simple Makefile for an OpenWrt package `my_app` that depends on the system bus (ubus):

```makefile
include $(TOPDIR)/rules.mk

PKG_NAME:=my_app
PKG_RELEASE:=1
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/my_app
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=My custom C daemon
  DEPENDS:=+libubus +libblobmsg-json
end define

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
end define

define Package/my_app/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/my_app $(1)/usr/sbin/
end define

$(eval $(call BuildPackage,my_app))
```

## Scenario 12

A boilerplate for a standalone OpenWrt C service daemon using the system bus:

```c
#include <libubus.h>
#include <libubox/uloop.h>

int main(int argc, char **argv)
{
    // Initialize the main event loop
    uloop_init();

    // Connect to the system bus (ubus)
    struct ubus_context *ctx = ubus_connect(NULL);
    if (!ctx) {
        fprintf(stderr, "Failed to connect to ubus\n");
        return -1;
    }

    // Add the ubus context to the event loop handler
    ubus_add_uloop(ctx);

    // Enter the event loop indefinitely
    uloop_run();

    // Cleanup when uloop_run exits (e.g., on signal)
    ubus_free(ctx);
    uloop_done();

    return 0;
}
```
