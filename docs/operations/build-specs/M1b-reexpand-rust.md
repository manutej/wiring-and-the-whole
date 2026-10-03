# Build spec M1b — reexpand gate in Rust (builders only)

## Done when

1. Pure `expand_factored` + legend check mirrors [`scripts/reexpand_gate.py`](../../scripts/reexpand_gate.py) for SliceUnit + CommandHandler rows.
2. CLI exits 0 on `wiringmap/examples/toybank-accounts.v0.pack`, 1 on tampered LEGEND (same as Python).
3. Hooked in `scripts/wiring_core_check.sh` after validate/refs.
4. `make pulse-loop` green.

## Out of scope

- PR, pipeline-io, pack build in Rust (M1c)
