# Agent instructions — editorial dashboards (Paris kit)

You are building **editorial concept dashboards**: teaching pages, not slide decks. Each talk is one navigable route with thesis, vocabulary, failure modes, a symbolic diagram, and one signature motion demo.

## Non‑negotiables

1. **Evidence discipline** — Metadata and counts from `data/catalog.json`. Claims and quotes from `data/digest.json` / `data/transcript-summaries.json` or fresh transcripts. Label auto-generated captions. Separate **fact** vs **inference** in copy.
2. **Timestamp cites** — Use `MM:SS` from digest `bullets` or transcript segments when stating what a speaker said.
3. **No ambient slop** — No particle fields, infinite gradients, or decorative motion. Motion serves teaching (vocab reveal, demo stage cycle, scroll progress).
4. **One signature interaction per talk page** — e.g. cycling `demoStages`, toggling failure modes, or a single MiniViz animation.
5. **Match existing patterns** — Read `explorer/src/data/talks.ts` and copy structure, tone, and density before adding talks.

## Architecture map

```
data/*.json          → facts + ingest state
stubs/*.json         → work queue for editorial expansion
explorer/src/data/talks.ts   → canonical Talk[] for UI
explorer/src/pages/HubPage.tsx       → index / filters / narrative
explorer/src/pages/TalkConceptPage.tsx → layout for each talk
explorer/src/components/MiniViz.tsx    → VizKind animations
explorer/src/components/SymbolDiagram.tsx → diagram union variants
explorer/src/App.tsx                   → hash routes /#/talk/:slug
```

## Talk object contract

TypeScript source of truth: `explorer/src/data/talks.ts` (`Talk`, `VizKind`, `diagram` union).

JSON Schema twin: `schemas/talk-concept.schema.json`.

Every **complete** talk needs:

- `slug` — kebab-case, stable URL
- `videoId` — YouTube id (link evidence)
- `metaphor`, `thesis`, `hook` — editorial layer (thesis is one sharp paragraph)
- `stats` — at least one stat with `cite` when from TubeAlfred
- `symbols` (3–4), `vocab` (3) with valid `viz`, `failureModes` (3), `demoStages` (4–5)
- `diagram` — existing variant or **new** variant implemented in `SymbolDiagram.tsx`
- `accent` — one hex accent per talk for hub card

## Workflow A — Ship pending concept pages

1. Load `stubs/talks-pending.json`.
2. For each entry, read matching `data/digest.json` → `insights[videoId]` and `transcript-summaries.json`.
3. Draft full `Talk` object; pick metaphor that **contrasts** or **extends** hub narrative (factories vs orchestras vs eval flywheel).
4. Append to `talks.ts`; register route if slug list is hardcoded anywhere (check `HubPage`, `App.tsx`, `SiteNav`).
5. If `vocab[].viz` uses a new kind, add case to `MiniViz.tsx` with exhaustive switch + `never` default.
6. `npm run build` in `explorer/`.

## Workflow B — Refresh hub editorial

1. Recompute top sessions by `views` from `data/catalog.json`.
2. Update hub copy in `HubPage.tsx` — dominant themes from `digest.json` → `dominant_narratives` and `theme_distribution`.
3. Mark cards with transcript badge when `videoId ∈ digest.transcripts_ingested`.
4. Keep hero stats honest (ingested count, not total uploads).

## Workflow C — New ingest from TubeAlfred

1. Diff channel uploads → update `data/catalog.json`.
2. Transcript new ids → extend digest + transcript-summaries (with bullets).
3. Add stub row to `stubs/talks-pending.json` or complete `Talk` if user wants full page immediately.

## Visual system

- Dark Station F editorial; fonts: Instrument Serif (headlines), Inter (body), JetBrains Mono (meta).
- Components under `explorer/src/components/ui/` follow shadcn-style APIs already in repo.
- Reference SVGs in `diagrams/` for hub/canvas parity; do not hotlink external assets for core diagrams.

## Quality checklist (before merge)

- [ ] Every stat or view count traceable to `data/` snapshot date
- [ ] No quote without timestamp or explicit “paraphrase” label
- [ ] `npm run build` passes
- [ ] New slugs reachable via `/#/talk/<slug>`
- [ ] Hub lists new talk with correct `accent` and theme pill
- [ ] TypeScript unions extended exhaustively (`VizKind`, `diagram`)

## Prompts

Use files in `prompts/` as user-message templates; prefer editing repo files over long chat-only output.
