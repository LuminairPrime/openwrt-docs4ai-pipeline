Here is a changelog-style list of the specific improvements required to elevate the three Opus 4.6 documents from 9.5/10 to a flawless 10/10:

### 1. `mission-statement-opus46-v0.md`
**Goal:** Achieve true conciseness without losing the core message.
*   **Removed:** The `## What This Folder Contains` table. While highly useful, a directory map belongs in the `README.md`, not the mission statement. Removing it saves significant tokens.
*   **Condensed:** The `## How It Works` section. Consolidated the 7 steps into a tighter, 4-phase loop (Discovery/Generation -> Execution -> Scoring -> Authoring/Verification) to improve readability and reduce AI context window bloat.
*   **Refined:** Merged overlapping concepts in `## Key Principles` to ensure the document focuses strictly on the *why* and the high-level *how*, leaving the deep execution details to the numbered contract files.

### 2. `docs/plans/scoring-pipeline-implementation-opus46-v0.md`
**Goal:** Align the scoring plan with the new folder organization architecture.
*   **Changed:** Updated Phase 5 (`Create the V4 Strict Scoring Prompt`) and Phase 6 (`Create Failure-Synthesis Prompt`) to place the new prompt files in the centralized `prompts/` directory instead of `artifacts/scoring/`. 
*   **Added:** A new integration note in the prompt creation phases instructing the prompts to use relative paths (e.g., `../artifacts/scoring/openwrt-calibration-fixtures.md`) to reference their required schemas, cleanly decoupling the prompt execution logic from the data payloads.
*   **Added:** Explicit instructions in Phase 2 (`Standardize Answer Keys`) to include the *veracity source link* directly in the key file's `Scoring Notes` section, ensuring the human operator never loses the link between a test's answer key and the authentic OpenWrt repo code that backs it.

### 3. `docs/plans/folder-organization-opus46-v0.md`
**Goal:** Enforce absolute consistency in the centralization of prompts.
*   **Changed:** Overruled the decision to keep scoring prompts inside `artifacts/scoring/`. To achieve a strict separation of concerns, *all* `.md` prompt templates (including scoring and synthesis) must live in the `prompts/` directory. `artifacts/scoring/` should strictly only hold data (schemas, calibration fixtures, and the `haiku/` run results).
*   **Added:** A explicit mandate to delete `artifacts/templates/` entirely. The plan previously left it conditionally alive if the YAML file remained, but for a 10/10 clean architecture, the `00-scenario-admission-template.yaml` should be moved to `artifacts/scenario-packets/_template/` so the top-level `templates/` folder can be confidently destroyed. 
*   **Added:** A specific git-operation cross-reference check in the Migration Steps (Group E) to ensure that the new `latest_cookbook_staging.json` file is correctly formatted to match exactly what the master `docs4ai` pipeline's `05a` assembly script expects to ingest.