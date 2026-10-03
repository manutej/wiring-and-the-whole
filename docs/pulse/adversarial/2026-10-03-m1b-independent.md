# Adversarial — 2026-10-03 M1b reexpand gate in Rust (independent)

**Panel:** Independent reviewer (did not implement M1b).  
**Target:** `cursor/mvp-engine-push-cd12` @ `b4bb859` — M1b hunks (`pack/reexpand.rs`, `wiring-reexpand`, `wiring_core_check.sh` hook).  
**Spec:** `docs/operations/build-specs/M1b-reexpand-rust.md`

## Commands run (this review)

| Command | Result |
|---------|---------|
| `make wiring-core-check` | **PASS** — validate 3×; java refs 8 + 9; Rust `wiring-reexpand` on toybank pack |
| `cargo test` (`crates/wiring-core`) | **PASS** — 10/10 |
| Manual Rust vs Python exit codes (toybank OK, tampered LEGEND) | **PASS** — 0 / 1 aligned |
| `make pulse-loop` | **PASS** — 35 functional; wiring-core hook green |

Tree pinned to `origin/cursor/mvp-engine-push-cd12` at `b4bb859` without modifying M1b implementation.

## What M1b actually shipped

- Pure functions: `normalize_text`, `validate_legend`, `expand_slice_unit_row`, `expand_command_handler_row` (5- and 6-arg), `expand_factored`, `run_reexpand_gate`.
- CLI: `wiring-reexpand` with `--canonical-legend` (default `experiments/e2-tokens/pack_LEGEND.txt`).
- Integration: last step in `scripts/wiring_core_check.sh` after validate + java refs parity.
- Tests: full toybank pack gate, tampered legend string, one 5-arg CommandHandler row.

**Unchanged enforcement paths:** `scripts/pulse_eval_functional.sh`, `scripts/pipeline_world_io.sh`, `make handler-family-pack-check`, and Makefile targets still invoke **Python** `reexpand_gate.py`.

## Failure modes (operational + semantic)

### A. Parity not continuously dual-run

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Rust-only wiring-core gate** | Rust drifts from Python; toybank pack still passes both | `make wiring-core-check` can stay green while Python-only pulse checks fail — until someone runs full pulse-eval |
| **Single-pack witness** | Regression only on handler wedge or newly built packs | No Rust gate on `fixtures/e3-commandhandler-wedge/pack` in wiring-core-check |
| **Logic mirror without byte diff** | Subtle regex / sort / newline difference | Toybank PASS hides divergence on other inst rows until those packs are tested |

### B. Semantic edge cases (Rust vs Python)

| Mode | Trigger | Symptom | Gated? |
|------|---------|---------|--------|
| **SliceUnit `re.S`** | Python `re.match(..., re.S)` on inst row; Rust regex is single-line | Multiline inst row (pathological) may parse differently | **No** — no multiline fixture |
| **Unknown inst row** | New inst type in factored file | Both error; stderr wording differs | Pulse Python tamper tests only |
| **Broken factored row** | Malformed `inst SliceUnit` / `CommandHandler` | Exit 1; message differs (`FAIL reexpand gate (...):` prefix on Rust CLI) | **Not in wiring-core-check** — pulse-eval Python only |
| **Missing pack files** | absent `pack_explicit.txt` | Both fail | Not separately tested on Rust in CI hook |
| **Legend path** | Rust CLI requires readable `--canonical-legend`; Python embeds repo path | Wrong cwd / missing legend file → Rust exit 1 with I/O message | Partial |

### C. CI / ops (shared with wiring-core)

| Mode | Trigger | Symptom |
|------|---------|---------|
| **SKIP when no cargo** | `cargo` absent | `wiring_core_check.sh` exit 0 with SKIP — reexpand not exercised |
| **Dual stack** | Fix in Python only (production paths) | Rust library stale relative to live gate until wiring-core-check runs |
| **Release binary** | Manual CLI without `cargo build --release` | Script builds release before gate; unit tests hit lib directly |
| **Over-claim** | MVP checklist / spine “M1b done” | Reads as full reexpand migration; pipeline still Python |

## Risk table

| Risk | Severity | Notes |
|------|----------|-------|
| **No Rust/Python reexpand parity script** | medium | M1a has pair-set gate; M1b relies on toybank + structural mirror |
| **Python remains canonical in pulse/pipeline** | medium | Expected for M1b; ops must not assume Rust is wired everywhere |
| **Handler wedge not in wiring-core-check** | medium | 29-handler pack is main CommandHandler stress witness |
| **Broken inst row untested on Rust in CI hook** | low–medium | Covered in lib tests only if added; currently pulse Python |
| **SKIP without cargo** | low–medium | Same class as validate/java refs |

## MUST-PROVE before calling reexpand migration “done”

1. `reexpand_parity.sh` (or equivalent): Rust vs Python exit code + expansion string on toybank and handler wedge packs each pulse.
2. Pulse functional checks for tampered factored rows duplicated for `wiring-reexpand` or pipeline switched to Rust with rollback.
3. Explicit spine/doc state: Python enforcement vs Rust canary until M1c pipeline-io.
4. Optional: golden tests for 6-arg CommandHandler row and SliceUnit edge ordering independent of full pack.

## Relation to prior adversarial notes

`docs/pulse/adversarial/2026-10-03-rust-core-phase1.md` listed “pack/reexpand in Rust” as MUST-PROVE later — M1b closes the **toybank gate + library** slice of that item, not pipeline cutover or handler-wedge Rust enforcement.
