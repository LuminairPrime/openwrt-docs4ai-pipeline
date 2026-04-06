# Manual AI-Agent Result Layout

Store cookbook-center manual runs under this directory.

Recommended structure:

```text
artifacts/results/<agent-label>/<run-label>/
```

Use one new run label per target-agent test iteration. That keeps repeated bank sweeps, evaluator passes, and later cookbook follow-up from overwriting one another.

Inside each run directory:

```text
00-run-manifest.yaml
summary.md
alpha/
  00-prompt-source.txt
  00-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
  evaluations/
    <evaluator-label>/
      02-manual-score.md
      03-operator-notes.md
zeta/
  00-prompt-source.txt
  00-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
iota/
  00-prompt-source.txt
  00-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
```

Use `_template/00-run-manifest.yaml` as the starting point for a new agent run.
Use `_template/summary.md` as the starting point for the run-root summary.
Use the other files in `_template/` as the starting point for the per-group artifacts.

For local IDE or CLI agents with file-write access, the agent may write the canonical
`01-raw-response.md` file directly. For web or chat agents without file-write access,
the human should copy the response into that file immediately after the run.

Do not let local agents create standalone scenario script files or scratch artifacts in
the repository during blind runs. The only expected repository write from the tested
agent is the canonical raw-response artifact when local execution mode is being used.

The score for each group should reference the mirrored grouped answer key first, then fall back to the underlying scenario packet if finer-grained interpretation is needed.

If an evaluator AI prepares a provisional score, place it under `evaluations/<evaluator-label>/` first. The top-level `02-manual-score.md` remains the human-accepted final score for that group in that run.

Run one group per isolated agent session by default. Do not reuse a conversation that already answered another grouped prompt file.

The human may administer the bank iteratively across multiple target AIs:

- once a scenario has already produced one accepted blind fail, the next iteration may omit it
- or the human may still run it again to capture extra failure learnings

Both are valid. One fail is enough to admit cookbook work, but duplicate failures may still be worth keeping if they fail differently.

Canonical naming rule for new v14 runs:

- Keep the group score file name fixed as `02-manual-score.md`
- Keep timestamps and operator metadata inside the file body and run manifest, not in the filename
- Treat older timestamp-suffixed v13 score files as historical imports only

That canonical filename applies to the final accepted score for the run. It does not prohibit provisional evaluator drafts under `evaluations/<evaluator-label>/`.

Minimum required per-group files for a complete run:

- `00-prompt-source.txt`
- `00-key-source.txt`
- `01-raw-response.md`
- `02-manual-score.md`
- `03-operator-notes.md`

`01-raw-response.md` is intentionally not templated because it should remain the unedited captured output.

