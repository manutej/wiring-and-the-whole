# Scale report (latest)

- **Generated:** 2026-10-04T00:55:06Z
- **Git:** `e4ebf58`

## Corpus honesty

Charter 10k is NOT a full Apache Fineract clone. It copies real Fineract-derived Java from in-repo experiment corpora (e3-ablation, e5-depth, e2-tokens) with parser-injected // refs: — not hand-wrapped placeholder code.

- Upstream: https://github.com/apache/fineract.git (pinned: False)
- `experiments/e3-ablation/raw (*CommandHandler.java)`
- `experiments/e5-depth/raw (*.java services)`
- `experiments/e2-tokens/raw (*.java)`

## View wiring

- Comprehensive Mermaid: https://wiring-graph-preview.vercel.app/charter-10k
- HTML dashboard (preview): https://wiring-graph-preview.vercel.app/scale-dashboard
- Static HTML (repo): `docs/operations/scale-dashboard/index.html`
- Docs: `docs/operations/VIEWING-WIRING-DIAGRAMS.md`

## Metrics JSON

```json
{
  "charter_1k": {
    "java_files": 29,
    "loc": 1350,
    "ref_tokens": 90
  },
  "slice_matrix_slices": 7,
  "edge_recall_frozen_pairs": 127,
  "edge_recall_distinct_pairs": 118,
  "handler_parsed": 29,
  "matrix_unique_java_bodies": 60,
  "matrix_unique_java_loc": 10663,
  "handler_measured_explicit_tokens": 1923,
  "handler_measured_factored_tokens": 947,
  "handler_breakeven_verdict_at_n514": "WIN",
  "charter_10k": {
    "java_files": 41,
    "loc": 10270,
    "ref_tokens": 92
  }
}
```

## Timing JSON

```json
{
  "rust": {
    "schema_version": "slice-matrix-timing.v0",
    "wiring_engine": "rust",
    "slice_count": 7,
    "slices": [
      {
        "id": "toybank-accounts",
        "refs_dir": "witness/toybank/accounts",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 1.39,
          "extract_ms": 1.92,
          "pack_ms": 3.67,
          "reexpand_ms": 3.45,
          "total_ms": 10.46
        }
      },
      {
        "id": "toybank-loans",
        "refs_dir": "witness/toybank/loans",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 1.21,
          "extract_ms": 1.23,
          "pack_ms": 2.2,
          "reexpand_ms": 2.03,
          "total_ms": 6.69
        }
      },
      {
        "id": "toybank-savings",
        "refs_dir": "witness/toybank/savings",
        "java_files": 3,
        "steps_ms": {
          "validate_ms": 0.85,
          "extract_ms": 1.29,
          "pack_ms": 1.94,
          "reexpand_ms": 1.83,
          "total_ms": 5.92
        }
      },
      {
        "id": "fineract-handlers-thin",
        "refs_dir": "fixtures/external/fineract-handlers-thin",
        "java_files": 7,
        "steps_ms": {
          "validate_ms": 0.87,
          "extract_ms": 1.14,
          "pack_ms": 2.03,
          "reexpand_ms": 1.81,
          "total_ms": 5.86
        }
      },
      {
        "id": "fineract-charter-1k",
        "refs_dir": "fixtures/external/fineract-charter-1k",
        "java_files": 29,
        "steps_ms": {
          "validate_ms": 1.32,
          "extract_ms": 1.71,
          "pack_ms": 2.45,
          "reexpand_ms": 1.92,
          "total_ms": 7.41
        }
      },
      {
        "id": "toybank-report",
        "refs_dir": "witness/toybank/report",
        "java_files": 1,
        "steps_ms": {
          "validate_ms": 0.83,
          "extract_ms": 1.31,
          "pack_ms": 2.16,
          "reexpand_ms": 1.86,
          "total_ms": 6.18
        }
      },
      {
        "id": "fineract-charter-10k",
        "refs_dir": "fixtures/external/fineract-charter-10k",
        "java_files": 41,
        "steps_ms": {
          "validate_ms": 1.17,
          "extract_ms": 2.96,
          "pack_ms": 2.41,
          "reexpand_ms": 1.97,
          "total_ms": 8.52
        }
      }
    ],
    "total_ms": 51.04
  },
  "python": {
    "schema_version": "slice-matrix-timing.v0",
    "wiring_engine": "python",
    "slice_count": 7,
    "slices": [
      {
        "id": "toybank-accounts",
        "refs_dir": "witness/toybank/accounts",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 86.58,
          "extract_ms": 24.08,
          "pack_ms": 23.76,
          "reexpand_ms": 22.11,
          "total_ms": 156.55
        }
      },
      {
        "id": "toybank-loans",
        "refs_dir": "witness/toybank/loans",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 77.75,
          "extract_ms": 23.72,
          "pack_ms": 27.38,
          "reexpand_ms": 21.97,
          "total_ms": 150.84
        }
      },
      {
        "id": "toybank-savings",
        "refs_dir": "witness/toybank/savings",
        "java_files": 3,
        "steps_ms": {
          "validate_ms": 81.96,
          "extract_ms": 23.09,
          "pack_ms": 23.21,
          "reexpand_ms": 21.56,
          "total_ms": 149.83
        }
      },
      {
        "id": "fineract-handlers-thin",
        "refs_dir": "fixtures/external/fineract-handlers-thin",
        "java_files": 7,
        "steps_ms": {
          "validate_ms": 76.7,
          "extract_ms": 23.16,
          "pack_ms": 23.17,
          "reexpand_ms": 21.37,
          "total_ms": 144.41
        }
      },
      {
        "id": "fineract-charter-1k",
        "refs_dir": "fixtures/external/fineract-charter-1k",
        "java_files": 29,
        "steps_ms": {
          "validate_ms": 82.66,
          "extract_ms": 28.04,
          "pack_ms": 25.23,
          "reexpand_ms": 22.83,
          "total_ms": 158.78
        }
      },
      {
        "id": "toybank-report",
        "refs_dir": "witness/toybank/report",
        "java_files": 1,
        "steps_ms": {
          "validate_ms": 78.71,
          "extract_ms": 23.56,
          "pack_ms": 23.34,
          "reexpand_ms": 21.45,
          "total_ms": 147.07
        }
      },
      {
        "id": "fineract-charter-10k",
        "refs_dir": "fixtures/external/fineract-charter-10k",
        "java_files": 41,
        "steps_ms": {
          "validate_ms": 88.09,
          "extract_ms": 27.69,
          "pack_ms": 24.6,
          "reexpand_ms": 22.52,
          "total_ms": 162.92
        }
      }
    ],
    "total_ms": 1070.4
  }
}
```
