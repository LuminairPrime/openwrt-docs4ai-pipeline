# Getting Started

## Purpose

This is the shortest path for maintainers who need to set up the repository, run the supported local validation flow, and find the right active docs.

## Prerequisites

```powershell
pip install -r .github/scripts/requirements.txt
npm install -g jsdoc-to-markdown
winget install --id JohnMacFarlane.Pandoc
```

Use the workspace interpreter directly when needed:

```powershell
.venv\Scripts\python.exe
```

Do not assume the system `python` on `PATH` is the repo interpreter.

## First Validation Commands

Run the smallest proof first, then expand:

```powershell
python tests/run_pytest.py
python tests/run_smoke.py
python tests/run_smoke_and_pytest.py
python tests/check_linting.py
```

Preferred one-command local proof:

```powershell
python tests/run_smoke_and_pytest.py
```

## AI Summary Workflow

Real AI-summary work is scratch-first and AI-store-first.

```powershell
python tools/manage_ai_store.py --option review
python tools/manage_ai_store.py --option promote
python tools/manage_ai_store.py --option full --keep-scratch
```

Use [guides/runbook-ai-summary-operations.md](guides/runbook-ai-summary-operations.md) for the full workflow and rollback guidance.

## When You Need Remote Proof

1. Push the branch or target commit.
2. Pin the exact commit SHA.
3. Wait for the matching hosted workflow run.
4. Read summary artifacts before raw logs.

Useful commands:

```powershell
git rev-parse HEAD
gh run list --workflow "openwrt-docs4ai pipeline (v12)" --limit 20 --json databaseId,headSha,status,conclusion,url
gh run watch <run_id> --exit-status --interval 15
gh run download <run_id> -n pipeline-summary -D tmp/ci/pipeline-summary
gh run download <run_id> -n extract-summary -D tmp/ci/extract-summary
```

The workflow name still uses the historical `v12` label. The active docs and output contracts do not.

## What To Read Next

- [ARCHITECTURE.md](ARCHITECTURE.md) for repository zones, the layer model, and the current doc taxonomy.
- [specs/pipeline-stage-catalog.md](specs/pipeline-stage-catalog.md) before changing stage order or rerun guidance.
- [specs/schema-definitions.md](specs/schema-definitions.md) before changing data fields, frontmatter, or output layout.
- [specs/release-tree-contract.md](specs/release-tree-contract.md) before changing the published corpus structure.
- [specs/cookbook-authoring-spec.md](specs/cookbook-authoring-spec.md) before changing authored cookbook content rules.