# Build log — senior architecture review (2026-10-03)

| Field | Value |
|-------|--------|
| **Role** | Senior architecture (COMPOUND-BUILD-SOP) |
| **Branch** | `cursor/mvp-engine-push-cd12` |
| **Review SHA** | `d582e48199cb34f8bd348accaae94840f970994d` |
| **Scope** | `crates/wiring-core` vs [`docs/architecture/2026-10-02-rust-core-multireader.md`](../../architecture/2026-10-02-rust-core-multireader.md) |
| **Craft lens** | [manutej/craft](https://github.com/manutej/craft) — effects-and-purity, trustworthy-tests, robustness-at-boundaries, right-sized-design |
| **Code changes** | None (review artifact only) |

## Executive summary

`wiring-core` is a **credible Phase 1–2 wedge**: structural validate + Java `// refs:` extract with **dual-run gates** (`make wiring-core-check`) against Python on three maps and two fixture trees. That matches the **incremental migration** story in the architecture doc, with deliberate shortcuts (no JSON Schema in Rust, no `WiringReader` trait, no graph IR surface, no pack/reexpand, no unified `wiring-cli`).

**Verdict for M1a:** architecture **direction holds**; **implementation shape drifts** from the target crate boundaries and public API sketched on 2026-10-02. Drift is mostly **acceptable for MVP** if treated as **technical debt with explicit paydown** before M1d (`WIRING_ENGINE=rust` in pipeline-io). The highest-risk drift is **semantic parity claims** (validate ≈ schema; extract ≈ `extract_refs.py`) while gates are **narrower** than production Python paths.

**Gate evidence (this review):**

| Command | Result |
|---------|--------|
| `make wiring-core-check` | PASS — 3× validate (Rust + Python); java refs 8 + 9 token parity |
| `cargo test --manifest-path crates/wiring-core/Cargo.toml` | PASS — 7 tests |

---

## Alignment matrix (target vs shipped)

| Architecture target ([2026-10-02](../../architecture/2026-10-02-rust-core-multireader.md)) | Shipped on branch | Alignment |
|---------------------------------------------------------------------------------------------|-------------------|-----------|
| Core: schema / validate | `validate_v0.rs` + `wiring-validate` | **Partial** — structural checks only; schema file read but not applied |
| Core: in-memory graph IR | Comment in `lib.rs`; serde structs used only inside validate | **Missing** — no exported IR types or graph ops |
| Core: extract **orchestration** (map evidence vs reader output) | Not present | **Missing** — Rust extract is standalone JSON fragment |
| Core: pack / reexpand | Not present | **Missing** (Phase 3) |
| Readers as plugins (`WiringReader`, separate crates) | `reader::java_refs` inside `wiring-core` | **Drift** — doc Phase 2 note allows in-crate path; target diagram still says `wiring-reader-java*` |
| Core never parses Java syntax | Java regex parser in core crate | **Drift** — acceptable short-term; violates stated boundary until split |
| `wiring-cli` subcommands | Two binaries: `wiring-validate`, `wiring-extract-java-refs` | **Drift** — fine for Phase 1–2 if renamed/merged at Phase 4 |
| `make wiring-core-check` on toybank + fineract + repo-rust-spine | Matches `scripts/wiring_core_check.sh` | **Match** |
| Python remains authoritative for schema edge cases | Rust + Python both run on same instances | **Match** |
| Pipeline hot path in Rust | `pipeline_world_io.sh` still Python extract/validate/pack | **Match** (not started — M1d) |

---

## Drift register (doc ↔ code)

### D1 — “Graph IR” named but not delivered

- **Doc:** core owns typed graph (units, ports, edges, junctions) and optional normalized graph IR for export.
- **Code:** `validate_v0_json` deserializes a subset of fields, runs id/kind checks, drops the struct. No `WiringMap` public type, no edge evidence, no Mermaid path.
- **Risk:** Preview and pack work will re-parse JSON or duplicate shapes unless IR lands before Phase 3.
- **Paydown:** Introduce `wiring_core::model::WiringMapV0` (or similar) as the single deserialize target; validate operates on that type; future pack reads the same type.

### D2 — Validate ≠ JSON Schema (intentional, easy to forget)

- **Doc:** embed or compile schema; stable error paths like Python where practical.
- **Code:** `validate_files` reads schema path then ignores content (`_schema_text`). Checks are a hand-maintained subset (version, meta, unit id prefix, duplicate ids, edge endpoints, five `edge_kind` values).
- **Gap vs schema:** port id pattern, junction shape, unit id charset, `additionalProperties`, edge evidence fields, etc. are **not** enforced in Rust.
- **Mitigation today:** dual gate with `validate_wiringmap.py` on frozen instances — **does not** prove Rust rejects the same invalid instances as Python on unseen inputs.
- **Paydown:** golden **invalid** fixtures (expect same pass/fail) or embed schema when toolchain pin lifts.

### D3 — Reader boundary collapsed into core

- **Doc:** `wiring-reader-java*` crates; `WiringReader` + `ReaderOutput` / `RefToken`.
- **Code:** `reader::java_refs` with ad hoc `ExtractFragment` JSON matching Python script output shape.
- **Spine map:** `repo-rust-spine.v0.json` still lists junction `crates.wiring-reader-java` as **planned** while implementation lives under `wiring-core`.
- **Paydown:** Before a third reader, extract trait + move Java to `crates/wiring-reader-java` (workspace member) to avoid `wiring-core` becoming a language grab bag.

### D4 — Extract parity scope vs production extract

- **Doc:** parity with `extract_refs.py` including orchestration against map evidence (Python `--example`).
- **Code / gates:** `java_refs_parity.sh` uses Python `--no-example-check`; only **two** trees; compares `(file, token)` set + count.
- **Production:** pipeline and slice checks still call Python with example/evidence semantics.
- **Paydown:** M1a done-criteria should add at least one gate with `--example` or Rust-side evidence check; extend parity to every CI tree that runs extract.

### D5 — CLI factoring vs `wiring-cli`

- Two release binaries duplicate clap/bootstrap patterns. Architecture targets one orchestrator for Phase 4 Makefile cutover.
- **Paydown:** optional `wiring-cli` stub with subcommands delegating to library fns; keep thin bins as aliases until deprecation.

### D6 — Repo layout: isolated crate lockfile

- Single `crates/wiring-core/Cargo.toml` + local `Cargo.lock`; no workspace root. Fine for one crate; blocks clean multi-crate reader split.
- **Paydown:** root `Cargo.toml` workspace when adding `wiring-reader-java` or `wiring-cli`.

### D7 — Architecture doc “current state” stale

- Doc opening still says **“No Rust in the tree yet”** while Phase 1–2 sections were updated inline. Readers skimming §Current state get the wrong picture.
- **Paydown:** doc edit (separate PR) — refresh §Current state; keep migration phases as source of truth.

### D8 — Operational false-green paths

- `wiring_core_check.sh`: missing `cargo` → `SKIP` exit **0** (documented in adversarial review).
- Parity script redirects Python stderr to `/dev/null`.
- **Paydown:** CI images must always have Rust; consider `SKIP` → exit 1 in pulse-eval contexts only.

---

## Craft anti-patterns (findings)

Applied per COMPOUND-BUILD-SOP §Craft. Severity: **blocker** = fix before M1× SHIP; **debt** = track on checklist; **nit** = optional polish.

### Effects-and-purity

| ID | Anti-pattern | Where | Severity |
|----|--------------|-------|----------|
| C-E1 | **“Pure” module performs filesystem walk** | `walk_java_refs`, `walk_java_files` in `reader/java_refs.rs` | **debt** — I/O belongs in binary or a thin `io` module; keep `refs_from_java_source` / `build_fragment` pure (good split already started). |
| C-E2 | **Library API reads paths** | `validate_files` in `lib.rs` | **debt** — prefer `validate_v0_json(&Value)` at boundary; file IO only in `wiring-validate`. |
| C-E3 | **Dual purity story in README** | “Pure parser” vs walk in same module | **nit** — clarify “pure token parse; CLI owns walk”. |

### Trustworthy-tests

| ID | Anti-pattern | Where | Severity |
|----|--------------|-------|----------|
| C-T1 | **Count-only goldens** | Token count 8/9 tests | **debt** — counts can match with wrong per-file distribution; gate uses pair set (better) but unit tests don’t assert full pair equality vs Python JSON. |
| C-T2 | **No invalid-instance tests for Rust validate** | Only `rejects_bad_version` | **debt** — pair with Python on a small invalid corpus before claiming validate parity. |
| C-T3 | **Release vs test profile drift** | Gate builds `--release`; dev `cargo test` uses debug lib | **nit** — gate rebuilds; document for operators running CLI manually. |
| C-T4 | **Whitespace regex parity** | `parses_whitespace_variants_like_python` | **good** — addresses prior literal-split drift; keep vectors in one shared fixture file (JSON or `.txt`) for Python + Rust tests. |

### Robustness-at-boundaries

| ID | Anti-pattern | Where | Severity |
|----|--------------|-------|----------|
| C-B1 | **`file_key` silent fallback** | `strip_prefix` fail → full path | **debt** — Python `relative_to` errors; Rust/Python can diverge on bad inputs (not gated). |
| C-B2 | **First matching refs line only** | Both Python and Rust | **accepted** — document as v0 contract; add test if spec changes. |
| C-B3 | **SKIP on missing toolchain** | `wiring_core_check.sh` | **blocker** for environments claiming M1 complete without Rust — pulse should fail closed where M1 is required. |
| C-B4 | **Schema path required but unused** | CLI always passes `--schema` | **nit** — confusing UX; either use schema or drop flag until embedded. |

### Right-sized-design

| ID | Anti-pattern | Where | Severity |
|----|--------------|-------|----------|
| C-R1 | **Aspirational module docs** | `lib.rs` “graph IR” | **debt** — doc/code mismatch erodes trust; trim comment or ship minimal public `WiringMapV0` type. |
| C-R2 | **Regex crate for one line pattern** | `java_refs.rs` | **acceptable** — matches Python `re`; alternative is hand-rolled scanner (not worth it). |
| C-R3 | **Pinned clap patch version** | `Cargo.toml` `=4.4.18` | **debt** — document toolchain pin reason (likely MSRV/agent env); revisit with workspace. |
| C-R4 | **Over-broad `validate_instance(_schema, …)`** | Public API ignores schema | **debt** — rename or wire schema to avoid false API promise. |

---

## What is well aligned (keep)

1. **Incremental phases with pulse green** — no big-bang; Python stays in loop until parity proven.
2. **Thin CLIs, logic in library** — correct direction for PyO3/subprocess wrappers later.
3. **Frozen instance triple** in validate gate — includes meta `repo-rust-spine` map (dogfood spine is first-class).
4. **Deterministic JSON** — `BTreeMap` for `refs_by_file` stabilizes output vs Python dict ordering concerns.
5. **Independent adversarial note** ([`docs/pulse/adversarial/2026-10-03-rust-java-refs-independent.md`](../../pulse/adversarial/2026-10-03-rust-java-refs-independent.md)) — gate limits documented; architecture review concurs.

---

## Recommended sequencing (architecture-only; not implemented here)

Priority order for builders on M1 → M1d without widening drift:

1. **Truth in naming** — adjust docs/comments or export minimal `WiringMapV0` type (D1, C-R1).
2. **Close M1a** — shared regex/vector fixture; parity with `--example` on toybank accounts (D4, C-T1).
3. **Invalid validate corpus** — dual-run fail/pass matrix (D2, C-T2).
4. **Workspace + reader crate split** — before CommandHandler reader (D3, D6).
5. **M1b/M1c** — pack/reexpand in core library (architecture Phase 3) before `wiring-cli` merge (D5).
6. **Pipeline flag** — Rust path behind `WIRING_ENGINE=rust` only after 1–3 are green (architecture Phase 4).

---

## Relation to MVP checklist

| Checklist ID | Arch review stance |
|--------------|-------------------|
| M1a | **Near** — gates green; craft items C-B3, C-T4, D4 remain for “done” vs “green”. |
| M1b–M1c | **Not started** — no drift concern yet; do not fold pack into validate crate without IR type (D1). |
| M1d | **Blocked** on pipeline integration + fail-closed CI Rust presence (D8, C-B3). |
| M1× independent eval | Use this doc + adversarial doc; architecture does not substitute eval SHIP. |

---

## Monitoring line

| UTC | Phase | Actor | Result |
|-----|-------|-------|--------|
| 2026-10-03 | M1 arch review | senior architecture | Drift register + craft anti-patterns logged; gates PASS at `d582e48` |
