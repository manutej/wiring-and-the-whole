# wiring-core (Phase 1)

Typed Rust library for **WiringMap v0** validation. Parity target: `scripts/validate_wiringmap.py`.

## Build

```bash
cargo build --release --manifest-path crates/wiring-core/Cargo.toml
```

## CLI

```bash
./crates/wiring-core/target/release/wiring-validate \
  --schema wiringmap/schema.v0.json \
  --instance wiringmap/examples/toybank-accounts.v0.json
```

## Repo self-wiring

Harness migration spine (compressed L1): `docs/dogfood/L1-rust-migration-spine.md` and `wiringmap/examples/repo-rust-spine.v0.json`.

## Java refs (Phase 2)

Pure parser in `src/reader/java_refs.rs`; CLI `wiring-extract-java-refs`. Parity with `scripts/extract_refs.py` via `scripts/java_refs_parity.sh`.

## CI

`make wiring-core-check` (validate + java refs parity; also in `make pulse-eval`).
