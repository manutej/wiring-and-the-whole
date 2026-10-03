# Evaluator (independent) — 2026-10-03 M1a java refs parity

**Verdict:** **SHIP** (M1a build spec only)

**Reviewer:** Independent panel; did not implement M1a.

**Branch / commit reviewed:** `cursor/mvp-engine-push-cd12` @ `d582e48199cb34f8bd348accaae94840f970994d` (M1a-relevant hunks only; same commit also adds compound-build ops docs — out of M1a gate).

## Build spec

`docs/operations/build-specs/M1a-java-refs-parity.md`

## M1a scope in commit

| Path | M1a? |
|------|------|
| `crates/wiring-core/src/reader/java_refs.rs` | yes — regex-aligned `refs_from_java_source` + unit test |
| `crates/wiring-core/Cargo.toml`, `Cargo.lock` | yes — `regex` dependency |
| `scripts/java_refs_parity.sh` | no diff (contract unchanged) |
| `docs/operations/*` (SOP, checklist, build log, M1b stub) | no — bundled in commit, not required for M1a SHIP |

## Done-when checklist

| # | Criterion | Result |
|---|-----------|--------|
| 1 | `refs_from_java_source` matches Python `REFS_LINE = re.compile(r"//\s*refs:\s*(.+)$")` per line; first match wins | **PASS** — `Regex::new(r"//\s*refs:\s*(.+)$")` + line loop + early return |
| 2 | Unit tests: `// refs:`, `//  refs:`, `//refs:` | **PASS** — `parses_single_refs_line`, `parses_whitespace_variants_like_python` (7/7 `cargo test`) |
| 3 | `scripts/java_refs_parity.sh` unchanged; toybank + fineract-thin | **PASS** — zero diff in commit; gate OK 8 + 9 tokens |
| 4 | `make wiring-core-check` and `make pulse-loop` green | **PASS** — see evidence |

## Evidence (independent commands)

Evaluated on clean tree at `d582e48` (`git reset --hard origin/cursor/mvp-engine-push-cd12`; no implementation edits).

| Command | Outcome |
|---------|---------|
| `make wiring-core-check` | **PASS** — validate parity (3 instances); java refs parity toybank (8 pairs); fineract-thin (9 pairs) |
| `cargo test` (`crates/wiring-core`) | **PASS** — 7 tests including whitespace variants |
| `scripts/java_refs_parity.sh` (both fixtures) | **PASS** |
| `make pulse-loop` | **PASS** — functional eval 35/35; wiring-core hook green |

Prior independent review (`docs/pulse/evaluations/2026-10-03-rust-java-refs-independent.md`) documented Rust literal `// refs:` drift; this commit closes that gap for M1a.

## SHIP rationale

M1a is a **builder-only** parity fix: Rust extraction now uses the same line regex semantics as `scripts/extract_refs.py`, with direct unit coverage for the three comment spellings and unchanged integration gates still green on witness trees.

## Non-blocking notes

1. Same commit carries MVP compound-build documentation and M1b spec stub — keep MR/review scope explicit so M1a is not confused with later milestones.
2. Pipeline and `--example` wiringmap checks remain Python-enforced (explicitly out of M1a scope).
3. Parity gate remains pair-set equality on two directories; semantic regressions on unlisted slices still require expanded fixtures or CI paths.

## Conditions (unchanged from Phase 2)

Do not mark spine `extract_py → rust` complete or claim full-repo semantic parity until pipeline cutover or broader golden vectors land.
