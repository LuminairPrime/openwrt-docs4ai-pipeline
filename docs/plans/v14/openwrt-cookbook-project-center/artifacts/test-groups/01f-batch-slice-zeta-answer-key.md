# Zeta Batch Answer Key

**Batch:** `01f-batch-slice-zeta.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 16

---

## Scenario 16 — ucode async parallel ping stream handling

**PASS criteria:** Must use `fs.popen()` process handles and `uloop.handle(..., uloop.ULOOP_READ)` to stream both command outputs live.

**Canonical Answer:**

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

**Pattern Notes:**

- shell background jobs using `&` fail this scenario
- FIFO fan-in or manual shell multiplexing fails this scenario
- omitting the explicit `uloop.ULOOP_READ` event mask fails this scenario
