# Plan-002: Documentation Content Upgrade

## Status
Proposed (2026-03-24)

## Context
Before we blindly move files into the new temporal structure (`specs/`, `plans/`, `guides/`), we must ensure the contents of the "Present-Tense" documents are actually accurate and authoritative for V13. 

An audit of the current repo yielded the following truths:
1. **The `docs-new` Specs are Excellent:** `release-tree-contract.md`, `pipeline-stage-catalog.md`, and `glossary-and-naming-contract.md` correctly outline V13 (e.g., they include the Stage 02i Cookbook injector).
2. **`docs/ARCHITECTURE.md` is Stale:** It still describes V12. It references the V5a release tree, explicitly points readers to `docs/specs/v12/`, and completely misses the Option 1 (Temporal) docs redesign we just agreed on.
3. **V13 Plans contain permanent Specs:** `03-v13-cookbook-content-spec-2026-03-22.md` is not just a plan; it is a permanent rulebook for how humans must write cookbook pages. It is currently buried in `plans/`.

## The Upgrade Execution Plan

We will perform these content upgrades **before** running the final folder move commands.

### Step 1: Rewrite Root `ARCHITECTURE.md`
- **Action:** Substantially update the markdown content.
- **Updates:** 
  - Change all references from V12 to V13.
  - Update the "Repository Zones" table to match the pristine Temporal layout (`docs/specs/`, `docs/plans/`, `docs/guides/`, `docs/archive/`).
  - Strip redundant stage mappings, deferring purely to the excellent `pipeline-stage-catalog.md`.

### Step 2: Extract the Cookbook Content Spec
- **Action:** Convert the `03-v13-cookbook-content-spec...` plan into a permanent, active document (e.g., `cookbook-authoring-spec.md`).
- **Content Edits:** Remove the ephemeral V13 project management checklists ("Minimum viable v13 cookbook", "Addendum review responses"). Preserve the strict evidence rules, content templates, and formatting contracts, as those govern the present and future.

### Step 3: Patch `pipeline-stage-catalog.md`
- **Action:** Minor content fix. 
- **Updates:** Line 5 currently asserts that the old V12 `execution-map.md` is the source of truth for stage ordering. We will delete this line, as the catalog itself contains the correct V13 execution order flowchart.

### Step 4: The Final Reorg (Option 1 Temporal Map)
Once the files are truthful, execute the pure folder moves (no content modifications here):

```bash
# 1. Archive all strictly V12 Plans and Specs (Mirrored Structure)
mkdir -p docs-new/archive/v12/plans
mkdir -p docs-new/archive/v12/specs
cp -r docs/plans/v12/* docs-new/archive/v12/plans/
cp -r docs/specs/v12/* docs-new/archive/v12/specs/

# 2. Archive the old V12 Architecture and Helpers
cp docs/ARCHITECTURE.md docs-new/archive/v12/ARCHITECTURE-v12.md
mkdir -p docs-new/archive/v12/helpers
cp -r docs/helpers/* docs-new/archive/v12/helpers/

# 3. Lay out the Option 1 Structure in docs-new
mkdir -p docs-new/specs
mkdir -p docs-new/architecture-decision-records
mkdir -p docs-new/guides

mv docs-new/output/release-tree-contract.md docs-new/specs/
mv docs-new/pipeline/pipeline-stage-catalog.md docs-new/specs/
mv docs-new/pipeline/regeneration-rules.md docs-new/specs/
mv docs-new/project/glossary-and-naming-contract.md docs-new/specs/
mv docs-new/cookbook-authoring-spec.md docs-new/specs/ # from step 2

# 4. Stub out missing useful documentation
touch docs-new/guides/guide-local-development-setup.md
touch docs-new/guides/runbook-testing-and-validation.md

# 5. Move the remaining V13 plans
mkdir -p docs-new/plans/
mv docs/plans/v13 docs-new/plans/

# 6. Execute the cutover
git rm -r docs
mv docs-new docs
git add docs
```
