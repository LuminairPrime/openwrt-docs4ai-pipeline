# Retired Root

This folder is intentionally no longer used as a repo-local skill inventory.

The April 2026 cleanup moved the useful keepers into `.agents/skills/` and
retired the old `.github/skills/` surface to avoid maintaining a second local
skill catalog.

Do not add new skills here.

If a skill is worth keeping, add it under `.agents/skills/`, update
`tools/agents-skills/skill-layout.json`, and mirror it with:

```powershell
python tools/agents-skills/sync_local_skills.py --force --prune
```