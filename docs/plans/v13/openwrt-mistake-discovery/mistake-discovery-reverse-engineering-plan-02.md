# OpenWrt Mistake Discovery & Validation Plan (V2)

## 1. Objectives Overview
This plan outlines a pipeline to identify common mistakes AI agents make when generating OpenWrt code, categorize these errors to build comprehensive cookbook tutorials, and ultimately use these tests to validate the effectiveness of the `openwrt-docs4ai` project.

By comparing AI outputs in an isolated environment against an environment enriched by our documentation, we can definitively measure the ROI of our project.

## 2. A/B Testing the Docs4AI Package
The core validation loop relies on executing the same prompts in two distinct local environments:
*   **Control Agent (Baseline)**: A standard LLM operating with only its pre-trained knowledge base (no `openwrt-docs4ai` context).
*   **Test Agent (Enhanced)**: The same LLM executing with the `openwrt-docs4ai` package fully loaded into its context/RAG pipeline.

**Success Metric**: The Test Agent correctly uses modern OpenWrt paradigms (ucode, procd, JS) and compiles/runs successfully, while the Control Agent falls back on hallucinations, standard Linux tools (systemd, bash), or legacy OpenWrt code (Lua).

## 3. The "Ignorant" Prompting Strategy
To get a true measure of the AI's baseline knowledge, our test prompts must be as naive as possible. We will **not** constrain the AI with hints like "use modern libraries," "use ubus," or "don't use systemd." 

**Example Test Prompt:**
> "I need a script for my OpenWrt router that starts my custom C daemon `/usr/bin/my_daemon`, keeps it running if it crashes, and reads its configuration from a file. Then, I need a web page for the router's admin interface to change that configuration."

The Control Agent will likely write a `systemd` unit file or `/etc/init.d/` script using raw bash, and an old Lua-based LuCI view. The Test Agent (with our documentation) should correctly produce a `procd` init script, a UCI config definition, and a modern LuCI JS/Vue frontend.

## 4. Test Source Catalog & Sourcing Strategy
We will build a test suite directly derived from the official OpenWrt ecosystem repositories (e.g., `openwrt/packages`, `openwrt/luci/applications`). Each test will have a traceable origin.

**Catalog Structure (JSON or YAML list):**
Each entry in our test list will track the following details to ensure provenance and accuracy:
*   **Remote Source File/Folder**: Explicit URL to the GitHub source.
*   **Date Retrieved**: Snapshot date (e.g., 2026-03-28) to account for upstream changes.
*   **Explanation**: Brief description of the source feature's actual role in OpenWrt.
*   **Test Concepts**: A 1-to-N mapping. A single source directory can inspire multiple distinct test snippits.
    *   *Concept A (Init)*: Prompt the AI to build the daemon's startup script based on how the real package does it.
    *   *Concept B (Frontend)*: Prompt the AI to build the LuCI configuration view for that package.
    *   *Concept C (Backend)*: Prompt the AI to write the ubus RPC bindings.

## 5. Test Harness & Evaluation Methodology
Testing AI outputs automatically requires layered planning, balancing rigorous checks against implementation cost. We need specific standards to evaluate the generations.

*   **Static Source Analysis (Primary for Frontend/JS/LuCI)**
    *   *Why*: Spinning up an entire OpenWrt web server and simulating DOM interactions for every AI generation is too brittle and expensive.
    *   *How*: We will use code inspection techniques (AST parsers, linters, regex) to perform static analysis rather than full simulation.
    *   *Checks*: Does the source include `L.ui`? Does it call `luci.http`? Did the AI output a `.lua` file instead of a `.js` file? 
*   **Pattern Matching / Anti-Pattern Detection (Primary for Shell/Init)**
    *   *How*: Grep output for banned terms (`systemctl`, `chkconfig`, `bash`). Check for required OpenWrt boilerplate (`USE_PROCD=1`, `procd_open_instance`).
*   **Compilation / Syntax Checks (Primary for C/ucode)**
    *   *How*: Run the generated C code through `gcc -std=c99 -Wall -fsyntax-only` linked with OpenWrt staging headers (if available) to verify valid types. Pass generated ucode through the `ucode` binary interpreter for syntax validation (`ucode -c`).

## 6. Execution Layers (Next Steps)
Delivering this testing harness and the subsequent guidebook requires these layered planning steps:
1.  **Target Acquisition**: Mine the OpenWrt repos (`luci/applications`, core packages). Create the initial populated "Test Catalog" mapping remote sources to naive "ignorant" prompts.
2.  **Environment Setup**: Establish the two local agent testing setups (one with docs, one without).
3.  **Harness Implementation**: Write a simple Python/shell harness to pipe the ignorant prompts from the Catalog into the local agents, retrieve the outputs, and apply the static evaluation methodologies.
4.  **Data Gathering**: Run the harness. Generate a "Scoresheet" showing exactly where the Control Agent hallucinated compared to the Test Agent.
5.  **Cookbook Authorship**: Manually review the highest severity failures on the Scoresheet to author the mitigation chapters for the cookbook.
