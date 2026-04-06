---
name: create-llms
description: Create or refresh an llms.txt file from repository structure and documentation.
---

# Create llms.txt

Use this skill when the repository needs a new or refreshed `llms.txt`.

## Required approach

1. Read the main README and the key architecture or specification docs first.
2. Identify the files that best explain the repo's purpose, contracts, and usage.
3. Group links into a small number of logical sections.
4. Keep descriptions short and specific.

## Format rules

- Start with one `#` heading containing the project name.
- Add a brief blockquote summary.
- Use `##` sections with markdown bullet links.
- Each entry should follow `[label](relative-path): short description`.
- Prefer durable docs, specs, guides, and examples over implementation clutter.

## Selection guidance

Include:

- primary README and getting-started docs
- architecture and specification documents
- important examples or contracts
- setup or configuration docs that shape usage

Exclude:

- generated outputs
- build artifacts
- redundant internals that do not help repo comprehension

## Validation

- confirm every link exists
- keep the file concise enough to scan quickly
- optimize for first-pass repository understanding