# PROTOCOLS E2 & E3 — RECONSTRUCTED OPERATIVE ESSENTIALS
Reconstructed 2026-09-16 from the Lens-E author abstract held in session context; the frozen
originals (EXPERIMENTS.md, delivered to the operator 2026-07-30) are AUTHORITATIVE — any
conflict resolves to them. Deviations in today's runs are recorded in each RESULTS file.

## E2 — TOKEN MICRO-EXAMPLE (discharges GA6) · effort ~0.5d
**Purpose.** The arithmetic nobody has done: does shipping wiring as (seed, marking) generator
data actually cost fewer tokens than explicit edge lists, once ALL fixed overheads (schema
legend, motif dictionary entry) are paid?
**Materials (frozen).** 3 real Apache Fineract composition sites: an `ApiResource` (REST
resource → command/query pipeline), a `RepositoryWrapper` (service → repository wrapper →
JPA repository), and a `@CommandType` handler (annotation-wired command handler). Fallback
chain: any Spring OSS repo → synthesized-realistic MVC triple (recorded as deviation).
**Procedure.** For each site: (1) extract the composition site's wiring (units, exported ports,
edges); (2) serialize form A = explicit edge list (aider-repo-map-style); (3) serialize form
B = seed (port-type vocabulary) + marking + ONE motif definition + instantiation table +
minimal schema legend; (4) GATE: mechanical re-expansion of B must reproduce A's edge set
byte-identically (else abort — forms not information-equivalent); (5) tokenize both with
cl100k (tiktoken; vendored/npm fallback per §0.1); (6) publish per site: F = fixed overhead of
form B (legend + motif def), m = per-instance marginal cost in B, e = per-instance cost in A,
break-even n\* = F/(e−m), and n_actual = instances of the motif actually present at the site
(and repo-wide estimate where cheap).
**Success/decision (frozen).** WIN: e > m and n\* < n_actual on ≥1 site (dictionary pays for
itself in-repo). KILL: e ≤ m (factored form is not even marginally cheaper) OR n\* > n_actual
on ALL three sites. AMBIGUOUS otherwise → carry both forms into E3.
**MAY claim after WIN:** the L2 token arithmetic is live at micro-scale (order-of-magnitude,
3 sites). **MAY NOT claim:** repo-scale savings; comprehension parity (that is E3); anything
about L3/L4.

## E3 — FORMAT-COMPREHENSION ABLATION (discharges GA7/GA8's cheapest core) · effort ~2–3d
**Purpose.** The decisive test of the whole L2 bet: can a model READ generator-data wiring as
well as explicit edges, at matched information?
**Materials (frozen).** ~30 extracted MVC composition sites (Fineract; fallback per §0.1);
arms: A = explicit spelled-out edge list; B = (seed, marking) + motif defs + instantiation
table + minimal legend, byte-identical to A on mechanical re-expansion; C = interface-only,
no wiring (floor). Questions: ~50 auto-generated from the extracted graph via templates
("which repository does endpoint X ultimately write through?", "which two services share
table T?") + ~10 planted-delta questions (one instance's flag differs — the R5 case);
answers mechanically checkable against the graph; question-generation firewalled from pack
design; frozen (SHA-256) before the first model call. Arms × 2 models × 2 context positions
(early/middle in padded context, for lost-in-the-middle).
**Grading (frozen).** Deterministic script against the graph; no LLM judging; arm-C-driven
question audit (a question arm C answers correctly is testing prior knowledge, not the wiring
— flag it).
**Decision rules (frozen).** B ≤ A − 5pts pooled accuracy at matched information ⇒ L2 FAILS
as serialized (one gloss-mitigation rerun allowed). B ≈ A with tokens(B) < tokens(A) after
overheads ⇒ core bet LIVE, full Fineract wedge justified. tokens(B) ≥ tokens(A) ⇒ E2's
arithmetic already killed it. Position-only failure ⇒ layout problem, not format problem.
Sanity aborts: floor guard (don't apply the 5-pt rule inside noise); if arm A itself scores
< chance-adjacent, the question set is broken — abort and regenerate.
