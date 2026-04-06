# Test Bank And Grouped Delivery

**Purpose:** Define the cookbook-center test inventory, explain what already exists from the original discovery project, and specify the grouped prompt files and manual result locations for future operator runs.

---

## 1. Why The Test Files Matter

After the cookbooks themselves, the test files are the next most important deliverable in this center.

They serve two separate purposes:

1. **Discovery:** show that an AI fails a blind OpenWrt task badly enough to justify cookbook work
2. **Verification:** show later that an AI given the cookbook can now answer the same task correctly

That means the prompt bank must be stable, reusable, and structured for repeated manual runs across different AI agents.

---

## 2. Original Scenario Bank Already Created

The inherited test bank from the original mistake-discovery project already contains **17 total scenarios**.

### Existing grouped batch files

| Batch | File | Scenario count | Scenario IDs |
| --- | --- | --- | --- |
| Alpha | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01a-batch-alpha.md` | 6 | S01, S05, S07, S10, S13, S16 |
| Beta | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01b-batch-beta.md` | 6 | S02, S04, S08, S11, S12, S17 |
| Gamma | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01c-batch-gamma.md` | 5 | S03, S06, S09, S14, S15 |

### Existing supporting files

| File | Purpose |
| --- | --- |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/00-batch-prompts.md` | Combined prompt inventory |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/02-metadata-catalog.json` | Scenario categories, intent, expected paradigms |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/03-golden-answers-key.md` | Frozen key truth surface |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01a-batch-alpha-key-sonnet46.md` | Alpha slice answer key |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01b-batch-beta-key-sonnet46.md` | Beta slice answer key |

The important naming lesson from v13 is that grouped question files and grouped answer keys live side-by-side and use mirrored names.

### Important interpretation

The cookbook center did **not** need to invent a net-new baseline bank from zero. The original project already produced the core question inventory and grouped-slice pattern.

---

## 3. New Tests Created In The Cookbook Center

### 3.1 Net-new scenario questions created so far

**Ten.**

The v14 center now extends the inherited 17-scenario bank with **10 source-backed scenario concepts**, numbered `Scenario 18` through `Scenario 27` in the v14 metadata catalog.

| Scenario | Focus |
| --- | --- |
| Scenario 18 | LuCI JS async `load()` plus `render()` lifecycle with `rpc.declare()` |
| Scenario 19 | hotplug guarded structured ubus forwarding |
| Scenario 20 | `/etc/uci-defaults/` mutation-only firstboot contract |
| Scenario 21 | `ucidef_*` helper boundary for board defaults |
| Scenario 22 | combined C `blobmsg_parse()` plus nested reply |
| Scenario 23 | OpenWrt runtime package install layout |
| Scenario 24 | rpcd ACL JSON install-path and permission contract |
| Scenario 25 | shell config-helper API boundary |
| Scenario 26 | native shell `jshn` JSON navigation |
| Scenario 27 | LuCI/runtime `network.interface dump` state-shape extraction |

### 3.2 New cookbook-center test deliverables created so far

The v14 center now carries a **27-scenario full master pack**, **14 admitted scenario packets**, and **9 grouped operator prompt files** for full-pack manual execution.

The four admitted packet targets are:

| Focused target | Packet | Origin |
| --- | --- | --- |
| `uci_load_validate` validation boundary | `artifacts/scenario-packets/04-scn-2026-004-procd-uci-load-validate-loglevel.yaml` | existing Scenario 06 as primary verification target; Scenario 01 as secondary umbrella target |
| C daemon init order / `ubus_add_uloop()` | `artifacts/scenario-packets/03-scn-2026-003-c-libubus-daemon-skeleton.yaml` | existing Scenario 12 |
| native ucode file IO + JSON | `artifacts/scenario-packets/02-scn-2026-002-ucode-native-json-file-read.yaml` | existing Scenario 13 |
| async ucode process streaming | `artifacts/scenario-packets/01-scn-2026-001-ucode-async-ping-streams.yaml` | existing Scenario 16 |

These are not new conceptual questions. They are focused cookbook-center rerun targets distilled from the original bank.

The newly added net-new packet targets are:

