# Public Distribution Product Output Naming And Layout Plan (V4a)

> **Incorporated into V5a.** Naming contract locked. See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md).

Recorded: 2026-03-15

Status: Decision baseline for the next implementation step

Scope: Plan the release-stage file and folder naming scheme, product output
layout, and lowest-risk pipeline changes needed so the public release tree
makes immediate sense to AI programming tools without requiring them to first
read maintainer documentation.

Relationship to V4b: V4a locks the selected product-output naming and layout
contract. V4b defines the delivery, staging, include, packaging, and
publication mechanics that act on that locked contract.

---

## 1. Purpose

The release repository is a product for AI programming tools and their human
operators.

It is not:

- a training corpus for model pretraining
- a dump of every intermediate pipeline artifact
- a public mirror of maintainer-facing pipeline vocabulary

The release tree should help tools like GitHub Copilot, Codex, Claude Code,
and similar IDE-integrated agents understand OpenWrt-specific APIs, workflows,
configuration patterns, and subsystem structure so they can make fewer mistakes
while helping users program OpenWrt systems.

The key product requirement for naming is this:

**A tool that sees only the release filenames and folder names should be able to
infer what to open first, what is broad versus targeted context, and which file
forms are alternate packagings of the same authoritative material.**

---

## 2. Product Boundary

### 2.1 What the release should contain

The release should contain only files that materially help OpenWrt developers
and their AI tools program OpenWrt packages and systems.

That normally includes:

- root routing files for AI tool entry
- human operator guidance for using the release tree
- module-level routing files
- module-level quick orientation maps
- module-level full single-file references
- module-level smaller page-based references
- optional typed helper files when they materially aid programming

### 2.2 What the release should not contain by default

The release should not contain files whose primary purpose is:

- extraction debugging
- maintainer-only provenance review
- pipeline correctness diagnosis
- internal drift accounting without direct programming value

That means the public release should plan to exclude, unless a concrete use case
is proven later:

- `L1-raw/`
- L1 `.meta.json` sidecars
- `repo-manifest.json`
- `cross-link-registry.json`
- `signature-inventory.json`
- `changelog.json`
- `CHANGES.md`

Those may still remain available in the development repository or full pipeline
output for maintainers.

---

## 3. What AI Tools Actually Do Today

The effective consumption order already works like a progressive abstraction
ladder:

```text
root llms router
  -> module llms router
     -> map.md
        -> bundled-reference.md
           -> chunked-reference/<topic>.md
```

This is the reverse of the build graph.

The build graph goes from extracted source to canonical page records to bundled
references and routers. The consumer graph goes from routers and maps down to
the exact topic pages only when needed.

That abstraction pattern is good and should be preserved. The main problem is
that the current public names leak pipeline stage names instead of consumer role
names.

---

## 4. Current Confusion Points

These are the highest-value user stories and confusion risks observed so far.

### 4.1 Confusion list

1. The biggest source of confusion is not the existence of layers. It is
   exposing pipeline-layer names such as `L1` and `L2` in the same public root
   as product-facing files.
2. The second biggest source of confusion is duplicate authority. A first-time
   tool sees a module-level complete reference file and a set of smaller topic
   files and has to infer whether one is canonical and the other is just a
   convenience copy.
3. The current names describe how the pipeline thinks better than how a
   consuming tool thinks.
4. `skeleton` is more precise than `overview`, but it still benefits from a
   clarifying word such as `structural` or `navigation`.
5. `complete-reference` is a strong phrase, but the page-based companion needs
   a matching name that makes the twin relationship obvious.
6. The release tree should tell a tool what the files are for before the tool
   reads the file bodies.

### 4.2 User stories

- As an AI programming tool dropped into the release root with no prior
  knowledge, I can infer which file starts the routing flow.
- As an AI programming tool inside a module folder, I can infer which file is
  the structural map, which file is the large one-file reference, and where the
  smaller page set lives.
- As an AI programming tool, I can tell from names alone that the large bundled
  reference and the smaller page set differ by packaging and context size, not
  by trust or authority.
- As a human operator, I can explain the release tree without needing to teach
  maintainers' internal pipeline vocabulary such as L1 and L2.
- As a maintainer, I can keep development-only artifacts in the development
  repository while producing a release tree that looks product-shaped from the
  start.
- As a release validator, I can assert that development-layer names do not leak
  into the product tree.

---

## 5. Build Dependency Chart

The release plan should respect the current dependency graph instead of trying
to re-architect the working pipeline in one risky pass.

