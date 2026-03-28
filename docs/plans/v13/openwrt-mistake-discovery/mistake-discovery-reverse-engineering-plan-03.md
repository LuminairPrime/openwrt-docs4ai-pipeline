# OpenWrt Mistake Discovery & Validation Plan (V3)
## The Detailed Source-to-Test Strategy & Evaluation Framework

## 1. Balancing Source Inspiration vs. Test Generation
To effectively test AI capabilities across OpenWrt's unique languages without overwhelming our own evaluation harness, we must balance the number of source files utilized against the volume of test prompts generated. 

*   **The Problem:** Repositories like `openwrt/luci` are overwhelmingly populated with pure JavaScript files. If we only scrape LuCI, our test suite will be 95% JS, providing no insight into the AI's ability to handle C-based `rpcd` plugins or `ucode` scripting.
*   **The Strategy (Ratio):** We will select roughly **5 remote source packages/folders**, ensuring exactly 1 from each language domain (Shell, uCode, C, JS). Each selected remote source will spawn **2 to 3 distinct Test Concepts** (e.g., prompt for the init script, then prompt for the RPC binding).
*   **Total Scope:** ~5 Source Archetypes -> ~15 Naive Prompts. This provides a statistically significant but manageable dataset to evaluate our `openwrt-docs4ai` RAG performance.

## 2. Backup Repositories
If the primary `openwrt/openwrt` and `openwrt/luci` repositories do not yield clear enough snippets, our fallback strategy will utilize:
1.  **`openwrt/packages`**: Abundant with C daemons and LuCI app backends (e.g., `rpcd-mod-*` extensions).
2.  **`openwrt/routing`**: Excellent source for advanced C-based routing daemons and netifd integration.

## 3. Concrete Test Catalog Examples
*Note: The dates and links below reflect our initial snapshot from the live OpenWrt repositories during planning.*