| Focused target | Packet |
| --- | --- |
| LuCI async load/render status form | `artifacts/scenario-packets/05-scn-2026-005-luci-load-render-rpc-status.yaml` |
| hotplug structured ubus forward | `artifacts/scenario-packets/06-scn-2026-006-hotplug-json-forward-ubus.yaml` |
| firstboot mutation-only `uci-defaults` | `artifacts/scenario-packets/07-scn-2026-007-uci-defaults-mutation-not-initd.yaml` |
| `ucidef_*` helper WAN defaults | `artifacts/scenario-packets/08-scn-2026-008-ucidef-helper-wan-pppoe.yaml` |
| C blobmsg parse plus nested reply | `artifacts/scenario-packets/09-scn-2026-009-c-blobmsg-parse-nested-reply.yaml` |
| package install runtime layout | `artifacts/scenario-packets/10-scn-2026-010-package-install-luci-rpcd-bootstrap.yaml` |

---

## 4. Grouped Prompt Rule

The grouped prompt file is the manual execution surface for AI-agent testing.

Grouped headers must carry an explicit execution contract that works for both web or
chat agents and local IDE or CLI agents. Use
`artifacts/templates/00-batch-prompt-header-template.md` as the reusable source for
that contract.

Do **not** deliver all focused scenarios in one giant prompt by default. The operator should avoid giving one model a long sequence of related tasks where answering the first one teaches it how to answer the next similar one.

### Default grouped-batch rule

- one question per domain/category/type per grouped batch wherever practical
- if two questions are architecturally adjacent enough that success on one would hint the answer path for the other, split them
- operator convenience carries real weight too, so fewer larger batches are preferred when the answer paths remain clearly non-adjacent

This is why the rerun layout is now periodically remapped instead of only growing by append-only micro-slices.

---

## 5. New Grouped Prompt Files To Run Manually

These are the new operator-facing grouped files created by the v14 center.

| Group | File | Scenarios inside | Why grouped this way |
| --- | --- | --- | --- |
| Alpha | `artifacts/test-groups/01a-batch-alpha.md` | S01, S03, S04 | one procd service boundary, one C ubus plugin boundary, and one modern LuCI JS form boundary |
| Beta | `artifacts/test-groups/01b-batch-beta.md` | S02, S06, S09 | mixes native ucode ubus access, procd validation, and hotplug shell handling |
| Gamma | `artifacts/test-groups/01c-batch-gamma.md` | S07, S05, S10 | separates C ubus reply construction, LuCI live-status rendering, and firstboot mutation |
| Delta | `artifacts/test-groups/01d-batch-delta.md` | S08, S11, S12 | keeps ucode UCI mutation, buildroot package boilerplate, and standalone C ubus runtime setup apart |
| Epsilon | `artifacts/test-groups/01e-batch-epsilon.md` | S13, S14, S19 | pairs native ucode fs/json, LuCI menu JSON, and guarded hotplug ubus forwarding |
| Zeta | `artifacts/test-groups/01f-batch-zeta.md` | S15, S18, S20 | combines blobmsg C parsing, LuCI async status lifecycle, and mutation-only `uci-defaults` |
| Eta | `artifacts/test-groups/01g-batch-eta.md` | S16, S21, S23 | groups async ucode process handling with `ucidef_*` helpers and package install layout |
| Theta | `artifacts/test-groups/01h-batch-theta.md` | S22, S24, S25 | keeps advanced C parse/reply, rpcd ACL permissions, and shell config helpers distinct |
| Iota | `artifacts/test-groups/01i-batch-iota.md` | S26, S27, S17 | ends with shell `jshn`, LuCI runtime-state extraction, and the diagnostic check kept last |

### Mirrored grouped answer keys

| Group | Answer key file |
| --- | --- |
| Alpha | `artifacts/test-groups/01a-batch-alpha-key.md` |
| Beta | `artifacts/test-groups/01b-batch-beta-key.md` |
| Gamma | `artifacts/test-groups/01c-batch-gamma-key.md` |
| Delta | `artifacts/test-groups/01d-batch-delta-key.md` |
| Epsilon | `artifacts/test-groups/01e-batch-epsilon-key.md` |
| Zeta | `artifacts/test-groups/01f-batch-zeta-key.md` |
| Eta | `artifacts/test-groups/01g-batch-eta-key.md` |
| Theta | `artifacts/test-groups/01h-batch-theta-key.md` |
| Iota | `artifacts/test-groups/01i-batch-iota-key.md` |

The v14 rule is now the same as the old system: grouped prompt files and grouped answer keys should be named similarly and stored similarly.

### What you need to manually run now

You now have:

