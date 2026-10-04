# Paris 2026 — reference index (L4/L5)

Operators and agents **default to L1–L3** inside each Paris factory `SKILL.md`. When a task needs depth in a **special area** (harness refresh, covariant evals, orchestra coordination, PR skills, DevEx baselines), pull **L4 curated excerpts** or **L5 transcript pointers** from here — do not paste bulk quotes into `SKILL.md`.

## Disclosure tiers (spec v1)

| Tier | Where | Agent default | How to load |
|------|--------|---------------|-------------|
| **L1** | `SKILL.md` — one-liner | Yes | Skill discovery |
| **L2** | `SKILL.md` — moves | Yes | Same |
| **L3** | `SKILL.md` — short FACT/CONJECTURE table | Yes | Same |
| **L4** | [`index.yaml`](./index.yaml) — `segments[]` with quotes + `maps_to_skill` | No | Skill trigger for special area, or `@research/ai-engineer-paris-2026/references/index.yaml` + segment `id` |
| **L5** | `index.yaml` — `l5_pointer` per talk | No | `@research/ai-engineer-paris-2026/transcript-summaries.json` or YouTube watch URL in index |

**Caption limitation:** All quotes align to **English (auto-generated)** YouTube captions. Prefer digest bullets and `transcript-summaries.json` over paraphrase. Fields marked `quote_label: INFERENCE` are editorial theme tags, not verbatim transcript claims.

## Example — L4 for `factory-harness`

1. Open [`index.yaml`](./index.yaml) → `talks.TN3mj92oZ8I.segments` (or lookup id `warp-stale-skills`).
2. Load segment ids from [`skills/factory-harness/SKILL.md`](../../../skills/factory-harness/SKILL.md) **References** (e.g. `warp-stale-skills`, `warp-pareto-routing`).
3. Use `quote` + `start`/`end` only for the active task; leave other talks out of context.

For full talk context without TubeAlfred, use **L5** `l5_pointer.summary_path` (opening + metadata) and fetch captions externally via `l5_pointer.youtube_watch` if needed.

## Maintenance

- Source of truth for ingested talks: `digest.json` → `transcripts_ingested`.
- CI: `make verify-research` checks index `video_id` keys ⊆ `transcripts_ingested`.
- New segments: FACT if in digest / `transcript-summaries.json` quotes or opening; INFERENCE if theme-only.
