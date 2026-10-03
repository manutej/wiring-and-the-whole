# Evaluator (independent) — 2026-10-03 M1 Engine MVP (M1a–M1d)

**Verdict:** **SHIP** (M1a–M1d engine bundle) — **conditional:** M1d is not yet committed; the SHIP applies to the M1d hunks exactly as evaluated below and must land as its own commit before M1 is marked done.

**Reviewer:** Independent panel; did not implement any M1 milestone.

**Branch / commit reviewed:** `cursor/mvp-engine-push-cd12` @ `4d84528218f6ad3695806d8820625caac4cc2f1f` (M1a `d582e48`, M1b `faef34d`, M1c `4d84528`) **plus** uncommitted working-tree hunks for M1d:

| Uncommitted file | sha256 (prefix) | M1 role |
|------------------|-----------------|---------|
| `scripts/pipeline_world_io.sh` | `83de0ccd8050` | M1d: `WIRING_ENGINE` switch, default `rust` |
| `scripts/wiring_core_check.sh` | `de7bcc610ea6` | M1b/M1c: Python reexpand cross-check + `l2_pack_parity.sh` hook, `--bins` |

The same working tree also carries uncommitted **M2** work (charter-1k fixture, edge-recall 125 pairs, `Makefile` charter targets, `pulse_eval_functional.sh`, preview `/charter`, `toybank-report.v0.json`). M2 is out of scope here and must not be bundled into the M1d commit.

## Build specs

- `docs/operations/build-specs/M1a-java-refs-parity.md` (previously SHIP: `2026-10-03-m1a-independent.md`)
- `docs/operations/build-specs/M1b-reexpand-rust.md`
- `docs/operations/build-specs/M1c-pack-rust.md`
- M1d: **no build spec file**; judged against `MVP-CHECKLIST.md` row ("`pipeline-io` Rust path (`WIRING_ENGINE=rust`)", gate `make pipeline-io`)

## M1 scope

| Path | Milestone | State |
|------|-----------|-------|
| `crates/wiring-core/src/reader/java_refs.rs` | M1a | committed |
| `crates/wiring-core/src/pack/reexpand.rs`, `src/bin/wiring_reexpand.rs` | M1b | committed |
| `crates/wiring-core/src/pack/build.rs`, `src/bin/wiring_build_l2_pack.rs`, `scripts/l2_pack_parity.sh` | M1c | committed |
| `Makefile` `pack-v0-check` (adds `l2_pack_parity.sh`) | M1c | committed |
| `scripts/wiring_core_check.sh` (reexpand dual + L2 parity hook) | M1b/M1c | **uncommitted** |
| `scripts/pipeline_world_io.sh` | M1d | **uncommitted** |

## Done-when checklist

| # | Criterion | Result |
|---|-----------|--------|
| M1a | Rust refs regex ≡ Python `REFS_LINE`; parity on toybank + fineract-thin | **PASS** — unchanged since M1a SHIP; 8 + 9 pairs green |
| M1b.1 | `expand_factored` + legend check mirror `reexpand_gate.py` (SliceUnit + CommandHandler 5/6-arg) | **PASS** — same regexes, same skip rules (`motif`/`foreach`/blank), same sort, same `normalize_text` legend compare |
| M1b.2 | CLI 0 on toybank pack, 1 on tampered LEGEND | **PASS** — `toybank_pack_reexpand`, `rejects_tampered_legend` tests |
| M1b.3 | Hooked in `wiring_core_check.sh` | **PASS** — committed hook (Rust only); working tree adds Python cross-run on same pack |
| M1b.4 / M1c.6 | `make pulse-loop` green | **PASS** on working tree (functional eval 36/36). Committed tip in a fresh worktree fails 1 check (meta-evaluator: `craft/` is gitignored and absent) — environmental, not M1 |
| M1c.1 | `build_l2_pack_from_wiringmap` mirrors Python `collect_unit_edges` / explicit / factored / LEGEND | **PASS** on corpus — see parity sweep; two off-corpus divergences noted below |
| M1c.2 | Internal `expand(factored) == explicit` before write | **PASS** — `build.rs` L164–167 |
| M1c.3 | CLI writes `<map>.pack/{LEGEND,pack_explicit,pack_factored}.txt` | **PASS** |
| M1c.4 | `l2_pack_parity.sh` byte-compares on toybank | **PASS** |
| M1c.5 | `make pack-v0-check` = Python build + reexpand + Rust parity | **PASS** |
| M1d | `pipeline-io` runs validate / L2 build / reexpand via Rust by default; Python path retained | **PASS** (working tree) — default engine `rust`; `python` path green; reports identical except temp paths |

## Evidence (independent commands)

Run on the working tree at `/workspace` (HEAD `4d84528` + uncommitted hunks above), plus a clean `git worktree` at `4d84528` for reproducibility. No implementation edits.

