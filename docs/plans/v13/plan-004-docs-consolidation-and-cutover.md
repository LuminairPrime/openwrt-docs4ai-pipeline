# Plan-004: Documentation Consolidation and Cutover

## Status
Proposed (2026-03-25)

## Supersedes
- `plan-001-docs-folder-reorganization.md` (naming conventions, archive strategy)
- `plan-002-docs-content-upgrade.md` (content accuracy audit, folder moves)
- `plan-003-docs-consolidation-and-cutover.md` (first merged cutover draft)

This plan keeps the useful structure from plan-003, fixes its execution bugs, and rewrites the runbook for the repository's Windows-first local workflow.

---

## Context

The project's maintainer documentation (`docs/`) evolved organically through V12 and the V13 implementation cycle. It now contains:

| Current path | What's in it | Status |
|---|---|---|
| `docs/ARCHITECTURE.md` | System architecture reference | **Stale** - still describes V12 zones and `docs/specs/v12/` as active |
| `docs/specs/v12/` | V12 spec set | **Mixed** - some files are still useful, others are V12-only |
| `docs/plans/v12/` | Historical V12 plans | **Archive-ready** |
| `docs/plans/v13/` | Active V13 planning set | **Active** - includes this plan |
| `docs/helpers/` | AI research artifacts and a large `llms.txt` dump | **Archive-ready** |
| `docs/archive/v12/` | Previously archived V12 materials | **Historical** |
| `docs/docs-new/` | V13 scaffold (`output/`, `pipeline/`, `project/`, `roadmap/`) | **Interim** - good content, transitional taxonomy |

### Problems this plan solves

1. **`ARCHITECTURE.md` is no longer truthful.** It still points maintainers at V12 locations that are no longer the intended active documentation surface.
2. **Permanent documentation rules are buried inside temporal plan files.** The cookbook authoring contract is the clearest example.
3. **`docs/docs-new/` solved the V13 implementation phase, not the long-term maintainer taxonomy.** The content is valuable; the layout is temporary.
4. **There is no root discovery surface for humans or agents.** `OVERVIEW.md` and `GETTING_STARTED.md` are still missing.
5. **`docs/helpers/` has no active role.** It should be archived instead of left ambiguous.
6. **Plan-003's cutover sequence was unsafe.** It would archive a rewritten `ARCHITECTURE.md` as if it were the V12 snapshot, and its rollback path was incomplete.
7. **Plan-003 assumed promoted docs were ready for a blind copy.** They are not. Several `docs/docs-new/` files still contain transitional links or stale wording that must be fixed as part of promotion.
8. **Plan-003 used bash commands in a Windows-first repository.** This runbook needs PowerShell commands that match local maintainer reality.

---

## Decisions

### D1: Flat long-term taxonomy

The final `docs/` layout uses a flat maintainer taxonomy plus agent-friendly root files:

```text
docs/
|- OVERVIEW.md
|- GETTING_STARTED.md
|- ARCHITECTURE.md
|- specs/
|- guides/
|- plans/
|  |- v13/
|  \- v14/
|- archive/
|  \- v12/
\- roadmap/
   \- deferred-features.md
```

**Why this layout wins:**
- `specs/` is the single home for permanent contracts and reference rules.
- `guides/` holds action-oriented maintainer docs regardless of whether they are guides, runbooks, or playbooks.
- `plans/` remains versioned because plans are inherently temporal.
- `archive/` keeps historical context separated from implementation truth.
- Root files make first-read navigation obvious for both humans and AI agents.

### D2: No ADR folder

This repository already records decisions in plan files. Creating a parallel ADR taxonomy adds ceremony without solving a real repository problem.

**Decision:** keep decision history in `plan-NNN-*.md` files. Extract any durable contract they produce into `docs/specs/` or `docs/guides/` before the plan is eventually archived.

### D3: Naming conventions

