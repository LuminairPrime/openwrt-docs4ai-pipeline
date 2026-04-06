# tools — Local Support Utilities

This directory holds non-numbered maintainer tools.

The numbering contract for this repository is strict:

- numbered files under `.github/scripts/` are real pipeline stages
- a bare stage id such as `04` cannot coexist with `04a`, `04b`, or other same-family siblings
- local support tools that are not part of the hosted numbered pipeline belong here instead

## Current Tooling

| Tool | Purpose |
| --- | --- |
| `manage_ai_store.py` | Scratch-first AI summary review, validation, audit, promotion, and cleanup |
| `agents-skills/sync_local_skills.py` | Refresh repo-local mirrored skill roots from the canonical `.agents/skills/` source |
| `agents-skills/backup_global_customization_roots.py` | Back up user-managed machine-global skill, agent, and rule roots before cleanup |
| `agents-skills/archive_global_skill_candidates.py` | Move explicit archive-candidate skills or profile-selected global skills out of user-managed machine-global skill roots |

## AI Store Workflow

Use `manage_ai_store.py` for local AI-summary work that should not change the
hosted numbered pipeline surface.

```powershell
python tools/manage_ai_store.py --option review
python tools/manage_ai_store.py --option promote
python tools/manage_ai_store.py --option full --keep-scratch --max-ai-files 300
```

The CLI reuses the shared AI helper libraries in `lib/`:

- `lib/ai_enrichment.py`
- `lib/ai_store_checks.py`
- `lib/ai_store_workflow.py`

See `docs/guides/runbook-ai-summary-operations.md` for the durable operator
workflow and fallback procedures.

## Cross-IDE Skill Maintenance

Use `tools/agents-skills/sync_local_skills.py` when repo-local Claude-style
skills under `.agents/skills/` need to be mirrored into `.claude/skills/` and
`.kilocode/skills/` for IDE compatibility.

```powershell
python tools/agents-skills/sync_local_skills.py --dry-run --prune
python tools/agents-skills/sync_local_skills.py --force --prune
```

The mirror layout is defined in `tools/agents-skills/skill-layout.json`.

Use `tools/agents-skills/backup_global_customization_roots.py` before any
destructive machine-global cleanup:

```powershell
python tools/agents-skills/backup_global_customization_roots.py --dry-run
python tools/agents-skills/backup_global_customization_roots.py
```

Archive the current explicit machine-global skill candidates with:

```powershell
python tools/agents-skills/archive_global_skill_candidates.py --dry-run
python tools/agents-skills/archive_global_skill_candidates.py
```

Apply a cleanup profile such as `near-zero-global` with:

```powershell
python tools/agents-skills/archive_global_skill_candidates.py --profile near-zero-global --dry-run
python tools/agents-skills/archive_global_skill_candidates.py --profile near-zero-global
```