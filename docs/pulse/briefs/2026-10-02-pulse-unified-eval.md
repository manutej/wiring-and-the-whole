# Implementer brief — pulse unified eval

Implementer lane only. Evaluator uses `RUBRIC-EVALUATOR.md` separately.

## Forbidden

- **Do not read** [`RUBRIC-EVALUATOR.md`](../RUBRIC-EVALUATOR.md) or any evaluator-only brief during this pulse.
- Do not score your own work against hidden rubrics.

## Pulse metadata

| Field | Value |
|-------|--------|
| Pulse ID | pulse-unified-eval |
| Branch | `cursor/pulse-unified-eval-cd12` |
| Operator | cloud agent |
| Date | 2026-10-02 |

## Scope

**In:**

- One JSON report merging `pack-blind-eval` + `cr-f95-stub` (`scripts/pulse_unified_eval_run.py`, `experiments/pulse-unified-eval/`)
- `make pulse-unified-eval-check`
- `make pulse-eval` check: unified report shape + `llm_invoked: false` unless `PACK_EVAL_LLM=1` and API key
- Pulse artifacts: adversarial gap list, evaluator scorecard (separate lanes)
- Update [`CONTEXT-COMPACT.md`](../../CONTEXT-COMPACT.md) and [`SCALE-PATH.md`](../../SCALE-PATH.md)

**Out:**

- Filling CR@F95 `accuracy_column` with live LLM scores
- Paris research branch merges
- Witness / E2 / E3 frozen JSON changes

## Done criteria

- [x] `make verify` PASS
- [x] `make pulse-eval` PASS (includes unified eval check)
- [x] `make pulse-unified-eval-check` emits single JSON with `pack_blind_eval` + `cr_f95_stub` sections
- [x] Top-level `llm_invoked` false in default stub run
- [x] Adversarial + scorecard files present under `docs/pulse/`

## Claims & provenance

- Ladder: DESIGN (harness covariant eval — Paris `wb-covariant-evals`)
- CONJECTURE: unified report sufficient for next Pareto baseline runs
- Frozen artifacts: none (prompt bundles may regenerate)

## Commands

```bash
make verify
make pulse-unified-eval-check
make pulse-eval
make pulse-loop
```

## Handoff to adversarial panel

- Diff summary, unified JSON schema, whether individual gates still pass alone
- Open: LLM lane not exercised in CI; accuracy column still null

## Handoff to evaluator

- PR link + this brief + adversarial notes (operator supplies rubric separately)
