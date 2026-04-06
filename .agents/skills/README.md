# Mirrored Skills

This directory is the canonical local skill source for the curated cross-IDE
subset managed by this repository.

- Canonical source: this directory
- Refresh command: `python tools/agents-skills/sync_local_skills.py`

Edit curated local skills here, then sync them to the mirror roots.

The current curated subset is intentionally Python-pipeline-focused rather than
trying to mirror the entire historical local skill inventory. It now includes
the generic Python and testing helpers that were previously only available from
machine-global roots, plus a small set of useful skills promoted out of the
older repo-local `.claude/skills/` inventory during the April 2026 cleanup.