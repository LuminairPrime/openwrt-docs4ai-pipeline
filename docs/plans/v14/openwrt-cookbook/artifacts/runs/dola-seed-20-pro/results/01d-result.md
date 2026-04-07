---

### Scenario 08
```ucode
#!/usr/bin/env ucode

'use strict';

import { uci } from 'uci';

// Open UCI context
const u = uci.open();

// Set new LAN IP address
u.set('network', 'lan', 'ipaddr', '10.10.10.1');

// Commit only the network config (avoids touching other sections)
u.commit('network');

// Sync filesystem to ensure changes persist across reboot
import { fs } from 'fs';
fs.sync();

u.close();
```
**Explanation**: Uses the official ucode UCI bindings, commits only the targeted config namespace, and explicitly performs a filesystem sync to guarantee data is written to flash before exiting. This avoids partial config corruption on power loss.

---

### Scenario 11
```makefile
include $(TOPDIR)/rules.mk

PKG_NAME:=my_app
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/my_app
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=Custom application example
  DEPENDS:=+libubus
endef

define Package/my_app/description
  Custom demonstration application for OpenWrt
endef

define Build/Compile
	$(TARGET_CC) $(TARGET_CFLAGS) $(TARGET_LDFLAGS) \
		-o $(PKG_BUILD_DIR)/my_app $(PKG_BUILD_DIR)/my_app.c \
		-lubus
endef

define Package/my_app/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/my_app $(1)/usr/bin/
endef

$(eval $(call BuildPackage,my_app))
```
**Explanation**: Standard OpenWrt package Makefile structure. Correctly declares libubus dependency, uses target compiler flags properly, and follows standard installation paths.

---

### Scenario 12
```c
#include <libubox/uloop.h>
#include <libubus.h>

static struct ubus_context *ubus_ctx;

int main(int argc, char **argv)
{
    uloop_init();

    ubus_ctx = ubus_connect(NULL);
    if (!ubus_ctx) {
        return 1;
    }

    ubus_add_uloop(ubus_ctx);

    /* Service implementation would be registered here */

    uloop_run();

    /* Cleanup on exit */
    ubus_free(ubus_ctx);
    uloop_done();

    return 0;
}
```
**Explanation**: Minimal correct boilerplate for OpenWrt system bus daemons. Uses the standard ubus + uloop event loop stack which is the standard runtime environment for all OpenWrt system services. No custom event loops should be used in OpenWrt daemons.