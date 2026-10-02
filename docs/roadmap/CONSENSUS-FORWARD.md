# Consensus forward — programme + research ingest

**Date:** 2026-10-02 · **Method:** plan draft → three firewalled roles (advocate, adversarial, operator) → merge below.  
**Audience:** cold agent, operator, reviewer.

## Intentions (what we are trying to endure)

1. **Reduce chaotic non-determinism** in how this repo is built and extended—not by slowing agents, but by **fixed contracts**, **tiered gates**, and **role separation** (implement / adversarial / verify / evaluate).
2. **Use structured “skills” methods** (Pocock: durable review artifacts, blast-radius tiers, small diffs; Voss: measurement over ritual; WorkOS: outcome metrics over output volume) as **automation for repo development**, not as conference décor.
3. **Keep the double operadic programme** (HANDOFF T1–T3: witness → wiringmap → pack → falsifiable compression) as the **spine**; Paris / Every corpora are **hypothesis and evidence inputs**, not the mission.

## Spec reality (what already binds us)

| Layer | Source of truth | Gate |
|--------|-----------------|------|
| Faithfulness | E1 witness | `make verify` |
| Token / comprehension pilots | E2, E3 frozen JSON | `make verify` |
| Wiring / pack stress | `wiringmap/schema.v0.json`, density fixtures | `make wiringmap-check`, `make pulse-eval` |
| Process | `docs/PULSE.md`, rubric firewall | Human **pulse** (not CI-only) |
| Build order | `docs/roadmap/BUILD-OUT-RESEARCH.md`, `plans/ADVERSARIAL.md` GA1–GA10 | Sequencing + claims ladder |
| Paris evidence | `research/ai-engineer-paris-2026/` | **Not** on verify today |

**Operator correction (panel consensus):** Treat **merge to `main` as blocked** until a pulse includes adversarial notes + `make pulse-eval` + firewalled evaluator SHIP—even if `PULSE.md` diagram ordering suggests merge earlier.

---

## Adversarial verdict (condensed)

**Directionally sane:** Subordinate YouTube research to **L1 evidence** (catalog, digest, raw transcripts); automate ingest with **loops + frozen JSON**; map Pocock tiers to **SKILL.md + scripts + make targets**.

**Failure if merged naively:**

- Paris branch carries **explorer + vendor tree** while claiming “corpus only” (theater).
- **`make verify` green** while ingest is **skipped** (credits 0) with no degraded flag.
- **Duplicate data** (`paris-editorial-dashboard-kit/data/` vs root research JSON) drifts.
- Conference **dominant_narratives** override OPTIONS / WiringMap critical path.
- **Pulse firewall** bypassed by unattended ingest or hub-refresh prompts.

**Three non-negotiable fixes before research is “programme-merged”:**

