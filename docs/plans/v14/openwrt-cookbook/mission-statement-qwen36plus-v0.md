# OpenWrt Cookbook Subpipeline — Mission Statement

**Version:** v14  
**Date:** 2026-04-07  
**Scope:** `docs/plans/v14/openwrt-cookbook/`

---

## Purpose

AI models are not trained on OpenWrt development. Even the best models make mistakes when programming for OpenWrt — they use deprecated Lua CBI patterns instead of LuCI JS, invent non-existent ubus APIs, manage service lifecycles with generic Linux init habits instead of procd, and mishandle ucode's native runtime.

This subpipeline exists to find those mistakes, reverse-engineer the correct patterns from the open-source OpenWrt codebase, and produce concise, potent cookbook tutorials that correct each mistake before a future AI encounters it.

**The mission:** Turn blind AI failures on OpenWrt tasks into durable, source-backed cookbook pages that teach the correct OpenWrt programming pattern — in as few characters as possible, so they fit in an AI tool's context window without inflating it.

---

## Why This Matters

The OpenWrt project's source code is open and available, but its repos are scattered across the internet and unorganized. Generic AI models trained on broad code corpora lack focused OpenWrt expertise. When an AI developer works on OpenWrt, most of its work (C programming, shell scripting, JSON parsing) is fine — but when it hits something OpenWrt-specific (ucode functions, procd init scripts, LuCI JS views, ubus RPC declarations), it makes predictable, repeatable mistakes.

This subpipeline systematically discovers those mistakes, documents the correct patterns, and feeds the lessons back into the main docs4ai pipeline so future AI tools have a fighting chance.

---

## How It Works: Three Linked Loops

### Loop A: Truth Capture

We define what is correct and false in current-era OpenWrt by studying the upstream source code, the existing cookbook corpus, archive evidence, and maintaining a golden answer key. Every claimed paradigm must be traceable to a live source or named historical evidence packet.

**Inputs:** Upstream OpenWrt code, LuCI, packages, procd, rpcd, libubus, libubox repos; existing cookbook corpus; archive threads and mailing-list evidence.

**Outputs:** Golden answer keys, scenario packets with authority sources, failure-family registries.

### Loop B: Blind Failure Measurement

We design scenarios that test one bounded OpenWrt lesson in blind form — no search, no repo access, no hints. We run these scenarios against AI agents (starting with the weakest viable model) and score the results against the frozen truth inputs.

**Inputs:** Admitted scenario packets, grouped batch prompt files, clean-room AI agent sessions.

**Outputs:** Raw responses per agent per batch, scored failure records, per-agent scorecards.

### Loop C: Remediation Promotion

We group failures into families (e.g., "service lifecycle belongs to procd, not generic Linux init"), decide whether each failure warrants cookbook treatment, author or extend cookbook pages, and verify that the new docs actually fix the lesson.

**Inputs:** Scored failures, failure-family registry, cookbook gap map, authority sources.

**Outputs:** Staged cookbook drafts, creation logs, review records, promoted pages in `static/cookbook-source/`, verification results.

---

## The Test-Scoring-Regeneration Loop

A core innovation of this subpipeline is its closed-loop test lifecycle:

1. **Generate tests** — Find OpenWrt code snippets, reverse-engineer them into blind test scenarios with answer keys.
2. **Administer tests** — Give batches of tests to AI agents in clean-room sessions (one batch per session, no cross-contamination).
3. **Score results** — Use a strict, domain-agnostic scoring AI (like Haiku) to evaluate answers against the golden keys. The scorer's own mistakes and hallucinations are captured as additional lessons.
4. **Analyze mistakes** — Cluster failures by pattern, identify which OpenWrt domains AI models consistently get wrong.
5. **Author cookbooks** — Write concise tutorials correcting each mistake family, sourced from the actual OpenWrt codebase.
6. **Verify** — Re-run the same tests against an AI equipped with the new cookbook docs. If failures decrease, the cookbook works.
7. **Regenerate** — Use the lessons learned to improve existing tests, create new tests from uncovered code areas, and strengthen the answer keys.

