# Public Distribution Delivery Specification (V3)

> **Partially superseded by V5a.** Delivery architecture preserved; public tree layout changed. See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md).

Recorded: 2026-03-15

Status: Authoritative implementation specification

Scope: Define the exact repository topology, delivery tree, packaging model,
and deployment rules for publishing the public OpenWrt product without leaking
internal build-folder names into the public contract.

## 1. Purpose

This document defines the final public-delivery architecture for the project.

The goal is simple:

1. The public website must live at the organization root domain.
2. The release repository must be named `corpus` and nothing public should rely
   on that name except the repository itself.
3. The downloadable ZIP must expand into a project-named folder,
   `openwrt-docs4ai/`, not `corpus/` and not `openwrt-condensed-docs/`.
4. Every published surface must be assembled from the same validated content and
   must be refreshed as an exact tree so stale files cannot linger.

This specification is written to teach a developer what to build, what not to
build, and which shortcuts are forbidden.

## 2. Final Outcome

After implementation, the product has three public delivery surfaces:

| Surface | Public identity | What the user sees |
| --- | --- | --- |
| Organization Pages site | `https://openwrt-docs4ai.github.io/` | Direct-root documentation site with no `corpus/` path and no `openwrt-condensed-docs/` path |
| Release repository | `openwrt-docs4ai/corpus` | A GitHub repository named `corpus` that contains the fresh release tree at repository root |
| Downloadable archive | `openwrt-docs4ai-YYYY-MM-DD.zip` | A ZIP that expands into `openwrt-docs4ai/` |

All three surfaces come from the same validated delivery tree.

## 3. Locked Decisions

These decisions are final for V3 and must not be reopened during
implementation.

| Topic | Decision | Constraint |
| --- | --- | --- |
| Organization | Use the GitHub organization `openwrt-docs4ai` | The Pages root domain is the organization site |
| Pages repository | Use `openwrt-docs4ai.github.io` | Required for the organization-root site |
| Release repository | Use `corpus` | `corpus` is a repository name only, not a public path or folder contract |
| Public project name | Use `openwrt-docs4ai` | This is the ZIP root folder name and product name |
| Public website layout | Use direct-root layout | No public `openwrt-condensed-docs/` wrapper folder |
| Release repository layout | Use direct-root layout | No repository-root `openwrt-condensed-docs/` wrapper folder |
| ZIP layout | Wrap the direct-root delivery tree inside `openwrt-docs4ai/` | Prevent loose-file extraction while keeping the public root contract clean |
| Delivery freshness | Publish exact trees only | Every target repo update must delete stale files |
| Auth model | Use a GitHub App installation token | No long-lived PAT-based publish flow |
| Same-day reruns | Update the same dated release and replace the dated asset | No same-day asset sprawl |

## 4. Public Naming Model

Each name has one job. Do not reuse one label for unrelated concerns.

| Concern | Name | Public meaning |
| --- | --- | --- |
| Source engineering repository | current development repository | Maintainer and pipeline workspace only |
| GitHub organization | `openwrt-docs4ai` | Owner of the public site and release repos |
| Pages repository | `openwrt-docs4ai.github.io` | Root-domain website source |
| Release repository | `corpus` | Repository and Releases surface only |
| Public product folder | `openwrt-docs4ai` | ZIP extraction root |
| ZIP asset | `openwrt-docs4ai-YYYY-MM-DD.zip` | Dated product snapshot |
| Internal legacy folder name | `openwrt-condensed-docs` | Internal source-repo or staging detail only, never a public contract |

### 4.1 Forbidden name leakage

The following rules are mandatory:

1. Do not expose `openwrt-condensed-docs` in public URLs.
2. Do not expose `openwrt-condensed-docs` in visible HTML path labels.
3. Do not expose `openwrt-condensed-docs` as the ZIP root folder.
4. Do not expose `corpus` in website paths or in ZIP folder names.
5. Do not teach consumers to browse a public `corpus/` subdirectory.

## 5. Repository Topology

### 5.1 Source engineering repository

The source repository remains the system of record for:

- pipeline code
- tests
- specs
- delivery assembly rules
- source-controlled public-root overlay files

