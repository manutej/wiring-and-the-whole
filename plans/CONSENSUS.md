# CONSENSUS.md — Round 1 (4 fable agents, single parallel batch) [restored verbatim 2026-09-16]

Verdicts: A(math) sound-with-repairs · B(prod-eng) buildable-with-narrowed-scope ·
C(compression) needs-restatement · D(suite-strategy) needs-reframe. No stop-the-line.
OC gate G1: all four RECONSTRUCTIONs re-compose to T1/T2/T3 + suite-minting → framing consistent
(D adds a missing output type, not a divergent reading).

## Binding repairs (integrated; supersede IDEATION.md where they conflict)

R1 **Single formal spine (A).** Codebase-as-module-of-systems is instantiated via the
cospan/port-plugging doctrine (any C with pushouts + marked ports — paper p.7, item 2b).
Doctrine labels (lens/variable-share) become *annotations* that drive elision heuristics;
heterogeneous tri-doctrine composition is explicitly conjecture/future work. Lens doctrine is
reserved for *runtime* semantics (services as Moore machines) as a second, separate module.

R2 **Noether demoted & split (A,B,D).**
- T2a (provable now): **equivariance/invariant-transfer** — wiring automorphism + isomorphic
  components ⇒ isomorphic black-boxed composite; every functorial invariant is constant on
  orbits. This is what licenses orbit folding. No "Noether" branding in formal claims.
- T2b (open, U4): genuine conserved-along-trajectory quantities via representable behaviors
  (conserved quantity = observable fixed by the flow, witnessed by a map into a trivial system).
  Petri P-invariants are the *target* T2b must recover, not evidence it works.
- T2c (mintable now, D): the Noether *design-review lens* as a prompt instrument — needs no
  theorem.
- Product framing (B): "invariant checklist generator at interfaces," never "derived by theorem."

R3 **Freeness claim corrected (A).** §8 freeness gives: wirings specifiable by generator data
alone + any pattern factoring is lossless by construction (substitution soundness). It does NOT
give canonical minimal presentations — minimality is a smallest-grammar-style engineering search
with algebraic soundness guarantees.

R4 **Compression claim restated falsifiably (B+C joint P0 — now discharged).** Pre-registered:
> On repos with measured wiring redundancy (R = 1 − orbits/nodes, C = motif coverage) above
> pre-declared thresholds, the 4-layer pipeline Pareto-dominates baselines at matched fidelity:
> fewer tokens to reach ≥95% of full-context accuracy (CR@F95) on a fixed task suite
> (cross-file Q&A, architectural bug-localization, module migration). Predicted LOSSES:
> implementation-local bugs, small/heterogeneous repos, break-even below N* queries.
Baselines: full context, BM25/embedding RAG, cAST/tree-sitter chunking, **aider repo-map**
(≈ layer-1 already — headline claim is marginal gain of layers 2–4 over interface-only),
LLMLingua-2 matched ratio, Headroom-class if reproducible, oracle ceiling.
Metric battery (C): CR@F95 · fixed-budget Q&A acc (4k/16k/64k) · bug-fix pass@1 split
impl-local vs cross-file · migration test-pass + square-commutation rate · cost-per-solved-task
with break-even N* · symmetry-soundness error <2%. Ablation: factor-then-fold attribution order,
cumulative + leave-one-out.

R5 **Orbits are approximate (B,C).** ε-symmetry: representative + structured per-instance
deltas; audit folded orbits for behavior-relevant diffs (the flag that differs IS often the
bug). Compare against boilerplate-elision, not verbatim shipping.

R6 **Extractor realism (B).** Static AST alone misses the wiring that matters (DI/reflection,
config routing, codegen). Extractor = AST + build graph (Gradle/Maven/Bazel = authoritative
port-plug layer) + config parsers + optional runtime traces (OpenTelemetry) as ground truth;
report edge precision/recall vs traces. DB tables are first-class variable-sharing nodes.
Scope v1: one monorepo, one language, one framework (JVM/Spring).

R7 **Suite-minting on the critical path (D).** New WU7 Mint: each chosen instrument ships as a
full SKILL.md (trigger, moves, quality checklist, failure modes, patch map into meta-suite,
one dogfood run). Wiki digestion gains INSTRUMENT HOOKS alongside JUICE HOOKS. Dashboard is
repurposed as the suite/knowledge INDEX, not summary garnish. G3 amended: every WU6 option
either mints an instrument or states why it can't.

R8 **Faithfulness witness (A upgrade; scheduled post-digestion).** ≤20-file real repo,
cospan-doctrine data spelled out (C, ports P, one pushout, one system map, one wiring
automorphism ⇒ composite isomorphism), checked against §4/§6 — converts "codebase = module of
systems" from asserted to demonstrated.

## Adopted slate (D + B wedge)
Instruments: systems-intake [prompt] · interface-first-context [prompt] · doctrine-typer
[hybrid] · wiring-mapper [code] · noether-lens/orbit-folder [hybrid] ·
migration-square-checker [hybrid].
First wedge (B): Apache Fineract (Spring, banking-domain) — wiring map + orbit statistics
(discharges U1) + 50-question comprehension/bug-localization benchmark at ≥60% fewer tokens
vs tree-sitter chunking at matched accuracy.

## Kaizen edit script #1 (applied to META-PLAN)
+WU7 Mint (in :synthesis, out N×:skill), critical path now …→WU4→(WU5∥WU6∥WU7).
WU2 template += INSTRUMENT HOOKS field. WU5 redefined as suite index dashboard.
G3 += instrument-or-explain rule. IDEATION.md claims superseded per R1–R6 carry a
"see CONSENSUS.md" provenance obligation in all downstream synthesis docs.