This loop repeats indefinitely. Each iteration grows the golden dataset, strengthens the cookbooks, and improves the test bank.

---

## Key Principles

### One Failure Is Enough

A single blind, source-backed, OpenWrt-specific failure is sufficient to open cookbook work. Repeated failures raise priority but are not required for admission.

### Failure-First

Cookbook pages exist to remediate something a real AI agent actually got wrong in blind conditions. Tutorials for tasks that blind agents already solve correctly are not useful outputs.

### Source-Backed

Every cookbook lesson must be traceable to the actual OpenWrt codebase or official documentation. AI failures are signals that a lesson may be missing — never the authority for what is correct.

### Concise

Cookbook pages target 700–1400 tokens. They must be small enough to fit in an AI context window without bloating it. Front-load the correction: state the right pattern and the wrong pattern within the first 200 tokens.

### Clean-Room Testing

Each AI agent takes tests in isolated sessions — one batch per session, no search, no repo access, no reading answer keys. This prevents context contamination and ensures honest measurement of what the model actually knows.

### Scorer Mistakes Are Data Too

Using a less-intelligent AI for scoring (like Haiku) reveals not only the test-taker's mistakes but also the scorer's own misunderstandings and hallucinations about OpenWrt. Both are captured as lessons.

---

## What This Folder Contains

| Path | Purpose |
|---|---|
| `README.md` | Operator quick-start: how to run batches, collect results, score, and promote |
| `00-operating-plan.md` | Master operating contract: three-loop model, decision rules, queue lifecycle |
| `01-cookbook-state-and-gap-map.md` | Current cookbook corpus inventory and known gaps |
| `02-v13-lineage-and-migration-map.md` | Historical lineage from prior v13 mistake-discovery project |
| `03-test-generation-contract.md` | How to create, admit, and retire test scenarios |
| `04-failure-family-framework.md` | Taxonomy for deduplicating blind failures into families |
| `05-promotion-and-review-contract.md` | How scored failures become cookbook work |
| `06-test-bank-and-grouped-delivery.md` | Full scenario inventory and batch grouping rules |
| `07-test-expansion-and-key-sourcing-plan.md` | Systematic test creation from authoritative sources |
| `08-cookbook-authoring-execution-contract.md` | How to author staged cookbook drafts from admitted scenarios |
| `09-staged-authoring-lifecycle.md` | Staging model: draft → log → review → promotion |
| `10-human-review-procedure.md` | Human review checklist and promotion decision recording |
| `artifacts/` | Working surface: test batches, answer keys, scenario packets, results, scoring, registries, templates, staging |
| `docs/` | Development prompts and implementation plans |
| `tmp/` | Scratch area for temporary analysis |

---

## Final Output

The final output of this subpipeline is a set of concise, source-backed cookbook pages published to `static/cookbook-source/` and consumed by the main docs4ai pipeline. These pages are also staged in `artifacts/authoring/` (or `staging/` — see reorganization plans) before promotion, where they can be reviewed, verified, and iterated upon.

The cookbook pipeline also maintains a JSON configuration marker that tells the main pipeline where to read the latest cookbook outputs from, enabling automated integration with the broader docs4ai release process.

---

## For the Next Maintainer

Start here:
1. Read this mission statement.
2. Read `00-operating-plan.md` for the full operating contract.
3. Read `12-how-to-run.md` (when available) for the end-to-end operator guide.
4. Read `11-pipeline-step-catalog.md` (when available) for the numbered step reference.

Every step in this pipeline has defined inputs, outputs, and clear responsibility assignments (human vs. AI). Prompt templates for each AI-administered step are stored in the `prompts/` folder (when available). The `artifacts/` folder is the live execution surface — do not edit it unless you are running a pipeline step.
