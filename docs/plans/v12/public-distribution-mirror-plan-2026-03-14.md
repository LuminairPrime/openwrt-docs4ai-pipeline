# Public Distribution Mirror Plan

> **Superseded by V5a.** See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md) for the active implementation specification.

Recorded: 2026-03-14

## Purpose

This plan defines the preferred first-draft architecture for splitting the
project into two public surfaces:

1. the source project repository, which contains the pipeline, tests, specs,
   and maintainer workflow
2. the product distribution repository, which contains the generated corpus for
   direct public consumption

The goal is to let a new maintainer implement the change end to end without
guesswork, while also giving a stakeholder a clean and understandable public
entry point such as `https://openwrt-docs4ai.github.io/llms.txt` without
exposing pipeline-development files.

## Executive Summary

- Keep this repository as the engineering system of record.
- Publish a second repository as the public distribution surface.
- Keep the generated corpus inside one top-level folder:
  `openwrt-condensed-docs/`.
- Keep the target repository root as a small public shell with its own landing
  files.
- Generate the ZIP from the same assembled distribution workspace that is pushed
  to the target repository.
- Name ZIP assets by date, not by the meaningless word `latest`.
- Implement cross-account publishing with a GitHub App from the start.

## Why The Split Exists

The split is justified because the project and the product serve different
audiences and have different stability requirements.

| Surface | Audience | What they need | What they do not need |
| --- | --- | --- | --- |
| Source project repository | Maintainers, contributors, reviewers, CI operators | pipeline code, tests, architecture docs, specs, bug logs, local workflow instructions | generated public-distribution shell decisions |
| Product distribution repository | Users, LLM operators, downstream tooling, casual GitHub visitors | generated corpus, browsing page, release ZIP, stable public URLs | `.github/`, tests, pipeline code, maintainer-only specs |

Short rule: the source repository explains how the corpus is made; the
distribution repository exposes the corpus itself.

## Locked First-Draft Decisions

| Topic | Decision | Reason |
| --- | --- | --- |
| Source repo role | Keep current role unchanged | It already owns extraction, validation, and publication logic |
| Target owner | Dedicated target account is acceptable for v1 | Simpler than an organization for a single distribution endpoint |
| Target repo | `openwrt-docs4ai.github.io` | Required if the target account should serve the root Pages URL |
| Generated corpus folder | `openwrt-condensed-docs/` | Already meaningful and correctly describes the artifact |
| Target repo root | Hand-maintained public shell plus generated corpus folder | Clear public landing surface without flattening the corpus |
| ZIP root | One folder only: `openwrt-condensed-docs/` | Prevents loose-file extraction and keeps the package self-contained |
| ZIP filename | `openwrt-docs4ai-YYYY-MM-DD.zip` | Human-readable, stable, and better than `latest` |
| HTML path semantics | Generated HTML speaks from the corpus root | Keeps web-visible paths consistent with extracted filesystem paths |
| Auth | GitHub App | Best long-term unattended automation model |

## Naming Model

Do not force one repeated name onto account, repository, folder, and archive.
Each name has a separate job.

| Item | Recommended name | Why |
| --- | --- | --- |
| Source repo | existing project repository name | It is an engineering system, not the public artifact |
| Target account | `openwrt-docs4ai` | Public distribution identity |
| Target repo | `openwrt-docs4ai.github.io` | Required user-site repo name |
| Generated corpus folder | `openwrt-condensed-docs` | Artifact identity on disk |
| ZIP asset | `openwrt-docs4ai-2026-03-14.zip` | Distribution identity plus publication date |

## Public Tree Layout

### Source project repository

This repository stays an engineering project.

```text
openwrt-docs4ai-v12-copilot/
|-- .github/
|   |-- scripts/
|   `-- workflows/
|-- lib/
|-- tests/
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- plans/
|   `-- specs/
|-- openwrt-condensed-docs/
|   |-- README.md                 generated artifact-scoped README
|   |-- index.html                generated artifact-scoped HTML index
|   |-- llms.txt
|   |-- llms-full.txt
|   |-- AGENTS.md
|   |-- L1-raw/
|   |-- L2-semantic/
|   `-- module folders...
`-- tmp/
```

### Target distribution repository

The target repository is not another copy of the source project. It is a public
distribution shell plus the generated corpus.

```text
openwrt-docs4ai.github.io/
|-- README.md                     hand-maintained public overview
|-- index.html                    hand-maintained public landing page
|-- llms.txt                      distribution-root router for AI users
|-- .nojekyll
`-- openwrt-condensed-docs/
    |-- README.md                 generated artifact-scoped README
    |-- index.html                generated artifact-scoped HTML index
    |-- llms.txt                  canonical corpus routing file
    |-- llms-full.txt
    |-- AGENTS.md
    |-- L1-raw/
    |-- L2-semantic/
    `-- module folders...
```

