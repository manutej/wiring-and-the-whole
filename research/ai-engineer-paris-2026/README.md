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

## Next ingest (priority by views)

See `digest.json` → `next_ingest_priority`.
