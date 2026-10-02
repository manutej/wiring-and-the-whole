# CR@F95 harness stub (v0)

Plumbing for **covariant evals** (Paris insight `wb-covariant-evals`): question firewall, token column, and a **reserved** accuracy column — **no LLM and no CR@F95 claim** until a pre-registered baseline run fills `accuracy_column`.

## Run configs

| File | Pack | Notes |
|------|------|--------|
| `run_config.handler-wedge.v0.json` | E3 CommandHandler wedge | Token budget column from L2 pack |
| `run_config.meta-l1.v0.json` | Meta L1 corpus | Accuracy column null (stub) |

## Gate

```bash
make cr-f95-stub-check
```

Emits JSON reports to stdout; stub runs must keep `"accuracy_column": null`. Future LLM fills validate against `schema.accuracy_column.v0.json`.

## Pulse alignment

See [`docs/pulse/LOOP-ENGINEERING.md`](../../docs/pulse/LOOP-ENGINEERING.md) — harness changes ship with frozen fixture bumps in the same PR.
