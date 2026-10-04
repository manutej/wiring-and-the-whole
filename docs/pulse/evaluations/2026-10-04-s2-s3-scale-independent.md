# Evaluator (independent) — 2026-10-04 Scale Build S2 + S3 bundle

**Verdict:** **NO-SHIP** (S2+S3 bundle as committed). The blocker is a single small fix (B1). Once B1 lands and the dual-engine matrix is gated in pulse, re-run the four gates below and this can flip to **SHIP** without re-review of the rest.

**S2 alone (`2ddb287`):** would be **SHIP**. All S2a–S2d done-when criteria pass, and the 5-shard matrix is green under both engines.

**Reviewer:** Independent evaluator; did not implement S2 or S3. No product code changed in this review.

**Branch / commits reviewed:** `cursor/scale-build-2-cd12` @ `79b0708` (S3, local commit not yet on remote at review start) on top of `2ddb287` (S2) and `de38de4` (skill doc). Base `main` @ `cff12eb`.

## Requested gates

| Command | Result |
|---------|--------|
| `make pulse-loop` | **PASS** — verify green; functional eval **39 passed, 0 failed** (matches build log) |
| `make scale-metrics-check` | **PASS** — charter 29 files / 1350 LOC / 90 ref tokens; 6 slices; 125 pairs; handler parsed 29; matrix sum 1743 |
| `make slice-matrix-check` (default `rust`) | **PASS** — 6/6 shards |
| `WIRING_ENGINE=python make slice-matrix-check` | **FAIL (exit 2)** — `SLICE MATRIX FAIL: toybank-report: pack` |

All four reproduced identically in a clean `git worktree` at `79b0708` (packs are gitignored, so this is a fresh-clone check). At `2ddb287` (S2 only, 5 shards) the Python matrix passes.

## Blocker

### B1 — Python engine crashes on the S3 `toybank-report` shard (Rust/Python pack divergence)

```
ValueError: bad inst row: 'inst SliceUnit(unit:ReportModule, edges=[])'
```

**Root cause:** `scripts/build_l2_pack.py` `short_unit()` only strips the `unit:` prefix via `split(".")[-1]`. A dotless id such as `unit:ReportModule` is returned unchanged. Python then builds two units: a phantom `unit:ReportModule` with no edges, and `ReportModule` with the two port-derived edges. The internal self-check crashes on the colon. Rust strips the prefix and emits the correct pack: `ReportModule -> accounts.Money, loans.Money`.

**Why it blocks:**

- S2c done-when #2 says the runner "honors `WIRING_ENGINE`", and S2a makes `python` one of exactly two supported engines. Under S3 the supported `python` engine fails a gated shard.
- `l2_pack_parity.sh` swept over all 6 manifest maps: 5 are byte-identical, and `toybank-report` diverges. Python is still the oracle in every dual gate, so the oracle can't build a shard the matrix claims.
- This divergence was **already flagged** in `2026-10-03-m1-engine-independent.md` (non-blocking note 1: "Resolve before M2 maps (e.g. `toybank-report`) flow through `build_l2_pack`"). S3b routed that map through `build_l2_pack` without resolving it.
- Pulse stays green because no check runs the matrix with `WIRING_ENGINE=python`.

**Minimal fix (verified in a scratch copy outside the repo, not committed):**

```python
def short_unit(unit_id: str) -> str:
    if unit_id.startswith("unit:"):
        return unit_id.removeprefix("unit:").split(".")[-1]
    return unit_id
```

With this change, Python output is byte-identical to Rust for `toybank-report`, `toybank-accounts` and `fineract-charter-1k` (`LEGEND.txt`, `pack_explicit.txt`, `pack_factored.txt`).

**Done when:**

1. Apply the fix above (or an equivalent).
2. `WIRING_ENGINE=python make slice-matrix-check` passes on 6/6 shards.
3. Add a pulse check for the Python-engine matrix, or run `l2_pack_parity.sh` over every manifest map, so this can't regress silently.

## S2 done-when

| # | Criterion | Result |
|---|-----------|--------|
| S2a.1 | `pipeline_world_io.sh` rejects invalid `WIRING_ENGINE` | **PASS** — pulse check `expect_exit 1 WIRING_ENGINE=bogus` |
| S2a.2 | `slice_matrix_run.sh` same rule | **PASS** — manual `WIRING_ENGINE=bogus` exits 1 (not gated in pulse) |
| S2a.3 | pipeline-io + slice matrix green on `rust` | **PASS** |
| S2b | `l2_pack_parity.sh` always rebuilds bins | **PASS** — unconditional `cargo build --release --bins` (closes M1 note 4) |
| S2c.1–3 | Manifest ≥5 slices; runner per slice; in pulse | **PASS** at S2 tip; **#2 broken by S3** (B1) |
| S2c.4 | JSON aggregate "slice id → status" | **Partial** — emits one overall `status: ok` plus a list of IDs, and only on full success. Exits on the first failing shard, so there is no per-shard status map |
| S2d.1 | Rust `--example` / `--no-example-check` | **PASS** — same default-example behavior as Python |
| S2d.2 | `java_refs_example_parity.sh` green on 3 slices | **PASS** — positive cases only (see adversarial doc) |
| S2d.3 | `java_refs_parity.sh` passes `--no-example-check` | **PASS** |