| Document type | Folder | Filename pattern | Example |
|---|---|---|---|
| Permanent spec / contract | `docs/specs/` | `{topic}.md` | `release-tree-contract.md` |
| Guide / tutorial | `docs/guides/` | `guide-{topic}.md` | `guide-local-development-setup.md` |
| Runbook | `docs/guides/` | `runbook-{topic}.md` | `runbook-pipeline-failure.md` |
| Playbook | `docs/guides/` | `playbook-{topic}.md` | `playbook-adding-new-modules.md` |
| Plan | `docs/plans/v{NN}/` | `plan-NNN-{topic}.md` | `plan-004-docs-consolidation-and-cutover.md` |
| Archived doc | `docs/archive/v{NN}/...` | original filename when practical | `schema-definitions.md` |
| Roadmap item | `docs/roadmap/` | descriptive | `deferred-features.md` |
| Root routing file | `docs/` | uppercase fixed name | `OVERVIEW.md` |

### D4: Tombstones are path-aware, not one-size-fits-all

Every archived Markdown file must begin with the same warning text, but the `OVERVIEW.md` link must be computed relative to the archived file's actual depth.

**Template:**

```markdown
> [!WARNING]
> **ARCHIVED - V12 ERA.** This document is retained for historical context only. It does not describe the current V13 pipeline. For current documentation, start from [OVERVIEW.md](<RELATIVE_PATH_TO_OVERVIEW>).
```

**Examples:**
- `docs/archive/v12/ARCHITECTURE-v12.md` -> `../../OVERVIEW.md`
- `docs/archive/v12/specs/schema-definitions.md` -> `../../../OVERVIEW.md`
- `docs/archive/v12/helpers/a-tier/example.md` -> `../../../../OVERVIEW.md`

`docs/archive/AGENTS.md` should instruct agents to ignore the directory for implementation work.

### D5: Sequence the cutover after V13 implementation work is complete

The V13 implementation prompt treats `docs/docs-new/` as the authoritative in-progress documentation tree. This cutover must run after phases 0-13 are complete and verified.

**Execution order:**
1. Finish V13 implementation work.
2. Run this cutover plan.
3. Commit as one logical docs-only change.

### D6: Archive `docs/helpers/`

`docs/helpers/` contains historical research artifacts, not current maintainer docs.

**Decision:** archive it under `docs/archive/v12/helpers/`. Apply tombstones to Markdown files only. Leave non-Markdown artifacts as plain historical files.

### D7: Triage `docs/specs/v12/`

| File | Disposition | Reason |
|---|---|---|
| `release-tree-contract.md` | Archive | Superseded by V6 contract |
| `system-architecture.md` | Archive | Replaced by rewritten `ARCHITECTURE.md` |
| `schema-definitions.md` | Promote to `docs/specs/` after review | Still a durable schema reference |
| `execution-map.md` | Archive | Replaced by `pipeline-stage-catalog.md` |
| `execution-roadmap.md` | Archive | V12-only execution sequence |
| `implementation-status.md` | Archive | V12 tracking state |
| `script-dependency-map.md` | Promote to `docs/specs/` after review | Still useful as a dependency reference |
| `v12-bug-log.md` | Archive | Historical defect log |
| `v12-stabilization-and-operations-plan-2026-03-09.md` | Archive | Historical operations plan |
| `feature-flag-contract.md` | Archive | Retired feature |
| `ai-summary-feature-spec.md` | Review before deciding | May still contain durable spec content |
| `ai-summary-operations-runbook.md` | Promote to `docs/guides/runbook-ai-summary-operations.md` after review | A runbook belongs in guides |
| `ai-tooling-user-stories-and-test-plan.md` | Archive | Historical planning artifact |

If a file marked for promotion still depends on V12-only concepts after review, archive it instead of promoting stale content.

### D8: Extract the cookbook authoring spec

`docs/plans/v13/03-v13-cookbook-content-spec-2026-03-22.md` mixes permanent content rules with temporal project planning.

**Decision:** extract the durable portions into `docs/specs/cookbook-authoring-spec.md` and keep the original plan file as historical rationale.

