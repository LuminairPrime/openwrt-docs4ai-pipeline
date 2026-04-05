# Cookbook Release Candidate Checklist

Use this checklist after deciding to create or revise a cookbook page.

## Before Authoring

- Scenario or blind failure is recorded
- Failure family is assigned
- Authority source is recorded
- Decision made: reject, golden-key-only, extend page, or new page
- Existing cookbook coverage checked
- Blind prompt or grouped prompt file identified
- Frozen answer key identified
- At least one raw blind-failure response archived for remediation-driven cookbook work
- Draft path reserved under `artifacts/authoring/drafts/`
- Creation-log path reserved under `artifacts/authoring/logs/`
- Review-record path reserved under `artifacts/authoring/reviews/`

## During Authoring

- Working draft lives under `artifacts/authoring/drafts/`
- Companion creation log lives under `artifacts/authoring/logs/`
- Companion human review record lives under `artifacts/authoring/reviews/`
- Page structure follows the active cookbook authoring spec
- Draft overview opens with `Correct pattern:` and `Wrong pattern:`
- When-to-use guidance is not redundantly repeated as frontmatter plus a standalone H2 plus overview prose
- Examples are source-backed
- Anti-patterns are real and OpenWrt-specific
- Verification notes record exact evidence used and pair repo-local and public upstream sources where both exist
- Related topic links include one-line decision hints
- For extensions and retroactive backfills, incumbent strengths were preserved or intentionally dropped with reasons
- Draft stays within the cookbook token budget, or the creation log explains why it does not

## Before Promotion

- Human review completed
- Review record decision captured and stored
- `common-ai-mistakes.md` link updates considered where appropriate
- Related topic links checked
- Final page path confirmed under `static/cookbook-source/`
- `reviewed_by` resolved to the accountable human reviewer for the promoted page
- Scenario moved from discovery to verification or benchmark-only state per `03-test-generation-contract.md`
- Draft, creation log, review record, and promoted page all agree on the final page shape

## If Review Fails

- Live cookbook page is not edited from the rejected draft
- Draft stays in staging and is revised in place
- Creation log notes the revision reason
- Review record captures the reject or revise decision and required follow-up
*** Add File: c:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\plans\v14\openwrt-cookbook-project-center\09-staged-authoring-lifecycle.md
# Staged Cookbook Authoring Lifecycle

**Purpose:** Make the staging-folder model explicit so cookbook work moves through repeatable lifecycle states instead of ad hoc edits to the live authored corpus.

---

## 1. Core Rule

Cookbook work discovered through the v14 cookbook center is authored in staging first.
The live corpus under `static/cookbook-source/` is the promotion target, not the working area.

Staging exists to keep three concerns separate:

- unsettled draft content
- provenance and scope decisions
- review and promotion decisions

---

## 2. Staging Artifact Set

Every staged cookbook unit has four coordinated artifacts:

1. draft page under `artifacts/authoring/drafts/`
2. creation log under `artifacts/authoring/logs/`
3. review record under `artifacts/authoring/reviews/`
4. promoted page under `static/cookbook-source/` after acceptance

The first three are required before promotion. The fourth exists only after promotion.

---

## 3. Lifecycle States

```text
candidate
	-> authoring-ready
	-> staged-draft
	-> in-human-review
	-> revise-in-draft | promotion-ready
	-> promoted
	-> verification
```

### 3.1 Candidate

The lesson is admitted as a scenario packet or cookbook gap, but no draft work has started.

### 3.2 Authoring-ready

The prompt, answer key, authority sources, and at least one raw blind failure are assembled.
This is the gate that permits draft creation.

### 3.3 Staged-draft

The draft and creation log exist in staging. The work is still unsettled and must not be treated as live cookbook truth.

### 3.4 In-human-review

The reviewer has the staged draft, creation log, and source packet open, and is recording a decision.

### 3.5 Revise-in-draft

The draft failed review or needs material correction. Revisions happen in staging only.

### 3.6 Promotion-ready

The review record accepts the draft, the checklist passes, and the page is ready to be synchronized into the live corpus.

