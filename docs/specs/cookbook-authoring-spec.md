# Cookbook Authoring Specification

**Source:** extracted from `docs/plans/v13/03-v13-cookbook-content-spec-2026-03-22.md`

## Purpose

This document defines the durable authoring contract for the cookbook module. It covers what a cookbook page is, what evidence it requires, how it should link into the shipped corpus, and how maintainers should review it.

Use this specification for ongoing cookbook maintenance. Use the original V13 plan file only for historical topic prioritization and implementation rationale.

## Source And Publication Path

Cookbook source files are authored in:

```text
static/cookbook-source/
```

Pipeline lineage:

```text
static/cookbook-source/
  -> L1-raw/cookbook/
  -> L2-semantic/cookbook/
  -> release-tree/cookbook/
```

## Cookbook Vs Reference Boundary

Cookbook pages answer task-oriented questions. They are not a second copy of the generated reference corpus.

Every cookbook page must:

- explain a concrete task or decision instead of an entire API surface
- point to authoritative reference pages for complete API detail
- stay opinionated when the corpus shows a clear preferred OpenWrt path
- call out transitional or legacy cases explicitly instead of flattening them into universal rules
- avoid generic Linux advice unless the OpenWrt-specific constraint is also explained

If a topic cannot be written without inventing undocumented behavior, it is not ready for cookbook treatment.

## Required Page Structure

Each cookbook page must include these sections in this order:

1. Title
2. When-to-use callout
3. Overview
4. Complete Working Example
5. Step-by-Step Explanation
6. Anti-Patterns
7. Related Topics
8. Verification Notes

The when-to-use material should normally appear as a short callout directly below the
title. Do not add a separate `## When-to-use` section unless a specific page genuinely
needs a longer decision rubric. Avoid repeating the same routing language in frontmatter,
the callout, and the `Overview`.

For cookbook pages created through the v14 cookbook center, the first lines of the
`Overview` section must front-load the correction:

- `Correct pattern:` one sentence naming the OpenWrt-specific right answer
- `Wrong pattern:` one sentence naming the generic or hallucinated answer this page corrects

For retroactive backfills and staged remakes of already-live pages, the creating agent must
also compare the staged draft against the current live page and preserve any still-valid
strengths unless there is an explicit documented reason to drop them.

## Required Authored Frontmatter

Cookbook source files must include YAML frontmatter with these fields:

| Field | Required | Notes |
| --- | --- | --- |
| `title` | Yes | Human-readable topic title |
| `description` | Yes | One-sentence routing summary |
| `module` | Yes | Always `cookbook` |
| `origin_type` | Yes | Always `authored` |
| `when_to_use` | Yes | One-sentence scenario description |
| `related_modules` | Yes | List of related module names |
| `era_status` | Yes | `current`, `transitional`, or `legacy` |
| `verification_basis` | Yes | Summary of evidence basis |
| `reviewed_by` | Yes | Lifecycle value during drafting and final human maintainer accountable for the promoted page |
| `last_reviewed` | Yes | ISO 8601 date |

`topic_slug` is derived from the filename and is not authored manually.

`reviewed_by` lifecycle values:

- `draft` while the page is still in staged authoring
- `placeholder` when the page has been promoted but final accountable reviewer ownership is still unresolved
- `<reviewer-name>` once a human maintainer has accepted accountability for the promoted page

## Required Inputs Before Authoring

Before a new cookbook page or material page extension is authored, the creating
agent must consume all of the following inputs:

1. the admitted scenario packet that opened the work
2. the blind prompt or grouped prompt file used to test the boundary
3. the frozen answer key for that scenario or grouped batch
4. at least one raw blind-failure response from
  `docs/plans/v14/openwrt-cookbook/artifacts/results/<agent-id>/<run-id>/`
  when the page is being created as a remediation unit rather than a speculative note
5. the authority source files or URLs that define the correct OpenWrt behavior
6. the list of existing cookbook pages considered before deciding on a new page or
  extension

If item 4 does not exist yet, the work can remain admitted and source-backed, but it
is not authoring-ready for cookbook remediation.

The raw blind-failure response must come from a real blind agent run. If no archived failed
answer exists yet, the operator may create one by running the scenario against an unaware agent
that is not given local OpenWrt documentation context and does not proactively consult the repo's
documentation tree before answering.

## Staged Authoring Workflow

When a cookbook page is created through the v14 cookbook center, authoring should use
a staging workflow rather than writing straight into the live corpus:

1. write the working draft under
  `docs/plans/v14/openwrt-cookbook/artifacts/authoring/drafts/`
2. write a companion creation log under
  `docs/plans/v14/openwrt-cookbook/artifacts/authoring/logs/`
