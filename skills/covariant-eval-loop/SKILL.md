---
name: covariant-eval-loop
description: Self-improving agents — covariant benchmarks, harness, and config; production traces into offline regression; logging flywheel. Auto-apply when changing agent evals, W&B/Weave-style logging, offline agent benches, or Arya/WBAF-like improvement loops.
---

# Covariant eval loop

**Covariance rule** (W&B @ 1:41, `XyV6bSMyq-I`): you cannot change the **benchmark**, **harness**, or **agent configuration** in isolation — they co-move. Long-running and self-improving agents need a **closed loop**: prod → traces → offline hill-climb → gated deploy.

## Progressive disclosure

**Layer 1:** Benchmark, harness, and agent config are **covariant** — change one, re-measure all; close prod→offline flywheel.

**Layer 2 moves:** Triple lock · prod instrumentation · trace export · offline bench · regression tasks · sim-to-real note · promotion gate.

**Layer 3 — transcript refs**

| video_id | MM:SS | Label | Snippet |
|----------|-------|-------|---------|
| `XyV6bSMyq-I` | 1:41 | FACT | Benchmarks, evaluations, and agent harness configs are all covariant |
| `XyV6bSMyq-I` | 2:41 | FACT | Production traces into offline envs to hill-climb — flywheel |
| `XyV6bSMyq-I` | 13:32 | FACT | WBAF caught missing weave.log via offline regression |
| `XyV6bSMyq-I` | 0:24 | FACT | Arya agent GA; deep dive on self-improving agent |

## Unified system

**OS stage:** Prove harness changes. **Upstream:** [`factory-harness`](../factory-harness/SKILL.md) · **Downstream:** [`agent-orchestra`](../agent-orchestra/SKILL.md), ship gates. **Programme:** [`systems-intake`](../systems-intake/SKILL.md). **Talk:** `XyV6bSMyq-I`.

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
