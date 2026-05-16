---
title: ucode Native File IO and JSON
module: cookbook
origin_type: authored
token_count: 1226
source_file: L1-raw/cookbook/ucode-native-file-io-and-json.md
last_pipeline_run: '2026-05-16T04:56:26.459188+00:00'
source_locator: static/cookbook-source/ucode-native-file-io-and-json.md
description: Correct current-era pattern for reading files and parsing JSON directly
  in ucode with fs.readfile() and json(), without shell wrappers or external parsers.
era_status: current
when_to_use: Use when a ucode script or rpcd plugin needs to read a non-UCI file,
  parse JSON, and extract structured values without dropping into shell helpers like
  jq, jsonfilter, or cat.
related_modules:
- ucode
- luci-examples
- uci
verification_basis: Verified against ucode fs and json reference material in the condensed
  corpus; current upstream ucode JSON tests; cross-batch defect synthesis for Scenario
  13
reviewed_by: placeholder
last_reviewed: '2026-04-05'
---

> **Source:** `static/cookbook-source/ucode-native-file-io-and-json.md`
> **Kind:** authored | **Method:** hand-authored
> **Normalized:** 2026-05-16

# ucode Native File IO and JSON

> **When to use:** Use when the data you need already lives in a JSON file and the script is written in ucode. In that situation, stay entirely inside the ucode runtime: read with `fs.readfile()` and parse with `json()`. Do not shell out to `cat`, `jq`, `jsonfilter`, `grep`, or `awk`.
> **Key components:** ucode, fs module, `json()`
> **Era:** Current (23.x+). Native file reads and native JSON parsing are the default ucode path for structured file input.

## Overview

The durable pattern is simple:

1. read the file contents natively
2. parse the JSON natively
3. pull structured values from the parsed object
4. handle missing files or bad JSON explicitly

This matters because a repeated blind-failure pattern is to write a ucode script that immediately collapses into shell thinking: `cat /etc/my_app/config.json | jq ...`. That is both slower and less maintainable than the APIs the runtime already provides.

## Complete Working Example

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

This is the whole pattern for the common case. The script stays inside ucode from start to finish, reads the file once, parses it once, and then accesses the key directly.

## Step-by-Step Explanation

### `fs.readfile()` is the normal file-read entry point

```ucode
const raw = fs.readfile('/etc/my_app/config.json');
```

Use `fs.readfile()` when the file is reasonably sized and the task is not line-streaming. That is the direct replacement for shelling out to `cat` from within ucode.

### `json()` parses structured input directly

```ucode
data = json(raw);
```

`json()` is the built-in parser for JSON strings in ucode. It returns objects, arrays, numbers, booleans, and `null` in native ucode value form. There is no need for `jq` or `jsonfilter` once the script is already running inside the ucode runtime.

### Handle bad files and bad JSON separately

Treat these as different failures:

- file could not be read
- file contents are not valid JSON
- JSON is valid but the key is missing

Those are three different operational problems and they deserve three different error messages.

### Keep this separate from UCI work

If the data belongs in `/etc/config/`, switch to [UCI Read/Write from ucode](./uci-read-write-from-ucode.md). This page is specifically for non-UCI JSON files and similar structured external input.

## Anti-Patterns

### WRONG: Shelling out to `cat` and `jq`

```ucode
let proc = fs.popen("cat /etc/my_app/config.json | jq -r .startup_delay", 'r');
print(proc.read('all'));
```

**Why it fails:** This adds extra subprocesses, adds quoting and shell-fragility problems, and ignores the direct file and parser APIs the runtime already exposes.

### WRONG: Parsing JSON with grep, sed, or awk

```ucode
let value = fs.popen("grep startup_delay /etc/my_app/config.json | awk -F: '{print $2}'", 'r').read('all');
```

**Why it fails:** JSON is a structured format. Text slicing works until whitespace, nesting, escaping, or formatting changes. The right abstraction already exists. Use it.

### WRONG: Using UCI APIs for non-UCI JSON files

```ucode
import { cursor } from 'uci';
const uci = cursor();
uci.get('my_app', 'main', 'startup_delay');
```

**Why it fails:** UCI is the persistent config system for `/etc/config/*`, not a general parser for arbitrary JSON files. Use the right storage surface for the right task.

## Related Topics

- [UCI Read/Write from ucode](./uci-read-write-from-ucode.md) - use this when the data should live in UCI instead of JSON files
- [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md) - use this when the parsed data should be exposed through rpcd or ubus instead of printed directly
- [Architecture Overview](./architecture-overview.md) - use this when deciding whether data should stay in a file, move to UCI, or be surfaced through ubus
- [ucode fs module reference](../../ucode/chunked-reference/c_source-api-module-fs.md) - exact file and handle API details

## Verification Notes

- `fs.readfile(path, [limit])` verified from condensed corpus `ucode/c_source-api-module-fs.md`
- `json()` semantics verified from current upstream ucode JSON tests under `tmp/authoring-repos/repo-ucode-full/tests/custom/03_stdlib/34_json`
- native file-read plus parse blind spot verified by Scenario 13 in the frozen test pack and cross-batch synthesis
- scenario packet reference for this page: `docs/plans/v14/openwrt-cookbook/artifacts/scenario-packets/02-scn-2026-002-ucode-native-json-file-read.yaml`
- known limitation: this page covers native JSON file parsing, not streaming process output or UCI-backed configuration mutation
