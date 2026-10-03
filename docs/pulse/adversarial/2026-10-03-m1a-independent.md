# Adversarial — 2026-10-03 M1a java refs parity (independent)

**Panel:** Independent reviewer (did not implement M1a).  
**Target:** `cursor/mvp-engine-push-cd12` @ `d582e48` — **M1a hunks only** (`java_refs.rs`, `regex` dep, tests).  
**Spec:** `docs/operations/build-specs/M1a-java-refs-parity.md`

## Commands run (this review)

| Command | Result |
|---------|--------|
| `make wiring-core-check` | **PASS** — validate 3×; java refs 8 + 9 token parity |
| `cargo test` (`crates/wiring-core`) | **PASS** — 7/7 |
| `scripts/java_refs_parity.sh` ×2 | **PASS** |
| `make pulse-loop` | **PASS** — 35 functional; wiring-core hook includes java refs parity |

Tree pinned to `origin/cursor/mvp-engine-push-cd12` at `d582e48` without modifying M1a implementation.

## What M1a actually changed

- Replaced literal `line.split("// refs:")` with compiled `//\s*refs:\s*(.+)$` (Python `REFS_LINE` equivalent).
- Tokenization after capture: `trim` + `split_whitespace` (aligns with Python `strip().split()` for normal whitespace).
- Added `parses_whitespace_variants_like_python` covering `//  refs:`, `//refs:`, and indented `// refs:`.
- Added `regex = "1.10"` to `wiring-core` — new transitive lockfile entries.

**Unchanged:** `scripts/java_refs_parity.sh`, CLI shape, walk/file_key, pipeline Python paths.

## Failure modes (post-M1a)

### A. Parser / semantics (reduced vs pre-M1a)

| Mode | Trigger | Symptom | M1a mitigated? |
|------|---------|---------|----------------|
| **Whitespace variant miss** | `//  refs:`, `//refs:` | Pre-M1a Rust returned `[]`; Python extracted | **Yes** — regex + unit tests |
| **Inline false positive** | Non-comment text before EOL matching `//\s*refs:` | First line match wins; same class as Python `.search(line)` | Partial — both languages, not M1a-specific |
| **Second refs line ignored** | Multiple `// refs:` in one file | Silent drop after first | By design (Python parity) |
| **CRLF vs LF** | `\r` in line | Regex `$` may differ from Python `$` on `\r\n` sources | **Unproven** — no CRLF unit vector; fixtures likely LF |
| **Unicode whitespace** | NBSP or exotic space before `refs:` | `\s` in Rust vs Python may differ for rare chars | **Unproven** — not in spec’s three forms |

### B. Gate / ops (unchanged from Phase 2)

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Two-tree coverage** | Regression on loans, density, handler-wedge Java | `java_refs_parity.sh` never compares those trees |
| **Pair-set-only diff** | Slice string or JSON ordering differs | Gate still **PASS** if pairs + count match |
| **No Rust `--example`** | WiringMap evidence stale | Python `--example` catches; Rust CLI does not; parity uses `--no-example-check` |
| **SKIP when no cargo** | `cargo` missing on PATH | `wiring_core_check.sh` can SKIP with exit 0 |
| **Dual stack** | Fix only Python in pipeline | Production extract stays Python until spine migration |

### C. Commit / process

| Mode | Trigger | Symptom |
|------|---------|---------|
| **Scope mixing** | Single commit = M1a code + compound SOP + M1b stub + build log | Reviewers may merge ops docs while debating parser; revert risk spans non-M1a files |
| **Dependency surface** | `regex` crate in `wiring-core` | Supply-chain / MSRV / compile time — acceptable for M1a but new moving part |

## Risk table

| Risk | Severity | Notes |
|------|----------|-------|
| **False “full parity” narrative** | medium | M1a fixes line regex only; gate still two fixtures, no example check |
| **CRLF / exotic whitespace** | low | Spec did not require; add vectors if Windows-checked Java enters CI |
| **Bundled non-M1a docs in one commit** | low | Process noise, not a parser defect |
| **Pipeline still Python-only** | medium | Expected out of scope; ops must not assume Rust extract in production |

## MUST-PROVE before extract spine cutover (beyond M1a)

1. Parity on every CI slice that runs `extract_refs.py --example` (not just toybank + fineract-thin pair sets).
2. Golden vectors for edge line endings and multi-line files if sources leave LF-only witnesses.
3. Explicit pipeline flag or replacement plan — M1a does not wire Rust into `pipeline_world_io.sh`.

## Verdict alignment

M1a build-spec **done-when** items are satisfied; remaining rows above are **Phase 2 / spine** debt, not blockers for labeling this milestone SHIP.
