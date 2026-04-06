# OpenWrt Development Test Instructions

**Your job:** Answer every scenario in the batch file you were given, one batch per session, in order.

**Read from:** `<batch-id>.md` — the files provided to you.

**Write to:** Print results to the screen and if you have filesystem write access write your results to `results/<batch-id>-result.md`.

**Five hard rules:**

1. **No search.** Do not use repository search, file-system read tools, web search, or external lookup. Answer from internal knowledge only.
2. **One batch per session.** Do not continue a session that has already answered a different batch file.
3. **Do not read `-key.md` files.** These are answer keys and must stay unread during your run.
4. **No extra files.** Do not create scripts, scratch files, or other artifacts outside the designated raw-response path.
5. **Stop after finishing.** Deliver all answers in this batch, then stop. Do not request the next batch.


---

## For the Human Operator

### Batch structure

The `artifacts/tests-batches/` folder contains nine prompt batches (`01a.md` through `01i.md`). The answer keys (`01a-key.md` through `01i-key.md`) live in `artifacts/tests-keys/`. The `tests-batches-manifest.yaml` in the `artifacts/` folder records the machine-readable batch membership and scenario assignments for the full 27-scenario pack.

### Sandboxed execution via `runs/`

Each agent run is scoped to `artifacts/runs/<agent-label>/<run-label>/`. Use one folder per agent–run combination. The `runs/` folder is the live sandboxed execution surface for active blind testing. The `results/` folder is reserved for aggregated cross-run analysis and imported legacy evidence.

### Scoring flow

1. Choose a batch prompt file from `artifacts/tests-batches/` and open a fresh isolated agent session.
2. Collect the agent response in `artifacts/runs/<agent-label>/<run-label>/<batch-id>/01-raw-response.md`.
3. Score the run against the paired `-key.md` file in `artifacts/tests-keys/`.
4. Record the decision in `02-manual-score.md` in the same batch subfolder.
5. Escalate any newly discovered blind failures to the failure-family registry.

### Operating plan

The full operating contract, queue model, and promotion rules live in [00-openwrt-cookbook-project-center-operating-plan.md](./00-openwrt-cookbook-project-center-operating-plan.md).
