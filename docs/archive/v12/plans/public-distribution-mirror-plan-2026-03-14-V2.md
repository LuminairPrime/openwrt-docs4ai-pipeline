# Public Distribution Mirror — Architecture & Implementation Specification (V2)

> **Superseded by V5a.** Auth and deploy details carried forward into V5a. See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md).

**Recorded:** 2026-03-14
**Supersedes:** `public-distribution-mirror-plan-2026-03-14.md`
**Status:** Active reference specification
**Scope:** Defines the complete architecture, constraints, implementation
sequence, and operational schema for publishing the generated
`openwrt-condensed-docs` corpus to a dedicated public distribution repository.

---

## 1. Purpose

This document is the authoritative long-term reference for splitting the
openwrt-docs4ai project into two public surfaces:

1. **Source project repository** — the pipeline, tests, specs, and maintainer
   workflow.
2. **Product distribution repository** — the generated corpus for direct public
   consumption, served via GitHub Pages and downloadable as dated ZIP releases.

This specification is written so that a developer can implement the entire
feature end to end without ambiguity. Every decision that was left open or
implicit in the V1 plan is now resolved with a concrete constraint.

---

## 2. Architectural Rationale

### 2.1 Why the split exists

The project and the product serve different audiences with different stability
requirements.

| Surface | Audience | They need | They do not need |
| --- | --- | --- | --- |
| Source repository | Maintainers, contributors, CI operators | Pipeline code, tests, architecture docs, specs, local workflow instructions | Distribution shell files, public landing pages |
| Distribution repository | Users, LLM operators, downstream tooling, casual visitors | Generated corpus, browsing page, release ZIP, stable public URLs | `.github/`, tests, pipeline code, maintainer specs |

**Rule:** The source repository explains how the corpus is made. The
distribution repository exposes the corpus itself.

### 2.2 What the current pipeline already does

Before this feature, the pipeline already:

- Builds the validated corpus into `staging/` (`OUTDIR`) inside the `process`
  job.
- Promotes `staging/` into `openwrt-condensed-docs/` (`PUBLISH_DIR`) inside the
  `deploy` job via `rsync -a --delete`.
- Mirrors `openwrt-condensed-docs/` into a `gh-pages` branch on the source
  repository for GitHub Pages.
- Runs on `push` to `main`, a monthly cron schedule, and `workflow_dispatch`.

This feature adds a second deployment target: a cross-account push to the
distribution repository plus a ZIP release asset.

---

## 3. Locked Decisions

These decisions are final and must not be revisited during implementation.

| # | Topic | Decision | Constraint |
| --- | --- | --- | --- |
| D1 | Source repo role | Unchanged; remains the engineering system of record | No distribution shell files live in this repository |
| D2 | Target owner type | **GitHub Organization** | See §4 for rationale; the organization name is `openwrt-docs4ai` |
| D3 | Target repo name | `openwrt-docs4ai.github.io` | Required for user-site Pages URL serving at the organization root |
| D4 | Corpus folder name | `openwrt-condensed-docs/` | Already meaningful; used consistently across source, target, and ZIP |
| D5 | Target repo root | Source-controlled public shell plus generated corpus folder | Shell files are version-controlled in the source repo and are deployed by CI |
| D6 | ZIP contents | Exactly `openwrt-condensed-docs/` and nothing else | The public shell is excluded; see §8.2 for packaging rules |
| D7 | ZIP filename | `openwrt-docs4ai-YYYY-MM-DD.zip` | Date-stamped; no `latest` alias; see §8.2 |
| D8 | Auth mechanism | GitHub App with installation token | Private key stored as Actions secret; see §6 |
| D9 | Deployment trigger | Same as existing pipeline: `push` to `main`, monthly cron, `workflow_dispatch` | No separate schedule; the distribution push is an extension of the existing `deploy` job |
| D10 | Git history strategy | Append-only commits on target `main` | No force-push; no orphan branch resets; see §9.2 |

---

## 4. Account Type Decision: Organization

### 4.1 Why Organization, not User

The V1 plan left this as "dedicated target account is acceptable." This V2
specification upgrades the decision to Organization for the following reasons:

1. **Multi-admin resilience.** An Organization allows adding multiple human
   owners. If the primary maintainer loses access, a second owner can recover
   the GitHub App, rotate secrets, and manage the repository without a
   GitHub Support ticket.
