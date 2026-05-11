# Plan: Unified QA Architecture (Mise + Testcontainers)

## 1. Objective
To upgrade the project's quality assurance (QA) pipeline by creating a deterministic, "CI-in-a-box" local testing environment. This will perfectly mirror the GitHub Actions Linux runner environment (`ubuntu-latest`) on local Windows machines, completely preventing "works locally but fails in CI" errors. 

By combining the **Mise** task runner for discoverability and **Testcontainers** for ephemeral isolation, both human developers and AI coding agents will have a foolproof, single-button execution command (`mise run qa`) to validate changes before pushing.

## 2. Architecture Overview
- **Mise (`vendors/mise/bin/mise.exe`)**: Acts as the universal task entry point. It standardizes environment variables and abstracts away complex command strings.
- **Testcontainers (`vendors/testcontainers-python`)**: Acts as the execution engine. Instead of running scripts directly on the host (which causes pathing and state-leakage issues), a Python script uses Testcontainers to programmatically spin up an isolated Docker container, execute the pipeline steps, and tear the container down cleanly.
- **WSL (Windows Subsystem for Linux)**: Provides the Docker daemon backend to run the Linux containers efficiently on Windows.

## 3. Implementation Phases

### Phase 1: Task Definition & Agent Discoverability
**Goal:** Create a standardized interface for humans and agents.
1. **Create `mise.toml`**: 
   - Define global environment variables.
   - Define a task: `qa` which simply executes `python tests/qa_pipeline_orchestrator.py`.
2. **Update `agents.md`**:
   - Add explicit instructions for AI agents: *"Do not execute pipeline scripts manually. To verify your work, you must execute `vendors\mise\bin\mise.exe run qa`. A non-zero exit code means your fix is incomplete."*

### Phase 2: The Testcontainers Orchestrator
**Goal:** Build the Python script that orchestrates the ephemeral CI environment.
1. **Create `tests/qa_pipeline_orchestrator.py`**:
   - Import `testcontainers-python`.
   - Configure a Docker container image that perfectly matches GitHub Actions (e.g., `python:3.12-slim` or an `ubuntu:22.04` base with Python installed).
2. **Container Configuration**:
   - **Mounting**: Bind-mount the current project directory into the container (e.g., to `/workspace`).
   - **Environment Variables**: Inject the exact environment variables defined in the `.github/workflows` YAML (e.g., `PIPELINE_RUN_DIR`, `OUTDIR`, `STAGED_DIR`, etc., pointing to temporary folders *inside* the container).

### Phase 3: Pipeline Execution Logic
**Goal:** Sequentially execute the pipeline and catch failures like the Step 08 validation error.
1. **Execution Sequence**:
   - The orchestrator script loops through the pipeline scripts (`01` through `08`).
   - For each script, it uses the Testcontainers `.exec_run()` method to execute it inside the container.
2. **Assertion and Logging**:
   - Assert that the exit code of every single script is `0`.
   - If a script fails (like the Step 05a crash or Step 08 validation failure), immediately halt the orchestrator, dump the container's `stdout`/`stderr` to the console, and exit with code `1`.
3. **Teardown**:
   - Testcontainers inherently guarantees teardown. Whether the test passes or crashes, the container is destroyed, ensuring zero state leakage into the next run.

## 4. Expected Outcomes
- **Zero CI Surprises**: Because the code executes in an isolated Linux container, path separators (`\` vs `/`), missing OS packages, and residual temporary files will no longer hide bugs locally.
- **Autonomous Agent Success**: Agents like InfCodeX/KodaX will be able to run `mise run qa`, see the exact failure that GitHub Actions would see, fix the issue, and re-run the test to verify—all without human intervention.
- **No Docker Headaches**: Developers will never have to manually run `docker run`, clean up orphaned containers, or manage complex `docker-compose` files. The Python script handles the entire lifecycle programmatically.
