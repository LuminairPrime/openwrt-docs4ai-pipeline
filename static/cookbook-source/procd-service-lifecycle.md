---
title: procd Service Lifecycle
description: Complete guide to writing a procd-managed init script for an OpenWrt service, covering the full lifecycle from start to reload to stop with supervised respawn.
module: cookbook
origin_type: authored
when_to_use: Use when writing a new /etc/init.d/ script that must integrate with the OpenWrt procd process supervisor for automatic respawn, controlled signal handling, and UCI-trigger-based reload.
related_modules: [procd, uci, wiki]
era_status: current
verification_basis: Corpus review of procd module (header_api-procd-api.md); wiki procd-init-scripts and procd-init-script-example pages; upstream procd.sh source via corpus
reviewed_by: placeholder
last_reviewed: 2026-03-23
---

# procd Service Lifecycle

> **When to use:** Use when writing a new `/etc/init.d/` service script on OpenWrt 23.x+. procd is the init system and process supervisor. It replaces sysvinit start/stop/restart patterns with a declarative instance model where the supervisor handles respawn, signals, and config-triggered reloads automatically.
> **Key components:** procd, UCI, bash
> **Era:** Current (23.x+). Sysvinit-style `start-stop-daemon` patterns do not integrate with procd supervision and are not covered here.

## Overview

procd is OpenWrt's init system and process supervisor. Unlike sysvinit, procd manages processes declaratively: you declare a service with its command, environment, and respawn policy, then procd supervises it. The supervisor restarts crashed processes, handles reload signals, and triggers config-aware restarts when UCI configuration changes.

Every `/etc/init.d/` script on a current OpenWrt system uses the procd API via sourcing `/lib/functions.sh` (which transitively loads the procd helper functions). The API is provided by `procd.sh` and exposes a small set of functions for declaring service instances.

The lifecycle is three phases: **start_service** (declare the supervised instance), **stop_service** (optional override; procd handles SIGTERM by default), and **reload_service** or **service_triggers** (UCI-aware reload without full restart). When the service depends on typed UCI config, the lifecycle also needs a validation boundary: `uci_load_validate` should sanitize and coerce config before procd ever launches the daemon.

## Complete Working Example

Below is a complete, annotated procd init script for a hypothetical service called `myapp` that reads config from `/etc/config/myapp` and runs as a dedicated user.

```bash
#!/bin/sh /etc/rc.common
# /etc/init.d/myapp
# USE_PROCD=1 tells rc.common to delegate lifecycle to procd functions
# instead of sysvinit start/stop/restart shims.

USE_PROCD=1

# START and STOP define the boot sequence priority (lower = earlier)
START=95
STOP=01

# start_service() is called by procd when the service should launch.
# procd_open_service / procd_close_service bracket the declaration.
start_service() {
    # Load config from UCI to pass as environment or arguments
    config_load 'myapp'

    local port
    config_get port main port '8080'   # default to 8080 if option not set

    # Open a service declaration for 'myapp'
    procd_open_service myapp

    # Declare one supervised process instance (name defaults to "instance1")
    procd_open_instance

    # Set the command to run. Each argument is a separate array element.
    procd_set_param command /usr/bin/myapp --port "$port"

    # Respawn policy: fail_threshold(s) restart_timeout(s) max_fail
    # If the process fails within 3600s more than 5 times, stop respawning.
    procd_set_param respawn 3600 5 5

    # Redirect stdout and stderr to syslog (facility: daemon)
    procd_set_param stdout 1
    procd_set_param stderr 1

    # Optional: file triggers -- if these files change, procd reload_config
    # will trigger a service reload (used for non-UCI config files)
    # procd_set_param file /etc/myapp/extra.conf

    procd_close_instance
    procd_close_service
}

# service_triggers() declares which UCI config changes trigger a reload.
# When 'uci commit myapp' is run, procd will call reload_service.
service_triggers() {
    procd_add_reload_trigger 'myapp'
}

# reload_service() is called instead of stop/start when a trigger fires.
# Default behavior (omitting this function) is to call stop_service
# then start_service. Override only if you need a graceful in-process
# reload (e.g., sending SIGHUP to reload config without process restart).
reload_service() {
    stop
    start
}
```

