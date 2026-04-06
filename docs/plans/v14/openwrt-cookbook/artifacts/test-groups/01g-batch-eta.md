# OpenWrt Cookbook Center Balanced Tests (Eta Batch)

**Execution Contract:**
- **Session isolation:** Run this batch in one fresh isolated agent session. Do not reuse a conversation that has already answered another grouped batch.
- **Clean-room boundary:** Do not use repository search, file-system read tools, browser tools, web search, or other external lookup methods to research answers. Do not read other files in this repository to infer the expected OpenWrt patterns. The only allowed filesystem action during a blind local run is writing the final compiled response to the designated raw-response artifact.
- **Output routing:** Web or chat agents without file-write access should return one markdown response in chat. Local IDE or CLI agents with file-write access should not create standalone code files, scratch scripts, or other extra artifacts in the repository; instead, write the complete compiled response to `artifacts/results/<agent-label>/<run-label>/eta/01-raw-response.md` relative to the repository root.
- **Answer shape:** Execute the following OpenWrt development scenarios sequentially inside this batch only. Output the requested code snippet for each scenario, clearly separated by headers (for example `### Result for Scenario 16`). Provide a brief explanation of the libraries or architecture you chose for each. Treat each scenario independently.

---

## Scenario 16
Write an OpenWrt script that runs two continuous `ping` commands to two different IP addresses like 10.10.10.2 and 10.10.10.3simultaneously (in parallel, not sequentially). It must capture their output asynchronously and print both ping results live to the screen, prefixing each output line with the target IP address so the two distinct streams are easily identifiable.

---

## Scenario 21
Write an OpenWrt board-defaults shell snippet that uses the helper APIs from `/lib/functions/uci-defaults.sh` to declare the WAN interface on `dsl0` with protocol `pppoe`, instead of writing raw `uci set` commands.

---

## Scenario 23
Write the OpenWrt `Package/install` snippet for a package that needs to ship a LuCI JS view, an ACL file, an rpcd helper, a `/etc/config/` file, and a `/etc/uci-defaults/` bootstrap script.