2. **Machine-user isolation.** Organizations provide a clean boundary between
   human identities and automated API consumers. The GitHub App is installed on
   the Organization's repository, not bound to a personal account's identity.
3. **Zero cost.** GitHub Organizations are free for public repositories.
4. **Identical Pages URL.** An Organization named `openwrt-docs4ai` serves
   content from `openwrt-docs4ai.github.io` identically to a User account.
5. **No conversion penalty risk.** While GitHub allows converting a User to an
   Organization, the conversion strips SSH keys, personal tokens, and can
   disrupt GitHub App installations. Starting as an Organization eliminates the
   risk of a future migration.

### 4.2 Domain name reservation

The GitHub namespace (`openwrt-docs4ai`) is claimed at account creation time.
The account type (User vs Organization) does not affect namespace reservation.
However, because converting User → Organization is a one-way operation that
interrupts authentication state and governance expectations, creating it as an
Organization from Day 1 avoids future disruption with no downside.

---

## 5. Naming Model

Each name has a separate job. Do not collapse them.

| Item | Name | Purpose |
| --- | --- | --- |
| Source repo | `openwrt-docs4ai-v12-copilot` (current) | Engineering system identity |
| Target org | `openwrt-docs4ai` | Public distribution identity |
| Target repo | `openwrt-docs4ai.github.io` | GitHub Pages user-site repo |
| Corpus folder | `openwrt-condensed-docs` | Artifact identity on disk and in URLs |
| ZIP asset | `openwrt-docs4ai-YYYY-MM-DD.zip` | Distribution identity plus publication date |
| GitHub App | `openwrt-docs4ai-publisher` (recommended) | CI automation identity |

---

## 6. Authentication Architecture

### 6.1 GitHub App setup

| Property | Value |
| --- | --- |
| App name | `openwrt-docs4ai-publisher` |
| App owner | The source repository owner's account |
| Repository permissions | `Contents: Read & Write` |
| Installation scope | Installed on `openwrt-docs4ai/openwrt-docs4ai.github.io` only |

### 6.2 Secrets stored in the source repository

| Secret name | Value | Used by |
| --- | --- | --- |
| `DIST_APP_ID` | The GitHub App's numeric App ID | `deploy` job |
| `DIST_APP_PRIVATE_KEY` | The PEM-encoded private key | `deploy` job |

### 6.3 Token exchange at runtime

The `deploy` job exchanges the App ID and private key for a short-lived
installation access token using a verified Action such as
`actions/create-github-app-token@v2`. The token is scoped to the target
repository and expires automatically.

**Constraint:** The installation token must never be logged, exported to
artifacts, or passed between jobs. It is created and consumed within the same
job.

---

## 7. Repository Layouts

### 7.1 Source project repository

```text
openwrt-docs4ai-v12-copilot/
├── .github/
│   ├── scripts/                  numbered pipeline scripts
│   └── workflows/                GitHub Actions workflows
├── lib/                          shared Python support code
├── tests/                        local tests and smoke runners
├── docs/
│   ├── ARCHITECTURE.md
│   ├── plans/
│   └── specs/
├── templates/
│   └── distribution-shell/       source-controlled target shell files
├── openwrt-condensed-docs/       generated corpus (committed)
└── tmp/                          ephemeral workspace
```

The `templates/distribution-shell/` directory is new. It contains the
source-controlled copies of the target repository root files. This ensures they
are version-tracked, reviewable, and testable inside the engineering
repository, while being deployed verbatim to the distribution repository root
during CI.

### 7.2 Target distribution repository

```text
openwrt-docs4ai.github.io/
├── README.md                     from templates/distribution-shell/
├── index.html                    from templates/distribution-shell/
├── llms.txt                      from templates/distribution-shell/
├── .nojekyll                     from templates/distribution-shell/
└── openwrt-condensed-docs/       synced by CI from source pipeline output
    ├── README.md                 generated
    ├── index.html                generated
    ├── llms.txt                  generated (canonical corpus router)
    ├── llms-full.txt             generated
    ├── AGENTS.md                 generated
    ├── L1-raw/                   generated
    ├── L2-semantic/              generated
    └── {module}/                 generated
```

### 7.3 ZIP archive

```text
openwrt-docs4ai-YYYY-MM-DD.zip
└── openwrt-condensed-docs/
    ├── README.md
    ├── index.html
    ├── llms.txt
    ├── llms-full.txt
    ├── AGENTS.md
    ├── L1-raw/
    ├── L2-semantic/
    └── {module}/
```

