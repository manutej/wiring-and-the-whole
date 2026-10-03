# Adversarial — 2026-10-03 rust-core Phase 1

| Risk | Severity | Mitigation this pulse |
|------|----------|------------------------|
| Rust/Python validator drift | high | Same schema + three frozen instances in `wiring_core_check.sh` |
| Spine map is narrative, not extracted from git | medium | Edges cite L1 + pipeline; not auto-synced — update map when scripts move |
| "Rust core" over-claim | high | Only validate shipped; pack/extract still Python |
| Dual maintenance cost | medium | Pulse eval fails if Rust gate breaks; Python remains default in `wiringmap-check` |

**MUST-PROVE later:** byte-identical error paths; pack/reexpand in Rust; reader trait with Java golden files.