### Target 1: The Core Shell Daemon (`procd` / `uci`)
*   **Remote Source:** `openwrt/openwrt` -> `package/base-files/files/etc/init.d/system`
*   **Link:** [init.d/system](https://github.com/openwrt/openwrt/blob/master/package/base-files/files/etc/init.d/system)
*   **Date Retrieved:** 2026-03-28
*   **Explanation:** The fundamental OpenWrt system initialization script. It uses `procd_open_instance` and `uci_load_validate` to read `/etc/config/system` and apply the timezone/hostname.
*   **Test Concept A (Init Generation):** 
    > *"Write a startup script that runs at boot. It needs to start '/sbin/my_daemon' and restart it if it crashes. It should also read the 'hostname' variable from a configuration file and apply it."* (Look for failure to use `USE_PROCD=1`).
*   **Test Concept B (Validation Generation):** 
    > *"Write a script function to validate that a configuration file has a valid integer for 'loglevel' before starting the service."* (Look for failure to use `uci_load_validate`).

### Target 2: The Modern Scripting Backend (`ucode` / `ubus`)
*   **Remote Source:** `openwrt/openwrt` -> `package/network/utils/wireguard-tools/files/wireguard.uc`
*   **Link:** [wireguard.uc](https://github.com/openwrt/openwrt/blob/master/package/network/utils/wireguard-tools/files/wireguard.uc)
*   **Date Retrieved:** 2026-03-28
*   **Explanation:** A modern `ucode` script used to interface with `ubus` network objects and manage WireGuard interfaces dynamic state.
*   **Test Concept A (RPC Invocation):**
    > *"Write a script to list all active network interfaces by asking the system bus, and print their IP addresses in JSON format."* (Look for AI using Python or Lua instead of ucode, or failing to import `ubus`).

### Target 3: The C-Backend Plugin (`libubus` / `rpcd`)
*   **Remote Source:** `openwrt/packages` -> `utils/rpcd-mod-wireguard/src/api.c`
*   **Link:** [rpcd-mod-wireguard/api.c](https://github.com/openwrt/packages/blob/master/utils/rpcd-mod-wireguard/src/api.c)
*   **Date Retrieved:** 2026-03-28
*   **Explanation:** An RPC daemon plugin written in C. It exposes standard Linux WireGuard properties securely to the LuCI web interface via `ubus`.
*   **Test Concept A (RPC Object Registration):**
    > *"I am writing a C plugin daemon. Write the C code required to register a new system API module called 'my_plugin' that has one method called 'getStatus'."* (Look for AI failing to include `<libubus.h>` or hallucinating a generic REST API server).

### Target 4: The JavaScript Frontend (`LuCI` / `L.ui`)
*   **Remote Source:** `openwrt/luci` -> `applications/luci-app-firewall/htdocs/luci-static/resources/view/firewall/zones.js`
*   **Link:** [firewall/zones.js](https://github.com/openwrt/luci/blob/master/applications/luci-app-firewall/htdocs/luci-static/resources/view/firewall/zones.js)
*   **Date Retrieved:** 2026-03-28
*   **Explanation:** A standard LuCI configuration interface using modern OpenWrt JS paradigms. It dynamically renders a form mapped to UCI configuration without legacy Lua.
*   **Test Concept A (View Rendering):**
    > *"Write a web page for my router's admin panel. It needs to have a form that lets the user change their firewall zone settings and save them."* (Look for AI generating HTML/PHP, legacy Lua CBI, or React instead of a `luci.view` extending `form.Map`).

## 4. AI-Driven Evaluation Framework
Instead of relying purely on complex static analysis tools or rigid regex parsing, we will leverage an **Evaluating Agent** to rigorously audit the outputs of the **Generating Agent**. This multi-agent debate dynamic allows us to scale testing quickly while still detecting nuanced architectural mistakes.

### 4.1. The Testing Loop
1.  **Generation Phase:** Provide Prompt X (a Naive Prompt from our Catalog) to the Generating Agent. It outputs raw source code.
2.  **Audit Phase:** The Evaluating Agent is supplied with:
    *   The original Request (Prompt X)
    *   The generated source code from the Generating Agent
    *   An Evaluation Prompt containing strict OpenWrt architectural rules and the "Known Good" source material we mapped in our Catalog.
3.  **Reporting Phase:** The Evaluating Agent analyzes the submission and generates a structured output file (JSON or YAML) answering two core criteria:
    *   `passed`: Boolean (True/False).
    *   `failure_explanation`: If false, a detailed breakdown of what standard was violated.
    *   `classified_error_types`: An array of error string tags mapping back to our Taxonomy Library (see below).

### 4.2. The Failure Taxonomy Library
To transform arbitrary failures into actionable documentation fixes, we will classify mistakes against a predefined library of Error Categories. Every failure picked up by the Evaluating Agent must be assigned one or more of these tags. As we run tests, this library will naturally expand to catch new unforeseen AI ignorance.

**Initial Failure Taxonomy / Categories:**
*   `ERR_LINUX_HALLUCINATION`: The AI fell back on standard Linux utilities (`apt`, `systemd`, `ip`, `ifconfig`) instead of OpenWrt equivalents (`opkg`, `procd`, `ubus`, `netifd`).
*   `ERR_LEGACY_API`: The AI used deprecated OpenWrt architecture (e.g., Lua for frontend views instead of `luci.view` JS, or raw `sh` instead of `ucode`).
*   `ERR_MISSING_BOILERPLATE`: The AI missed mandatory OpenWrt structure elements (e.g., missing `procd_open_instance` in an init script, or forgetting `#include <libubus.h>`).
*   `ERR_STATE_MANAGEMENT`: The AI tried to maintain state via flat files in `/etc/` or `/tmp/` rather than utilizing the `uci` configuration system dynamically.

### 4.3. Creating Mitigations (The "Fix")
Once an AI completes a test cycle, the test harness will aggregate the `classified_error_types`. We will then use these frequencies to author the final `docs4ai` product:
*   If `ERR_LINUX_HALLUCINATION` is highly prevalent in daemon generation, we will author a specific `openwrt-docs4ai` module titled: *"Translating Standard Linux Daemons into OpenWrt Procd Instances."*
*   If `ERR_LEGACY_API` occurs often in LuCI frontend tests, we will author a cookbook section on: *"Migrating from Lua CBI to Modern JavaScript LuCI Views."* 

This ensures our documentation product is entirely data-driven, directly patching the most critical intelligence gaps in current foundational models rather than addressing theoretical problems.
