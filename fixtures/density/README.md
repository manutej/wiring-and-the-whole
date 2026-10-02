# Density ladder (wiringmap stress fixtures)

Small adversarial toy repos at increasing **file/ref complexity** — run without scanning production trees. Used by `make wiringmap-stress` (`scripts/wiringmap_stress.sh` + [`stress_manifest.json`](stress_manifest.json)).

## Ladder (ASCII)

```
  D0  witness/toybank/accounts/     4 files   hand wiringmap (canonical)
   │                                      │
   ▼                                      ▼
  D1  d1-minimal/                  2 units   extract FAIL (missing ref)
   │
   ▼
  D2  d2-fork/                     3 files   validate FAIL (bad doctrine_tag)
   │                               + valid wiringmap for extract PASS
   ▼
  D3  d3-orbit/                    8 files   accounts ‖ savings MVC orbit
                                   nested    extract + validate PASS
```

| Step | Path | Intent | Expected gate |
|------|------|--------|----------------|
| **D0** | `witness/toybank/accounts/` | Baseline E1 slice | validate **0**, extract **0** |
| **D1** | `d1-minimal/` | Omitted `// refs:` token in wiringmap | extract **1** |
| **D2** | `d2-fork/` | Schema-invalid `invalid.v0.json` | validate **1**, extract **0** |
| **D3** | `d3-orbit/` | Duplicate rename orbit (two `Money.java`) | validate **0**, extract **0** |

## Expected exit codes

| Subcommand | D0 | D1 | D2 | D3 |
|------------|----|----|----|-----|
| `validate_wiringmap.py` | 0 | (skip) | 1 | 0 |
| `extract_refs.py` | 0 | 1 | 0 | 0 |
| **`wiringmap_stress.sh` (overall)** | **0** when all rows match manifest |

## Add D4 (extensibility)

1. Create `fixtures/density/d4-yourcase/` with `*.java` `// refs:` lines and optional `wiringmap.v0.json`.
2. Append one object to [`stress_manifest.json`](stress_manifest.json) with `refs_dir`, optional `extract_example` / `validate_instance`, and `expect.{extract_exit,validate_exit}`.
3. Re-run `make wiringmap-stress` — no changes to `extract_refs.py` or `validate_wiringmap.py` required.

## Manual probes

```bash
python3 scripts/extract_refs.py fixtures/density/d1-minimal --example fixtures/density/d1-minimal/wiringmap.v0.json
python3 scripts/validate_wiringmap.py wiringmap/schema.v0.json fixtures/density/d2-fork/invalid.v0.json
make wiringmap-stress
```