## Step-by-Step Explanation

### `USE_PROCD=1`

This flag tells `/etc/rc.common` (the shell shim that backs all init scripts) to use procd delegation mode. Without it, the script uses legacy sysvinit-style `start`/`stop`/`restart` functions. **Always set this flag.** Forgetting it is the single most common procd init script mistake.

### `START` and `STOP`

Boot sequence priorities. `START=95` means this service starts late in the boot sequence (after networking, after UCI defaults have been applied). `STOP=01` means it stops early during shutdown. Adjust these to match your service's dependency order.

### `procd_open_service` / `procd_close_service`

These bracket the full service declaration. The argument to `procd_open_service` is the service name used in `procd_running()` checks and in logread output.

### `procd_open_instance` / `procd_close_instance`

These bracket a single process instance. One service can have multiple instances (e.g., two daemons that together form one logical service). Each instance gets its own supervised process.

### `procd_set_param command`

Sets the command and arguments. Each argument is a **separate shell argument** — no string concatenation or quoting tricks. Incorrect quoting here causes the process to launch with wrong arguments without any shell error.

### `procd_set_param respawn`

The three values are:
- `fail_threshold`: time window in seconds during which failures are counted
- `restart_timeout`: time in seconds between restart attempts
- `max_fail`: maximum failures before supervision is abandoned

Setting `max_fail 0` means infinite restarts. Setting it to 5 means the process is abandoned after 5 failures in the time window.

The example values in this page are illustrative, not universal defaults. Keep the pattern, but tune the thresholds and restart timeout for the actual daemon's failure mode and recovery cost.

### `service_triggers` and `procd_add_reload_trigger`

This is the UCI integration point. `procd_add_reload_trigger 'myapp'` means: whenever `uci commit myapp` is called (by any process), procd will call this service's `reload_service` function. Without this, config changes require manual `service myapp restart`.

### Typed UCI validation with `uci_load_validate`

Use `uci_load_validate` when the service cannot safely treat config values as unchecked strings. This is the current-era OpenWrt pattern for typed config validation inside a procd init script.

```bash
validate_myapp_section() {
    uci_load_validate "myapp" "myapp" "$1" "$2" \
        'enabled:bool:0' \
        'loglevel:uinteger:4' \
        'listen_port:port:8080'
}

load_myapp() {
    local section="$1"

    [ "$2" = 0 ] || {
        echo "validation failed for section $section" >&2
        return 1
    }

    [ "$enabled" = "1" ] || return 0

    procd_open_instance
    procd_set_param command /usr/bin/myapp --loglevel "$loglevel" --port "$listen_port"
    procd_set_param respawn
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_close_instance
}

start_service() {
    config_load "myapp"
    config_foreach validate_myapp_section "myapp" load_myapp
}

service_triggers() {
    procd_add_reload_trigger "myapp"
    procd_add_validation validate_myapp_section
}
```

What this does:

- `uci_load_validate` checks the section against typed rules before launch
- validated option values are exported into local shell variables like `$loglevel`
- `config_foreach` ties validation and instance creation together per section
- `procd_add_validation` registers the validator so config-driven reload paths stay aligned with the same schema

Use this pattern instead of hand-written `grep`, `awk`, or regex parsing against `/etc/config/myapp`. Those generic shell checks bypass the OpenWrt validation contract and drift quickly when the config evolves.

## Anti-Patterns

### WRONG: sysvinit-style start/stop without USE_PROCD

```bash
#!/bin/sh /etc/rc.common
START=95
STOP=01

start() {
    start-stop-daemon -S -x /usr/bin/myapp -- --port 8080
}

stop() {
    start-stop-daemon -K -x /usr/bin/myapp
}
```

