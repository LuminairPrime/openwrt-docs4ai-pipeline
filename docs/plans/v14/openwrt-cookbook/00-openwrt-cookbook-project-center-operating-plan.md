# V14 OpenWrt Cookbook Project Center Operating Plan

**Status:** Proposed working prototype  
**Date:** 2026-04-05  
**Applies To:** Future cookbook discovery, test generation, cookbook promotion, and later OpenWrt skill extraction  
**This document is canonical:** All rationale, selection logic, and operating decisions for the cookbook system belong here. The other files in this folder are factual inventories, copied artifacts, or operational checklists.

---

## 1. Purpose

This project center exists to answer one question in a reproducible way:

> How do we turn blind AI failures on OpenWrt tasks into durable, source-backed cookbook pages that teach the correct OpenWrt programming pattern?

The answer is not "run recursive AI experiments until something looks good". The answer is a controlled system with:

1. fixed truth inputs
2. fixed rules for creating new tests
3. fixed rules for deciding when a failure deserves cookbook treatment
4. fixed rules for deciding whether the result becomes a new page, an update to an existing page, or only a golden-key change

This center is a coordination layer, not a new pipeline stage. The live authored cookbook corpus remains under `static/cookbook-source/`, and the live publication pipeline remains the main repository pipeline.

The second-most important deliverable of this center, after the cookbook pages themselves, is the test bank and its grouped delivery files. The cookbook system needs stable blind prompts both to discover missing lessons and to verify later that an AI supplied with the cookbook can now answer those same questions correctly.

---

## 2. Core Decision

This center adopts:

- **Option 3: Golden-key / ontology first** as the conceptual backbone
- **Option 4: Decision-cookbook layer** as the publication model

And it retains one execution discipline from the earlier option matrix:

- **Strict failure-first measurement** for blind reruns and later remediation verification

In plain terms:

- truths and falsenesses are defined first
- tests are created to probe those truths blindly
- failures are clustered into programming families
- cookbook pages teach durable OpenWrt decisions and task patterns, not isolated mistakes

Most importantly, cookbook work stays failure-first. A cookbook page exists to remediate
something a real AI agent actually got wrong in blind conditions. Tutorials for tasks that
blind agents already solve correctly are not useful outputs for this project center.

---

## 3. Why This Center Exists

The repository already contains most of the raw material needed for a strong cookbook system:

- a scenario bank
- a metadata catalog with expected paradigms
- a golden answers key
- cross-batch failure synthesis
- a cookbook authoring spec
- a substantial authored cookbook corpus

What has been missing is a single, clearly written operating plan that explains:

- how new tests are created
- where test inspiration comes from
- how correctness criteria are selected
- how one failure becomes a cookbook candidate
- when a candidate becomes a new page versus an extension of an existing page
- how this later turns into an OpenWrt coding skill or agent

This document is intended to be the answer another maintainer could read first and then use to continue the work.

---

## 3A. Working Artifacts In This Center

The core working artifacts for the prototype now live here:

- seed registry: [artifacts/registry/00-failure-family-registry.seed.yaml](./artifacts/registry/00-failure-family-registry.seed.yaml)
- live operator registry: [artifacts/registry/01-failure-family-registry.live.yaml](./artifacts/registry/01-failure-family-registry.live.yaml)
- scenario admission template: [artifacts/templates/00-scenario-admission-template.yaml](./artifacts/templates/00-scenario-admission-template.yaml)
- grouped prompt header template: [artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md)
- admitted packet examples: `artifacts/scenario-packets/`
- grouped operator prompt files: `artifacts/test-groups/`
- manual agent result bundles: `artifacts/results/`

Use the seed registry as the frozen starting ontology. Use the live registry to track mutable workflow state over time.

Use the scenario-admission template when defining a new candidate packet. Use the grouped prompt
header template when creating or refreshing grouped prompt files so the shared execution contract
stays consistent across manual-run surfaces.

---

## 4. Non-Negotiable Decisions

### 4.1 Canonical authored-source path

The live authored cookbook path is:

```text
static/cookbook-source/
```

That path is the active filesystem contract in [schema-definitions.md](../../specs/schema-definitions.md).

Older references to `content/cookbook-source/` are historical v13 wording and must not be used as current path truth.

### 4.2 One failure can be enough

One blind, source-backed, OpenWrt-specific failure is enough to open a cookbook candidate.

