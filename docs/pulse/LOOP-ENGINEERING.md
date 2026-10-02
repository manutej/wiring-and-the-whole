# Loop engineering — pulse × Paris research

How **programme pulse** (implement → adversarial → gates → interface tests → firewalled evaluator) aligns with **Paris / Every research lanes** and the expert-video synthesis on branch `cursor/ai-engineer-paris-research-8e4f`.

**Operator protocol (canonical):** [`docs/PULSE.md`](../PULSE.md)  
**This page:** engineering checklist + in-repo Paris guide paths (no substitute for the rubric firewall).

---

## Branch lanes (do not cross-contaminate)

| Lane | Branch pattern | Owns | Must not silently edit |
|------|----------------|------|-------------------------|
| Programme | `main` | witness, E2/E3 frozen JSON, wiringmap, skills, pulse harness | — |
| Paris ingest + kit | `cursor/ai-engineer-paris-research-*` | `research/ai-engineer-paris-2026/`, insights YAML, consensus docs | programme frozen artifacts |
| Every transcripts | `cursor/every-to-transcripts-*` | `research/every-to/` raw transcripts | same |

Paris JSON is **tier-0 signal**, not on `make verify` today. Merge hygiene and `make verify-research` live on **`cursor/ai-engineer-paris-research-8e4f`** → `docs/roadmap/CONSENSUS-FORWARD.md` (not on `main` until chartered merge).

---

## Paris guide paths (in-repo)

Use these when mapping conference evidence → pulse / L1 / skills (paths exist on `cursor/ai-engineer-paris-research-8e4f`; merge via charter, not drive-by).

| Path | Role |
|------|------|
| [`research/ai-engineer-paris-2026/README.md`](../../research/ai-engineer-paris-2026/README.md) | Corpus charter, TubeAlfred policy, transcript status |
| [`research/ai-engineer-paris-2026/LOOP.md`](../../research/ai-engineer-paris-2026/LOOP.md) | 12h ingest timer log (research clock — not programme CI) |
| [`research/ai-engineer-paris-2026/paris-editorial-dashboard-kit/AGENTS.md`](../../research/ai-engineer-paris-2026/paris-editorial-dashboard-kit/AGENTS.md) | Editorial agent rules: fact vs inference, timestamp cites, no slop |
| [`docs/research-insights/paris-2026.yaml`](../research-insights/paris-2026.yaml) | Actionable rows → `maps_to_skill` / `maps_to_l1` / `maps_to_pulse` |
| `docs/roadmap/CONSENSUS-FORWARD.md` (Paris branch) | Advocate / adversarial / operator consensus; three clocks |
| [`plans/CONSENSUS.md`](../../plans/CONSENSUS.md) | Round-1 binding repairs (R1–R8), suite-minting |
| [`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md) | GA1–GA10 register; hostile-review gaps |

**Every lane (second feature branch):** `cursor/every-to-transcripts-8e4f` — raw transcript ingest under `research/every-to/` (same provenance rules as Paris README).

---

## Independent implementers — rules

Source: [`docs/PULSE.md`](../PULSE.md), [`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](IMPLEMENTER-BRIEF-TEMPLATE.md), Paris row **pocock-pr-skills** → brief limits.

1. **Single brief, single scope** — Copy the implementer template to `docs/pulse/briefs/YYYY-MM-DD-topic.md`. Fill scope, done criteria, forbidden reads. One pulse-sized PR when possible (CONSENSUS-FORWARD Phase 2).
2. **Firewall** — Do **not** read [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md) or evaluator-only notes during the same pulse. Do not self-score hidden dimensions.
3. **Evidence discipline** (Paris kit) — Separate **fact** vs **inference**; timestamp cites for speaker claims; no decorative “factory theater.”
4. **Implement then stop** — Hand off diff summary + open questions + **what you did not test** to the adversarial panel. Do not label your own recap “adversarial.”
5. **Gates you run** — `make verify` for programme paths; `make pulse-eval` when harness/touched targets change. Verify passing is **necessary, not sufficient** for pulse closure.
6. **Outcome over volume** (WorkOS row) — Done means navigation / L1 / witness obligations met, not commit or PR count.

---

## Adversarial evaluators — rules