### ZIP archive

The ZIP intentionally excludes the target repository root shell.

```text
openwrt-docs4ai-2026-03-14.zip
`-- openwrt-condensed-docs/
    |-- README.md
    |-- index.html
    |-- llms.txt
    |-- llms-full.txt
    |-- AGENTS.md
    |-- L1-raw/
    |-- L2-semantic/
    `-- module folders...
```

This layout is preferred because users can extract the ZIP anywhere and get the
correct project-defined folder name without inventing their own extraction root.

## URL Map

The public site should make sense to both humans and tooling.

| URL | Role | Owner |
| --- | --- | --- |
| `https://openwrt-docs4ai.github.io/` | public landing page for the product distribution | hand-maintained target shell |
| `https://openwrt-docs4ai.github.io/README.md` | repository-level overview | hand-maintained target shell |
| `https://openwrt-docs4ai.github.io/llms.txt` | public AI entry router | root distribution file |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/` | generated corpus folder root | generated corpus |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/index.html` | generated human corpus browser | generated corpus |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/llms.txt` | canonical generated AI routing file | generated corpus |
| target repo Releases page | dated ZIP downloads | workflow-published assets |

The root `llms.txt` exists only to route public AI users into the corpus without
requiring them to understand the repository split. It is not a duplicate blind
copy of the inner corpus `llms.txt`; it is a distribution-level router.

## README Scope

### Source repository README

Keep [README.md](../../../README.md) hand-maintained. It should describe the engineering
project:

- what the source project does
- how maintainers work on it
- where architecture and specs live
- what the generated output tree is

It should not try to be the public product landing page.

### Target repository root README

Keep the target root `README.md` hand-maintained. It should describe the public
distribution:

- what the distributed corpus is
- who it is for
- where the generated corpus folder lives
- where to browse online
- where to download the dated ZIP
- where the source project repository lives

It should not explain pipeline internals in detail.

### Generated corpus README

Keep `openwrt-condensed-docs/README.md` generated by the pipeline. It should
explain the generated artifact only:

- what `llms.txt` is for
- what `llms-full.txt` is for
- what `AGENTS.md` is for
- what `index.html` is for
- what `L1-raw/` and `L2-semantic/` contain
- which consumers should use which entry points

It should not describe governance, account structure, or maintainer process.

## HTML Scope And Path Semantics

The generated corpus HTML must describe the extracted corpus root, not the target
repository root and not an abstract browser root.

That means the generated file at
`openwrt-condensed-docs/index.html` should render visible paths like:

```text
./index.html
./llms.txt
./L1-raw/luci/js_source-api-cbi.md
./ucode/ucode.d.ts
```

Those labels are accurate when a user is viewing the generated corpus as a
folder, whether from a ZIP extraction or from the public folder URL.

This requires the display-path contract in
[openwrt-docs4ai-07-generate-web-index.py](../../../.github/scripts/openwrt-docs4ai-07-generate-web-index.py)
and
[openwrt-docs4ai-08-validate-output.py](../../../.github/scripts/openwrt-docs4ai-08-validate-output.py)
to become configurable.

## Distribution Build Rule

The source workflow should assemble one exact public-distribution workspace after
the existing validated staging output is complete.

```text
validated final-staging
        |
        v
assembled public-distribution workspace
        |-- target root shell files
        `-- openwrt-condensed-docs/
                generated corpus
```

From that exact workspace:

1. push the workspace to the target repository
2. build the ZIP from the `openwrt-condensed-docs/` subtree
3. upload the ZIP to the target repository release

This is the critical anti-drift rule. The ZIP must not be built from a separate
later process on the target repository.

## ZIP Publishing Rule

The ZIP naming and replacement behavior should be explicit.

| Item | Rule |
| --- | --- |
| Asset filename | `openwrt-docs4ai-YYYY-MM-DD.zip` |
| Release cadence | update on every successful public mirror update |
| Same-day multiple publishes | replace the same dated asset for that UTC day |
| ZIP root | one folder only: `openwrt-condensed-docs/` |
| Included files | generated corpus subtree only |
| Excluded files | target root shell files such as root `README.md`, root `index.html`, and root `llms.txt` |

The date labels publication day, not a unique build identity. If the project
later needs multiple separately downloadable snapshots per day, add time or a
short run identifier as a second field. The first draft does not require that.

## Features Required

### Must change

