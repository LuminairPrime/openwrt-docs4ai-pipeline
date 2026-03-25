# Plan-003: Documentation Consolidation and Cutover

## Status
Proposed (2026-03-25)

## Supersedes
- `plan-001-docs-folder-reorganization.md` (naming conventions, archive strategy)
- `plan-002-docs-content-upgrade.md` (content accuracy audit, folder moves)

This plan merges the useful parts of both predecessors, drops the contradictions, and fills in the structural gaps. Plan-001 and plan-002 should be treated as historical drafts once this plan is accepted.

---

## Context

The project's maintainer documentation (`docs/`) evolved organically through V12. It now contains:

| Current path | What's in it | Status |
|---|---|---|
| `docs/ARCHITECTURE.md` | System architecture reference | **Stale** — still describes V12 zones, links to `docs/specs/v12/` |
| `docs/specs/v12/` | 13 active V12 spec files | **Mixed** — some contain permanent truths, some are V12-only |
| `docs/plans/v12/` | 23 historical planning files | **Archive-ready** — all V12 planning is complete |
| `docs/plans/v13/` | 15 active V13 planning files | **Active** — includes this plan |
| `docs/helpers/` | AI research files, `llms.txt` dump | **Archive-ready** — V12 exploration artifacts |
| `docs/archive/v12/` | 10 already-archived V12 files | **Done** — already archived |
| `docs/docs-new/` | V13 scaffold (output, pipeline, project, roadmap) | **Interim** — built by dev prompt Phase 2, will be restructured |

### Problems this plan solves

1. **`ARCHITECTURE.md` lies.** It references V12 specs, the V5a release tree, and a folder layout that no longer matches reality.
2. **Permanent specs are trapped in temporal folders.** The cookbook content contract (`03-v13`) is a permanent rulebook buried in `plans/v13/`. Future maintainers won't find it.
3. **`docs-new/` has a transitional layout.** The `output/`, `pipeline/`, `project/` subfolders served Phase 2 scaffolding but aren't the final taxonomy. The content is excellent; the folder names are wrong.
4. **No agent-friendly entry points.** There's no `OVERVIEW.md` or `GETTING_STARTED.md` at the docs root for AI or human discovery.
5. **`docs/helpers/` is undocumented.** Nobody knows if it's active or dead.

---

## Decisions

### D1: Flat taxonomy (from plan-002)

The final `docs/` layout uses four top-level folders plus agent-friendly root files:

```
docs/
├── OVERVIEW.md                          ← Agent/human entry point
├── GETTING_STARTED.md                   ← Quick-start for new contributors
├── ARCHITECTURE.md                      ← Rewritten for V13
├── specs/                               ← Permanent reference contracts
├── guides/                              ← How-to docs, runbooks, playbooks
├── plans/                               ← Versioned planning (temporal)
│   ├── v13/
│   └── v14/                             ← future
├── archive/                             ← Tombstoned historical context
│   └── v12/
└── roadmap/                             ← Deferred features, backlog
    └── deferred-features.md
```

**Why this layout wins:**
- Flat hierarchy is faster for both `fd`/`grep` and AI agent traversal
- `specs/` as a single folder means permanent contracts don't scatter across `output/`, `pipeline/`, `project/`
- `guides/` consolidates all action-oriented docs regardless of whether they're tutorials, runbooks, or playbooks
- `plans/` stays versioned because plans are inherently temporal
- `archive/` is clearly separated with tombstone warnings

### D2: No ADR folder

Plan-001 rejected the term "ADR" as corporate jargon but then plan-002 created `architecture-decision-records/`. This plan resolves the contradiction: **there is no separate ADR folder.**

Significant decisions are recorded as `plan-NNN-*.md` files in `docs/plans/`. Their "Decision" section (if present) is the permanent record. When a plan is archived, the decision record moves with it — but the relevant *spec* it produced stays in `docs/specs/`.

This matches the project's existing culture. Every important decision already lives in a plan file.

### D3: Naming conventions