Negative `--example` parity, checked manually: loans refs against the accounts map fail in **both** engines with the **identical 16-pair mismatch set**. A missing example file exits 1 in both. `cargo test`: 12/12.

## S3 done-when

| ID | Item | Result |
|----|------|--------|
| S3a | `scale-metrics-check` | **PASS** with caveats M1 and M2 below. Each of the five bounds trips when tightened by one (charter max LOC, slices, pairs, parsed, sum LOC), so the gate is not tautological |
| S3b | 6-shard matrix incl. `toybank-report` | **FAIL** under `python` (B1); PASS under `rust` |
| S3c | `docs/SCALE-DIAGRAMS.md` + preview `/scale` | **PASS** — `tsc --noEmit` clean; `next build` prerenders `/scale`; all 5 TS diagram sources are mirrored verbatim in the markdown. Visual Mermaid render not checked |
| S3d | Math limits refresh | **Partial** — the build-log row asserts alignment, but `2026-10-03-math-limits.md` was not updated, and the gate reads the field that doc says not to over-read (M1) |

## Math cross-check vs `2026-10-03-math-limits.md`

| Claim | Independent recomputation | Verdict |
|-------|---------------------------|---------|
| Charter ~1350 LOC | `find … -name '*.java' \| xargs cat \| wc -l` = **1350**, 29 files; within frozen [1300, 1600] | **Solid** |
| 125 recall pairs | 8+8+8+9+2+90 = **125**; `make edge-recall-sample-check` OK; charter 90 pairs = charter 90 ref tokens | **Solid** |
| Handler parsed 29 | `manifest.json` `parsed: 29`, `skipped_count: 1` (§3: 30 raw / 29 / 1) | **Solid** |
| Token report | `handler_family_token_report.py` live output **== frozen** JSON; F = 98+54 = 152; n\* = ⌈152/(58−26)⌉ = **5**; measured @29: 947 < 1923 (Δ 976) | **Solid** |
| Breakeven "WIN" in gate | Gate checks `breakeven.verdict_at_n`, the **514-constant extrapolation** (§4: "do not treat as measured") | **Mis-keyed** (M1) |
| "~1743 LOC touched" / "matrix union" | Sum is 1743, but all 7 `fineract-handlers-thin` files are the same Fineract handlers as in charter-1k (differ only in `// refs:` lines). Distinct-source LOC ≈ **1417**, under the frozen `min_java_loc_touched_by_matrix: 1700` | **Overstated** (M2) |

## Must-fix before integration PR (non-blocking individually)

- **M1 — Key the handler WIN on measured data.** With `tokens.factored_full` set to 5000 (measured @29 now loses), `scale-metrics-check` still exits 0, because `verdict_at_n` stays `"WIN"`. Gate on `factored_full < explicit_full` (measured, n = 29). Keep `verdict_at_n` as display-only. Also, `handler_token_decision` always prints `null`: the report reads `decision` / `family_decision`, and neither key exists.
- **M2 — Rename and recompute "union".** `matrix_union_loc` sums per-slice LOC. Either dedupe by source (the thin ⊂ charter handlers) or rename it to `matrix_sum_java_loc` and re-derive the 1700 bound. Today the bound is met only by counting 7 handlers twice. Update the S3 build-log and diagram wording to match.

## Non-blocking notes

1. `pipeline_world_io.sh` still silently falls back to Python when cargo is missing. `slice_matrix_run.sh` fails closed. S2a only specifies invalid-value rejection, so this is consistent with the spec, but the two runners now behave differently.
2. Relative `--example` paths resolve against the **cwd** in Rust and against the **repo root** in Python. From `/tmp`, Rust exits 1 and Python exits 0. No gated caller is affected.
3. The "Parallel CI shards" diagram is aspirational. `slice_matrix_run.sh` runs shards sequentially, and the stdout "reducer" JSON echoes the manifest IDs rather than per-shard status.
4. The 6-shard matrix is dominated by charter-1k (1350 of 1743 LOC). Together, the four toybank shards are 67 LOC.
5. `SCALE-BUILD-3-CHECKLIST.md` marks S3b **done**. Revert it to pending until B1 lands.