- **14 admitted packets** total
- **10 net-new scenario concepts** beyond the original 17
- **9 grouped prompt files** total

The current grouped manual-run set covers the **full 27-scenario pack** delivered in **9 grouped prompt files** after the balanced alpha-to-iota remap.

---

## 6. File Locations

### Prompt groups

Store grouped manual-run prompt files here:

```text
docs/plans/v14/openwrt-cookbook/artifacts/test-groups/
```

Store the mirrored grouped answer keys in the same directory.

### Scenario packets

Store admitted machine-readable packets here:

```text
docs/plans/v14/openwrt-cookbook/artifacts/scenario-packets/
```

### Manual AI-agent results

Store manual run outputs here:

```text
docs/plans/v14/openwrt-cookbook/artifacts/results/
```

---

## 7. Result Layout Per AI Agent

Each tested AI agent should get its own results subtree.

Each **run label** is one test-administration iteration for one target AI agent. Use a new run label every time the human starts a new agent-specific sweep so raw outputs, scoring, and later evaluator notes cannot overwrite earlier iterations.

### Recommended path shape

```text
artifacts/results/<agent-label>/<run-label>/<group-name>/
```

Example:

```text
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/alpha/
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/zeta/
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/iota/
```

### Expected files inside each group result folder

| File | Purpose |
| --- | --- |
| `00-prompt-source.txt` | Which grouped prompt file was used |
| `00-key-source.txt` | Which mirrored grouped answer key was used |
| `01-raw-response.md` | The agent's unedited raw answer |
| `02-manual-score.md` | Human-accepted final score for this group in this run |
| `03-operator-notes.md` | Ambiguities, partial success notes, and follow-up observations |
| `evaluations/<evaluator-label>/...` | Optional provisional or alternate AI-assisted evaluation artifacts for this same raw response |

### Expected files at the run root

| File | Purpose |
| --- | --- |
| `00-run-manifest.yaml` | Agent name, model, operator, date, groups run |
| `summary.md` | Cross-group human summary for that run |

### Evaluator output placement

If a separate AI agent is used to help review or score a run, do **not** let that provisional output overwrite the canonical group score file immediately.

Use this path shape first:

```text
artifacts/results/<target-agent-label>/<run-label>/<group-name>/evaluations/<evaluator-label>/
```

Inside that evaluator subfolder, the reviewing AI may write its own draft scoring and notes.
Only the human-accepted final evaluation should live at the canonical top-level path:

```text
artifacts/results/<target-agent-label>/<run-label>/<group-name>/02-manual-score.md
```

This keeps repeated evaluator passes from colliding while preserving one authoritative per-group score file.

### Canonical naming rule for new v14 runs

For all new v14 cookbook-center runs, the score artifact is always named:

```text
02-manual-score.md
```

Do not create new timestamp-suffixed score filenames for v14 runs. Put the scoring date, run label,
agent/model identity, and verdict details inside `00-run-manifest.yaml` and `02-manual-score.md`.

Historical v13 imports may still reference timestamp-suffixed score files, but those are legacy inputs,
not the naming model for new v14 result bundles.

The canonical filename does **not** mean there is only one evaluator pass forever. It means each run has one final accepted score file per group. Draft or alternate evaluator passes belong under `evaluations/<evaluator-label>/` until the human accepts one.

### Canonical file forms

Use these templates when creating a new result bundle:

- `artifacts/results/_template/00-run-manifest.yaml`
- `artifacts/results/_template/summary.md`
- `artifacts/results/_template/00-prompt-source.txt`
- `artifacts/results/_template/00-key-source.txt`
- `artifacts/results/_template/02-manual-score.md`
- `artifacts/results/_template/03-operator-notes.md`

`01-raw-response.md` is the only intentionally untemplated artifact because it must preserve the agent output exactly as received.

---

## 8. Manual Execution Workflow

1. Choose the grouped prompt file in `artifacts/test-groups/`
2. Run that exact prompt against one target AI agent in a fresh isolated session dedicated to that single group
3. Preserve the raw answer under the agent's results subtree:
	- if the target is a local IDE or CLI agent with file-write access, let it write directly to the canonical `01-raw-response.md` path for that run and group
	- if the target is a web or chat agent without file-write access, copy the response into that file immediately after the run
4. Score it manually against the mirrored grouped answer key plus the source truth packet and cookbook expectations
5. Record whether the scenario stays in discovery, moves to cookbook candidate open, or is used as verification-only evidence