### 3.7 Promoted

The settled page exists in `static/cookbook-source/` and is backed by matching staged artifacts.

### 3.8 Verification

The associated scenario is now used to verify whether the promoted page actually remediates the blind failure.

---

## 4. Promotion Rules

Promotion is allowed only when all of the following are true:

- the staged draft exists
- the creation log exists
- the review record exists
- the review decision is `accept` or `accept-with-edits`
- the release-candidate checklist passes

Promotion is blocked when:

- evidence is incomplete
- the page is too broad or generic
- the review decision is `revise-in-draft` or `return-to-evidence`

---

## 5. Retroactive Backfill For Already-Live Pages

Some cookbook pages reached `static/cookbook-source/` before the staging lifecycle was formalized.

Those pages may be reconciled retroactively by:

1. creating a staged draft that matches the intended promoted content
2. creating a creation log from the original scenario packet and authority sources
3. recording a review decision using the current review procedure
4. updating the live page only for spec-conformance or review-driven corrections

This backfill process is valid. It should be marked explicitly in the creation log so the audit trail is honest about timing.

---

## 6. Anti-Patterns

- writing directly into `static/cookbook-source/` before the draft exists
- treating a creation log as optional metadata rather than required provenance
- claiming final review without a review record
- leaving a rejected draft half-promoted in the live corpus
- allowing staging to become a graveyard of orphan drafts with no lifecycle state

---

## 7. Minimal Governance Expectation

Every staged cookbook unit should make it easy for a future maintainer to answer four questions quickly:

1. What failure or gap opened this work?
2. What exact authority was used?
3. Why was the page scoped this way?
4. Who accepted the promoted version, and what did they check?
*** Add File: c:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\plans\v14\openwrt-cookbook-project-center\10-human-review-procedure.md
# Human Review Procedure For Staged Cookbook Work

**Purpose:** Define how a human reviewer evaluates a staged cookbook draft and records a promotion decision.

**Authority:** This procedure applies to cookbook work staged under the v14 project center. It complements [09-staged-authoring-lifecycle.md](./09-staged-authoring-lifecycle.md) and [08-cookbook-authoring-execution-contract.md](./08-cookbook-authoring-execution-contract.md).

---

## 1. Required Inputs

Before reviewing a staged cookbook unit, open all of the following:

1. the staged draft in `artifacts/authoring/drafts/`
2. the creation log in `artifacts/authoring/logs/`
3. the source scenario packet
4. the blind prompt or grouped prompt file
5. the frozen answer key
6. at least one archived raw failure response for remediation-driven work
7. the current live page if the review is for an extension or retroactive backfill

If these inputs are not available, the reviewer should stop and return the work to evidence collection.

---

## 2. Review Questions

The reviewer should answer these questions in order.

1. Is the lesson clearly OpenWrt-specific and source-backed?
2. Does the draft correct the real blind failure rather than drifting into a generic subsystem tutorial?
3. Does the `Overview` front-load `Correct pattern:` and `Wrong pattern:` clearly enough for AI consumption?
4. Does the working example represent the right abstraction boundary for modern OpenWrt?
5. Are the anti-patterns real, current, and tied to observed failure shapes?
6. Do the verification notes name the exact corpus files, upstream files, or URLs checked?
7. Does the page stay within the intended token budget, or does the creation log justify the exception?
8. Do the draft, creation log, and intended promoted page agree on page shape and scope?

---

## 3. Allowed Decisions

The review record must end in exactly one decision.

| Decision | Meaning |
| --- | --- |
| `accept` | Draft is ready for promotion as written |
| `accept-with-edits` | Draft is promotable after listed minor edits are applied |
| `revise-in-draft` | Draft is directionally correct but needs material changes in staging |
| `return-to-evidence` | Inputs or authority are insufficient; do not continue authoring yet |

`accept-with-edits` is only for bounded, non-structural corrections. If the scope, authority, or main teaching boundary is wrong, use `revise-in-draft`.

---

## 4. Review Output Artifact

Every human review produces one review record under:

```text
artifacts/authoring/reviews/<cookbook-slug>-review-record.md
```

The record must include:

- reviewer identity
- review date
- staged draft path
- creation log path
- reviewed evidence inputs
- decision
- required changes or explicit acceptance notes
- promotion readiness statement

Use [artifacts/authoring/reviews/00-human-review-record-template.md](./artifacts/authoring/reviews/00-human-review-record-template.md) as the default template.

---

## 5. Promotion Rule

The reviewer does not edit the live page first and rationalize later.

Instead, promotion order is:

1. review staged draft
2. record decision
3. apply any accepted edits in staging
4. confirm checklist passes
5. synchronize the settled content into `static/cookbook-source/`

If the decision is `revise-in-draft` or `return-to-evidence`, the live page is not updated from that draft.

---

## 6. Retroactive Review Of Already-Live Pages

When an already-live page is being backfilled into the staging workflow, the reviewer should treat the staged draft as the proposed canonical source of truth and compare it against the live page.

The review record should say explicitly whether:

- the live page already matches the staged draft
- the live page needs small conformance edits
- the page should be revised in staging before any further promotion claim

---

## 7. Escalation Conditions

The reviewer should stop and escalate instead of accepting when:

- the claimed authority does not support the draft
- the page invents undocumented behavior
- the page collapses multiple boundaries into one oversized lesson
- the anti-patterns are generic Linux advice instead of OpenWrt-specific misses
- the evidence chain cannot be reconstructed from the staged artifacts

---

## 8. Minimal Reviewer Standard

Human review here is not cosmetic copy-editing. The reviewer is confirming that the page is a bounded, source-backed correction that belongs in the long-lived cookbook corpus.
*** Add File: c:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\plans\v14\openwrt-cookbook-project-center\artifacts\authoring\reviews\README.md
# Human Review Records

Store cookbook-center human review records under this directory.

Recommended naming:

```text
<cookbook-slug>-review-record.md
```

Use `00-human-review-record-template.md` as the starting point.

The review record is the decision surface that connects the staged draft and creation log to the promoted page in `static/cookbook-source/`.
*** Add File: c:\Users\MC\Documents\AirSentinel\openwrt-docs4ai-pipeline\docs\plans\v14\openwrt-cookbook-project-center\artifacts\authoring\reviews\00-human-review-record-template.md
# Human Review Record Template

## Review Target

- Target page: `static/cookbook-source/TODO.md`
- Draft page: `artifacts/authoring/drafts/TODO-draft.md`
- Creation log: `artifacts/authoring/logs/TODO-creation-log.md`
- Review date: `2026-04-05`
- Reviewer: `TODO`

## Inputs Reviewed

- Scenario packet: `TODO`
- Blind or grouped prompt: `TODO`
- Frozen answer key: `TODO`
- Raw failure response(s):
	- `TODO`
- Authority sources checked:
	- `TODO`
- Existing live page compared (if any): `TODO`

## Review Questions

- OpenWrt-specific and source-backed: `pass/fail`
- Draft corrects the real blind failure: `pass/fail`
- `Correct pattern:` and `Wrong pattern:` front-loaded clearly: `pass/fail`
- Working example uses the right current-era OpenWrt boundary: `pass/fail`
- Anti-patterns are real and OpenWrt-specific: `pass/fail`
- Verification notes cite exact evidence: `pass/fail`
- Token budget acceptable or justified: `pass/fail`
- Draft, log, and promoted page shape agree: `pass/fail`

## Findings

### Required changes

- `TODO`

### Advisory notes

- `TODO`

## Decision

- Decision: `accept | accept-with-edits | revise-in-draft | return-to-evidence`
- Promotion readiness: `ready | not ready`
- If not ready, next action: `TODO`

## Reviewer Accountability

- Name to use in promoted `reviewed_by`: `TODO`
- Review comments captured here are the authoritative human decision record for this staged cookbook unit.

## After Promotion

- Affected scenarios scheduled for verification rerun
- Family status updated
- Gap map updated if the work closed a known gap
