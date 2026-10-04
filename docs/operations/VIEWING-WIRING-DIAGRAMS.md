# Viewing wiring diagrams

## Comprehensive charter map (30 units, 92 edges)

Charter maps use **`WiringMapBrowser`**: primary **force lattice** (layered d3-force, glued junctions, cell-sheaf glue colors), plus searchable handler → callee table and per-handler focus Mermaid. A single full-graph Mermaid for 30 handlers / 90+ edges is intentionally hidden under “Legacy full graph”.

| Piece | Path |
|-------|------|
| **Force lattice UI** | `preview/graph/src/components/WiringForceLattice.tsx` |
| **Map → lattice + sheaf stub** | `preview/graph/src/lib/wiringMapToLatticeGraph.ts` |
| **Visual law (reference)** | [manutej/cell-sheaf](https://github.com/manutej/cell-sheaf) — restriction curves, glue palette |

| Surface | URL / path |
|---------|------------|
| **Preview (live)** | [wiring-graph-preview.vercel.app/charter-10k](https://wiring-graph-preview.vercel.app/charter-10k) |
| **Charter 1k (smaller)** | [/charter](https://wiring-graph-preview.vercel.app/charter) |
| **Source JSON** | `fixtures/external/fineract-charter-10k/wiringmap.v0.json` |
| **Preview data copy** | `preview/graph/src/lib/data/charter-10k.v0.json` |
| **Mermaid builder** | `preview/graph/src/lib/wiringmapToMermaid.ts` |

Local preview:

```bash
cd preview/graph && npm ci && npm run dev
# open http://localhost:3000/charter-10k
```

The page shows the diagram plus expandable **Mermaid source** (generated from the map, not hand-drawn).

## Programme / scale diagrams

- **Preview:** [/scale](https://wiring-graph-preview.vercel.app/scale) — compound loop, 7-shard matrix, scale ladder.
- **Markdown mirror:** `docs/SCALE-DIAGRAMS.md`
- **Chart strings:** `preview/graph/src/lib/scaleDiagrams.ts`

## Metrics dashboard (timing + honesty)

| Surface | URL / path |
|---------|------------|
| **Preview dashboard** | [/scale-dashboard](https://wiring-graph-preview.vercel.app/scale-dashboard) |
| **Static HTML (offline)** | `docs/operations/scale-dashboard/index.html` |
| **Report markdown** | `docs/operations/reports/SCALE-REPORT-LATEST.md` |
| **Regenerate** | `make scale-report` |

## What the diagram does *not* show

- Unmapped service/repository Java (context LOC only).
- Repo-wide Fineract or OpenRig graphs — only **declared slice** maps.

Next leap (S5): inventory-first analysis of [OpenRig](https://github.com/mvschwarz/openrig) — see `docs/operations/build-specs/S5-openrig-large-repo.md`.
