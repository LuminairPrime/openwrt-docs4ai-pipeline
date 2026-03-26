# Project Name Migration Prompt 00

## Goal

Rename the source repository and local folder with the least risk, while preserving a working local setup, GitHub setup, and publish pipeline.

This plan prioritizes operational correctness over exhaustive cleanup. Old low-impact references may remain if they do not affect runtime, CI, publishing, or maintainer workflows.

## Verified External Guidance

The current plan is based on these documented facts from GitHub and VS Code:

1. GitHub repository renames preserve issues, stars, wiki links, and most web/git redirects, but GitHub recommends updating local remotes anyway with `git remote set-url origin NEW_URL`.
2. GitHub does not redirect workflows that call a GitHub Action from a renamed repository. If this repository is consumed externally as an action, a plain rename can break those callers.
3. GitHub warns not to recreate a new repository later under the old name, or redirects to the renamed repository can stop working.
4. VS Code does not have a separate "project" identity. For a single-folder setup, the folder you open is the workspace. After a folder rename, the practical recovery step is to reopen the renamed folder and verify workspace-scoped settings, tasks, launch configs, and interpreter selection.
5. VS Code path breakage risk is lower when configs use `${workspaceFolder}` rather than hardcoded absolute paths.

## Variables - Set Once Before Running

| Variable | Current | Target |
|---|---|---|
| `SOURCE_REPO_OWNER` | `LuminairPrime` | `LuminairPrime` |
| `SOURCE_REPO_NAME` | `openwrt-docs4ai-v12-copilot` | `openwrt-docs4ai-pipeline` |
| `LOCAL_FOLDER_NAME` | `openwrt-docs4ai-v12-copilot` | `openwrt-docs4ai-pipeline` |
| `DIST_ORG` | `openwrt-docs4ai` | unchanged |
| `DIST_PAGES_REPO` | `openwrt-docs4ai.github.io` | unchanged |
| `DIST_RELEASE_REPO` | `corpus` | unchanged |

Target: `openwrt-docs4ai-pipeline`.

## Practical Scope Rules

### Must be correct

- GitHub repository identity and local `origin` remote
- Local folder/workspace path
- GitHub Actions secrets, permissions, and publish flow
- Active scripts or configs that embed the old source repo name or local path
- Maintainer docs that contain operational copy-paste paths or URLs

### Allowed hangnails

- Archive material
- Session history or tool-generated logs
- Proposal docs and non-executed notes
- Non-operational narrative mentions of the old name

### Broad replace policy

- A broad search/replace is allowed in `docs/`, but exclude `docs/archive/`.
- Do not mass-edit `tmp/`, `.specstory/history/`, generated outputs, or cached artifacts just for cosmetic consistency.

## Repo-Specific Findings Already Verified

These findings should shape the migration plan so we do not over-edit:

1. VS Code risk is low in this repo.
   - `.vscode/settings.json` exists but contains no hardcoded repo path.
   - No `.code-workspace` file was found.
   - No repo-local `tasks.json` or `launch.json` was found.
2. No internal workflow references were found that call this repository as a GitHub Action via `uses: LuminairPrime/openwrt-docs4ai-v12-copilot@...`.
3. Operational old-name hits currently confirmed:
   - `DEVELOPMENT.md` line 46: absolute local path example
   - `.github/scripts/openwrt-docs4ai-02a-scrape-wiki.py` lines 48-49: user-agent and contact URL
   - `.specstory/.project.json` line 6: project name metadata
4. Low-priority old-name hits currently confirmed:
   - `tests/proposals/PRE-RELEASE-TEST-PLAN-OPUS.md`
5. Publish targets are intentionally separate from the source repo identity.
   - `.github/workflows/openwrt-docs4ai-00-pipeline.yml` sets:
     - `DIST_PAGES_REPO: openwrt-docs4ai/openwrt-docs4ai.github.io`
     - `DIST_RELEASE_REPO: openwrt-docs4ai/corpus`
   - Those values must remain unchanged.

## Migration Strategy

This migration will use an **In-Place GitHub Rename**. This strategy offers the lowest-risk cutover with maximum continuity, preserving repository history, issues, PRs, stars, settings, and most redirects. 