### 5.1 Current build graph

```text
upstream sources
  -> clone/fetch stage
     -> repo-manifest.json
  -> extractor stages
     -> L1 markdown
     -> L1 sidecar metadata
  -> normalization stage
     -> L2 canonical markdown pages
     -> cross-link registry
  -> optional AI enrichment
     -> enriched L2 frontmatter
  -> assembly stage
     -> module skeleton files
     -> module complete-reference files
  -> companion generation
     -> AGENTS.md
     -> product README.md
  -> typed tooling generation
     -> module .d.ts files
  -> telemetry generation
     -> changelog files
     -> signature inventory
  -> routing generation
     -> root llms.txt
     -> root llms-full.txt
     -> module llms.txt
  -> HTML generation
     -> product index.html
  -> validation
     -> publishable output tree
```

### 5.2 Current consumer graph

```text
README.md or AGENTS.md
  -> llms.txt
     -> module llms.txt
        -> map.md
           -> bundled-reference.md
              -> chunked-reference/<topic>.md
```

This consumer graph is the one the release names should serve.

---

## 6. Naming Design Goals

The release naming system should satisfy all of the following:

1. Communicate file role from the path alone.
2. Distinguish broad-context files from targeted-context files.
3. Make twin relationships obvious when two file forms contain the same
   underlying programming documentation.
4. Avoid leaking internal stage names such as `L1-raw` and `L2-semantic`.
5. Preserve existing conventions only when they materially help tools.
6. Minimize pipeline risk by preferring rename-and-relocate changes over deep
   extractor rewrites.
7. Allow a human operator to add release-specific files without editing target
   repositories directly.
8. Support fixed-schema module children so an AI tool can predict the same
   filenames inside every module folder.
9. Require public output names to come from shared config or lib constants
   instead of being scattered as string literals across scripts and workflow
   files.

---

## 7. Twin-File Naming Discussion

### 7.1 The real relationship between the current forms

The current module-level complete reference file is assembled by concatenating
the bodies of the smaller canonical pages.

That means the important distinction is not authority. The important
distinction is packaging form:

- one large file for broad ingestion
- many smaller pages for targeted ingestion

Therefore the release naming should communicate **same documentation, different
form**.

### 7.2 Should every smaller page carry the large-file phrase in its filename?

Probably not.

The smaller topic pages should remain topic-discoverable. Prefixing every leaf
filename with a long phrase like `single-file-complete-reference` or similar
would make the filenames harder to scan and weaken topical findability.

Preferred rule:

- put the form meaning in the folder name
- keep the leaf filenames topical and specific
- put an explicit authority and usage note in the module router and in the
  large bundled file

Example:

```text
luci/
├── bundled-reference.md
└── chunked-reference/
   ├── javascript-api-cbi.md
   ├── javascript-api-firewall.md
   └── ...
```

This is clearer than repeating the packaging role in every leaf filename.

### 7.3 Is folder-level context enough?

For tools that preserve path context, yes, usually.

For maximum clarity, the path should be reinforced by visible text in:

- the module `llms.txt`
- the module `README.md`
- the first paragraph of the single-file bundled reference

Recommended short note for the bundled file:

> This file contains the same authoritative programming documentation as the
> pages in `./chunked-reference/`. Use this file for broad ingestion.
> Use the page set for targeted ingestion and smaller context windows.

### 7.4 Is `concat` useful in the filename?

It is precise, but it describes the build operation rather than the user value.

Tradeoff:

- `concatenated` or `concat` explains implementation
- `single-file` explains the form the user experiences

Recommendation:

- keep implementation words such as `concatenated` out of the primary filename
- mention the concatenation fact in the opening note or metadata

Rationale: AI tools need to know what to open, not how the file was built.

### 7.5 Locked naming contract

The naming decision for the next implementation step is now locked.

Inside every module folder, the public release contract is:

- `llms.txt`
- `map.md`
- `bundled-reference.md`
- `chunked-reference/`
- optional `types/`

Example:

```text
uci/
├── llms.txt
├── map.md
├── bundled-reference.md
└── chunked-reference/
    ├── data-types.md
    ├── network-qos.md
    └── read-write.md
```

### 7.6 Why this contract is selected

This contract wins because it optimizes for the actual consumer behavior of
IDE-integrated AI tools.

- `map.md` is the clearest fixed-schema orientation filename.
- `bundled-reference.md` and `chunked-reference/` share the same root word,
   which makes the twin relationship visible from filenames alone.
