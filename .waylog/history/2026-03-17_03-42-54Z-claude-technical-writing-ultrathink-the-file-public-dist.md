# @technical-writing ultrathink the file public-dist
_Exported on 03/25/2026 at 19:57:53 GMT-3 from Claude via WayLog_


**User**

@technical-writing ultrathink the file public-distribution-mirror-plan-2026-03-15-V5a.md has the next feature implementation plan for this project. basically it's a refactor to make the outputs generate in a better form, ready for the next stage of improvement after that, which is deploying automatically to a different github account repo so the full consumer/user-facing product of our project and nothing else is present in one website without extra confusing bits from our development tree. consider this plan file and the other project docs and suggest what documentation should be written and reviewed and how long it should be before implementation of the next feature set begins.

---


**Claude**

Let me read the plan file and key project documentation first.

---


**Claude**

Now let me read the spec files and look at what other documentation exists.

---


**Claude**

Let me also check a few more files for completeness.

---


**Claude**

Here's my documentation assessment for the V5a implementation.

---

## Documentation Readiness Assessment for V5a Implementation

### Current State

Your documentation suite is mature and well-structured. V5a itself is the strongest plan document in the series — it has rework maps, phase gates, rollback definitions, and conflict resolutions. The gap is not in the plan; it's in **the spec documents that V5a will invalidate**.

---

### 1. Documents That Must Be Updated Before Implementation Begins

These documents currently describe the pre-V5a contract. If developers start Phase 0 while these still say `{module}-skeleton.md` and `openwrt-condensed-docs/` as the public surface, the specs and the code will diverge on day one.

| Document | What's Wrong | Effort |
|---|---|---|
| **`docs/specs/v12/schema-definitions.md`** | Every L3/L4 path, every `llms.txt` bullet format example, every module routing example uses old names (`*-skeleton.md`, `*-complete-reference.md`, `L2-semantic/` paths in routing). This is the most critical update — it's the contract source-of-truth. | **Medium-high.** ~2 hours of careful editing. Every bullet format template, every path example, every "required characteristics" block needs a pass. |
| **`docs/specs/v12/execution-map.md`** | Layer locations (lines 6–10) reference `openwrt-condensed-docs/` as the output root. Key handoffs section references skeletons and monoliths by old names. The post-V5a pipeline adds `05e` and changes the output topology. | **Medium.** ~1 hour. |
| **`docs/ARCHITECTURE.md`** | Layer model table, output philosophy, execution contract, and remote promotion contract all reference the old output root and old file names. | **Medium.** ~1 hour. |

**Recommendation:** Update these three documents as the first action of Phase 0, before writing any code. The constants you add to `lib/config.py` should be nameable from the updated spec, not from the old one.

---

### 2. Documents That Should Be Updated Between Phase 1 and Phase 4

These can lag behind the spec updates because they describe operational procedures rather than contracts. They become stale only once the feature flag is turned on and tests switch.

| Document | What Changes | When |
|---|---|---|
| **`DEVELOPMENT.md`** | Environment variables table needs `ENABLE_RELEASE_TREE`. Repository rules section references `openwrt-condensed-docs/` as the stable output root. Script families table will gain `05e`. Remote publish policy needs the dual-tree model. | After Phase 1 gate passes |
| **`CLAUDE.md`** | Architecture tables, key conventions, known deferred items, and the "two LLM surfaces" section all need the V5a vocabulary. | After Phase 2 gate passes |
| **`README.md`** | Output model section references `openwrt-condensed-docs/`, `L1-raw/`, `L2-semantic/`, and the current gh-pages mirroring story. | After Phase 5 (when old contract is fully retired) |
| **`tests/README.md`** | Will need a new entry for `pytest_09_release_tree_contract_test.py` and possibly updated sample-input descriptions. | After Phase 2 |

---

### 3. New Documents That Should Be Written

| Document | Purpose | When |
|---|---|---|
| **`docs/specs/v12/release-tree-contract.md`** | A standalone, authoritative reference for the V5a public output contract — the final release tree layout (V5a §7), gatekeeper rules (§9), delivery surfaces (§8), and the "guaranteed absent" list (§7.1). This extracts the *durable contract* from the *plan narrative* so that after implementation, developers reference a clean spec rather than a 660-line plan document. | **Before Phase 0.** ~1–2 hours to extract and refine. |
| **`docs/specs/v12/feature-flag-contract.md`** (lightweight) | A short document defining `ENABLE_RELEASE_TREE` semantics: default value, what each script does when on/off, test expectations per flag state. V5a describes this across multiple phase sections but doesn't centralize it. | **Before Phase 1.** ~30 minutes. |

