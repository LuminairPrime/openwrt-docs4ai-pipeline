## Scenario 26
```bash
. /usr/share/libubox/jshn.sh
json_load "$payload"
json_select network
json_get_var proto proto
json_get_var device device
json_select ..
```

## Scenario 27
```javascript
var ubus = require('ubus');
var conn = ubus.connect();
var result = conn.call('network.interface', 'dump');
var lanInterface = result.interface.lan;
var ipv4Addresses = lanInterface['ipv4-address'];
if (ipv4Addresses && ipv4Addresses.length > 0) {
    var firstIPv4 = ipv4Addresses[0].address;
    // firstIPv4 is the first non-loopback IPv4 address for lan
}
```

## Scenario 17
Ucode is a scripting language developed for OpenWrt to replace shell scripts with a more powerful and safer alternative. It was created to provide better performance, security, and ease of use for configuration and automation tasks. It is good for writing system scripts, handling UCI configurations, and interacting with OpenWrt's system components efficiently.

## Scenario 08
```ucode
import "uci";

var cursor = uci.cursor();
cursor.set("network", "lan", "ipaddr", "10.10.10.1");
cursor.commit();
```

## Scenario 11
```
include $(TOPDIR)/rules.mk

PKG_NAME:=my_app
PKG_VERSION:=1.0
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/my_app
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=My Custom Application
  DEPENDS:=+libubus
endef

define Package/my_app/description
  A custom C program for OpenWrt.
endef

define Build/Prepare
  mkdir -p $(PKG_BUILD_DIR)
  cp src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
  $(call Build/Compile/Default)
endef

define Package/my_app/install
  $(INSTALL_DIR) $(1)/usr/bin
  $(INSTALL_BIN) $(PKG_BUILD_DIR)/my_app $(1)/usr/bin/
endef

$(eval $(call BuildPackage,my_app))
```

## Scenario 12
```c
#include <libubus.h>
#include <libubox/uloop.h>

int main(int argc, char **argv) {
    uloop_init();
    ubus_context *ctx = ubus_connect(NULL);
    if (!ctx) {
        return -1;
    }
    ubus_add_uloop(ctx);
    uloop_run();
    ubus_free(ctx);
    uloop_done();
    return 0;
}
```