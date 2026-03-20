# Release Tree Contract (V5a)

## Purpose

This document defines the published release-tree contract for the openwrt-docs4ai output product. It is the authoritative reference for the public output layout, replacing scattered descriptions across plan documents V1–V5a.

The release-tree is direct-root — no `openwrt-condensed-docs/` wrapper. Modules sit at root. This contract is derived from V5a (`docs/plans/v12/public-distribution-mirror-plan-2026-03-15-V5a.md`), specifically §3.1 resolution, §3.2, §3.4, §3.5, §7, §7.1, §8, and §9.

---

## Release Tree Layout

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

---

## Module Schema

Every module folder contains the following files:

| File / Directory | Role |
| --- | --- |
| `llms.txt` | Per-module LLM routing index. Lists the module's chunked topics and key references. |
| `map.md` | Navigation map (semantic skeleton). Provides a structured outline of the module with cross-links to chunked topics. |
| `bundled-reference.md` | Complete bundled reference for the module. For oversized modules, becomes a sharding index (see Oversized Module Sharding). |
| `chunked-reference/` | Directory of per-topic Markdown files derived from L2 semantic pages. Always present. |
| `chunked-reference/{topic}.md` | Individual topic file. One file per semantic page from the L2 layer. |
| `types/` | Optional. Present only for modules that export TypeScript IDE schemas. |
| `types/{module}.d.ts` | TypeScript declaration file for IDE schema support. |

---

## Oversized Module Sharding

When a module exceeds the token limit for a single file:

- `bundled-reference.md` remains the stable, fixed index filename.
- `bundled-reference.md` becomes an index document that points to `bundled-reference.part-{NN}.md` files.
- Part files sit alongside `bundled-reference.md` in the module root — not inside `chunked-reference/`.
- `chunked-reference/` topic files are always present regardless of sharding status.

Example layout for an oversized module:

```text
ucode/
├── bundled-reference.md          ← index, points to parts
├── bundled-reference.part-01.md
├── bundled-reference.part-02.md
├── chunked-reference/
│   └── ...
├── llms.txt
├── map.md
└── types/
    └── ucode.d.ts
```

---

## Guaranteed Absent Items

The following items must never appear anywhere in the published release-tree:

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

## Root Files

The release-tree root contains exactly these fixed files:

| File | Role |
| --- | --- |
| `README.md` | Human-readable introduction to the published corpus. |
| `AGENTS.md` | Agent navigation guide listing all modules and their entry points. |
| `llms.txt` | Root LLM routing index. Entry point for LLM-driven navigation across all modules. |
| `llms-full.txt` | Full expanded routing index with all topic links. |
| `index.html` | Web landing page served by the Pages site. |

---

## Support Tree

`support-tree/` is the internal pipeline staging area. It is ephemeral during CI runs and is not a persistent on-disk contract. Its internal layout may change without notice.

When present, it contains:

| Path | Contents |
| --- | --- |
| `support-tree/raw/` | L1-raw output (normalized source extracts and `.meta.json` sidecars). |
| `support-tree/semantic-pages/` | L2-semantic output (enriched Markdown with YAML frontmatter). |
| `support-tree/telemetry/` | `changelog.json`, `CHANGES.md`, `signature-inventory.json`. |
| `support-tree/manifests/` | `cross-link-registry.json`, `repo-manifest.json`. |

`support-tree/` may be uploaded as a CI artifact for debugging. It is never published to any public surface.

---

## Delivery Surfaces

All three delivery surfaces share the same validated release-tree as their content source. Target-specific overlays are applied after validation, before publish.

| Surface | Root URL / Path | Content source |
| --- | --- | --- |
| Pages site | `https://openwrt-docs4ai.github.io/` | Validated release-tree + `pages-include/` overlay |
| Release repo | `https://github.com/openwrt-docs4ai/corpus` | Validated release-tree + `release-repo-include/` overlay |
| ZIP download | `openwrt-docs4ai-YYYY-MM-DD.zip` → `openwrt-docs4ai/` | Validated release-tree (no target-specific overlays) |

---

## Gatekeeper Rules

All six checks must pass before any cross-repo publish. Failure of any check blocks publish and fails the job visibly.

| Check | Assertion |
| --- | --- |
| Root router exists | `release-tree/llms.txt` exists and is > 512 bytes |
| Root index exists | `release-tree/index.html` exists |
| Module count | At least 4 module directories exist |
| No legacy leakage | No `L1-raw/`, `L2-semantic/`, or `openwrt-condensed-docs` anywhere in `release-tree/` |
| Fixed schema | Every module directory has `llms.txt`, `map.md`, `bundled-reference.md`, `chunked-reference/` |
| Chunked non-empty | Every module's `chunked-reference/` has at least one `.md` file |

---

## Release Include Overlays

Source-controlled overlay directories are merged into the release-tree after generation, before validation.

```text
release-inputs/
├── release-include/          (common overlay, applied to all surfaces)
├── pages-include/            (Pages-only overlay, e.g. .nojekyll)
└── release-repo-include/    (release-repo-only overlay, reserved)
```

- `release-inputs/release-include/` contents are applied to all delivery surfaces.
- `release-inputs/pages-include/` contents are applied only to the Pages surface (e.g. `.nojekyll`).
- `release-inputs/release-repo-include/` is reserved for future use.
- Include files take precedence over generated files of the same name.

---

## Name Mapping From Old Contract

Quick reference for names that changed between the pre-V5a contract and the V5a contract:

| Old name | New name |
| --- | --- |
| `{module}-skeleton.md` | `map.md` |
| `{module}-complete-reference.md` | `bundled-reference.md` |
| `{module}-complete-reference.part-{NN}.md` | `bundled-reference.part-{NN}.md` |
| `L2-semantic/{module}/` | `{module}/chunked-reference/` |
| `openwrt-condensed-docs/` | `release-tree/` (internal pipeline) / direct-root (public) |
| `# {module} Complete Reference` (H1) | `# {module} Bundled Reference` |
| `# {module} (Skeleton Semantic Map)` (H1) | `# {module} Navigation Map` |

---

## Relationship to Other Documents

- **Source:** This document is derived from V5a (`docs/plans/v12/public-distribution-mirror-plan-2026-03-15-V5a.md`). For implementation phasing and rollback gates, see V5a §5.
- **Pre-V5a contract:** For the current pre-V5a schema in active use, see [`schema-definitions.md`](schema-definitions.md). That document will be updated as implementation phases complete.
- **Rework map:** For the per-file change map (exact strings, line ranges, affected scripts), see V5a §4.
- **Stage dependency:** For pipeline execution order, see [`execution-map.md`](execution-map.md).