- The module folder already carries the namespace, so repeating the module name
   inside child filenames wastes tokens and weakens predictability.
- The terms describe how the user should consume the files, not how the build
   pipeline created them.
- The same filenames can exist in every module folder, enabling zero-shot
   traversal after the first successful encounter.

### 7.7 Required authority and usage note

The fixed-schema filenames are strong, but the equal-authority rule still needs
to be stated explicitly in the visible routing text.

Every module-level routing surface should reinforce all of the following:

- `chunked-reference/` and `bundled-reference.md` contain the same
   authoritative programming content.
- `chunked-reference/` is for targeted lookups and smaller context windows.
- `bundled-reference.md` is for broad ingestion and subsystem-wide context.
- tools should normally read one form or the other for a task, not both.

Minimum places to carry that note:

- module `llms.txt`
- opening section of `map.md`
- opening section of `bundled-reference.md`

### 7.8 Terms removed from the public contract

The following terms should no longer appear in the public release naming
contract for this feature:

- `skeleton`
- `complete-reference`
- `source-docs`
- `combined-reference`
- `concatenated-reference`
- `L1-raw`
- `L2-semantic`

Some of these may still exist internally during the refactor, but they are no
longer valid public-facing names.

---

## 8. Router And Map Terminology

The term `router` is useful conceptually, but the file naming should preserve
existing `llms.txt` conventions because they already carry meaning for AI tool
consumers.

Recommendation:

- keep the filename `llms.txt`
- use visible titles and README copy that call it a router
- avoid renaming the actual file away from `llms.txt` unless a future product
  decision intentionally abandons that convention

Example visible title or lead line inside the file:

```text
# luci AI Retrieval Router
```

This gets the semantic benefit of the word `router` without breaking a useful
convention.

---

## 9. Main Output Root Versus Published Release Tree

The refactored pipeline should write into one main output root that contains two
required child folders.

```text
main-output/
├── release-tree/
└── support-tree/
```

The actual folder names must later come from shared config or lib constants.
The names above are the plan-level working terms for now.

### 9.1 `release-tree/`

`release-tree/` is the exact public tree.

Rules:

- it contains only release-ready files and folders
- it is the only subtree eligible for release-repo sync and ZIP packaging
- it uses the final public names locked by V4a
- target repositories should not need to reinterpret or rename anything inside
   it

### 9.2 `support-tree/`

`support-tree/` contains non-release artifacts that still matter to the
pipeline, maintainers, or validators.

Typical examples:

- extracted raw captures
- intermediate canonical page records
- telemetry and provenance artifacts
- stage diagnostics and other maintainer-only machine outputs

This folder is intentionally outside the public release contract.

### 9.3 Former `L2-semantic/` redistribution rule

The old public meaning of `L2-semantic/` is not being preserved under a new
name. The change is deeper than a rename.

The rule for the next implementation step is:

- the public release tree no longer exposes a top-level `L2-semantic/`
- the semantic programming content that used to sit under
   `L2-semantic/{module}/` is redistributed into the corresponding module's
   `chunked-reference/`
- if the pipeline still needs an internal semantic-page workspace, that
   workspace lives only under `support-tree/`

### 9.4 Risk guidance

The pipeline should still be refactored with minimal structural risk.

Preferred approach:

1. keep early extraction and normalization stages mostly intact
2. move release-shaping into a late assembly step
3. write public names only into `release-tree/`
4. keep internal helper surfaces under `support-tree/`
5. let V4b define how `release-tree/` is validated and published

---

## 10. Version-Controlled Release Include

There should be a version-controlled include directory in the development
repository that can add or override files inside the release tree.

Working plan location:

```text
release-inputs/
└── release-include/
```

This keeps hand-authored release assembly inputs in one logical parent folder
instead of scattering them at repository root.

The final directory names must later come from shared config or lib constants,
but the behavior is locked now.

### 10.1 Include purpose

The include exists so the operator can intentionally inject or replace files in
the release output without editing target repositories by hand.

Examples:

- replacing the generated root `README.md`
- adding a release-only helper file
- overriding a generated root guidance file
- adding future hand-authored release files that the generator does not own

### 10.2 Include rules

1. The generator writes `release-tree/` first.
2. `release-inputs/release-include/` is applied after that generation step.
3. The include may add new files or replace generated files by path.
4. The same overlaid release tree is the source for both release-repo sync and
   ZIP packaging.
