# Cross-IDE Local Skills

This directory owns the repo-local skill layout for IDEs that read different
project folders.

## Current Contract

- Canonical source: `.agents/skills/`
- Mirror roots: `.claude/skills/`, `.kilocode/skills/`
- Retired root: `.github/skills/` (tombstone README only)

Useful repo-local Copilot skills were folded into `.agents/skills/`, and the
rest were dropped. `.github/skills/` now contains only a tombstone README so
the repo does not carry a second local skill inventory.

The sync tool mirrors the curated repo-local subset listed in
`skill-layout.json` into the local compatibility roots.

The current curated subset is centered on this repository's actual maintenance
surface: Python, CI, debugging, QA, review, documentation, and security.

## Sync Command

```powershell
python tools/agents-skills/sync_local_skills.py --dry-run
python tools/agents-skills/sync_local_skills.py --force
```

Use `--target` when you need to refresh only one mirror root.

```powershell
python tools/agents-skills/sync_local_skills.py --target .claude/skills --force
```

## Editing Rules

- Edit curated local skills only in `.agents/skills/`
- Do not hand-edit mirrored copies under `.claude/skills/` or `.kilocode/skills/`
- Keep `.github/skills/` limited to the tombstone README unless a future
	migration explicitly reopens it