That failure must be a real agent failure, not a hypothetical concern. Acceptable evidence is:

- an archived blind failure from prior runs, including the v13 mistake-discovery results
- a fresh blind run against an unaware agent with no OpenWrt file-system documentation help,
  performed specifically to test the scenario when no archived failure exists yet

Repeated failures are still useful, but they are used to:

- increase priority
- confirm breadth
- merge duplicates into families
- justify umbrella pages

They are **not** required for admission.

They are also not a substitute for the first real miss. Cookbook work begins only after an
actual blind failure is observed and archived.

### 4.3 Discovery and benchmarking are different modes

This center recognizes two valid modes:

- **Cookbook discovery mode:** find missing lessons quickly
- **Competence benchmarking mode:** profile a model against a fixed bank

The default mode for cookbook work is cookbook discovery mode.

### 4.4 Failed discovery tests leave the active queue

When a scenario fails in cookbook discovery mode and that failure opens an accepted cookbook candidate, that scenario leaves the active discovery queue.

It does **not** disappear entirely. It moves to one of these states:

- cookbook candidate open
- cookbook authored, pending verification
- benchmark-only

This prevents the discovery loop from repeatedly rediscovering the same already-known lesson.

Later discovery iterations against a different AI agent may therefore omit that already-accepted failing scenario from the required discovery set.
That is allowed because one blind failure is sufficient to admit the lesson into cookbook construction.

However, later iterations may still rerun the same scenario on purpose when the operator wants more failure evidence.
Two failures can still be useful if they fail for different reasons, trigger different falsenesses, or expose a better teaching angle for the eventual cookbook page.

---

## 5. Operating Model

The cookbook system is three linked loops, not one recursive loop.

```text
Loop A: Truth Capture
  upstream code + corpus docs + archive evidence + golden key maintenance

Loop B: Blind Failure Measurement
  scenario design + blind prompting + scoring + failure recording

Loop C: Remediation Promotion
  failure families + cookbook decision + authoring + retest + later skill extraction
```

Each loop has a different acceptance rule.

| Loop | Goal | Acceptance Rule |
| --- | --- | --- |
| Truth Capture | Define what is correct or false in current-era OpenWrt | Every claimed paradigm must be traceable to a live source or a named historical evidence packet |
| Blind Failure Measurement | See whether a blind AI actually misses the pattern | The prompt stays blind and the score stays anchored to the frozen truth inputs |
| Remediation Promotion | Decide what documentation to write or extend | The failure must map to a durable OpenWrt lesson and a real cookbook destination |

---

## 6. Canonical Units

The system uses three different units on purpose.

### 6.1 Scenario

The unit of raw measurement.

A scenario asks one bounded OpenWrt question in blind form.

### 6.2 Failure Family

The unit of synthesis.

A failure family groups multiple failures that all require the same corrective OpenWrt lesson.

### 6.3 Cookbook Page

The unit of publication.

A cookbook page teaches a durable task boundary or decision boundary. One page may absorb several failure families.

This separation prevents the common mistake of turning every failed prompt into its own published page.

---

## 7. Source-Of-Truth Precedence

When there is conflict, use this precedence order.

| Rank | Source | Usage |
| --- | --- | --- |
| 1 | Current upstream OpenWrt, LuCI, packages, procd, rpcd, libubus, libubox code | Highest authority for implementation patterns |
| 2 | Current repo corpus and authored cookbook pages | Repository-local truth surface for routing, summaries, and already-verified teaching material |
| 3 | Active frozen test-pack artifacts in this project center | Reproducibility inputs for reruns |
| 4 | OpenWrt wiki or official release material | Useful for public-facing phrasing and historical explanation |
| 5 | Archive threads and mailing-list evidence | Strong source for recurring confusion, migration pain, and historical context |
| 6 | Prior synthesis docs and model score summaries | Useful evidence, but not final authority by themselves |

Observed AI failures are never a correctness source. They are only signals that a lesson may be missing, unclear, or badly surfaced.

---

## 8. Criteria And Where They Come From

The system uses several different kinds of criteria. They come from different sources.

