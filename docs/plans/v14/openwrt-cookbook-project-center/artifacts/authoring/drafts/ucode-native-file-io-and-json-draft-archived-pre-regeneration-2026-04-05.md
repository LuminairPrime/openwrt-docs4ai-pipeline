---
title: "ucode Native File IO and JSON"
description: "Correct current-era pattern for reading files and parsing JSON directly in ucode with fs.readfile() and json(), without shell wrappers or external parsers."
module: cookbook
origin_type: authored
when_to_use: "Use when a ucode script or rpcd plugin needs to read a non-UCI file, parse JSON, and extract structured values without dropping into shell helpers like jq, jsonfilter, or cat."
related_modules: [ucode, luci-examples, uci]
era_status: current
verification_basis: "draft - staged retroactive backfill for SCN-2026-002 using imported real blind failure evidence"
reviewed_by: draft
last_reviewed: 2026-04-05
---

> [!IMPORTANT]
> This is a staged draft prepared for retroactive backfill. Do not treat it as the
> accepted promoted source of truth until a human review record is completed.

## When-to-use

> Use this when the data already lives in a JSON file and the script itself is written in ucode.
> In that case, stay inside the ucode runtime: read the file with `fs.readfile()`, parse it with
> `json()`, and extract values from the resulting object. Do not shell out to `cat`, `jq`,
> `jsonfilter`, `grep`, or `awk`.

## Overview

**Correct pattern:** in a ucode script, import the `fs` module, call `fs.readfile()` once, parse the returned string with `json()`, and read the structured fields directly.

**Wrong pattern:** answer a ucode runtime task with a shell snippet or subprocess chain built around `cat`, `jq`, `jsonfilter`, `jshn`, `grep`, `awk`, or `sed`.

This page exists because a repeated blind-failure pattern is to see “OpenWrt” and immediately fall back to shell-era JSON habits. That answer sounds plausible, but it teaches the wrong boundary. Once the task is already inside ucode, the runtime itself owns file I/O and JSON parsing.

The durable lesson is simple:

1. read the file natively
2. parse the JSON natively
3. check missing file, bad JSON, and missing key as separate failures

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

## Step-by-Step Explanation

### 1. Import the ucode file API

```ucode
import * as fs from 'fs';
```

This is the native runtime surface for file access. If the task is already a ucode task,
there is no reason to spawn a shell just to read a file.

### 2. Read the file directly

```ucode
const raw = fs.readfile('/etc/my_app/config.json');
```

`fs.readfile()` returns the file contents as a string. For this kind of small configuration
file, that is the normal entry point.

### 3. Parse the JSON directly

```ucode
data = json(raw);
```

`json()` is the native JSON parser for a JSON string inside ucode. Once the string has been
read, the correct next step is to parse it inside the same runtime, not to hand it back out to
`jq`, `jsonfilter`, or `jshn` wrappers.

### 4. Separate failure types clearly

Do not collapse everything into one generic error. The operationally useful distinctions are:

- file missing or unreadable
- file read succeeded but JSON is malformed
- JSON is valid but `startup_delay` is absent or null

Those three conditions point to different real problems and should stay separate.

### 5. Keep this separate from UCI work

This page is for non-UCI JSON files. If the data belongs in `/etc/config/*`, switch to
[UCI Read/Write from ucode](./uci-read-write-from-ucode.md) instead of treating UCI as generic JSON.

## Anti-Patterns

### WRONG: `cat` plus `jq`

```ucode
let proc = fs.popen("cat /etc/my_app/config.json | jq -r .startup_delay", 'r');
print(proc.read('all'));
```

This pays process-spawn overhead, adds shell quoting risk, and ignores the APIs the ucode runtime
already exposes directly.

### WRONG: `jsonfilter` or `jshn` inside a ucode task

```ucode
let proc = fs.popen("jsonfilter -i /etc/my_app/config.json -e '@.startup_delay'", 'r');
print(proc.read('all'));
```

`jsonfilter` and `jshn` belong to shell-tier patterns. They are not the right answer once the code is
already running inside ucode.

### WRONG: text slicing JSON with grep, awk, or sed

```ucode
let proc = fs.popen("grep startup_delay /etc/my_app/config.json | awk -F: '{print $2}'", 'r');
print(proc.read('all'));
```

JSON is structured data. Text slicing appears to work until formatting, escaping, or nesting changes.

## Related Topics

- [UCI Read/Write from ucode](./uci-read-write-from-ucode.md)
- [ucode rpcd Service Pattern](./ucode-rpcd-service-pattern.md)
- [Architecture Overview](./architecture-overview.md)
- [ucode fs module reference](../ucode/c_source-api-module-fs.md)

## Verification Notes

- Exact corpus files checked:
  - `docs/plans/v14/openwrt-cookbook-project-center/artifacts/scenario-packets/02-scn-2026-002-ucode-native-json-file-read.yaml`
  - `docs/plans/v14/openwrt-cookbook-project-center/artifacts/test-groups/01e-batch-slice-epsilon.md`
  - `docs/plans/v14/openwrt-cookbook-project-center/artifacts/test-groups/01e-batch-slice-epsilon-answer-key.md`
  - `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01a-batch-slice-alpha-answer-key-sonnet46.md`
  - `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/results/alpha/significantotter.txt`
  - `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/results/alpha/significantotter-score-20260328-0628pm.md`
  - `static/cookbook-source/ucode-native-file-io-and-json.md`
  - `static/cookbook-source/uci-read-write-from-ucode.md`
- Exact upstream files or URLs checked:
  - `openwrt-condensed-docs-renamed/ucode/c_source-api-module-fs.md`
  - `https://github.com/openwrt/openwrt/blob/master/package/utils/cli/files/usr/share/ucode/cli/utils.uc`
- Human reviewer to record in `reviewed_by`: pending human backfill review
- `last_reviewed` date to set at promotion: 2026-04-05
- Known caveats, limitations, or transitional edges: this page teaches native JSON file parsing in ucode, not streaming process output, not UCI mutation, and not shell-tier `jshn` usage.
