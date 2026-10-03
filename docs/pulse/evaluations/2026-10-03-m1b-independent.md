# Evaluator (independent) — 2026-10-03 M1b reexpand gate in Rust

**Verdict:** **SHIP** (M1b build spec only)

**Reviewer:** Independent panel; did not implement M1b.

**Branch / commit reviewed:** `cursor/mvp-engine-push-cd12` @ `b4bb8599f797724cfb462cc128a72504aca16ac1`

## Build spec

`docs/operations/build-specs/M1b-reexpand-rust.md` (sole rubric for this verdict)

## M1b scope in branch

| Path | M1b? |
|------|------|
| `crates/wiring-core/src/pack/reexpand.rs` | yes — `expand_factored`, legend check, SliceUnit + CommandHandler rows |
| `crates/wiring-core/src/pack/mod.rs`, `src/lib.rs` | yes — module export |
| `crates/wiring-core/src/bin/wiring_reexpand.rs`, `Cargo.toml` | yes — `wiring-reexpand` CLI |
| `scripts/wiring_core_check.sh` | yes — reexpand hook after validate + java refs |
| `docs/operations/MVP-CHECKLIST.md` (M1b row) | narrative only — not evidence |

**Out of M1b scope (per spec):** PR/pipeline-io, pack build in Rust (M1c); replacing Python in `pulse_eval_functional.sh` or `pipeline_world_io.sh`.

## Done-when checklist

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Pure `expand_factored` + legend check mirrors `scripts/reexpand_gate.py` for SliceUnit + CommandHandler rows | **PASS** — same row dispatch, regex shapes, edge sort, motif/foreach skip, trailing newline; toybank pack byte gate via `run_reexpand_gate`; unit test for 5-arg CommandHandler |
| 2 | CLI exits 0 on `wiringmap/examples/toybank-accounts.v0.pack`, 1 on tampered LEGEND (same as Python) | **PASS** — independent dual-run; both exit 0 on canonical pack, 1 on appended LEGEND tamper |
| 3 | Hooked in `scripts/wiring_core_check.sh` after validate/refs | **PASS** — runs `wiring-reexpand` on toybank pack with `experiments/e2-tokens/pack_LEGEND.txt` |
| 4 | `make pulse-loop` green | **PASS** — verify + pulse-eval 35/35; wiring-core hook includes reexpand |

## Evidence (independent commands)

Evaluated on tree at `b4bb859` (no implementation edits; local unstaged ops doc edits ignored).

| Command | Outcome |
|---------|---------|
| `make wiring-core-check` | **PASS** — validate 3×; java refs 8 + 9; `PASS reexpand gate (toybank-accounts.v0.pack)` |
| `cargo test` (`crates/wiring-core`) | **PASS** — 10/10 including `toybank_pack_reexpand`, `rejects_tampered_legend`, `command_handler_five_arg` |
| Rust vs Python reexpand (toybank + tampered LEGEND) | **PASS** — matching exit codes 0 / 1 |
| `make pulse-loop` | **PASS** — functional eval 35 passed; wiring-core reexpand line green |

Do **not** treat implementer checklist rows or bundled MVP ops docs as primary evidence without command logs.

## SHIP rationale

M1b delivers a **library + CLI** re-expansion gate that structurally tracks `reexpand_gate.py`, passes the frozen toybank L2 pack, rejects bad LEGEND with exit 1 like Python, and is wired into the existing `make wiring-core-check` / pulse functional path without claiming pipeline cutover.

## Non-blocking notes

1. `wiring_core_check.sh` runs **Rust only** on toybank — there is no `reexpand_parity.sh` dual-run like M1a java refs; parity is implied by shared logic + toybank integration test, not by comparing Rust vs Python stdout on every gate invocation.
2. Pulse functional battery still exercises **Python** `reexpand_gate.py` for tampered factored rows, handler wedge, and pipeline I/O — appropriate for M1b scope but means two implementations remain authoritative in different CI lanes.
3. Handler-family pack (`fixtures/e3-commandhandler-wedge/pack`) is not in `wiring-core-check`; CommandHandler coverage is partial (5-arg unit test + toybank pack content).

## Conditions (before calling reexpand “migration complete”)

1. Dual-run parity script or shared golden vectors for reexpand output on toybank **and** handler wedge (or explicit decision that toybank alone is sufficient until M1c).
2. Wire Rust into `pulse_eval_functional.sh` / pipeline behind flag, or document Python as sole enforcement on those paths until cutover.
3. Do not mark spine `reexpand_py → rust` complete in L1 docs until production paths switch or parity gates cover them.
