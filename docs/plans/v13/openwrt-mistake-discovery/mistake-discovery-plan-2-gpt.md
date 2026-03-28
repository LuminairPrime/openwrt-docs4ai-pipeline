# Final Plan: Mistake Discovery to Cited Cookbook Authoring

## Status
Proposed (2026-03-27)

## Purpose

Turn OpenWrt mailing-list archives, forum patterns, bug reports, and upstream fixes into a repeatable research workflow that produces:

1. a ranked list of real OpenWrt programming mistakes and failure scenarios
2. verified positive examples from actual OpenWrt source repositories
3. hand-authored cookbook files in `content/cookbook-source/`

This plan treats mistake discovery as a documentation research sub-project, not as a permanent pipeline stage. The existing cookbook pipeline already works: authored markdown in `content/cookbook-source/` is ingested by `02i`, normalized by `03`, and shipped into the final release-tree. The new work is the research and authoring process that creates better cookbook source files.

## Review Outcome

The existing opus plan is strong on parsing, threading, scoring, and provenance. The key changes in this final plan are:

1. generated mailing-list analysis artifacts are temporary research outputs, not first-class pipeline outputs
2. human-curated lesson selection is a mandatory gate before cookbook drafting
3. all final cookbooks stay in one canonical directory: `content/cookbook-source/`
4. cookbook examples must cite exact upstream web URLs and the date they were read
5. no new production pipeline stage is required for mistake mining
6. `data/override/` is not the right home for cookbooks because it stores AI-summary overrides, not authored corpus pages

## Core Decisions

### Decision 1: Keep cookbook source in one place

All cookbook pages remain in:

```text
content/cookbook-source/
```

Reasoning:

- the cookbooks are high-signal onboarding material for AI tools and human readers
- cookbook value is task-oriented, not repo-oriented; a page about shell quoting or `for` loops should be easy to find regardless of which repo supplied the example
- the existing `02i-ingest-cookbook.py` contract already expects markdown files in this directory

### Decision 2: Do not use `data/override/`

`data/override/` is for JSON overrides of AI-generated summaries. It is not a document source tree, it is not human-readable corpus content, and it does not participate in the cookbook ingest flow. Cookbook files should therefore not live there.

### Decision 3: Separate transient research outputs from persistent authored outputs

Use three storage zones:

```text
docs/plans/v13/openwrt-mistake-discovery/
  mistake-discovery-plan-1-opus.md
  mistake-discovery-plan-2-gpt.md
  OpenWrt_Archives/
  OpenWrt_Archives_Processed_Small/
  readme.md
  scrape-openwrt-mailing-list.ps1
  research-log.md                 <- persistent human notes, prompts, search logs
  shortlist.md                    <- persistent curated lesson shortlist
                                <- generated processed outputs live next to raw archives
                                <- and can be deleted and rebuilt from source archives

content/cookbook-source/
  *.md                           <- final authored cookbooks only
```

Reasoning:

- raw archives and planning material are part of the project history
- processed mining outputs should sit beside the raw archive set they were derived from, making review and re-runs easier
- processed mining outputs are still generated artifacts and can be deleted and rebuilt; they are research outputs, not release-tree inputs
- final cookbook pages are durable curated corpus content and belong in the cookbook source directory

### Decision 4: Human review is mandatory between mining and authoring

The research pipeline can surface candidate mistakes and threads, but it cannot be allowed to auto-publish cookbook lessons. A human must confirm that each lesson is:

- actually about OpenWrt development rather than unrelated infrastructure noise
- important enough to deserve cookbook treatment
- paired with a positive example that reflects current OpenWrt practice

## End-to-End Workflow

The work proceeds in five phases.

### Phase 0: Setup and Scope Lock

#### Goal

Define the source set, the initial mistake categories, and the success criteria before mining begins.

#### Inputs

- mailing-list archives in `docs/plans/v13/openwrt-mistake-discovery/OpenWrt_Archives/`
- the current cookbook source directory
- upstream repos already used by the pipeline: `openwrt`, `packages`, `luci`, `ucode`, and other directly relevant repos

#### Outputs

- a short research log entry recording the archive set, date range, and chosen categories
- an explicit target list of cookbook pages to create or revise

#### Initial category set

- shell and BusyBox/ash pitfalls
- UCI read/write and transaction mistakes
- procd service lifecycle mistakes
- LuCI JS and RPC/ACL wiring mistakes
- hotplug and event-handler mistakes
- build-system and package Makefile mistakes
- networking and firewall misconfiguration patterns
- C-language and embedded-systems mistakes relevant to OpenWrt code
- ucode-specific mistakes

#### Acceptance criteria

- source directories are fixed for the run
- category vocabulary is frozen for the first mining pass
- success is defined as curated cookbook-ready lessons, not just mined thread counts

