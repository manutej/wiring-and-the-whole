# Context compact — cold-start snapshot (2026-10-02)

Single page for agents on **`main`**. Detail: [`SCALE-PATH.md`](SCALE-PATH.md), [`HANDOFF.md`](../HANDOFF.md) (history).

## Mission

**Module of systems** (T1) · symmetries (T2) · beat naive tokens at matched fidelity (T3). **Demonstrated ≠ proved** (`plans/ADVERSARIAL.md`).

## Measure vs spec (honest)

| Spec (scale) | We measure today | Gap |
|--------------|------------------|-----|
| CR@F95 Pareto | `make cr-f95-stub-check` (meta L1 + handler-wedge; Q firewall + tokens + null accuracy column) | No LLM, no 95% accuracy |
| GA7 mixed-site comprehension | Frozen E3 in `make verify` | Not 50+10; not wedge pack |
| GA6 token WIN | E2 frozen + handler **29/30** pack | Not 514 handlers |
| Edge recall | `make edge-recall-sample-check` (13 frozen pairs) | Not staff slice / not 514 handlers |
| Wiring I/O | `pipeline-io`, **30×** `pulse-eval`, D0–D4, thin slice, wedge | `// refs:` only |

## Shipped harness

| Area | Proof |
|------|--------|
| E1 | 13/13 — `make verify` |
| E2/E3 | WIN + B-PASSES — frozen JSON |
| Wedge 1 | **29/30** CommandHandler L2 — `make handler-family-pack-check` |
| Wedge 2 pin | `MANIFEST.txt` — `make external-slice-check` |
| L1 dogfood | meta / toybank / fineract-thin / handler-wedge — **all support `--answer-mode io`** |
| Pulse | `make pulse-eval` (**30** checks after CR accuracy column) |
| Blind pack eval | meta + handler-wedge stub — `make pack-blind-eval-check` |

## Commands (copy-paste)

```bash
make verify && make pulse-eval
make handler-family-pack-check
make external-slice-check
make cr-f95-stub-check
make pack-blind-eval-check
make edge-recall-sample-check
make dogfood-grade              # meta L1, I/O mode
```

## Next scale jumps

1. ~~Blind **pack-only** stub~~ — `make pack-blind-eval-check`; optional `PACK_EVAL_LLM=1` + API key.  
2. ~~Wedge 2 **edge-recall** sample gate~~ — `make edge-recall-sample-check` (8+5 pairs); extend to vertical slice.  
3. ~~CR@F95 **accuracy column** plumbing~~ — null + schema; **next:** LLM baseline fill + Pareto.

## Pointers

- Scale ladder: [`SCALE-PATH.md`](SCALE-PATH.md) · Pulse ops: [`PULSE.md`](PULSE.md) · Depth: [`pulse/PULSE-DEPTH.md`](pulse/PULSE-DEPTH.md)  
- Wedge fixture: [`fixtures/e3-commandhandler-wedge/README.md`](../fixtures/e3-commandhandler-wedge/README.md)
