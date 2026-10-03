# MVP checklist (measured)

**Target:** M1 Engine MVP → M2 1k charter. Update status inline as we go.

| ID | Item | Gate | Status |
|----|------|------|--------|
| M0 | Demo (verify, pipeline-io, preview) | Already on main | **done** |
| M1a | Rust java refs ≡ Python regex + tests | `make wiring-core-check` | **done** (eval SHIP) |
| M1b | Rust reexpand byte parity (toybank pack) | dual vs `reexpand_gate.py` | **done** (eval SHIP) |
| M1c | Rust L2 pack from map (toybank) | `make pack-v0-check` dual | **done** |
| M1d | `pipeline-io` Rust path (`WIRING_ENGINE=rust`) | `make pipeline-io` | **done** |
| M1× | Independent eval SHIP on M1 bundle | eval doc | **done** (conditional SHIP) |
| M2a | 1k charter manifest + fetch pin | `make charter-1k-check` | **done** |
| M2b | Edge-recall ~100+ pairs on charter | pulse-eval | **done** (125 total) |
| **PR** | Single integration PR | All M1 + eval | **draft** ([#42](https://github.com/manutej/wiring-and-the-whole/pull/42)) |

Build log: [`build-log/2026-10-03-mvp-push.md`](build-log/2026-10-03-mvp-push.md)
