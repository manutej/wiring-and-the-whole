---
name: covariant-eval-loop
description: Self-improving agents — covariant benchmarks, harness, and config; production traces into offline regression; logging flywheel. Auto-apply when changing agent evals, W&B/Weave-style logging, offline agent benches, or Arya/WBAF-like improvement loops.
---

# Covariant eval loop

**Covariance rule** (W&B @ 1:41, `XyV6bSMyq-I`): you cannot change the **benchmark**, **harness**, or **agent configuration** in isolation — they co-move. Long-running and self-improving agents need a **closed loop**: prod → traces → offline hill-climb → gated deploy.

## When to use

- **Self-improving** coding or research agents.
- Adding tools/skills to a factory harness ([`factory-harness`](../factory-harness/SKILL.md)).
- Designing **regression suites** that catch SDK/logging omissions (WBAF example @ 13:32).

## When NOT to use

- Static one-shot codegen with no telemetry.
- Claiming sim-to-real proof without documented gap (label CONJECTURE).

## Core moves (7)

1. **Triple lock** — Document current `(benchmark_version, harness_version, agent_config_id)` hash; bump all affected pieces in one PR when any leg changes.
2. **Prod instrumentation** — Structured logs/traces (Weave-style) on every tool call and model turn worth debugging.
3. **Trace export** — Production failures and wins become **offline episodes** (@ 2:41 flywheel).
4. **Offline bench** — Runnable without prod keys; deterministic subset for CI; richer suite nightly.
5. **Regression tasks** — Small tasks that caught real bugs (e.g. missing `weave.log` call @ 13:32) — never delete without replacement.
6. **Sim-to-real note** — Explicit list of what offline **does not** capture (latency, human approval, data drift).
7. **Gate** — No harness promotion without offline pass **and** labeled eval delta for reviewers.

## Quality gate

- [ ] Changing harness triggers **bench update** in same change set.
- [ ] **≥1 regression task** tied to a past incident or miss.
- [ ] Trace → offline pipeline documented (even if manual at first).
- [ ] Eval results stored as **artifacts**, not chat-only.
- [ ] Programme repos: run `make verify` / `make pulse-eval` when applicable.

## Failure modes

| Symptom | Fix |
|---------|-----|
| Bench green, prod broken | Add trace-derived cases; covary config |
| Overfitting offline | Holdout prod sample; rotate tasks |
| Logging gap undetected | SDK/regression task per critical span |

## Cross-links

- Slice intake: [`systems-intake`](../systems-intake/SKILL.md) (covariant section).
- Merge discipline: [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md).

## Provenance

- Zubin Aysola — *How We Built an Agent That Improves Itself* (`XyV6bSMyq-I`, @ 1:41, 2:41, 13:32)
