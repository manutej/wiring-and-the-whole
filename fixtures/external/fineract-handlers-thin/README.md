# fineract-handlers-thin — vendored external slice

**Not** a checkout of [apache/fineract](https://github.com/apache/fineract). This directory is a **fixed copy** of seven `@CommandType` command handlers taken from the meta-repo’s E3 ablation corpus.

## Provenance

| Field | Value |
|-------|--------|
| Source tree | `experiments/e3-ablation/raw/*.java` |
| Selection | Seven handlers with `@CommandType` (loan, loancharge, delinquency, center, client transfer) |
| Pin note | Vendored slice from e3-ablation at repo commit; **not** a live upstream pin |
| `// refs:` | Hand-maintained on **three** handlers only (`DisburseLoan`, `CloseLoan`, `AddLoanCharge`) for wiringmap extract; other files rely on import heuristics in `scripts/fineract_slice_check.sh` |

## What is **not** included

- Full Fineract module tree, Gradle build, or Spring application context
- REST resources, persistence (JPA) implementations, or integration tests
- Command registration wiring outside these handler classes
- Payment-type / resilience4j handlers (different command stack; omitted from this slice)

## Files in slice

1. `DisburseLoanCommandHandler.java` — `LOAN` / `DISBURSE`
2. `CloseLoanCommandHandler.java` — `LOAN` / `CLOSE`
3. `AddLoanChargeCommandHandler.java` — `LOANCHARGE` / `CREATE`
4. `CreateDelinquencyRangeCommandHandler.java` — `DELINQUENCY_RANGE` / `CREATE`
5. `SaveCenterCollectionSheetCommandHandler.java` — `CENTER` / `SAVECOLLECTIONSHEET`
6. `WithdrawClientTransferCommandHandler.java` — `CLIENT` / `WITHDRAWTRANSFER`
7. `MarkLoanAsFraudCommandHandler.java` — `LOAN` / `SETFRAUD`

## Wiring artifacts

- `wiringmap.v0.json` — hand-curated L1 map for the three ref-annotated handlers (partial coverage by design)
- `wiringmap.v0.partial.json` — alias copy for density / dogfood docs (same content)

## Commands

```bash
python3 scripts/extract_refs.py fixtures/external/fineract-handlers-thin \
  --example fixtures/external/fineract-handlers-thin/wiringmap.v0.json
python3 scripts/validate_wiringmap.py wiringmap/schema.v0.json \
  fixtures/external/fineract-handlers-thin/wiringmap.v0.json
make external-slice-check
```
