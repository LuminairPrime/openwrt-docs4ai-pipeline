# Public Distribution Product & Delivery Plan (V5a)

Recorded: 2026-03-15

Status: Consolidated implementation-ready specification

Scope: Unify the product-output naming and layout contract (V4a), the delivery
mechanics (V4b), and the publication architecture (V3) into one actionable
document with phased implementation, explicit rollback gates, and a complete
rework map of every file that must change.

---

## 1. Why V5a Exists

V3, V4a, and V4b each advanced the plan, but they left three problems
unresolved:

1. **Contradictory public-tree models.** V3 still published the corpus inside
   an `openwrt-condensed-docs/` wrapper with a separate "distribution shell"
   above it. V4a eliminated wrappers and moved to a direct-root `release-tree/`
   where modules sit at root. The two specs describe different public trees and
   different URL contracts. V5a resolves this: the V4a direct-root model wins.

2. **No per-file rework map.** V4a listed categories of scripts that "clearly
   need updates" but did not map the exact old-contract strings inside each
   file, the exact replacement strings, or the order of safe changes. Without
   that map, a developer must survey the whole codebase before writing a single
   line. V5a provides the map.

3. **No rollback-safe phase gates.** V4b described a recommended sequence but
   did not define what condition must be true before advancing to the next
   phase, or what happens if one phase fails. V5a adds explicit go/no-go
   checkpoints so that a failed phase leaves the pipeline in a known-good
   state.

---

## 2. Consolidated Locked Decisions

These decisions are final. They supersede any conflicting statement in V1
through V4b.

| # | Decision | Source |
| --- | --- | --- |
| D1 | The public release tree is direct-root. No `openwrt-condensed-docs/` wrapper in any public surface. | V4a §9, supersedes V2/V3 |
| D2 | Every public module folder uses `llms.txt`, `map.md`, `bundled-reference.md`, `chunked-reference/`, and optional `types/`. | V4a §7.5 |
| D3 | Module names are not repeated in child filenames inside the module folder. | V4a §13 |
| D4 | The pipeline main output root contains `release-tree/` and `support-tree/`. Only `release-tree/` is publishable. | V4a §9 + V4b §2 |
| D5 | `release-inputs/release-include/` adds or overrides files after generation, before validation. | V4a §10 + V4b §3 |
| D6 | The former top-level public `L2-semantic/` is replaced by per-module `chunked-reference/`. | V4a §9.3 |
| D7 | All public output names come from shared config or lib constants, not scattered string literals. | V4a §6 goal 9, V4b §4 |
| D8 | The GitHub organization is `openwrt-docs4ai`. Two target repos: `openwrt-docs4ai.github.io` (Pages) and `corpus` (Releases). | V3 §3, §5 |
| D9 | The ZIP expands into `openwrt-docs4ai/` (project-named, not `corpus/`). | V3 §7 |
| D10 | Authentication uses a GitHub App with installation tokens, not long-lived PATs. | V2 §6, V3 §14 |
| D11 | Git history on target repos is append-only. No force-push. | V2 §9.2 |
| D12 | Same-day reruns update the existing release and replace the dated ZIP asset. | V2 §9.3, V3 §15.2 |
| D13 | Existing source-repo deploy behavior must remain intact even if new distribution steps fail. | REVIEW §2.D, V2 §9.4 |
| D14 | The `openwrt-condensed-docs` name is internal to the source repo only; it must never appear in any public path, URL, or visible label. | V3 §4.1, V4a §7.8 |

---

## 3. Resolved Conflicts

### 3.1 V3 wrapper vs V4a direct-root

V3 §6 defined a public tree with `L1-raw/`, `L2-semantic/`, `CHANGES.md`,
`changelog.json`, `cross-link-registry.json`, `repo-manifest.json`, and
`signature-inventory.json` at product root.

V4a §2, §9 eliminated all of those from the public tree.

**Resolution:** V4a wins. The public release tree contains only:

```text
release-tree/
├── README.md
├── AGENTS.md
├── llms.txt
├── llms-full.txt
├── index.html
├── {module}/
│   ├── llms.txt
│   ├── map.md
│   ├── bundled-reference.md
│   ├── chunked-reference/
│   │   └── {topic}.md ...
│   └── types/ (optional)
│       └── {module}.d.ts
└── ... (more modules)
```

