# Mistake Discovery & Reverse Engineering Plan (Initial Concept)

This document captures the initial brainstorming and discussion for the OpenWrt mistake discovery and reverse engineering plan.

## 1. The Strategy: Full Packages vs. Code Snippets

**The Code Snippet Approach (Recommended for Volume & Discovery)**
*   **Why it works:** OpenWrt development isn't just one language; it's an orchestration of highly specific APIs (`uci`, `ubus`, `procd`, `LuCI/JS`). Testing snippets allows us to isolate these APIs. For example, testing "how effectively can an AI parse a UCI config file in C using `libuci`?"
*   **The benefit:** Fast generation, cheap API costs, and easy side-by-side static comparison against the "known good" original source. You can blast 10 models with 10 paradigms and instantly see where they hallucinate standard Linux tools instead of OpenWrt tools.

**The Full Package Approach (Recommended for Architectural Validation)**
*   **Why it works:** Packages test the "glue." Can the AI write the `Makefile`, the `procd` init script, the `ucode` backend, and the `JS` frontend, and wire them all together?
*   **The benefit:** This reveals higher-level architectural misunderstandings.
*   **Recommendation:** Use **Snippets** to discover 90% of the API-level mistakes and write the core cookbook. Reserve just **2 small Full Packages** as a "Final Exam" to test if an AI, when equipped with your new cookbook, can successfully generate a working package from scratch.

## 2. Taxonomy of OpenWrt Paradigms (Snippet Selection Criteria)

To get broad coverage, we should pull our snippets and packages from these core OpenWrt domains. When selecting source material, we should look for code that strictly adheres to the modern standards (e.g., JS/ucode over Lua).

1.  **LuCI Frontend (JavaScript/Vue):**
    *   *Snippet idea:* A basic `luci.http` request/response.
    *   *Snippet idea:* A `LuCI CBI` (Configuration Binding Interface) form rendering a UCI model in JS.
2.  **ubus / Backend Scripting (ucode / shell):**
    *   *Snippet idea:* An `/etc/init.d/` standard `procd` script that sets up a service instance, reads UCI, and respawns.
    *   *Snippet idea:* A `ucode` script invoking a `ubus` method to list network interfaces and parsing the JSON.
3.  **C System Daemons (Default core, like `procd` or `netifd`):**
    *   *Snippet idea:* A C function utilizing `libubus` to register an object and expose a method.
    *   *Snippet idea:* A C function utilizing `libuci` to iterate over sections in a config file.
4.  **C Backend Plugins/Extensions (Addons):**
    *   *Snippet idea:* Writing an `rpcd` (RPC Daemon) plugin in C to expose a custom shell command to the web interface.

## 3. The Reverse-Engineering Prompt Design

To accurately measure AI ignorance, the prompt itself must be meticulously designed to provide *just enough* functional requirement context without giving away the OpenWrt-specific API answers. 

**Drafting a Unified Prompt Template:**
> "You are an expert OpenWrt embedded Linux developer. Your task is to implement the following specific component for an OpenWrt environment.
>
> **Task Description:** [Insert functional description of the snippet, e.g., 'Write a procd init script that starts /usr/bin/mydaemon, reads the 'port' option from the 'myservice' uci file, and restarts on crash.']
>
> **Constraints:**
> 1. You MUST use modern OpenWrt paradigms, tools, and libraries (e.g., ubus, uci, procd). Do not use standard Linux alternatives like systemd or standard bash if an OpenWrt native tool exists.
> 2. Write only the precise code snippet required. 
> 3. After the code, provide a brief 'Developer Log' detailing any assumptions you made about the OpenWrt APIs, and any OpenWrt-specific documentation you felt you were lacking or unsure about."

## 4. Evaluating Mistakes & Building the Guides

Once we have the AI outputs, evaluating them becomes a pattern-matching game against the original source code. 

**Anticipated Classes of Mistakes (The "Gotchas"):**
*   **The "Standard Linux" Hallucination:** Using `systemctl`, `apt-get`, or standard `bashrc` instead of `procd`, `opkg`, and `uci`.
*   **The "Legacy Code" Trap:** Generating `Lua` code for LuCI instead of modern `LuCI-app-JS / ucode`.
*   **Missing Boilerplate:** Failing to include necessary C headers (`#include <uci.h>`), or missing the `procd_open_instance` call in an init script.

**Guide / Cookbook Structure:**
We will research top-tier engineering cookbooks (like *Effective C++* or *Python Cookbook*), but a highly effective structure for AI-training cookbooks usually involves:
1.  **The Anti-Pattern (What AIs usually get wrong):** Show the common hallucinated code.
2.  **The OpenWrt Standard (The Solution):** Show the correct API usage.
3.  **The 'Why':** Explain the architecture (e.g., "Why we use uci instead of flat files").
4.  **RAG/Agent Context:** Bullet points directly formatted for an AI agent's system prompt (e.g., for the future `openwrt-backend` agent).

## 5. Proposed Next Steps (Phase 1 Deliverables)

1.  **The Snippet Target List:** Define 10 specific code snippet scenarios (covering JS, ucode, C libuci, C libubus, procd) and locate them in the actual OpenWrt/LuCI source trees.
2.  **The Package Target List:** Identify 2 small, modern, well-written packages (perhaps one simple LuCI app, and one C-daemon) to use as the final "architectural" test.
3.  **Prompt Generation:** Formalize the exact prompts we will use for the 10 snippets.
