# Scale build 2 checklist (post-MVP merge)

**Branch:** `cursor/scale-build-2-cd12` · **PR:** hold until all rows green · **Base:** `main` @ M1+M2 merge (#42).

| ID | Item | Gate | Status |
|----|------|------|--------|
| S2a | `WIRING_ENGINE` fail-closed (`rust` \| `python`) | pipeline-io + slice matrix | **done** |
| S2b | L2 parity always rebuilds Rust bins | `l2_pack_parity.sh` | **done** |
| S2c | Multi-slice runner (shard-local pipeline) | `make slice-matrix-check` | **done** |
| S2d | Rust extract `--example` wiringmap coverage | `make wiring-core-check` | **done** |
| S2× | Independent eval SHIP on S2 bundle | eval doc | **done** (S2-only SHIP; see S3 bundle) |
| **PR** | Single integration PR | S2× SHIP | **hold** |

Build log: [`build-log/2026-10-03-scale-build-2.md`](build-log/2026-10-03-scale-build-2.md)
