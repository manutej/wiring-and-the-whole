# Pulse depth — full programme vs harness-only

This repo runs **two layers** of quality loops. Do not confuse them.

## Harness-only (what `make pulse-eval` proves)

- Functional pass/fail scripts: pack reexpand, density D0–D4, slice MANIFEST, L1 I/O grading, blind pack stub, edge-recall sample, CR@F95 stub columns.
- **No** firewalled evaluator rubric score, **no** adversarial panel transcript, **no** live LLM accuracy claim.

## Full pulse (operator protocol)

See [`PULSE.md`](../PULSE.md): implement → adversarial panel → merge gate → interface tests → **firewalled evaluator** against [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md).

Checklist when running a **deep** pulse (template — fill per round, no fake scores):

- [ ] Implementer brief filed; evaluator rubric **not** read by implementer.
- [ ] Adversarial panel produced numbered gaps with severities.
- [ ] `make verify` + `make pulse-eval` green on merge candidate.
- [ ] Evaluator scored artifacts-only; blockers documented if rubric fail.
- [ ] SCALE-PATH / CONTEXT-COMPACT updated if behavior or honest limits changed.

## Executive report (post-pulse)

After gates pass, file a user-facing summary per [`PULSE-REPORT-SPEC.md`](PULSE-REPORT-SPEC.md) (**APPROVED 2026-10-02**): plain-language metadata (UTC duration, branch, PR, agents table) plus **Done / Tested / Next** — three sections, three bullets each, **no jargon in the whole file**.

## When to extend harness vs run deep pulse

| Signal | Harness bump | Full pulse |
|--------|--------------|------------|
| New make target or gate | Add `pulse-eval` case | Optional if claim changes |
| New scale claim (CR@F95, GA7) | **Not enough** alone | Required + pre-registration |
| Doc-only | `pulse-gate` reminder | Skip evaluator unless user asks |