The items V3 listed at root that V4a removed are relocated:

| V3 root item | V5a location |
| --- | --- |
| `L1-raw/` | `support-tree/raw/` |
| `L2-semantic/` | redistributed into `{module}/chunked-reference/` |
| `CHANGES.md` | `support-tree/telemetry/CHANGES.md` |
| `changelog.json` | `support-tree/telemetry/changelog.json` |
| `cross-link-registry.json` | `support-tree/manifests/cross-link-registry.json` |
| `repo-manifest.json` | `support-tree/manifests/repo-manifest.json` |
| `signature-inventory.json` | `support-tree/telemetry/signature-inventory.json` |

### 3.2 V3 delivery-root overlays vs V4a release-include

V3 §8 defined `delivery-root/common/`, `delivery-root/pages/`, and
`delivery-root/release/` as source-controlled overlay directories.

V4a §10 defined `release-inputs/release-include/` as the single overlay point.

**Resolution:** Merge both. Use one overlay parent directory with
target-specific children:

```text
release-inputs/
├── release-include/          (common overlay, applied to all surfaces)
├── pages-include/            (Pages-only overlay, e.g. .nojekyll)
└── release-repo-include/    (release-repo-only overlay, if ever needed)
```

This preserves the V3 concern about target-specific files (`.nojekyll` for
Pages) while keeping the V4a single-overlay concept.

### 3.3 Module-local README.md

V4a §14 question 1 asked whether module-local `README.md` should be in the
first fixed-schema contract.

**Resolution:** Not in the first pass. The `llms.txt` + `map.md` routing pair
is sufficient. A module `README.md` can be added later if proven necessary.

### 3.4 Oversized module strategy

V4a §14 question 4 asked how `bundled-reference.md` handles oversized modules.

**Resolution:** For the first pass, keep the existing sharding behavior:

- `bundled-reference.md` remains the stable index filename.
- If a module exceeds the token limit, `bundled-reference.md` becomes an index
  that points to `bundled-reference.part-{NN}.md` files.
- `chunked-reference/` topic files are always present regardless of sharding.
- The sharded parts sit alongside `bundled-reference.md`, not inside
  `chunked-reference/`.

### 3.5 Support-tree persistence

V4a §14 question 2 asked whether `support-tree/` stays persistent.

**Resolution:** `support-tree/` is ephemeral during CI runs and may be uploaded
as a CI artifact for debugging. It is not a persistent on-disk contract. Its
internal layout may change without notice.

---

## 4. Complete Rework Map

This section maps every file in the current codebase that contains
old-contract names, the exact strings that must change, and what they become.

### 4.1 Shared configuration — `lib/config.py`

Current state: defines `OUTDIR`, `L1_RAW_WORKDIR`, `L2_SEMANTIC_WORKDIR`, and
`REPO_MANIFEST_PATH`. All paths are relative to `OUTDIR` which defaults to
`openwrt-condensed-docs`.

Required changes:

| Current | New | Notes |
| --- | --- | --- |
| `OUTDIR` defaults to `openwrt-condensed-docs` | `OUTDIR` becomes the main output root (formerly "working output" only) | Internal stages still write here |
| - | Add `RELEASE_TREE_DIR` = `OUTDIR / release-tree` | New constant |
| - | Add `SUPPORT_TREE_DIR` = `OUTDIR / support-tree` | New constant |
| - | Add `RELEASE_INCLUDE_DIR` = `release-inputs/release-include` | New constant, relative to repo root |
| - | Add public-name constants: `MODULE_MAP_FILENAME`, `MODULE_BUNDLED_REF_FILENAME`, `MODULE_CHUNKED_REF_DIRNAME`, `MODULE_TYPES_DIRNAME` | Central ownership of `map.md`, `bundled-reference.md`, `chunked-reference`, `types` |
| `L1_RAW_WORKDIR` = `OUTDIR/L1-raw` | Keep as working path, but under `SUPPORT_TREE_DIR/raw` in release assembly | Internal stages untouched |
| `L2_SEMANTIC_WORKDIR` = `OUTDIR/L2-semantic` | Keep as working path, but under `SUPPORT_TREE_DIR/semantic-pages` in release assembly | Internal stages untouched |