## Hard Invariants

1. Do not rename pipeline script filenames such as `openwrt-docs4ai-*.py` or the workflow filename `openwrt-docs4ai-00-pipeline.yml` unless the user explicitly asks for that separate naming change.
2. Do not rename or alter distribution targets under `${DIST_ORG}`.
3. Never mass-edit these locations during the migration:
   - `.specstory/history/`
   - `docs/archive/`
   - `tmp/`
   - generated output trees unless there is a proven operational reason
4. It is acceptable to leave old repo-name references in low-impact files after the cutover.

## Prompt To Execute The Migration

Use the exact prompt below in a new coding-agent session when ready.

---

You are executing a source repository rename with a strict in-place rename strategy, minimal-risk scope, and explicit stop conditions.

## Core Operating Rule

Do the minimum required to keep the project working.

Do not chase every stale string. Preserve correctness for:
- local development
- GitHub repo access
- CI/workflows
- publish flow
- maintainer copy-paste paths

Leave accepted hangnails alone.

## Inputs For This Run

- Current source repo: `LuminairPrime/openwrt-docs4ai-v12-copilot`
- Target source repo: `LuminairPrime/openwrt-docs4ai-pipeline`
- Current local folder: `openwrt-docs4ai-v12-copilot`
- Target local folder: `openwrt-docs4ai-pipeline`
- Distribution targets that must remain unchanged:
  - `openwrt-docs4ai/openwrt-docs4ai.github.io`
  - `openwrt-docs4ai/corpus`

## Phase 0 - Preflight Check

1. Run:
   - `git status`
   - `git rev-parse HEAD`
   - `git branch --show-current`
   - `git remote -v`
2. If the working tree is not clean, STOP and ask the user to commit or stash first.
3. Create a working branch:
   - `git checkout -b rename/source-repo-to-pipeline`
4. Confirm there is no internal evidence that this repo is consumed as a GitHub Action.
   - Search for `uses: LuminairPrime/openwrt-docs4ai-v12-copilot@`
5. Create a small execution checklist file in `docs/plans/v13/` only if needed for tracking.

## Execution Phases

### Phase 1 - User GitHub UI Actions

STOP GATE. The user must complete and confirm all of these before the agent continues.

1. Rename the repository in GitHub Settings from `openwrt-docs4ai-v12-copilot` to `openwrt-docs4ai-pipeline`.
2. Confirm branch protections or rulesets still apply to `main`.
3. Confirm Actions secrets still exist:
   - `DIST_APP_ID`
   - `DIST_APP_PRIVATE_KEY`
4. Confirm the GitHub App installation still has access to:
   - `openwrt-docs4ai/corpus`
   - `openwrt-docs4ai/openwrt-docs4ai.github.io`
5. Confirm Actions are still enabled and the workflow is visible.
6. Confirm the user does not plan to reuse the old repository name later for a different repository.

Do not proceed until the user confirms all six items.

### Phase 2 - Local Remote And Folder Repair

1. Inspect the current `origin` scheme from `git remote -v` and preserve that scheme.
2. Update the remote URL.
   - HTTPS example:
     - `git remote set-url origin https://github.com/LuminairPrime/openwrt-docs4ai-pipeline.git`
   - SSH example:
     - `git remote set-url origin git@github.com:LuminairPrime/openwrt-docs4ai-pipeline.git`
3. Verify:
   - `git remote -v`
4. Ask the user to close VS Code.
5. Ask the user to rename the local folder from `openwrt-docs4ai-v12-copilot` to `openwrt-docs4ai-pipeline`.
6. Ask the user to reopen VS Code at the renamed folder.
7. Confirm the terminal cwd is the renamed folder.
8. Confirm the Python environment is still selected correctly. If needed, reselect `.venv/Scripts/python.exe` from the reopened workspace.

Do not proceed until the user confirms the renamed folder is open and `git remote -v` shows the target repo.

### Phase 3 - Targeted Source Edits

Apply only the minimal operational edits first.

Required edits currently known:

1. `DEVELOPMENT.md`
   - Update the one absolute local path example containing `openwrt-docs4ai-v12-copilot/.venv/Scripts/python.exe`.