| Criterion Type | What It Means | Primary Source |
| --- | --- | --- |
| Test inspiration criterion | Why a new scenario should exist | Blind failures, archive confusion, upstream transitions, uncovered cookbook gaps |
| Correctness criterion | What the correct answer must do | Upstream source, current corpus, frozen golden key |
| Blindness criterion | What must be hidden from the target model | Scenario prompt-writing rules in this center |
| Promotion criterion | Whether the failure should open documentation work | This operating plan + failure family framework |
| Authoring criterion | What the cookbook page must contain | Active cookbook authoring spec |
| Publication criterion | Where authored material lives and how it ships | Active schema definitions and release-tree contract |

---

## 9. Where New Tests Come From

New tests must come from one or more of the following inspiration channels.

### 9.1 Preferred inspiration channels

1. **A blind AI failure that exposed an uncovered OpenWrt lesson**
2. **A known gap in the current cookbook corpus**
3. **A current upstream pattern or migration boundary likely to confuse generic Linux reasoning**
4. **A recurring archive or community confusion pattern**
5. **A missing lesson needed for a future OpenWrt skill or agent**

### 9.2 Test inspiration ladder

Use this ladder in order.

1. Name the OpenWrt boundary being taught.
2. Find the live authoritative implementation or documentation.
3. Confirm the lesson is not already adequately covered in `static/cookbook-source/`.
4. Decide whether the lesson is small enough for one scenario.
5. Record the exact source that justifies the expected paradigm.
6. Write a blind prompt that asks for the output without naming the solution.

If steps 1 through 5 cannot be completed, the topic is not ready to become a scenario.

If the scenario is admitted but there is no archived failing answer yet, the operator may run
the prompt against a deliberately unaware subagent that:

- receives only the blind prompt
- is not given OpenWrt-specific local documentation context
- is not asked to search the repository documentation tree for help first

That run exists only to determine whether a real blind failure occurs. If the unaware agent
passes cleanly, the topic should not be promoted into cookbook remediation work.

---

## 10. Rules For Creating A New Scenario

Every new scenario must satisfy all of the following.

1. It targets one bounded OpenWrt decision boundary.
2. It can be scored with a clear pass/fail result.
3. The expected paradigm is traceable to a live source.
4. The prompt does not include the answer path or source URL.
5. The failure can map to a failure family.
6. The lesson could plausibly become a cookbook page or page extension.

### 10.1 Good scenario shapes

- a procd init script that must use `uci_load_validate`
- a LuCI JS view that must use `rpc.declare`
- a ucode task that must use native `fs.readfile()` and `json()`
- a C daemon skeleton that must use `uloop_init()` then `ubus_connect()` then `ubus_add_uloop()`

---

## 10A. Grouped Test Delivery Rule

The scenario bank is not delivered to target AI agents as one giant monolithic prompt by default. The operator-facing delivery unit is the **grouped batch file**.

Grouped batches exist for two reasons:

1. to keep manual evaluation time-efficient
2. to avoid letting one solved question teach the model how to answer a later similar question in the same prompt

Therefore the default rule is:

- one question per domain/category/type in a batch wherever practical
- do not place multiple closely related questions in the same prompt if solving one would materially hint the answer path for the other
- when in doubt, split the adjacent questions into separate grouped batches

The historical Alpha, Beta, and Gamma slices are the model for this delivery style. The v14 center preserves that discipline and applies it again to new focused rerun groups.

### 10.2 Bad scenario shapes

- a broad prompt that mixes multiple unrelated OpenWrt boundaries
- a prompt whose only correct answer depends on unverified folklore
- a prompt that is really a generic Linux question with no OpenWrt-specific lesson
- a prompt whose answer is already fully taught by an existing cookbook page and adds no new edge

---

## 11. Administration Modes

### 11.1 Default: cookbook discovery mode

This is the default for future cookbook work.

Operator workflow:

1. Start with the active discovery queue.
2. Run the queue against the weakest currently viable model, or another intentionally low-competence baseline.
3. For each blind fail:
   - score it against the frozen truth inputs
   - assign a failure family
   - decide whether it opens a cookbook candidate
4. If it opens a cookbook candidate, remove that scenario from the active discovery queue.
5. Carry only passed scenarios forward to the next model in discovery mode.

Reasoning:

- this maximizes discovery efficiency
- one failure is enough to reveal the need for a lesson
- repeated discovery of the same lesson wastes operator time

### 11.2 Optional: full-bank sweep mode

This mode runs the full scenario bank against multiple models once, even if cost is slightly higher.

Use it when:

- a broad cross-model picture is needed
- failure-family merging needs stronger evidence
- a release-quality synthesis document is being produced

