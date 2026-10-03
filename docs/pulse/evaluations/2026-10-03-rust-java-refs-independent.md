# Evaluator (independent) — 2026-10-03 rust java refs (PR #40)

**Verdict:** **SHIP** (Phase 2 scoped slice only)

**Reviewer:** Independent panel; did not implement PR #40.

## Scope reviewed

- `crates/wiring-core/src/reader/java_refs.rs` — parse, walk, fragment build
- `crates/wiring-core/src/bin/wiring_extract_java_refs.rs` — CLI
- `scripts/java_refs_parity.sh` — Rust vs Python gate
- Integration: `scripts/wiring_core_check.sh`, `make wiring-core-check`, pulse functional hook

**Out of scope for this SHIP:** Replacing Python in `pipeline_world_io.sh`, wiringmap `--example` parity in Rust, full-repo Java slices.

## Evidence (independent)

| Check | Outcome |
|-------|---------|
| `make wiring-core-check` | PASS (validate 3 instances; java refs 8 + 9 tokens) |
| `cargo test` in `crates/wiring-core` | PASS (6/6) |
| Off-fixture parse probe (`//  refs:`, `//refs:`) | Python matches; Rust does not — **not caught by gate** |

Rejected as primary evidence: `docs/pulse/evaluations/2026-10-03-rust-java-refs.md` (implementer self-SHIP, no command log).

## SHIP rationale

The merge delivers a **tested Rust reader + CLI** and a **repeatable parity gate** on frozen toybank-accounts and fineract-handlers-thin trees, hooked into pulse functional eval. That matches a Phase 2 “compound reader” increment without claiming pipeline cutover.

## Conditions (non-blocking for this verdict)

1. Treat Python `extract_refs.py` as **enforcement** for wiringmap evidence until Rust gains `--example` or pipeline switches.
2. Extend parity fixtures or add unit tests for regex-equivalent comment forms before claiming full semantic parity.
3. Do not mark L1 spine item `extract_py → rust` complete in docs until pipeline uses Rust or parity covers all CI extract paths.

## Top risks (summary)

1. **False confidence in “Python parity”** — gate is pair-set equality on two directories; parser semantics differ on whitespace variants.
2. **Operational dual stack** — fixes must land in two places; production extract path remains Python-only.
3. **Narrow regression surface** — loans/savings toybank, density fixtures, and handler-wedge slices are not in `java_refs_parity.sh`.
