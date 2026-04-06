# Test Generation Contract

**Purpose:** Define how future OpenWrt scenarios are selected, designed, admitted, run, and retired for cookbook discovery and later verification.

---

## 1. Fixed Inputs

This v14 prototype treats these as the canonical rerun packet:

- `artifacts/tests-full/full-prompts.md`
- `artifacts/tests-full/metadata-catalog.json`
- `artifacts/tests-full/golden-answers-key.md`

New scenarios may be added later, but every new addition must clear the same admission rules documented here.

This contract covers both scenario creation and grouped prompt delivery. Scenarios are the unit of truth and scoring; grouped prompt files are the unit of manual execution against an AI agent.

---

## 2. Purpose Of A Scenario

A scenario exists to test one bounded OpenWrt lesson in blind form.

It is not meant to:

- survey a whole subsystem at once
- act like a tutorial
- carry internal reasoning about why it exists

That reasoning belongs in the metadata record and the project-center docs, not in the prompt itself.

---

## 3. Where New Test Inspiration Comes From

### 3.1 Allowed inspiration sources

New tests may be inspired by:

1. a blind failure from a model or future skill
2. an uncovered gap in the live cookbook corpus
3. a current upstream OpenWrt pattern or migration boundary
4. a recurring archive or community confusion pattern
5. a missing lesson needed for a planned future OpenWrt skill or agent

However, inspiration alone is not enough to justify cookbook remediation. To create a cookbook
because of a scenario, the operator must still archive a real blind failed answer for that
scenario.

### 3.2 Required source split

Each new scenario must have both:

- **an inspiration source** explaining why the scenario exists
- **an authority source** explaining what the correct answer must do

These are often related, but they are not the same thing.

Example:

- inspiration source: a blind AI failed by using Lua CBI
- authority source: current LuCI JS view code and the live cookbook page for modern LuCI forms

---

## 4. Scenario Admission Rules

Admit a scenario only if all of the following are true.

1. It targets one bounded OpenWrt decision boundary.
2. The expected paradigm can be named concretely.
3. The correct answer can be traced to a live authority source.
4. The prompt can be written blindly.
5. The failure can be classified into a failure family.
6. The lesson is not already redundant with an existing active scenario.

If the scenario is being prepared for cookbook remediation rather than only for benchmark or
coverage purposes, it must also satisfy one of these evidence paths:

- an archived blind failed answer already exists
- a fresh blind run against an unaware agent is scheduled specifically to determine whether the
	scenario actually fails in practice

---

## 5. Scenario Packet Fields

At minimum, every admitted scenario should have or imply these fields.

| Field | Meaning |
| --- | --- |
| Scenario ID | Stable identifier |
| Category | Broad OpenWrt subsystem or pattern area |
| Prompt | Blind user-facing task request |
| Intent | Why this scenario exists |
| Inspiration source | What exposed the need for the test |
| Authority source | What justifies the expected answer |
| Expected paradigms | Minimal must-have patterns |
| Explicit falsenesses | Known wrong paths when applicable |
| Failure family | Deduplication target |
| Discovery status | Candidate, active, open, verification, benchmark-only, retired |
| Cookbook destination | New page, extend page, golden-key-only, reject |

The current v13 metadata catalog already contains part of this structure. Future expansions should preserve backward compatibility with the existing packet where possible.

For new work, use the machine-readable candidate packet at [artifacts/templates/00-scenario-admission-template.yaml](./artifacts/templates/00-scenario-admission-template.yaml).

---

## 6. Prompt-Writing Rules

Every scenario prompt must follow these rules.

1. Use ordinary OpenWrt task language.
2. Do not mention source URLs.
3. Do not say the prompt is a test.
4. Do not include the exact expected API calls in the prompt unless the real-world task would naturally name them.
5. Keep the prompt narrow enough that scoring remains binary.
6. Preserve enough OpenWrt specificity that a generic Linux answer can fail.

## 6A. Grouped Delivery Rules

The same scenario bank may be delivered in different grouped slices depending on operator needs, but the default grouping discipline is:

1. keep only one question from each domain/category/type in a grouped batch wherever practical
2. do not place two adjacent lessons in the same batch if success on one would teach the answer path for the other
3. treat operator administration convenience as half of the grouping priority weight: if a larger batch remains clearly non-adjacent, prefer fewer copy-paste files over needless micro-slices
4. prefer more small batches over one overloaded batch only when the larger prompt would create meaningful cross-question learning effects
5. periodic full remaps of the grouped batch set are allowed when they reduce operator burden without weakening rules 1 and 2
6. keep the grouped prompt files stable enough that later cookbook verification reruns remain comparable
7. run each grouped prompt file in a fresh isolated agent session by default; do not reuse a conversation that has already answered another batch

