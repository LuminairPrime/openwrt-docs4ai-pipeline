---
name: pytest-coverage
description: Run pytest with coverage, inspect uncovered lines, and close the gaps with tests.
---

# Pytest Coverage

Use this skill when coverage matters more than just pass or fail.

## Workflow

1. Run pytest with coverage output.
2. Focus on the touched module or test slice first.
3. Inspect uncovered lines.
4. Add targeted tests for missed branches and error paths.
5. Re-run the same narrow coverage check.

## Commands

```bash
pytest --cov --cov-report=annotate:cov_annotate
pytest tests/path/test_file.py --cov=package.module --cov-report=annotate:cov_annotate
```

## What to inspect

- files with coverage below target
- lines marked with `!` in `cov_annotate`
- missing branches, not just happy-path statements

## Priorities

- validate behavior first
- add narrow tests before broad suite runs
- cover edge cases and error handling before chasing cosmetic percentage gains