### Phase 1: Automated Mistake Mining

#### Goal

Reduce the mailing-list corpus to a smaller, searchable lesson-candidate dataset without losing thread context.

#### Implementation guidance

Use the strongest parts of the opus plan unchanged in principle:

1. parse and normalize messages
2. preserve enough quoted and diff context to understand corrections
3. reconstruct threads globally before thread-level filtering
4. score threads for lesson potential
5. emit machine-readable lesson candidates with provenance

The opus plan's revised structure is the correct baseline:

```text
Stage 1A: Parse + Normalize + Hard Junk Exclusion
Stage 1B: Global Thread Reconstruction
Stage 2:  Thread-Level Scoring + Filtering
Stage 3:  Lesson Candidate Extraction
Stage 4:  Finalize + Index
```

#### Output location

All generated outputs go under:

```text
docs/plans/v13/openwrt-mistake-discovery/OpenWrt_Archives_Processed_Small/
```

Suggested layout:

```text
docs/plans/v13/openwrt-mistake-discovery/OpenWrt_Archives_Processed_Small/
  parsed/
  threaded/
  scored/
  lessons/
  reports/
```

#### Execution-critical safeguards

The following safeguards from the opus plan are required, not optional. Without them the first run is likely to fail, lose context, or produce misleading candidates.

1. Use a PowerShell-native parser rather than Python `mailbox.mbox()`.
  Reason: the archive format uses Mailman-style `From user at domain` separators and obfuscated addresses that are a poor fit for naive mbox tooling.
2. Split messages with a boundary matcher based on `Regex.Matches`, not a simple `Split`.
  Reason: this preserves byte offsets for provenance and handles variable spacing in the `From ` separator lines more safely.
3. Thread globally before filtering.
  Reason: month-spanning threads will be orphaned if files are processed independently or if message-level keyword filters run before threading.
4. Keep three body views per message when practical.
  Reason: scoring wants aggressively cleaned text, while lesson extraction needs quoted context and diff summaries.
  Minimum set:
  - `body_for_scoring`: quotes and bulky diff content removed
  - `body_no_diff`: prose retained with minimal diff stripping
  - `quoted_context_pairs`: extracted quote-plus-correction pairs when present
5. Summarize diffs instead of discarding them blindly.
  Reason: file paths, hunk headers, and a few changed lines often contain the only clue to the actual fix.
6. Do not hard-drop short messages only because they are short.
  Reason: terse review replies like `NACK - leaks memory` may be high-value signals.
7. Escape regex patterns carefully.
  Reason: unescaped `.` in phrases like `use.after.free` creates noisy false positives.
8. Parse dates with a tolerant helper and preserve the original date string.
  Reason: mailing-list dates are inconsistent and should not crash thread sorting.
9. Decode MIME headers and quoted-printable or multipart bodies.
  Reason: encoded subjects and bodies are common enough that skipping this will silently destroy signal.
10. Emit `stats.json` and `samples.md` at each stage.
  Reason: the mining workflow needs QA checkpoints, otherwise errors will only show up much later during lesson review.
11. Separate `dropped` from `sidelined` content.
  Reason: `[VOTE]`, CI, and process-heavy threads may be low priority without being pure noise.
12. Track lesson completeness separately from lesson score.
  Reason: a strong problem statement with no fix in the archive is still useful if the codebase can supply the correct example.

#### Required output artifacts

- `threads-passing.jsonl`
- `lesson_candidates.jsonl`
- `stats.json` per stage
- `samples.md` per stage
- a human-readable ranked report of candidate lessons

Recommended additional artifacts:

- `messages-primary.jsonl`
- `messages-sidelined.jsonl`
- `messages-dropped.jsonl`
- `threads-scored.jsonl`
- `top_lessons.jsonl`
- `codebase-search-guide.md`

#### Automation suitability

This phase is highly automatable and can be executed well by the agent.

#### Acceptance criteria

- thread reconstruction happens before thread-level filtering
- every lesson candidate links back to the original archive file and message ID
- month-spanning threads are reconstructed correctly from the full processed message set
- encoded headers and quoted-printable bodies do not break parsing
- the final candidate list is small enough for human review

### Phase 2: Human Curation and Lesson Selection

#### Goal

Turn the mined candidate list into a smaller set of cookbook-worthy scenarios.

#### What the agent can do well

- cluster similar mistakes
- rank candidates by frequency, severity, and teachability
- produce a deduplicated shortlist
- highlight which lessons already overlap existing cookbooks

#### What is best done manually by you

- deciding which lessons are strategically important for the cookbook module
- rejecting topics that are too obscure, too stale, or too repo-specific
- reviewing borderline forum or mailing-list cases where domain judgment matters more than text mining

#### Curation rubric

