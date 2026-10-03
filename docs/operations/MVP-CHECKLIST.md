# MVP checklist (measured)

**Target:** M1 Engine MVP → M2 1k charter. Update status inline as we go.

| ID | Item | Gate | Status |
|----|------|------|--------|
| M0 | Demo (verify, pipeline-io, preview) | Already on main | **done** |
| M1a | Rust java refs ≡ Python regex + tests | `make wiring-core-check` | in_progress |
| M1b | Rust reexpand byte parity (toybank pack) | dual vs `reexpand_gate.py` | **done** |
| M1c | Rust L2 pack from map (toybank) | `make pack-v0-check` dual | pending |
| M1d | `pipeline-io` Rust path (`WIRING_ENGINE=rust`) | `make pipeline-io` | pending |
| M1× | Independent eval SHIP on M1 bundle | eval doc | pending |
| M2a | 1k charter manifest + fetch pin | external-slice pattern | pending |
| M2b | Edge-recall ~100+ pairs on charter | pulse-eval | pending |
| **PR** | Single integration PR | All M1 + eval | **hold** |

Build log: [`build-log/2026-10-03-mvp-push.md`](build-log/2026-10-03-mvp-push.md)