**Why it fails:** This script runs `myapp` as a child of the init script, not under procd supervision. If `myapp` crashes, it is not restarted. If `myapp` is already running when `start` is called, `start-stop-daemon` behavior depends on PID file presence. There is no UCI reload integration. The `/lib/functions.sh` config helpers (`config_load`, `config_get`) are available but the result is a script that runs outside the procd model entirely.

### CORRECT: USE_PROCD with procd_set_param

Use `USE_PROCD=1` and the procd API as shown in the working example above. The key behavioral differences:
- procd tracks the PID and supervises it directly
- crashes trigger automatic respawn per the declared policy
- `service myapp reload` triggers `reload_service` without a full restart
- `procd_running myapp` can check status from other scripts

### WRONG: Hardcoding config values in the command

```bash
procd_set_param command /usr/bin/myapp --port 8080 --host 192.168.1.1
```

**Why it fails:** Config changes require editing the init script. UCI integration is bypassed. The standard OpenWrt pattern is to load config via `config_load` in `start_service` and pass values as environment variables or arguments derived from UCI.

### CORRECT: Load from UCI in start_service

```bash
start_service() {
    config_load 'myapp'
    local port
    config_get port main port '8080'
    procd_open_service myapp
    procd_open_instance
    procd_set_param command /usr/bin/myapp --port "$port"
    # ...
    procd_close_instance
    procd_close_service
}

service_triggers() {
    procd_add_reload_trigger 'myapp'
}
```

### WRONG: Validating with grep or regex against `/etc/config/`

```bash
start_service() {
    local loglevel
    loglevel="$(grep "option loglevel" /etc/config/myapp | awk '{ print $3 }')"
    echo "$loglevel" | grep -Eq '^[0-9]+$' || return 1

    procd_open_instance
    procd_set_param command /usr/bin/myapp --loglevel "$loglevel"
    procd_close_instance
}
```

**Why it fails:** UCI config is not meant to be parsed as ad hoc text inside init scripts. This bypasses the validation helpers shipped with procd, makes anonymous sections awkward, and breaks as soon as quoting, defaults, or option types evolve.

## Running user and resource limits

```bash
# Run the service as a non-root user (user must exist on the system)
procd_set_param user nobody
procd_set_param group nogroup

# Optional: set resource limits (ulimit-style)
procd_set_param limits "nofile=1024"
```

Drop privileges by setting `user` and `group` parameters. These are applied before `execve`. The user must exist in `/etc/passwd` on the target image — if it does not exist at boot time, procd will refuse to start the service.

## Related Topics

- [procd API Reference](../procd/header_api-procd-api.md) — full parameter list for `procd_set_param`
- [OpenWrt Era Guide](./openwrt-era-guide.md) — init system era context (sysvinit vs procd)
- [UCI Read/Write from ucode](./uci-read-write-from-ucode.md) — companion guide for config access from ucode plugins
- [Architecture Overview](./architecture-overview.md) — where procd fits in the full component stack

## Verification Notes

- procd API (`procd_open_service`, `procd_open_instance`, `procd_set_param`, etc.) verified against `procd/header_api-procd-api.md` in corpus
- `procd_add_reload_trigger` function name verified from same source
- `uci_load_validate()` helper signature verified from `tmp/authoring-repos/repo-openwrt-full/package/system/procd/files/procd.sh`
- real `uci_load_validate` call shape verified from `tmp/authoring-repos/repo-packages/utils/rtl-ais/files/rtl_ais.init` and `tmp/authoring-repos/repo-packages/net/aria2/files/aria2.init`
- `USE_PROCD=1` pattern and `service_triggers` function verified from `wiki/wiki_page-guide-developer-procd-init-scripts.md` file listing
- respawn parameter order (fail_threshold, restart_timeout, max_fail) matches procd corpus documentation
- Scenario packet reference for this extension: `docs/plans/v14/openwrt-cookbook-project-center/artifacts/scenario-packets/04-scn-2026-004-procd-uci-load-validate-loglevel.yaml`
- Known limitation: `reviewed_by` remains `placeholder` until a human maintainer claims final reviewer ownership