Keep a lesson if it meets most of these:

- appears multiple times across mailing list, forum, issue, or commit history
- has a clear "what went wrong" statement
- has a current positive example available in upstream code
- teaches a transferable OpenWrt pattern rather than a one-off patch quirk
- fits the cookbook boundary: task-oriented, actionable, and current-era

#### Persistent artifacts

Record the curated shortlist in:

```text
docs/plans/v13/openwrt-mistake-discovery/shortlist.md
```

Each shortlisted lesson should include:

- working title
- category
- why it matters
- source thread URL or archive locator
- target upstream repo(s) for positive-example mining
- whether it maps to a new cookbook or a revision of an existing one

#### Acceptance criteria

- every shortlisted lesson has a clear cookbook destination
- duplicate lessons are merged
- existing cookbook overlap is called out explicitly

### Phase 3: Positive Example Mining from Upstream Source

#### Goal

For each shortlisted mistake, find real OpenWrt code that demonstrates the correct pattern.

#### Search order

Search the actual source repos in this order:

1. `openwrt/openwrt`
2. `openwrt/packages`
3. `openwrt/luci`
4. `jow-/ucode` or the current authoritative ucode source used by this repo
5. other directly relevant OpenWrt repos only when needed

#### Preferred evidence types

1. current code on the default branch, pinned to a commit SHA when cited
2. merged fixes that demonstrate the correct replacement of a known bad pattern
3. well-established helper functions or canonical implementations used repeatedly in the tree

#### Required evidence contract for each example

Every positive example collected for cookbook authoring must record:

- exact web URL to the source file or commit
- pinned commit SHA where possible
- exact path and line range
- date read
- short explanation of why this snippet is the positive example

Recommended evidence record format:

```text
Topic: Shell quoting in init scripts
Pattern: Quote variable expansions in test expressions and command arguments
Source URL: https://github.com/openwrt/openwrt/blob/<sha>/package/network/services/dnsmasq/files/dnsmasq.init#L42-L55
Repo path: package/network/services/dnsmasq/files/dnsmasq.init
Date read: 2026-03-27
Why selected: Canonical procd init script using quoted variables and defensive local assignment
```

#### Automation suitability

This phase is partly automatable.

The agent can do well at:

- searching repos with grep and git history
- extracting candidate snippets
- producing source URL records
- grouping multiple good examples for comparison

Manual review is still valuable for:

- deciding which snippet is most teachable
- rejecting examples that are technically correct but too context-heavy for cookbook use

#### Acceptance criteria

- every shortlisted lesson has at least one positive source example
- URLs are web-resolvable and commit-pinned where feasible
- every example includes a recorded read date

### Phase 4: Cookbook Drafting

#### Goal

Write or revise cookbook markdown pages using the curated problem set and the verified positive examples.

#### Output location

```text
content/cookbook-source/
```

#### Authoring rules

Use the existing cookbook content contract from `03-v13-cookbook-content-spec-2026-03-22.md`.

Each cookbook should:

- solve a concrete task or decision
- explain the mistake pattern and why it fails
- present at least one real positive example from the upstream codebase
- include anti-patterns or WRONG/CORRECT comparisons where useful
- link to related cookbook pages and module reference docs
- record how the page was verified

#### Citation rule

The cookbook page must visibly include the source provenance for its code examples. At minimum, the verification notes section should include:

- exact source URL
- path and line range
- date read

Recommended format inside a cookbook:

```text
Source evidence:
- https://github.com/openwrt/openwrt/blob/<sha>/package/network/services/dnsmasq/files/dnsmasq.init#L42-L55
  Read: 2026-03-27
- https://github.com/openwrt/packages/blob/<sha>/net/example/files/example.init#L10-L28
  Read: 2026-03-27
```

#### New-file versus revise-existing decision

Use this rule:

- revise an existing cookbook if the shortlisted lesson is a major missing section within that topic
- create a new cookbook if the lesson is a standalone task or recurring mistake family that deserves direct discoverability

#### Acceptance criteria

- every cookbook is understandable without opening the archive-mining outputs
- every code example traces to a real upstream source URL and read date
- every page still fits the cookbook, not reference, boundary

### Phase 5: Normal Publishing Through the Existing Pipeline

#### Goal

Ship the finished cookbook pages through the existing documentation pipeline with no special-case runtime dependency on the mistake-mining process.

#### Key rule

The mistake-mining workflow is optional and infrequent. The pipeline must continue to run normally whether or not the mining workflow is rerun in the future.

That means:

- do not add a mandatory production stage that re-mines mailing lists on each pipeline run
- do not make cookbook validity depend on the presence of the archive-mining outputs in `tmp/`
- do not make `02i` or `03` fetch live upstream code to resolve cookbook citations

