# OpenWrt Cookbook Center Balanced Tests (Epsilon Batch)

**Execution Contract:**
- **Session isolation:** Run this batch in one fresh isolated agent session. Do not reuse a conversation that has already answered another grouped batch.
- **Clean-room boundary:** Do not use repository search, file-system read tools, browser tools, web search, or other external lookup methods to research answers. Do not read other files in this repository to infer the expected OpenWrt patterns. The only allowed filesystem action during a blind local run is writing the final compiled response to the designated raw-response artifact.
- **Output routing:** Web or chat agents without file-write access should return one markdown response in chat. Local IDE or CLI agents with file-write access should not create standalone code files, scratch scripts, or other extra artifacts in the repository; instead, write the complete compiled response to `artifacts/results/<agent-label>/<run-label>/epsilon/01-raw-response.md` relative to the repository root.
- **Answer shape:** Execute the following OpenWrt development scenarios sequentially inside this batch only. Output the requested code snippet for each scenario, clearly separated by headers (for example `### Result for Scenario 13`). Provide a brief explanation of the libraries or architecture you chose for each. Treat each scenario independently.

---

## Scenario 13
Write an OpenWrt script snippet that safely reads an external JSON file from `/etc/my_app/config.json`, parses the data natively, and prints the value of the `startup_delay` key.

---

## Scenario 14
Write the modern OpenWrt LuCI menu definition snippet (JSON format) required to register a new menu tab under 'Network' called 'My Tool' that renders a specific Javascript view.

---

## Scenario 19
Write an OpenWrt hotplug script snippet that reacts only when the `wan` interface comes up, builds a structured JSON payload from the hotplug environment, and forwards it to a ubus method.