| Document type | Folder | Filename pattern | Example |
|---|---|---|---|
| Permanent spec / contract | `docs/specs/` | `{topic}.md` | `release-tree-contract.md` |
| Guide / tutorial | `docs/guides/` | `guide-{topic}.md` | `guide-local-development-setup.md` |
| Runbook (tactical) | `docs/guides/` | `runbook-{topic}.md` | `runbook-pipeline-failure.md` |
| Playbook (strategic) | `docs/guides/` | `playbook-{topic}.md` | `playbook-adding-new-modules.md` |
| Plan (temporal) | `docs/plans/v{NN}/` | `plan-NNN-{topic}.md` or dated | `plan-003-docs-consolidation.md` |
| Archived doc | `docs/archive/v{NN}/` | original filename | `system-architecture.md` |
| Roadmap item | `docs/roadmap/` | descriptive | `deferred-features.md` |
| Agent root | `docs/` | `UPPERCASE.md` | `OVERVIEW.md` |

Prefix conventions (`guide-`, `runbook-`, `plan-NNN-`) make document purpose scannable even when a file is found via global search outside its folder context.

### D4: Tombstone policy for archived documents

Every `.md` file under `docs/archive/` must begin with this warning on the first line:

```markdown
> [!WARNING]
> **ARCHIVED — V12 ERA.** This document is retained for historical context only. It does not describe the current V13 pipeline. For current documentation, start from [OVERVIEW.md](../../OVERVIEW.md).
```

Additionally, `docs/archive/AGENTS.md` instructs AI agents to ignore the directory for implementation purposes:

```markdown
# Archive Notice

This directory contains historical V12 documentation preserved for context.
Do NOT use these files to understand current pipeline behavior.
Current documentation starts at `docs/OVERVIEW.md`.
```

### D5: Sequencing — this runs after the V13 dev prompt completes

The V13 development prompt (phases 0–13) expects `docs/docs-new/` in its current `output/pipeline/project/roadmap` layout. Running this cutover mid-development would break the dev prompt's exit criteria.

**Execution order:**
1. Complete V13 dev prompt phases 0–13 (pipeline code, cookbook content)
2. Run this plan's content upgrades and folder moves
3. Commit as a single logical unit: `docs: V13 documentation consolidation and cutover`

If V13 dev work is done in multiple sessions, this plan runs in the final session or a dedicated follow-up session after all pipeline phases pass.

### D6: `docs/helpers/` disposition

`docs/helpers/` contains V12-era AI research artifacts (tier-list explorations, a 166KB `llms.txt` dump, and subfolders `a-tier/`, `b-tier/`, `c-tier/`). These are historical research materials, not active documentation.

**Decision:** Archive the entire folder to `docs/archive/v12/helpers/` with tombstone warnings. Nothing in it is needed for V13 operations.

### D7: `docs/specs/v12/` triage

The 13 files in `docs/specs/v12/` fall into three categories:

| File | Disposition | Reason |
|---|---|---|
| `release-tree-contract.md` | **Superseded** → archive | V6 contract lives in `docs-new/output/` |
| `system-architecture.md` | **Superseded** → archive | Replaced by rewritten `ARCHITECTURE.md` |
| `schema-definitions.md` | **Promote** → `docs/specs/` | Permanent schema reference, update version refs |
| `execution-map.md` | **Superseded** → archive | V13 pipeline-stage-catalog replaces this |
| `execution-roadmap.md` | **Superseded** → archive | V12-only execution sequence |
| `implementation-status.md` | **Superseded** → archive | V12 tracking doc |
| `script-dependency-map.md` | **Promote** → `docs/specs/` | Permanent dependency reference, update for V13 |
| `v12-bug-log.md` | **Archive** | V12 bug history |
| `v12-stabilization-and-operations-plan-*.md` | **Archive** | V12 operations |
| `feature-flag-contract.md` | **Archive** | Retired feature (already noted in deferred-features) |
| `ai-summary-feature-spec.md` | **Evaluate** | May contain permanent spec content |
| `ai-summary-operations-runbook.md` | **Promote** → `docs/guides/` | Rename to `runbook-ai-summary-operations.md` |
| `ai-tooling-user-stories-and-test-plan.md` | **Archive** | V12 planning artifact |

> [!IMPORTANT]
> The triage above is a starting point. Each "Promote" file needs a quick read during execution to confirm its content is still accurate before it enters `docs/specs/` or `docs/guides/`. If it references V12-only concepts without updates, it gets archived instead.

### D8: Cookbook content spec extraction

`docs/plans/v13/03-v13-cookbook-content-spec-2026-03-22.md` contains permanent authoring rules (content contract, evidence rules, cross-link contract, content template) mixed with temporal project planning (topic inventory, acceptance checklists, addendum responses).

**Decision:** Extract the permanent portions into `docs/specs/cookbook-authoring-spec.md`. The original plan file stays in `docs/plans/v13/` as the historical record of *why* those rules exist.

