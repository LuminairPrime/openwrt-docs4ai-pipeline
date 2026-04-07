I’m pulling the exact weak spots from the Opus drafts so the improvement list is specific and defensible rather than generic.

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/mission-statement-opus46-v0.md)

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/docs/plans/scoring-pipeline-implementation-opus46-v0.md#1-1), lines 1 to 220

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/docs/plans/scoring-pipeline-implementation-opus46-v0.md#221-221), lines 221 to 484

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/docs/plans/folder-organization-opus46-v0.md#1-1), lines 1 to 260

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/docs/plans/v14/openwrt-cookbook/docs/plans/folder-organization-opus46-v0.md#261-261), lines 261 to 408

The Opus set is already the strongest set. To push it to 10/10, I would tighten consistency, authority boundaries, and migration safety.

**Cross-Document Fixes**
- Unify the canonical results-path story. mission-statement-opus46-v0.md says new outputs live under the results tree, while scoring-pipeline-implementation-opus46-v0.md launches the scorer against the runs tree. A 10/10 set should pick one canonical input shape and explain how legacy runs are adapted.
- Reconcile the admission threshold for documentation work. mission-statement-opus46-v0.md is failure-first, which reads as “one real blind miss is enough to matter,” but scoring-pipeline-implementation-opus46-v0.md suggests a minimum-two-failures rule for doc tasks. Those rules should not disagree.
- Use one status convention for current, planned, and backlog artifacts. mission-statement-opus46-v0.md handles planned files well, but folder-organization-opus46-v0.md mixes immediate structural changes with speculative future docs. A 10/10 set would tag each proposal as current, next-step, or backlog.

**Mission Statement**
- Add a short non-goals section after mission-statement-opus46-v0.md. It should explicitly say this is not a general OpenWrt handbook, not a replacement for the parent pipeline, and not a no-human-review publishing path.
- Add a truth-hierarchy section near mission-statement-opus46-v0.md. The file strongly says source-backed, but it never ranks authority sources. A 10/10 version would state upstream code first, official docs second, scenario packets and keys third, archived evidence next, AI outputs last.
- Replace the proof claim in mission-statement-opus46-v0.md with a small evidence subsection that points to the exact validation artifact or run showing v14 outperforming v13.
- Add a compact human-versus-AI responsibility matrix keyed to mission-statement-opus46-v0.md. Right now it says human-in-the-loop, but operators still need a one-screen view of which steps are human judgment, AI execution, or joint review.
- Tighten the folder inventory in mission-statement-opus46-v0.md by adding a status column. That would make planned docs like 11 and 12, plus the canonical mission-statement promotion, impossible to misread as already live.
- Add a short success-criteria section after mission-statement-opus46-v0.md. A 10/10 mission statement should define what “pipeline works” means: blind failure captured, source-backed lesson authored, staged draft reviewed, promoted page lands in static/cookbook-source, and a retest shows measurable improvement.

**Scoring Plan**
- Tighten the authority model in scoring-pipeline-implementation-opus46-v0.md. The current plan lets Allowed Variants come from cookbook corpus and prior scoring runs. That is too permissive. A 10/10 version would say correctness comes from scenario packets, upstream code, official docs, and explicit key improvements, not prior model behavior.
- Fix the primary-answer rule wording in scoring-pipeline-implementation-opus46-v0.md. The gate diagram compresses the rule to “first code block,” but the assessment logic is broader: first complete code block or first primary actionable explanation. The plan should handle prose-only answers, mixed prose-plus-code answers, and explicitly labeled anti-pattern examples.
- Add a key-to-scenario synchronization step. Rewriting only the tests-keys files in scoring-pipeline-implementation-opus46-v0.md risks drift if scenario packets or manifests carry overlapping truth claims.
- Delay hard archival until one v4 dry run succeeds. scoring-pipeline-implementation-opus46-v0.md archives the v2 assets immediately. Safer would be deprecate first, validate v4 on one historical batch, then archive.
- Make verification less generic in scoring-pipeline-implementation-opus46-v0.md. A 10/10 version would require replaying at least the known bad patterns from the assessment, especially the hallucination case, primary-answer ambiguity, and fabricated API case.
- Fix the scorer launch template in scoring-pipeline-implementation-opus46-v0.md so it matches the actual canonical results layout and the organization plan’s “results is canonical, runs is legacy” stance.
- Reconcile the synthesis threshold in scoring-pipeline-implementation-opus46-v0.md. “Minimum 2 failures to warrant a DOC task” is a policy choice, not a mitigation, and it conflicts with failure-first unless you explicitly separate admission from prioritization.
- Split the huge inline schemas and templates into main-path plan content plus appendices or companion stubs. The document is excellent but slightly too dense. A 10/10 version would be easier to diff and execute if the operational plan stayed lean and reusable schemas lived in appendices.

**Organization Plan**
- Split the plan into two tracks: minimum viable reorganization and future expansion. folder-organization-opus46-v0.md currently mixes structural cleanup with speculative new prompts and guides. A 10/10 plan would clearly separate must-do cleanup from backlog authoring work.
- Reclassify the authoring-to-staging rename in folder-organization-opus46-v0.md. Calling that low risk understates how many references it touches across contracts and staged artifact docs. It should be medium risk and gated on same-pass reference repair.
- Give the mission drafts a cleaner archive home. In folder-organization-opus46-v0.md, moving them straight into the live plans directory preserves them but also clutters the active plans area. A 10/10 version would likely use a history or archive subfolder.
- Add a grep-backed impact inventory before renames and moves. folder-organization-opus46-v0.md is useful, but the plan would be stronger if it first enumerated every file currently referencing authoring, development prompts, or the old contract names.
- Make latest_cookbook_staging.json a provisional integration decision rather than an assumed deliverable. The idea in folder-organization-opus46-v0.md is plausible, but a 10/10 plan would either tie it to parent-pipeline conventions or explicitly mark it as pending an integration decision.
- Separate prompt centralization from prompt invention. The prompts folder in folder-organization-opus46-v0.md is strong, but net-new prompts like cookbook authoring, veracity check, and do’s-and-don’ts upgrade should be staged as later deliverables unless the plan can show they are already operationally required.
- Add post-migration proof steps. After folder-organization-opus46-v0.md, a 10/10 plan should require one operator-journey test, one internal-link sweep, one old-path sweep, and one promotion-path verification to static/cookbook-source.

1. I can compress this into a high-impact shortlist of the top 5 changes across all three Opus files.
2. I can turn this into a side-by-side “current wording vs 10/10 wording” edit brief for each Opus file without modifying anything.