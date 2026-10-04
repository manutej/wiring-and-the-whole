# Software factory skill / plugin package — implementable spec v1

**Status:** harmonized · **Spec version:** 1.0.0 · **Package version:** `plugin-manifest.json` → `1.0.0` · **Corpus:** 9 ingested Paris 2026 talks (`research/ai-engineer-paris-2026/digest.json`) · **Package root:** `skills/paris-level-up/`

**Progress & distance traveled:** [`software-factory-skills-PROGRESS.md`](./software-factory-skills-PROGRESS.md) (timeline, coverage matrix, done vs pending).

### Version lineage

| Version | Commit (branch) | Summary |
|---------|-----------------|---------|
| — (skills only) | [`4db24e8`](https://github.com/manutej/wiring-and-the-whole/commit/4db24e8) | 8 Paris factory `SKILL.md` + `paris-level-up/README` curriculum |
| **v0 spec** | [`35b6c4c`](https://github.com/manutej/wiring-and-the-whole/commit/35b6c4c) | Spec v0, progressive disclosure (L1/L2/L3), consensus iterations 1–3, manifest stub |
| **v1 spec** | (this revision) | Cross-artifact consistency, spec rename v0→v1, progress report, registry/manifest alignment |

Supersedes [`software-factory-skill-plugin.v0.md`](./software-factory-skill-plugin.v0.md) (redirect stub only).

## Purpose

Ship a **Cursor-compatible skill bundle** (repo skills today; `plugin-manifest.json` stub) that encodes a coherent **software factory operating system** for long-running agents and team coding factories — with **progressive disclosure** so operators can act on Layer 1–2 while auditors drill to Layer 3 transcript cites.

## Caption limitation (read once)

All ingested talks use **English (auto-generated) YouTube captions**. Timestamps and quoted snippets are **best-effort alignments** to those captions, not manual transcripts. Where digest/editorial bullets exist, prefer them over paraphrase. Claims not present in ingested JSON are **pending ingest** or **CONJECTURE** (editorial synthesis).

## Charter boundaries (read once)

| Lane | Scope | Must not |
|------|--------|----------|
| **Paris corpus + factory skills** | `research/ai-engineer-paris-2026/`, 8 skills under `skills/paris-level-up/`, registry rows | Change T1–T3 programme claims or witness frozen JSON without pulse |
| **Programme (T1)** | `interface-first-context`, `systems-intake`, `symmetry-lens` | Ship inside Paris plugin bundle; referenced at OS boundaries only |

Detail: [`docs/research/CORPUS-CHARTER.md`](../research/CORPUS-CHARTER.md) · operating model: [`docs/roadmap/CONSENSUS-FORWARD.md`](../roadmap/CONSENSUS-FORWARD.md).

## Package architecture

```text
skills/paris-level-up/
├── README.md                 # Curriculum + unified OS map
├── plugin-manifest.json      # name, version, skills[], triggers[]
└── (skills live as siblings)
    factory-operator/
    process-embedded-factory/
    factory-harness/
    covariant-eval-loop/
    agent-orchestra/
    pr-pulse-discipline/
    eval-over-review/
    devex-metrics-grounding/

Programme boundary (T1 — not in Paris bundle):
    interface-first-context/
    systems-intake/
    symmetry-lens/
```

### Install / discovery model (repo skills)

| Mode | Behavior |
|------|----------|
| **Repo skill** | Agent reads `SKILL.md` when `description` frontmatter matches user task (Cursor skill discovery). |
| **Curriculum** | Human or meta-agent loads `paris-level-up/README.md` order for greenfield factory design. |
| **Registry** | `docs/research-insights/paris-2026.yaml` maps `video_id` → skill path; CI via `make verify-research`. |
| **Plugin stub** | `plugin-manifest.json` lists skill paths + trigger phrases for packaged install. |

### Trigger model

Each skill `description` field holds **auto-apply phrases** (factory, harness, PR bottleneck, covariant eval, orchestra, DevEx, etc.). Plugin stub duplicates high-value triggers for marketplace packaging.

**Composition trigger:** user mentions “coding factory”, “long-running agents”, “software factory OS” → load `factory-operator` then follow README pipeline.

## Progressive disclosure schema

Every Paris factory skill MUST include a `## Progressive disclosure` section with:

### Layer 1 — One-liner

Single sentence operable definition; no new claims beyond existing Core moves.

### Layer 2 — Moves

3–7 bullet **moves** (may mirror “Core moves” titles); imperative verbs; no transcript quotes. Label in skills: **`Layer 2 moves:`** (inline list).

### Layer 3 — Transcript refs

Markdown table under **`Layer 3 — transcript refs`**:

| `video_id` | MM:SS | Label | Snippet / quote |
|------------|-------|-------|-----------------|
| … | … | FACT / CONJECTURE | ≤120 chars from digest, `transcript-summaries.json`, or caption hook |

**Rules:**

- **FACT:** snippet appears in `digest.json` bullets, `transcript-summaries.json` quotes/opening, or charter-committed editorial stub with same `video_id`.
- **CONJECTURE:** synthesis (e.g. explorer thesis, cross-talk pairing) — must be labeled; never scored as FACT in evaluator pass.
- **Pending ingest:** catalog-only videos — not used in Paris bundle skills.

### Unified system

Subsection **`## Unified system`** (or bold **Unified system** under progressive disclosure): **OS stage**, **upstream/downstream skills**, **primary talk(s)**. One talk minimum per skill; **dual-map** where one talk spans two skills by design (see matrix below).

## Unified factory OS (long-running agents)

```mermaid
flowchart LR
  subgraph define["Define & justify"]
    FO[factory-operator]
    DM[devex-metrics-grounding]
  end
  subgraph embed["Embed in work"]
    PE[process-embedded-factory]
  end
  subgraph platform["Platform loop"]
    FH[factory-harness]
    CE[covariant-eval-loop]
  end
  subgraph scale["Multi-session"]
    AO[agent-orchestra]
  end
  subgraph ship["Ship gates"]
    PR[pr-pulse-discipline]
    EV[eval-over-review]
  end
  subgraph boundary["Programme T1"]
    IF[interface-first-context]
    SI[systems-intake]
  end

  FO --> PE --> FH --> CE
  CE --> AO
  AO --> PR --> EV
  DM -.-> FO
  DM -.-> EV
  SI -.-> CE
  IF -.-> AO
  FO --- Hvbo & Factory & Lloyd
  PE --- Hvbo
  FH --- Gupta & Lloyd
  CE --- W&B
  AO --- Holtz
  PR --- Pocock
  EV --- Voss
  DM --- Reock
```

### Talk coverage matrix (9 ingested)

Each `video_id` in `digest.json` → `transcripts_ingested` appears in **exactly one primary skill** row; **dual-map** rows add a secondary skill for split themes.

| video_id | Speaker | Primary skill | Dual-map (secondary) | Role in OS |
|----------|---------|---------------|----------------------|------------|
| `HvboD89DyQ8` | Cooke, WorkOS | process-embedded-factory | factory-operator | Embed + skeptic metrics |
| `vGCJ7diEtrw` | Tížková, Factory | factory-operator | — | Builder economics / build-buy |
| `tUPPVhBBcoM` | Lloyd, Warp | factory-harness | factory-operator (L3 cite) | Environment-centric factory |
| `TN3mj92oZ8I` | Gupta, Warp | factory-harness | — | Harness + refresh + routing |
| `XyV6bSMyq-I` | Aysola, W&B | covariant-eval-loop | — | Covariant eval flywheel |
| `TRfzFJCJ7ZE` | Holtz, Conductor | agent-orchestra | — | Parallel coordination |
| `LlgiOCmFG_w` | Pocock, AIHero | pr-pulse-discipline | — | PR/pulse brakes |
| `_mi3alkqy4s` | Voss, Arize | eval-over-review | — | Eval over ritual review |
| `Se8jHLliLXE` | Reock, DX | devex-metrics-grounding | — | Org measurement |

## Multi-agent consensus (this spec)

Three iterations documented under [`software-factory-skills-consensus/`](./software-factory-skills-consensus/). Roles:

1. **Advocate** — proposes unified OS + skill sections.
2. **Faithfulness evaluator** — reads **only** `digest.json`, `transcript-summaries.json`, `catalog.json` (no advocate prose); scorecard per talk/skill.
3. **Operator synthesizer** — merges evaluator deltas into next iteration.

Final skill content is iteration-3 output; v1 spec adds harmonization + progress narrative only (no core-move rewrites).

## Implementation phases

| Phase | Deliverable | Acceptance | Status |
|-------|-------------|------------|--------|
| **P0** | Spec + consensus artifacts | 3 iterations on disk | **Done** |
| **P1** | 8 `SKILL.md` + README progressive disclosure | Layer 1–3 + Unified system | **Done** |
| **P2** | `plugin-manifest.json` | Valid JSON; skills[] matches paths | **Done** (v1.0.0) |
| **P3** | Registry row for spec | `paris-2026.yaml` target | **Done** |
| **P4** | CI | `make verify` + `make verify-research` PASS | **Done** on branch |
| **P5** | Optional enrichments | See PROGRESS § Pending | **Not started** |

## Acceptance tests — faithfulness

Automatable / manual checks for reviewers:

1. **Coverage:** Every id in `digest.json` → `transcripts_ingested` appears in ≥1 skill Layer 3 table.
2. **No orphan skills:** Each skill lists ≥1 ingested `video_id` in Layer 3.
3. **FACT audit:** Spot-check 3 FACT rows per skill against `transcript-summaries.json` or digest bullets; mismatches → fail.
4. **CONJECTURE hygiene:** Any cross-talk synthesis (e.g. “pairs with Pocock”) labeled CONJECTURE in Layer 3 or spec.
5. **Caption banner:** README or spec states auto-caption limitation once (this doc § Caption limitation).
6. **Pending ingest:** Catalog videos not in `transcripts_ingested` must not appear as FACT (e.g. Antigravity `buHC7bQE1X4` = pending).
7. **Research gate:** `make verify-research` passes on branch.
8. **Version alignment:** `plugin-manifest.json` `version` + this doc title + registry spec `target` path all reference **v1**.

## Pulse alignment

Factory pulses should use [`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](../pulse/IMPLEMENTER-BRIEF-TEMPLATE.md): small PR, firewalled evaluator, `make verify-research` when Paris JSON or skills change.

## References

- **Progress report:** [`software-factory-skills-PROGRESS.md`](./software-factory-skills-PROGRESS.md)
- Corpus charter: [`docs/research/CORPUS-CHARTER.md`](../research/CORPUS-CHARTER.md)
- Registry: [`docs/research-insights/paris-2026.yaml`](../research-insights/paris-2026.yaml)
- Pulse: [`docs/PULSE.md`](../PULSE.md)
- PR: [GitHub #4](https://github.com/manutej/wiring-and-the-whole/pull/4) (`cursor/ai-engineer-paris-research-8e4f`)
