# AI Engineer Paris 2026 — research corpus

Machine-readable digest of [@aiDotEngineer](https://www.youtube.com/@aiDotEngineer) conference uploads (Sep 23–24, 2026, STATION F).

## Files

| File | Purpose |
|------|---------|
| `explorer/` | **Navigable shadcn-style concept dashboard** (Vite + React) |
| `catalog.json` | Recent session uploads (title, views, theme tag) |
| `digest.json` | Event metadata, narratives, ingest state |
| `transcript-summaries.json` | Openings + word counts for ingested talks |

## TubeAlfred tools used

- `youtube_url_resolve`, `youtube_channel_get`, `youtube_channel_videos`
- `youtube_search_query`, `youtube_video_get`
- `youtube_video_transcript`, `youtube_comments_list`

## Transcript status

- **6** individual talks ingested (auto-generated English captions).
- **2** main-stage livestreams: lineup in video description; captions not in metadata at fetch time.

## Ingest policy (TubeAlfred)

- **CI truth** is committed JSON (`catalog.json`, `digest.json`, `transcript-summaries.json`), not live API calls.
- **`digest.json` → `last_ingest_status`:** when `skipped_insufficient_credits`, treat corpus as **degraded**; `make verify-research` warns and merge is OK only if documented (see `docs/research/CORPUS-CHARTER.md`).
- **12h timer** (`LOOP.md`): metadata diff only when credits are zero; **batch** transcript fetches when credits return (top IDs from `next_ingest_priority`), then refresh digest — no per-tick heroics.
- **Never** wire TubeAlfred to programme CI.

## Explorer (optional)

The `explorer/` dashboard is a **local teaching surface** (Vite + React). Run `npm ci && npm run build` under `explorer/` after clone; artifacts are gitignored. Programme gates use canonical JSON at this directory root, not the UI.

## Next ingest (priority by views)

See `digest.json` → `next_ingest_priority`.
