# Paris editorial dashboard kit

Extract this folder anywhere your agents work (monorepo, sidecar, or fresh checkout). It bundles **evidence JSON**, a **Vite/React explorer template**, and **agent playbooks** for building high-quality editorial dashboards from conference ingest.

## Quick start (human)

```bash
cd explorer
npm install
npm run dev
```

Open `http://127.0.0.1:5173/#/` — six concept pages ship today; three more talks are stubbed in `stubs/talks-pending.json`.

## Quick start (agent)

1. Read **`AGENTS.md`** (required).
2. Sync facts from **`data/digest.json`** — never invent quotes; use `bullets` timestamps or fetch transcripts.
3. Expand pending talks in **`stubs/talks-pending.json`** into full entries in **`explorer/src/data/talks.ts`**.
4. If you add a new `VizKind` or `diagram` union member, extend **`MiniViz.tsx`** and **`SymbolDiagram.tsx`** in the same PR.
5. Run `npm run build` in `explorer/` before calling the dashboard done.

## Contents

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Editorial contract, quality bar, workflows |
| `data/` | `catalog.json`, `digest.json`, `transcript-summaries.json` |
| `stubs/talks-pending.json` | Talks with transcripts but no concept page yet |
| `schemas/talk-concept.schema.json` | JSON Schema mirror of `Talk` type |
| `prompts/` | Copy-paste task prompts for hub refresh and new talk pages |
| `explorer/` | shadcn-style Paris talk explorer (source only) |
| `diagrams/` | SVG reference maps for hub/canvas work |
| `.cursor/rules/` | Optional Cursor rule when this kit lives in a repo |

## Refreshing data

Replace files under `data/` from your TubeAlfred ingest loop (`research/ai-engineer-paris-2026/` in the wiring-and-the-whole repo), then re-run the agent workflow in `prompts/expand-pending-talks.md`.

## License

Same as parent repository; conference content belongs to speakers and AI Engineer.
