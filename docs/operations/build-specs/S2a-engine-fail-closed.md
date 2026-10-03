# Build spec S2a — WIRING_ENGINE fail-closed

**Done when:**

1. `pipeline_world_io.sh` exits non-zero if `WIRING_ENGINE` is not `rust` or `python`.
2. `scripts/slice_matrix_run.sh` uses the same rule.
3. `make pipeline-io` and `make slice-matrix-check` pass with default `rust`.
