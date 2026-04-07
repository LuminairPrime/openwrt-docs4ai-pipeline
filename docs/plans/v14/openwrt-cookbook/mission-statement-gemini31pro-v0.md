# OpenWrt Cookbook Pipeline - Mission Statement

**Version:** 2 (v14 Subpipeline)  
**Goal:** Establish an AI-first pipeline to generate highly concentrated, token-efficient programming documentation ("cookbooks") for the OpenWrt project.

## 1. The Core Problem
Most general-purpose Large Language Models (LLMs) have a relatively shallow training subset regarding OpenWrt internal systems (e.g., `ucode`, `procd`, `netifd`, `ubus` integrations). As a result, when AIs are tasked with OpenWrt development, they frequently hallucinate APIs, misuse patterns, and confidently produce broken code.

## 2. The Solution Mechanism
To fix AI performance on OpenWrt, we must aggressively target what they are *bad* at and provide concise corrections before they write code. This is accomplished through a defined loop:

1. **Source Discovery:** Reverse-engineer established, working OpenWrt code to understand the correct implementation.
2. **Test Generation:** Ask an AI to recreate this functionality from scratch.
3. **Execution & Mistake Capture:** Capture the AI's generated code and grade it, specifically cataloging its recurring errors and hallucinations.
4. **Cookbook Generation:** Based on the common failures, construct extremely concise, tutorial-style "cookbooks" focused directly on correcting these specific AI blind spots.
5. **Validation:** Direct the AI to re-take the test using the newly generated cookbook. A successful test proves the utility of the generated docs.

## 3. Operational Advantages
* **"Affordable" AI Scorers:** We intentionally use fast, capable-but-not-cutting-edge models (like Claude 3 Haiku / Claude 3.5 Haiku) for test scoring. Their misunderstandings and errors in grading provide a *second layer* of intelligence regarding how lower-tier agents misinterpret OpenWrt concepts, informing the final cookbook material.
* **Batching Strategy:** Human operators organize test files into sensibly sized, domain-segregated batches. This ensures each AI testing run operates in a "clean room" context without accidentally inheriting the solution from an unrelated prompt in its context window.
* **Small Context Inflation:** Cookbooks must be structurally concise to fit easily into AI developer system prompts without wasting tokens or diluting focus.

## 4. Pipeline Execution & Human Interaction
This pipeline relies on systematic, documented steps where the human operator orchestrates the progression using verified AI prompts. 

* **Prompts as Infrastructure:** Every step—from scanning code, to generating tests, to scoring results, to summarizing failures—relies on established, documented prompt templates. 
* **Sequential Processing:** Future pipeline actions are categorized into numeric stages (e.g., `00-`, `01-`) so operators know exactly which inputs yield the necessary outputs for the next step.
* **Final Delivery:** The ultimate output is a `staging` folder containing generated `cookbooks-RANDOM_NUMBER` files. A JSON configuration file will act as a pointer to the most recently validated, "golden" cookbook staging path, allowing the master `docs4ai` pipeline to retrieve its final documentation artifact.

Ultimately, this project systematically harvests real-world OpenWrt AI development failures and transmutes them into a unified knowledge base explicitly tailored to guide future AI coding agents.
