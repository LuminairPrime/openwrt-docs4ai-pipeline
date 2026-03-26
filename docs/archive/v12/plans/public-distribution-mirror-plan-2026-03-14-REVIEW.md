# Engineering Strategy Review: Public Distribution Mirror Plan

> **Superseded by V5a.** All concerns addressed in V5a. See [public-distribution-mirror-plan-2026-03-15-V5a.md](public-distribution-mirror-plan-2026-03-15-V5a.md).

**Target Document:** `public-distribution-mirror-plan-2026-03-14.md`
**Review Date:** 2026-03-14
**Reviewer:** Software Engineering / Architecture

## 1. Executive Summary

While the conceptual separation of the pipeline repository from the product distribution repository is fundamentally sound, the current plan contains several technical ambiguities and hidden traps. If handed to a developer in its current state, these gaps grant too much implementation freedom, which raises the risk of a brittle, partially correct, or operationally inconsistent deployment.

The first-draft plan is directionally right, but it is underspecified in the exact areas that usually break deployment architecture work:

- ownership of files in the target repository
- packaging boundaries between the public shell and the generated corpus
- failure isolation during cross-repository publishing
- URL and path contracts for the root router versus the generated corpus
- idempotent release behavior across repeated runs on the same day
- exact sequencing of implementation so the feature can be landed safely

The core problem is not that the design is wrong. The problem is that the design, as originally written, leaves too many implementation decisions implicit. Those gaps would allow different developers to make locally reasonable but globally incompatible choices.

## 2. Hidden Ambiguities and Technical Risks

### A. Workspace assembly ambiguity

The original plan states that the ZIP should be generated from the same assembled distribution workspace that is pushed to the target repository, but it also states that the ZIP intentionally excludes the target repository root shell.

That creates a design contradiction.

If the target repository workspace contains:

- root `README.md`
- root `index.html`
- root `llms.txt`
- `.nojekyll`
- `openwrt-condensed-docs/`

then a ZIP built from that exact workspace would also contain the root shell unless the implementation adds a second exclusion rule. That means the workflow actually needs two staging views derived from the same validated corpus:

1. a Pages mirror staging tree that includes the shell plus `openwrt-condensed-docs/`
2. a ZIP staging tree that contains only `openwrt-condensed-docs/`

Without naming those two staging areas explicitly, a developer could implement the wrong packaging boundary and still believe they followed the plan.

### B. Target repository file ownership ambiguity

The original plan describes the target repository root as a hand-maintained public shell. That sounds simple, but it leaves an operational question unanswered: who owns those files over time?

Possible interpretations include:

- manually edited only in the target repo
- copied from templates in the source repo
- partially overwritten by CI and partially maintained by hand

Those interpretations are not equivalent.

If the root shell is manually edited directly in the target repository while the corpus is CI-managed from the source repository, drift becomes unavoidable. The source repo stops being the real system of record for the deployed public product.

To avoid that split-brain situation, the shell should be source-controlled in the engineering repository, ideally under a dedicated template directory such as `templates/distribution-shell/`, and then deployed verbatim into the target repository root. That makes the shell reviewable, testable, and versioned alongside the deployment logic.

### C. Release cadence ambiguity

The original plan says ZIP assets are dated, but it does not state which events should trigger publication.

That matters because the current workflow already runs on:

- `push` to `main`
- monthly `schedule`
- `workflow_dispatch`

If all three continue to publish the distribution mirror, the dated release model needs an explicit same-day update rule. Otherwise the implementation could fail on the second successful run of the day because the tag or asset already exists.

A correct plan must specify at least the following:

- whether all existing deploy triggers also publish the distribution repo
- whether same-day runs replace the existing asset or create a second uniquely named one
- whether release tags are date-only or date-plus-run identifiers

Without that, release behavior is left to developer choice.

### D. Cross-repository failure domain ambiguity

The original plan does not clearly separate failure impact between:

- source repository promotion
- source repository Pages mirror
- target repository mirror push
- target repository release creation

That omission is dangerous because a developer might restructure the existing deploy job so that a new cross-account failure blocks or corrupts the already-working source-repo promotion behavior.

The correct failure contract should be:

