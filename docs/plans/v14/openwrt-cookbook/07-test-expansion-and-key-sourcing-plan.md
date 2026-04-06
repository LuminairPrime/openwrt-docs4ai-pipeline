# Test Expansion And Key Sourcing Plan

**Purpose:** Define how the cookbook center should create more unique tests without drifting into random prompt generation or low-value duplicates.

---

## 1. Short Answer

Yes, more unique tests should come from real OpenWrt source material, but not by blindly downloading repos and clipping arbitrary snippets.

The right workflow is:

1. mine authoritative OpenWrt source boundaries
2. identify a teachable contract
3. freeze the answer key from that same authority source
4. only then write the blind prompt

That order matters because it prevents the prompt from outrunning the truth surface.

---

## 2. Primary Source Pools

Prefer sources already available in this repository workspace before fetching anything new.

### 2.1 Local upstream clones already present

Use current local clones under `tmp/authoring-repos/` first. These are already the fastest path to canonical snippet mining.

Typical high-value targets include:

- `tmp/authoring-repos/repo-openwrt-full/`
- `tmp/authoring-repos/repo-procd/`
- `tmp/authoring-repos/repo-uhttpd/`
- `tmp/authoring-repos/repo-ucode-full/`

### 2.2 Condensed corpus outputs

Use the corpus under `openwrt-condensed-docs-renamed/` when the goal is to discover already-normalized reference surfaces, API pages, or cross-linked module content.

### 2.3 Existing cookbook-center governance artifacts

Use these to avoid duplicate work:

- family registry
- gap map
- admitted scenario packets
- inherited 17-scenario bank

### 2.4 Fresh downloads only when necessary

Only fetch a new upstream repo or refresh an existing clone when the needed contract is not already available locally.

---

## 3. What Counts As A Good New Test

A strong new test should satisfy all of these:

1. **OpenWrt-specific boundary:** the right answer depends on OpenWrt APIs, runtime conventions, filesystem conventions, or service architecture
2. **Compact truth surface:** the canonical answer can fit in a short snippet or short structured answer key
3. **Binary scoring:** there is a clear pass/fail rule, not a fuzzy style debate
4. **Blind-spot potential:** a generic Linux, generic JavaScript, or generic C answer is likely to miss the correct OpenWrt boundary
5. **Family uniqueness:** it adds a new family or a materially new sub-boundary inside an existing family

If a candidate only changes nouns but not the real contract, it is not a new unique test.

---

## 4. Mining Workflow

### Step 1: Mine interesting boundaries

Look for compact examples that reveal a durable contract, such as:

- the only correct call order
- a required helper that blind models often omit
- an OpenWrt-specific file location or runtime ownership boundary
- a required module import or API surface that generic answers skip

### Step 2: Name the boundary

Before writing any prompt, state the exact contract being tested.

Examples:

- `ubus_add_uloop()` is required after `ubus_connect()` in standalone C daemons
- `fs.readfile()` plus `json()` is the native ucode path for JSON file input
- `uci_load_validate` is the typed init-script validation boundary in procd

### Step 3: Check for duplication

Compare the candidate against:

- the inherited 17-scenario bank
- the live failure-family registry
- currently admitted packets

If the candidate only duplicates an existing scenario family, reject it or fold it into an existing packet.

### Step 4: Freeze the answer key first

Create the canonical answer key from the authority source before finalizing the blind prompt.

That answer key should contain:

- pass criteria
- canonical snippet
- pattern notes
- explicit falsenesses if needed
- source anchors

### Step 5: Write the blind prompt

Only after the answer key is frozen should the blind prompt be written.

This keeps the prompt honest and prevents designing tests around imagined rather than source-backed behavior.

### Step 6: Group carefully

Once the scenario exists, place it into a grouped batch only if it does not contaminate adjacent questions.

If that step creates a new grouped prompt file or forces a regrouping refresh, copy the execution
contract from
[artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md)
rather than drafting the header ad hoc. Future remaps should preserve the same clean-room and
output-routing language by default so a regrouping pass does not silently weaken the blind-run
contract.

There is currently no dedicated grouped-prompt regeneration script documented or implemented for
this project-center workflow. Until one exists, follow the manual grouped-prompt refresh
procedure in [06-test-bank-and-grouped-delivery.md](./06-test-bank-and-grouped-delivery.md).

---

## 5. key Policy

The cookbook center should mirror the old grouped-slice convention:

- grouped question file and grouped answer key live side-by-side
- names should mirror each other
- grouped run manifests should point to both files

### Naming rule

Examples:

- `01a-batch-alpha.md`
- `01a-batch-alpha-key.md`

- `01b-batch-beta.md`
- `01b-batch-beta-key.md`

- `01c-batch-gamma.md`
- `01c-batch-gamma-key.md`

- `01d-batch-delta.md`
- `01d-batch-delta-key.md`

- `01e-batch-epsilon.md`
- `01e-batch-epsilon-key.md`

- `01f-batch-zeta.md`
- `01f-batch-zeta-key.md`

- `01g-batch-eta.md`
- `01g-batch-eta-key.md`

- `01h-batch-theta.md`
- `01h-batch-theta-key.md`

- `01i-batch-iota.md`
- `01i-batch-iota-key.md`

This naming policy keeps the operator workflow obvious and matches the historical project shape.

The current v14 full-pack rebatch spans `alpha` through `iota` and is intentionally tuned for one isolated agent session per grouped prompt file.

Any future remap that regenerates those grouped prompt files should treat
[artifacts/templates/00-batch-prompt-header-template.md](./artifacts/templates/00-batch-prompt-header-template.md)
as the single reusable source for the shared header block. Only the batch-specific body content
and group-specific path examples should vary across regenerated files.

---

## 6. Recommended Next Families To Mine

The next good test families should come from boundaries that are both unique and still underrepresented.

Likely candidates include:

1. LuCI JS rpcd and form/render boundaries not already covered by the original bank
2. shell hotplug event handling boundaries that are easy to answer generically and incorrectly
3. UCI default or firstboot persistence boundaries that require exact OpenWrt file placement
4. blobmsg parsing and reply-construction boundaries in native C ubus handlers
5. Makefile and package integration boundaries where generic Linux packaging advice fails on OpenWrt

These should be mined one family at a time, not sprayed into the bank all at once.
