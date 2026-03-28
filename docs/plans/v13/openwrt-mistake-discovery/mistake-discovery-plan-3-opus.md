

Let me study the existing cookbook infrastructure before writing the plan.   

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/data/override)

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/content/cookbook-source/architecture-overview.md#1-1), lines 1 to 40

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/content/cookbook-source)

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/content/cookbook-source/common-ai-mistakes.md#1-1), lines 1 to 50

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/data/override/README.md#1-1), lines 1 to 30

Searched for text `02i-ingest-cookbook` (`**/*.py`), 1 result

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/content/cookbook-source/common-ai-mistakes.md#50-50), lines 50 to 60

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/.github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py#1-1), lines 1 to 50

Good. Now I have the full picture. Let me read the rest of the ingest script briefly and then write the plan. 

Read [](file:///c%3A/Users/MC/Documents/AirSentinel/openwrt-docs4ai-pipeline/.github/scripts/openwrt-docs4ai-02i-ingest-cookbook.py#50-50), lines 50 to 120

Now I have all the context. Here's the detailed plan:

---

## Plan F — Mistake-Driven Cited Cookbook Upgrade

### What This Is (and Isn't)

This is **not** a pipeline code change. The pipeline already handles cookbooks end-to-end: `content/cookbook-source/*.md` → `02i` ingest → `03` normalize → `05a` assemble → `06` routing indexes → `08` validate. Nothing in scripts needs modification.

This is a **documentation authoring sub-project** — a structured research-and-write effort that produces new `.md` files in cookbook-source. Once placed there, the existing pipeline picks them up automatically on the next run. The effort itself is reproducible from saved prompts and research logs, but is not a recurring pipeline stage.

### Why cookbook-source Is the Right Location (Not override)

| Criterion | cookbook-source | override |
|-----------|--------------------------|-------------------|
| Purpose | Authored documentation files | JSON overrides for AI-generated summaries |
| Format | Markdown with YAML frontmatter | JSON matching base schema |
| Pipeline entry point | `02i` ingest, then full L1→L2→release-tree flow | `04` summary application only |
| Appears in `llms.txt`, `AGENTS.md`, release-tree | Yes — as first-class corpus content | No — overrides are invisible metadata |
| Human-readable standalone | Yes | No |
| Module assignment | `module: cookbook` | Inherits from the file it overrides |

override is for correcting AI summaries, not for authoring documents. Cookbooks are authored, standalone, human-readable reference documents. They belong in cookbook-source, which is already purpose-built for exactly this.

The existing 7 cookbooks (architecture overview, common AI mistakes, era guide, LuCI form, package Makefile, procd lifecycle, UCI read/write) prove the pattern works. This plan adds more using a research-backed methodology.

---

### Phase 1 — Mistake Discovery: Division of Labor

| Research Source | Who Executes | How | Justification |
|----------------|-------------|-----|---------------|
| **Common coding mistakes in C (embedded/BusyBox)** | I automate | Web search for established mistake lists, cross-reference with OpenWrt coding style docs | Well-documented domain; web search yields canonical lists (CERT C, common embedded pitfalls) |
| **Common mistakes in shell scripting (ash/busybox)** | I automate | Web search for BusyBox/ash-specific gotchas, POSIX shell pitfalls | Canonical sources exist (wooledge.org, shellcheck rules) |
| **Common mistakes in Lua** | I automate | Web search for Lua gotchas | Small language, well-documented pitfalls |
| **Common mistakes in ucode** | I automate, you review | Search the ucode repo issues/commits for `fix:` patterns; cross-reference with existing `ucode/` corpus | Niche language — web has less coverage, but the repo itself is small and searchable |
| **OpenWrt forum thread mining** | You do manually | Browse `forum.openwrt.org` for threads with high reply counts in "Installing and Using" / "Developers" categories; collect URLs of "solved" threads where the fix involved a coding pattern | Forum requires human judgment to separate signal from noise; thread quality varies enormously |
| **OpenWrt mailing list mining** | You do manually | Skim `lists.openwrt.org` archives for patch discussions with "fix", "properly handle" in subject | Mailing lists are dense; human scanning is more efficient than automated parsing |
| **GitHub issue/PR mining (`openwrt/openwrt`, `openwrt/luci`, `openwrt/packages`)** | I automate the search, you curate results | I run `gh search issues`, `gh search commits` queries with patterns like `fix:`, `bug`, `revert`; you select which results are cookbook-worthy | Search is automatable; deciding "is this a common enough mistake to document?" requires domain judgment |
| **GitHub commit message mining** | I automate | `git log --grep="fix:" --oneline` against cloned repos in `tmp/repo-*` | Purely mechanical; I can extract and categorize |

**Summary**: I handle the broad web-search and git-history mining (produces raw lists). You handle forum/mailing-list curation and final selection of which mistakes warrant a cookbook entry. I then collate everything into a ranked taxonomy.

### Phase 2 — Cookbook Placement and Structure

All cookbooks live in cookbook-source. No new directories. Each new cookbook follows the established frontmatter contract that `02i` validates:

```yaml
---
title: "Correct Shell Quoting in OpenWrt Init Scripts"
description: "Demonstrates proper variable quoting in ash/BusyBox shell scripts used by procd init systems, with WRONG/CORRECT pairs sourced from upstream fix commits."
module: cookbook
origin_type: authored
when_to_use: "Use when writing or reviewing shell scripts for OpenWrt init.d, hotplug handlers, or UCI-default scripts."
related_modules: [procd, openwrt-core, openwrt-hotplug]
era_status: current
verification_basis: "Patterns sourced from openwrt/openwrt commit abc1234 (2025-11-02), openwrt/packages commit def5678 (2025-09-14)"
reviewed_by: placeholder
last_reviewed: 2026-03-27
---
```

The `related_modules` field is what connects a cookbook to the rest of the corpus. A single cookbook about shell quoting can cross-reference procd, openwrt-core, and hotplug — its placement in cookbook-source doesn't limit its module associations.

### Phase 3 — Source Citations

Every code example in a cookbook must cite its source with a stable URL and a retrieval date. Format:

```markdown
### CORRECT: Quoting variables in procd init scripts

<!-- Source: https://github.com/openwrt/openwrt/blob/abc1234def/package/network/services/dnsmasq/files/dnsmasq.init#L42-L55 -->
<!-- Retrieved: 2026-03-27 -->

​```sh
#!/bin/sh /etc/rc.common

START=19
USE_PROCD=1

start_service() {
    local enabled
    enabled="$(uci_get dnsmasq @dnsmasq[0] enabled 1)"
    [ "$enabled" = "0" ] && return 0
    # ...
}
​```
```

**Why commit SHA in the URL, not `main`**: branch-tip links go stale silently. A SHA-pinned URL points to an immutable snapshot. If the code changes upstream, the URL still works — readers see what was cited. The `Retrieved:` date tells them when it was verified as current practice.

**Why HTML comments, not visible text**: The citation metadata is for authors and future updaters. Readers see the code. The pipeline doesn't need to parse citations — they're documentation-level metadata, not build-time data.

---

### Execution Plan — Step by Step

#### Step 0: Establish the Research Log

Create `content/cookbook-research/README.md` (or a single `content/cookbook-research-log.md` — your preference) to capture all prompts, search queries, and source URLs used during research. This is the reproducibility artifact. It does NOT get ingested by the pipeline — it's a maintainer reference.

#### Step 1: I Run Automated Mistake Discovery

I execute web searches and git-log mining across these categories:

1. **Shell/ash pitfalls** — unquoted variables, `[` vs `[[`, arithmetic expansion, process substitution absence in ash, `local` scoping
2. **C embedded pitfalls** — buffer overflows in config parsing, unchecked `malloc`, string format vulnerabilities, endianness assumptions
3. **Lua gotchas** — 1-indexed arrays, nil-in-table-length, global variable leaks, string immutability misconceptions
4. **ucode-specific issues** — `json()` vs `parse()`, import scoping, `proto()` misuse
5. **UCI operation mistakes** — missing `uci commit`, wrong section syntax, `uci add_list` vs `uci set`, anonymous section handling
6. **LuCI JS view mistakes** — wrong form class hierarchy, missing `require`, stale CBI patterns, RPC call structure
7. **Hotplug handler mistakes** — wrong env vars, missing ACTION guard, race conditions with interface up/down

**Output**: A categorized list per category with ~10-20 common mistakes each, with source links.

#### Step 2: I Mine the Cloned Repos for Fix Commits

Against the repos already cloned by `01-clone-repos.py` (openwrt, luci, ucode), I run:

```sh
git log --all --oneline --grep="fix:" | head -100
git log --all --oneline --grep="properly" | head -50
git log --all --diff-filter=M --format="%H %s" -- "*/files/*.init" | head -50
```

**Output**: A list of commit SHAs + one-line descriptions where bugs were fixed, grouped by subsystem.

#### Step 3: You Curate Forum/Mailing List Sources

You browse the forum and mailing lists, collecting URLs in a simple format:

```
URL: https://forum.openwrt.org/t/example/12345
Topic: Shell quoting breaks dnsmasq init
Mistake Category: shell-quoting
Notes: User had unquoted variable in uci_get call
```

This doesn't need to be exhaustive — 15-25 high-quality threads is enough to validate and supplement the automated research.

#### Step 4: I Collate Into a Mistake Taxonomy

I merge all sources into a ranked taxonomy:

| Rank | Mistake | Frequency | Sources | Existing Cookbook Coverage |
|------|---------|-----------|---------|--------------------------|
| 1 | Era confusion (Lua CBI vs JS LuCI) | Very High | web, forum, GitHub | ✅ Already in common-ai-mistakes.md |
| 2 | Unquoted variables in init scripts | High | web, commits, forum | ❌ Needs new cookbook |
| 3 | Missing `uci commit` | High | forum, commits | Partial in `uci-read-write-from-ucode.md` |
| ... | ... | ... | ... | ... |

We then pick the top N uncovered mistakes and assign each one a cookbook file.

#### Step 5: I Draft Each Cookbook

For each selected mistake, I:

1. Find 1-3 instances of the **correct** pattern in the actual OpenWrt source (using SHA-pinned URLs)
2. Construct the WRONG example from the researched mistake pattern
3. Write the prose explaining why it fails and what the correct approach handles
4. Fill in the YAML frontmatter with `verification_basis` citing the exact commits/files
5. Include `<!-- Source: ... -->` and `<!-- Retrieved: ... -->` comments on every code block

#### Step 6: You Review, I Revise

You read each draft for:
- Technical accuracy (does the CORRECT code actually do what the prose claims?)
- Relevance (is this a mistake people actually hit, or is it theoretical?)
- Completeness (are there other common variations of this mistake?)

I revise based on your feedback.

#### Step 7: Files Land in cookbook-source, Pipeline Does the Rest

No pipeline changes. `02i` picks them up. `03` normalizes them. `05a` assembles them into release-tree. `06` includes them in `llms.txt`. `08` validates them. Done.

---

### Proposed New Cookbook Topics (Subject to Step 4 Ranking)

Based on preliminary knowledge of common OpenWrt development issues:

| Filename | Topic | Primary Mistake Addressed |
|----------|-------|--------------------------|
| `shell-quoting-init-scripts.md` | Variable quoting in ash/BusyBox init scripts | Unquoted expansions causing word splitting |
| `uci-transactions-and-commit.md` | UCI read-modify-write lifecycle | Missing `uci commit`, partial updates |
| `hotplug-handler-guards.md` | Writing safe hotplug event handlers | Missing ACTION/INTERFACE checks, race conditions |
| `procd-jail-resource-limits.md` | procd jail and resource limit configuration | Using generic Linux cgroup/systemd patterns instead of procd jail syntax |
| `firewall-zone-rule-ordering.md` | Firewall zone and rule configuration | Rule ordering mistakes, zone direction confusion |
| `package-makefile-variables.md` | OpenWrt Makefile variable contracts | Using generic GNU Make patterns instead of OpenWrt build system variables |
| `dsa-network-config.md` | DSA-era network/VLAN configuration | Using swconfig syntax on DSA devices |
| `ucode-json-parsing.md` | Parsing JSON safely in ucode | Confusion between `json()`, `parse()`, and `sprintf()` for structured data |
| `luci-rpc-acl-wiring.md` | LuCI ↔ rpcd RPC call + ACL setup | Missing ACL file, wrong RPC method signature, endpoint naming |
| `busybox-command-differences.md` | BusyBox vs GNU coreutils divergences | Using GNU-only flags (`grep -P`, `sed -i''`, `find -printf`) |

---

### What This Approach Avoids

1. **No fabricated code** — every CORRECT example is cited from the actual OpenWrt repos
2. **No new pipeline stages** — uses the existing `02i` → release-tree flow
3. **No runtime dependencies** — cookbooks are static markdown; citations are frozen at authoring time
4. **No AI-generated code examples** — AI writes the *prose around* cited code, never the code itself
5. **No structural changes** — same cookbook-source directory, same frontmatter contract, same `module: cookbook`

### What Makes This Reproducible

- Research log in `content/cookbook-research-log.md` captures every search query, URL, and prompt
- Each cookbook's `verification_basis` field names exact commits and files
- Each code block's HTML comment cites a SHA-pinned GitHub URL + retrieval date
- The entire effort can be re-run against newer repo snapshots by repeating Steps 1-6 with updated clones