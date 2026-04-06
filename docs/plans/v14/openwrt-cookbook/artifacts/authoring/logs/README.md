# Creation Logs

Store cookbook-center creation logs under this directory.

Recommended naming:

```text
<cookbook-slug>-creation-log.md
```

Use `00-creation-log-template.md` as the starting point.

The creation log is the provenance and audit surface for staged cookbook authoring.
It records:

- which scenario packet and grouped prompt drove the work
- which blind-failure evidence and answer key were used
- which authority sources were checked
- what scope decisions were made
- how the staged draft was reconciled against any incumbent live page
- whether any token-budget exception was needed

The creation log is required before promotion. It is the companion document that
connects the staged draft in `../drafts/` to the human decision record in `../reviews/`.

If you want a concrete filled example instead of the blank template, see:

- `../examples/ucode-native-file-io-and-json-creation-log.md`
