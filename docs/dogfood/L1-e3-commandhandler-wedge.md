# L1 — e3-commandhandler-wedge · CommandHandler family (dogfood)

**Scope:** Twenty-four `@CommandType` handlers parsed from [`experiments/e3-ablation/raw/`](../../experiments/e3-ablation/raw/) into [`fixtures/e3-commandhandler-wedge/pack/`](../../fixtures/e3-commandhandler-wedge/pack/). **Budget:** L2 motif + inst rows only; no Java bodies in the pack. **Machine mirror:** [`fixtures/e3-commandhandler-wedge/manifest.json`](../../fixtures/e3-commandhandler-wedge/manifest.json).

**Skill under test:** [`interface-first-context`](../../skills/interface-first-context/SKILL.md).

---

## Scale metrics

| metric | value |
|--------|------:|
| Java files in pool (`*CommandHandler.java`) | 30 |
| Parsed into pack (v0 parser) | 24 |
| Skipped (alternate handler styles) | 6 |
| Explicit lines (4 per handler) | 96 |
| `inst CommandHandler` rows in factored pack | 24 |

---

## Interface catalog

| unit_id | source (pool) | @CommandType (entity / action) |
|---------|---------------|--------------------------------|
| `handler.DisburseLoanCommandHandler` | `DisburseLoanCommandHandler.java` | LOAN / DISBURSE |
| `handler.CloseLoanCommandHandler` | `CloseLoanCommandHandler.java` | LOAN / CLOSE |
| `handler.AddLoanChargeCommandHandler` | `AddLoanChargeCommandHandler.java` | LOANCHARGE / CREATE |

*(21 additional handlers — same 4-line explicit block shape; see manifest.)*

---

## Per-unit cards

### `handler.DisburseLoanCommandHandler`

**Annotation**

- `@CommandType(entity = "LOAN", action = "DISBURSE")`

**Wiring (outbound)**

- → `LoanWritePlatformService#disburseLoan` (di)

---

## Wiring edges (flat)

- `handler.DisburseLoanCommandHandler` → `LoanWritePlatformService#disburseLoan` (di)
- `handler.CloseLoanCommandHandler` → `LoanWritePlatformService#closeLoan` (di)
- `handler.AddLoanChargeCommandHandler` → `LoanChargeWritePlatformService#addLoanCharge` (di)

*(One primary call edge per parsed handler — 24 total.)*

---

## E2 reference (CommandHandler family)

Single-site micro-example **S3** from [`experiments/e2-tokens/E2-RESULTS.json`](../../experiments/e2-tokens/E2-RESULTS.json):

| site | e_explicit (per handler) | m_row (inst) | F_fixed (legend+motif) | n_star breakeven |
|------|-------------------------:|-------------:|-----------------------:|-----------------:|
| S3 | 62 | 27 | 152 | 5 |

Wedge pack uses the same legend and **CommandHandler** motif as E2 S3; full-family token report: [`fixtures/e3-commandhandler-wedge/token_report.json`](../../fixtures/e3-commandhandler-wedge/token_report.json).

---

## Parallel / upstream boundary

- `experiments/e3-ablation/raw/` **‖** this wedge — same handler lineage; build reads the pool PATH LIST, not a live Fineract clone.
- `fixtures/external/fineract-handlers-thin/` **‖** seven-handler thin slice (separate L1 dogfood pack).

---

## Operator proof

```bash
make handler-family-pack-check
python3 scripts/handler_family_token_report.py --write
```

See [`docs/SCALE-PATH.md`](../SCALE-PATH.md) Wedge 1.