1. existing source-repo promotion continues to run exactly as it does today
2. existing source `gh-pages` mirroring continues to run exactly as it does today
3. only after those steps succeed should the new distribution mirror branch of work begin
4. if the new target-repo push fails, the source repo must still remain successfully deployed

That order preserves current known-good behavior while isolating the new feature's risk.

### E. Empty or truncated corpus deployment risk

The original plan assumes that if `final-staging` exists, it is safe to publish. That assumption is too weak for a cross-repository public deployment.

A pipeline can produce a syntactically valid but materially broken corpus if, for example:

- an upstream input silently changes format
- a generator outputs only headers or partial files
- the routing index becomes tiny because module discovery failed
- HTML generation succeeds while the corpus is incomplete

Before any cross-repo deployment, the workflow should run a gatekeeper check with minimum health assertions such as:

- `openwrt-condensed-docs/llms.txt` exists
- `openwrt-condensed-docs/llms.txt` is above a minimum size threshold
- `openwrt-condensed-docs/index.html` exists
- a minimum number of module directories exist

Without a gatekeeper, the plan allows technically successful deployment of a broken product.

### F. Root router versus inner corpus router ambiguity

The original plan correctly says the root `llms.txt` should be a distribution-level router and not a blind copy of the inner corpus `llms.txt`. That is a good decision, but it still needs a stricter contract.

Specifically, the plan should state:

- root `llms.txt` links must point into `./openwrt-condensed-docs/`
- inner corpus `llms.txt` links remain relative to the corpus root itself
- the two routing scopes must never be mixed

Without that explicit rule, a developer may rewrite generated corpus links as if they live at repository root, which would break ZIP-extracted behavior and weaken the extracted-package contract.

### G. Git history strategy ambiguity

The plan originally says to publish to the target repository but does not define whether updates should be:

- force-pushed snapshots
- normal append-only commits
- orphan-branch resets
- branch-replacement worktrees

This matters because the target repository is public infrastructure. Destructive history strategies make auditing and recovery harder. The design should explicitly prefer append-only commits on `main` for the distribution repo, with a bot-authored commit message that includes the source commit identity.

### H. Account type ambiguity

The first draft treated a dedicated regular account as acceptable for v1. That is functionally true, but from an operations perspective it is weaker than an organization.

The meaningful differences are not Pages rendering. The public site looks the same either way. The real differences are:

- multi-admin recovery
- separation of human and automation concerns
- easier long-term governance
- avoiding a future user-to-organization conversion event

The plan should state a default preference instead of leaving the choice too open.

## 3. Account Strategy: Regular User vs Organization

### Current engineering assessment

There is no namespace penalty to reserving the name under a regular GitHub account first. GitHub lets you claim the namespace either way, and that name is what matters for the Pages endpoint.

However, there is an operational penalty to starting with a regular user if the project later needs to become a multi-maintainer long-lived public distribution surface.

The tradeoffs are:

| Topic | Regular user account | Organization |
| --- | --- | --- |
| Namespace reservation | good | good |
| Pages URL shape | same | same |
| Multi-admin recovery | weak | strong |
| Governance model | personal | team-oriented |
| GitHub App operational model | acceptable | better |
| Future conversion risk | present | none |

### Recommendation

Use an Organization from day one unless speed of initial setup is materially blocked by that choice.

The reason is not aesthetic. It is operational durability. This feature is supposed to become a long-term public publishing surface. The small amount of setup convenience gained by using a regular user account is not worth the future conversion risk if the project later needs shared ownership.

### Is there a penalty to reserving the domain under the wrong type?

Not in the sense of losing the name. The namespace is still reserved.

The real penalty is migration friction if the account later needs to change type or governance model. That friction includes:

- transferring ownership semantics
- revalidating app installation assumptions
- rechecking secret management and admin recovery paths
- re-documenting operational ownership

So the answer is:

- **no penalty for the name itself**
- **real penalty for the surrounding operational model if you choose the wrong ownership structure early**

## 4. Recommended Implementation Order

The original plan listed major steps, but it needed a more constrained order so developers cannot implement the most dangerous pieces first.

The safest implementation sequence is:

### Phase 0: Lock the design contract

Before code changes, finalize the architectural rules in one durable plan document.

This must include:

- account type decision
- file ownership model
- staging directory model
- release replacement behavior
- gatekeeper rules
- trigger model

