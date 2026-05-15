We are going to test a new tool to see how well it implements a project upgrade. Please execute this plan exactly as written:

1. and 2. Cursor will use Plan mode to write the plan, then switch to an appropriate execution mode to execute the plan. The preliminary plan file which Cursor will base its new plan and implementation on is: `C:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\.worktrees\mise-test-files\mise-test-cursor.md`

3. **Setup the Worktree:** Create a new git worktree branching off `main` at: `.worktrees/mise-test-cursor` (relative to the current repository root).
4. **Enter Workspace:** Change your working directory into the new `.worktrees/mise-test-cursor` worktree.
5. Removed
6. **Mark Start Time:** Note the exact system time just before starting the tool.
7. **Execute Task:** Read the contents of the `.worktrees/mise-test-files/mise-test-cursor.md` file from the main repository. Pass that file's exact text (or its file path if the tool readme prefers a file path) as the instruction/prompt to cursor plan and/or execution mode to implement the feature upgrade.
8. **Mark End Time:** Note the exact system time the moment the tool finishes executing.
9. Removed
10. Removed
11. **Final Evaluation:** Review the work cursor produced against the prompt requirements. Score its work out of 10. Append your review, the calculated total execution time, and the final score to the bottom of the original `.worktrees/mise-test-files/readme-mise-test-cursor.md` file in the main repository for me to read at the end.

---

## Cursor Execution Review (Appended)

- Start time: `2026-05-12T04:42:49.2727967-03:00`
- End time: `2026-05-12T05:04:46.1549604-03:00`
- Total execution time: `00:21:56.8821637` (`1316.882` seconds)

### Review
Implemented the requested worktree flow end-to-end: created `.worktrees/mise-test-cursor` from `main`, added `mise.toml` with a `qa` task, added root `AGENTS.md` guidance requiring `vendors\mise\bin\mise.exe run qa`, and created `tests/qa_pipeline_orchestrator.py` using Testcontainers to run pipeline steps `01` through `08` in an ephemeral Linux container with fail-fast behavior and environment variable injection.

Validation was executed with the exact required command. The run now starts a container, installs prerequisites (`git`, `pandoc`, `nodejs`, `npm`, `jsdoc-to-markdown`, Python requirements), executes the numbered pipeline through step `08`, and correctly propagates non-zero failures. The final run fails at step `08` with a hard validation failure (`release-tree contains legacy file names`), which confirms fail-fast and non-zero exit behavior for real pipeline defects.

### Final Score
`9.0 / 10`