Two distinct lanes: **adversarial panel** (gap finding) and **evaluator** (rubric scoring). Both are **independent** of the implementer chain-of-thought.

### Adversarial panel

Source: [`docs/PULSE.md`](../PULSE.md) § Steps, [`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md), CONSENSUS-FORWARD operating model.

1. **Separate subagents** — Parallel panel, not the implementer’s summary. Style: GA register (concrete failure modes, severity, cheap checks).
2. **Deliverable** — Numbered gaps; MUST-PROVE / CONJECTURE hooks; suggested checks that are **not** frozen-json echo.
3. **Before merge narrative** — Operator treats merge to `main` as blocked until adversarial notes exist **and** `make pulse-eval` passes **and** firewalled evaluator SHIP (CONSENSUS-FORWARD correction).
4. **Research ingest** — Do not let dominant conference narratives override wiringmap / witness critical path without an explicit programme pulse.

### Evaluator (firewalled)

Source: [`docs/pulse/RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md).

1. **Inputs** — Rubric + artifacts + PR link only (no implementer CoT).
2. **Must not** — Implement fixes or renegotiate scope mid-flight with the implementer.
3. **Output** — Dimension scores D1–D7, fail conditions, **SHIP | NO-SHIP**. Store **outside** implementer context.
4. **Fail if** — Implementer had rubric access; adversarial skipped on witness/experiments/claims; interface tests absent for user-visible changes.

---

## Three clocks (consensus)

| Clock | Runs | Must not |
|-------|------|----------|
| **Commit** | `make verify` + touched targets from [`docs/CONTEXT-COMPACT.md`](../CONTEXT-COMPACT.md) | Claim pulse “done” from verify alone |
| **12h timer** | Paris `LOOP.md` catalog diff → transcripts → digest | Block programme CI; hide credit skips |
| **Human `pulse`** | `make pulse-loop` or verify + `make pulse-eval` + adversarial + evaluator | Implementer reads rubric; self-labeled adversarial |

---

## Harness alignment (covariant evals)

Paris **wb-covariant-evals** (W&B): benchmarks, harness, and agent config move together — offline gates must track programme artifacts.

| Target | What it proves today |
|--------|----------------------|
| `make pack-blind-eval-check` | Blind pack-only L1 stub (meta + handler-wedge); firewall on prompt bundles |
| `make pack-blind-results-check` | Archived pack-blind results JSON vs schema + live stub grade alignment |
| `make edge-recall-sample-check` | Frozen extract ↔ wiringmap pairs (29 pairs, wedge-2 sample) |
| `make cr-f95-stub-check` | Question firewall + token column + **reserved** accuracy column (no LLM claim) |
| `make pulse-unified-eval-check` | **Single JSON** merging pack-blind + cr-f95 stub (`llm_invoked` false unless `PACK_EVAL_LLM=1`) |

Extend harness and frozen fixtures in the **same PR** when adopting a Paris insight row (CONSENSUS-FORWARD Phase 2 example).

---

## Automation

| Make target | Script | Use |
|-------------|--------|-----|
| `make pulse-gate` | [`scripts/pulse_gate.sh`](../../scripts/pulse_gate.sh) | `make verify` + process reminders |
| `make pulse-loop` | [`scripts/pulse_loop_gate.sh`](../../scripts/pulse_loop_gate.sh) | verify + `pulse-eval` + loop checklist |
| `make pulse-eval` | [`scripts/pulse_eval_functional.sh`](../../scripts/pulse_eval_functional.sh) | Functional harness regression battery |

---

## Related

- [`docs/PULSE.md`](../PULSE.md)
- Post-pulse executive report (**APPROVED 2026-10-02**, plain language only): [`PULSE-REPORT-SPEC.md`](PULSE-REPORT-SPEC.md) · depth note in [`PULSE-DEPTH.md`](PULSE-DEPTH.md) · example [`reports/2026-10-02-pulse-meaty.md`](reports/2026-10-02-pulse-meaty.md)
- [`skills/systems-intake/SKILL.md`](../../skills/systems-intake/SKILL.md) — covariant eval section (Paris adopted)
- Programme scale: [`docs/SCALE-PATH.md`](../SCALE-PATH.md)