**Risk reduction:** Do NOT change `OUTDIR` semantics for early stages. Early
stages continue to write `L1-raw/` and `L2-semantic/` under the existing
`OUTDIR`. Only the late assembly stage reads from those locations and writes
into `release-tree/`.

### 4.2 Assembly stage — `05a-assemble-references.py`

Current hard-coded strings and their required changes:

| Line range | Current string | Required change |
| --- | --- | --- |
| Line 6-8 (docstring) | `OUTDIR/{module}/{module}-complete-reference.md`, `{module}-skeleton.md` | Update docstring to new names |
| Line 36 | `L2_DIR = os.path.join(OUTDIR, "L2-semantic")` | Keep for reading; assembly output paths change |
| Line 157 | `f"{module}-complete-reference.part-{index:02d}.md"` | `f"bundled-reference.part-{index:02d}.md"` |
| Line 330 | `f"{module}-complete-reference.md"` | `"bundled-reference.md"` (from config constant) |
| Line 331 | `f"{module}-skeleton.md"` | `"map.md"` (from config constant) |
| Line 327 | `out_mod_dir = os.path.join(OUTDIR, module)` | `os.path.join(RELEASE_TREE_DIR, module)` |
| Line 202 | `f"# {module} Complete Reference"` | `f"# {module} Bundled Reference"` |
| Line 293 | `f"# {module} (Skeleton Semantic Map)"` | `f"# {module} Navigation Map"` |

**New responsibility:** Script `05a` must also write `chunked-reference/`
topic files. Currently, L2 semantic pages exist under `OUTDIR/L2-semantic/
{module}/` but are not explicitly copied into a module-local page folder. The
assembly stage must:

1. Write `bundled-reference.md` (renamed from `{module}-complete-reference.md`)
2. Write `map.md` (renamed from `{module}-skeleton.md`)
3. Copy or link each L2 topic page into `{module}/chunked-reference/{topic}.md`

This is the most significant new code in the rework.

### 4.3 Companion generators — `05b-generate-agents-and-readme.py`

Current state: generates `AGENTS.md` and `README.md` with references to
old paths.

Required changes:

| Current reference | Required change |
| --- | --- |
| `{module}-skeleton.md` | `map.md` |
| `{module}-complete-reference.md` | `bundled-reference.md` |
| `L2-semantic/` | `chunked-reference/` (or remove if not mentioned) |
| `./openwrt-condensed-docs/` | remove from all visible text |

Output location changes from `OUTDIR/` to `RELEASE_TREE_DIR/`.

### 4.4 Routing index generator — `06-generate-llm-routing-indexes.py`

Current state: generates root `llms.txt`, `llms-full.txt`, and per-module
`llms.txt` files with hard-coded references to old names.

Required changes:

| Current reference | Required change |
| --- | --- |
| `{module}-skeleton.md` | `map.md` |
| `{module}-complete-reference.md` | `bundled-reference.md` |
| `L2-semantic/{module}/{topic}.md` references in module `llms.txt` | `chunked-reference/{topic}.md` |
| `L2-semantic/` references in `llms-full.txt` | `{module}/chunked-reference/{topic}.md` |

Output location changes from `OUTDIR/` to `RELEASE_TREE_DIR/`.

### 4.5 Web index generator — `07-generate-web-index.py`

Current state: generates `index.html` with hard-coded `openwrt-condensed-docs`
path prefixes and old filenames in visible labels.

Required changes:

| Current reference | Required change |
| --- | --- |
| `./openwrt-condensed-docs/` prefix in visible paths | Direct-root `./` prefix |
| `L2-semantic/` labels and links | `{module}/chunked-reference/` |
| `{module}-skeleton.md` labels | `map.md` |
| `{module}-complete-reference.md` labels | `bundled-reference.md` |
| Title referencing `openwrt-condensed-docs publish tree` | Update to product name |

