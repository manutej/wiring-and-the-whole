# fineract-charter-10k — experiments PATH LIST (~10k LOC)

**Not a Fineract checkout.** This charter copies **42** Java files from in-repo
experiments (`e3-ablation`, `e5-depth`, `e2-tokens`) for **scale honesty** — validate → extract → pack → reexpand
at ~10k LOC without claiming repo-wide wiring.

## Wiring discipline

- **30** `@CommandType` handlers carry `// refs:` and full map units (same family as charter-1k).
- **Service / repository** files add LOC and realism; they are **not** fully mapped (Spring DI out of scope).

Orthogonal handlers excluded: PaymentTypeCreateCommandHandler.java.

## Gates

```bash
make charter-10k-check
make slice-matrix-check   # includes this shard when listed in manifest
```

Bootstrap: `python3 scripts/bootstrap_fineract_charter_10k.py`
