# Cookbook Authoring Execution Contract

**Purpose:** Define how a trusted local agent should turn an admitted scenario into a staged cookbook draft, a reviewable creation log, and finally a promoted page in the live cookbook corpus.

**Authority:** This contract extends [../../../specs/cookbook-authoring-spec.md](../../../specs/cookbook-authoring-spec.md).

---

## 1. Why This Contract Exists

The cookbook center already defined:

- how blind failures are discovered
- how failures are grouped into families
- how a family is promoted into cookbook work
- where settled cookbook pages live

This document defines the middle step that was previously only implicit: how the creating agent must work when authoring the cookbook itself.

---

## 2. Required Inputs Before A Draft Can Start

The creating agent must not start a draft until it has read all of the following:

1. the admitted scenario packet
2. the blind prompt or grouped prompt file used for the test
3. the frozen answer key for that scenario or grouped batch
4. at least one archived raw blind-failure response from
  `artifacts/results/<agent-label>/<run-label>/` for the scenario when the work is remediation-driven
5. the authority source files or URLs that define the correct OpenWrt behavior
6. the existing cookbook pages reviewed during the packet coverage check

### 2.1 Hard rule for remediation work

If the page is being authored because an AI actually failed the task, a raw failure response is mandatory input. Without it, the lesson stays admitted and source-backed, but it is not yet authoring-ready.

If no archived failed answer exists yet, the operator may generate one by running the scenario
against an unaware agent that is not given OpenWrt repository documentation context. That run is
an evidence-gathering step, not a shortcut around the failure-first rule.

---

## 3. Workflow States

```text
admitted packet
  -> authoring-ready
  -> draft written under artifacts/authoring/drafts/
  -> creation log written under artifacts/authoring/logs/
  -> review record written under artifacts/authoring/reviews/
  -> human review and promotion checklist
  -> promoted page under static/cookbook-source/
```

If the draft fails review, it stays in the drafts area and is revised there. The live cookbook corpus is only the promotion target.

---

## 4. Filesystem Contract

### 4.1 Draft location

```text
docs/plans/v14/openwrt-cookbook/artifacts/authoring/drafts/
```

Naming rule:

```text
<cookbook-slug>-draft.md
```

Example:

```text
artifacts/authoring/drafts/ucode-async-process-pattern-draft.md
```

### 4.2 Creation log location

```text
docs/plans/v14/openwrt-cookbook/artifacts/authoring/logs/
```

Naming rule:

```text
<cookbook-slug>-creation-log.md
```

Example:

```text
artifacts/authoring/logs/ucode-async-process-pattern-creation-log.md
```

### 4.3 Promotion target

```text
static/cookbook-source/
```

The draft directory is the working area. `static/cookbook-source/` is the settled authored corpus.

### 4.4 Review record location

```text
docs/plans/v14/openwrt-cookbook/artifacts/authoring/reviews/
```

Naming rule:

```text
<cookbook-slug>-review-record.md
```

Example:

```text
artifacts/authoring/reviews/ucode-native-file-io-and-json-review-record.md
```

---

## 5. Creating-Agent Responsibilities

The creating agent must:

1. identify the 1 to 3 primary wrong patterns shown by the archived failure responses
2. translate those into one bounded corrective lesson
3. verify that the lesson is sourced from current OpenWrt authority rather than generic Linux intuition
4. keep the page scoped to the failure boundary instead of expanding into a full subsystem tutorial
5. compare the staged draft against the current live page when the work is an extension or retroactive backfill
6. preserve still-valid incumbent strengths unless there is a documented reason to drop them
7. record the decisions in the creation log before promotion

The creating agent must not write a generic tutorial that ignores the actual blind failure shape.
It must also leave the staged draft in a form a human reviewer can approve or reject without
reconstructing the evidence chain from scratch.

The creating agent must not silently regress useful existing content from the live page. If an
existing anti-pattern, routing hint, or boundary note is removed, the creation log must explain why.

---

## 6. Token-Efficient Cookbook Design Rules

Cookbooks in this project are written for AI consumption as well as human reading.

### 6.1 Default budget

- Target roughly 700 to 1400 tokens per page.
- Exceed 1600 tokens only when the working example or a required caveat makes that unavoidable.
- Any exception must be justified in the creation log.

### 6.2 Front-loaded correction

Within the first 200 tokens of the `Overview` section, the draft must state:

- `Correct pattern:` the OpenWrt-specific right answer
- `Wrong pattern:` the common generic or hallucinated answer being corrected

### 6.3 Keep explanation proportional

- Prefer one complete working example over many partial snippets.
- Explain only the parts needed to correct the observed failure.
- Link outward for broader reference detail instead of duplicating the full API surface.
- Prefer a short callout below the title over a standalone `## When-to-use` section.
- Avoid repeating the same routing sentence in frontmatter, a dedicated H2, and the `Overview`.

### 6.4 Navigation and authority quality

- `Related Topics` entries must include a one-line decision hint such as `- use this when ...`.
- Verification notes should pair repo-local authority paths with the public upstream URL when both exist.
- If the page cites only a local pipeline artifact where a stable upstream URL also exists, the creation log must explain the omission.

---

## 7. Creation Log Minimum Contents

Every draft must have a companion creation log that records:

- target page and draft path
- packet, prompt, key, and raw-failure inputs consumed
- authority sources checked
- primary wrong patterns targeted
- incumbent live-page strengths reviewed
- incumbent content preserved, merged, or intentionally dropped
- what was intentionally excluded and why
- approximate token count of the draft
- confidence, open caveats, and what the reviewer should verify next

The creation log is the provenance and audit surface for cookbook authoring decisions.

---

## 8. Review And Promotion

### 8.1 Required reviewers

- human review is mandatory before promotion into `static/cookbook-source/`
- a second trusted-agent pass is recommended for a new standalone page and optional for a minor extension
- human review must be recorded using
  [10-human-review-procedure.md](./10-human-review-procedure.md)
  and stored beside the staging artifacts

### 8.2 Promotion gate

Promotion into the live cookbook corpus happens only after:

1. the draft exists
2. the creation log exists
3. the review record exists
4. the promotion checklist passes
5. the final page path is confirmed
6. the reviewer accepts the page as a bounded, source-backed correction

---

## 9. Failure Cases

If the draft fails review because it is too broad, too generic, or insufficiently grounded:

- keep it in `artifacts/authoring/drafts/`
- revise the draft, do not overwrite the live page yet
- update the creation log with the revision reason
- update the review record with the reject or revise decision

If the authority surface is still incomplete, revert the work back to packet or evidence collection rather than forcing publication.