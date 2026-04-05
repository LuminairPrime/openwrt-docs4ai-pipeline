# Manual AI-Agent Result Layout

Store cookbook-center manual runs under this directory.

Recommended structure:

```text
artifacts/results/<agent-id>/<run-id>/
```

Inside each run directory:

```text
00-run-manifest.yaml
summary.md
delta/
  00-prompt-source.txt
  00-answer-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
epsilon/
  00-prompt-source.txt
  00-answer-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
zeta/
  00-prompt-source.txt
  00-answer-key-source.txt
  01-raw-response.md
  02-manual-score.md
  03-operator-notes.md
```

Use `_template/00-run-manifest.yaml` as the starting point for a new agent run.

The score for each group should reference the mirrored grouped answer key first, then fall back to the underlying scenario packet if finer-grained interpretation is needed.