This is required because otherwise developers may implement mutually inconsistent assumptions.

### Phase 1: Provision target infrastructure manually

Before touching the workflow, create the external target infrastructure once.

Steps:

1. create the target account or organization
2. create `openwrt-docs4ai.github.io`
3. enable GitHub Pages on the target repository
4. create and install the GitHub App
5. store the App ID and private key in source repo secrets

Reason: until this exists, the deploy job can only be designed, not validated end to end.

### Phase 2: Introduce source-controlled shell templates

Add a dedicated template directory in the source repo, for example:

```text
templates/distribution-shell/
```

Files:

- `README.md`
- `index.html`
- `llms.txt`
- `.nojekyll`

Reason: this resolves the file-ownership ambiguity before workflow logic is added.

### Phase 3: Add gatekeeper and packaging logic locally

Before cross-repository push logic, add the guardrails:

- gatekeeper checks on the generated corpus
- ZIP packaging logic
- explicit staging area layout

Reason: these can be tested without needing the target repository push to be live.

### Phase 4: Extend the deploy workflow with isolated new steps

Only after the above phases are done should the workflow gain:

- GitHub App token minting
- target repository checkout
- corpus sync into target repo
- release creation and asset upload

Reason: by this point the deployment inputs and boundaries are already concrete.

### Phase 5: Add tests and documentation for long-term maintenance

After end-to-end proof, update:

- maintainer docs
- architecture docs
- tests that lock the new contracts in place

Reason: otherwise the feature will regress later because its operational constraints remain undocumented.

## 5. Recommended Deployment Schedule and Operations Model

### Trigger model

The cleanest first operational model is to keep the new distribution publishing tied to the same events that already drive deployment:

- push to `main`
- monthly scheduled run
- manual `workflow_dispatch`

That avoids creating a second independent scheduling system.

### Same-day publish behavior

Because the asset is date-stamped, same-day reruns should replace the existing asset for that day rather than inventing a second name unless there is a strong requirement for build-level archival.

That means:

- the release tag can stay date-based
- the ZIP asset name can stay date-based
- reruns on the same date update the release body and replace the asset

This keeps the public surface stable and avoids asset-name sprawl.

### Operational schema for high-quality operation

A high-quality operational publishing model should look like this:

1. generate and validate corpus in the source repo exactly as today
2. promote corpus back into the source repo exactly as today
3. mirror source repo Pages output exactly as today
4. run distribution gatekeeper checks
5. build the ZIP from the validated corpus subtree
6. clone the target repo into a clean runner temp directory
7. sync `openwrt-condensed-docs/` into the target repo
8. copy shell templates into the target root
9. commit and push if there are changes
10. create or update the release for the day
11. upload or replace the dated ZIP asset

This order matters because it preserves existing known-good behavior first, then layers the new distribution publishing on top of it.

## 6. Concrete Constraints Developers Must Not Violate

To avoid buggy implementation freedom, the following rules should be explicit and non-optional.

1. **The distribution repository is a deployment target, not a development environment.**
   No direct hand-editing there should be considered authoritative.
2. **Shell files must be source-controlled in the engineering repo.**
   The target repo receives them by deployment, not by manual drift.
3. **The ZIP and the public mirror must originate from the same validated corpus state.**
   They may use different staging views, but they must share the same source data.
4. **A broken or suspiciously small corpus must not publish.**
   Gatekeeper checks are required.
5. **Existing source-repo deploy behavior must remain intact even if the new target-repo steps fail.**
6. **Root routing files and inner corpus routing files must have distinct scope-aware link contracts.**
7. **Release update behavior for repeated same-day runs must be explicit and idempotent.**
8. **The account ownership model must support long-term recovery, not just initial convenience.**

## 7. Final Engineering Judgment

The underlying feature is worth doing and the split is technically justified.

The first draft was a good architectural direction statement, but not yet a safe implementation document. It still allowed enough freedom that two competent developers could have built incompatible versions of the feature while both claiming they followed the plan.

The plan becomes strong only when it resolves the following categories explicitly:

- target ownership
- shell ownership
- packaging boundaries
- deployment sequencing
- failure isolation
- release idempotency
- routing scope
- gatekeeper enforcement

Once those are written down concretely, the feature becomes implementation-safe instead of merely conceptually appealing.
