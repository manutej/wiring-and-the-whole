# wiring-core (scaffold)

Planned Rust crate for **language-independent** WiringMap v0 operations: validate, in-memory graph IR, extract orchestration, and L2 pack / reexpand parity with today’s Python harness.

**Design doc:** [`docs/architecture/2026-10-02-rust-core-multireader.md`](../../docs/architecture/2026-10-02-rust-core-multireader.md)

**Status:** not wired into CI yet. No `Cargo.toml` until Phase 1 validate lands with golden tests against `wiringmap/examples/` and `fixtures/density/`.

Language-specific parsing lives in separate reader crates (e.g. `wiring-reader-java`), not here.