The purpose of grouping is not just convenience. It protects the blindness of later questions inside the same agent conversation.

When creating a new grouped prompt file or refreshing an existing grouped prompt header, use
[artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md)
as the canonical source for the execution-contract language. Do not hand-rewrite that header
from memory. The grouped prompt files should inherit the same clean-room, session-isolation,
and output-routing contract unless the project center explicitly changes that contract in one
place first.

---

## 7. Criteria Extraction Rules

When designing a new scenario, build the expected paradigm list like this:

1. identify the exact OpenWrt boundary being tested
2. locate the authority source
3. extract the smallest set of required patterns that make the answer structurally correct
4. record only the paradigms needed for binary scoring
5. move broader explanation into cookbook work, not into the metadata packet

Bad pattern list:

- too many tiny implementation details
- stylistic preferences that do not affect structural correctness
- rules derived only from a model failure rather than a source

Good pattern list:

- `USE_PROCD=1`
- `rpc.declare`
- `blobmsg_parse`
- `ubus_add_uloop()`
- `fs.readfile()` and `json()`

---

## 8. Default Discovery Administration

The default cookbook-discovery algorithm is progressive and conservative.

### Step sequence

1. Start with the active discovery queue.
2. Run all active discovery scenarios against the weakest currently viable baseline model.
3. Score every result against the frozen truth packet.
4. For every failure, decide whether it opens cookbook work.
5. Remove accepted cookbook-opening failures from the active discovery queue.
6. Carry forward only the passed scenarios to the next model in discovery mode.

If a scenario has good source backing but no archived failed answer yet, run it first against a
deliberately unaware agent with no repo-doc guidance. If that agent passes, the topic should not
open cookbook remediation work.

### Why this is the default

- the goal is to discover missing lessons efficiently
- one failure is enough to justify cookbook work
- discovery time should not be wasted re-proving already-known gaps

---

## 9. Optional Full-Bank Sweep

A full-bank sweep is also valid.

Use it when:

- the operator wants broader model comparison
- the cost is low enough to justify one sweep
- multiple-model evidence would meaningfully improve priority ranking or family merging

Important: this mode improves prioritization and synthesis, but it does not change the admission rule. One blind failure is still enough to open cookbook work.

---

## 10. Scenario Retirement Rules

### 10.1 Remove from active discovery when

- the failure opened an accepted cookbook candidate
- the scenario has already served its discovery purpose

### 10.2 Keep in verification when

- a cookbook page or page extension is now expected to remediate the lesson

### 10.3 Keep in benchmark-only when

- the scenario is still valuable for profiling later models or a future OpenWrt skill

### 10.4 Retire completely when

- it is redundant with a stronger scenario
- the boundary is no longer current-era relevant
- the scoring logic cannot be kept stable

---

## 11. Discovery Outcomes

Each scored discovery result must resolve to one of these states.

| Result | Meaning |
| --- | --- |
| Pass | Scenario stays active unless retired for another reason |
| Fail, no cookbook work | May become golden-key-only or be rejected |
| Fail, cookbook work opened | Move scenario out of active discovery |
| Fail, duplicate of existing family | Merge into family and do not open duplicate work |

---

## 12. Relationship To Existing Cookbook Coverage

Before opening a new scenario, check whether the lesson is already adequately covered by an existing live page.

If yes, prefer one of these actions instead:

- strengthen the golden key
- tighten the existing cookbook page
- create a verification rerun tied to the existing page

Do not create a new scenario only because a model failed if the lesson is already fully served and the real need is remediation measurement.

---

## 13. Minimal Operator Workflow For A New Test

1. Name the OpenWrt boundary.
2. Record the inspiration source.
3. Record the authority source.
4. Draft a blind prompt.
5. Extract the expected paradigms.
6. Assign a provisional failure family.
7. Check for duplication against current active scenarios.
8. Admit or reject.

If admitted, the scenario enters the candidate or active discovery queue depending on readiness.

The expected output of that workflow is a filled copy of [artifacts/templates/00-scenario-admission-template.yaml](./artifacts/templates/00-scenario-admission-template.yaml).

Admitted real packets should then be stored under `artifacts/scenario-packets/` so the operator can distinguish live candidates from the blank template.

After admission, decide whether the scenario should immediately appear in a batch prompt file under `artifacts/tests-batches/` or remain only as a packet until enough non-overlapping scenarios exist to form a clean batch.