Cookbook pages are static authored documents. If they become outdated, they are revised like any other documentation page.

#### Acceptance criteria

- the pipeline still ingests cookbook pages exactly as it does today
- deleting the temporary mining outputs does not break release generation
- cookbook content remains durable authored corpus content

## Automation Split: Agent Versus Human

| Task | Agent | Human | Notes |
|---|---|---|---|
| Parse and thread mailing-list archives | Strong fit | Optional spot-check | Highly automatable |
| Score and cluster lesson candidates | Strong fit | Review shortlist | Good automation, but not final authority |
| Search general web for common language mistakes | Strong fit | Optional sanity check | Good for C, shell, Lua, embedded constraints |
| Search OpenWrt issues, commits, and repo history | Strong fit | Review selected lessons | Mechanically strong |
| Browse forums and mailing lists for nuanced, high-signal cases | Partial fit | Best done manually | Human judgment matters more |
| Decide which lessons deserve cookbook pages | Support only | Primary owner | Product and editorial choice |
| Find positive code examples in upstream repos | Strong fit | Review final snippet choice | Agent can gather several options |
| Draft cookbook prose around verified examples | Strong fit | Review accuracy and usefulness | Best with human acceptance gate |
| Final approval to commit cookbook pages | Support only | Primary owner | Editorial sign-off |

## Relationship to Existing Cookbooks

Before drafting any new page, compare the shortlist against the current cookbook inventory in `content/cookbook-source/`.

Expected outcomes:

- some new lessons become new pages
- some new lessons expand `common-ai-mistakes.md`
- some new lessons deepen `uci-read-write-from-ucode.md`, `procd-service-lifecycle.md`, or `luci-form-with-uci.md`

This prevents duplicate pages and keeps the cookbook module coherent.

## Suggested First Wave

The first run should target a small, high-signal set of lessons rather than trying to exhaust the archives.

Recommended first wave:

1. shell quoting and process-control mistakes in init scripts
2. UCI transaction and commit mistakes
3. LuCI JS plus rpcd ACL wiring mistakes
4. hotplug handler guards and event assumptions
5. package Makefile and build-flag mistakes

These are frequent, highly teachable, and map cleanly to the cookbook module.

## Operator Prompt Pack

### Prompt A: Mining pass

```text
Mine the OpenWrt mailing-list archives under docs/plans/v13/openwrt-mistake-discovery/OpenWrt_Archives/.
Write processed outputs under docs/plans/v13/openwrt-mistake-discovery/OpenWrt_Archives_Processed_Small/.
Use a PowerShell-native parser that handles Mailman-style separators, global threading before filtering, MIME decoding, robust date parsing, and per-stage QA artifacts.
Parse messages, reconstruct threads globally before filtering, score threads for lesson potential, and produce a ranked lesson-candidate report.
Preserve provenance to original archive files, message IDs, and thread roots.
Do not write cookbook files yet.
```

### Prompt B: Shortlist curation support

```text
Review the mined lesson candidates and produce a deduplicated shortlist of cookbook-worthy OpenWrt programming mistakes.
Group similar mistakes, rank them by teachability and frequency, identify overlap with existing cookbook pages, and recommend which ones should become new cookbooks versus revisions of current pages.
Do not invent fixes. Keep explicit links back to the mined candidate evidence.
```

### Prompt C: Positive example search

```text
For each shortlisted OpenWrt mistake, search the real upstream source repositories for correct implementations of the same pattern.
Return exact source URLs, commit-pinned links where possible, file paths, line ranges, read dates, and a short reason each snippet is a good positive example.
Prefer current, canonical implementations over obscure one-off fixes.
```

### Prompt D: Cookbook drafting

```text
Draft or revise cookbook markdown files in content/cookbook-source/ using the approved mistake shortlist and the verified positive examples from upstream OpenWrt repositories.
Follow the cookbook content contract already defined in docs/plans/v13/03-v13-cookbook-content-spec-2026-03-22.md.
Include visible source evidence with exact URLs and read dates.
Keep the pages task-oriented and do not turn them into generic reference manuals.
```

## Acceptance Criteria for the Whole Project

The mistake-discovery effort is successful when all of the following are true:

1. a reproducible research workflow exists for shrinking the archive corpus into lesson candidates
2. the workflow produces curated, human-approved lesson scenarios rather than auto-published docs
3. every shipped cookbook example is grounded in real upstream OpenWrt code
4. every shipped cookbook example includes an exact source URL and read date
5. all final cookbook pages live in `content/cookbook-source/`
6. the normal docs pipeline can ingest and ship the new cookbook pages without any new required mining stage

## Recommended Next Action

Implement the mining scripts as a temporary research tool under the mistake-discovery workspace, run a first pass against one archive slice, produce a shortlist, and only then start drafting the first wave of cookbook pages.