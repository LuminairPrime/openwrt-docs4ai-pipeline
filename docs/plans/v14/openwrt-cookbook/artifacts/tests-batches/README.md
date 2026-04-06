# OpenWrt Cookbook Batch Test Instructions

**Purpose:** Blind-prompt batch files for testing AI agents on OpenWrt development tasks. Results drive cookbook discovery and later verification that authored pages improved model competence.

**Your job:** Answer every scenario in the batch file you were given, one batch per session, in order.

**Read from:** `artifacts/tests-batches/<batch-id>.md` — the file provided to you.

**Write to:** `artifacts/runs/<agent-label>/<run-label>/<batch-id>/01-raw-response.md` — your complete response goes here and nowhere else.

**Five hard rules:**

1. **No search.** Do not use repository search, file-system read tools, web search, or external lookup. Answer from internal knowledge only.
2. **One batch per session.** Do not continue a session that has already answered a different batch file.
3. **Do not read `-key.md` files.** These are answer keys and must stay unread during your run.
4. **No extra files.** Do not create scripts, scratch files, or other artifacts outside the designated raw-response path.
5. **Stop after finishing.** Deliver all answers in this batch, then stop. Do not request the next batch.