Output location changes to `RELEASE_TREE_DIR/`.

### 4.6 Validator — `08-validate-output.py`

Current state: validates old names and paths.

Required changes:

| Current validation | Required change |
| --- | --- |
| Checks for `L2-semantic/` existence | Check for `chunked-reference/` inside each module |
| Checks for `{module}-skeleton.md` | Check for `map.md` |
| Checks for `{module}-complete-reference.md` | Check for `bundled-reference.md` |
| Checks for `openwrt-condensed-docs/` root paths in HTML | Check for direct-root paths |
| - | Add: reject `L1-raw/`, `L2-semantic/` in `release-tree/` |
| - | Add: reject `openwrt-condensed-docs` in any visible text |
| - | Add: validate `release-tree/` vs `support-tree/` separation |
| - | Add: validate release-include merge integrity |

### 4.7 Test support — `tests/support/smoke_pipeline_support.py`

Current hard-coded assertions that must change:

| Line | Current assertion | Required change |
| --- | --- | --- |
| 248 | `L2-semantic/wiki/wiki_page-service-events.md` | Path under `wiki/chunked-reference/` |
| 261 | `ucode/ucode-complete-reference.md` | `ucode/bundled-reference.md` |
| 262 | `ucode/ucode-skeleton.md` | `ucode/map.md` |
| 273 | `L2-semantic/procd/c_source-init-service.md` | `procd/chunked-reference/c_source-init-service.md` |
| 277 | `L2-semantic/wiki/wiki_page-service-events.md` | `wiki/chunked-reference/wiki_page-service-events.md` |
| 281 | `ucode-complete-reference.md` | `bundled-reference.md` |
| 306-309 | `./ucode-skeleton.md`, `./ucode-complete-reference.md`, `../L2-semantic/ucode/` | `./map.md`, `./bundled-reference.md`, `./chunked-reference/` |
| 321 | `./L2-semantic/ucode/c_source-api-fs.md` | `./ucode/chunked-reference/c_source-api-fs.md` |
| 339-344 | `./openwrt-condensed-docs/` prefixed paths | Direct-root `./` paths |

### 4.8 Pytest contract tests — `tests/pytest/pytest_02_fixture_pipeline_contract_test.py`

Any assertions referring to old names must be updated to match the new
contract. The exact changes mirror those in §4.7.

### 4.9 Pytest warning regression tests — `tests/pytest/pytest_06_warning_regression_test.py`

Any paths referencing `L2-semantic/`, `*-skeleton.md`, or
`*-complete-reference.md` must be updated.

### 4.10 Workflow — `.github/workflows/openwrt-docs4ai-00-pipeline.yml`

Required new workflow steps (added after existing deploy steps):

1. Create dual output root (`release-tree/` + `support-tree/`)
2. Run late assembly into `release-tree/`
3. Apply `release-inputs/release-include/`
4. Apply `release-inputs/pages-include/` (for Pages target)
5. Run gatekeeper validation on merged `release-tree/`
6. Mint GitHub App installation token
7. Push to `openwrt-docs4ai.github.io`
8. Push to `corpus`
9. Create/update dated release and ZIP on `corpus`

Existing steps 1–5 (source-repo promotion, `gh-pages` mirror) remain unchanged
per D13.

### 4.11 Files not requiring changes

These early-stage scripts do not need public-contract changes:

- `01-clone-repos.py` — clones upstream, no public names
- `02a` through `02h` — extractors write to `WORKDIR/L1-raw/`, internal only
- `03-normalize-semantic.py` — writes to `WORKDIR/L2-semantic/`, internal only
- `04-generate-ai-summaries.py` — enriches L2 frontmatter, no public names

These scripts write into the existing `WORKDIR` which becomes part of
`support-tree/`. They do not need renaming because their output paths are
never public.

---

## 5. Phased Implementation With Rollback Gates

Each phase has a go/no-go gate. If the gate fails, the previous phase's
state is the safe rollback point. The pipeline continues to produce the
current old-contract output until the phase that switches public output
is explicitly activated.

### Phase 0: Add shared configuration constants

**Goal:** Centralize all public output names in `lib/config.py`.

