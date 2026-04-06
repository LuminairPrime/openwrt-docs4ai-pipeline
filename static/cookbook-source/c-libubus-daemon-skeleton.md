---
title: C libubus Daemon Skeleton
description: Minimal current-era skeleton for a standalone OpenWrt C daemon that initializes uloop, connects to ubus, binds the bus into the loop, and blocks cleanly in the event loop.
module: cookbook
origin_type: authored
when_to_use: Use when writing a standalone OpenWrt C daemon that needs to participate in the ubus event system directly rather than exposing methods through a ucode rpcd plugin.
related_modules: [openwrt-core, procd, ucode]
era_status: current
verification_basis: Verified against current OpenWrt ubus and procd source trees; frozen Scenario 12 truth packet; current corpus coverage for adjacent rpcd and ubus patterns
reviewed_by: placeholder
last_reviewed: 2026-04-05
---

# C libubus Daemon Skeleton

> **When to use:** Use when the backend must be a native C daemon and needs the OpenWrt event loop and ubus runtime directly. If the real task is only a small privileged backend API for LuCI, prefer [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md) instead.
> **Key components:** C, libubox, uloop, libubus
> **Era:** Current (23.x+). The durable startup order is `uloop_init()` -> `ubus_connect()` -> `ubus_add_uloop()` -> `uloop_run()`.

## Overview

The foundational OpenWrt C daemon boundary is not “open a socket and sleep forever”. It is:

1. initialize the uloop runtime
2. connect to the system bus
3. register the ubus file descriptor with the uloop event loop
4. enter the loop

Missing step 3 is a common failure. The process may appear to have started, but no ubus traffic will ever be integrated into the loop correctly.

## Complete Working Example

```c
#include <stdio.h>

#include <libubox/uloop.h>
#include <libubus.h>

int main(void)
{
	struct ubus_context *ctx;

	uloop_init();

	ctx = ubus_connect(NULL);
	if (!ctx) {
		fprintf(stderr, "failed to connect to ubus\n");
		uloop_done();
		return 1;
	}

	ubus_add_uloop(ctx);

	/*
	 * Object registration or request handlers would be added here.
	 * This skeleton is intentionally limited to the runtime contract.
	 */

	uloop_run();

	ubus_free(ctx);
	uloop_done();
	return 0;
}
```

This is the minimal current-era runtime skeleton. It does not register objects or methods yet; it only establishes the correct daemon lifecycle and event-loop integration.

## Step-by-Step Explanation

### Initialize the event loop first

```c
uloop_init();
```

The daemon needs the loop runtime before it can safely integrate ubus into that loop. Reversing the order creates a runtime contract violation.

### Connect to ubus

```c
ctx = ubus_connect(NULL);
```

Passing `NULL` uses the default system ubus socket. If the connection fails, stop immediately and return a clear error instead of dropping into an inert loop.

### Bind ubus into uloop

```c
ubus_add_uloop(ctx);
```

This is the critical call most generic answers miss. Connecting to ubus is not enough. The ubus file descriptor must still be attached to the uloop event system or the daemon will never participate correctly in bus activity.

### Enter the loop only after setup is complete

```c
uloop_run();
```

Once the loop starts, the daemon waits for events. Registration of objects, watchers, or subscriptions should happen before this call.

## Anti-Patterns

### WRONG: Sleeping forever instead of using the event loop

```c
while (1) {
	sleep(5);
}
```

**Why it fails:** This creates a generic Unix daemon shape, not an OpenWrt ubus-integrated runtime. There is no event dispatch, no ubus loop integration, and no proper handoff to libubox.

### WRONG: Omitting `ubus_add_uloop()`

```c
uloop_init();
ctx = ubus_connect(NULL);
uloop_run();
```

**Why it fails:** The daemon connected to ubus, but it never registered the ubus file descriptor with the event loop. This is the exact failure shape that triggered the cookbook gap.

### WRONG: Connecting to ubus before loop setup

```c
ctx = ubus_connect(NULL);
uloop_init();
ubus_add_uloop(ctx);
```

**Why it fails:** The current-era pattern initializes the loop runtime first. Reordering this setup is a bad default to teach because it obscures the runtime contract and drifts from current OpenWrt practice.

## Related Topics

- [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md) - use this when a small rpcd plugin is sufficient and a native C daemon would be unnecessary complexity
- [ubus Observability Pattern](./ubus-observability-pattern.md) - use this when the daemon's real job is publishing runtime state for other components to consume
- [Architecture Overview](./architecture-overview.md) - use this when deciding whether the backend belongs in C, ucode rpcd, or another boundary

## Verification Notes

- `ubus_add_uloop()` presence verified from current upstream sources including `tmp/authoring-repos/repo-procd/ubus.c`, `tmp/authoring-repos/repo-ucode-full/lib/ubus.c`, and `tmp/authoring-repos/repo-uhttpd/ubus.c`
- frozen Scenario 12 truth packet confirms required runtime order: `uloop_init()` -> `ubus_connect()` -> `ubus_add_uloop()` -> `uloop_run()`
- adjacent existing cookbook page checked: `static/cookbook-source/ucode-rpcd-service-pattern.md`
- scenario packet reference for this page: `docs/plans/v14/openwrt-cookbook/artifacts/scenario-packets/03-scn-2026-003-c-libubus-daemon-skeleton.yaml`
- known limitation: this page is intentionally limited to daemon startup and event-loop binding, not object registration or blobmsg handler implementation
