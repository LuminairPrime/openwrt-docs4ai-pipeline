# OpenWrt Cookbook Subpipeline — Mission Statement

**Version:** v14 (successor to v13 mistake-discovery project)
**Date:** 2026-04-07
**Location:** `docs/plans/v14/openwrt-cookbook/`

---

## Mission

This folder is a pipeline for manufacturing concise, source-backed programming tutorials ("cookbooks") that fix the specific mistakes AI models make when programming for OpenWrt. AI models are not trained deeply on OpenWrt internals — ucode, procd, netifd, ubus, LuCI JS, rpcd, libubus, libubox — so they hallucinate APIs, misuse lifecycle patterns, and confidently produce broken code. The cookbooks correct these blind spots before a future AI encounters them, in as few tokens as possible so they fit in a context window without inflating it.

The pipeline works by systematically discovering what AI gets wrong, documenting the correct pattern from the actual OpenWrt source code, and proving the fix works. The proof of concept is validated: a v14 cookbook was verified as better than its v13 predecessor on the same topic.

---

## How It Works

The pipeline operates a single iterative loop with seven concrete steps:

1. **Discover** — Scan the OpenWrt codebase (ucode, LuCI, packages, procd, rpcd repos) for code worth testing. Reverse-engineer working implementations into blind test scenarios with golden answer keys.

2. **Batch** — Group test scenarios into domain-segregated batches (`artifacts/tests-batches/01a.md` through `01i.md`). Each batch mixes different OpenWrt domains so no single context insight steamrolls multiple answers. The human operator manages batch composition.

3. **Test** — Administer batches to AI agents in clean-room sessions: one batch per session, no search, no repo access, no answer keys. Each agent's raw output goes to `artifacts/results/<agent>/<run>/<batch>/`.

4. **Score** — Feed results to a strict scoring AI using a domain-agnostic prompt (`artifacts/scoring/openwrt-test-scoring-prompt-v4.md`, planned). The scorer has zero embedded OpenWrt knowledge — it only checks answers against the golden keys using rigid rules. **Crucially, using a less-intelligent scorer (like Haiku) reveals the scorer's own misunderstandings and hallucinations about OpenWrt. These scorer mistakes are captured separately as additional lessons** in a scorer-lessons log.

5. **Analyze** — Cluster failures by pattern using the failure-family framework (`04-failure-family-framework.md`). Identify which OpenWrt domains AI models consistently get wrong. Three systemic failure modes have been identified: lenience/drift (accepting architecturally wrong answers), hallucination (inventing code patterns), and fabrication blindness (trusting plausible-sounding but nonexistent APIs like `ubus_reply_create`).

6. **Author** — Write concise cookbook pages (700–1400 tokens) correcting each failure family. Every lesson must trace to the actual OpenWrt source — AI failures are signals, never the authority for what is correct. Staged drafts go through `artifacts/authoring/` with creation logs and human review records.

7. **Verify & Regenerate** — Re-run the same tests against an AI equipped with the new cookbook docs. If failures decrease, the cookbook works. Use lessons learned to improve existing tests, create new tests from uncovered code areas, and strengthen the answer keys. Repeat from step 1.

---

## Key Principles

**Failure-first.** Cookbook pages exist to remediate something a real AI agent actually got wrong in blind conditions. Tutorials for tasks that blind agents already solve correctly are not useful outputs.

**Source-backed.** Every cookbook lesson must be traceable to the actual OpenWrt codebase or official documentation. AI failures are discovery signals, not truth.

**Concise.** Target 700–1400 tokens per cookbook page. Front-load the correction: state the right pattern and the wrong pattern within the first 200 tokens.

**Clean-room testing.** Each AI takes tests in isolated sessions — one batch per session, no search, no repo access, no reading answer keys. This prevents context contamination and ensures honest measurement.

**Prompts as infrastructure.** Every pipeline step — test generation, scoring, do's/don'ts upgrades, veracity checks, cookbook authoring — needs a proven, recorded, documented AI prompt template that the human operator feeds to the relevant agent.

**Human-in-the-loop.** The human decides what to test, composes batches, reviews scored results, promotes cookbook pages, and decides when to regenerate. AI agents execute the steps; the human orchestrates the sequence.

---

## What This Folder Contains

| Path | Purpose |
|---|---|
| `README.md` | Operator quick-start: how to run batches, collect results, score, and promote |
| `mission-statement.md` | This document (once promoted from versioned drafts) |
| `00-openwrt-cookbook-project-center-operating-plan.md` | Master operating contract: loop model, decision rules, queue lifecycle |
| `01-current-cookbook-state-and-gap-map.md` | Cookbook corpus inventory and known gaps |
| `02-v13-lineage-and-migration-map.md` | Historical lineage from prior v13 project |
| `03-test-generation-contract.md` | Scenario admission rules, prompt-writing rules, grouped delivery |
| `04-failure-family-framework.md` | Taxonomy for deduplicating blind failures into families |
| `05-promotion-and-review-contract.md` | How scored failures become cookbook work |
| `06-test-bank-and-grouped-delivery.md` | 27-scenario inventory, 9 grouped batches, result layout per agent |
| `07-test-expansion-and-key-sourcing-plan.md` | Systematic test creation from authoritative sources |
| `08-cookbook-authoring-execution-contract.md` | How to author staged cookbook drafts from admitted scenarios |
| `09-staged-authoring-lifecycle.md` | Staging model: draft, creation log, review record, promotion |
| `10-human-review-procedure.md` | Human review checklist and promotion decision recording |
| `11-pipeline-step-catalog.md` | *(planned)* Numbered step reference with inputs/outputs per stage |
| `12-how-to-run.md` | *(planned)* End-to-end operator guide |
| `artifacts/` | Working surface: test batches, answer keys, scenario packets, results, scoring, authoring staging, registries, templates |
| `docs/plans/` | Implementation plans (scoring pipeline, folder reorganization) |
| `docs/development prompts/` | Prompts used to develop the pipeline itself |
| `tmp/` | Scratch analysis |

---

## Relationship to the Parent Pipeline

This cookbook subpipeline lives inside the `openwrt-docs4ai-pipeline` project. Its final output — a set of promoted cookbook pages — is published to `static/cookbook-source/` in the parent project root, where the main pipeline's stage `05a` assembles it into the release tree alongside wiki extracts, API references, and IDE schemas.

A JSON configuration marker (planned: `latest_cookbook_staging.json`) will point the parent pipeline to the latest validated cookbook staging path, or the human operator manually promotes accepted runs to the static source folder.

---

## Start Here

1. **Read this mission statement** — you're here.
2. **Read `README.md`** — operator quick-start for running test batches and collecting results.
3. **Read `00-openwrt-cookbook-project-center-operating-plan.md`** — the full operating contract with decision rules.
4. **Browse `artifacts/tests-batches/`** — see the actual test files that AI agents receive.
5. **Browse `artifacts/scoring/`** — see the scoring assessments and prompt evolution.

Every step in this pipeline has defined inputs, outputs, and responsibility assignments (human vs. AI). The `artifacts/` folder is the live execution surface — it changes with each pipeline run. The numbered contract files (00–10) at the root are durable operating agreements that change only when the pipeline design evolves.
