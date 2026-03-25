# Plan-001: Documentation Folder Reorganization and DX Naming Conventions

## Status
Proposed (2026-03-24)

## Context
The project's pipeline maintainer documentation (`docs/`) has evolved through iterative versions (V12, V13). The cutover strategy for V13 requires finalizing a `docs-new/` scaffold and gracefully archiving legacy sprawl. 

Previously, this document proposed using strict "ADRs" (Architecture Decision Records). However, reviewing this through the lens of **Developer Experience (DX)** and **Developer Advocacy**, the term "ADR" is corporate, intimidating, and excludes non-professional GitHub contributors. We want a "Pit of Success" that minimizes the barrier to entry. Additionally, following the **CodeDocs** AI-agent principles, our top-level documentation needs structured, predictable entry points.

## Decision
1. **Approachable Naming (DX/DevRel)**: Replace the standard "ADR" nomenclature with "Plan", a highly recognizable term that already aligns with the project's existing `docs/plans/` culture. 
2. **Agent-First Roots (CodeDocs)**: Ensure AI-agent-friendly entry points (`OVERVIEW.md`, `GETTING_STARTED.md`) exist at the root of the active docs structure.
3. **Bridge and Cutover**: Execute the V13 cutover by creating an `archive/` bridge to preserve historical V12 context.
4. **Tombstone Archives**: Apply explicit negative constraints ("Tombstoning") to all archived documents to prevent AI context poisoning.

## Naming Conventions & Categories

To optimize for scanning, AI agent discovery, and contributor empathy, we enforce the following naming conventions across the V13 `docs/` scaffold:

| Document Type | Purpose | V13 Folder Location | Filename Pattern | Example |
|---|---|---|---|---|
| **Plans & Decisions** | Historical reasoning and feature definitions. | `docs/plans/` | `plan-NNN-topic.md` | `plan-001-docs-reorganization.md` |
| **CodeDocs Roots** | High-level system understanding and local quickstarts. | `docs/` | `OVERVIEW.md`, `GETTING_STARTED.md` | `OVERVIEW.md` |
| **Runbooks** | Action layer. Step-by-step procedures for operational tasks. | `docs/pipeline/runbooks/` | `runbook-topic.md` | `runbook-pipeline-failure.md` |
| **Architecture** | Context layer. System maps. | `docs/project/` or `docs/pipeline/` | `architecture-topic.md` | `architecture-data-flow.md` |
| **Specs & Contracts** | Reference layer. Exhaustive details on schemas. | `docs/output/` or `docs/pipeline/` | `contract-topic.md` | `contract-release-tree.md` |
| **Tutorials** | Learning layer. Focus on "Time-to-first-success" (< 5 mins). | `docs/project/` | `tutorial-topic.md` | `tutorial-local-setup.md` |
| **Archived** | Historical context layer. Deprecated files. | `docs/archive/v12/` | `[original-name].md` | `mirror-plan.md` |

*(Note: Prefixing filenames ensures that even if a file is moved or an agent searches globally, the document's DX purpose is immediately obvious).*

## Consequences
- **Positive:** "Plans" are instantly understood by anyone. Using `OVERVIEW` and `GETTING_STARTED` standardizes the repository for AI parsing.
- **Negative:** Renames existing docs, but drastically improves long-term maintainability.

---

## Runbook: Executing the V13 Cutover (Docs Reorg)

**Prerequisites:**
- `docs-new/` is fully populated per the V13 spec.
- Uncommitted working tree changes are stashed.

### Step 1: Prepare the Archive Bridge
Maintain the relative path distances of V12 artifacts to prevent breaking cross-links.

```bash
mkdir -p docs-new/archive/v12
cp -r docs/plans/v12 docs-new/archive/v12/plans
cp -r docs/specs/v12 docs-new/archive/v12/specs
cp docs/ARCHITECTURE.md docs-new/archive/v12/ARCHITECTURE.md
```

- `docs/architecture-decision-records/`: Permanent historical log of *why* choices were made.
- `docs/plans/`: Roadmaps, checklists, and temporal work lists that dictate *what* is happening next.
- `docs/guides/`: Tutorials, how-to's, runbooks, and recipes that show *how* to use the project.
- `docs/archive/`: Historical context. **This folder perfectly mirrors the root structure** for each version (e.g., `archive/v12/specs/`, `archive/v12/plans/`).

### Step 2: Tombstone the Archived Documents
Iterate through every `.md` file inside `docs-new/archive/v12/` and prepend an explicit AI warning on line 1.

```markdown
> [!WARNING] ARCHIVED DOCUMENT
> This document belongs to the V12 era. It is retained for historical context only. Do not use this to understand the current V13 pipeline implementation.
```

### Step 3: Create Archive Indices (CodeDocs compliance)
1. **`docs-new/archive/AGENTS.md`**
   Instruct AIs to ignore the directory for implementations.
2. **`docs-new/archive/README.md`**
   Explain to humans why V12 is kept here.

### Step 4: Execute the Folder Swap
Swap the active `docs/` directory and commit the changes.

```bash
git rm -r docs
mv docs-new docs
git add docs
```

## Glossary of Documentation Types

Within the `docs/guides/` folder (and across the project), standard industry terminology helps set reader expectations:

*   **Guide** (`guide-*.md`): The broadest term. An educational, narrative document focused on learning, onboarding, or understanding a workflow (e.g., `guide-local-development-setup.md`).
*   **Runbook** (`runbook-*.md`): A purely tactical, step-by-step checklist for executing a specific routine operation or responding to a known failure (e.g., `runbook-pipeline-validation-failures.md`). Highly actionable, often containing explicit bash commands.
*   **Playbook** (`playbook-*.md`): A strategic, high-level process for handling complex, multi-stage, or novel scenarios (e.g., `playbook-adding-new-modules.md`). Provides the "what, when, and why" rather than just the "how", often orchestrating multiple runbooks.

## Suggested Authoring Workflow (Optional)

In previous versions, large monolithic files in `plans/` acted simultaneously as product roadmaps, technical specs, decision logs, and execution checklists. This can make archiving difficult because retiring the checklist also buries the permanent architectural decisions.

If you find it helpful in the future when dealing with complex features, consider splitting the work into the new taxonomy right from the start:
1.  **The Decision:** `docs/architecture-decision-records/decision-005-adopt-xml.md` (Why are we doing this?)
2.  **The Spec:** `docs/specs/xml-output-contract.md` (How does the finished feature work?)
3.  **The Plan:** `docs/plans/v14/01-v14-xml-upgrade-checklist.md` (What files are we editing today?)

When the work is done, only the `Plan` gets moved to the `archive/`. The `Spec` and `Decision` stay active and easily discoverable. *(Note: This is merely a suggestion for keeping history clean; if authoring large monolithic plans feels more productive or easier to your workflow, prioritize what works best for you!)*