**What gets extracted:**
- Content Contract (required sections, frontmatter, cross-link contract, verification records)
- Evidence Rules (1–5)
- Content Template
- Maintenance Policy

**What stays in the plan:**
- Topic Inventory and priorities
- Acceptance Criteria checklists
- Addendum review responses
- Authoring process (session-specific guidance)

---

## Content Upgrades (Before Folder Moves)

All content work happens *before* the structural cutover. You don't want to move a file and edit its content in the same commit — that makes `git blame` useless.

### CU-1: Rewrite `ARCHITECTURE.md`

**Action:** Substantial rewrite of `docs/ARCHITECTURE.md`.

**Changes:**
- Update "Repository Zones" table to reflect V13 layout (`docs/specs/`, `docs/guides/`, `docs/plans/`, `docs/archive/`)
- Remove references to `docs/specs/v12/` as the active spec location
- Update "Active Documents" section to list V13 spec files
- Add the `cookbook` module to the execution contract (stage `02i`)
- Reference `pipeline-stage-catalog.md` instead of duplicating stage mappings
- Update the archive policy to reference the tombstone convention from D4
- Note the V13 docs-new cutover as completed (if it has been)

**Does NOT change:**
- Layer model (still accurate)
- Naming conventions (still accurate)
- Remote promotion contract (still accurate, updated by dev prompt if needed)

### CU-2: Extract the cookbook authoring spec

**Action:** Create `docs/specs/cookbook-authoring-spec.md` from portions of `03-v13-cookbook-content-spec`.

**Source sections to extract (from 03-v13):**
- "Content Contract" (lines 99–170)
- "Evidence Rules" (lines 235–272)
- "Content Template" (lines 172–231)
- "Maintenance Policy" (lines 522–531)
- "Cookbook vs Reference Boundary" (lines 83–96)
- "Cross-link contract" (lines 149–161)

**Modifications during extraction:**
- Remove references to "this spec" and "02-v13" — make it standalone
- Add a header linking back to the original plan for full context
- Add a version line: `Extracted from: 03-v13-cookbook-content-spec (2026-03-22)`

### CU-3: Patch `pipeline-stage-catalog.md`

**Action:** Minor fix. Line 5 of `docs/docs-new/pipeline/pipeline-stage-catalog.md` states the old V12 `execution-map.md` is the source of truth for stage ordering. Delete this line — the catalog itself is now authoritative.

### CU-4: Create `OVERVIEW.md`

**Action:** Create `docs/OVERVIEW.md` as the primary entry point.

**Content:**
- One-paragraph project summary (what this repo does)
- "Where to find things" table linking to `specs/`, `guides/`, `plans/`, `archive/`
- Quick links to the 3–5 most important files (ARCHITECTURE.md, release-tree-contract, pipeline-stage-catalog, cookbook-authoring-spec, GETTING_STARTED)
- A note for AI agents: "Start here. Read ARCHITECTURE.md next for the system design."

**Size target:** Under 60 lines. This is a routing document, not a narrative.

### CU-5: Create `GETTING_STARTED.md`

**Action:** Create `docs/GETTING_STARTED.md` for new contributors.

**Content:**
- Prerequisites (Python, Windows dev env, git)
- Clone and setup (point to `DEVELOPMENT.md` at repo root)
- "Where to read next" based on what you want to do:
  - *Understand the pipeline:* → `specs/pipeline-stage-catalog.md`
  - *Write cookbook content:* → `specs/cookbook-authoring-spec.md`
  - *Fix a bug:* → `ARCHITECTURE.md` → relevant stage script
  - *Plan a new feature:* → `plans/v13/` → create a new `plan-NNN-*.md`

**Size target:** Under 80 lines. Links to existing docs, doesn't duplicate them.

---

## Structural Cutover Runbook

### Pre-flight checks

Before running any move commands:

```bash
# 1. Confirm no uncommitted changes
git status

# 2. Confirm V13 dev prompt work is complete (all tests pass)
python tests/run_pytest.py

# 3. Confirm docs-new scaffold exists with content
ls docs/docs-new/output/release-tree-contract.md
ls docs/docs-new/pipeline/pipeline-stage-catalog.md
ls docs/docs-new/pipeline/regeneration-rules.md
ls docs/docs-new/project/glossary-and-naming-contract.md
ls docs/docs-new/roadmap/deferred-features.md
```

### Step 1: Create the target structure