**Extract:**
- Cookbook vs reference boundary
- Content contract
- Cross-link contract
- Evidence rules
- Content template
- Maintenance policy

**Leave in the plan:**
- Topic inventory and priorities
- Acceptance checklists
- Review addenda and session-specific guidance

### D9: The runbook is PowerShell-first

All command examples in this plan use PowerShell and assume the maintainer is operating from the repository root on Windows.

### D10: Promotion includes a required rewrite pass

Promoting `docs/docs-new/` content is not just a file copy. Each promoted file must be reviewed for final-location correctness.

**Required fixes before promotion is considered complete:**
- `release-tree-contract.md`: predecessor link must point at the archived V12 contract, not `docs/docs-new/...`
- `pipeline-stage-catalog.md`: remove the old `execution-map.md` "source of truth" line
- `glossary-and-naming-contract.md`: replace the stale `cookbook_entry` origin-type reference with `authored`
- `deferred-features.md`: update the V6 contract reference to its final `docs/specs/` path
- Newly promoted root/spec/guide/roadmap files must not contain `docs/docs-new/` links unless they are explicitly describing historical cutover context

### D11: Rollback needs both Git and a file snapshot

Plan-003's rollback only restored tracked files. That leaves newly created files behind.

**Decision:** create a timestamped backup copy of the entire `docs/` tree under `tmp/` before the cutover starts. Use that snapshot as the last-resort rollback path if the cutover has already created new files or deleted old directories.

---

## Content Upgrades Before Cleanup

### CU-0: Snapshot the pre-cutover docs tree

Before rewriting anything, create a timestamped backup under `tmp/` and preserve the current V12 `ARCHITECTURE.md` content.

### CU-1: Rewrite `ARCHITECTURE.md`

**Action:** substantially rewrite `docs/ARCHITECTURE.md`.

**Changes:**
- update repository zones to the final V13 docs taxonomy
- stop referring to `docs/specs/v12/` as the active spec location
- list the promoted V13 spec files as the active reference set
- include the `cookbook` module and stage `02i`
- point readers at `pipeline-stage-catalog.md` for ordered stage ownership
- describe archive handling using the tombstone policy from D4

**Do not change:**
- the layer model unless implementation evidence requires it
- the remote promotion contract unless the live pipeline changed

### CU-2: Extract `cookbook-authoring-spec.md`

Create `docs/specs/cookbook-authoring-spec.md` from the durable sections of the 03-v13 plan.

**Make it standalone:**
- remove plan-internal phrasing such as "this spec" where it assumes the parent plan
- add a short header noting it was extracted from the 03-v13 plan
- keep the content contract and evidence rules intact

### CU-3: Patch promoted docs for final-location correctness

Perform a content-fix pass on the promoted docs as part of the cutover.

**Minimum required fixes:**
- `docs/specs/release-tree-contract.md`: predecessor link -> `../archive/v12/specs/release-tree-contract.md`
- `docs/specs/pipeline-stage-catalog.md`: delete the stale `execution-map.md` source-of-truth line
- `docs/specs/glossary-and-naming-contract.md`: `cookbook_entry` -> `authored`
- `docs/roadmap/deferred-features.md`: V6 contract reference -> `../specs/release-tree-contract.md`

### CU-4: Create `OVERVIEW.md`

Create `docs/OVERVIEW.md` as the root routing document.

**Content target:**
- one-paragraph project summary
- a "where to find things" table for `specs/`, `guides/`, `plans/`, and `archive/`
- links to `ARCHITECTURE.md`, `release-tree-contract.md`, `pipeline-stage-catalog.md`, `cookbook-authoring-spec.md`, and `GETTING_STARTED.md`
- a short note telling AI agents to start here and then read `ARCHITECTURE.md`

### CU-5: Create `GETTING_STARTED.md`

Create `docs/GETTING_STARTED.md` as the maintainer quick-start.

**Content target:**
- prerequisites for the Windows local environment
- pointer to root `DEVELOPMENT.md` for setup and validation commands
- "read next" paths for understanding the pipeline, writing cookbook content, fixing a bug, and planning a feature