### Iterative administration across multiple target agents

The cookbook subpipeline may be run in iterations.

Example:

- Iteration 1: run the grouped bank against AI agent A and accept any blind failing scenarios into cookbook construction
- Iteration 2: run the bank, or a reduced bank, against AI agent B to find different failures

Once a scenario has already produced one accepted blind failure, the human operator has two supported choices for later iterations:

1. **Reduced-follow-on mode**
	Do not run that already-accepted failing scenario again if the only goal is to keep finding new missing lessons.

2. **Full-rerun mode**
	Still run the scenario again, because another model may fail differently and provide additional cookbook-relevant learning.

Both are valid. One fail is sufficient for acceptance, but duplicate failures can still be worth collecting.

### Duplicate-failure review policy

If a later iteration repeats a scenario that was already accepted from an earlier iteration, the reviewing AI or human reviewer may choose either of these review modes:

- **Full review:** score the duplicate normally because it may contain different falsenesses or a more instructive failure shape
- **Short duplicate review:** record that the failure is materially the same as an already accepted failure and reference the earlier accepted score instead of redoing a full writeup

If the human skips a previously accepted scenario in a later iteration, record that skip in the run manifest rather than editing the canonical grouped prompt files themselves.

If the human reruns the duplicate and the evaluator chooses to skip full scoring, still leave a short note or short score record in the current run so later readers understand why the group was not fully rescored.

The important rule is conversational isolation. Do not run Delta, Epsilon, and Zeta as one continuous mega-prompt if that would let the agent learn from earlier answers.

---

## 9. Machine-Readable Group Inventory

The grouped prompt layout is also represented in:

- [artifacts/test-groups/02-grouped-run-manifest.yaml](./artifacts/test-groups/02-grouped-run-manifest.yaml)

Use that file as the machine-readable grouping contract and this document as the human-readable operator explanation.

The manifest owns:

- group names and grouped file pairings
- scenario membership inside each group
- grouping rationale and category mix

The manifest does **not** own the shared execution-contract header text that appears at the top
of the grouped prompt files. That shared header is governed by
[artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md).

### 9A. Manual grouped-prompt refresh procedure

There is currently no dedicated grouped-prompt regeneration script documented or implemented in
this repository. Until such a script exists, refresh grouped prompt files manually in this order:

1. update [artifacts/test-groups/02-grouped-run-manifest.yaml](./artifacts/test-groups/02-grouped-run-manifest.yaml) first so the machine-readable group membership is correct
2. create or refresh the grouped prompt file header from [artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md)
3. vary only the batch-specific parts of that header, such as the group name, example scenario labels, and canonical `01-raw-response.md` path for that group
4. place the scenario bodies in the intended order without changing the shared clean-room, session-isolation, or output-routing contract ad hoc
5. confirm the paired key file and grouped-run manifest still point to the same group file names after the refresh
6. if the remap changes the operator-facing grouped layout, update the grouped tables and examples in this document as part of the same change

That procedure keeps the grouping contract, shared header contract, and operator docs synchronized even while grouped prompt refresh remains manual.

---

## 10. Plan To Create More Unique Tests

The plan is **not** to browse random snippets and then reverse-engineer prompts from whatever looks interesting.

The plan is to mine source-backed OpenWrt boundaries systematically and only admit a new scenario when all four conditions hold:

1. the snippet teaches a real OpenWrt-specific contract
2. the contract is easy for blind AI agents to miss or hallucinate
3. the task can be scored with a binary pass rule
4. the scenario adds a genuinely new boundary instead of duplicating an existing family

### Preferred source order

1. current local upstream clones already present under `tmp/authoring-repos/`
2. condensed corpus output under `openwrt-condensed-docs-renamed/`
3. current authored cookbook gap map and family registry
4. only then fresh upstream fetching if a required repo surface is missing locally

### Candidate mining workflow

1. scan current OpenWrt source and condensed docs for compact canonical examples
2. identify the boundary the snippet proves
3. check whether that boundary already exists in the 17-scenario bank or current family registry
4. if unique, create a scenario packet first
5. then create a canonical answer key from the same authority source
6. only after that, place the scenario into a grouped prompt batch that does not contaminate adjacent questions

This workflow is documented in more detail in [07-test-expansion-and-key-sourcing-plan.md](./07-test-expansion-and-key-sourcing-plan.md).