| Area | Needed change |
| --- | --- |
| `lib/config.py` | add distribution target, corpus display root, site URL, and ZIP naming config |
| `07` generator | support configurable visible root semantics and release-link rendering |
| `08` validator | validate configurable path semantics and root-shell/corpus split |
| workflow deploy phase | assemble target distribution workspace, mint GitHub App token, push target repo, upload ZIP asset |
| tests | assert new root shell, corpus split, and ZIP contract |
| maintainer docs | explain source-vs-product split and GitHub App setup |

### Can stay the same

| Area | Why it stays |
| --- | --- |
| extraction stages | they already produce the validated corpus |
| current source-repo publish output | still useful for local inspection and current verification |
| module `llms.txt` generation | remains part of the corpus product |
| generated corpus folder name | already accurate and useful |
| current local-first verification model | still the right first gate |

## GitHub App Architecture

### Why GitHub App is the preferred method

GitHub App is preferred here because the project is intended to run unattended
for the long term.

| Topic | GitHub App | PAT |
| --- | --- | --- |
| Identity | service-like actor | tied to a human account |
| Permissions | fine-grained, installation-scoped | easier to over-scope |
| Token lifetime | short-lived installation tokens minted on demand | long-lived secret used directly |
| Long-term maintainability | strong | weak |
| Initial setup complexity | higher | lower |

The installation token expiring hourly is not a maintenance problem. The workflow
is expected to mint a fresh token each run. The long-lived secret is the app
private key.

### Required GitHub App capabilities

The GitHub App should be installed only on the target distribution repository and
granted the minimum permissions needed for:

- repository contents write
- metadata read
- releases write

If target Pages settings are configured once manually, the App does not need to
own recurring Pages-administration changes.

## Risks And Mitigations

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| ZIP and mirrored tree diverge | users download one artifact and browse another | build both from the same assembled distribution workspace |
| Public users land on the wrong README | source-project docs confuse product consumers | keep hand-maintained target root shell separate from generated corpus docs |
| HTML path labels do not match extraction layout | trust in the package decreases | make path labels relative to the extracted corpus root |
| Root `llms.txt` becomes a stale blind copy | AI consumers get broken links | make root `llms.txt` a distribution router, not a copied corpus file |
| GitHub App setup complexity blocks adoption | feature stalls | include exact setup steps and verification commands in maintainer docs |
| Future account or owner move breaks Pages URLs | public links become unstable | treat target namespace as durable and document transfer risks up front |
| Same-day asset replacement obscures older snapshots | users cannot fetch every build separately | accept in first draft; add timestamped assets only if needed later |

## Organization Versus Dedicated User Account

For this feature, the difference is primarily ownership and governance, not how
the public Pages site looks.

- A GitHub Pages site served from an organization-owned repository does not look
  materially different from one served from a user-owned repository.
- The public site itself is just static content.
- The meaningful differences are backend ownership, access control, auditability,
  and how easy it is to share administration with other maintainers.

First-draft choice: use a dedicated target account if that gets the feature
moving faster.

Reason: the product output is simple and generated, so an organization is not a
functional requirement today.

Still, keep the workflow parameterized so the target can be changed later.

## Implementation Phases

1. Add the saved architecture plan and lock the naming model.
2. Add config variables for public distribution root, target repo, and ZIP
   naming.
3. Rework the generated corpus HTML and validator to support configurable corpus
   root semantics.
4. Define the target root shell files and the root `llms.txt` router contract.
5. Extend the deploy workflow to assemble the public-distribution workspace.
6. Add GitHub App authentication and target-repo push.
7. Add dated ZIP creation and release upload.
8. Update tests and maintainer docs.

## Verification Criteria

The feature is only complete when all of the following are true:

1. A new developer can read this plan and implement the distribution workflow
   without architectural guesswork.
2. A stakeholder can visit the target GitHub Pages site and understand the
   product without seeing the pipeline-development files.
3. `https://openwrt-docs4ai.github.io/llms.txt` routes clearly into the corpus.
4. `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/index.html` shows
   paths that match the extracted corpus root.
5. The ZIP file contains only `openwrt-condensed-docs/` at archive root.
6. The ZIP contents and the mirrored corpus subtree match.
7. The source repository continues to run and publish successfully with its
   current responsibilities intact.

## Outcome Expected From This Plan

- The project stays a project.
- The product gets its own clean public distribution site.
- The generated corpus remains honest about its own filesystem shape.
- The ZIP feels like a real package instead of a pile of loose files.
- A public visitor can follow a root URL such as `/llms.txt` without getting
  mixed up with maintainer-only source files.