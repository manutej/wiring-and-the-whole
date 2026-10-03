# Build spec S2c — multi-slice pipeline runner

**Done when:**

1. `fixtures/slice-matrix/manifest.v0.json` lists ≥5 slices (toybank accounts/loans/savings, fineract-thin, charter-1k).
2. `scripts/slice_matrix_run.sh` runs validate → extract → pack → reexpand per slice; honors `WIRING_ENGINE`.
3. `make slice-matrix-check` wired into `make pulse-eval`.
4. Machine-readable aggregate JSON on stdout (slice id → status).