This mode is optional because it does not change admission. It improves prioritization and confidence.

### 11.3 Verification mode

After a cookbook page is authored or materially revised, rerun only the affected scenario subset.

The purpose is not rediscovery. The purpose is remediation measurement.

### 11.4 Benchmark mode

When profiling one specific model or a future OpenWrt skill, run a chosen benchmark suite. This may include scenarios already retired from discovery.

---

## 12. Queue Model

The scenario bank is not one flat list forever.

| Queue State | Meaning | Next Move |
| --- | --- | --- |
| Candidate | Proposed test not yet admitted | Review against scenario creation rules |
| Active discovery | Used to find missing lessons | Run in discovery mode |
| Cookbook candidate open | Scenario already exposed a missing lesson | Stop using it for discovery; move into family and promotion flow |
| Verification | Scenario now tests whether the cookbook fixed the lesson | Rerun after authoring |
| Benchmark-only | Still useful for profiling models or skills | Exclude from discovery, keep for benchmarking |
| Retired | No longer useful or was merged into another scenario | Keep lineage note only |

### Queue lifecycle

```text
Candidate
  -> Active discovery
  -> Blind fail
  -> Cookbook candidate open
  -> Cookbook authored or existing page extended
  -> Verification
  -> Benchmark-only or Retired
```

---

## 13. One Failure Enough: Admission Rule

One failure is enough to open cookbook work when all of the following are true:

1. the failure was blind
2. the failure is OpenWrt-specific
3. the corrective lesson is source-backed
4. the lesson is not already adequately covered
5. the lesson is teachable as a bounded task or decision

### 13.1 Iterative administration after the first accepted failure

After a scenario has already produced one accepted blind failure, later human test-administration iterations have two valid options:

1. **Reduced-follow-on mode**
  Skip that already-accepted scenario in later discovery runs, because the admission threshold has already been met.

2. **Full-rerun mode**
  Keep running the scenario anyway, because a second model may fail differently and produce additional cookbook-relevant evidence.

The center supports both modes. The important distinction is this:

- one accepted failure is enough to justify cookbook construction
- additional failures are optional evidence, not a prerequisite for acceptance

If a later run includes an already-accepted failing scenario again, the reviewer may either:

- do a full fresh evaluation because the duplicate failure still teaches something new
- or mark it as a duplicate accepted fail and use a short confirmation record that points back to the earlier accepted run

Repeated failures change **priority**, not **admissibility**.

Admission still requires a real failed answer. The system does not create cookbook work from
speculation alone.

### What repeated failures are still used for

- to decide whether a lesson becomes a standalone page instead of a short section
- to merge many concrete failures into one umbrella family
- to decide whether a family is structural versus incidental
- to justify skill-extraction importance later

---

## 14. Failure Families As The Deduplication Layer

The failure family is the bridge between blind tests and cookbook pages.

Examples:

- missing `USE_PROCD=1`
- manual watchdog loop in shell
- PID file management in init scripts

All three may cluster into one broader family:

> **Service lifecycle and supervision on OpenWrt belongs to procd, not generic Linux init habits.**

Likewise:

- `jq` in ucode
- shelling out to `cat` for JSON
- inventing raw file descriptor reads for `fs.popen()`

May cluster into:

> **ucode is a native runtime with its own file, JSON, module, and async model.**

This project center keeps the detailed family taxonomy in [04-failure-family-framework.md](./04-failure-family-framework.md).

---

## 15. Outcome Decision Rules

Not every failure becomes a new page.

### 15.1 Possible outcomes

| Outcome | Use When |
| --- | --- |
| Reject | The failure is not OpenWrt-specific, not source-backed, or not durable |
| Golden-key-only update | The truth schema needs refinement but cookbook coverage is already sufficient |
| Extend existing page | The lesson belongs inside an existing cookbook page |
| New standalone page | The lesson is durable, bounded, and not already covered |
| Umbrella page | Several families share one higher-level OpenWrt decision boundary |
| Skill extraction note | The lesson is stable enough to later shape an OpenWrt coding skill |

### 15.2 Decision rule

Prefer **extend existing page** over **new page** unless the lesson has its own strong identity, repeated importance, or a clean task boundary.

Prefer **golden-key-only** when the failure sharpens scoring but does not introduce a meaningful new teaching need.

---

## 16. Cookbook Pages Are Remediation Units

