# Software factory skills — progress & distance traveled

**Branch:** `cursor/ai-engineer-paris-research-8e4f` · **PR:** [GitHub #4](https://github.com/manutej/wiring-and-the-whole/pull/4) · **Canonical spec:** [`software-factory-skill-plugin.v1.md`](./software-factory-skill-plugin.v1.md) · **Package:** [`skills/paris-level-up/`](../../skills/paris-level-up/)

## Charter boundaries (once)

| Lane | What it is | What it is not |
|------|------------|----------------|
| **Paris research corpus** | Tier-0 evidence: `research/ai-engineer-paris-2026/` (catalog, digest, transcripts), ingest loop, explorer optional | Programme spine (witness, E2/E3, WiringMap MUST-PROVE) |
| **Paris factory skills (8)** | Actionable OS for coding factories / long-running agents; maps to ingested talks | Replacement for T1 skills or pulse firewall |
| **Programme skills (3)** | `interface-first-context`, `systems-intake`, `symmetry-lens` — referenced at factory OS boundaries | Bundled in `plugin-manifest.json` `skills[]` (listed under `programme_boundary_skills` only) |

Governance: [`docs/research/CORPUS-CHARTER.md`](../research/CORPUS-CHARTER.md) · [`docs/roadmap/CONSENSUS-FORWARD.md`](../roadmap/CONSENSUS-FORWARD.md).

## Timeline

| When | Milestone | Key artifacts / commits |
|------|-----------|-------------------------|
| 2026-10-01+ | Paris corpus v1 on branch | Research JSON, `make verify-research`, registry seed |
| 2026-10-02 | Consensus forward plan | [`docs/roadmap/CONSENSUS-FORWARD.md`](../roadmap/CONSENSUS-FORWARD.md), charter, yaml rows |
| 2026-10-04 | **8 factory skills shipped** | [`4db24e8`](https://github.com/manutej/wiring-and-the-whole/commit/4db24e8) — `skills/paris-level-up/README.md` + 8× `SKILL.md` |
| 2026-10-04 | **Spec v0 + progressive disclosure** | [`35b6c4c`](https://github.com/manutej/wiring-and-the-whole/commit/35b6c4c) — spec v0, L1/L2/L3, consensus ITERATION 1–3, manifest stub |
| 2026-10-04 | **Spec v1 harmonization** | This commit — v1 spec, PROGRESS doc, version alignment (manifest `1.0.0`) |

Ingest loop: corpus **frozen at 9 talks** since TubeAlfred credits exhausted ([`digest.json`](../../research/ai-engineer-paris-2026/digest.json) `last_ingest_status`: `skipped_insufficient_credits`).

## Coverage matrix

### 9 talks × 8 skills × registry

**Legend:** ✓ = Layer 3 FACT row(s) in skill; **P** = primary ownership in OS map; **D** = dual-map secondary cite.

| video_id | Words | factory-operator | process-embedded | factory-harness | covariant-eval | agent-orchestra | pr-pulse | eval-over-review | devex-metrics | Registry row(s) |
|----------|------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-----------------|
| `HvboD89DyQ8` | 2978 | ✓ D | ✓ **P** | | | | | | | `workos-outcome-metrics`, `workos-embed-process` |
| `vGCJ7diEtrw` | 3710 | ✓ **P** | | | | | | | | `factory-com-build` |
| `tUPPVhBBcoM` | 3636 | ✓ D | | ✓ **P** | | | | | | `warp-lloyd-environment` → harness; Lloyd L3 also in operator |
| `TN3mj92oZ8I` | 2374 | | | ✓ **P** | | | | | | `warp-stale-skills` |
| `XyV6bSMyq-I` | 3968 | | | | ✓ **P** | | | | | `wb-covariant-evals` |
| `TRfzFJCJ7ZE` | 3083 | | | | | ✓ **P** | | | | `holtz-orchestra` |
| `LlgiOCmFG_w` | 4156 | | | | | | ✓ **P** | | | `pocock-pr-skills` |
| `_mi3alkqy4s` | 4412 | | | | | | | ✓ **P** | | `voss-measure-review` |
| `Se8jHLliLXE` | 3787 | | | | | | | | ✓ **P** | `dx-data-grounding` |

**Totals:** 9/9 ingested IDs in Layer 3; 8/8 skills have ≥1 ingested ID; **32,104** transcript words across ingested talks (`digest.json` → `insights.*.transcript_words`).

**Dual-map (documented):** WorkOS split operator vs embed; Lloyd Warp cited in harness (primary) and operator (environment L3).

**Registry:** 10 adopted talk rows + 1 spec row → [`docs/research-insights/paris-2026.yaml`](../research-insights/paris-2026.yaml) (`software-factory-skill-plugin-spec` → v1 path).

### Plugin manifest ↔ curriculum

| Skill path | README order | In `plugin-manifest.json` `skills[]` |
|------------|-------------|--------------------------------------|
| `skills/factory-operator/SKILL.md` | 1 | ✓ |
| `skills/process-embedded-factory/SKILL.md` | 2 | ✓ |
| `skills/factory-harness/SKILL.md` | 3 | ✓ |
| `skills/covariant-eval-loop/SKILL.md` | 4 | ✓ |
| `skills/agent-orchestra/SKILL.md` | 5 | ✓ |
| `skills/pr-pulse-discipline/SKILL.md` | 6 | ✓ |
| `skills/eval-over-review/SKILL.md` | 7 | ✓ |
| `skills/devex-metrics-grounding/SKILL.md` | 8 | ✓ |

Triggers in manifest match spec § Trigger model (10 phrases). Programme boundary: 3 paths in `programme_boundary_skills` only.

### Progressive disclosure labels (spec ↔ skills)

| Spec section | All 8 Paris `SKILL.md` |
|--------------|------------------------|
| Layer 1 — One-liner | `**Layer 1:**` |
| Layer 2 — Moves | `**Layer 2 moves:**` |
| Layer 3 — Transcript refs | `**Layer 3 — transcript refs**` + table |
| Unified system | `**Unified system**` under `## Progressive disclosure` |

Consensus write-up: [`software-factory-skills-consensus/ITERATION-3.md`](./software-factory-skills-consensus/ITERATION-3.md) (frozen at SHIP; v1 does not reopen scores).

## What’s done vs pending

### Done (v1 scope)

- [x] 9-talk corpus ingested with digest + transcript word counts
- [x] 8 factory skills + curriculum README + ascii OS map
- [x] Progressive disclosure L1/L2/L3 + unified system on all 8 skills
- [x] 3-iteration faithfulness consensus (advocate / evaluator / operator)
- [x] Implementable spec (v0 → **v1**), redirect stub for old v0 path
- [x] `plugin-manifest.json` stub (name, skills, triggers, programme boundary)
- [x] Registry adoption rows for all talks + spec
- [x] `make verify-research` gate on branch (with ingest degraded warn when credits 0)

### Pending (out of v1 / spec P5)

- [ ] **TubeAlfred credits** — batch ingest top IDs from `digest.json` → `next_ingest_priority` (e.g. `buHC7bQE1X4`, `YIVkERhy8xo`, …)
- [ ] **Catalog-only sessions** — ~21 catalog entries without transcripts; no FACT rows until ingested
- [ ] **`make verify-skills`** — optional FACT linter (iteration-3 follow-up)
- [ ] **Richer MM:SS bullets** — talks with hook-only digest (Factory.com, Lloyd mid-talk claims)
- [ ] **Marketplace plugin** — publish beyond repo-local discovery
- [ ] **Merge to `main`** — requires pulse evaluator SHIP per CONSENSUS-FORWARD (branch still DRAFT PR)

## v1 revision summary (4db24e8 → 35b6c4c → v1)

| Area | After `4db24e8` | After `35b6c4c` | v1 harmonization |
|------|-----------------|-----------------|-------------------|
| Skills | Core moves + provenance | + L1/L2/L3 + unified system | Labels unchanged; link spec v1 in operator only |
| Spec | — | v0 single doc | **v1** canonical + v0 redirect; primary/dual-map matrix; P0–P4 marked done |
| Manifest | — | v0.1.0, spec v0 path | **1.0.0**, spec v1 path |
| Registry | talk rows | + spec row (v0 target) | spec target → **v1** |
| Consensus | — | ITERATION 1–3 | unchanged; referenced from v1 |
| Ops docs | CONTEXT compact 8 skills | — | + PROGRESS link; CONSENSUS-FORWARD execution log row |

## Quick navigation

- Spec v1: [`software-factory-skill-plugin.v1.md`](./software-factory-skill-plugin.v1.md)
- Consensus: [`software-factory-skills-consensus/`](./software-factory-skills-consensus/)
- Digest (9 talks): [`research/ai-engineer-paris-2026/digest.json`](../../research/ai-engineer-paris-2026/digest.json)
- Cold start: [`docs/CONTEXT-COMPACT.md`](../CONTEXT-COMPACT.md)
