# Scale report (latest)

- **Generated:** 2026-10-04T01:03:52Z
- **Git:** `3fe1c7a`

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
          "validate_ms": 1.62,
          "extract_ms": 2.19,
          "pack_ms": 3.65,
          "reexpand_ms": 2.57,
          "total_ms": 10.05
        }
      },
      {
        "id": "toybank-loans",
        "refs_dir": "witness/toybank/loans",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 1.05,
          "extract_ms": 1.44,
          "pack_ms": 2.38,
          "reexpand_ms": 2.03,
          "total_ms": 6.92
        }
      },
      {
        "id": "toybank-savings",
        "refs_dir": "witness/toybank/savings",
        "java_files": 3,
        "steps_ms": {
          "validate_ms": 0.89,
          "extract_ms": 1.27,
          "pack_ms": 2.24,
          "reexpand_ms": 1.95,
          "total_ms": 6.37
        }
      },
      {
        "id": "fineract-handlers-thin",
        "refs_dir": "fixtures/external/fineract-handlers-thin",
        "java_files": 7,
        "steps_ms": {
          "validate_ms": 0.95,
          "extract_ms": 1.34,
          "pack_ms": 2.31,
          "reexpand_ms": 1.84,
          "total_ms": 6.44
        }
      },
      {
        "id": "fineract-charter-1k",
        "refs_dir": "fixtures/external/fineract-charter-1k",
        "java_files": 29,
        "steps_ms": {
          "validate_ms": 1.34,
          "extract_ms": 1.68,
          "pack_ms": 2.47,
          "reexpand_ms": 5.53,
          "total_ms": 11.04
        }
      },
      {
        "id": "toybank-report",
        "refs_dir": "witness/toybank/report",
        "java_files": 1,
        "steps_ms": {
          "validate_ms": 1.12,
          "extract_ms": 1.17,
          "pack_ms": 2.46,
          "reexpand_ms": 2.49,
          "total_ms": 7.26
        }
      },
      {
        "id": "fineract-charter-10k",
        "refs_dir": "fixtures/external/fineract-charter-10k",
        "java_files": 41,
        "steps_ms": {
          "validate_ms": 1.21,
          "extract_ms": 3.21,
          "pack_ms": 2.67,
          "reexpand_ms": 2.32,
          "total_ms": 9.41
        }
      }
    ],
    "total_ms": 57.49
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
          "validate_ms": 81.95,
          "extract_ms": 25.72,
          "pack_ms": 23.57,
          "reexpand_ms": 30.48,
          "total_ms": 161.75
        }
      },
      {
        "id": "toybank-loans",
        "refs_dir": "witness/toybank/loans",
        "java_files": 4,
        "steps_ms": {
          "validate_ms": 78.98,
          "extract_ms": 23.23,
          "pack_ms": 23.55,
          "reexpand_ms": 22.01,
          "total_ms": 147.8
        }
      },
      {
        "id": "toybank-savings",
        "refs_dir": "witness/toybank/savings",
        "java_files": 3,
        "steps_ms": {
          "validate_ms": 78.31,
          "extract_ms": 23.79,
          "pack_ms": 23.2,
          "reexpand_ms": 21.72,
          "total_ms": 147.04
        }
      },
      {
        "id": "fineract-handlers-thin",
        "refs_dir": "fixtures/external/fineract-handlers-thin",
        "java_files": 7,
        "steps_ms": {
          "validate_ms": 77.46,
          "extract_ms": 23.78,
          "pack_ms": 23.85,
          "reexpand_ms": 21.91,
          "total_ms": 147.03
        }
      },
      {
        "id": "fineract-charter-1k",
        "refs_dir": "fixtures/external/fineract-charter-1k",
        "java_files": 29,
        "steps_ms": {
          "validate_ms": 90.54,
          "extract_ms": 25.0,
          "pack_ms": 25.29,
          "reexpand_ms": 24.25,
          "total_ms": 165.1
        }
      },
      {
        "id": "toybank-report",
        "refs_dir": "witness/toybank/report",
        "java_files": 1,
        "steps_ms": {
          "validate_ms": 79.01,
          "extract_ms": 23.7,
          "pack_ms": 24.12,
          "reexpand_ms": 21.93,
          "total_ms": 148.78
        }
      },
      {
        "id": "fineract-charter-10k",
        "refs_dir": "fixtures/external/fineract-charter-10k",
        "java_files": 41,
        "steps_ms": {
          "validate_ms": 85.65,
          "extract_ms": 26.76,
          "pack_ms": 24.55,
          "reexpand_ms": 22.05,
          "total_ms": 159.03
        }
      }
    ],
    "total_ms": 1076.53
  }
}
```
