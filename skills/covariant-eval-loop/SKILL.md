---
name: covariant-eval-loop
description: Covariant agent improvement — bench, harness, and config move together; traces into offline regression. Triggers — agent evals, Weave logging, offline agent benches, self-improving agent loops.
---

# Covariant eval loop

You cannot change **benchmark**, **harness**, or **agent configuration** in isolation. Close prod → traces → offline hill-climb → gated deploy.

## Progressive disclosure

**Layer 1:** Benchmark, harness, and config are **covariant** — change one, re-measure all.

**Layer 2 moves:** Triple lock · prod traces · offline bench · regression tasks · promotion gate.

**Layer 3:** Segment ids in **References**.

**Unified system:** Prove harness changes. **Upstream:** [`factory-harness`](../factory-harness/SKILL.md) · **Downstream:** [`agent-orchestra`](../agent-orchestra/SKILL.md). Programme: [`systems-intake`](../systems-intake/SKILL.md).

## When to use

- Self-improving coding/research agents; adding tools/skills; regression suites for SDK/logging gaps.

## When NOT to use

- Static one-shot codegen; sim-to-real proof without documented gap (label CONJECTURE).

## Core moves

1. **Triple lock** — Document `(benchmark_version, harness_version, agent_config_id)`; bump affected legs in one PR (`wb-covariant-triple`).
2. **Trace flywheel** — Prod failures/wins → offline episodes (`wb-trace-flywheel`).
3. **Offline bench** — Deterministic CI subset + richer nightly; no prod keys in CI.
4. **Regression tasks** — Keep tasks that caught real bugs (`wb-weave-regression`); note sim-to-real gaps explicitly.
5. **Promotion gate** — No harness promotion without offline pass + eval delta artifact; programme: `make verify` / `make pulse-eval` when applicable.

## Quality gate

- [ ] Harness change includes bench update in same change set.
- [ ] ≥1 regression task tied to a past miss.
- [ ] Trace → offline pipeline documented (manual OK at first).
- [ ] Eval results stored as artifacts, not chat-only.
- [ ] Sim-to-real limitations written down.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Bench green, prod broken | Trace-derived cases | `wb-trace-flywheel` |
| Overfitting offline | Holdout prod sample | `wb-covariant-triple` |
| Logging gap | SDK regression task | `wb-weave-regression` |
| Config-only “fix” | Covary harness+bench | `wb-covariant-triple` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `wb-arya-intro`, `wb-covariant-triple`, `wb-trace-flywheel`, `wb-weave-regression`
- L5: `transcript-summaries.json#XyV6bSMyq-I`

Cross-links: [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md) for merge gates.