| Command | Outcome |
|---------|---------|
| `make wiring-core-check` | **PASS** — validate parity (3 instances); java refs 8 + 9 pairs; reexpand Rust + Python; L2 pack Rust ≡ Python |
| `make pack-v0-check` | **PASS** — Python build, reexpand, `l2 pack parity (toybank)` |
| `WIRING_ENGINE=rust make pipeline-io` | **PASS** — `engine=rust`; toybank 8 refs / 8 edges; fineract-thin 9 / 9 |
| `WIRING_ENGINE=python make pipeline-io` | **PASS** — `engine=python`; JSON report identical to rust run except tmp paths |
| `make pipeline-io` (no env) | **PASS** — reports `wiring_engine: rust` (default confirmed) |
| `cargo test` (`crates/wiring-core`) | **PASS** 11/11 when pack present; **FAIL 3/11 on clean checkout** (see Condition 2) |
| `make pulse-loop` | **PASS** (working tree, 36/36) |
| `l2_pack_parity.sh <map>` sweep over every tracked `*.v0.json` with `units` + charter-1k | **PASS** on 11 maps (toybank ×3 + preview copy, fineract-thin ×2, density d1/d2/d2-invalid/d3, charter-1k). `repo-rust-spine` fails **identically** in both engines (`internal error: expand(factored) != explicit`) — existing builder limit, not drift |
| cargo absent from `PATH` | **PASS** — `WARN: cargo missing; falling back to python engine`, pipeline green |

### Clean-checkout reproduction (committed tip `4d84528`, fresh worktree)

```
make wiring-core-check   -> ERROR: missing toybank pack at .../toybank-accounts.v0.pack   (exit 2)
cargo test               -> 8 passed; 3 failed (toybank_pack_reexpand, rejects_tampered_legend,
                            toybank_build_matches_python_golden)
make pack-v0-check       -> PASS  (generates the pack)
make wiring-core-check   -> PASS
cargo test               -> 11 passed
```

`*.v0.pack/` is gitignored, so the M1b/M1c gates and their unit tests depend on a pack generated by an earlier target. `pulse_eval_functional.sh` builds the pack first (L35), so `pulse-loop` is self-consistent; standalone runs on a fresh clone are not.

## Parity review (code read)

Rust ports are line-for-line mirrors of the Python sources: same regexes, same `BTreeMap`/`BTreeSet` ordering as Python `sorted()` (UTF-8 byte order ≡ code-point order), same trailing-newline normalization, same internal re-expansion invariant. Two **off-corpus** divergences in `build.rs`, both reproduced with synthetic inputs:

| Input | Python `build_l2_pack.py` | Rust `wiring-build-l2-pack` |
|-------|---------------------------|-----------------------------|
| Dotless unit id `unit:Foo` | `short_unit` returns `unit:Foo` → `ValueError: bad inst row` (crash) | strips prefix → `Foo`, builds pack (exit 0) |
| Port without `#` (`port:b.B`) | emits `edge A -> B#` (exit 0) | `port missing # symbol` (exit 1) |

Neither appears in any gated fixture. The uncommitted M2 file `wiringmap/examples/toybank-report.v0.json` (`unit:ReportModule`) does hit the first row: Python crashes, Rust succeeds. No script consumes it today.

## SHIP rationale

All four requested gates are green, and the Rust and Python engines produce byte-identical L2 packs on every in-repo wiringmap the Python builder accepts. Reexpand semantics match `reexpand_gate.py`, including the CommandHandler rows Rust doesn't yet build. `pipeline-io` defaults to Rust for validate, L2 build and reexpand, keeps a working Python path, and falls back cleanly when cargo is missing. Rust is still a builder-side parity port; Python stays the oracle in every dual gate.

## Conditions (must hold before M1 is marked done / integration PR)

1. **Commit M1d separately.** Commit `scripts/pipeline_world_io.sh` and `scripts/wiring_core_check.sh` as evaluated (hashes above) in their own `feat(mvp): M1d …` commit. Keep the M2 charter, edge-recall and preview hunks out of it. The pushed branch currently has no M1d.
2. **Clean-clone gate.** Make `wiring_core_check.sh` build the toybank pack when it is missing (e.g. `python3 scripts/build_l2_pack.py …` or the Rust CLI), and stop the three pack unit tests from reading the gitignored `*.v0.pack/`. Either generate into a temp dir in-test or commit a golden fixture outside the ignore glob. Fix this before the integration PR so a reviewer's fresh `make wiring-core-check` / `cargo test` is green.

## Non-blocking notes

1. **Off-corpus builder drift** (table above): pick one behavior for dotless unit ids and `#`-less ports, then add a dual negative vector to `l2_pack_parity.sh`. Resolve before M2 maps (e.g. `toybank-report`) flow through `build_l2_pack`.
2. `WIRING_ENGINE` accepts any value. `WIRING_ENGINE=bogus` silently runs the Python path and reports `"wiring_engine": "bogus"`. Reject values other than `rust`/`python`.
3. `pipeline-io` with `engine=rust` still runs Python for `extract_refs.py --example` and `grade_l1_questions.py`. "Rust path" means validate + L2 build + reexpand only. Don't claim spine `extract_py → rust` cutover.
4. `l2_pack_parity.sh` only builds the binary when it is missing. If you run it standalone (e.g. via `make pack-v0-check`) after editing Rust sources, it can compare against a stale binary. `wiring_core_check.sh` always rebuilds first, so that gate is unaffected.
5. Add an M1d build spec (`docs/operations/build-specs/M1d-*.md`) so the done-when criteria are written down, not taken from the checklist row.
6. `MVP-CHECKLIST.md` (working tree) already marks M1d/M2a/M2b **done** before commit and eval. Update it after Condition 1 lands.
