---
title: ucode Async Process Pattern
description: Source-backed pattern for running external commands from ucode with fs.popen() and wiring live output into the uloop event system with explicit read events.
module: cookbook
origin_type: authored
when_to_use: Use when a ucode script needs to launch one or more external commands and consume their output live without falling back to shell background jobs, FIFOs, or manual polling loops.
related_modules: [ucode, openwrt-core, luci-examples]
era_status: current
verification_basis: Verified against ucode fs and uloop reference surfaces in the condensed corpus; cross-batch defect synthesis for Scenario 16; unetmsg upstream ucode example showing explicit ULOOP_READ handling
reviewed_by: placeholder
last_reviewed: 2026-04-05
---

# ucode Async Process Pattern

> **When to use:** Use when a ucode script must run an external command and stream its output as it arrives, especially when two or more commands need to be observed concurrently. This is the OpenWrt-native replacement for shell `&` background jobs, `mkfifo` fan-in tricks, and ad hoc `while read` multiplexing.
> **Key components:** ucode, fs module, uloop module, process handles
> **Era:** Current (23.x+). Treat `fs.popen()` plus `uloop.handle(..., uloop.ULOOP_READ)` as the durable async boundary for ucode process streaming.

## Overview

The durable pattern is:

1. launch the command with `fs.popen()` in read mode
2. hand the returned process handle to `uloop.handle()`
3. pass the explicit event mask `uloop.ULOOP_READ`
4. read output incrementally inside the callback with `proc.read("line")`

This matters because the most common blind AI failure in this area is to treat ucode like shell glue: start two processes with `&`, merge them through FIFOs, and then parse the combined stream manually. That is exactly the wrong abstraction level on current OpenWrt. ucode already has a native event loop and handle model. Use it.

## Complete Working Example

```ucode
#!/usr/bin/env ucode
'use strict';

import * as fs from 'fs';
import * as uloop from 'uloop';

const targets = [ '10.10.10.2', '10.10.10.3' ];

function attach_ping(target) {
	let proc = fs.popen(`ping ${target}`, 'r');

	if (!proc)
		die(`failed to launch ping for ${target}: ${fs.error()}\n`);

	uloop.handle(proc, function(events) {
		if (!(events & uloop.ULOOP_READ))
			return;

		let line;

		while ((line = proc.read('line')) != null)
			print(`${target}: ${line}`);
	}, uloop.ULOOP_READ);
}

for (let target in targets)
	attach_ping(target);

uloop.run();
uloop.done();
```

This example keeps both `ping` processes live and lets uloop deliver whichever stream becomes readable first. Each printed line is tagged with its source target so the merged output stays understandable.

## Step-by-Step Explanation

### `fs.popen()` returns the process handle you monitor

```ucode
let proc = fs.popen(`ping ${target}`, 'r');
```

`fs.popen()` launches the child process and returns a process-handle object. That handle is the thing you pass to `uloop.handle()`. Do not invent your own descriptor wrapper and do not shell out only to read all output later in one batch.

### `uloop.handle()` needs an explicit event mask

```ucode
uloop.handle(proc, callback, uloop.ULOOP_READ);
```

The event mask is not optional. The common failure shape is to register the callback without `uloop.ULOOP_READ`, which means the script never declares what event should wake the callback.

### Stream the process incrementally

```ucode
while ((line = proc.read('line')) != null)
	print(`${target}: ${line}`);
```

Use `read('line')` when the producer emits line-oriented output. This keeps memory bounded and lets the script react to each new line as soon as it arrives. For JSON blobs or one-shot command output, `read('all')` may be fine, but that is a different task boundary.

### `uloop.run()` drives the whole script

```ucode
uloop.run();
uloop.done();
```

`uloop.run()` blocks and dispatches readable-handle callbacks until the script is interrupted or the loop is explicitly ended. `uloop.done()` then releases the loop state. For continuously running commands like `ping`, the script intentionally stays alive until the operator stops it.

For finite commands, extend this pattern with explicit EOF cleanup: when `proc.read('line')` starts returning `null`, unregister the handle, decrement any active-job counter, and call `uloop.end()` once the last process finishes.

## Anti-Patterns

### WRONG: Shell background jobs inside ucode

```ucode
system('ping 10.10.10.2 &');
system('ping 10.10.10.3 &');
```

**Why it fails:** This punts concurrency back to the shell, gives you no structured ownership of the process handles, and leaves output interleaving to shell behavior rather than the ucode event loop.

### WRONG: FIFO fan-in and manual multiplexing

```sh
mkfifo /tmp/ping.pipe
ping 10.10.10.2 > /tmp/ping.pipe &
ping 10.10.10.3 > /tmp/ping.pipe &
while read line; do
	echo "$line"
done < /tmp/ping.pipe
```

**Why it fails:** This is a shell hack, not a ucode pattern. It creates extra state, makes provenance of each line ambiguous, and throws away the current OpenWrt runtime's native async handle model.

### WRONG: Inventing descriptor reads for process handles

```ucode
let proc = fs.popen('ping 10.10.10.2', 'r');
let buf = fs.read(proc, 128);
```

**Why it fails:** The process handle already exposes the read surface. The blind-failure pattern here is to imagine a POSIX-style raw descriptor API that the ucode fs layer does not provide for this task.

## Related Topics

- [UCI Read/Write from ucode](./uci-read-write-from-ucode.md) - use this when the script's real job is persistent config mutation rather than async process IO
- [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md) - use this when the output should become a backend API rather than terminal streaming
- [Architecture Overview](./architecture-overview.md) - use this when deciding whether work belongs in ucode, rpcd, ubus, or the browser
- [ucode fs module reference](../ucode/c_source-api-module-fs.md) - detailed handle and read semantics
- [ucode uloop module reference](../ucode/c_source-api-module-uloop.md) - detailed event loop and event constant reference

## Verification Notes

- `fs.popen(command, [mode])` and process-handle reading verified from corpus `ucode/c_source-api-module-fs.md` and condensed ucode references
- `uloop.handle(handle, callback, events)` and `uloop.run()` verified from corpus `ucode/c_source-api-module-uloop.md`
- explicit `ULOOP_READ` usage verified from `tmp/authoring-repos/repo-openwrt-full/package/network/services/unetmsg/files/usr/share/ucode/unetmsg/unetmsgd-remote.uc`
- line-oriented `read("line")` usage verified from current upstream ucode examples under `tmp/authoring-repos/repo-openwrt-full/package/network/services/hostapd/files/hostapd.uc`
- scenario packet reference for this page: `docs/plans/v14/openwrt-cookbook-project-center/artifacts/scenario-packets/01-scn-2026-001-ucode-async-ping-streams.yaml`
- finite-command cleanup is intentionally documented as an extension because the primary remediation target is continuous multi-stream output
- known limitation: the example demonstrates the current streaming pattern, but `reviewed_by` remains `placeholder` until a human maintainer performs final review
