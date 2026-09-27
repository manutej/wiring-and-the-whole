# OPTIONS — 5 Practical, High-ROI Implementations
[restored verbatim 2026-09-16 · sequencing re-derived artifacts-first in PATH-FORWARD.md
(lost from disk; delivered in-conversation); noether-lens renamed symmetry-lens per GA10]
Gate G3 applied: every option traces to wiki pages + ideation hypotheses + consensus repairs,
and either mints an instrument or states why it can't (R7). Ranked by (time-to-demonstrable-ROI
× defensibility). "Code" = real systems needed; "Prompt" = mental-model/prompt instrument
usable immediately with zero code.

---

## Option 1 — Operadic Context Compiler (OCC): the compression wedge
**What:** A pipeline that turns a repo into LLM context packs: L1 interface-only projection →
L2 pattern dictionary (ship seed+marking, not spelled-out graphs [07, p68–72]) → L3 ε-orbit
folding (representative + deltas) → L4 doctrine-annotated elision.
**Why direct ROI:** Token cost is a line item today. The pre-registered claim (CONSENSUS R4):
Pareto-dominance at matched fidelity (CR@F95) on high-redundancy repos, positioned as a layer
ABOVE AST-aware methods (aider repo-map ≈ our L1 alone — the headline is the marginal gain of
L2–L4). Full protocol in COMPRESSION.md.
**Split:** Code: extractor, dictionary builder, orbit folder, benchmark harness. Prompt:
interface-first-context discipline delivers a manual version of L1 *today*.
**First milestone (falsifiable):** Apache Fineract wedge — orbit-statistics table (discharges
U1) + 50-question benchmark: match full-context accuracy within noise at ≥60% fewer tokens vs
tree-sitter chunking. [2026-09-16: E2 WIN + E3 pilot B-PASSES are the micro-scale precursors.]
**Mints:** `interface-first-context` [prompt — mintable now].

## Option 2 — WiringMap Extractor: the plumbing product
**What:** The T1 deliverable: interface catalog + doctrine-annotated wiring (call/DI edges,
import/link edges, DB-table & broker-topic junctions as first-class nodes [02, Ex 2.19; R6]) +
system card per unit; serialized as UWD-style data [07 vocabulary]. Scope v1: one JVM/Spring
monorepo. Ground-truthed against OpenTelemetry traces (edge precision/recall — the number a
staff engineer demands first).
**Why direct ROI:** Orgs have call graphs OR service catalogs OR config wiring — never unified.
Differentiation vs Sourcegraph/CodeQL/Backstage: the *unified*, doctrine-typed map whose output
format is an LLM context pack (feeds Option 1) and whose schema is *derived* from the cospan
doctrine, so composition and black-boxing come with guarantees, not conventions. [GA10 caveat:
"derived/guaranteed" language is licensed only as demonstrated-on-witness until MUST-PROVEs land.]
**Split:** Code: static+build+config extractors, trace reconciler. Prompt: `doctrine-typer`
lens works at the whiteboard immediately (six discriminators from [05]).
**First milestone:** Wiring map of one Spring monorepo with edge recall ≥90% against traces on
service-to-service edges.
**Mints:** `doctrine-typer` [hybrid — lens mintable now, labeler later].

## Option 3 — Migration Square Harness: the hard-problem capstone
**What:** Language/framework migration as system maps: translate leaf units, then verify each
composition by its commuting square (translated-composite ≅ composite-of-translations at the
interface) [01, p6 axiom 5; 04, Ex 4.25 — local squares compose to whole-program correctness].
Interface-correctness, honestly labeled (residual gap to full observational equivalence named
per R1 repair; the equivalence judge is designed in EXPERIMENTS.md §E4, per GA5).
**Why direct ROI:** The strangler-fig pattern engineers already trust, given an algebraic
spine: context per step bounded by interface + local wiring, correctness decomposed into
per-square gates — what makes million-file translation *tractable* rather than imaginable.
**Split:** Code: square-checker (interface-level test synthesis + equivalence judge), migration
sequencer over the WiringMap. Prompt: `migration-square-checker` protocol usable now in any
refactor review ("name the interface map; show the square; what witnesses commutation?").
**First milestone:** [Per ADVERSARIAL early-migration milestone: fold a depth-≥3 Fineract
slice Java→Kotlin into wedge one with seeded faults and the square-gate catch-rate report.]
**Mints:** `migration-square-checker` [hybrid].

## Option 4 — Symmetry Auditor: orbits, invariants, anomalies
**What:** T2a productized (equivariance, never "Noether" in formal claims — R2): compute ε-orbits
of the wiring map; emit (a) orbit statistics (feeds Option 1's L3), (b) interface-level
invariant checklists a refactor must preserve ("checklist generator, not theorem-derived"),
(c) symmetry-breaking diffs as review flags (the 1-of-37-services-that-differs IS the review
item; in-paper witness for caution: non-unique system maps [04, p48]).
**Why direct ROI:** Immediate code-review and consistency-enforcement value in framework-heavy
orgs; zero dependence on open math (T2b stays research). Cheapest option to demo after Option 2
exists (it is a query over the WiringMap).
**Split:** Code: orbit computation (graph iso on typed local neighborhoods + ε-deltas).
Prompt: `symmetry-lens` design-review protocol — usable today.
**First milestone:** On the Fineract map: orbit table + 20 symmetry-breaking diffs triaged by a
maintainer; precision of "this asymmetry is a bug or debt" ≥50%.
**Mints:** `symmetry-lens` [prompt now, code later].

## Option 5 — The DOTS Suite + Paper: the meta-move itself
**What:** (a) Mint the instrument suite (systems-intake from Inf. Def 1.1's six questions +
ontology axioms [01, p5–6]; the four instruments above; each with SKILL.md-grade trigger, moves,
quality checklist, failure modes, patch map into the existing meta-suite — meta-operad's OC
gates slot in as the verification layer). (b) Write the papers per PATH-FORWARD: one empirical
(crossover/CR@F95) + one formal companion (MUST-PROVE 1–5).
**Why direct ROI:** The suite compounds every future session; the paper is the credibility
asset that makes Options 1–4 fundable/publishable. ~90% prompt, ~10% code.
**First milestone:** 6 SKILL.md files + the R8 faithfulness witness. [Witness DONE 13/13;
SKILL.md files remain the standing minting debt.]
**Mints:** `systems-intake` [prompt — mintable now] + the suite packaging.

---

## Sequencing (as amended by ADVERSARIAL + PATH-FORWARD)
Artifacts first: witness (DONE) → E2 (DONE, WIN) → E3 (pilot DONE, B-PASSES; full protocol
next) → mint the three free instruments → Fineract wedge (Options 2+1 with the early-migration
chain folded in) → Symmetry Auditor (4) → Migration Harness (3). Option 5 is the standing
meta-track. The prompt-instrument halves of ALL five options are usable immediately.

## What could kill each (pre-registered, from consensus)
1: low-redundancy repos; boilerplate the LLM already knows (measure marginal value, not verbatim
savings). 2: reflection/config wiring beyond parsers (trace reconciliation is the mitigation,
and its recall number is the honest deliverable). 3: interface-correctness gap on stateful
behavior (runtime overlay needed; F-ladder fidelity choice). 4: orbits too approximate to fold
soundly (<2% soundness budget; audit metric). 5: instruments that don't survive dogfooding
(each requires one real run before it ships — meta-suite discipline).
