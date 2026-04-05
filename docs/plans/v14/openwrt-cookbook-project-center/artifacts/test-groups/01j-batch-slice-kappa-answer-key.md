# Kappa Batch Answer Key

**Batch:** `01j-batch-slice-kappa.md`
**Type:** Canonical cookbook-center grouped answer key
**Scenarios:** 21

---

## Scenario 21 — ucidef helper WAN PPPoE boundary

**PASS criteria:** Must source `/lib/functions/uci-defaults.sh` and use `ucidef_set_interface_wan()` instead of raw `uci set` commands.

**Canonical Answer:**

```sh
#!/bin/sh

. /lib/functions/uci-defaults.sh

ucidef_set_interface_wan "dsl0" "pppoe"
```

**Pattern Notes:**

- this tests helper API selection, not generic raw network config editing
- raw `uci set network.wan...` answers fail the scenario
