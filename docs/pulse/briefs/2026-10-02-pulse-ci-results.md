# Implementer brief — pulse CI pack-blind results

Implementer lane only. Evaluator uses `RUBRIC-EVALUATOR.md` separately.

## Forbidden

- **Do not read** [`RUBRIC-EVALUATOR.md`](../RUBRIC-EVALUATOR.md) or any evaluator-only brief during this pulse.
- Do not score your own work against hidden rubrics.

## Pulse metadata

| Field | Value |
|-------|--------|
| Pulse ID | pulse-ci-results |
| Branch | `cursor/pulse-ci-results-cd12` |
| Operator | cloud agent |
| Date | 2026-10-02 |

## Scope

**In:**

- `make pack-blind-results-check` — schema validate `experiments/pack-blind-eval/results/stub.report.v0.json` and compare live stub grades to archived case rows
- `scripts/validate_pack_blind_results.py` + `make pulse-eval` cases (happy path + deliberate drift failure)
- Meaty pulse minimum duration policy in [`PULSE-DEPTH.md`](../PULSE-DEPTH.md)
- Pulse artifacts: adversarial gap list, evaluator scorecard, executive report
- Update [`CONTEXT-COMPACT.md`](../../CONTEXT-COMPACT.md) next path

**Out:**

- Writing harness output to disk on every CI run (artifact stays pinned stub for now)
- Filling CR@F95 accuracy column or LLM baselines
- Witness / E2 / E3 frozen JSON changes

## Done criteria

- [x] `make verify` PASS
- [x] `make pulse-loop` PASS twice (timings in executive report)
- [x] `make pack-blind-results-check` PASS
- [x] `make pulse-eval` PASS (includes new checks)
- [x] Adversarial + scorecard + report under `docs/pulse/`

## Claims & provenance

- Ladder: DESIGN (CI guard on archived blind-pack results shape)
- CONJECTURE: pinned stub + live alignment catches drift without persisting every run
- Frozen artifacts: `stub.report.v0.json` unchanged unless case counts change legitimately

## Commands

```bash
make verify
make pack-blind-results-check
make pulse-eval
make pulse-loop
```

## Handoff to adversarial panel

- Whether stub-only pinning leaves stdout-only runs unchecked on disk
- Meaty pulse 5-minute rule — enforcement is procedural, not automated

## Handoff to evaluator

- PR link + this brief + adversarial notes (operator supplies rubric separately)
