# E3 CommandHandler family wedge (scale path Wedge 1)

**Purpose:** Build L2 **CommandHandler** motif packs from a **PATH LIST** (`experiments/e3-ablation/raw/*.java`) without scanning all of Fineract.

## Scale story

| Metric | Value |
|--------|------:|
| Java files in pool | 30 |
| Parsed into pack (parser v1) | 29 |
| Skipped (orthogonal family) | 1 — `PaymentTypeCreateCommandHandler` |
| Sidecar annotations | 1 — [`annotation_sidecar.v0.json`](annotation_sidecar.v0.json) |
| Explicit lines | 116 (4 per handler) |
| Factored lines | 1 motif + 29 inst rows |

Re-expansion must **byte-match** explicit (`make handler-family-pack-check`).

## Commands

```bash
python3 scripts/build_handler_family_pack.py
python3 scripts/reexpand_gate.py fixtures/e3-commandhandler-wedge/pack
make handler-family-pack-check
```

## I/O contract

- **Input:** vendored handler sources only (same discipline as external thin slice).
- **Output:** `pack/LEGEND.txt`, `pack_explicit.txt`, `pack_factored.txt`, `manifest.json`.
- **Not claimed:** full 514-handler family coverage, Spring DI completeness, or CR@F95.

See [`docs/SCALE-PATH.md`](../../docs/SCALE-PATH.md).
