# Public Distribution Delivery Mechanics Plan (V4b)

> **Incorporated into V5a.** Mechanics absorbed. See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md).

Recorded: 2026-03-15

Status: Decision baseline aligned to the selected V4a contract

Scope: Define the delivery, staging, packaging, and publication mechanics that
act on the finalized V4a product-output tree.

This document assumes that V4a already locked the following product contract:

- every public module folder uses `llms.txt`, `map.md`,
  `bundled-reference.md`, and `chunked-reference/`, with optional `types/`
- module names are not repeated in child filenames inside the module folder
- the refactored main output root contains both a release-ready tree and a
  support-only tree
- the former public `L2-semantic/` surface is replaced by module-local
  `chunked-reference/`
- `release-inputs/release-include/` may add or override files in the
   release-ready tree before publication

---

## 1. Purpose

V4b converts the selected V4a naming and layout contract into an implementation
plan that can be handed to the pipeline refactor.

The core mechanics requirement is this:

**The pipeline must generate one exact release-ready tree, one separate
support-only tree, and one predictable include merge, and only the release-ready
tree may be published to external release surfaces.**

---

## 2. Main Output Root Contract

The pipeline should keep one main output root. Inside that root it should create
two required child folders.

```text
OUTDIR/
├── release-tree/
└── support-tree/
```

The actual directory names must come from shared config or lib constants. The
names shown here are the plan-level working names.

### 2.1 `release-tree/`

`release-tree/` is the exact publishable product tree.

Rules:

1. It contains only release-ready files and folders.
2. It already uses the final public names locked in V4a.
3. It is the only subtree eligible for release-repo sync and ZIP packaging.
4. External publication targets must not rename or reinterpret its contents.

### 2.2 `support-tree/`

`support-tree/` contains everything that still matters to the pipeline but
does not belong in the public release tree.

Typical contents may include:

- raw extracted captures
- canonical semantic page records if the pipeline still needs them internally
- telemetry, manifests, and provenance helpers
- validator support files and maintainer-only machine outputs

Rules:

1. `support-tree/` is not a public contract.
2. `support-tree/` is never pushed to the release repository.
3. `support-tree/` may be kept as a CI artifact or local inspection surface.

---

## 3. Release Include Contract

The development repository should contain one version-controlled include path
that can add or override files in the release tree.

Working location:

```text
release-inputs/
└── release-include/
```

The final directory names must later come from shared config or lib constants.

### 3.1 Include behavior

The include is applied after the generator finishes writing `release-tree/`.

Merge order:

1. Generate `release-tree/` from pipeline-owned outputs.
2. Apply `release-inputs/release-include/` by path.
3. Validate the merged `release-tree/`.
4. Publish that validated merged tree to the release repository and ZIP.

### 3.2 Include rules

1. The include may add new files.
2. The include may replace generated files by exact relative path.
3. The include does not apply to `support-tree/`.
4. Target repositories are never the authoritative place for release-only hand
   edits.
5. The same merged `release-tree/` is used for both release-repo sync and ZIP
   packaging so those two surfaces cannot drift.

---

## 4. Naming And Path Constants

All public output names must be owned by shared config or lib constants rather
than repeated as string literals across scripts and workflow YAML.

### 4.1 Required constants

At minimum, the shared configuration surface should own constants for:

- the main output root
- the release-ready tree directory name
- the support-tree directory name
- the release-inputs directory name
- the release-include directory name
- `map.md`
- `bundled-reference.md`
- `chunked-reference/`
- root `llms.txt`
- root `llms-full.txt`
- module `llms.txt`
- optional `types/`

### 4.2 Current literals that must be retired from public assembly logic

The current pipeline still embeds public-shape literals that V4b should retire
or isolate behind shared configuration.

Examples already present in the codebase:

- `openwrt-condensed-docs`
- `L2-semantic`
- `*-complete-reference.md`
- `*-skeleton.md`
- workflow publish directory assumptions that point directly at one public tree

### 4.3 Configuration rule

`OUTDIR` may remain the environment variable that points to the main output
root, but it should no longer imply that the main output root itself is the
publishable release tree.

---

## 5. Stage Responsibilities After Refactor

