# E5-RESULTS — Depth-graded operadic evaluation at scale (E5 → panel → E5.1)
Run 2026-09-19 · 112 questions (108 unique) across 10 depth levels · 40 real Fineract units
(30 @CommandType handlers + 8 service impls + 2 repository wrappers, develop branch) · arms
A (explicit) vs B (factored, byte-identical re-expansion gate) · evaluators under a veteran-QA
persona · 10 operadic-interview decomposition trees (29 sub-questions) · deterministic grading
· one-time 3-member veteran-QA fable audit panel · artifacts: manifest{,.v1}.json,
questions{,.v1}.json, pack{A,B}{,.v1}.txt, prompts/, responses/, responses_v2/,
E5-GRADES.json (raw), E5.1-GRADES.json (panel-corrected + rerun).

## The arc (the honest story, in order)

**1. Raw E5 (v1):** parity at D1–D4/D6/D10; apparent B collapse at D5 (0.542 vs 1.0; haiku
0.083) and D7 (0.25 vs 0.708); pooled B−A = −10.2pts → would fail the 5-pt rule at depth.
OC trees Q89–91 inconsistent in ALL four runs.

**2. QA panel (one-time, 3 fable veterans):** verdict — the headline was **~80% harness
artifact**:
- D7/D8 B-collapse: an UNDOCUMENTED `-` sentinel (packB's legend never said "`-` = omit the
  anno line"), so both B models classified all 30 handlers as annotated. Information
  equivalence held only via the builder's private expansion function — a spec leak, not a
  comprehension failure.
- D5 haiku: an ambiguous `*Repository*` glob (suffix vs substring reading); item-level recall
  was 0.79 with precision 1.0 — binary set-grading manufactured the 0.083.
- D9: self-contradictory "primary service" key; B's apparent +12.5 was answer-key leakage via
  the inst slot; dual-keying makes all runs ~1.0.
- OC instrument: 4/10 trees were **decomposition theater** — guaranteed-inconsistent by
  construction (yes/no last-sub vs list root; missing composition node). As a model-defect
  detector: 100% false-positive rate. As an accidental harness self-test: it worked perfectly
  — the "inconsistent in every run" signature is model-independent and diagnostic. Genuine
  model failures were consistent-and-wrong (OC ≠ correctness, demonstrated in both directions).
- D6's 100% measures nothing: uniform gold (`LoanRepository`), name-derivable, OC-scaffolded.
  Flagged NON-DISCRIMINATING.

**3. E5.1 rerun (falsifiable-fix loop):** applied exactly two spec fixes — a 2-line legend
addition defining `-` and Constants.* fills, and one glob-defining clause — archived v1,
re-froze hashes, re-ran both B arms. Panel predictions vs measured:
| Prediction | Measured | Verdict |
|---|---|---|
| QA-2: sentinel fix → B D7 ≥ 0.75 | 0.708 pooled; **per-model B D7 == A D7 exactly** (haiku 0.417=0.417, sonnet 1.0=1.0) | confirmed in mechanism (residual is arm-independent enumeration weakness) |
| QA-2: glob gloss → B_haiku D5 ≥ 0.83 | **1.000** (recall 1.0) | confirmed, exceeded |
| QA-1: corrected pooled ≈ −2pts | **−3.7pts** | confirmed in direction & order |

## Corrected headline (what E5 actually shows)
**At 10 depth levels over a real 40-unit wiring graph, the factored (seed, marking, motif,
delta) representation passes the frozen ≤5-pt rule: pooled B−A = −3.7pts.** Sonnet reads both
forms at **exact parity — 100% at every depth in both arms**. The entire residual gap is a
haiku-only robustness cost (0.861 vs 0.935 overall), concentrated in large-list enumeration
(D7 orbit lists of 20+ names — where haiku errs equally in the EXPLICIT arm) and one D9 item.
Multi-hop traversal through motif indirection (inst → impl binding → edge enumeration) is
intact 12/12 even for haiku. OC on the 6 COMPOSE-valid trees: 6/6 consistent-and-correct in
all runs.

## What the operadic interview earned
It caught the harness's own composition defect before any human did (4/10 trees whose golds
don't compose to the root — flagged label-free by universal inconsistency), and localized
B_haiku's v1 D5 failure to the fact-source rather than reasoning (consistent-wrong pairs).
**V2 spec (recorded, from QA-3):** build-time COMPOSE-witness gate (assert f(sub-golds) ==
root-gold + answer-type compatibility before any model call — this alone would have rejected
all 4 bad trees for free); trees aimed at the depths that actually degrade (D7–D9); per-edge
pairwise checks with `all_subs_correct` REPORTED (v1 computed then discarded it); two
conditions (gold-substituted subs vs model-answer-chained subs) to measure error propagation;
no conditional probabilities on cells < 5.

## Recorded deviations & limits
1. One corpus (Fineract, one framework, convention-heavy); haiku/sonnet harness models;
   same-author question templates (mechanical, graph-only, hash-frozen pre-call) — the
   full-protocol firewall still owed.
2. D3 has 6 (not 12) questions — fan-out pool exhausted; 4 D9 duplicates deduped in grading;
   D6 retained but flagged non-discriminating and needing rebuild (heterogeneous endpoints +
   the E3-style arm-C audit, which E5 dropped and should restore).
3. The v1→v2 fix changed pack B's hash (recorded; v1 artifacts archived). A-arm was not
   re-run (unchanged pack; D5 gloss could only help an arm already at 1.0 there).
4. Binary set-grading remains the primary metric (item-recall now reported alongside);
   all-or-nothing on 20-name lists is a harsh but pre-registered choice.

## MAY / MAY-NOT claim
MAY: at depth levels 1–10 on real Spring wiring, the factored form is read at parity by a
strong model and within 4pts by a weak one, once the pack's expansion spec is complete —
"information-equivalent" must mean **spec-equivalent for the reader, not just
re-expandable by the builder** (the E5 lesson, now binding on all future pack designs).
MAY NOT: cross-corpus generality; CR@F95 (needs baselines + fidelity anchor); anything about
L3/L4; that OC v1 validates model reasoning (it validated the harness).

## Sequence position
E2 (WIN) → E3 pilot (B-passes, depth ≤2) → **E5/E5.1 (B passes at depth 1–10 after spec
completion; sonnet exact parity)** → next: full-protocol E3/E5 merge with firewalled question
minting + restored arm-C audit + rebuilt D6 + OC-v2 COMPOSE gate, then the Fineract wedge.
