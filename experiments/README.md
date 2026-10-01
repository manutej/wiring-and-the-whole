# Experiments — run order and verification

Prerequisites: **python3**, **node** + npm (E2 tokenizer uses vendored `tiktoken` via `experiments/package.json`).

## One command (repo root)

```bash
make verify
```

Runs three offline gates (no LLM API calls):

| Gate | Command | Proves |
|------|---------|--------|
| **E1** | `python3 witness/run_witness.py` | 13/13 R8 faithfulness checks on toybank (`all_pass: true`). Protocol: [`PROTOCOL-E1.md`](PROTOCOL-E1.md). |
| **E2** | `npm ci` in `experiments/`, then `e2-tokens/e2_run.py` | GA6 micro-scale token arithmetic matches frozen [`e2-tokens/E2-RESULTS.json`](e2-tokens/E2-RESULTS.json) (byte-identical re-expansion gate, e/m/F, n*, WIN). Protocol: [`PROTOCOLS-E2-E3-RECONSTRUCTED.md`](PROTOCOLS-E2-E3-RECONSTRUCTED.md) · narrative: [`e2-tokens/E2-RESULTS.md`](e2-tokens/E2-RESULTS.md). |
| **E3** | `e3-ablation/e3_grade.py` on checked-in `responses/` | Deterministic grades match frozen [`e3-ablation/E3-GRADES.json`](e3-ablation/E3-GRADES.json) (pilot B-PASSES verdict). Results: [`e3-ablation/E3-RESULTS.md`](e3-ablation/E3-RESULTS.md). |

## Manual runs

```bash
make witness    # E1 only
make e2         # E2 only (installs npm deps)
```

E5 depth harness is **not** part of `make verify` (heavier; see `e5-depth/`).

## Wiringmap / dogfood (pulse)

From repo root:

```bash
make wiringmap-check      # schema + toybank extract
make wiringmap-stress     # density ladder D0–D4 (fixtures/density/)
make dogfood-grade        # L1 meta question pack
make dogfood-grade-toybank
make dogfood-grade-fineract-thin
make external-slice-check # fixtures/external/fineract-handlers-thin
```