```bash
mkdir -p docs/specs
mkdir -p docs/guides
mkdir -p docs/roadmap
mkdir -p docs/archive/v12/plans
mkdir -p docs/archive/v12/specs
mkdir -p docs/archive/v12/helpers
```

### Step 2: Promote docs-new specs to their permanent home

These files were already written and validated during the V13 dev prompt. We're moving them out of the interim `docs-new/` scaffold into the final flat layout.

```bash
# Specs from docs-new
cp docs/docs-new/output/release-tree-contract.md docs/specs/release-tree-contract.md
cp docs/docs-new/pipeline/pipeline-stage-catalog.md docs/specs/pipeline-stage-catalog.md
cp docs/docs-new/pipeline/regeneration-rules.md docs/specs/regeneration-rules.md
cp docs/docs-new/project/glossary-and-naming-contract.md docs/specs/glossary-and-naming-contract.md

# Extracted cookbook authoring spec (created in CU-2)
# Already placed at docs/specs/cookbook-authoring-spec.md

# Roadmap
cp docs/docs-new/roadmap/deferred-features.md docs/roadmap/deferred-features.md
```

### Step 3: Promote eligible V12 specs

```bash
# These files get promoted after manual content review (see D7)
cp docs/specs/v12/schema-definitions.md docs/specs/schema-definitions.md
cp docs/specs/v12/script-dependency-map.md docs/specs/script-dependency-map.md

# This runbook gets promoted to guides
cp docs/specs/v12/ai-summary-operations-runbook.md docs/guides/runbook-ai-summary-operations.md
```

### Step 4: Archive everything else

```bash
# V12 plans (all 23 files)
cp -r docs/plans/v12/* docs/archive/v12/plans/

# V12 specs (everything not promoted)
cp docs/specs/v12/release-tree-contract.md docs/archive/v12/specs/
cp docs/specs/v12/system-architecture.md docs/archive/v12/specs/
cp docs/specs/v12/execution-map.md docs/archive/v12/specs/
cp docs/specs/v12/execution-roadmap.md docs/archive/v12/specs/
cp docs/specs/v12/implementation-status.md docs/archive/v12/specs/
cp docs/specs/v12/v12-bug-log.md docs/archive/v12/specs/
cp docs/specs/v12/v12-stabilization-and-operations-plan-2026-03-09.md docs/archive/v12/specs/
cp docs/specs/v12/feature-flag-contract.md docs/archive/v12/specs/
cp docs/specs/v12/ai-summary-feature-spec.md docs/archive/v12/specs/
cp docs/specs/v12/ai-tooling-user-stories-and-test-plan.md docs/archive/v12/specs/

# Stale ARCHITECTURE.md (the rewritten one stays at docs/ARCHITECTURE.md)
cp docs/ARCHITECTURE.md docs/archive/v12/ARCHITECTURE-v12.md

# Helpers directory
cp -r docs/helpers/* docs/archive/v12/helpers/

# Already-archived V12 files stay where they are
# docs/archive/v12/ already has 10 files — they don't move
```

### Step 5: Apply tombstone warnings

Run this for every `.md` file under `docs/archive/v12/`:

```bash
# For each .md file, prepend the tombstone warning
# (Use your editor, a script, or do it by hand — there are ~45 files)
```

Each file gets this prepended as line 1:

```markdown
> [!WARNING]
> **ARCHIVED — V12 ERA.** This document is retained for historical context only. It does not describe the current V13 pipeline. For current documentation, start from [OVERVIEW.md](../../OVERVIEW.md).

```

### Step 6: Create archive index files

**`docs/archive/AGENTS.md`:**
```markdown
# Archive Notice

This directory contains historical V12 documentation preserved for context.
Do NOT use these files to understand current pipeline behavior.
Current documentation starts at `docs/OVERVIEW.md`.
```

**`docs/archive/README.md`:**
```markdown
# Documentation Archive

This directory preserves documentation from previous versions for historical reference.

## V12

The `v12/` subdirectory contains planning documents, specifications, and research
artifacts from the V12 development cycle. These documents record the reasoning
behind decisions that shaped the current pipeline but are no longer authoritative
for implementation.

For current documentation, see [docs/OVERVIEW.md](../OVERVIEW.md).
```

### Step 7: Clean up the old structure

```bash
# Remove the now-empty interim scaffold
rm -rf docs/docs-new

# Remove the now-archived source directories
rm -rf docs/specs/v12
rm -rf docs/plans/v12
rm -rf docs/helpers
```

### Step 8: Verify and commit

