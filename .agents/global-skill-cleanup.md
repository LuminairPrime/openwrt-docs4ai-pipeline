# Global Skill Cleanup

This file documents the April 2026 cross-IDE skill cleanup work.

It is intentionally kept under `.agents/` rather than the main `docs/` tree
because it is an operational note about local AI customization surfaces, not a
project-domain document for the OpenWrt docs pipeline itself.

## Local Skill Folders

| Path | Role |
| --- | --- |
| `.agents/skills/` | Canonical local source of truth for the shared curated skill set |
| `.claude/skills/` | Repo-local compatibility mirror for Claude-style discovery |
| `.kilocode/skills/` | Repo-local compatibility mirror for Kilo Code |
| `.github/skills/` | Retired repo-local Copilot skill surface with a tombstone README |
| `.github/instructions/` | Copilot-specific instruction surface |

## What The Cleanup Did

The cleanup intentionally converged the local Claude-style skill folders on one
shared curated set.

1. Compared the older local skill inventories under `.agents/skills/`,
   `.claude/skills/`, and `.kilocode/skills/`
2. Chose `.agents/skills/` as the primary authored source
3. Promoted useful skills from the older repo-local `.claude/skills/` inventory
   into `.agents/skills/`
4. Pruned skills that were irrelevant to this repository's Python, CI,
   documentation, and review scope or to the adjacent OpenWrt-oriented
   development and maintenance scope
5. Redeployed the curated set from `.agents/skills/` back into `.claude/skills/`
   and `.kilocode/skills/`
6. Folded the keepers from `.github/skills/` into `.agents/skills/` and
   retired that second repo-local skill inventory instead of keeping it alive

## Scope Of The Curated Set

The kept skill set is intended to cover the overlap between:

- this repository's Python, GitHub Actions, docs, review, QA, and maintenance work
- nearby OpenWrt-related development and maintenance needs such as shell,
  review, bug investigation, QA, documentation, and security hygiene

This is why the final local set favors review, testing, debugging, CI,
documentation, secret handling, and shell skills, while dropping broader or
less relevant historical extras from the repo-local Claude mirror.

## Sync Contract

The mirror contract lives in `tools/agents-skills/skill-layout.json`.

Refresh and prune the repo-local mirrors with:

```powershell
python tools/agents-skills/sync_local_skills.py --dry-run --prune
python tools/agents-skills/sync_local_skills.py --force --prune
```

Use pruning mode so `.claude/skills/` and `.kilocode/skills/` remain exact
mirrors of the curated `.agents/skills/` set instead of gradually collecting
historical extras again.

## Global Cleanup Note

Machine-global custom skill roots were separately reduced under the
`near-zero-global` policy and archived out of the global skill surfaces after
the useful local skills had already been pulled into the repository-local
canonical source.

## Curated Skill Relevance Review

Scores use a 0-5 scale:

- `5` = core
- `4` = strong
- `3` = useful but situational
- `2` = weak or niche
- `1` = poor fit
- `0` = irrelevant

The two scope columns are:

- `Current Repo`: this repository's Python, GitHub Actions, docs pipeline, CI,
  review, and maintenance work
- `OpenWrt Future`: a likely future OpenWrt-adjacent repo focused on LuCI JS,
  ucode, shell, review, docs, testing, and lower-level maintenance workflows

| Skill | Current Repo | OpenWrt Future | Notes |
| --- | ---: | ---: | --- |
| `api-design` | 2 | 2 | Useful only when work is API-contract heavy |
| `changelog-generator` | 5 | 3 | Strong here because release and docs pipeline changes are frequent |
| `ci-cd-pipeline-builder` | 5 | 3 | Very strong here due to GitHub Actions and pipeline work |
| `clean-code` | 4 | 5 | Strong general engineering value, especially for future JS, shell, and C cleanup |
| `code-review` | 3 | 4 | Good structured review aid, more valuable in lower-level OpenWrt review |
| `code-reviewer` | 4 | 4 | Strong lightweight review layer for both scopes |
| `codebase-onboarding` | 4 | 3 | Good for docs-heavy onboarding and repo handoff |
| `context-map` | 4 | 4 | Useful workflow guardrail for finding the smallest relevant edit surface |
| `create-llms` | 4 | 3 | Strong fit here because the repo already produces and validates llms-style outputs |
| `codedocs` | 5 | 4 | Excellent fit here, still strong for OpenWrt corpus or module docs |
| `dependency-auditor` | 4 | 2 | Good here for Python and npm tooling drift, weaker for embedded-facing work |
| `developer-experience` | 3 | 3 | Useful, but not central to either repo |
| `env-secrets-manager` | 4 | 2 | Strong here because CI, envs, and secret hygiene matter more |
| `find-bugs` | 4 | 5 | Strong here, even stronger for OpenWrt code and script review |
| `gh-address-comments` | 3 | 3 | Useful if PR-review workflow is active, otherwise secondary |
| `gh-cli` | 4 | 3 | Strong for CI and PR triage here, still useful in any GitHub-backed OpenWrt workflow |
| `gh-fix-ci` | 5 | 2 | Core for this repo's GitHub Actions work, much weaker for non-CI OpenWrt work |
| `git-commit-helper` | 4 | 4 | Good general workflow utility |
| `investigate` | 4 | 5 | Strong everywhere, especially good for tricky OpenWrt debugging |
| `pr-review-expert` | 4 | 5 | Strong for both, especially where changes have blast radius |
| `pytest-coverage` | 4 | 1 | Strong here for tight Python test proof, weak once work shifts away from Python |
| `python-patterns` | 5 | 0 | Core here, irrelevant for LuCI JS, ucode, and C |
| `python-testing` | 5 | 0 | Core here, irrelevant for LuCI JS, ucode, and C |
| `qa` | 3 | 2 | Moderately useful here, weaker unless the OpenWrt repo has a testable app or UI surface |
| `readme-updater` | 2 | 2 | Nice to have, but weak compared with stronger docs skills |
| `runbook-generator` | 2 | 2 | Operationally useful, but not central to either repo's daily flow |
| `secret-scanner` | 4 | 3 | Strong here, still useful for OpenWrt repos with CI, tokens, and scripts |
| `shell-scripting` | 3 | 5 | Moderate here, critical for OpenWrt-adjacent workflows |
| `technical-writing` | 4 | 5 | Strong here, extremely strong for OpenWrt docs, cookbook, and reference work |
| `test-strategy` | 4 | 5 | Strong in both contexts |

## Strongest Cross-Project Keepers

- `clean-code`
- `code-reviewer`
- `find-bugs`
- `investigate`
- `pr-review-expert`
- `technical-writing`
- `test-strategy`
- `shell-scripting`

## Most Project-Specific To This Repo

- `python-patterns`
- `python-testing`
- `create-llms`
- `gh-fix-ci`
- `ci-cd-pipeline-builder`
- `changelog-generator`

## Weakest Overall Candidates If The Set Needs Another Tightening Pass

- `api-design`
- `readme-updater`
- `runbook-generator`
- `developer-experience`
- `qa`
- `dependency-auditor` or `env-secrets-manager` if the future local set shifts
  harder toward OpenWrt-only development and away from CI-heavy Python work

## Operational Recommendation

If this repository remains primarily a Python, GitHub Actions, and docs-pipeline
workspace, the current 30-skill set is reasonable.

If the next pass is to optimize specifically for a future OpenWrt-focused local
set, the best first cuts would be the strongly Python-specific skills and the
weaker documentation or ops helpers that do not materially improve review,
debugging, shell work, or technical writing.