5. The include does not apply to `support-tree/`.
6. Target repositories are never the authoritative place for manual release-only
   edits.

---

## 11. Current And Proposed Product Trees

### 11.1 Current public-shape tree today

```text
openwrt-condensed-docs/
├── README.md
├── AGENTS.md
├── llms.txt
├── llms-full.txt
├── index.html
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

### 11.2 Proposed main output root

```text
main-output/
├── release-tree/
│  ├── README.md
│  ├── AGENTS.md
│  ├── llms.txt
│  ├── llms-full.txt
│  ├── index.html
│  ├── luci/
│  │  ├── llms.txt
│  │  ├── map.md
│  │  ├── bundled-reference.md
│  │  └── chunked-reference/
│  │     ├── javascript-api-cbi.md
│  │     ├── javascript-api-firewall.md
│  │     └── ...
│  ├── luci-examples/
│  ├── openwrt-core/
│  ├── openwrt-hotplug/
│  ├── procd/
│  ├── uci/
│  ├── ucode/
│  │  ├── llms.txt
│  │  ├── map.md
│  │  ├── bundled-reference.md
│  │  ├── chunked-reference/
│  │  └── types/
│  │     └── ucode.d.ts
│  └── wiki/
└── support-tree/
   ├── raw/
   ├── semantic-pages/
   ├── manifests/
   └── telemetry/