3. write a human review record under
  `docs/plans/v14/openwrt-cookbook/artifacts/authoring/reviews/`
4. run the v14 promotion and review gates
5. only then promote the settled content into `static/cookbook-source/`

The creation log must record which inputs were consumed, which failure patterns were
targeted, what was deliberately excluded, and why the final page shape was chosen.

The review record must capture the review decision, the exact issues found, and whether
the draft is accepted, revised in staging, or returned to evidence collection. Human
review procedure is defined in
`docs/plans/v14/openwrt-cookbook/10-human-review-procedure.md`.

## Metadata Mapping Contract

The cookbook ingest and normalization stages must preserve authored metadata:

- `02i` derives the slug from the filename.
- `02i` carries authored fields into the L1 sidecar.
- `03` carries the authored metadata forward into L2 where routing and validation consumers can use it.

## Cross-Link Contract

Cookbook pages are authored for the final shipped release-tree location.

Within a cookbook page:

- another cookbook topic uses `./other-topic.md`
- the cookbook index uses `../map.md` or `../bundled-reference.md`
- a reference page in another module uses `../../<module>/chunked-reference/<topic>.md`
  — these are authored for the `release-tree/cookbook/chunked-reference/` position and
  must not use a single `../` prefix. The assembly stage (`05a`) will pass them through
  unchanged. Do not use `../module/file.md` from cookbook chunked pages.
- a top-level shipped file such as root `llms.txt` uses `../../llms.txt`

Never invent a future path. If the path is not part of the current contract, add the contract first or avoid the link.

## Navigation Contract

`Related Topics` must not be a bare list of links. Each related link must include a one-line
decision hint that tells the reader or downstream agent when to follow it.

Preferred pattern:

```markdown
- [Topic Name](./topic-name.md) - use this when ...
```

This is part of the cookbook's routing surface, not optional decoration.

## Evidence Rules

### No ungrounded claims

Every factual claim must be traceable to at least one of:

- current corpus material
- current upstream OpenWrt repository code
- official OpenWrt wiki content
- an explicitly named external research packet when the topic requires it

### No fabricated URLs

Any upstream URL must resolve. If the exact commit is unavailable, link to the current branch rather than guessing an invalid path.

### Anti-patterns must be real

Anti-pattern examples should come from:

- observed AI failure modes
- documented upstream deprecated patterns
- real community confusion patterns

### Code examples must be verifiable

- ucode examples must use documented ucode APIs or shipped type declarations
- LuCI JavaScript examples must use documented LuCI APIs
- shell and UCI examples must rely on standard OpenWrt tooling
- Makefile examples must match the OpenWrt buildroot contract

## Verification Notes Minimum

Every cookbook page must record:

- exact corpus files and upstream files checked
- exact upstream URLs when available
- the human reviewer named in `reviewed_by`
- the `last_reviewed` date
- any known limitation, transitional caveat, or unresolved edge case

When the authority comes from source code, prefer a paired citation surface:

- the local corpus or pipeline path used during authoring
- the corresponding public upstream repository URL when one exists

Repo-local pipeline references are acceptable on their own only when there is no stable public
upstream source to link. When both surfaces exist, record both so future regeneration remains
auditable even if one surface moves.

For pages authored through the v14 staging flow, the promoted page should also be backed
by a draft, creation log, and review record that agree on the final page shape.

## Incumbent Reconciliation Contract

When a staged draft extends or remakes an already-live cookbook page, the creating agent must
explicitly review the incumbent page for still-valid strengths, including:

- useful anti-pattern examples not covered by the new draft
- better `Related Topics` routing hints
- clearer boundary explanations or caveats
- stronger working-example framing that remains source-backed

Each meaningful incumbent element removed by the new draft must be classified in the creation
log as one of:

- `preserved`
- `merged`
- `intentionally dropped`

`intentionally dropped` entries require a reason tied to scope, staleness, duplication, or
authority quality. Silent regression is not acceptable.

## AI Consumption And Token Budget Rules

Cookbook pages are written for both human maintainers and AI agents that may receive
only a narrow context window.

- Target roughly 700 to 1400 tokens for the whole page.
- Exceed 1600 tokens only when the working example or transitional caveats genuinely
  require it, and record the reason in the creation log.
- Put the corrective pattern before the long explanation.
- Prefer one complete working example over several partial examples.
- Keep the explanation focused on the observed failure boundary; link outward instead
  of turning the page into a full subsystem tutorial.

## Maintenance Policy

- Cookbook pages are maintained manually and are not regenerated by default.
- Re-review a page when upstream APIs it depends on materially change.
- Re-review a page when the era guide changes.
- Re-review a page when repeated AI failures show the page is stale or misleading.
- Prefer updating a page with explicit evidence over accumulating undocumented local lore.