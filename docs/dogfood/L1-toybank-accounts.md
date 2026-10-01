# L1 — toybank · accounts/ · witness substrate (dogfood)

**Scope:** E1 faithfulness slice only — four Java files under [`witness/toybank/accounts/`](../../witness/toybank/accounts/). **Budget:** ports + wiring; no bodies, no savings/ledger vertical. **Machine mirror:** [`wiringmap/examples/toybank-accounts.v0.json`](../../wiringmap/examples/toybank-accounts.v0.json).

**Skill under test:** [`interface-first-context`](../../skills/interface-first-context/SKILL.md).

---

## Interface catalog

| unit_id | path | role | port_count |
|---------|------|------|------------|
| `accounts.AccountsController` | `witness/toybank/accounts/AccountsController.java` | HTTP adapter | 2 exported (+1 internal) |
| `accounts.AccountsService` | `witness/toybank/accounts/AccountsService.java` | application service | 2 |
| `accounts.AccountsRepository` | `witness/toybank/accounts/AccountsRepository.java` | persistence | 2 |
| `accounts.Money` | `witness/toybank/accounts/Money.java` | value type (κ demo elsewhere) | 2 fields |

---

## Per-unit cards

### `accounts.AccountsController`

**Ports (exported only)**

- `list` — method: `Page list(int p)`
- `get` — method: `Dto get(long id)`

**Wiring (outbound)**

- → `accounts.AccountsService#fetchPage` (call)
- → `accounts.AccountsService#fetchOne` (call)
- → `shared.AuditDto#log` (ref — junction)
- → `shared.PageDto#of` (ref — junction)

### `accounts.AccountsService`

**Ports (exported only)**

- `fetchPage` — method: `Page fetchPage(int p)`
- `fetchOne` — method: `Dto fetchOne(long id)`

**Wiring (outbound)**

- → `accounts.AccountsRepository#findPage` (call)
- → `accounts.AccountsRepository#findOne` (call)
- → `shared.EventTopics#EVT` (ref — topic junction)

### `accounts.AccountsRepository`

**Ports (exported only)**

- `findPage` — method: `Page findPage(int p)`
- `findOne` — method: `Dto findOne(long id)`

**Wiring (outbound)**

- → `shared.PageDto#of` (ref — junction)

### `accounts.Money`

**Ports (exported only)**

- `amountCents` — field: `long`
- `currency` — field: `String`

**Wiring (outbound)**

- *(none in this slice — type stands alone for witness collision planting)*

---

## Wiring edges (flat)

- `accounts.AccountsController#list` → `accounts.AccountsService#fetchPage` (call)
- `accounts.AccountsController#get` → `accounts.AccountsService#fetchOne` (call)
- `accounts.AccountsController#log` → `shared.AuditDto#log` (ref)
- `accounts.AccountsController#list` → `shared.PageDto#of` (ref)
- `accounts.AccountsService#fetchPage` → `accounts.AccountsRepository#findPage` (call)
- `accounts.AccountsService#fetchOne` → `accounts.AccountsRepository#findOne` (call)
- `accounts.AccountsService` → `shared.EventTopics#EVT` (ref)
- `accounts.AccountsRepository#findPage` → `shared.PageDto#of` (ref)

---

## Parallel product boundary

- `witness/toybank/savings/` **‖** `accounts/` — no edges in E1 vertical slice; safe truncation.

---

## Omissions log

- Method bodies — `impl-local`
- `AccountsService#log`, `AccountsRepository#log` — internal / empty stub
- Savings, ledger, shared DTO source files — `out-of-slice` (junction labels only)

---

## Quality gate (self-check)

- [x] Ports only — signatures as stubs
- [x] Edge endpoints named (ports or junction labels)
- [x] No L2 motif shorthand — L1 only
- [x] Claims discipline — toy scale, demonstrated on witness