**Constraint:** The ZIP contains exactly the `openwrt-condensed-docs/` tree and
nothing else. No shell files. No `.git`. No `tmp/`.

---

## 8. Build and Packaging Rules

### 8.1 Staging directories

The `deploy` job must use two logically distinct staging areas. These are runner
temporary paths, not committed directories.

| Staging area | Contents | Used for |
| --- | --- | --- |
| `$RUNNER_TEMP/dist-pages/` | Target repo checkout with shell plus synced corpus | GitHub Pages push |
| `$RUNNER_TEMP/dist-artifact/` | Copy of `openwrt-condensed-docs/` only | ZIP packaging |

**Constraint:** These two staging areas must be populated from the same
validated `final-staging` artifact downloaded earlier in the job. They must not
be populated from different pipeline runs or different build steps.

### 8.2 ZIP packaging rules

1. Copy the validated `final-staging` artifact into
   `$RUNNER_TEMP/dist-artifact/openwrt-condensed-docs/`.
2. Create the ZIP from `$RUNNER_TEMP/dist-artifact/` so that the archive root
   is `openwrt-condensed-docs/`.
3. Name the ZIP `openwrt-docs4ai-$(date -u +%Y-%m-%d).zip`.
4. The ZIP must not contain the distribution shell files (`README.md`,
   `index.html`, `llms.txt`, `.nojekyll` from the target root).

### 8.3 Pages sync rules

1. Clone the target repository `main` branch into `$RUNNER_TEMP/dist-pages/`.
2. Sync the generated corpus using `rsync` with explicit path boundaries so the
   resulting target tree contains `openwrt-condensed-docs/` as a full subtree.
3. Copy shell files from the source repository's
   `templates/distribution-shell/` into the target root, overwriting any
   previous deployed copies.
4. Commit and push from `$RUNNER_TEMP/dist-pages/` to the target `main` branch.

**Design note:** Shell files are source-controlled in the engineering repo under
`templates/distribution-shell/` and are deployed by CI. This makes them
reviewable, testable, and immune to manual drift on the target repository. The
target repository root should never be treated as an authoritative edit surface.

---

## 9. Deployment Constraints

### 9.1 Gatekeeper: pre-push sanity checks

Before the cross-repository push executes, the pipeline must assert all of the
following conditions. If any check fails, the push must be skipped and the job
must exit with a non-zero status.

| Check | Assertion | Rationale |
| --- | --- | --- |
| Corpus existence | `openwrt-condensed-docs/llms.txt` exists | Prevents pushing an empty or broken corpus |
| Corpus minimum size | `openwrt-condensed-docs/llms.txt` is greater than 512 bytes | Prevents pushing a stub or truncated routing file |
| Index existence | `openwrt-condensed-docs/index.html` exists | Prevents pushing without a browsable landing page |
| Module count | At least 4 module subdirectories exist under `openwrt-condensed-docs/` | Prevents pushing a partially generated corpus |

### 9.2 Git history strategy on the target repository

- **Append-only.** Every CI push creates a normal commit on `main`. No
  force-push, no orphan branch reset, no history rewriting.
- **Commit message format:**
  `docs: corpus update YYYY-MM-DD (source commit SHORTHASH)`
  where `SHORTHASH` is the 7-character SHA of the source repository commit that
  triggered the pipeline.
- **Committer identity:** `github-actions[bot]` with the noreply email.
- **History growth management:** normal Git delta compression is expected to be
  sufficient for this text-heavy repository. No history-pruning strategy is part
  of V1.

### 9.3 Release minting

After a successful push to the target repository, the pipeline creates or updates
a GitHub Release on `openwrt-docs4ai/openwrt-docs4ai.github.io` with:

| Property | Value |
| --- | --- |
| Tag name | `v$(date -u +%Y-%m-%d)` |
| Release name | `openwrt-docs4ai $(date -u +%Y-%m-%d)` |
| Body | Auto-generated from commit message; include source commit SHA |
| Asset | `openwrt-docs4ai-YYYY-MM-DD.zip` |
| Pre-release | `false` |
| Draft | `false` |

**Constraint:** If a release with the same tag already exists, the pipeline must
update the existing release rather than failing. The dated ZIP asset must be
replaced in place for same-day reruns.

### 9.4 Failure isolation