---

## Structural Cutover Runbook

### Preconditions

Before starting the cutover:
- the V13 implementation prompt work is complete
- `python tests/run_pytest.py` passes
- `docs/docs-new/` exists and contains the V13 scaffold content
- the working tree is clean, or the operator intentionally set aside unrelated work first

### Step 0: Pre-flight and backup snapshot

```powershell
$ErrorActionPreference = 'Stop'

git status --short
python tests/run_pytest.py

$requiredDocsNewFiles = @(
  'docs/docs-new/output/release-tree-contract.md',
  'docs/docs-new/pipeline/pipeline-stage-catalog.md',
  'docs/docs-new/pipeline/regeneration-rules.md',
  'docs/docs-new/project/glossary-and-naming-contract.md',
  'docs/docs-new/roadmap/deferred-features.md'
)

foreach ($path in $requiredDocsNewFiles) {
  if (-not (Test-Path $path)) {
    throw "Missing required scaffold file: $path"
  }
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path 'tmp' "docs-cutover-backup-$timestamp"
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
Copy-Item 'docs' $backupRoot -Recurse
Write-Host "Backup created at $backupRoot"
```

### Step 1: Create target directories

```powershell
$targetDirs = @(
  'docs/specs',
  'docs/guides',
  'docs/roadmap',
  'docs/archive/v12/plans',
  'docs/archive/v12/specs',
  'docs/archive/v12/helpers'
)

foreach ($path in $targetDirs) {
  New-Item -ItemType Directory -Path $path -Force | Out-Null
}
```

### Step 2: Snapshot the V12 architecture file before rewriting it

This avoids the plan-003 bug where the rewritten V13 file would have been archived as if it were the original V12 version.

```powershell
Copy-Item 'docs/ARCHITECTURE.md' 'docs/archive/v12/ARCHITECTURE-v12.md' -Force
```

### Step 3: Promote `docs/docs-new/` content and apply final-location fixes

```powershell
Copy-Item 'docs/docs-new/output/release-tree-contract.md' 'docs/specs/release-tree-contract.md' -Force
Copy-Item 'docs/docs-new/pipeline/pipeline-stage-catalog.md' 'docs/specs/pipeline-stage-catalog.md' -Force
Copy-Item 'docs/docs-new/pipeline/regeneration-rules.md' 'docs/specs/regeneration-rules.md' -Force
Copy-Item 'docs/docs-new/project/glossary-and-naming-contract.md' 'docs/specs/glossary-and-naming-contract.md' -Force
Copy-Item 'docs/docs-new/roadmap/deferred-features.md' 'docs/roadmap/deferred-features.md' -Force
```

After the copy, fix the final-path issues from D10 in the promoted files before continuing.

### Step 4: Add extracted and newly authored root docs

By this point, the following new files should exist in their final locations:
- `docs/specs/cookbook-authoring-spec.md`
- `docs/OVERVIEW.md`
- `docs/GETTING_STARTED.md`

### Step 5: Promote eligible V12 docs after manual review

```powershell
Copy-Item 'docs/specs/v12/schema-definitions.md' 'docs/specs/schema-definitions.md' -Force
Copy-Item 'docs/specs/v12/script-dependency-map.md' 'docs/specs/script-dependency-map.md' -Force
Copy-Item 'docs/specs/v12/ai-summary-operations-runbook.md' 'docs/guides/runbook-ai-summary-operations.md' -Force
```

If `ai-summary-feature-spec.md` survives manual review as durable documentation, promote it deliberately. Otherwise archive it.

### Step 6: Archive the remaining V12 docs and helpers

