# Consensus iteration 1

**Roles:** Advocate (proposal) · Faithfulness evaluator (digest + transcript-summaries only) · Operator (merge notes)

## Advocate — unified system proposal (v1)

**Package:** `skills/paris-level-up/` curriculum + 8 skills as factory OS.

**Pipeline:** `factory-operator` → `process-embedded-factory` → `factory-harness` → `covariant-eval-loop` → `agent-orchestra` → (`pr-pulse-discipline` + `eval-over-review`) → `devex-metrics-grounding` feedback to operator.

**New requirement:** Each skill gains `## Progressive disclosure` (L1/L2/L3 table) + `## Unified system` cross-links.

**Talk map (v1):** 9 videos → 8 skills (WorkOS split operator/embed; Warp split Lloyd/Gupta; Factory.com on operator).

**Plugin stub:** `plugin-manifest.json` with triggers for “software factory”, “coding factory”, “PR bottleneck”.

---

## Faithfulness evaluator — scorecard (firewalled)

*Sources only: `research/ai-engineer-paris-2026/digest.json`, `transcript-summaries.json`, `catalog.json`. Did not read advocate prose above during scoring.*

### Per talk

| video_id | Ingest | Evidence density | Gaps |
|----------|--------|------------------|------|
| `HvboD89DyQ8` | yes | Strong: digest bullets @ 2:36, 3:34, 3:56, 4:10 + quotes in summaries | None critical |
| `vGCJ7diEtrw` | yes | Weak: hook only in digest; no MM:SS bullets | Need L3 cites from opening (EY/Adobe, definition) — FACT @ 0:00 |
| `tUPPVhBBcoM` | yes | Weak: hook only | Lloyd OSS / 6mo no code = **CONJECTURE** unless cited from opening |
| `TN3mj92oZ8I` | yes | Strong bullets + quotes | 9:29 routing — digest only, accept FACT |
| `XyV6bSMyq-I` | yes | Strong bullets + quotes | sim-to-real “gap” in bullet — paraphrase, label FACT if in caption |
| `TRfzFJCJ7ZE` | yes | Hook only | Orchestra metaphor — opening mentions Conductor app FACT @ 0:00; “sections/score” = **CONJECTURE** without MM:SS |
| `LlgiOCmFG_w` | yes | Hook + audience themes | Deep module / review agent — **CONJECTURE** (comments/themes, not digest bullets) |
| `_mi3alkqy4s` | yes | Hook | “Death of review” thesis — opening FACT; specific eval product claims need cites or CONJECTURE |
| `Se8jHLliLXE` | yes | Hook | “400+ orgs” in **catalog title**, not in opening snippet — label **CONJECTURE** or cite title as metadata FACT |

### Per skill (existing SKILL.md claims vs evidence)

| Skill | Score (0–5) | Hallucinations / overreach | Missing cites |
|-------|-------------|------------------------------|---------------|
| factory-operator | 4 | “Ramp blogged inspects” not in ingested snippet — OK as speaker ref if in talk; unverified @ 0:00 | vGCJ7, tUPPVh need L3 tables |
| process-embedded-factory | 5 | Horizon naming — verify in caption @ 3:56 paraphrase | TARS @ 4:10 covered in quotes |
| factory-harness | 5 | — | Lloyd talk under-cited vs Gupta |
| covariant-eval-loop | 5 | — | — |
| agent-orchestra | 3 | Conductor product details beyond opening | Need L3 @ 0:00 Conductor desktop FACT |
| pr-pulse-discipline | 3 | Pulse/firewall is **programme**, not Pocock transcript | Pocock L3 only hook; tier/blasts **CONJECTURE** without MM:SS |
| eval-over-review | 3 | Arize product specifics | L3 from opening bandwidth mismatch FACT |
| devex-metrics-grounding | 3 | “400+ orgs” from title not opening | Quarterly/DORA from opening FACT |

**Auto-caption:** Not repeated in skills yet — **missing** (spec-level OK).

---

## Operator — merge notes for iteration 2

1. Add **Layer 3 tables** to all 8 skills; pull MM:SS from digest/stubs/quotes where available; else **0:00 opening FACT** with short snippet.
2. Mark explorer-derived moves (deep module, blast radius, score/sections) **CONJECTURE** in L3 or footnote in L2.
3. Split **Warp**: Gupta cites on harness; Lloyd cites on harness + operator environment line.
4. **devex-metrics:** cite “400+ orgs” as **catalog/title FACT**, not transcript FACT.
5. **pr-pulse:** label programme pulse cross-links CONJECTURE relative to Paris corpus.
6. Add caption limitation to `paris-level-up/README.md` once.

**Deltas for advocate v2:** Progressive disclosure mandatory; faithfulness acceptance tests in spec; plugin stub retained.
