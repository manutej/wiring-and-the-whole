# Adversarial — 2026-10-04 Scale Build S2 + S3 (independent)

**Verdict:** **NO-SHIP**. B1 below is a live, reproducible gate failure: `WIRING_ENGINE=python make slice-matrix-check` exits 2. Every other probe found gaps rather than failures.

**Panel:** Independent reviewer (did not implement S2/S3).  
**Target:** `cursor/scale-build-2-cd12` @ `79b0708` (S3) / `2ddb287` (S2).  
**Specs:** `S2a-engine-fail-closed.md`, `S2c-slice-matrix.md`, `S2d-rust-extract-example.md`, `SCALE-BUILD-3-CHECKLIST.md`.  
**Evaluator doc:** [`../evaluations/2026-10-04-s2-s3-scale-independent.md`](../evaluations/2026-10-04-s2-s3-scale-independent.md)

## Probes run

| Probe | Expectation | Result |
|-------|-------------|--------|
| `WIRING_ENGINE=python make slice-matrix-check` @ `79b0708` | 6/6 | **FAIL** — `toybank-report: pack` (`bad inst row: 'inst SliceUnit(unit:ReportModule, edges=[])'`) |
| Same @ `2ddb287` (S2, 5 shards) | 5/5 | PASS |
| `l2_pack_parity.sh` over all 6 manifest maps | byte-identical | 5/6; **`toybank-report` diverges** (Python crash, Rust correct) |
| Scratch-copy fix of `short_unit` (strip `unit:` before `split(".")`) | parity | byte-identical on report / accounts / charter |
| `WIRING_ENGINE=bogus bash scripts/slice_matrix_run.sh` | exit 1 | PASS (not in pulse) |
| Rust vs Python `--example` with wrong map (loans refs vs accounts map) | both fail, same pairs | PASS — 16-pair mismatch sets identical |
| `--example /nope.json` | both exit 1 | PASS |
| No flags on `witness/toybank/loans` (default = accounts map) | both exit 1 | PASS (parity of defaults) |
| Relative `--example` from cwd `/tmp` | same exit | **Diverges** — Rust 1 (cwd-relative), Python 0 (repo-relative) |
| `expected.v0.json` each bound tightened by one | gate fails | PASS — all 5 errors reported |
| `token_report.json` `factored_full` → 5000 (measured @29 loses) | gate fails | **Gate passes (exit 0)** — keyed on `verdict_at_n` (514 extrapolation) |
| Distinct-source LOC over matrix | ≥ 1700 | **≈ 1417**. The 7 thin handlers duplicate charter-1k handlers (only `// refs:` lines differ); the reported 1743 is a sum |
| Clean worktree @ `79b0708`: rust matrix / scale-metrics / python matrix | green / green / green | green / green / **FAIL** |
| `preview/graph`: `tsc --noEmit`, `next build` | clean, `/scale` prerendered | PASS |
| `docs/SCALE-DIAGRAMS.md` ↔ `scaleDiagrams.ts` | in sync | PASS — 5/5 blocks verbatim |

## Failure modes

### A. Dual-engine claims without dual-engine gates

| Mode | Trigger | Symptom | Gated? |
|------|---------|---------|--------|
| **Oracle can't build a shard** (B1) | Dotless unit id (`unit:ReportModule`) | Python `build_l2_pack.py` crashes; Rust succeeds | **No** — pulse runs the matrix on `rust` only |
| **Parity only on toybank-accounts** | Any map other than the default | Rust/Python pack drift is invisible to `wiring-core-check` / `pack-v0-check` | **No** |
| **Example parity is positive-only** | Coverage logic drifts on mismatch paths | `java_refs_example_parity.sh` compares exit codes on passing cases only | **No** (manual negative probe passed) |
| **Known issue re-entered** | M1 eval note 1 said to resolve dotless-ID drift before `toybank-report` hits `build_l2_pack` | S3b added the shard without the fix | — |

### B. Math-honesty gate gaps (S3a)

| Mode | Trigger | Symptom |
|------|---------|---------|
| **WIN keyed on extrapolation** | `verdict_at_n` = n\* < 514 constant | Measured @29 regression (factored ≥ explicit) passes the "math honesty" gate. Contradicts math-limits §4/§7 |
| **"Union" is a sum** | Overlapping shards (thin ⊂ charter by source) | 1743 vs ≈1417 distinct. The 1700 floor holds only via double counting |
| **Dead report field** | `handler_token_decision` reads `decision` / `family_decision` | Always `null` in the JSON report |
| **Python-only ref count** | `ref_token_count()` shells to `extract_refs.py` | Metrics gate never exercises the Rust extractor |

### C. Ops / runner

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Fail-fast with no partial report** | First failing shard | Exits before the aggregate JSON. A CI shard dashboard gets no per-shard status (S2c.4 partial) |
| **Sequential, not parallel** | `slice_matrix_run.sh` loop | Diagram says "Parallel CI shards". True only if CI fans out per manifest row, which nothing does yet |
| **Inconsistent cargo-missing behavior** | No cargo | `pipeline_world_io.sh` → WARN + Python fallback; `slice_matrix_run.sh` → fail. Both defensible, but undocumented |
| **Shard weight skew** | Matrix composition | charter-1k = 1350 / 1743 LOC. Toybank ×4 = 67 LOC. "6 shards" overstates breadth |

## Risk table

| Risk | Severity | Notes |
|------|----------|-------|
| B1: Python engine fails a gated shard | **high (blocker)** | Requested gate red; one-line fix verified |
| No dual-engine matrix in pulse | medium | Root reason B1 shipped green |
| Handler WIN keyed on 514 extrapolation | medium | Gate can't catch a measured regression |
| "Union" LOC double counts | medium | Bound and docs overstate scale by ~23% |
| Relative `--example` path divergence | low | No gated caller |
| Reducer JSON lacks per-shard status | low | Spec says "slice id → status" |

## MUST-PROVE before SHIP

1. `WIRING_ENGINE=python make slice-matrix-check` passes 6/6 (B1 fixed in `build_l2_pack.py`).
2. Pulse runs the matrix under `python` too, or runs `l2_pack_parity.sh` over every manifest map.
3. Re-run `make pulse-loop`, `make scale-metrics-check` and `make slice-matrix-check` (both engines). All green.

**Should land in the same PR:** handler WIN keyed on measured `factored_full < explicit_full`; matrix LOC renamed to "sum" or deduped, with the bound re-derived; `SCALE-BUILD-3-CHECKLIST.md` S3b set back to pending until item 1 holds.

## Closed since M1 eval

- `WIRING_ENGINE=bogus` is now rejected in both runners (M1 note 2).
- `l2_pack_parity.sh` now always rebuilds binaries (M1 note 4).
