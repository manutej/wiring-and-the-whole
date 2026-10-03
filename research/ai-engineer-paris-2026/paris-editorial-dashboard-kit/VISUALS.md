# Visual reference — TubeAlfred & Paris 2026 learnings

Interactive canvas: open **TubeAlfred + Paris 2026 — Visual Map** in Cursor (canvas id `6e28b13a-af45-4321-a5f0-7a94bc314e11`).

## TubeAlfred read pipeline

```mermaid
flowchart TB
  Q[Question / URL / channel handle]
  Q --> R[youtube_url_resolve]
  Q --> D[youtube_search_query / channel_videos]
  R --> E[youtube_video_get / videos_batch]
  D --> E
  E --> T[youtube_video_transcript]
  E --> C[youtube_comments_list]
  T --> OUT[Evidence-backed digest]
  C --> OUT
  E --> OUT
```

## What each layer gives you

| Layer | Source tools | You get | You do **not** get |
|-------|----------------|---------|---------------------|
| Identity | `url_resolve`, `channel_get` | IDs, handles, canonical URLs | Private channel analytics |
| Discovery | `search_query`, `channel_videos` | Ranked public results (snapshot) | Stable SEO rank truth |
| Metadata | `video_get`, `batch` | Title, description, duration, public counts | Retention, CTR, revenue |
| Speech | `video_transcript` | Timestamped segments, caption kind | Speaker diarization guarantees |
| Audience | `comments_list` | Public comment text + engagement | Representative sentiment |

## Paris 2026 — conceptual story (from ingest)

```mermaid
flowchart LR
  A[Agent coding speed] --> B[PR / review bottleneck]
  B --> R[Brakes: skills · evals · tiered review]
  B --> F[Software factories]
  F --> O[Orchestras / multi-agent control planes]
  R --> AR[Autoresearch loops]
  AR --> P[Physical AI · world models]
```

## Evidence discipline

- **Metadata** = schedule lineups, view counts, publish times (TubeAlfred snapshot).
- **Transcript** = speaker claims; cite timestamps when quoting.
- **Comments** = sampled public reactions; never “all viewers think…”
- **Inference** = theme clustering and narrative arrows in diagrams — labeled as synthesis.