**Changes:**
- Add constants for `RELEASE_TREE_DIR`, `SUPPORT_TREE_DIR`,
  `MODULE_MAP_FILENAME`, `MODULE_BUNDLED_REF_FILENAME`,
  `MODULE_CHUNKED_REF_DIRNAME`, `MODULE_TYPES_DIRNAME`,
  `RELEASE_INCLUDE_DIR`, `PAGES_INCLUDE_DIR`

**Gate:** All existing tests pass with no behavioral change. The new constants
are defined but not yet consumed by any stage.

**Rollback:** Revert the `lib/config.py` additions. Zero risk.

---

### Phase 1: Add release assembly stage (dual output, feature-flagged)

**Goal:** Create a new late-stage script `05e-assemble-release-tree.py` that
reads from the existing pipeline output and writes the V5a `release-tree/`.

**Changes:**
- New script `05e-assemble-release-tree.py`:
  - Creates `RELEASE_TREE_DIR`
  - Creates `SUPPORT_TREE_DIR`
  - For each module:
    - Copies/renames `{module}-complete-reference.md` → `bundled-reference.md`
    - Copies/renames `{module}-skeleton.md` → `map.md`
    - Copies L2 topic pages into `chunked-reference/`
    - Copies optional `types/` files
    - Generates module `llms.txt` with new paths
  - Copies root files (`llms.txt`, `llms-full.txt`, `README.md`, `AGENTS.md`,
    `index.html`) with path rewrites
  - Moves support-only artifacts to `support-tree/`
- Feature flag: `ENABLE_RELEASE_TREE` env var (default `false`)
- When flag is off, existing stages still produce old-contract output

**Why a new script instead of modifying 05a:** This is the single most
important risk-reduction decision. Script `05a` currently works. Inserting
rename logic into it creates a change where a bug can break the existing
pipeline. A new script that runs after `05a` and reads its output means:

- `05a` continues to produce known-good old-contract files
- `05e` produces the new contract files alongside them
- Both can be validated before any consumer switches
- If `05e` is broken, deleting it restores the old pipeline

**Gate:** When `ENABLE_RELEASE_TREE=true`:
- `release-tree/` contains the full V5a layout
- `support-tree/` contains L1, L2, telemetry, and manifests
- All old-contract output still exists unchanged under `OUTDIR/`
- All existing tests pass (they still check `OUTDIR/`)
- A new parallel test suite validates `release-tree/`

**Rollback:** Set `ENABLE_RELEASE_TREE=false`. The script is skipped. Old
output is unchanged.

---

### Phase 2: Add release-tree validation

**Goal:** Create new tests and a validator that assert the V5a contract on
`release-tree/`.

**Changes:**
- New test file:
  `tests/pytest/pytest_09_release_tree_contract_test.py`
  - Asserts every module has `llms.txt`, `map.md`, `bundled-reference.md`,
    `chunked-reference/`
  - Asserts no `L1-raw/`, `L2-semantic/`, `openwrt-condensed-docs` anywhere
    in `release-tree/`
  - Asserts bundled-vs-chunked parity for at least one module
  - Asserts `release-tree/` contains no `support-tree/` items
- Extend `08-validate-output.py` with a `release-tree` validation mode
  (behind feature flag)

**Gate:** All new tests pass against the `release-tree/` produced by Phase 1.
All existing tests still pass against old `OUTDIR/` output.

**Rollback:** Delete the new test file and validation mode. Zero risk.

---

### Phase 3: Add release-include merge

**Goal:** Implement the overlay merge from `release-inputs/release-include/`.

**Changes:**
- Create `release-inputs/release-include/` in the source repo (initially
  empty or with a `README.md` explaining its purpose)
- Create `release-inputs/pages-include/.nojekyll`
- Create `release-inputs/release-repo-include/` (empty, reserved)
- Add merge logic to `05e-assemble-release-tree.py`:
  after generating `release-tree/`, copy `release-include/` contents on top
- Add merge-precedence test

**Gate:** Include merge produces expected results. A test file placed in
`release-include/` appears in the merged `release-tree/`. A generated file
replaced by an include-override contains the override content. Existing tests
pass.

