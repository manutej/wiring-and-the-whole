# L1 — fineract-handlers-thin · external slice (dogfood)

**Scope:** Seven vendored `@CommandType` handlers under [`fixtures/external/fineract-handlers-thin/`](../../fixtures/external/fineract-handlers-thin/). **Budget:** exported ports + DI wiring for **all seven** ref-annotated units; no method bodies, no full Fineract tree. **Machine mirror:** [`fixtures/external/fineract-handlers-thin/wiringmap.v0.json`](../../fixtures/external/fineract-handlers-thin/wiringmap.v0.json).

**Skill under test:** [`interface-first-context`](../../skills/interface-first-context/SKILL.md).

---

## Scale metrics

| metric | value |
|--------|------:|
| Java handlers in slice | 7 |
| Units in wiringmap | 7 |
| Junction entries | 6 |
| Directed wiring edges | 9 |

---

## Interface catalog

| unit_id | path | role | port_count |
|---------|------|------|------------|
| `handler.DisburseLoanCommandHandler` | `fixtures/external/fineract-handlers-thin/DisburseLoanCommandHandler.java` | LOAN / DISBURSE | 1 |
| `handler.CloseLoanCommandHandler` | `fixtures/external/fineract-handlers-thin/CloseLoanCommandHandler.java` | LOAN / CLOSE | 1 |
| `handler.AddLoanChargeCommandHandler` | `fixtures/external/fineract-handlers-thin/AddLoanChargeCommandHandler.java` | LOANCHARGE / CREATE | 1 |
| `handler.MarkLoanAsFraudCommandHandler` | `fixtures/external/fineract-handlers-thin/MarkLoanAsFraudCommandHandler.java` | LOAN / SETFRAUD | 1 |
| `handler.CreateDelinquencyRangeCommandHandler` | `fixtures/external/fineract-handlers-thin/CreateDelinquencyRangeCommandHandler.java` | DELINQUENCY_RANGE / CREATE | 1 |
| `handler.SaveCenterCollectionSheetCommandHandler` | `fixtures/external/fineract-handlers-thin/SaveCenterCollectionSheetCommandHandler.java` | CENTER / SAVECOLLECTIONSHEET | 1 |
| `handler.WithdrawClientTransferCommandHandler` | `fixtures/external/fineract-handlers-thin/WithdrawClientTransferCommandHandler.java` | CLIENT / WITHDRAWTRANSFER | 1 |

---

## Per-unit cards

### `handler.DisburseLoanCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `LoanWritePlatformService#disburseLoan` (di — junction)
- → `infrastructure.DataIntegrityErrorHandler#handleDataIntegrityIssues` (di — junction)

**Command surface (annotation only)**

- `@CommandType(entity = "LOAN", action = "DISBURSE")`

### `handler.CloseLoanCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `LoanWritePlatformService#closeLoan` (di — junction)

**Command surface**

- `@CommandType(entity = "LOAN", action = "CLOSE")`

### `handler.AddLoanChargeCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `LoanChargeWritePlatformService#addLoanCharge` (di — junction)
- → `infrastructure.DataIntegrityErrorHandler#handleDataIntegrityIssues` (di — junction)

**Command surface**

- `@CommandType(entity = "LOANCHARGE", action = "CREATE")`

### `handler.MarkLoanAsFraudCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `LoanWritePlatformService#markLoanAsFraud` (di — junction)

**Command surface**

- `@CommandType(entity = "LOAN", action = "SETFRAUD")`

### `handler.CreateDelinquencyRangeCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `DelinquencyWritePlatformService#createDelinquencyRange` (di — junction)

**Command surface**

- `@CommandType(entity = "DELINQUENCY_RANGE", action = "CREATE")`

### `handler.SaveCenterCollectionSheetCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `CollectionSheetWritePlatformService#updateCollectionSheet` (di — junction)

**Command surface**

- `@CommandType(entity = "CENTER", action = "SAVECOLLECTIONSHEET")`

### `handler.WithdrawClientTransferCommandHandler`

**Ports (exported only)**

- `processCommand` — method: `CommandProcessingResult processCommand(JsonCommand command)`

**Wiring (outbound)**

- → `TransferWritePlatformService#withdrawClientTransfer` (di — junction)

**Command surface**

- `@CommandType(entity = "CLIENT", action = "WITHDRAWTRANSFER")`

---

## Wiring edges (flat)

- `handler.DisburseLoanCommandHandler#processCommand` → `LoanWritePlatformService#disburseLoan` (di)
- `handler.DisburseLoanCommandHandler#processCommand` → `infrastructure.DataIntegrityErrorHandler#handleDataIntegrityIssues` (di)
- `handler.CloseLoanCommandHandler#processCommand` → `LoanWritePlatformService#closeLoan` (di)
- `handler.AddLoanChargeCommandHandler#processCommand` → `LoanChargeWritePlatformService#addLoanCharge` (di)
- `handler.AddLoanChargeCommandHandler#processCommand` → `infrastructure.DataIntegrityErrorHandler#handleDataIntegrityIssues` (di)
- `handler.MarkLoanAsFraudCommandHandler#processCommand` → `LoanWritePlatformService#markLoanAsFraud` (di)
- `handler.CreateDelinquencyRangeCommandHandler#processCommand` → `DelinquencyWritePlatformService#createDelinquencyRange` (di)
- `handler.SaveCenterCollectionSheetCommandHandler#processCommand` → `CollectionSheetWritePlatformService#updateCollectionSheet` (di)
- `handler.WithdrawClientTransferCommandHandler#processCommand` → `TransferWritePlatformService#withdrawClientTransfer` (di)

---

## Parallel / upstream boundary

- `experiments/e3-ablation/raw/` **‖** this slice — same lineage, but dogfood and extract gates read **only** `fixtures/external/fineract-handlers-thin/` unless a pulse expands scope.
- Full Apache Fineract repository **‖** this slice — no Gradle module graph, no API layer.

---

## Omissions log

- Method bodies — `impl-local`
- Platform service implementations (`LoanWritePlatformService`, etc.) — `out-of-slice` (junction labels only)
- REST, persistence, scheduler, security — `out-of-slice`

---

## Quality gate (self-check)

- [ ] Every exported port names a **public** `processCommand` signature stub (no body read).
- [ ] Wiring edges match `wiringmap.v0.json` evidence strings.
- [ ] No claim of full Fineract coverage in this pack.
