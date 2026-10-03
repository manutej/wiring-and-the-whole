# fineract-charter-1k — pinned handler vertical (~1k LOC)

**Not a Fineract checkout.** 29 Java files copied from
(excludes orthogonal `CommandHandler<Req,Res>` APIs: PaymentTypeCreateCommandHandler.java)
[`experiments/e3-ablation/raw/`](../../experiments/e3-ablation/raw/) with hand-maintained
[`wiringmap.v0.json`](wiringmap.v0.json) and parser-injected `// refs:` on
29 wired handlers.

## What is **not** included

- Full Fineract tree, runtime, or staff traces
- Auto WiringMap from production DI

## Gates

```bash
make charter-1k-check
python3 scripts/extract_refs.py fixtures/external/fineract-charter-1k \
  --example fixtures/external/fineract-charter-1k/wiringmap.v0.json
```

Refresh stub fetch plan: `./scripts/fetch_fineract_charter_1k.sh --apply`
