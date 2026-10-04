# Scale build 3 checklist (scale-out + diagrams)

**Branch:** `cursor/scale-build-2-cd12` (carries S2+S3 until integration PR) · **PR:** hold until S2× + S3× SHIP.

| ID | Item | Gate | Status |
|----|------|------|--------|
| S2× | S2 bundle independent eval | eval doc | **done** (NO-SHIP bundle → B1 fixed) |
| S3a | Scale metrics (LOC, recall, slices, handler WIN) | `make scale-metrics-check` | **done** |
| S3b | Slice matrix + report module (6 shards) | `make slice-matrix-check` | **done** |
| S3c | Scale / compound diagrams (preview + doc) | `/scale` route + `docs/SCALE-DIAGRAMS.md` | **done** |
| S3d | Math limits refresh vs measured gates | build-log math row | **done** |
| S3× | Independent eval SHIP S2+S3 | eval doc | **done** (re-SHIP after B1 @ follow-up) |
| **PR** | Integration PR (S2+S3) | S3× SHIP | **hold** |

Build log: [`build-log/2026-10-04-scale-build-3.md`](build-log/2026-10-04-scale-build-3.md)