**Rollback:** Remove the merge logic from `05e`. The `release-include/`
directory stays inert.

---

### Phase 4: Switch late stages to write into release-tree

**Goal:** Modify scripts `05a`, `05b`, `06`, `07`, `08` to consume
`RELEASE_TREE_DIR` when the feature flag is on.

**Changes:**
- `05a`: output paths use config constants; filenames use new names
- `05b`: text references updated; output to `RELEASE_TREE_DIR`
- `06`: routing text references updated; output to `RELEASE_TREE_DIR`
- `07`: path labels and links updated; output to `RELEASE_TREE_DIR`
- `08`: validation logic updated per §4.6
- Script `05e` is retired (its functionality is absorbed into the modified
  stages)

This is the riskiest phase because it modifies working scripts.

**Risk mitigation:**
- Feature flag controls whether stages write to old or new paths
- A full smoke test run with `ENABLE_RELEASE_TREE=false` proves old contract
  is intact
- A full smoke test run with `ENABLE_RELEASE_TREE=true` proves new contract
  works
- Only after both pass green does the flag default change

**Gate:** Full smoke tests pass in both flag states. The `release-tree/`
output matches what Phase 1's `05e` produced. The old `OUTDIR/` output matches
what the pipeline produced before Phase 4.

**Rollback:** Reset feature flag to `false`. All stages revert to old output
paths.

---

### Phase 5: Update test suite to new contract

**Goal:** Modify `smoke_pipeline_support.py`, `pytest_02`, and `pytest_06`
to assert the new contract as the primary contract.

**Changes:**
- Update all assertions per §4.7, §4.8, §4.9
- Old-contract assertions are removed
- Feature flag default changes to `true`

**Gate:** Full test suite passes with the new contract as primary. Manual
inspection of `release-tree/` output confirms correctness.

**Rollback:** Restore old assertions and set flag to `false`.

---

### Phase 6: Provision public infrastructure and deploy

**Goal:** Set up the external GitHub organization, repos, and deploy workflow.

**Changes:**
1. Create `openwrt-docs4ai` GitHub organization
2. Create `openwrt-docs4ai.github.io` repo (Pages)
3. Create `corpus` repo (Releases)
4. Create and install GitHub App
5. Store secrets in source repo
6. Add deploy workflow steps per §4.10
7. First live publish

**Gate:** Live Pages site serves direct-root content. Release repo has a
fresh commit. ZIP expands into `openwrt-docs4ai/` with the V5a layout.
No `openwrt-condensed-docs`, `L1-raw`, or `L2-semantic` visible anywhere.

**Rollback:** Disable the new workflow steps. Source-repo deploy continues
unchanged.

---

### Phase 7: Remove old contract and feature flag

**Goal:** Clean up the codebase after live validation.

**Changes:**
- Remove `ENABLE_RELEASE_TREE` feature flag
- Remove old-contract code paths
- Retire script `05e` if not already retired in Phase 4
- Update `DEVELOPMENT.md` and architecture docs

**Gate:** Full test suite, CI pipeline, and live deploy all green without the
old contract code paths.

**Rollback:** Restore the feature flag and old paths. This is the only phase
with a moderate rollback cost, which is why it is last.

---

## 6. Rework Summary By Risk Level

| Risk | Phase | Files affected | What can go wrong | Mitigation |
| --- | --- | --- | --- | --- |
| **None** | 0 | `lib/config.py` | Nothing; additive only | Constants unused until Phase 1 |
| **Low** | 1 | New `05e` script | New script bugs produce bad `release-tree/` | Does not touch existing output; feature-flagged off |
| **Low** | 2 | New test file, `08` extension | Bad test logic gives false confidence | Tests run against Phase 1 output; manual cross-check |
| **Low** | 3 | `release-inputs/`, `05e` merge logic | Include merge overwrites wrong file | Merge is additive; test asserts exact behavior |
| **High** | 4 | `05a`, `05b`, `06`, `07`, `08` | Bug in modified script breaks existing pipeline | Feature flag; dual smoke test; rollback to flag=false |
| **Medium** | 5 | Test support, pytest files | Wrong assertions pass bad output | Diff old vs new assertions for parity |
| **Medium** | 6 | Workflow YAML, external infra | Deploy fails or publishes wrong tree | Deploy is additive after existing deploy; gatekeeper checks |
| **Low** | 7 | Cleanup only | Premature removal of fallback | Only after live validation |

