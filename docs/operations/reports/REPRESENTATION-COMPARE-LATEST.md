# Representation compare (L2 vs AST vs raw)

Generated 2026-10-04T01:03:51Z · git `3fe1c7a`

## Token size (cl100k_base, 29-handler wedge)

| Representation | Tokens | vs L2 factored |
|----------------|-------:|---------------:|
| L2 factored (+ legend) | 1045 | 1.0× |
| L2 explicit (+ legend) | 2021 | 1.93× |
| L2 interface markdown pack | 813 | 0.78× |
| AST struct (javalang) | 5241 | 5.02× |
| Raw Java sources | 11962 | 11.45× |

## Test agent score (wiring + topology questions)

| Representation | Pass | Fail | N/A | Wiring pass rate |
|----------------|-----:|-----:|----:|-----------------:|
| L2 factored | 5 | 0 | 2 | 100% |
| L2 explicit | 4 | 0 | 3 | 100% |
| L2 markdown | 6 | 1 | 0 | 75% |
| AST struct | 5 | 0 | 2 | 100% |
| Raw Java | 5 | 0 | 2 | 100% |

## Analysis

**Compression:** L2 factored is ~11× smaller than raw Java and ~5× smaller than javalang AST struct on the 29-handler wedge. **Quality tradeoff:** L2 markdown scores highest on curated L1/dogfood (meta + topology tables). L2 factored/explicit excel at operadic inst rows and lossless reexpand; AST/raw excel at syntax and call-site fidelity per file. **AST gap:** Plain AST dumps omit annotation *values* unless augmented (we add @CommandType entity/action via source regex). They do not encode cross-handler wiring edges or breakeven token economics without a separate graph pass. **When to use which:** Agent context = prefer L2 factored for wiring at scale; navigation/audit = L2 md; refactor tools = AST; ground truth dispute = raw Java. **This run:** test agent pass count — L2 md 6/7, AST struct 5/7, L2 factored 5/7.