The goal is to change late-stage assembly behavior without forcing a risky
rewrite of earlier extraction stages.

### 5.1 Early stages

Early extraction and normalization stages may remain structurally similar during
the first refactor pass.

They can continue to produce:

- raw extracted artifacts
- internal semantic or canonical page records
- support registries or manifests needed for validation and later assembly

These outputs belong under `support-tree/` once the dual-output-root model is
in place.

### 5.2 Release assembly stage

The late assembly stage becomes the owner of the public release tree.

Its responsibilities are:

1. Create the root release files.
2. Create each module folder.
3. Write module `llms.txt` files.
4. Write `map.md` for each module.
5. Write `bundled-reference.md` for each module.
6. Write each module's `chunked-reference/` topic files.
7. Copy optional typed helpers into `types/`.

### 5.3 Former `L2-semantic/` handling

The former public `L2-semantic/` tree is no longer a valid public output.

The stage rule is:

- if semantic page records still exist as a staging dependency, they live under
   `support-tree/`
- the public release tree receives that content redistributed into
  module-local `chunked-reference/`
- no stage may emit a top-level public `L2-semantic/` into `release-tree/`

### 5.4 Companion generation updates

Any stage that currently teaches or validates the old public surface must be
updated to the new contract.

That includes generators or validators for:

- root routing files
- module routing files
- product README and AGENTS guidance
- HTML browse pages
- release-shape validation

---

## 6. Publication Rules

### 6.1 Release repository sync

The release repository sync must source only from validated `release-tree/`
after include merge.

Rules:

1. Start from a clean checkout of the release repository.
2. Delete stale tracked and untracked content except `.git`.
3. Copy the validated merged `release-tree/` to repository root.
4. Commit and push only if content changed.

### 6.2 ZIP packaging

The ZIP must also source only from validated `release-tree/` after include
merge.

Rules:

1. Start from a clean temporary ZIP staging directory.
2. Copy the validated merged `release-tree/` into the ZIP staging root.
3. Build the dated ZIP from that staging directory.
4. Do not build the ZIP from a target-repository checkout.

### 6.3 Support-tree publication rule

`support-tree/` is not synced to the release repository and is not included in
the release ZIP.

If it is preserved externally at all, it should be preserved only as a CI or
debug artifact with clearly non-release semantics.

### 6.4 Future Pages rule

If a Pages mirror continues to exist or returns later, it should consume the
same validated `release-tree/` or a deliberately documented derivative of it.
It must not rebuild public names independently.

---

## 7. Validation And Acceptance Checks

The refactor is not complete until validators can prove the dual-output model
and the new public contract.

### 7.1 Release-tree checks

Validators should assert all of the following:

1. Root release files exist.
2. Each module has `llms.txt`, `map.md`, `bundled-reference.md`, and
   `chunked-reference/`.
3. `chunked-reference/` contains topic-shaped files rather than old public L2
   paths.
4. No top-level `L1-raw/` or `L2-semantic/` leaks into `release-tree/` unless a
   future plan explicitly reintroduces them.

### 7.2 Include checks

Validators should also prove:

1. the release include can add a file deterministically
2. the release include can replace a generated file deterministically
3. the merged `release-tree/` is the same tree used for both release-repo sync
   and ZIP packaging

### 7.3 Configuration checks

Tests should verify that the public naming contract is driven from shared
constants rather than duplicated literals across the codebase.

---

## 8. Recommended Implementation Sequence

The safest implementation order is:

1. Centralize public output names in config or lib constants.
2. Change the main output root to create `release-tree/` and `support-tree/`.
3. Move the current public assembly logic so it writes only into
   `release-tree/`.
4. Update late-stage generators and validators to emit `map.md`,
   `bundled-reference.md`, and `chunked-reference/`.
5. Add the release-include merge.
6. Switch release-repo sync and ZIP packaging to consume only the validated
   merged `release-tree/`.
7. Add tests that lock the new contract and prevent top-level `L2-semantic/`
   leakage.

### 8.1 Anti-pattern to avoid

Do not start by renaming public paths in target repositories while the pipeline
still emits the old contract internally. The refactor should first establish the
dual-output-root model and a late release assembly step, then switch the
publication surfaces to that assembled release tree.