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

The point of staging is not just cleanliness. It also enforces the failure-first rule: the draft
should be traceable back to a real blind failure before it becomes part of the durable cookbook
corpus.

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

The prompt, answer key, authority sources, and at least one real raw blind failure are assembled.
This is the gate that permits draft creation.

If the scenario has source backing but no failed answer yet, it is not authoring-ready. The next
step is evidence collection, not cookbook drafting.

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

## 4. Real-Failure Requirement

Cookbook staging is for remediating real blind misses.

Accepted evidence paths are:

- archived failure from prior runs, including older v13 evidence bundles
- fresh blind run against an unaware agent when no archived failure exists yet

The unaware-agent fallback is valid only when the run is kept blind:

- no local OpenWrt documentation context is provided up front
- no repo-doc browsing is requested before the answer
- the raw answer is archived exactly as returned

If the unaware agent answers the scenario correctly, do not open cookbook remediation work for that topic unless a different real blind failure is later observed.

---

## 5. Promotion Rules

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

## 6. Retroactive Backfill For Already-Live Pages

Some cookbook pages reached `static/cookbook-source/` before the staging lifecycle was formalized.

Those pages may be reconciled retroactively by:

1. creating a staged draft that matches the intended promoted content
2. creating a creation log from the original scenario packet and authority sources
3. reconciling the staged draft against the current live page so still-valid incumbent strengths are preserved or explicitly dropped with reasons
4. recording a review decision using the current review procedure
5. updating the live page only for spec-conformance or review-driven corrections

This backfill process is valid. It should be marked explicitly in the creation log so the audit trail is honest about timing.

---

## 7. Anti-Patterns

- writing directly into `static/cookbook-source/` before the draft exists
- treating a creation log as optional metadata rather than required provenance
- claiming final review without a review record
- opening cookbook work from a hypothetical gap without a real failed answer
- leaving a rejected draft half-promoted in the live corpus
- allowing staging to become a graveyard of orphan drafts with no lifecycle state

---

## 8. Minimal Governance Expectation

Every staged cookbook unit should make it easy for a future maintainer to answer four questions quickly:

1. What failure or gap opened this work?
2. What exact authority was used?
3. Why was the page scoped this way?
4. Who accepted the promoted version, and what did they check?