```bash
# Verify no broken internal links in docs/
# (manual scan or simple grep for relative links)
grep -r '](../' docs/ --include='*.md' | head -20

# Verify the new structure looks right
find docs/ -name '*.md' | sort

# Commit
git add docs/
git commit -m "docs: V13 documentation consolidation and cutover

- Rewrite ARCHITECTURE.md for V13 (CU-1)
- Extract cookbook-authoring-spec from 03-v13 plan (CU-2)
- Add OVERVIEW.md and GETTING_STARTED.md entry points (CU-4, CU-5)
- Promote docs-new specs to docs/specs/ flat layout
- Archive V12 plans, specs, and helpers with tombstone warnings
- Remove interim docs-new scaffold
- Triage V12 specs: promote 3, archive 10

Supersedes: plan-001, plan-002"
```

---

## Post-Cutover Verification

After the commit, confirm:

- [ ] `docs/OVERVIEW.md` exists and has correct links
- [ ] `docs/GETTING_STARTED.md` exists and links to `DEVELOPMENT.md`
- [ ] `docs/ARCHITECTURE.md` references V13 layout, not V12
- [ ] `docs/specs/` contains: `release-tree-contract.md`, `pipeline-stage-catalog.md`, `regeneration-rules.md`, `glossary-and-naming-contract.md`, `cookbook-authoring-spec.md`, `schema-definitions.md`, `script-dependency-map.md`
- [ ] `docs/guides/` contains at least: `runbook-ai-summary-operations.md`
- [ ] `docs/plans/v13/` is untouched (still has all 15 active files)
- [ ] `docs/roadmap/deferred-features.md` exists
- [ ] `docs/archive/v12/` contains all archived files with tombstone warnings
- [ ] `docs/archive/AGENTS.md` and `docs/archive/README.md` exist
- [ ] `docs/docs-new/` no longer exists
- [ ] `docs/specs/v12/` no longer exists
- [ ] `docs/helpers/` no longer exists
- [ ] No relative links in `docs/` are broken
- [ ] `python tests/run_pytest.py` still passes (docs changes shouldn't affect tests, but verify)

---

## Rollback

If something goes wrong during the cutover, the simplest rollback is:

```bash
git checkout -- docs/
```

Since all operations are `cp` (not `mv`) until Step 7, and Step 7 only runs after verification, there's always a clean rollback path.

---

## What This Plan Intentionally Does NOT Do

1. **Does not touch `docs/plans/v13/`.** Those are active working documents. They move to `docs/archive/v13/` when V13 development closes, not during it.
2. **Does not create `guide-local-development-setup.md` or `runbook-testing-and-validation.md`.** Plan-002 proposed stubbing these. Empty stubs add noise without value. Create them when someone writes the actual content.
3. **Does not create an `architecture-decision-records/` folder.** Decisions live in plan files (see D2).
4. **Does not change any pipeline code.** This is purely a docs restructuring.
5. **Does not run during V13 dev prompt execution.** See D5 for sequencing.

---

## Appendix: Glossary of Documentation Types

For contributor reference when creating new docs in `docs/guides/`:

- **Guide** (`guide-*.md`): Educational, narrative document for learning or onboarding. Explains *why* alongside *how*.
- **Runbook** (`runbook-*.md`): Tactical step-by-step checklist for executing a specific operation or responding to a known failure. Highly actionable, often contains literal bash commands.
- **Playbook** (`playbook-*.md`): Strategic, high-level process for complex multi-stage scenarios. Orchestrates multiple runbooks. Provides *what, when, and why* rather than just *how*.

When in doubt, start with a guide. Promote to a runbook when the procedure stabilizes. Create a playbook only when you find yourself chaining multiple runbooks together.

---

## Appendix: Suggested Authoring Workflow for Future Versions

When working on complex features in future versions (V14+), consider splitting work into the taxonomy from the start:

1. **The Plan:** `docs/plans/v14/plan-NNN-feature-name.md` — *What* are we doing and *why*?
2. **The Spec:** `docs/specs/feature-contract.md` — *How* does the finished feature work?
3. **The Guide:** `docs/guides/guide-feature-usage.md` — *How* do contributors use it?

When the version closes, only the Plan gets archived. The Spec and Guide stay active and discoverable. This prevents the V12 problem where archiving a plan also buried the permanent rules it contained.

*(This is a suggestion, not a mandate. If monolithic plans feel more productive, use them — just be prepared to extract specs before archiving.)*
