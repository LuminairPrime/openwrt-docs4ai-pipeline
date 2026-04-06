# OpenWrt Cookbook Center Balanced Tests (Iota Batch)

**Execution Contract:**
- **Session isolation:** Run this batch in one fresh isolated agent session. Do not reuse a conversation that has already answered another grouped batch.
- **Clean-room boundary:** Do not use repository search, file-system read tools, browser tools, web search, or other external lookup methods to research answers. Do not read other files in this repository to infer the expected OpenWrt patterns. The only allowed filesystem action during a blind local run is writing the final compiled response to the designated raw-response artifact.
- **Output routing:** Web or chat agents without file-write access should return one markdown response in chat. Local IDE or CLI agents with file-write access should not create standalone code files, scratch scripts, or other extra artifacts in the repository; instead, write the complete compiled response to `artifacts/results/<agent-label>/<run-label>/iota/01-raw-response.md` relative to the repository root.
- **Answer shape:** Execute the following OpenWrt development scenarios sequentially inside this batch only. Output the requested code snippet for each scenario, clearly separated by headers (for example `### Result for Scenario 26`). Provide a brief explanation of the libraries or architecture you chose for each. Treat each scenario independently. Keep Scenario 17 last in this batch.

---

## Scenario 26
Write an OpenWrt shell snippet that sources the native shell JSON helper, loads a JSON string from `$payload`, enters the `network` object, reads the `proto` and `device` fields, then navigates back out cleanly.

---

## Scenario 27
Write a LuCI/OpenWrt JS snippet that calls the runtime network-interface dump over ubus and extracts the first non-loopback IPv4 address for the `lan` interface from the returned data structure.

---

## Scenario 17
What is OpenWrt ucode, why was it created, and what is it good for?
