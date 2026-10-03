# Rust core + multi-language readers — architecture direction (2026-10-02)

**Status:** proposed · **Not a rewrite PR** — this doc records target shape and migration phases while Python harness and Java fixtures remain the source of truth for CI today.

**Related:** [`docs/reports/2026-10-02-vision-and-capabilities.md`](../reports/2026-10-02-vision-and-capabilities.md), [`wiringmap/README.md`](../../wiringmap/README.md), [`preview/graph/README.md`](../../preview/graph/README.md).

---

## Current state (repo today)

- **Harness / tooling (what runs CI):** mostly **Python** under `scripts/` (validate, extract, pack build, reexpand gate, dogfood grading, pulse eval) plus **bash** orchestration (`verify.sh`, `pipeline_world_io.sh`, `pulse_loop_gate.sh`). Token experiments use a small **Node** dependency (`experiments/` + tiktoken).
- **Language-neutral artifacts:** **JSON** WiringMap v0 instances and [`wiringmap/schema.v0.json`](../../wiringmap/schema.v0.json); L2 packs as text (`LEGEND`, explicit, factored); frozen eval JSON under `experiments/` and `fixtures/`.
- **Stakeholder preview:** **TypeScript / Next.js** in `preview/graph/` (Mermaid from bundled toybank map; witness iframe; pipeline diagram).
- **Code under test (fixtures, not the engine):** **Java** in `witness/toybank/` (synthetic “toy bank”), `fixtures/external/fineract-handlers-thin/` (seven vendored Fineract-style handlers), and density adversarial slices. Maps are hand-curated JSON aligned to those slices; extractors are Java-specific (`// refs:` lines, `@CommandType` handler parser).
- **No Rust** in the tree yet; no repo-wide static analyzer emitting WiringMap from arbitrary codebases.

---

## Target architecture

### Core engine (Rust crate: `wiring-core`)

Single **typed** library responsible for language-agnostic operations on the wiring domain:

| Responsibility | Notes |
|----------------|--------|
| **Schema / validate** | WiringMap v0 against JSON Schema (embed or compile schema); stable error paths matching today’s `validate_wiringmap.py` messages where practical |
| **IR** | In-memory graph: units, ports, edges, junctions; optional normalized **graph IR** for Mermaid/export (shared with preview via JSON or WASM later) |
| **Extract orchestration** | Apply **evidence rules** from map instances to structured ref tokens; compare to reader output (parity with `extract_refs.py`) |
| **Pack / reexpand** | Faithfulness gate for L2 factored packs (parity with `reexpand_gate.py` / `build_l2_pack.py`) |

Design goals: **fast** validation and pack ops on large maps; **deterministic** outputs for CI; **no LLM** in the core path.

### Reader trait + per-language adapters

Readers are **plugins** (separate crates or FFI boundaries), not part of the core schema:

```text
trait WiringReader {
  fn language_id(&self) -> &str;           // e.g. "java", "python", "typescript"
  fn scan_tree(&self, root: &Path, opts: ScanOpts) -> ReaderOutput;
}

struct ReaderOutput {
  ref_tokens: Vec<RefToken>,              // file-local evidence
  optional_motifs: Vec<MotifRow>,           // e.g. CommandHandler family
}
```

| Adapter (phase order) | Scope | Parity target |
|---------------------|--------|----------------|
| **java-refs** | `// refs:` comment lines | `scripts/extract_refs.py` |
| **java-command-handler** | `@CommandType` handlers | `scripts/command_handler_parse.py` |
| **python-reader** | imports / call graph stubs (later) | new fixtures |
| **ts-js-reader** | ES modules, typed imports (later) | new fixtures |

The **core** never parses Java syntax directly; it only consumes normalized `RefToken` / motif rows from readers. That keeps the repo **language-independent** at the map and IR layer while allowing multiple extraction strategies.

### CLI and bindings

- **`wiring-cli`** (Rust binary): `validate`, `extract --reader java-refs`, `pack`, `reexpand` — eventual drop-in for hot paths in `make wiringmap-check` / `pipeline-io`.
- **Optional:** PyO3 or subprocess wrapper so `scripts/*.py` become thin shells during migration (same argv/JSON stdout contracts as today).

### Preview / TS

Keep **Next.js preview** as a consumer: load JSON or call WASM build of `wiring-core` for client-side validate/to-Mermaid later. TS does **not** need to be the core runtime; it remains the graph UI layer.

---

## Migration phases (incremental)

1. **Phase 0 — spec freeze (now)**  
   - JSON schema + frozen pulse fixtures remain canonical.  
   - This document + empty `crates/wiring-core/` scaffold.

2. **Phase 1 — validate in Rust** *(in progress on `main` via pulse branch)*  
   - Structural v0 validate in `wiring-core` + `wiring-validate` CLI; `make wiring-core-check` runs **Rust + Python** on toybank, fineract-thin, and [`repo-rust-spine.v0.json`](../../wiringmap/examples/repo-rust-spine.v0.json).  
   - Full JSON Schema via embedded schema in Rust deferred (toolchain pin); Python `jsonschema` remains authoritative for schema edge cases.

3. **Phase 2 — extract parity (Java readers)**  
   - Port ref-line and CommandHandler parsers to `wiring-reader-java*`.  
   - Golden tests: same `refs_by_file` / counts as current extract JSON in `pipeline-io`.

4. **Phase 3 — pack + reexpand**  
   - Port L2 build and reexpand gate; handler-family pack becomes a regression target (`make handler-family-pack-check`).

5. **Phase 4 — CLI owns hot path**  
   - `Makefile` targets call `wiring-cli` first; Python scripts deprecated behind feature flag or removed per target.

6. **Phase 5 — additional languages**  
   - New readers + small witness slices (Python/TS); maps still v0 JSON; no change to adversarial metrics definition.

Each phase lands as **small PRs** with pulse-loop green; no big-bang rewrite.

---

## What stays Python during transition

| Keeps Python (for now) | Why |
|------------------------|-----|
| Pulse loop orchestration, meta-evaluator hook, dogfood **question** JSON grading | Fast iteration; not performance-critical |
| CR@F95 stub, pack-blind eval harness, LLM firewall plumbing | Research/experiment lane |
| Fineract fetch/slice shell scripts | Git/sparse-checkout I/O |
| E2/E3 frozen experiment runners | Frozen baselines; migrate only when intentionally rebaselining |
| One-off research scripts under `experiments/` | Out of core path |

Python **validators/extractors/pack builders** remain until Rust parity is demonstrated on the same fixtures; then they become thin wrappers or are deleted target-by-target.

---

## Feasibility (honest)

- **Rust core for validate + IR + pack:** high feasibility; schema is JSON; graph ops are bounded; CI already provides golden outputs.
- **Java readers:** medium — regex/comment parsing today is narrow; CommandHandler motif is a defined family; full Java AST is explicitly out of scope for v0.
- **Python / TS readers:** feasible as **new** adapters once trait and golden-test pattern exist; no commitment to full language semantics in one step.
- **Risk:** dual implementation drift — mitigated by requiring pulse-loop parity before switching defaults.

---

## Non-goals (this programme)

- Replacing Fineract or vendoring full Apache trees in core  
- LLM-in-the-loop extraction in `wiring-core`  
- Rewriting witness Java or demo Next app as part of core migration  

---

## Next actionable PR (suggested)

1. Add `wiring-core` validate-only + `cargo test` golden file from `toybank-accounts.v0.json`.  
2. Wire optional `make wiringmap-check-rust` behind existing `wiringmap-check`.
