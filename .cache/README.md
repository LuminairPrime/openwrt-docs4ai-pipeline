## Shared cache layout

Durable machine-local caches live under `.cache/shared/`.

- `.cache/shared/wiki/cache-state.json` is the warm-cache sentinel written only
  after a successful `vendors\mise\bin\mise.exe run qa-wiki-refresh`.
- `.cache/shared/wiki/http-metadata/` stores the wiki scraper metadata restored
  into the container's `downloads/.cache/` directory for stage `02a`.
- `tmp/ci/qa/<timestamp>/` remains the per-run evidence root for logs and
  summaries. It is not a durable cache.

You can safely delete `.cache/shared/wiki/` at any time. The next
`qa-wiki-refresh` run recreates it from upstream. Do not commit mutable cache
contents beneath `.cache/shared/`.
