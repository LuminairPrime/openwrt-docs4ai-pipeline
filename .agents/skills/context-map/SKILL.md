---
name: context-map
description: Generate a concise map of the files and dependencies relevant to a task before editing.
---

# Context Map

Use this skill when a task touches multiple files and you need a fast map before editing.

## Goal

Identify the smallest set of files that directly control the requested behavior.

## Workflow

1. Find the primary file or symbol named in the task.
2. Identify direct dependencies, neighboring tests, and call sites.
3. List only the files that are likely to be edited or validated.
4. Note one local risk before changing code.

## Output

Produce a short context map with these sections:

- Files to modify
- Nearby dependencies
- Relevant tests or validation commands
- One or two reference implementations if they matter
- Risks or open questions

Stop once the next edit surface is clear. Do not turn this into a broad repo survey.