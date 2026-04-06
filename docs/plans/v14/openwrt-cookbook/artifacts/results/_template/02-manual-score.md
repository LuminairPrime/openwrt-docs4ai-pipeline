# Manual Score Record

## Run Context

- Agent label: `<agent-label>`
- Model: `<model-name>`
- Run label: `<YYYY-MM-DD-rerun-01>`
- Group name: `<alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota>`
- Scored by: `<operator>`
- Scored on: `YYYY-MM-DD`
- Prompt source: `00-prompt-source.txt`
- Answer key source: `00-key-source.txt`
- Group default evaluation mode: `full-review | short-duplicate-review | skipped-as-already-accepted`
- Earlier accepted-fail reference: `none | artifacts/results/<agent-label>/<run-label>/<group-name>/02-manual-score.md`

## Group Verdict

- Overall result: `pass | fail | mixed`
- Cookbook impact: `no-change | verification-evidence | cookbook-candidate-open | benchmark-only`

## Scenario Score Table

| Scenario | Verdict | Review mode | Earlier accepted-fail reference | Required paradigms present | Triggered falsenesses | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SXX | pass/fail | full-review / short-duplicate-review / skipped-as-already-accepted | none / prior score path |  |  |  |

## Triggered Truths And Falsenesses

### Confirmed truths

- 

### Triggered falsenesses

- 

## Narrative Scoring Notes

Briefly explain why each borderline case still passed or failed. If a grouped answer key was insufficient on its own, cite which underlying packet clarified the decision.

If this run repeated a scenario that had already been accepted as a cookbook-opening fail in an earlier iteration, say whether this duplicate was:

- materially the same failure and therefore only short-reviewed
- or a genuinely different failure shape worth preserving as new cookbook evidence

## Follow-up

- Needs new cookbook work: `yes | no`
- Failure family update needed: `yes | no`
- Additional blind rerun needed: `yes | no`
- Duplicate failure adds new cookbook learning: `yes | no`
- Notes:
  - 