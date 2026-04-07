## Scenario 26
# Source JSON helper and extract network.proto and network.device
. /usr/share/libubox/jshn.sh
load_json "$payload"
json_get_var proto proto
json_get_var device device
## Values are now in $proto and $device variables
# Clean exit (no explicit cleanup needed for jshn.sh)

## Scenario 27
// LuCI/OpenWrt JS snippet to get LAN IPv4 address
function getLanIPv4() {
    return new Promise((resolve, reject) => {
        require(['ubus'], function(ubus) {
            ubus.call('network.interface', 'dump', {}, function(err, data) {
                if (err) {
                    reject(err);
                    return;
                }
                
                // Find lan interface
                const lanInterface = data.interface.find(
                    iface => iface['interface'] === 'lan'
                );
                
                if (!lanInterface) {
                    reject(new Error('LAN interface not found'));
                    return;
                }
                
                // Find first non-loopback IPv4 address
                const ipv4Addr = lanInterface['ipv4-address'].find(
                    addr => addr.address !== '127.0.0.1'
                );
                
                if (ipv4Addr) {
                    resolve(ipv4Addr.address);
                } else {
                    reject(new Error('No non-loopback IPv4 address found for LAN'));
                }
            });
        });
    });
}

// Usage:
getLanIPv4().then(ip => {
    console.log('LAN IPv4:', ip);
}).catch(err => {
    console.error('Error:', err);
});

## Scenario 17
OpenWrt ucode is a lightweight, embeddable scripting language derived from Lua, designed specifically for OpenWrt's embedded environment. It was created to provide a minimal-footprint alternative to full Lua interpreters for system configuration and automation tasks on resource-constrained devices. Ucode is good for system configuration scripts, event handling, and lightweight automation where memory usage must be minimized, offering Lua-like syntax with significantly reduced resource consumption.

## Scenario 08
# ucode script to change LAN IP address and commit to flash
#!/usr/bin/ucode
require("uci")

# Change network.lan.ipaddr to 10.10.10.1
uci_set("network", "lan", "ipaddr", "10.10.10.1")

# Commit changes to flash storage
uci_commit("network")

# Exit cleanly
exit(0)

## Scenario 11
# Makefile for OpenWrt package compiling my_app with system bus dependency
include $(TOPDIR)/rules.mk

PKG_NAME:=my_app
PKG_VERSION:=1.0
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)-$(PKG_RELEASE)

include $(INCLUDE_DIR)/package.mk

define Package/my_app
	SECTION:=utils
	CATEGORY:=Utilities
	TITLE:=My custom application
	DEPENDS:=+libubox +libubus
endef

define Package/my_app/description
	A custom C application for OpenWrt that depends on system bus libraries
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
	$(MAKE) -C $(PKG_BUILD_DIR) \
		CC="$(TARGET_CC)" \
		CFLAGS="$(TARGET_CFLAGS)" \
		LDFLAGS="$(TARGET_LDFLAGS)"
endef

define Package/my_app/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/my_app $(1)/usr/bin/
endef

$(eval $(call BuildPackage,my_app))

## Scenario 12
/*
 * Boilerplate for standalone OpenWrt C service daemon using system bus (ubus)
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <libubus.h>
#include <libubox/uloop.h>

static struct ubus_context *ctx;
static struct ubus_subscriber subscriber;

static void signal_handler(int sig) {
    fprintf(stderr, "Received signal %d, shutting down...\n", sig);
    ubus_free(ctx);
    exit(0);
}

static void connection_lost(struct ubus_context *ctx) {
    fprintf(stderr, "Connection to ubus lost, attempting reconnect...\n");
    // Reconnection logic would go here
}

int main(int argc, char **argv) {
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    uloop_init();
    
    ctx = ubus_connect(NULL);
    if (!ctx) {
        fprintf(stderr, "Failed to connect to ubus\n");
        return 1;
    }
    
    ubus_set_connection_lost_cb(ctx, connection_lost);
    
    // Add your object definitions and method registrations here
    // Example:
    // static struct ubus_method methods[] = {
    //     { .name = "ping", .handler = my_ping_handler },
    // };
    // static struct ubus_object_type obj_type =
    //     UBUS_OBJECT_TYPE("my_service", methods);
    // static struct ubus_object obj = {
    //     .name = "my_service",
    //     .type = &obj_type,
    //     .methods = methods,
    //     .n_methods = ARRAY_SIZE(methods),
    // };
    // ubus_add_object(ctx, &obj);
    
    fprintf(stderr, "Service daemon started, entering main loop...\n");
    uloop_run();
    
    /* Cleanup */
    ubus_free(ctx);
    uloop_done();
    
    return 0;
}