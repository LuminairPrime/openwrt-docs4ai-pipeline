# Amelia Orchestrator: Operations & Execution Guide

This document is written by a previous agent to instruct you on how to correctly operate the `amelia` CLI and Server orchestrator to execute test plans and workflows.

## 1. Environment Requirements
- **WSL Only:** Amelia relies on Linux-specific file locks, pty systems, and virtual environments. **You MUST run all Amelia commands inside WSL.** Do not attempt to run Amelia natively in Windows PowerShell.
- **Python Environment:** Amelia is installed as a global tool via `uv`. The executable is located at `/home/mc/.local/bin/amelia`.
- **Database:** Amelia relies on a local PostgreSQL instance running on port `5434`.

## 2. Server Architecture
Amelia operates on a Server/Client architecture.
- **The Server:** Manages LangGraph state, checkpointing, event broadcasting, and the web dashboard. **It must be running in the background before you issue any CLI commands.**
- **The Dashboard:** Once the server is running, a fully built web dashboard is accessible at `http://127.0.0.1:8420`.
- **The CLI:** Used to queue workflows, manage profiles, and interact with the server.

### Startup Scripts
To ensure the environment variables and provider keys are correctly loaded, use the provided helper scripts located in the Windows Temp directory (mapped to `/mnt/c/...` in WSL):
1. **Start the Server:** 
   Run `/mnt/c/Users/MC/AppData/Local/Temp/start_server.sh` as a background process. Wait for it to announce `Uvicorn running on http://127.0.0.1:8420`.
2. **Start a Workflow:** 
   Run `/mnt/c/Users/MC/AppData/Local/Temp/start_workflow.sh` to trigger the default test plan.

## 3. Configuration & Authentication (Already Solved)
You do **not** need to debug API keys or provider routing. The previous agent has already hardened the `dev` profile in the PostgreSQL database to use the `deepseek-v4-pro` model. 
- It uses an advanced trick: It forces LangChain's Anthropic wrapper to hit DeepSeek's Anthropic-compatible endpoint (`https://api.deepseek.com/anthropic`). 
- This bypasses a known bug where LangChain drops DeepSeek's `reasoning_content` on multi-turn conversations. 
- **Actionable:** Always use `--profile dev` when starting workflows. The `start_workflow.sh` script already does this.

## 4. The Workflow Lifecycle (Plan -> Execute)
When you trigger a task via `amelia start ... --queue --plan`, the following lifecycle occurs:

### Phase 1: Planning (Architect Node)
- Amelia's "Architect" agent will spawn. It will explore the codebase using the `write_todos` tool to read the project structure and build an implementation plan.
- **Monitoring:** You can poll the workflow status using `curl -s http://127.0.0.1:8420/api/workflows/<workflow_id>`. Look for `"status": "pending"` and `"data": {"stage": "architect_node"}`.

### Phase 2: Execution (Developer Node)
- Once the Architect finishes, the plan is usually saved to `docs/plans/<date>-<issue-id>.md`.
- Depending on the CLI flags, Amelia will either pause for user approval or immediately hand the plan over to the "Developer" agent to begin writing code.
- The Developer agent will execute bash commands, write files, and run tests iteratively until the plan is complete.

## 5. Your Directives for the Test Plan
When executing the user's test plan:
1. Ensure your terminal is in the correct worktree (`.worktrees/mise-test-amelia`).
2. Start the Amelia server using the provided `start_server.sh` script.
3. Trigger the workflow. (If the test plan requires specific instructions, you can run the `amelia start` command manually, ensuring you pass `--profile dev`).
4. **DO NOT INTERFERE:** Once the workflow is queued, do not attempt to write code for Amelia or fix its bugs. Your job is simply to orchestrate the start of the tool, monitor its output/status, and record the start/end timestamps to judge its out-of-the-box performance.
5. If the workflow crashes (status becomes `failed`), record the failure reason gracefully. Do not attempt to rewrite Amelia's internal Python source code.

## 6. Known Gotchas & Troubleshooting (Updated)
- **Agent Profile Mapping (The 401 Bug):** If using the DeepSeek/Anthropic override, you MUST ensure *every* agent in the profile (including `task_reviewer`, `evaluator`, `plan_validator`, etc.) has the Anthropic provider set via the database or API. If an internal agent like `task_reviewer` is missed, it defaults to OpenAI and crashes with a `401 Missing Authentication header` during multi-task handoffs.
- **Branch Restrictions:** `amelia start` will refuse to execute if the worktree's current branch is not a default branch (e.g., `main`, `master`, `develop`). You must checkout or rename your branch to one of these before running `amelia start`, allowing Amelia to auto-branch from it.
- **Web GUI Path Corruption:** If you open Amelia's Web GUI on a Windows browser, it may overwrite the profile's `repo_root` with a Windows-style path (`c:\Users\...`). This crashes the Linux backend. Always ensure the database profile uses the WSL absolute path (`/mnt/c/...`).
- **Sync vs Async Execution:** Using `--queue --plan` forces Amelia to pause after the Architect node for human approval. Omitting both flags causes Amelia to run the entire LangGraph (Architect -> Developer -> Reviewer) continuously end-to-end without pausing.

## 7. Future: Windows Native Feasibility
Although Section 1 states WSL is required, a deep dive into Amelia's Python source code reveals no hard UNIX-level blockers preventing a native Windows port:
- It does **not** rely on UNIX `fcntl` (file locks) or `pty` (pseudo-terminals).
- It uses standard `asyncio.create_subprocess_exec` for execution.
- Docker sandboxing is handled via network APIs, not local Linux cgroups.
- **Conclusion:** Amelia can be made natively cross-platform for Windows PowerShell with minor refactoring to normalize `pathlib` usage and route shell commands through `powershell.exe -Command`.