| Failure point | Impact | Recovery |
| --- | --- | --- |
| Gatekeeper check fails | No push, no release; pipeline fails visibly | Fix the upstream corpus generation issue and re-run |
| Target repo clone fails | No push, no release; pipeline fails visibly | Check network, App token, target repo existence |
| Push to target fails | No release; pipeline fails visibly | Check App permissions, branch protection rules |
| Release creation fails | Corpus is live on Pages but no ZIP download | Re-run pipeline or create the release manually |

**Rule:** A failure in the distribution push must never affect the existing
source repository promotion step. The `deploy` job must attempt the source-repo
promotion and `gh-pages` mirror first, and only then attempt the cross-account
distribution push. This preserves current verified behavior if the new feature
fails.

---

## 10. URL Map

| URL | Content | Owner |
| --- | --- | --- |
| `https://openwrt-docs4ai.github.io/` | Public landing page | Shell `index.html` |
| `https://openwrt-docs4ai.github.io/README.md` | Public overview | Shell `README.md` |
| `https://openwrt-docs4ai.github.io/llms.txt` | Distribution-level AI router | Shell `llms.txt` |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/` | Generated corpus root | Generated `index.html` |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/index.html` | Human corpus browser | Generated |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/llms.txt` | Canonical AI routing file | Generated |
| `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/llms-full.txt` | Flat catalog | Generated |
| Releases page | Dated ZIP downloads | CI-published |

### 10.1 Root `llms.txt` routing contract

The root `llms.txt` is a **distribution-level router**, not a copy of the inner
corpus `llms.txt`. Its job is to direct an LLM consumer into the corpus without
requiring knowledge of the repository structure.

**Required content pattern:**

```text
# openwrt-docs4ai

> OpenWrt documentation corpus for LLM context ingestion.

