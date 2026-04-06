# Cross-IDE Skill Layout

This repository uses a canonical-copy-plus-sync model for repo-local skills.
The goal is to keep project-relevant Python, OpenWrt-adjacent maintenance, CI,
documentation, review, and testing skills local to the repository while
avoiding machine-global skill bloat across unrelated projects.

## Local Roots

| Path | Role |
| --- | --- |
| `.agents/skills/` | Canonical local source of truth |
| `.claude/skills/` | Compatibility mirror for the curated local subset |
| `.kilocode/skills/` | Mirror root for Kilo Code |
| `.github/skills/` | Retired local Copilot skill root with a tombstone README |
| `.github/instructions/` | Minimal Copilot instruction overlay set |

## Skill Cleanup Outcome

The April 2026 skill cleanup did five things:

1. compared the older repo-local skill roots and treated `.agents/skills/` as
   the new primary authored source
2. promoted the useful Claude-style local skills needed for this repository
   into `.agents/skills/`
3. pruned repo-local mirror roots down to the curated project set instead of
   leaving historical extras in place
4. redeployed that exact curated set back into `.claude/skills/` and
   `.kilocode/skills/` so the local IDE-facing skill folders converge again
5. retired the old `.github/skills/` inventory after moving the keepers into
   the canonical `.agents/skills/` set

That means `.agents/skills/` is now the only place that should be hand-edited
for the shared local skill set. The other Claude-style local roots are mirror
targets, not separate inventories.

## Why This Layout Exists

Different IDEs and agent runtimes discover local skills from different folders.
Keeping a single canonical root reduces drift while still allowing per-project
local skills to appear in the roots that a specific IDE expects.

This repository no longer keeps a separate repo-local Copilot skill inventory
under `.github/skills/`. The keepers from that surface were folded into the
canonical `.agents/skills/` set, and the dropped entries were removed instead
of being carried forward as a second catalog.

The repo also keeps a small Copilot instruction surface under
`.github/instructions/`, but that folder is no longer used as a second
generated skill dump. The April 2026 cleanup removed the broad
`install-claude-skills.ps1` imports and kept only a narrow set of filetype- or
workflow-targeted instruction files:

- `github-actions-ci-cd-best-practices.instructions.md`
- `markdown.instructions.md`
- `markdown-accessibility.instructions.md`
- `python.instructions.md`
- `shell.instructions.md`
- `update-docs-on-code-change.instructions.md`

Anything broader than that should live as a proper skill under `.agents/skills/`,
not as a repo-wide Copilot instruction overlay.

This repository uses `.agents/skills/` as the canonical authored copy because
it is the narrowest local root already present in the repo and is a better fit
for a curated project-local subset than the larger historical inventory under
`.claude/skills/`.

## Current Scope

The mirrored local subset focuses on the work that matches this repository:

- Python maintenance and review
- Python patterns and test strategy
- API and architecture-adjacent documentation support
- GitHub Actions and CI support
- code review, debugging, and QA
- documentation and onboarding
- security, PR workflow, and ops/runbook helpers

The curated subset is declared in `tools/agents-skills/skill-layout.json` and
currently includes local pipeline helpers such as `gh-fix-ci`, `qa`,
`code-reviewer`, `codedocs`, `technical-writing`, `python-patterns`,
`python-testing`, `test-strategy`, `api-design`, `clean-code`, `context-map`,
`create-llms`, `gh-cli`, `pytest-coverage`, `env-secrets-manager`,
`gh-address-comments`, `git-commit-helper`, and `runbook-generator`.

This is intentionally narrower than the larger machine-global skill packs that
may exist elsewhere on the same workstation.

## Maintenance

Refresh mirror roots with:

```powershell
python tools/agents-skills/sync_local_skills.py --dry-run --prune
python tools/agents-skills/sync_local_skills.py --force --prune
```

The sync layout is configured in `tools/agents-skills/skill-layout.json`.

## Editing Rules

1. Edit the curated local subset only under `.agents/skills/`
2. Treat `.claude/skills/` and `.kilocode/skills/` as generated mirrors for
   the curated subset listed in `skill-layout.json`
3. Treat `.github/skills/` as retired and do not repopulate it
4. If a skill is useful to multiple local IDE roots, add it to `.agents/skills/`
   and update `skill-layout.json` instead of hand-copying it into the mirrors