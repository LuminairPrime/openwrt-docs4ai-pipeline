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
| Alpha | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01a-batch-slice-alpha.md` | 6 | S01, S05, S07, S10, S13, S16 |
| Beta | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01b-batch-slice-beta.md` | 6 | S02, S04, S08, S11, S12, S17 |
| Gamma | `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01c-batch-slice-gamma.md` | 5 | S03, S06, S09, S14, S15 |

### Existing supporting files

| File | Purpose |
| --- | --- |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/00-batch-prompts.md` | Combined prompt inventory |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/02-metadata-catalog.json` | Scenario categories, intent, expected paradigms |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/03-golden-answers-key.md` | Frozen answer-key truth surface |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01a-batch-slice-alpha-answer-key-sonnet46.md` | Alpha slice answer key |
| `docs/plans/v13/openwrt-mistake-discovery/ai-defect-discovery-pipeline/scenarios/01b-batch-slice-beta-answer-key-sonnet46.md` | Beta slice answer key |

The important naming lesson from v13 is that grouped question files and grouped answer keys live side-by-side and use mirrored names.

### Important interpretation

The cookbook center did **not** need to invent a net-new baseline bank from zero. The original project already produced the core question inventory and grouped-slice pattern.

---

## 3. New Tests Created In The Cookbook Center

### 3.1 Net-new scenario questions created so far

**Six.**

The v14 center now extends the inherited 17-scenario bank with **6 new source-backed scenario concepts**, numbered `Scenario 18` through `Scenario 23` in the v14 metadata catalog.

| Scenario | Focus |
| --- | --- |
| Scenario 18 | LuCI JS async `load()` plus `render()` lifecycle with `rpc.declare()` |
| Scenario 19 | hotplug guarded structured ubus forwarding |
| Scenario 20 | `/etc/uci-defaults/` mutation-only firstboot contract |
| Scenario 21 | `ucidef_*` helper boundary for board defaults |
| Scenario 22 | combined C `blobmsg_parse()` plus nested reply |
| Scenario 23 | OpenWrt runtime package install layout |

### 3.2 New cookbook-center test deliverables created so far

The v14 center has now created **10 admitted scenario packets** total and **8 grouped operator prompt files** total.

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

Do **not** deliver all focused scenarios in one giant prompt by default. The operator should avoid giving one model a long sequence of related tasks where answering the first one teaches it how to answer the next similar one.

### Default grouped-batch rule

- one question per domain/category/type per grouped batch wherever practical
- if two questions are architecturally adjacent enough that success on one would hint the answer path for the other, split them
- manual test efficiency matters, but blindness matters more

This is why the two ucode-heavy rerun targets are isolated into separate grouped prompt files below.

---

## 5. New Grouped Prompt Files To Run Manually

These are the new operator-facing grouped files created by the v14 center.

| Group | File | Scenarios inside | Why grouped this way |
| --- | --- | --- | --- |
| Delta | `artifacts/test-groups/01d-batch-slice-delta.md` | S06, S12 | shell/procd validation and C daemon init order are distinct enough to share a batch |
| Epsilon | `artifacts/test-groups/01e-batch-slice-epsilon.md` | S13 | isolated because native ucode file/JSON handling teaches the ucode runtime boundary directly |
| Zeta | `artifacts/test-groups/01f-batch-slice-zeta.md` | S16 | isolated because solving async ucode streaming can teach later ucode execution patterns |
| Eta | `artifacts/test-groups/01g-batch-slice-eta.md` | S18 | isolated LuCI async lifecycle boundary |
| Theta | `artifacts/test-groups/01h-batch-slice-theta.md` | S19, S23 | intentional cross-domain pair: hotplug runtime and package install layout |
| Iota | `artifacts/test-groups/01i-batch-slice-iota.md` | S20 | isolated `uci-defaults` mutation-only boundary |
| Kappa | `artifacts/test-groups/01j-batch-slice-kappa.md` | S21 | isolated helper-driven board-default boundary |
| Lambda | `artifacts/test-groups/01k-batch-slice-lambda.md` | S22 | isolated native C blobmsg parse/reply boundary |

### Mirrored grouped answer keys

| Group | Answer key file |
| --- | --- |
| Delta | `artifacts/test-groups/01d-batch-slice-delta-answer-key.md` |
| Epsilon | `artifacts/test-groups/01e-batch-slice-epsilon-answer-key.md` |
| Zeta | `artifacts/test-groups/01f-batch-slice-zeta-answer-key.md` |
| Eta | `artifacts/test-groups/01g-batch-slice-eta-answer-key.md` |
| Theta | `artifacts/test-groups/01h-batch-slice-theta-answer-key.md` |
| Iota | `artifacts/test-groups/01i-batch-slice-iota-answer-key.md` |
| Kappa | `artifacts/test-groups/01j-batch-slice-kappa-answer-key.md` |
| Lambda | `artifacts/test-groups/01k-batch-slice-lambda-answer-key.md` |

The v14 rule is now the same as the old system: grouped prompt files and grouped answer keys should be named similarly and stored similarly.

### What you need to manually run now

You now have:

- **10 admitted packets** total
- **6 net-new scenario concepts** beyond the original 17
- **8 grouped prompt files** total

The newly created grouped manual-run set adds **6 new scenarios** delivered in **5 new grouped prompt files**.

---

## 6. File Locations

### Prompt groups

Store grouped manual-run prompt files here:

```text
docs/plans/v14/openwrt-cookbook-project-center/artifacts/test-groups/
```

Store the mirrored grouped answer keys in the same directory.

### Scenario packets

Store admitted machine-readable packets here:

```text
docs/plans/v14/openwrt-cookbook-project-center/artifacts/scenario-packets/
```

### Manual AI-agent results

Store manual run outputs here:

```text
docs/plans/v14/openwrt-cookbook-project-center/artifacts/results/
```

---

## 7. Result Layout Per AI Agent

Each tested AI agent should get its own results subtree.

### Recommended path shape

```text
artifacts/results/<agent-id>/<run-id>/<group-id>/
```

Example:

```text
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/delta/
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/epsilon/
artifacts/results/claude-opus-4-6-thinking/2026-04-05-rerun-01/zeta/
```

### Expected files inside each group result folder

| File | Purpose |
| --- | --- |
| `00-prompt-source.txt` | Which grouped prompt file was used |
| `01-raw-response.md` | The agent's unedited raw answer |
| `02-manual-score.md` | Human scoring against the relevant truth packet |
| `03-operator-notes.md` | Ambiguities, partial success notes, and follow-up observations |

### Expected files at the run root

| File | Purpose |
| --- | --- |
| `00-run-manifest.yaml` | Agent name, model, operator, date, groups run |
| `summary.md` | Cross-group human summary for that run |

---

## 8. Manual Execution Workflow

1. Choose the grouped prompt file in `artifacts/test-groups/`
2. Run that exact prompt against one target AI agent in a clean conversation
3. Save the raw answer under the agent's results subtree
4. Score it manually against the mirrored grouped answer key plus the source truth packet and cookbook expectations
5. Record whether the scenario stays in discovery, moves to cookbook candidate open, or is used as verification-only evidence

The important rule is conversational isolation. Do not run Delta, Epsilon, and Zeta as one continuous mega-prompt if that would let the agent learn from earlier answers.

---

## 9. Machine-Readable Group Inventory

The grouped prompt layout is also represented in:

- [artifacts/test-groups/02-grouped-run-manifest.yaml](./artifacts/test-groups/02-grouped-run-manifest.yaml)

Use that file as the machine-readable grouping contract and this document as the human-readable operator explanation.

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