2. `.github/scripts/openwrt-docs4ai-02a-scrape-wiki.py`
   - Update the user-agent string repo name.
   - Update the contact URL repo name.
3. `.specstory/.project.json`
   - Update `project_name`.

Optional low-priority edits:

4. `tests/proposals/PRE-RELEASE-TEST-PLAN-OPUS.md`
   - Don't bother with this.
5. `docs/`
   - Broad search/replace is allowed for active docs only.
   - Exclude `docs/archive/`.
   - Do not spend time fixing harmless references.

Do not edit generated output trees just to remove cosmetic old-name references.

### Phase 4 - VS Code And Workspace Sanity Check

This repo is currently low-risk for VS Code path breakage, but still verify:

1. `.vscode/settings.json` has no hardcoded old folder path.
2. No `.code-workspace` file exists that needs folder-path repair.
3. No repo-local `tasks.json` or `launch.json` exists that needs path repair.
4. If any such files are found during execution, prefer `${workspaceFolder}`-based paths over absolute paths.
5. Open a new terminal in VS Code and verify the cwd resolves to the renamed workspace path.

### Phase 5 - Workflow And Publish Contract Verification

Read `.github/workflows/openwrt-docs4ai-00-pipeline.yml` and confirm these values remain unchanged:

- `DIST_PAGES_REPO: openwrt-docs4ai/openwrt-docs4ai.github.io`
- `DIST_RELEASE_REPO: openwrt-docs4ai/corpus`
- `actions/create-github-app-token@v2` steps still use `DIST_APP_ID` and `DIST_APP_PRIVATE_KEY`

Also confirm there is no source-repo-name-dependent logic in the workflow that would break after the rename.

### Phase 6 - Validation

Run in this order:

1. Reference scan for the old repo name in active files only.
   - Exclude:
     - `.specstory/history/`
     - `docs/archive/`
     - `tmp/`
     - of course exclude this migration plan file
2. `python tests/run_pytest.py`
3. `python tests/run_smoke.py`
4. `python tests/check_linting.py` only if the changed files make that worthwhile

If failures appear, fix only rename-related regressions.
Do not turn this into unrelated cleanup.

### Phase 7 - GitHub Validation

After local validation passes:

1. Push the branch.
2. Open a PR.
3. Trigger or wait for one workflow run.
4. Confirm the publish flow still succeeds to:
   - `openwrt-docs4ai/corpus`
   - `openwrt-docs4ai/openwrt-docs4ai.github.io`

## Hard Stop Conditions

Immediately STOP and ask the user before proceeding if any of these are true:

1. The GitHub rename has not been completed by the user.
2. The local folder rename and workspace reopen have not been completed by the user.
3. Required secrets are missing.
4. GitHub App access to distribution repos is missing.
5. Evidence appears that external callers use this repo as a GitHub Action and the user has not accepted that migration risk.

## Completion Criteria

The migration is successful only when all are true:

1. The local folder is renamed and the workspace opens correctly.
2. `origin` points to the target repository and push works.
3. The Python environment is still usable from the renamed workspace.
4. Local validation completes at the expected baseline.
5. One GitHub Actions run completes successfully.
6. Publish still succeeds to the unchanged distribution repos.
7. Any remaining old-name references are only accepted hangnails.

## Final Output Format

Report back with:

1. Files changed, grouped by:
   - operational docs
   - scripts/tooling
   - workflow/config verification
   - optional docs sweep
2. Remaining old-name references that were intentionally left behind.
3. Any follow-up recommendations that are non-blocking.

---

## Notes For This Repository

These facts are already known and should be treated as the starting assumptions during execution:

- This repo is a single-folder VS Code workspace, not a named IDE project.
- `.vscode/settings.json` currently has no path literals to repair.
- No `.code-workspace` file is present.
- No repo-local `tasks.json` or `launch.json` was found.
- The current workflow publishes to external distribution repos under `openwrt-docs4ai`, and those targets should not be renamed.
- The only currently confirmed operational old-name hits are in `DEVELOPMENT.md`, `.github/scripts/openwrt-docs4ai-02a-scrape-wiki.py`, and `.specstory/.project.json`.
- It is acceptable if low-priority files still contain the old name after the migration, as long as the system works.
