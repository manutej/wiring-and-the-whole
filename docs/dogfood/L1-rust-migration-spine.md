# L1 — rust-migration-spine · harness · compressed

**Scope:** How this repo’s own **meta wiring** (`L1-wiring-and-the-whole`) compresses into a **Rust core** migration spine. Ports-only; no Python source bodies.

**Source map (machine):** [`wiringmap/examples/repo-rust-spine.v0.json`](../../wiringmap/examples/repo-rust-spine.v0.json)

**Parent L1:** [`L1-wiring-and-the-whole.md`](L1-wiring-and-the-whole.md) — cold start → `make verify` → experiments.

---

## Grading facts

| fact_key | value |
|----------|-------|
| `rust_crate_path` | crates/wiring-core |
| `rust_validate_binary` | wiring-validate |
| `python_validate_script` | scripts/validate_wiringmap.py |
| `migration_phase_active` | 1 |
| `spine_edge_count` | 8 |

---

## Interface catalog (Python → Rust)

| unit_id | path today | rust_target (phase) | role |
|---------|------------|---------------------|------|
| `validate_py` | `scripts/validate_wiringmap.py` | `wiring_core::validate_files` (1) | JSON Schema gate |
| `extract_py` | `scripts/extract_refs.py` | `wiring-reader-java` (2) | ref tokens |
| `pack_py` | `scripts/build_l2_pack.py` | `wiring_core::pack` (3) | L2 factored text |
| `reexpand_py` | `scripts/reexpand_gate.py` | `wiring_core::reexpand` (3) | faithfulness gate |
| `pipeline_sh` | `scripts/pipeline_world_io.sh` | `wiring-cli` orchestration (4) | round-trip I/O |
| `validate_rs` | `crates/wiring-core/.../wiring_validate.rs` | **shipped Phase 1** | parity CLI |

---

## Wiring edges (flat)

- `pipeline_sh` → `validate_py` (call)
- `pipeline_sh` → `extract_py` (call)
- `pipeline_sh` → `pack_py` (call)
- `pipeline_sh` → `reexpand_py` (call)
- `validate_py` → `validate_rs` (ref: parity)
- `pipeline_sh` → `L1-wiring#verify` (ref: meta dogfood)
- `validate_rs` → `wiring-core` (ref: library home)
- `extract_py` → `wiring-reader-java` (ref: Phase 2)

---

## Compressed use

1. Read this pack (or the JSON map) to see **order of migration**: validate → readers → pack/reexpand → CLI.
2. Run **`make wiring-core-check`** — Rust and Python must agree on the same golden maps.
3. Expand using the full meta L1 when you need programme context (handoff, adversarial, witness).
