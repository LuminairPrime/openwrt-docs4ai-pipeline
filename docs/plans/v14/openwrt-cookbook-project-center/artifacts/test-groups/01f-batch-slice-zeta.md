# OpenWrt Cookbook Center Focused Reruns (Zeta Batch)

**Instructions:**
Read the following OpenWrt development scenario. Output the requested code snippet under a clear result header (for example `### Result for Scenario 16`). Provide a brief explanation of the libraries or architecture you chose.

---

## Scenario 16
Write an OpenWrt script that runs two continuous `ping` commands to two different IP addresses like 10.10.10.2 and 10.10.10.3 simultaneously (in parallel, not sequentially). It must capture their output asynchronously and print both ping results live to the screen, prefixing each output line with the target IP address so the two distinct streams are easily identifiable.
