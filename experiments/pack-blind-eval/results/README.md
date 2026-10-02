# Pack-blind eval — persisted results (v0)

| File | Role |
|------|------|
| [`schema.results.v0.json`](schema.results.v0.json) | JSON Schema for archived run output |
| [`stub.report.v0.json`](stub.report.v0.json) | Pin shape + example case rows (stub I/O mode) |

Live harness output: `make pack-blind-eval-check` (stdout JSON).

CI alignment: `make pack-blind-results-check` validates `stub.report.v0.json` against the schema and compares live stub grades to the archived case rows (included in `make pulse-eval`).
