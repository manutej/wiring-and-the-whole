# Adversarial — 2026-10-03 rust java refs (independent, PR #40)

**Panel:** Independent reviewer (did not implement PR #40).  
**Artifacts:** `crates/wiring-core/src/reader/java_refs.rs`, `wiring_extract_java_refs.rs`, `scripts/java_refs_parity.sh`, `scripts/wiring_core_check.sh`.

## Commands run (this review)

| Command | Result |
|---------|--------|
| `make wiring-core-check` | **PASS** — 3× validate parity; java refs parity toybank accounts (8 tokens); fineract-thin (9 tokens) |
| `cargo test` (in `crates/wiring-core`) | **PASS** — 6 tests including token-count goldens |

Do **not** treat `docs/pulse/evaluations/2026-10-03-rust-java-refs.md` as evidence; it is implementer self-SHIP with no independent command log.

## What actually shipped

- Pure-ish core: `refs_from_java_source`, `file_key`, `walk_java_refs`, `build_fragment`, JSON emit.
- Thin CLI: `wiring-extract-java-refs` (stdout JSON only).
- Gate: `java_refs_parity.sh` compares **(file, token) set** and `ref_token_count` vs Python with `--no-example-check` on **two** trees only.
- Pulse: `scripts/pulse_eval_functional.sh` invokes full `wiring_core_check.sh`.

Production paths (`pipeline_world_io.sh`, `fineract_slice_check.sh`, density probes) still call **Python** `extract_refs.py` only.

## Failure modes (operational + semantic)

### A. Silent or partial parity

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Parse semantic drift** | Comment uses Python-accepted forms Rust rejects: `//  refs:` (extra space), `//refs:` (no space) | Python extracts tokens; Rust returns `[]` for that file; gate **only fails if a fixture uses that style** (current witness does not) |
| **Inline false positive** | Code line contains substring `// refs:` inside a string before real comment | Both take first line match; Rust splits on literal `// refs:` anywhere on line (same class of bug as Python regex on line) |
| **Second refs line ignored** | Multiple `// refs:` lines in one file | Both keep first only; later refs silently dropped |
| **file_key mismatch** | Java path not under `refs_dir` (symlink, wrong arg) | Python `relative_to` errors; Rust `strip_prefix` falls back to full path — **divergence not covered by gate** |
| **Encoding** | Non–UTF-8 Java source | Rust `read_to_string` fails walk; Python `read_text(encoding="utf-8")` fails similarly — error messages differ, not gated |
| **Empty / missing dirs** | Bad CLI path | Both error; exit 1 |

### B. Gate limitations

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Pair-set-only diff** | `slice` string differs, key order differs, pretty JSON differs | Gate still **PASS** if pairs and count match |
| **Two-fixture coverage** | Regression on `witness/toybank/loans`, density slices, handler-wedge | No Rust/Python compare in `wiring-core-check` |
| **No example/evidence check in Rust** | WiringMap evidence stale vs Java refs | Python `--example` catches; Rust CLI has **no** equivalent; parity script explicitly disables example check |
| **stderr swallowed** | Python prints OK to stderr | Parity redirects stderr to `/dev/null` — harder to debug failed runs |
| **Release binary stale** | Edit Rust without rebuild before manual CLI | Script rebuilds if missing; `cargo test` uses lib path (can pass while release binary old until next gate run) |

### C. CI / ops

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Skip entire wiring-core gate** | `cargo` not on PATH | `wiring_core_check.sh` prints `SKIP` and **exit 0** — false green |
| **Dual implementation** | Fix bug in one of Python/Rust only | Drift until someone runs `make wiring-core-check` or pulse eval |
| **Python remains canonical in pipeline** | Operator assumes Rust CLI is wired | Pipeline still Python-only; Rust is parity/canary until spine migration |

## Risk table

| Risk | Severity | Notes |
|------|----------|-------|
| **Advertised “parity” is fixture-narrow, not semantic** | high | Literal `// refs:` vs Python `//\s*refs:\s*`; proved by off-fixture probes |
| **Two-tree gate + no example check** | medium | Misses wiringmap evidence drift Rust would not catch anyway |
| **Dual stack + pipeline still Python** | medium | Phase 2 adds maintenance without cutting over extract path |
| **SKIP when no cargo** | low–medium | Environment-dependent false pass |
| **Over-claim in README/spine** | low | “Parity with extract_refs.py” reads stronger than pair-set on 2 dirs |

## MUST-PROVE before calling extract “done”

1. Shared golden vectors (including whitespace variants) or one parser spec + property tests.
2. Parity on every slice that runs `extract_refs.py --example` in CI (toybank accounts at minimum in pipeline-io).
3. Either wire Rust into pipeline behind flag or document Python as sole enforcement until cutover.
4. Rust wiringmap example coverage or explicit decision that validate+extract stay split.
