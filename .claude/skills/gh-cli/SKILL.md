---
name: gh-cli
description: Use GitHub CLI effectively for pull requests, Actions, issues, and repository triage.
---

# GitHub CLI

Use this skill when the task involves GitHub state that is easier to inspect or act on with `gh`.

## Common tasks

- inspect workflow runs and logs
- list or view pull requests
- review issues and comments
- create or update pull requests
- query repository metadata

## Preferred workflow

1. Verify authentication with `gh auth status` when needed.
2. Prefer focused read commands before mutating commands.
3. Scope results with `--repo`, `--json`, `--limit`, or search qualifiers.
4. Summarize the important fields instead of dumping raw output.

## Useful commands

```bash
gh pr list --limit 20
gh pr view <number> --json title,body,headRefName,baseRefName
gh run list --limit 20 --json databaseId,workflowName,status,conclusion,url
gh run view <run_id> --log-failed
gh issue list --limit 20
```

## Guidance

- Prefer JSON output when the result will be filtered or summarized.
- Use `gh run download` for artifacts before reading raw logs.
- Avoid destructive commands unless the user asked for them explicitly.