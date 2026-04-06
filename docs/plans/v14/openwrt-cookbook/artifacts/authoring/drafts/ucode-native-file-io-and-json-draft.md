---
title: "ucode Native File IO and JSON"
description: "Correct current-era OpenWrt pattern for reading a JSON file inside ucode with fs.readfile() and parsing it with json(), without shell helpers or text filters."
module: cookbook
origin_type: authored
when_to_use: "Use when a ucode script or rpcd helper needs structured data from a non-UCI JSON file and should stay entirely inside the ucode runtime."
related_modules: [ucode, luci-examples, uci]
era_status: current
verification_basis: "drafted from SCN-2026-002, the 01e batch verification slice, imported real blind-failure evidence, the live cookbook page, and current local plus upstream ucode authority surfaces"
reviewed_by: draft
last_reviewed: 2026-04-05
---

> [!IMPORTANT]
> This is a staged draft. Do not move it into `static/cookbook-source/` until the
> creation log exists, human review is recorded, and the promotion checklist passes.

# ucode Native File IO and JSON

> **When to use:** Use this pattern when the input already lives in a JSON file such as `/etc/my_app/config.json` and the consumer is a ucode script or rpcd helper. Read the file with `fs.readfile()`, parse it with `json()`, and keep read, parse, and missing-key failures separate.

## Overview

**Correct pattern:** In current OpenWrt ucode, read the file natively with `fs.readfile()`, parse the returned string with `json()`, then extract the required field from the parsed object.

**Wrong pattern:** Do not switch to `/bin/sh`, `jsonfilter`, `jq`, `grep`, `awk`, or `sed` just because the source file contains JSON; that changes the abstraction boundary and teaches the wrong runtime model.

This page exists to correct the specific blind failure behind Scenario 13: answering a ucode task with a shell pipeline and claiming `jsonfilter` is the native OpenWrt solution. That is wrong for this boundary. `jsonfilter` may be relevant in shell workflows, but once the task is already inside ucode, the modern OpenWrt path is to stay inside ucode for both file I/O and JSON parsing.

The bounded lesson here is narrow on purpose:

1. read the external file once
2. parse the JSON once
3. extract the needed property natively
4. report file-read, parse, and missing-key failures distinctly

If the data should instead live in `/etc/config/*`, this page is the wrong tool. Follow the UCI page linked below.

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

This is the intended OpenWrt-era answer for the scenario packet. The file read stays in the `fs` module, parsing stays in `json()`, and the final field access happens on the parsed object rather than through a second toolchain.

## Step-by-Step Explanation

### Read the file with `fs.readfile()`

`fs.readfile(path, [limit])` is the direct ucode API for loading a file into a string. For a small configuration-style JSON file, that is the right entry point. It replaces the shell instinct to run `cat` and capture process output.

```ucode
const raw = fs.readfile('/etc/my_app/config.json');
```

If the call fails, it returns `null`, and `fs.error()` exposes the filesystem error text for the last failure.

### Parse the string with `json()`

`json()` is the native parser for JSON input in ucode. When given a string, it returns normal ucode values: objects, arrays, numbers, booleans, or `null`. On malformed input, it throws a syntax exception instead of silently guessing.

```ucode
data = json(raw);
```

That is the main boundary this page corrects. For this task, you already have the JSON text in the runtime. There is no reason to invoke `jsonfilter`, `jq`, or any other external parser.

### Keep failure modes separate

The scenario slice and answer key both expect a safe snippet, not just a happy-path one-liner. Three operational failures matter here:

- the file cannot be read at all
- the file exists but contains invalid JSON
- the JSON parses but `startup_delay` is absent

Treating those as separate failures makes debugging faster and preserves the actual boundary of the problem.

### Keep this distinct from UCI-backed configuration

This page is specifically for external JSON files. If the data belongs in OpenWrt's persistent configuration system under `/etc/config/*`, use [UCI Read/Write from ucode](./uci-read-write-from-ucode.md) instead. Do not force arbitrary JSON into UCI APIs, and do not treat UCI examples as the default pattern for generic file parsing.

## Anti-Patterns

### WRONG: shelling out to `jsonfilter` or `jq`

```sh
jsonfilter -e '@.startup_delay' /etc/my_app/config.json
```

This is the real failure shape from the archived blind run. It answers a ucode-runtime task with a shell utility and teaches the wrong OpenWrt abstraction. Inside ucode, use `fs.readfile()` plus `json()` instead.

### WRONG: text slicing JSON with `grep`, `awk`, or `sed`

```sh
grep startup_delay /etc/my_app/config.json | awk -F: '{print $2}'
```

JSON is structured data. Text slicing breaks on whitespace, nested objects, arrays, escaped strings, and formatting changes. The parser already exists. Use it.

### WRONG: treating non-UCI JSON as if it were `/etc/config/*`

```ucode
import { cursor } from 'uci';
const c = cursor();
print(c.get('my_app', 'main', 'startup_delay'));
```

UCI is the right abstraction only for UCI-managed configuration. It is not a generic JSON reader.

## Related Topics

- [UCI Read/Write from ucode](./uci-read-write-from-ucode.md) - use this when the setting belongs in `/etc/config/*` and should be managed through UCI rather than a standalone JSON file.
- [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md) - use this when the parsed JSON should feed an rpcd method or ubus-exposed service instead of being printed directly.
- [Architecture Overview](./architecture-overview.md) - use this when the real decision is whether data should stay in a file, move to UCI, or be surfaced through a service boundary.
- [ucode fs module reference](../../ucode/chunked-reference/c_source-api-module-fs.md) - use this when you need the full `fs` API surface, limits, and handle semantics beyond this narrow cookbook pattern.

## Verification Notes

- Exact corpus files checked:
  - `docs/plans/v14/openwrt-cookbook/artifacts/scenario-packets/02-scn-2026-002-ucode-native-json-file-read.yaml`
  - `docs/plans/v14/openwrt-cookbook/artifacts/tests-batches/01e.md`
  - `docs/plans/v14/openwrt-cookbook/artifacts/tests-keys/01e-key.md`
  - `docs/plans/v14/openwrt-cookbook/artifacts/results/significantotter/2026-03-28-import-01/01e/01-raw-response.md`
  - `docs/plans/v14/openwrt-cookbook/artifacts/results/significantotter/2026-03-28-import-01/01e/02-manual-score.md`
  - `docs/plans/v14/openwrt-cookbook/artifacts/results/significantotter/2026-03-28-import-01/01e/03-operator-notes.md`
  - `openwrt-condensed-docs-renamed/L1-raw/ucode/c_source-api-module-fs.md`
  - `static/cookbook-source/ucode-native-file-io-and-json.md`
- Exact upstream files or URLs checked:
  - `https://ucode.mein.io/module-fs.html`
  - `https://github.com/jow-/ucode/blob/master/lib/fs.c`
  - `https://github.com/jow-/ucode/blob/master/lib.c`
  - `https://github.com/jow-/ucode/blob/master/tests/custom/03_stdlib/34_json`
- Paired local and public authority surfaces captured where available: yes
- Human reviewer to record in `reviewed_by`: pending staged human review; do not replace `draft` until review is recorded.
- `last_reviewed` date to set at promotion: keep `2026-04-05` only as the staged-draft date until promotion review resolves.
- Known caveats, limitations, or transitional edges: this page teaches the bounded file-read plus JSON-parse pattern only. It does not cover streaming parsers, process output, JSON emission, or broader configuration-placement decisions beyond routing the reader to UCI or service-pattern material.
