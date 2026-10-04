# Independent note — L2 vs AST representation compare

**Scope:** 29-handler e3 wedge · test agent on 7 wiring/topology questions · cl100k tokens.

## Token compression (measured)

| Rep | Tokens | vs L2 factored |
|-----|-------:|---------------:|
| L2 factored (+ legend) | 1,045 | 1.0× |
| L2 explicit (+ legend) | 2,021 | 1.9× |
| L2 interface markdown | 813 | 0.8× (curated prose) |
| AST struct (javalang + CommandType attrs) | 5,241 | 5.0× |
| Raw Java pool | 11,962 | 11.5× |

Handler-family pack report (legend+motif+inst only): **947** factored vs **1923** explicit — same order of ~2× WIN with reexpand gate.

## Test agent quality (this harness)

| Rep | Pass / 7 | Wiring pass rate | N/A |
|-----|---------:|-----------------|-----|
| L2 markdown | 6 | 75% | 0 |
| L2 factored | 5 | 100% | 2 (meta/path) |
| L2 explicit | 4 | 100% | 3 |
| AST struct | 5 | 100% | 2 |
| Raw Java | 5 | 100% | 2 |

**L2 md** wins **meta** (experiments path) and **pool counts** via tables; loses one row when per-unit cards omit a handler (CloseLoan action only in catalog table — fixable by complete cards or regex on catalog).

**L2 factored** answers all wiring Qs with inst-row fields; cannot answer meta without prose.

**AST** matches wiring when `@CommandType` values are augmented from source (javalang alone drops annotation arguments). Call-site `disburseLoan` is visible; no cross-handler edge list.

## Quality vs AST (conceptual)

| Dimension | L2 operadic pack | AST struct |
|-----------|------------------|------------|
| Cross-unit wiring | **Curated edges / inst motif** | Per-file calls only |
| Token budget at scale | **Designed to shrink** | Grows with syntax noise |
| Lossless round-trip | **reexpand gate** | N/A |
| Refactor / IDE tasks | Weak | **Strong** |
| Spring DI / junctions | **Named in map** | Invisible without analysis |

## Relation to E3 pilot

E3 reported factored packs at **~63% of explicit tokens** with **B ≥ A** comprehension on audit pool. This harness is colder and rule-based (not LLM): it shows **no wiring comprehension tax** on factored vs explicit for encoded questions — both score 100% wiring on answerable items. Markdown adds navigation affordances at similar token size to factored.

## Verdict

**SHIP** as an engineering compare harness; not a CR@F95 claim. Next: blind LLM arm on same question bank.