I would **not** write a separate migration guide or transition document. V5a §4 (the rework map) already serves that role well. Duplicating it would create a maintenance burden.

---

### 4. Documents That Need Review (Not Rewrite)

| Document | Review Goal | Effort |
|---|---|---|
| **`docs/specs/v12/v12-stabilization-and-operations-plan-2026-03-09.md`** | Confirm it's clearly marked as historical/completed. V5a is the next phase. No reader should confuse stabilization work with distribution work. | ~15 min |
| **`docs/specs/v12/implementation-status.md`** | Add a section acknowledging V5a as the next active work item. The "Next Priority" line at the bottom still points at AI-summary architecture. | ~15 min |
| **`docs/specs/v12/ai-summary-operations-runbook.md`** | No changes needed unless V5a's `release-tree/` relocation affects AI store paths (it shouldn't — AI store is in `data/`, not in the output tree). Quick confirmation read. | ~10 min |
| **V1–V4b plan documents** | V5a §10 already declares their supersession status. No action needed, but consider adding a one-line header to each: `> Superseded by V5a. See public-distribution-mirror-plan-2026-03-15-V5a.md.` | ~20 min total |

---

### 5. Recommended Timeline

| Day | Activity |
|---|---|
| **Day 1** | Write `release-tree-contract.md`. Update `schema-definitions.md` with the new naming contract (dual-state: document both old and new with clear "V5a replaces this" markers until Phase 5). |
| **Day 2** | Update `execution-map.md` and `ARCHITECTURE.md`. Write the short feature-flag contract. Review and annotate `implementation-status.md` with V5a as next active item. |
| **Day 3** | Add supersession headers to V1–V4b. Do a read-through of `DEVELOPMENT.md` to mark paragraphs that will need updating (don't rewrite yet — that comes with Phase 1). Quick review of `ai-summary-operations-runbook.md` to confirm no path conflicts. |
| **Day 4+** | Begin Phase 0 implementation. |

**Total pre-implementation documentation work: 3 focused working days**, or roughly 8–10 hours of writing and review. This is proportional to the scope — V5a touches every late-stage script, the entire test suite, and the output contract. Starting implementation without the spec updates means every developer (including future AI sessions) will be reading specs that contradict the code they're writing.

---

### 6. One Structural Recommendation

Your `docs/specs/v12/` directory currently mixes durable contracts (`schema-definitions.md`, `execution-map.md`) with time-bound plans (`stabilization-and-operations-plan-2026-03-09.md`). After V5a implementation, consider whether the completed plan documents should move to `docs/archive/v12/` alongside V1–V4b, leaving `docs/specs/v12/` as the live contract surface only. This matches the pattern you already established for the stabilization-era archives.

---


**User**

spin up sonnet agents to fix all the files you mentioned, create any files that are needed, and bring the project up to the state necessary for development to proceed with the new refactor

---


**Claude**

Launching 9 parallel agents to update all documentation files. Each agent handles a distinct set of files with no overlap.

---


**Claude**

All 9 agents completed successfully. Here's what was done:

### New Files Created (2)
- **`docs/specs/v12/release-tree-contract.md`** — Standalone authoritative reference for the V5a public output contract (layout, module schema, sharding, gatekeeper rules, delivery surfaces, name mapping)
- **`docs/specs/v12/feature-flag-contract.md`** — `ENABLE_RELEASE_TREE` semantics: behavior per flag state, test expectations, lifecycle, interaction with other variables

### Spec Documents Updated (3)
- **`docs/specs/v12/schema-definitions.md`** — Dual-labeled "(current, pre-V5a)" / "(V5a)" throughout L1–L5 sections, LLM routing contract, AGENTS.md guidance, new V5a Output Topology section
- **`docs/specs/v12/execution-map.md`** — Transition note, `release-tree/`/`support-tree/` in layer locations, `05e` in script flow + contract matrix + handoffs, `ENABLE_RELEASE_TREE` in env vars
- **`docs/specs/v12/implementation-status.md`** — Next Priority section now points to V5a with links to the three new/updated spec documents

### Architecture & Maintainer Docs Updated (4)
- **`docs/ARCHITECTURE.md`** — V5a in purpose, 3 new repo zones, layer model V5a row, output philosophy, execution contract `05e`, remote promotion V5a deploy, active documents list
- **`DEVELOPMENT.md`** — V5a in purpose, `ENABLE_RELEASE_TREE` env var, `05e` in script families, repository rules, remote publish policy, dual LLM surfaces, current focus
- **`CLAUDE.md`** — V5a in description, layer model note, `05e` in stage flow table, LLM surfaces, key conventions, known items, reference files
- **`README.md`** — V5a in description, output model transition paragraph, status bullet, repository guidance link

### Plan Documents Annotated (6)
- **V1, REVIEW, V2, V3, V4a, V4b** — Each received a supersession header linking to V5a as the active specification

The project documentation is now aligned for Phase 0 implementation to begin. All specs describe both the current and V5a contracts, the feature flag is documented, and the release-tree contract has its own standalone reference.

---


**User**

write a prompt for commanding a dumber AI than you to develop and test the v5a plan. how to do it, what files to rely on, what not to do, etc

---


**Claude**

Let me check the current state of a few key files to make sure paths and details are accurate in the prompt.

---


**Claude**

Now I have what I need. Let me write the prompt.

---


**Claude**

Written to `docs/plans/v12/v5a-implementation-prompt.md`.

The prompt is structured as **copy-paste blocks** — one per phase, each self-contained:

- **Context Block** + **Rules** go into every session
- **Phase N** section gets added when you're ready for that phase
- **Troubleshooting Reference** goes in when things go sideways

Key design choices for a less capable model:

1. **Explicit file lists** — tells it exactly what to read, what to modify, what never to touch
2. **Literal string replacements** — spells out every `old → new` pattern instead of leaving it to infer from the plan
3. **Validation commands after every phase** — with both flag states
4. **"If you think X needs changing, you're wrong"** guardrails — prevents the common failure mode of over-reaching into upstream scripts
5. **One commit per phase** — keeps rollback clean
6. **Troubleshooting section** — covers the 8 most likely failure modes based on the codebase structure (Windows paths, module discovery, optional files, text rewriting)

---


**User**

does your dev plan include naming/renaming the pipeline script files to follow the project schema of ordering them in numerical order of their execution and then using alphabet letters for denoting files that can be run in parallel for optimal performance outside of testing? or does it create random file names without justification and I'' need to refactor them at the end?

---


**Claude**



The prompt follows the project's naming convention correctly. Specifically:

- **`05e-assemble-release-tree.py`** — uses the `05` stage family with letter suffix `e`, placing it after `05d` and within the same stage family as `05a`–`05d`. This is correct because all `05*` scripts depend on the same upstream (`03`/`04` output) and are parallelizable siblings.

- **`pytest_09_release_tree_contract_test.py`** — follows the existing `pytest_{NN}_` numbering pattern, placed after the current highest (`pytest_06`).

However, there's a subtlety worth calling out: **`05e` is not truly parallelizable with `05a`**. It reads `05a`'s output (the complete-reference and skeleton files). By the project convention documented in `ARCHITECTURE.md`, letter suffixes denote siblings that "may be parallelized in deployment when their direct dependencies are satisfied." In Phase 1, `05e` depends on `05a` through `07` — it's a post-assembly step, not a sibling.

Two options:

1. **Keep `05e` as a transitional name** — it's temporary anyway. In Phase 4, `05e` is retired and its logic is absorbed into the modified `05a`–`08`. The name only lives for Phases 1–3, then disappears.

2. **Rename to a true post-assembly position** — something like `05z` to signal "runs after all other `05*` siblings" or use a new stage number entirely, but the plan explicitly avoids bare `05` coexisting with `05a`, and `06` is taken.

The prompt as written takes option 1 — the script is explicitly documented as transitional and gets retired in Phase 4. The naming convention violation is bounded and short-lived. Want me to change the approach, or is the transitional compromise acceptable?

---


**User**

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

---


**User**

> /exit

---


**User**

> ⎿ Bye!

---
