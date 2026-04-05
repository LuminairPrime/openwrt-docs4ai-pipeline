# Theta Batch Answer Key

**Batch:** `01h-batch-slice-theta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 19, 23

---

## Scenario 19 — Hotplug guarded structured ubus forward

**PASS criteria:** Must guard on `$ACTION` and `$INTERFACE`, build a structured JSON payload, and forward it through `ubus call`.

**Canonical Answer:**

```sh
#!/bin/sh

[ "$ACTION" = "ifup" ] || exit 0
[ "$INTERFACE" = "wan" ] || exit 0

. /usr/share/libubox/jshn.sh

json_init
json_add_string action "$ACTION"
json_add_string interface "$INTERFACE"
[ -n "$DEVICE" ] && json_add_string device "$DEVICE"

ubus call myservice hotplug "$(json_dump)"
```

**Pattern Notes:**

- early exit filtering is required
- cron or polling loops fail the scenario
- a plain service restart without structured event forwarding fails the scenario

---

## Scenario 23 — Package runtime install layout

**PASS criteria:** Must provide a `Package/install` block that places config, rpcd helper, ACL, LuCI view, and `uci-defaults` assets into the correct OpenWrt package destinations.

**Canonical Answer:**

```make
define Package/mytool/install
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./files/etc/config/mytool $(1)/etc/config/mytool

	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/90-mytool $(1)/etc/uci-defaults/90-mytool

	$(INSTALL_DIR) $(1)/usr/share/acl.d
	$(INSTALL_DATA) ./files/usr/share/acl.d/mytool.json $(1)/usr/share/acl.d/mytool.json

	$(INSTALL_DIR) $(1)/usr/libexec/rpcd
	$(INSTALL_BIN) ./files/usr/libexec/rpcd/mytool $(1)/usr/libexec/rpcd/mytool

	$(INSTALL_DIR) $(1)/www/luci-static/resources/view/mytool
	$(INSTALL_DATA) ./htdocs/luci-static/resources/view/mytool/status.js \
		$(1)/www/luci-static/resources/view/mytool/status.js
endef
```

**Pattern Notes:**

- this is a runtime install layout question, not a compile boilerplate question
- generic Linux install commands outside the OpenWrt package DSL fail the scenario