```

The support subfolders shown above are illustrative. Their exact names may
change during implementation, but they remain support-only and never become
public release names.

---

## 12. Rename Matrix

| Current name or concept | New contract | Notes |
| --- | --- | --- |
| `L1-raw/` | support-only, not released | Can remain under `support-tree/` if still useful |
| `L2-semantic/{module}/<topic>.md` | `release-tree/{module}/chunked-reference/<topic>.md` | Public semantic content is redistributed into module-local chunked references |
| `*-skeleton.md` | `{module}/map.md` | Fixed public schema; no module prefix inside the module folder |
| `*-complete-reference.md` | `{module}/bundled-reference.md` | Fixed public schema; paired with `chunked-reference/` |
| module page folder | `{module}/chunked-reference/` | Fixed public schema |
| root `llms.txt` | `release-tree/llms.txt` | Keep filename; root router remains part of the public contract |
| module `llms.txt` | `{module}/llms.txt` | Keep filename; module router remains part of the public contract |
| module `.d.ts` at module root | `{module}/types/<module>.d.ts` | Optional typed helpers stay optional |

---

## 13. Locked V4a Direction

The next implementation step should treat the following as fixed requirements.

1. Every public module folder uses the fixed schema `llms.txt`, `map.md`,
   `bundled-reference.md`, and `chunked-reference/`, with optional `types/`.
2. The module directory is the namespace. Child filenames do not repeat the
   module name.
3. The main output root contains both `release-tree/` and `support-tree/`.
4. Only `release-tree/` is eligible for release-repo sync and ZIP packaging.
5. `release-inputs/release-include/` is applied after release-tree assembly so
   hand-authored files can add to or override generated release files.
6. The former top-level `L2-semantic/` public surface is replaced by
   per-module `chunked-reference/` folders.
7. All public output names must come from shared config or lib constants rather
   than hard-coded strings spread across scripts and workflow files.

---

## 14. Remaining Non-Blocking Questions

These questions remain open, but none of them should block the next
implementation step.

1. Should module-local `README.md` files remain optional or be part of the
   first fixed-schema release contract?
2. Should `support-tree/` keep a persistent semantic-page subtree after the
   refactor, or can later stages consume temporary working files instead?
3. Should future Pages publication consume `release-tree/` unchanged, or should
   it be allowed a small target-specific include later?
4. What is the oversized-module rule for `bundled-reference.md` when a module
   still exceeds practical single-file limits?
   - keep a stable `bundled-reference.md` index that points to
     `bundled-reference.part-*.md`
   - or require very large modules to rely more heavily on
     `chunked-reference/`

---

## 15. Additional Risks To Watch

The following risks should be treated as active implementation concerns, not as
background commentary.

### 15.1 Bundled and chunked parity risk

`bundled-reference.md` and `chunked-reference/` are supposed to be equal in
authority. If late assembly omits sections, rewrites links differently, or
injects different explanatory text into the two forms, the public contract will
silently break.

### 15.2 Oversized module risk

The current pipeline already shards oversized monoliths into part files. That
behavior does not disappear just because the public contract was renamed.

This must be double-checked before implementation starts on large modules such
as `wiki`, because the new `bundled-reference.md` contract needs an explicit
large-module strategy.

### 15.3 Link rewriting risk

The root router, module routers, bundled references, HTML browse output, and
validation logic currently assume old paths such as `L2-semantic/` and old file
names such as `*-skeleton.md` and `*-complete-reference.md`.

If any one of those surfaces is left behind, the public tree will look renamed
but still route tools into the wrong places.

### 15.4 Duplicate retrieval risk

IDE-integrated AI tools may index both `bundled-reference.md` and the files in
`chunked-reference/`. That can cause duplicate retrieval hits, token waste, and
conflicting ranking behavior if the routing notes are weak or the search layer
later treats both forms equally.

### 15.5 Include precedence risk

`release-inputs/release-include/` only remains safe if it has one clear merge
point after release generation and before validation. Multiple include passes,
or target-repository hotfixes after publish, would reintroduce drift.

### 15.6 Deterministic topic-path risk

The leaf names inside `chunked-reference/` must stay stable and topic-shaped
across runs. If their naming rules drift, the release will create noisy diffs,
broken links, and weaker external references.

---

## 16. Double-Check List Before Implementation Starts

These items should be explicitly checked before code changes begin.

1. Confirm whether module-local `README.md` is in or out of the first locked
   public contract.
2. Confirm the large-module rule for `bundled-reference.md`, including whether
   part files remain part of the public surface.
3. Confirm whether root `README.md`, `AGENTS.md`, and root routing files are
   generator-owned by default or expected to be commonly replaced by
   `release-inputs/release-include/`.
4. Confirm whether the support tree is a persistent on-disk contract or merely
   a convenient late-stage staging tree whose internal children may evolve.
5. Confirm whether future Pages publication should consume `release-tree/`
   unchanged or whether a separate Pages-only include is expected later.
6. Confirm whether semantic search duplication between bundled and chunked forms
   needs only documentation in the first pass or a stronger ignore/indexing
   strategy later.

---

## 17. Expected Script And Test Impact

The refactor will touch more than naming docs. The current codebase already has
hard-coded expectations around old public paths and filenames.

### 17.1 Scripts that clearly need contract updates

The main late-stage script surfaces that will need public-contract updates are:

- `.github/scripts/openwrt-docs4ai-05a-assemble-references.py`
- `.github/scripts/openwrt-docs4ai-05b-generate-agents-and-readme.py`
- `.github/scripts/openwrt-docs4ai-06-generate-llm-routing-indexes.py`
- `.github/scripts/openwrt-docs4ai-07-generate-web-index.py`
- `.github/scripts/openwrt-docs4ai-08-validate-output.py`

They currently encode assumptions about:

- `L2-semantic/`
- `*-skeleton.md`
- `*-complete-reference.md`
- old HTML labels and routing targets

Earlier stages such as `03` and `04` may keep more of their current internal
shape, but they still need to be double-checked once the dual-tree output model
is introduced.

### 17.2 Tests that will definitely need updates

The following current test surfaces are directly tied to the old contract and
should be expected to change:

- `tests/support/smoke_pipeline_support.py`
- `tests/pytest/pytest_02_fixture_pipeline_contract_test.py`
- `tests/pytest/pytest_06_warning_regression_test.py`

These files currently assert old paths and filenames such as:

- `L2-semantic/...`
- `ucode-skeleton.md`
- `wiki-skeleton.md`
- `*-complete-reference.md`
- HTML labels rooted under `./openwrt-condensed-docs/...`

### 17.3 Test and validation work that should be added

The refactor should also add new checks for:

1. `release-tree/` versus `support-tree/` separation.
2. exclusion of `support-tree/` from release-repo sync and ZIP packaging.
3. merge precedence and replacement behavior for
   `release-inputs/release-include/`.
4. bundled-versus-chunked parity for representative modules.
5. absence of top-level public `L1-raw/` and `L2-semantic/` leakage in the
   release tree.
6. updated root and module routing files that point to `map.md`,
   `bundled-reference.md`, and `chunked-reference/`.
7. the selected oversized-module behavior if sharded bundled-reference parts are
   retained.

---

## 18. V4b Handoff

V4b should now implement mechanics against the locked V4a contract.

That means V4b needs to define:

- the exact config or lib constants that own public output names
- dual-output-root creation and promotion rules
- release-include merge order and validation
- release-repo and ZIP rules that consume only `release-tree/`
- acceptance checks proving that the old top-level `L2-semantic/` surface no
  longer leaks into the public release tree