Cookbook pages are not raw mistake catalogs.

They are remediation units.

That means:

- the page must teach the correct OpenWrt pattern
- the page may mention several anti-patterns
- the page is organized around what to do, not around what a model got wrong

This is why the system publishes to durable pages like:

- `firstboot-uci-defaults-pattern.md`
- `hotplug-handler-pattern.md`
- `ucode-rpcd-service-pattern.md`
- `inter-component-communication-map.md`

And uses `common-ai-mistakes.md` as a hub, not as the full teaching surface.

---

## 17. Visual Map Of The Whole System

```text
Authoritative OpenWrt Reality
  |- upstream code
  |- corpus docs
  |- archive evidence
  |- cookbook corpus
  `- frozen golden key

        |
        v

Test Inspiration
  |- uncovered cookbook gap
  |- observed blind failure
  |- migration boundary
  |- archive confusion
  `- future skill need

        |
        v

Scenario Design
  |- blind prompt
  |- metadata record
  `- expected paradigms + falsenesses

        |
        v

Blind Run + Score
  |- pass
  `- fail -> failure family

        |
        v

Failure Family Registry
  |- reject
  |- golden-key-only
  |- extend existing page
  `- new page

        |
        v

Cookbook Remediation
  |- author or revise page
  |- update hub links
  `- schedule verification rerun

        |
        v

Retest / Benchmark / Future Skill Extraction
```

---

## 18. What This Center Copies And Why

This center physically copies only the minimum artifact set needed for reproducible reruns:

- `artifacts/test-pack/00-batch-prompts.md`
- `artifacts/test-pack/02-metadata-catalog.json`
- `artifacts/test-pack/03-golden-answers-key.md`

Everything else is summarized or referenced.

Reason:

- copied artifacts provide a stable rerun packet
- summarized docs prevent another scattered planning tree
- live references avoid forking the repo's active contracts

---

## 19. Relationship To Existing Cookbook Coverage

The current cookbook corpus is already high quality and broad enough that v14 should not begin by inventing dozens of new topics.

The first v14 priority is to improve system discipline:

- identify true gaps
- retire already-served discovery scenarios
- resolve evidence debt
- replace placeholder reviewer ownership
- create a stable promotion pathway from failure to page

This is documented factually in [01-current-cookbook-state-and-gap-map.md](./01-current-cookbook-state-and-gap-map.md).

---

## 20. Relationship To Future OpenWrt Skill / Agent Work

The future skill or agent should not be generated directly from raw scenarios or raw model failures.

It should be generated from stabilized artifacts:

1. cookbook pages
2. the golden answers key
3. the failure-family framework
4. verification results showing which lessons actually changed model behavior

This ensures the later skill inherits validated teaching units rather than unfinished experiment fragments.

---

## 21. First Practical Use Of This Center

The next maintainer using this center should do work in this order:

1. Read this operating plan.
2. Read [01-current-cookbook-state-and-gap-map.md](./01-current-cookbook-state-and-gap-map.md).
3. Use [03-test-generation-contract.md](./03-test-generation-contract.md) to propose or admit any new scenario.
4. Use [04-failure-family-framework.md](./04-failure-family-framework.md) to classify the result.
5. Use [05-promotion-and-review-contract.md](./05-promotion-and-review-contract.md) to decide whether to author, extend, or reject.
6. Use [08-cookbook-authoring-execution-contract.md](./08-cookbook-authoring-execution-contract.md) to author the page and companion log.
7. Use [artifacts/promotion/00-release-candidate-checklist.md](./artifacts/promotion/00-release-candidate-checklist.md) before considering the cookbook work settled.

---

## 22. Immediate V14 Prototype Goals

This prototype is considered useful if it achieves all of the following:

1. another maintainer can explain where new tests should come from
2. another maintainer can tell when one failure is enough to open cookbook work
3. another maintainer can tell whether to create a new page or extend an existing one
4. the copied test-pack artifacts are frozen and easy to find
5. the rationale lives here instead of being spread across v13 notes

---

## 23. Summary

This center changes the cookbook system from a promising experiment into an intentional operating model.

Its central decisions are simple:

- source truth first
- blind tests second
- failure families before page decisions
- one failure is enough to open work
- repeated failures raise priority, not admission
- cookbook pages teach durable OpenWrt decisions, not isolated prompt errors
- future skill extraction comes after cookbook stabilization, not before
