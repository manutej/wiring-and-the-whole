# Build spec M1c — L2 pack from WiringMap in Rust (builders only)

## Done when

1. `build_l2_pack_from_wiringmap` mirrors [`scripts/build_l2_pack.py`](../../../scripts/build_l2_pack.py) for SliceUnit on toybank (`collect_unit_edges`, explicit + factored text, canonical LEGEND copy).
2. Internal `expand(factored) == explicit` check before write (same invariant as Python `main`).
3. CLI `wiring-build-l2-pack` writes `<map>.pack/{LEGEND,pack_explicit,pack_factored}.txt`.
4. `scripts/l2_pack_parity.sh` byte-compares Rust vs Python on `wiringmap/examples/toybank-accounts.v0.json`.
5. `make pack-v0-check` runs Python build + reexpand + Rust parity.
6. `make wiring-core-check` and `make pulse-loop` green.

## Out of scope

- Handler-family pack (`build_handler_family_pack.py`)
- `pipeline-io` / `WIRING_ENGINE=rust` switch (M1d)
- PR creation
- Eval docs / blind pack eval
