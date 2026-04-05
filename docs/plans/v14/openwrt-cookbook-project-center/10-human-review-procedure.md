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
6. Do the verification notes name the exact corpus files, upstream files, or URLs checked, and do they pair local and public sources where possible?
7. Do the `Related Topics` links include one-line decision hints instead of a bare link list?
8. Did the staged draft preserve still-valid strengths from the current live page, or explicitly justify why something was dropped?
9. Does the page stay within the intended token budget, or does the creation log justify the exception?
10. Do the draft, creation log, and intended promoted page agree on page shape and scope?
11. Is the underlying failure actually a real blind miss rather than a hypothetical topic candidate?

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

If the reviewer cannot confirm a real blind failed answer exists, the decision must be `return-to-evidence`.

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
- the draft dropped any still-valid incumbent strength and, if so, whether that drop is justified

---

## 7. Escalation Conditions

The reviewer should stop and escalate instead of accepting when:

- the claimed authority does not support the draft
- the page invents undocumented behavior
- the page collapses multiple boundaries into one oversized lesson
- the anti-patterns are generic Linux advice instead of OpenWrt-specific misses
- the evidence chain cannot be reconstructed from the staged artifacts
- the staged work cannot be tied back to a real blind failed answer

---

## 8. Minimal Reviewer Standard

Human review here is not cosmetic copy-editing. The reviewer is confirming that the page is a bounded, source-backed correction that belongs in the long-lived cookbook corpus.