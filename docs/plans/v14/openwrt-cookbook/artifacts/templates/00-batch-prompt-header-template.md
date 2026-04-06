# Batch Prompt Header Template

Use this template when creating or refreshing grouped batch prompt headers and the
master inventory prompt header.

## Required Contract Sections

### 1. Session isolation

- Run the prompt in one fresh isolated agent session.
- Do not reuse a conversation that has already answered another grouped batch.

### 2. Clean-room boundary

- Do not use repository search, file-system read tools, browser tools, web search,
  or other external lookup methods to research answers.
- Do not read other files in this repository to infer the expected OpenWrt pattern.
- The only allowed filesystem action during a blind local run is writing the final
  compiled response to the designated raw-response artifact.

### 3. Dual-environment output routing

- Web or chat agents without file-write access should return one markdown response
  in chat.
- Local IDE or CLI agents with file-write access should not create standalone code
  files, scratch scripts, or other extra artifacts in the repository.
- For grouped blind runs, local agents should write the complete compiled response
  to `artifacts/results/<agent-label>/<run-label>/<group-name>/01-raw-response.md`
  relative to the repository root.
- For non-grouped inventory runs, the operator should supply one explicit output
  destination before execution or capture the response manually after the run.

### 4. Answer shape

- Execute the scenarios sequentially only within the current prompt surface.
- Separate answers with clear headers such as `### Result for Scenario 01`.
- Provide the requested snippet and a brief explanation of the library choices,
  runtime boundary, or architecture used.
- Treat each scenario independently.

## Notes

- Do not force a canned fallback token such as `Failure`; the blind run should stay
  an honest internal-knowledge answer or explicit uncertainty statement.
- The grouped files under `artifacts/test-groups/` are the default blind-run
  surface. The combined `00-batch-prompts.md` file is the full inventory reference
  and should not be the default execution surface.