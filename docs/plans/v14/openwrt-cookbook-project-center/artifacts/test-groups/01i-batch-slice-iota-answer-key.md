# Iota Batch Answer Key

**Batch:** `01i-batch-slice-iota.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 20

---

## Scenario 20 — uci-defaults mutation only

**PASS criteria:** Must be a `/etc/uci-defaults/` mutation-only script using `uci set`, `uci commit`, and `exit 0`, without any init-script call.

**Canonical Answer:**

```sh
#!/bin/sh

uci set myservice.@core[0].enabled='1'
uci commit myservice

exit 0
```

Place it in `/etc/uci-defaults/`, for example as `/etc/uci-defaults/90-myservice-enable`.

**Pattern Notes:**

- this is a firstboot config mutation boundary only
- calling `/etc/init.d/myservice start` or reload from this script fails the scenario
