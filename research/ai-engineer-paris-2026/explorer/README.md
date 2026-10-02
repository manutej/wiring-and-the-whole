# Paris 2026 Talk Explorer

Navigable shadcn-style concept dashboard for the six TubeAlfred-ingested AI Engineer Paris talks.

## Run

```bash
cd research/ai-engineer-paris-2026/explorer
npm install
npm run dev
```

Open the local URL (default port 5173). Routes use hash routing (`/#/talk/pr-bottleneck`) for static hosting.

## Build

```bash
npm run build
npm run preview
```

## Structure

- `src/data/talks.ts` — editorial content, metaphors, failure modes, demo stages
- `src/pages/TalkConceptPage.tsx` — concept page archetype per talk
- `src/components/MiniViz.tsx` — teaching animations (vocab cards)
- `src/components/SymbolDiagram.tsx` — per-talk SVG concept maps

Design: dark Station F editorial, Instrument Serif + Inter + JetBrains Mono, motion for reveal + live demo cycling only (no ambient particle slop).