```powershell
Copy-Item 'docs/plans/v12/*' 'docs/archive/v12/plans/' -Recurse -Force

$archiveSpecFiles = @(
  'docs/specs/v12/release-tree-contract.md',
  'docs/specs/v12/system-architecture.md',
  'docs/specs/v12/execution-map.md',
  'docs/specs/v12/execution-roadmap.md',
  'docs/specs/v12/implementation-status.md',
  'docs/specs/v12/v12-bug-log.md',
  'docs/specs/v12/v12-stabilization-and-operations-plan-2026-03-09.md',
  'docs/specs/v12/feature-flag-contract.md',
  'docs/specs/v12/ai-summary-feature-spec.md',
  'docs/specs/v12/ai-tooling-user-stories-and-test-plan.md'
)

foreach ($path in $archiveSpecFiles) {
  Copy-Item $path 'docs/archive/v12/specs/' -Force
}

Copy-Item 'docs/helpers/*' 'docs/archive/v12/helpers/' -Recurse -Force
```

Already archived V12 top-level files remain where they are.

### Step 7: Apply path-aware tombstones

Use a small PowerShell helper so the `OVERVIEW.md` link matches each archived file's directory depth.

```powershell
$archiveFiles = Get-ChildItem 'docs/archive/v12' -Recurse -File -Filter '*.md'

foreach ($file in $archiveFiles) {
  $relativeToDocs = [System.IO.Path]::GetRelativePath($file.Directory.FullName, (Resolve-Path 'docs').Path)
  $overviewPath = (Join-Path $relativeToDocs 'OVERVIEW.md').Replace('\', '/')
  $notice = @(
    '> [!WARNING]',
    "> **ARCHIVED - V12 ERA.** This document is retained for historical context only. It does not describe the current V13 pipeline. For current documentation, start from [OVERVIEW.md]($overviewPath).",
    ''
  ) -join [Environment]::NewLine

  $body = Get-Content $file.FullName -Raw
  if ($body -notmatch '^> \[!WARNING\]') {
    Set-Content -Path $file.FullName -Value ($notice + $body)
  }
}
```

### Step 8: Create archive index files

Create:
- `docs/archive/AGENTS.md`
- `docs/archive/README.md`

`docs/archive/AGENTS.md` must tell agents not to use the archive to understand current implementation. `docs/archive/README.md` must explain that `archive/v12/` is historical context only and point readers to `../OVERVIEW.md`.

### Step 9: Validate links, stale references, and final structure before cleanup

#### 9a. Relative Markdown link check for active docs

Run this against the final active docs surface, not against archived files and not against historical plan files.

```powershell
$activeRoots = @('docs/ARCHITECTURE.md', 'docs/OVERVIEW.md', 'docs/GETTING_STARTED.md')
$activeRoots += (Get-ChildItem 'docs/specs' -File -Filter '*.md').FullName
$activeRoots += (Get-ChildItem 'docs/guides' -File -Filter '*.md').FullName
$activeRoots += (Get-ChildItem 'docs/roadmap' -File -Filter '*.md').FullName

$linkRegex = '\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)'
$brokenLinks = New-Object System.Collections.Generic.List[string]

foreach ($path in $activeRoots) {
  $fullPath = (Resolve-Path $path).Path
  $content = Get-Content $fullPath -Raw
  $directory = Split-Path $fullPath -Parent
  $matches = [regex]::Matches($content, $linkRegex)

  foreach ($match in $matches) {
    $target = $match.Groups[1].Value.Split('#')[0]
    if ([string]::IsNullOrWhiteSpace($target)) {
      continue
    }

    $candidate = [System.IO.Path]::GetFullPath((Join-Path $directory $target))
    if (-not (Test-Path $candidate)) {
      $brokenLinks.Add("$path -> $target")
    }
  }
}

if ($brokenLinks.Count -gt 0) {
  $brokenLinks | Set-Content 'tmp/docs-cutover-broken-links.txt'
  throw 'Broken relative links found in active docs. See tmp/docs-cutover-broken-links.txt.'
}
```

#### 9b. Stale reference scan for promoted docs

This catches the specific transitional leaks already observed in plan-003 review.

