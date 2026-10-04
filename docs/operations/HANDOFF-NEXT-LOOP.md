# Handoff — next compound loop (post S4 dashboard)

**For:** fresh agent resuming cold · **Branch context:** `main` + open PR [#46](https://github.com/manutej/wiring-and-the-whole/pull/46) (scale dashboard / report).

## Where we are

| Milestone | Status |
|-----------|--------|
| S4 charter ~10k | **Merged #44** — experiments PATH LIST, 7-shard matrix, `/charter-10k` |
| Scale report + HTML dashboard | **PR #46** — `make scale-report`, `/scale-dashboard`, static HTML |
| L2 vs AST quality compare | **Scripted** — `make representation-compare` |
| S5 OpenRig large repo | **Prep only** — inventory + JSONL index scaffold |

## Performance (now visible)

Regenerate: `make scale-report` → `fixtures/scale-report/latest.v0.json`

- **7-shard matrix (Rust):** see `slice_matrix_timing.rust.total_ms` (~50 ms on CI VM).
- **Charter 10k shard (Rust):** ~8–9 ms total; **extract** dominates vs pack/reexpand.
- **Python engine:** ~10× slower on same matrix (see report JSON).

Preview: [/scale-dashboard](https://wiring-graph-preview.vercel.app/scale-dashboard) — **Pipeline performance** section at top after #46 merge.

## Token compression (what we tried)

- **L2 factored pack** vs **explicit** on 29-handler wedge: **947 vs 1923** tokens (cl100k) — lossless reexpand gate.
- **Not** compressing full 10k Java — only wired map + pack path.
- Compare doc: `docs/operations/reports/REPRESENTATION-COMPARE-LATEST.md`.

## Test agent: L2 vs AST vs raw

```bash
make representation-compare
```

- **Agent:** rule-based cold navigation on `fixtures/representation-compare/wiring_questions.v0.json`.
- **AST:** `javalang` + `@CommandType` attrs from source regex (values not in raw AST tree alone).
- **Latest scores (typical):** L2 factored/AST/raw **5/7** wiring; L2 md **6/7** (curated tables; incomplete per-unit cards for all handlers).

## View wiring

- **Comprehensive diagram:** `/charter-10k` (Mermaid from full WiringMap).
- **Docs:** `docs/operations/VIEWING-WIRING-DIAGRAMS.md`, `docs/operations/CORPUS-PROVENANCE.md`.

## Next loop priorities

1. **Merge #46** → Vercel shows performance + dashboard.
2. **S5a:** clone/pin [OpenRig](https://github.com/mvschwarz/openrig), `repo_inventory_v0.py` artifact.
3. **Extend test agent** with LLM-blind eval (existing pack-blind harness) for representation arms.
4. **Ledger L1–L4** from `PRODUCTION-RETROACTIVE-LEDGER.md`.

## Gates (copy-paste)

```bash
make pulse-loop
make scale-report && make scale-report-check
make representation-compare
```

## Do not claim

- Full Fineract 10k checkout (experiments corpus only).
- AST comparison without noting javalang + regex augmentation for annotation values.
- Repo-wide token WIN from 29-handler wedge alone without “measured wedge” qualifier.