---

## 7. Final Release Tree Contract

When all phases are complete, the published product tree looks like this:

```text
(repository root or ZIP root openwrt-docs4ai/)
├── README.md
├── AGENTS.md
├── llms.txt
├── llms-full.txt
├── index.html
├── luci/
│   ├── llms.txt
│   ├── map.md
│   ├── bundled-reference.md
│   └── chunked-reference/
│       ├── javascript-api-cbi.md
│       └── ...
├── luci-examples/
│   ├── llms.txt
│   ├── map.md
│   ├── bundled-reference.md
│   └── chunked-reference/
│       └── ...
├── openwrt-core/
│   └── ...
├── openwrt-hotplug/
│   └── ...
├── procd/
│   └── ...
├── uci/
│   └── ...
├── ucode/
│   ├── llms.txt
│   ├── map.md
│   ├── bundled-reference.md
│   ├── chunked-reference/
│   │   └── ...
│   └── types/
│       └── ucode.d.ts
└── wiki/
    └── ...
```

### 7.1 Items guaranteed absent from the public tree

- `L1-raw/`
- `L2-semantic/`
- `openwrt-condensed-docs/`
- `corpus/`
- `*-skeleton.md`
- `*-complete-reference.md`
- `cross-link-registry.json`
- `repo-manifest.json`
- `signature-inventory.json`
- `changelog.json`
- `CHANGES.md`
- Any `.meta.json` sidecar

---

## 8. Delivery Surfaces

| Surface | Root | Source |
| --- | --- | --- |
| Pages site | `https://openwrt-docs4ai.github.io/` | Validated `release-tree/` + `pages-include/` |
| Release repo | `https://github.com/openwrt-docs4ai/corpus` | Validated `release-tree/` + `release-repo-include/` |
| ZIP download | `openwrt-docs4ai-YYYY-MM-DD.zip` → `openwrt-docs4ai/` | Validated `release-tree/` (no target-specific overlays) |

All three surfaces share the same validated `release-tree/` as their content
source. Target-specific overlays (`.nojekyll` for Pages) are applied after.

---

## 9. Gatekeeper Rules

Before any cross-repo publish, the pipeline must assert:

| Check | Assertion |
| --- | --- |
| Root router exists | `release-tree/llms.txt` exists and is > 512 bytes |
| Root index exists | `release-tree/index.html` exists |
| Module count | At least 4 module directories exist |
| No legacy leakage | No `L1-raw/`, `L2-semantic/`, `openwrt-condensed-docs` anywhere in `release-tree/` |
| Fixed schema | Every module dir has `llms.txt`, `map.md`, `bundled-reference.md`, `chunked-reference/` |
| Chunked non-empty | Every module's `chunked-reference/` has at least one `.md` file |

Failure of any check blocks publish and fails the job visibly.

---

## 10. Document Supersession

| Document | Status after V5a |
| --- | --- |
| V1 (`public-distribution-mirror-plan-2026-03-14.md`) | Historical; fully superseded |
| REVIEW (`-REVIEW.md`) | Historical; all concerns addressed |
| V2 (`-V2.md`) | Historical; auth and deploy details carried forward |
| V3 (`-V3.md`) | Partially superseded; delivery architecture preserved, public tree changed |
| V4a (`-V4a.md`) | Incorporated; naming contract locked |
| V4b (`-V4b.md`) | Incorporated; mechanics absorbed |
| **V5a (this document)** | **Active; implementation-ready specification** |

---

## 11. Open Questions (Non-Blocking)

These do not block implementation but should be revisited after Phase 5:

1. Should the root `llms.txt` carry an explicit "router" title line as
   suggested in V4a §8?
2. Should `release-inputs/pages-include/` support a Pages-specific
   `index.html` override for the site landing page?
3. What is the long-term telemetry and changelog strategy for the public tree
   once the support files are excluded?