```powershell
$promotedFiles = @(
  'docs/ARCHITECTURE.md',
  'docs/OVERVIEW.md',
  'docs/GETTING_STARTED.md'
)
$promotedFiles += (Get-ChildItem 'docs/specs' -File -Filter '*.md').FullName
$promotedFiles += (Get-ChildItem 'docs/guides' -File -Filter '*.md').FullName
$promotedFiles += (Get-ChildItem 'docs/roadmap' -File -Filter '*.md').FullName

$stalePatterns = @('docs/docs-new/', 'docs/specs/v12/', 'cookbook_entry')
$staleHits = foreach ($path in $promotedFiles) {
  Select-String -Path $path -Pattern $stalePatterns -SimpleMatch
}

if ($staleHits) {
  $staleHits | Format-Table Path, LineNumber, Line -AutoSize
  throw 'Stale transitional references remain in promoted docs.'
}
```

#### 9c. Final structure check

```powershell
Get-ChildItem 'docs' -Recurse -File -Filter '*.md' |
  Sort-Object FullName |
  Select-Object FullName
```

### Step 10: Remove the old transitional directories only after validation passes

```powershell
Remove-Item 'docs/docs-new' -Recurse -Force
Remove-Item 'docs/specs/v12' -Recurse -Force
Remove-Item 'docs/plans/v12' -Recurse -Force
Remove-Item 'docs/helpers' -Recurse -Force
```

### Step 11: Commit

```powershell
git add docs
git commit -m "docs: V13 documentation consolidation and cutover"
```

---

## Post-Cutover Verification

After the cutover commit, confirm:

- `docs/OVERVIEW.md` exists and points to the active docs surface
- `docs/GETTING_STARTED.md` exists and points to root `DEVELOPMENT.md`
- `docs/ARCHITECTURE.md` refers to the V13 docs taxonomy, not `docs/specs/v12/`
- `docs/specs/` contains `release-tree-contract.md`, `pipeline-stage-catalog.md`, `regeneration-rules.md`, `glossary-and-naming-contract.md`, `cookbook-authoring-spec.md`, `schema-definitions.md`, and `script-dependency-map.md`
- `docs/guides/` contains at least `runbook-ai-summary-operations.md`
- `docs/roadmap/deferred-features.md` exists
- `docs/plans/v13/` is untouched by the cutover itself
- `docs/archive/v12/` contains the archived materials with tombstones on Markdown files
- `docs/archive/AGENTS.md` and `docs/archive/README.md` exist
- `docs/docs-new/`, `docs/specs/v12/`, `docs/plans/v12/`, and `docs/helpers/` no longer exist
- the active docs link check passes
- `python tests/run_pytest.py` still passes

---

## Rollback

If the cutover fails before commit:

1. Prefer restoring from the timestamped backup created in Step 0.
2. Use Git restore for tracked content if needed.
3. Remove newly created docs paths only after confirming they contain no work you want to keep.

**Tracked-file restore:**

```powershell
git restore --source=HEAD --staged --worktree docs
```

**Full snapshot restore:**

```powershell
$backupRoot = 'tmp/docs-cutover-backup-YYYYMMDD-HHMMSS'

if (Test-Path 'docs') {
  Remove-Item 'docs' -Recurse -Force
}

Copy-Item (Join-Path $backupRoot 'docs') 'docs' -Recurse
```

The snapshot restore is the reliable fallback if the cutover already created new files or deleted old directories.

---

## What This Plan Intentionally Does Not Do

1. It does not archive `docs/plans/v13/`.
2. It does not add empty guide or runbook stubs.
3. It does not create an ADR directory.
4. It does not change pipeline code.
5. It does not run during the active V13 implementation prompt.

---

## Appendix: Documentation Types

- **Guide** (`guide-*.md`): educational and narrative; explains why and how.
- **Runbook** (`runbook-*.md`): tactical and step-by-step; optimized for execution.
- **Playbook** (`playbook-*.md`): strategic and multi-stage; coordinates larger workflows.

When in doubt, start with a guide. Promote it to a runbook when the procedure becomes deterministic. Create a playbook only when several stable runbooks need orchestration.
