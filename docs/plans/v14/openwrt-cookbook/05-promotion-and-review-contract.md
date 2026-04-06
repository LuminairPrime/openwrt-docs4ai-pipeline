# Promotion And Review Contract

**Purpose:** Define how a scored failure becomes cookbook work and what must be true before that work is considered complete.

**Authority:** This contract extends [../../../specs/cookbook-authoring-spec.md](../../../specs/cookbook-authoring-spec.md).

---

## 1. Admission Rule

A single blind failure is enough to open cookbook work when it is:

1. OpenWrt-specific
2. source-backed
3. not already adequately covered
4. teachable as a bounded task or decision

This opens work. It does not automatically decide the final publication shape.

The failure must be a real agent failure. If the scenario has no archived failure yet, the
operator may run a fresh blind test against an unaware agent, but cookbook work does not open
until that run produces a real miss.

---

## 2. Promotion Outcomes

| Outcome | Use when |
| --- | --- |
| Reject | The failure does not represent a durable or source-backed OpenWrt lesson |
| Golden-key-only | The truth schema needs refinement but cookbook coverage is already adequate |
| Extend existing page | The missing lesson fits naturally inside a current cookbook page |
| New standalone page | The lesson is durable, specific, and insufficiently covered anywhere else |
| Umbrella page | Several families point to one bigger OpenWrt decision boundary |

---

## 3. Promotion Questions

Ask these in order.

1. Is the failure clearly OpenWrt-specific?
2. Can the correct lesson be sourced from current authority?
3. Is there already a page that should own the lesson?
4. Is the lesson big enough to deserve a standalone page?
5. Will the resulting page teach a durable pattern rather than a one-off patch?

If the answer to question 1 or 2 is no, reject or keep the change at golden-key-only level.

---

## 4. Authoring-Ready Gates Before Drafting

Before authoring or revising a page, confirm:

- scenario and failure are recorded
- family assignment exists
- authority source is recorded
- target page decision exists
- the work does not duplicate an already-covered lesson
- the creating agent has the blind prompt or grouped prompt file
- the creating agent has the frozen answer key
- at least one raw blind-failure response is archived under
	`artifacts/results/<agent-label>/<run-label>/` for new-page or material-remediation work
- a draft path and a creation-log path have been reserved under `artifacts/authoring/`

If the raw failure response is missing, the scenario may stay admitted, but cookbook
authoring does not start yet.

If the missing evidence is the only blocker, the next action is to run the scenario against an
unaware agent with no OpenWrt documentation context and archive the result. A clean pass from
that unaware run is evidence against writing a cookbook for the topic.

---

## 5. Drafting Workflow And Staging Paths

The cookbook center uses a staged authoring workflow.

### 5.1 Draft location

The creating agent writes the working draft under:

```text
artifacts/authoring/drafts/
```

Example:

```text
artifacts/authoring/drafts/ucode-async-process-pattern-draft.md
```

### 5.2 Creation log location

The creating agent writes a companion log under:

```text
artifacts/authoring/logs/
```

Example:

```text
artifacts/authoring/logs/ucode-async-process-pattern-creation-log.md
```

The creation log records:

- which prompt, answer key, packet, and raw failures were consumed
- which authority sources were checked
- which failure patterns were treated as the primary correction targets
- what was intentionally excluded to preserve scope and token budget
- confidence and open caveats before promotion

### 5.3 Review record location

The human review record lives under:

```text
artifacts/authoring/reviews/
```

Example:

```text
artifacts/authoring/reviews/ucode-async-process-pattern-review-record.md
```

The review record must be created from the staged draft and companion creation log. The
required review method is defined in
[10-human-review-procedure.md](./10-human-review-procedure.md).

### 5.4 Promotion boundary

The live authored corpus under `static/cookbook-source/` is the promotion target, not
the drafting workspace. If the draft fails review, it stays in `artifacts/authoring/drafts/`
until revised.

Human review is mandatory before claiming a final promoted cookbook page. A second
trusted-agent pass is optional but recommended for major new pages.

---

## 6. Review Gates After Drafting

Before considering the cookbook update complete, confirm:

- draft content exists in `artifacts/authoring/drafts/`
- companion creation log exists in `artifacts/authoring/logs/`
- companion human review record exists in `artifacts/authoring/reviews/`
- the promoted page location is correct under `static/cookbook-source/`
- frontmatter matches the active cookbook authoring spec
- `reviewed_by` is not left unresolved if final review is being claimed
- verification notes name the exact evidence sources used
- verification notes pair repo-local authority paths with public upstream URLs where both exist
- the page opens with the corrective pattern before the long explanation
- the page stays within the cookbook token budget (target 700 to 1400 tokens), or the log explains why it exceeds it
- related topic links include one-line decision hints and `common-ai-mistakes.md` links are updated where appropriate
- incumbent strengths from the current live page were preserved or intentionally dropped with a stated reason when the work is an extension or retroactive backfill
- the review record decision matches the promoted page and does not leave unresolved major issues

---

## 7. Verification Gate

After authoring, the affected scenario subset should be moved into verification mode.

Use the scenario lifecycle states defined in [03-test-generation-contract.md](./03-test-generation-contract.md) when deciding whether the scenario moves to verification or benchmark-only status.

The verification outcome can be one of:

- improvement observed
- no change yet, but page remains structurally correct and useful
- page needs revision because the scenario still reveals a coverage gap

This means cookbook work is allowed to be valuable even before a later model proves the remediation effect, but the retest status must still be recorded.

---

## 8. Priority Uplift Rules

Repeated failures should raise priority when they show:

- multiple models missing the same lesson
- multiple scenarios collapsing into the same family
- a structural current-era OpenWrt boundary
- a lesson likely to matter for a future OpenWrt skill or agent

Repeated failure is a priority multiplier, not an admission requirement.

---

## 9. Release-Candidate Checklist

Use the procedural checklist in [artifacts/promotion/00-release-candidate-checklist.md](./artifacts/promotion/00-release-candidate-checklist.md) when promoting cookbook work from draft to settled candidate.
