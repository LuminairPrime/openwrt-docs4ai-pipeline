# Epsilon Batch Answer Key

**Batch:** `01e-batch-slice-epsilon.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 13

---

## Scenario 13 — native ucode file read and JSON parse

**PASS criteria:** Must use native ucode file IO and native JSON parsing, specifically `fs.readfile()` and `json(...)`.

**Canonical Answer:**

```ucode
#!/usr/bin/env ucode
'use strict';

import * as fs from 'fs';

const path = '/etc/my_app/config.json';
const raw = fs.readfile(path);

if (raw == null)
	die(`unable to read ${path}: ${fs.error()}\n`);

let data;

try {
	data = json(raw);
}
catch (err) {
	die(`invalid JSON in ${path}: ${err}\n`);
}

if (data?.startup_delay == null)
	die(`missing startup_delay in ${path}\n`);

print(`${data.startup_delay}\n`);
```

**Pattern Notes:**

- `cat`, `jq`, `jsonfilter`, `jshn`, `grep`, `awk`, and `sed` all fail the intended boundary
- this is a native ucode runtime test, not a shell scripting test