1. **`make verify-research`** (or verify stage): schema-check Paris JSON; fail on divergent duplicates; treat unhealthy ingest status explicitly.
2. **Merge allowlist:** corpus files only on `main`; explorer/` optional submodule or branch; no committed `node_modules` / `dist` without reproducible build hash in verify.
3. **`docs/research/CORPUS-CHARTER.md`:** Paris/Every may not change T1–T3 claims or MUST-PROVE; generative ingest follows pulse lanes.

---

## Enduring plan (phases = capability gates, not dates)

### Phase 0 — Frozen ground (maintain)

- Keep **`make verify`** green on programme paths.
- Cold start: **`docs/CONTEXT-COMPACT.md`** + minted **`skills/`** (use compact as ops truth for SKILL count).
- Paris: **`LOOP.md` tick log**; never wire live TubeAlfred to CI.

### Phase 1 — Research as tier-0 signal factory

- **Ingest contract:** fact vs inference; MM:SS cites; snapshot dates on view counts.
- **`docs/research-insights/paris-2026.yaml`:** actionable rows only → `maps_to_skill | maps_to_l1 | maps_to_pulse | status`.
- **Every lane:** `research/every-to/transcripts/raw/` same provenance rules; unified charter.
- **Credits policy:** batch when funded; log skips; committed snapshot is CI truth.

### Phase 2 — Pocock instruments on this repo

- Complete **`systems-intake`**, **`symmetry-lens`** where BUILD-OUT still open; adopt Paris rows into **one SKILL + L1 question** per pulse-sized PR.
- **Small PRs:** one registry adoption OR one wiringmap slice OR one SKILL+L1 pair + pulse brief.
- Example adoptions:
  - **Covariant evals (W&B):** harness change ↔ frozen fixture bump in same PR.
  - **PR bottleneck (Pocock):** implementer brief limits + mandatory adversarial lane.
  - **Outcome metrics (WorkOS):** dogfood scores **navigation under L1 pack**, not commit volume.

### Phase 3 — Operadic spine (programme priority)

Per BUILD-OUT-RESEARCH (unchanged priority):

1. WiringMap v0 **Fineract edge** on main.
2. **Pack builder v0** + `make pack-v0-check` (reexpand gate).
3. Witness **C₀ → Code_X** split when foundation returns.

Paris **explorer** stays **optional teaching surface** until Phase 3 exit criteria met for map+pack on main.

### Phase 4 — Covariant eval plane

- Extend verify family for E5 subset **or** document sibling target explicitly.
- Full E3 + CR@F95 only after map+pack; firewall question minting (GA8).
- **Pulse** default for any change that touches claims, frozen JSON, or skills.

---

## Operating model (three clocks)

| Clock | Runs | Must not |
|-------|------|----------|
| **Commit** | `make verify` (+ touched targets from CONTEXT-COMPACT) | Claim “done” from verify alone on pulse work |
| **12h timer** | Paris catalog diff → transcripts → digest | Block programme CI; hide skip status |
| **Human `pulse`** | verify + pulse-eval + adversarial + evaluator | Implementer reads rubric; self-labeled adversarial |

**Branch lanes:** `main` (programme); `cursor/ai-engineer-paris-research-*` (Paris); `cursor/every-to-transcripts-*` (Every)—no silent edits to witness / E2 / E3 frozen files from research lanes.

---

## Consensus checklist (agents: “done”)

1. **`make verify` PASS**; frozen JSON changes labeled intentional.
2. **Correct lane**—research edits don’t mix programme artifacts without scope.
3. **Pulse artifacts** if scope was pulse: brief, adversarial output, **`make pulse-eval`**, interface notes, evaluator SHIP (firewalled).
4. **Claims ladder**—no banned wording; GA deferrals marked CONJECTURE / MUST-PROVE.
5. **Cold path**—next agent finds commands via CONTEXT-COMPACT / SKILL / wiringmap README.

---

## Immediate next actions (ordered)

1. Implement **`make verify-research`** + **`docs/research/CORPUS-CHARTER.md`** (programme PR on `main` or Paris branch with charter only).
2. **Seed `paris-2026.yaml`** from existing digest bullets (≥8 rows, cites).
3. **Paris branch hygiene:** strip or gitignore `explorer/node_modules`; document explorer as optional; sync kit `data/` with canonical research JSON or fail verify-research.
4. **Programme:** Fineract wiringmap edge (BUILD-OUT next commit).
5. When TubeAlfred credits return: **one batch** ingest (top 2–3 IDs) → digest → registry candidates—not per-tick heroics.

---

## References

- Programme: `HANDOFF.md`, `docs/roadmap/BUILD-OUT-RESEARCH.md`, `plans/ADVERSARIAL.md`, `docs/PULSE.md`
- Paris: `research/ai-engineer-paris-2026/LOOP.md`, `paris-editorial-dashboard-kit/AGENTS.md`
- Every: `research/every-to/README.md` (on `cursor/every-to-transcripts-*`)