It is not a public delivery surface.

### 5.2 Pages repository

The Pages repository exists only to serve the organization-root site.

Repository:

```text
openwrt-docs4ai/openwrt-docs4ai.github.io
```

Rules:

1. The repository root is the public product root.
2. The repository is published from `main` branch root.
3. The deployed tree must be an exact assembled tree, not a partial overlay on
   top of previous contents.
4. The repository is not manually edited.

### 5.3 Release repository

The release repository exists to hold the fresh product tree and dated ZIP
releases.

Repository:

```text
openwrt-docs4ai/corpus
```

Rules:

1. The repository root is the public product root.
2. The repository name `corpus` is visible on GitHub only as repository
   identity.
3. The repository is not the Pages source for the root-domain site.
4. The repository is not manually edited.
5. GitHub Releases are created here, not on the Pages repository.

## 6. Canonical Public Tree Contract

The public product tree is direct-root. This is the contract that must be
served by the Pages repository and committed into the release repository.

```text
public-root/
├── README.md
├── index.html
├── llms.txt
├── llms-full.txt
├── AGENTS.md
├── CHANGES.md
├── changelog.json
├── cross-link-registry.json
├── repo-manifest.json
├── signature-inventory.json
├── L1-raw/
├── L2-semantic/
├── luci/
├── luci-examples/
├── openwrt-core/
├── openwrt-hotplug/
├── procd/
├── uci/
├── ucode/
└── wiki/
```

### 6.1 Direct-root rules

The public tree rules are strict:

1. `README.md` is a product-root README, not the source-repo README.
2. `index.html` is a product-root HTML index.
3. `llms.txt` and `llms-full.txt` are product-root routing files.
4. All module folders live at product root.
5. `L1-raw/` and `L2-semantic/` live at product root.
6. No outer `openwrt-condensed-docs/` folder is allowed on either public repo.

## 7. ZIP Contract

The ZIP package wraps the direct-root public tree inside a project-named folder
for extraction hygiene.

```text
openwrt-docs4ai-YYYY-MM-DD.zip
└── openwrt-docs4ai/
    ├── README.md
    ├── index.html
    ├── llms.txt
    ├── llms-full.txt
    ├── AGENTS.md
    ├── CHANGES.md
    ├── changelog.json
    ├── cross-link-registry.json
    ├── repo-manifest.json
    ├── signature-inventory.json
    ├── L1-raw/
    ├── L2-semantic/
    ├── luci/
    ├── luci-examples/
    ├── openwrt-core/
    ├── openwrt-hotplug/
    ├── procd/
    ├── uci/
    ├── ucode/
    └── wiki/
```

### 7.1 ZIP rules

1. The ZIP root folder name is `openwrt-docs4ai`.
2. The ZIP root folder name must not be `corpus`.
3. The ZIP root folder name must not be `openwrt-condensed-docs`.
4. The ZIP contents must match the canonical public tree.
5. Pages-only files such as `.nojekyll` are not required inside the ZIP.
6. The ZIP must be built from the same validated delivery tree used for the two
   target repositories.

## 8. Source-Controlled Delivery Inputs

The source repository must own the public-root files that are not simply copied
from generated output.

Create this directory layout in the source repository:

```text
delivery-root/
├── common/
│   └── README.md
├── pages/
│   └── .nojekyll
└── release/
    └── (optional release-repo-only root files)
```

### 8.1 Why this directory exists

This directory exists for one reason: target repositories must never become the
authoritative source for hand-authored public-root files.

The source repository remains authoritative for:

- the public-root README
- Pages-only root files such as `.nojekyll`
- any future release-repo-only root files

### 8.2 Overlay ownership rules

| Path in source repo | Ownership | Applied to |
| --- | --- | --- |
| `delivery-root/common/` | Shared public-root overlay | Pages repo, release repo, ZIP |
| `delivery-root/pages/` | Pages-only overlay | Pages repo only |
| `delivery-root/release/` | Release-repo-only overlay | Release repo only |

### 8.3 Required first implementation

For V3, the required source-controlled public-root overlay is:

1. `delivery-root/common/README.md`
2. `delivery-root/pages/.nojekyll`

`delivery-root/release/` must exist even if it is empty at first, because the
architecture explicitly allows release-repo-only files later.

## 9. Assembly Model

The build must produce one canonical delivery tree and fan it out into three
delivery targets.

### 9.1 Canonical assembly flow

```text
validated generated output
        |
        v
canonical delivery tree
        |
        +--> Pages tree
        +--> Release repo tree
        `--> ZIP tree
```

### 9.2 Canonical delivery tree rules

The canonical delivery tree must be created in a clean temporary directory on
every run.

Assembly order:

1. Start from an empty temporary directory.
2. Copy the validated generated output into that directory.
3. If the generated output still exists under an internal wrapper such as
   `openwrt-condensed-docs/`, strip that wrapper during assembly so the
   temporary directory becomes the direct-root public tree.
4. Overlay `delivery-root/common/` last so source-controlled public-root files
   can intentionally replace generated root files when required.

### 9.3 Pages tree rules

The Pages tree is built from the canonical delivery tree plus the Pages-only
overlay.

Assembly order:

1. Start from a clean checkout of `openwrt-docs4ai.github.io`.
2. Delete all tracked and untracked content in the checkout except `.git`.
3. Copy the canonical delivery tree to repository root.
4. Overlay `delivery-root/pages/`.
5. Commit and push only if content changed.

### 9.4 Release repository tree rules

The release repository tree is built from the canonical delivery tree plus the
release-only overlay.

Assembly order:

1. Start from a clean checkout of `corpus`.
2. Delete all tracked and untracked content in the checkout except `.git`.
3. Copy the canonical delivery tree to repository root.
4. Overlay `delivery-root/release/`.
5. Commit and push only if content changed.

### 9.5 ZIP tree rules

The ZIP tree is built from the canonical delivery tree, not from either target
repository checkout.

Assembly order:

1. Start from an empty temporary ZIP staging directory.
2. Create `openwrt-docs4ai/` inside that staging directory.
3. Copy the canonical delivery tree into `openwrt-docs4ai/`.
4. Create the dated ZIP from that staging directory.

## 10. Freshness and Exact-Tree Rules

Freshness is a core requirement, not a best-effort preference.

### 10.1 Mandatory freshness rules

1. Every public deployment begins from clean temporary assembly directories.
2. Every target repository checkout is cleaned before content is copied in.
3. Every copy into a target repository uses delete semantics.
4. No target repository is allowed to keep orphaned files from older releases.
5. The ZIP is built from the current canonical delivery tree only.
6. The release process must never re-zip the current contents of the release
   repository as a shortcut.

### 10.2 What the developer must not do

The developer must not:

1. copy new files over an old target tree without deleting missing files
2. treat the previous release repo checkout as a staging source
3. build the ZIP from the release repo checkout
4. manually patch target repositories to fix drift
5. let Pages and release repo trees diverge except for explicit surface-only
   overlay files

## 11. Public Path Contract

The product root is the public browsing root.

That means the human-visible path contract is root-relative.

### 11.1 Required visible path examples

The following are correct:

```text
./index.html
./llms.txt
./wiki/llms.txt
./ucode/ucode.d.ts
./L2-semantic/wiki/wiki_page-guide-developer-luci.md
```

The following are forbidden:

```text
./openwrt-condensed-docs/index.html
./openwrt-condensed-docs/wiki/llms.txt
./corpus/index.html
./corpus/wiki/llms.txt
```

### 11.2 HTML generator rules

The generated product-root `index.html` must:

1. display root-relative visible labels
2. link to actual root-relative files and folders
3. avoid any visible `openwrt-condensed-docs` prefix
4. avoid any visible `corpus` prefix
5. describe the product tree as the published root tree, not as a nested
   subtree

### 11.3 Routing-file rules

The product-root `llms.txt` and `llms-full.txt` must:

1. route from the direct-root product tree
2. use links such as `./luci/llms.txt` and `./wiki/llms.txt`
3. avoid links that begin with `./openwrt-condensed-docs/`
4. avoid links that begin with `./corpus/`

## 12. File Ownership Rules

Every file in the two target repositories must have one owner.

| Target path | Owner | Notes |
| --- | --- | --- |
| `README.md` | `delivery-root/common/README.md` | This is the public-root README, not the source-repo README |
| `index.html` | generated product output unless explicitly replaced by overlay later | Product-root HTML browse page |
| `llms.txt` | generated product output | Product-root AI router |
| `llms-full.txt` | generated product output | Product-root flat catalog |
| `AGENTS.md` | generated product output | Product-root agent instructions |
| `CHANGES.md` and root JSON registries | generated product output | Product telemetry and release metadata |
| `.nojekyll` | `delivery-root/pages/.nojekyll` | Pages repo only |
| everything under `L1-raw/`, `L2-semantic/`, and module folders | generated product output | Direct-root content tree |

### 12.1 Ownership rule for target repositories

Target repositories are deployment targets only.

That means:

1. no direct hand edits are authoritative there
2. no hotfix commit is allowed there unless the same change is first made in the
   source repository
3. any manual patch in a target repo must be treated as drift and removed on the
   next publish unless codified in the source repo

## 13. Source Repository Behavior

The source repository may continue to use `openwrt-condensed-docs/` internally
while implementation is in progress, but that internal name must not remain part
of the public contract.

### 13.1 Internal-to-public transition rule

If the source pipeline still generates a nested directory like
`openwrt-condensed-docs/`, the assembly step must flatten that content into the
canonical direct-root delivery tree.

### 13.2 Source repository Pages rule

The source repository `gh-pages` branch, if it continues to exist during the
transition, is not the final public contract.

The public contract for V3 is:

1. organization-root Pages site from `openwrt-docs4ai.github.io`
2. release repository `corpus`
3. dated ZIP releases from `corpus`

## 14. Authentication and Automation

### 14.1 GitHub App model

Use a GitHub App installed on both public target repositories.

Required installation scope:

1. `openwrt-docs4ai/openwrt-docs4ai.github.io`
2. `openwrt-docs4ai/corpus`

Required repository permissions:

1. metadata read
2. contents write

### 14.2 Secrets stored in the source repository

The deploy workflow should use source-repo secrets for:

1. GitHub App ID
2. GitHub App private key

The workflow must mint short-lived installation tokens during the deploy job.

### 14.3 Forbidden auth shortcuts

Do not:

1. use a maintainer PAT as the long-term deployment mechanism
2. store long-lived repo tokens for `corpus` or `openwrt-docs4ai.github.io`
3. manually copy SSH deploy keys into the workflow as the primary model

## 15. Release and Tagging Rules

GitHub Releases belong on `openwrt-docs4ai/corpus`.

### 15.1 Release naming rules

| Item | Rule |
| --- | --- |
| Release tag | `vYYYY-MM-DD` |
| Release name | `openwrt-docs4ai YYYY-MM-DD` |
| ZIP asset | `openwrt-docs4ai-YYYY-MM-DD.zip` |

### 15.2 Same-day rerun rules

If the pipeline republishes on the same UTC date:

1. update the existing dated release
2. replace the existing dated ZIP asset
3. do not create a second same-day asset with a different filename unless a new
   future spec explicitly requires build-level archival

## 16. Primary Implementation Targets

The current codebase already contains the old nested assumptions. The following
areas must be updated to implement V3 correctly.

| Area | Why it must change |
| --- | --- |
| [lib/config.py](../../../lib/config.py) | Remove public coupling to `openwrt-condensed-docs` and add delivery-tree configuration if needed |
| [.github/scripts/openwrt-docs4ai-07-generate-web-index.py](../../../.github/scripts/openwrt-docs4ai-07-generate-web-index.py) | Generate root-relative visible paths and root-relative links |
| [.github/scripts/openwrt-docs4ai-08-validate-output.py](../../../.github/scripts/openwrt-docs4ai-08-validate-output.py) | Validate the direct-root contract and reject legacy-prefix leakage |
| [.github/workflows/openwrt-docs4ai-00-pipeline.yml](../../../.github/workflows/openwrt-docs4ai-00-pipeline.yml) | Assemble the canonical delivery tree and publish it to two repos plus ZIP |
| generated output tests under [tests/pytest/](../../../tests/pytest/) and [tests/support/](../../../tests/support/) | Lock the new direct-root contract, freshness rules, and ZIP contract |

## 17. Implementation Sequence

Implement in this order.

### Phase 0: Provision public infrastructure

1. Create the `openwrt-docs4ai` organization if it does not already exist.
2. Create `openwrt-docs4ai.github.io`.
3. Create `corpus`.
4. Configure the GitHub App and install it on both repos.

### Phase 1: Add source-controlled public-root inputs

1. Create `delivery-root/common/README.md`.
2. Create `delivery-root/pages/.nojekyll`.
3. Create `delivery-root/release/`.

### Phase 2: Build the canonical delivery tree

1. Add a clean delivery-tree assembly step.
2. Strip any internal outer wrapper during assembly.
3. Apply the common overlay.

### Phase 3: Fix product-root generators and validators

1. Update the HTML generator to emit root-relative visible paths.
2. Update routing-file generation if it still emits legacy prefixes.
3. Update validators to reject legacy prefix leakage.

### Phase 4: Publish to the two target repositories

1. Assemble a clean Pages tree.
2. Assemble a clean release-repo tree.
3. Push each tree only if content changed.

### Phase 5: Publish dated ZIP releases

1. Assemble the ZIP tree from the canonical delivery tree.
2. Create or update the dated release on `corpus`.
3. Upload or replace the dated ZIP asset.

### Phase 6: Lock tests and documentation

1. Add tests for direct-root URLs and visible labels.
2. Add tests for stale-file deletion behavior.
3. Update maintainer docs with the new repo topology and delivery flow.

## 18. Validation Requirements

The implementation is not complete until all of the following are verified.

### 18.1 Tree-contract validation

1. No public repo root contains an `openwrt-condensed-docs/` wrapper.
2. The Pages repo root matches the canonical delivery tree plus Pages-only
   overlay files.
3. The release repo root matches the canonical delivery tree plus
   release-repo-only overlay files.
4. The ZIP expands into `openwrt-docs4ai/` and matches the canonical delivery
   tree.

### 18.2 Path-contract validation

1. `index.html` displays `./index.html`, not
   `./openwrt-condensed-docs/index.html`.
2. `index.html` displays `./wiki/llms.txt`, not
   `./openwrt-condensed-docs/wiki/llms.txt`.
3. `llms.txt` and `llms-full.txt` use direct-root links.
4. No visible path contains `./corpus/`.

### 18.3 Freshness validation

1. A test fixture with an orphaned target file must prove that publish removes
   the orphan.
2. A same-day rerun must prove that the dated release is updated, not duplicated.
3. A Pages publish and a release-repo publish from the same run must prove they
   came from the same canonical delivery tree.

## 19. Do and Do Not

### 19.1 Do

1. Build one canonical delivery tree per run.
2. Treat target repositories as disposable deployment targets.
3. Keep the public site root and release repo root direct-root.
4. Keep the ZIP root project-named.
5. Keep `corpus` limited to repository identity.

### 19.2 Do not

1. Do not publish a public `openwrt-condensed-docs/` wrapper.
2. Do not publish a public `corpus/` wrapper.
3. Do not reuse the source-repo README as the public-root README.
4. Do not allow stale files to survive between releases.
5. Do not build the ZIP from a target repository checkout.
6. Do not manually patch the target repositories as a normal workflow.

## 20. Acceptance Criteria

This specification is satisfied only when all of the following are true:

1. `https://openwrt-docs4ai.github.io/` serves the product from root with no
   `corpus/` segment and no `openwrt-condensed-docs/` segment.
2. `https://github.com/openwrt-docs4ai/corpus` contains a fresh direct-root
   product tree.
3. `openwrt-docs4ai-YYYY-MM-DD.zip` expands into `openwrt-docs4ai/`.
4. The product-root HTML and routing files display root-relative paths.
5. A republish removes stale files from both public repositories.
6. The source repository remains the only authoritative editing surface.