## Documentation Corpus
- [Corpus Routing Index](./openwrt-condensed-docs/llms.txt)
- [Flat Catalog](./openwrt-condensed-docs/llms-full.txt)
- [Agent Instructions](./openwrt-condensed-docs/AGENTS.md)
```

**Constraint:** All links in the root `llms.txt` must be relative paths
starting with `./openwrt-condensed-docs/`. The inner corpus `llms.txt` uses
paths relative to itself. These two scopes must never be mixed.

### 10.2 Root `index.html` routing contract

The root `index.html` should be a simple landing page that includes a visible
link to the corpus browser at `./openwrt-condensed-docs/index.html`. It may
optionally include an automatic meta-refresh redirect, but must also provide a
clickable link for accessibility and non-JavaScript consumers.

---

## 11. File Ownership and Mutability Rules

Every file in the distribution repository has exactly one owner.

| File or Path | Owner | CI behavior |
| --- | --- | --- |
| `README.md` (root) | `templates/distribution-shell/` | Overwritten every push from template |
| `index.html` (root) | `templates/distribution-shell/` | Overwritten every push from template |
| `llms.txt` (root) | `templates/distribution-shell/` | Overwritten every push from template |
| `.nojekyll` | `templates/distribution-shell/` | Overwritten every push from template |
| `openwrt-condensed-docs/` | Pipeline `final-staging` artifact | Entire subtree replaced via `rsync --delete` |

**Rule:** No file in the distribution repository is authoritative unless it is
owned either by the source repo templates or by the source repo generated
corpus. The distribution repository is a deployment target, not a development
environment.

---

## 12. Source Repository Changes Required

### 12.1 New directory: `templates/distribution-shell/`

Create the following files:

| File | Purpose |
| --- | --- |
| `templates/distribution-shell/README.md` | Public-facing overview of the distribution |
| `templates/distribution-shell/index.html` | Landing page with link or redirect to corpus browser |
| `templates/distribution-shell/llms.txt` | Distribution-level AI routing file |
| `templates/distribution-shell/.nojekyll` | Empty file to disable Jekyll on GitHub Pages |

### 12.2 Workflow modifications

The `deploy` job in `.github/workflows/openwrt-docs4ai-00-pipeline.yml` must be
extended. The new steps must be appended **after** the existing source-repo
promotion and `gh-pages` mirror steps so existing behavior is not disrupted.

New steps, in order:

1. Generate GitHub App token.
2. Run gatekeeper checks.
3. Prepare dist-artifact staging and create the ZIP.
4. Prepare dist-pages staging by cloning the target repo and syncing content.
5. Push to target repository.
6. Create or update GitHub Release and upload the ZIP.

### 12.3 Configuration surface

This feature does not require heavy Python-side configuration changes if the
runner-temporary paths remain workflow-owned. The primary code changes are:

- template shell files under `templates/`
- deploy workflow extensions
- tests that lock the contract
- optional small constants if path prefixes need to be shared by scripts

---

## 13. Implementation Phases

### Phase 0: Infrastructure provisioning

**Prerequisites:** None.
**Deliverables:** Target organization and repository exist and are configured.

| Step | Action | Verification |
| --- | --- | --- |
| 0.1 | Create GitHub Organization `openwrt-docs4ai` | Org profile page is accessible |
| 0.2 | Add at least one backup human owner to the org | Two owners visible in org settings |
| 0.3 | Create repository `openwrt-docs4ai/openwrt-docs4ai.github.io` | Repo exists and is public |
| 0.4 | Enable GitHub Pages on the repo, source: `main` branch, root `/` | Pages settings show deployment source |
| 0.5 | Create GitHub App `openwrt-docs4ai-publisher` | App ID and private key available |
| 0.6 | Install the App on the target repository | Installation visible in org settings |
| 0.7 | Store `DIST_APP_ID` and `DIST_APP_PRIVATE_KEY` as Actions secrets in the source repo | Secrets exist in source repo settings |

### Phase 1: Shell templates

**Prerequisites:** Phase 0 complete.
**Deliverables:** Shell template files committed to the source repository.

| Step | Action | Verification |
| --- | --- | --- |
| 1.1 | Create `templates/distribution-shell/` | Directory exists |
| 1.2 | Write `README.md` for the public distribution | Content describes the product, not pipeline internals |
| 1.3 | Write `index.html` for the public landing page | HTML links clearly to the corpus browser |
| 1.4 | Write root `llms.txt` router | All links point into `./openwrt-condensed-docs/` |
| 1.5 | Add `.nojekyll` | File exists |
| 1.6 | Commit the templates | Source repo diff shows all shell files under `templates/` |

### Phase 2: Gatekeeper and packaging logic

**Prerequisites:** Phase 1 complete.
**Deliverables:** Sanity checks and ZIP creation behavior are implemented and testable.

| Step | Action | Verification |
| --- | --- | --- |
| 2.1 | Implement gatekeeper checks from §9.1 | Checks pass against current valid corpus |
| 2.2 | Implement ZIP packaging logic from §8.2 | Archive contains exactly `openwrt-condensed-docs/` |
| 2.3 | Validate same-day rerun assumptions in release logic design | No duplicate asset naming ambiguity remains |

### Phase 3: Workflow integration

**Prerequisites:** Phases 0 through 2 complete.
**Deliverables:** Updated `deploy` job with cross-repo push and release steps.

| Step | Action | Verification |
| --- | --- | --- |
| 3.1 | Add GitHub App token generation to `deploy` | Token generation step succeeds in CI |
| 3.2 | Add gatekeeper step | Step passes or fails visibly in CI |
| 3.3 | Add dist-artifact staging and ZIP creation | ZIP is created with expected name and root |
| 3.4 | Add dist-pages staging and sync logic | Target staging matches §7.2 layout |
| 3.5 | Add target push step | Target repo receives a new commit |
| 3.6 | Add release creation or update step | Release appears with correct tag and asset |
| 3.7 | Run full `workflow_dispatch` pipeline | End-to-end success on a live target |

### Phase 4: Hardening and documentation

**Prerequisites:** Phase 3 verified green.
**Deliverables:** Documentation and tests are aligned with the final design.

| Step | Action | Verification |
| --- | --- | --- |
| 4.1 | Update `docs/ARCHITECTURE.md` with dual-repo deployment section | Architecture doc reflects the new model |
| 4.2 | Update `README.md` with public distribution link | Source README points to the public surface |
| 4.3 | Add or extend tests for gatekeeper and distribution contract | Local pytest passes |
| 4.4 | Verify same-day re-run behavior | Second run updates release rather than failing |
| 4.5 | Verify failure isolation manually | Source deploy still succeeds if target push is intentionally broken |

---

## 14. Deployment Sequence

```text
deploy job starts
│
├── 1. Checkout source repo
├── 2. Download final-staging artifact
├── 3. Promote staging → openwrt-condensed-docs/ on source repo
├── 4. Commit and push source repo changes if needed
├── 5. Mirror openwrt-condensed-docs/ → gh-pages branch
│
│   existing behavior ends; new distribution steps begin
│
├── 6. Generate GitHub App installation token
├── 7. Run gatekeeper sanity checks
│     └── FAIL? exit 1 and skip distribution publish
├── 8. Prepare dist-artifact staging
├── 9. Create ZIP from dist-artifact
├── 10. Prepare dist-pages staging
│      ├── clone target repo main
│      ├── sync openwrt-condensed-docs/
│      └── copy templates/distribution-shell/* to target root
├── 11. Commit and push target repo main
└── 12. Create or update GitHub Release with ZIP asset
```

**Critical ordering rule:** Steps 1 through 5 must remain intact and succeed
before steps 6 through 12 begin. A failure in steps 6 through 12 must not
invalidate the already-completed source-repo deployment work.

---

## 15. Testing Strategy

### 15.1 Local tests

| Test | What it checks | Location |
| --- | --- | --- |
| Gatekeeper unit test | Valid corpus passes, empty or stub corpus fails | `tests/pytest/` |
| Shell template contract test | Root `llms.txt` links resolve into the corpus path prefix | `tests/pytest/` |
| ZIP packaging test | Archive contains exactly `openwrt-condensed-docs/` | `tests/pytest/` |

### 15.2 CI integration tests

| Test | What it checks |
| --- | --- |
| `workflow_dispatch` live run | Full pipeline completes including distribution push |
| Same-day idempotency run | Existing release is updated, not duplicated |
| Gatekeeper rejection run | Intentionally broken corpus prevents target publish |

---

## 16. Operational Monitoring

### 16.1 Success indicators

After each pipeline run that includes a distribution push:

- Target repo `main` branch has a new commit.
- GitHub Pages at `https://openwrt-docs4ai.github.io/openwrt-condensed-docs/llms.txt`
  matches the source pipeline's generated `llms.txt`.
- A release exists with today's date tag and a non-empty ZIP asset.

### 16.2 Failure indicators

- `deploy` job fails after step 5: distribution push issue; source repo is
  unaffected.
- `deploy` job fails before step 5: existing pipeline issue; unrelated to this
  feature.
- Target repo has no commit for today: pipeline did not run or gatekeeper
  rejected the corpus.

---

## 17. Future Considerations Out of Scope for V1

These items are explicitly deferred.

| Item | Reason for deferral |
| --- | --- |
| Custom domain such as `docs.example.org` | Requires DNS and CNAME management; not needed for V1 |
| Multiple ZIP variants such as per-module archives | Adds complexity without proven user need |
| Automated release changelog generation | Requires diff analysis between releases |
| CDN or mirror distribution | GitHub Pages and Releases are sufficient for V1 |
| Source-repo root `llms.txt` | Intentionally deferred by the existing architecture |

---

## 18. Document Relationships

| Document | Relationship |
| --- | --- |
| [docs/ARCHITECTURE.md](../../../docs/ARCHITECTURE.md) | Must be updated in Phase 4 to describe the dual-repo model |
| [README.md](../../../README.md) | Must be updated in Phase 4 to mention the public distribution URL |
| [docs/archive/v12/specs/execution-map.md](../specs/execution-map.md) | Deploy description should be extended after implementation |
| [docs/archive/v12/specs/schema-definitions.md](../specs/schema-definitions.md) | Corpus contract remains unchanged |
| [docs/archive/v12/specs/implementation-status.md](../specs/implementation-status.md) | Should be updated after live Phase 3 verification |
| [openwrt-docs4ai-00-pipeline.yml](../../../.github/workflows/openwrt-docs4ai-00-pipeline.yml) | Primary implementation target |

---

## Appendix A: V1 ambiguities resolved in V2

| V1 issue | Resolution in V2 |
| --- | --- |
| ZIP built from the same workspace but shell excluded | §8 defines two explicit staging areas with different packaging scope |
| No deployment trigger cadence defined | §3 D9 locks triggers to the existing deploy model |
| No atomicity or failure-domain analysis | §9.4 and §14 define failure isolation and sequencing |
| No target git history strategy | §9.2 locks append-only bot commits |
| Ambiguous root versus inner `llms.txt` path semantics | §10.1 separates routing scopes explicitly |
| User versus Organization left open | §4 locks Organization with rationale |
| Shell files described as hand-maintained but not operationally owned | §7.1, §8.3, and §11 move shell ownership into source-controlled templates |
| No gatekeeper to prevent publishing broken corpora | §9.1 defines mandatory pre-push checks |
| No same-day release replacement rule | §9.3 defines update-in-place behavior |

This V2 document is the implementation-safe architecture reference for the
public distribution mirror feature.
