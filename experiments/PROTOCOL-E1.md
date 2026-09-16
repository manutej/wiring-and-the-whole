# PROTOCOL-E1 — R8 FAITHFULNESS WITNESS [verbatim from frozen EXPERIMENTS.md §E1; restored 2026-09-16]

**Purpose.** Discharge the demonstration half of [GA1] (Code-C constructed and exercised on a
real gluing, collision behavior explicit) and the vacuousness half of [GA3] (exhibit one
nontrivial functorial invariant actually computed and actually constant on an orbit). Converts
"codebase = module of systems" from asserted to demonstrated [R8]. Every formal adjective in
SYNTHESIS/NOETHER/COMPRESSION waits on this [ADVERSARIAL §3.1].

**Parametricity.** LENS F owns the choice of Code-C (FOUNDATION.md). This protocol is
parametric in a four-tuple **CODE-C = (C, M, P, κ)**: category, morphism class, port-marking
convention, collision policy. If FOUNDATION.md has not landed or does not fix the tuple, run
with default **C₀ (SymTab)**: objects = finite typed symbol tables (name, kind ∈ {class,
method, field, topic, table}, signature string) with namespace qualification; morphisms = kind-
and signature-preserving functions (not required injective); a *code unit* = body object X plus
interface map i: P → X marking where the exported ports sit [05 §3, p54]; pushouts = set-level
amalgamation, with a decidable *obstruction predicate* κ firing on non-monic or
signature-incompatible identifications — i.e., in C₀ all pushouts EXIST (presheaf-style, GA1's
"silent merge" branch) and collisions are flagged by a lint predicate, not by non-existence.
Whatever LENS F commits, the structure below is fixed; only the implementations of `object`,
`morphism`, `pushout`, `κ` swap.

**Materials.** A generated toy repo `witness/toybank/` (16 files, Java-flavored, no build —
regex-level parsing suffices): verticals `accounts/`, `savings/`, `loans/`, each `{XController,
XService, XRepository}` (9); `shared/{PageDto, AuditDto, EventTopics, AppConfig}` (4);
collision pair `accounts/Money.java` and `loans/Money.java` exporting `Money` with *different*
field signatures (2); `report/ReportModule.java` importing both (1). `accounts` and `savings`
are exact renamings of each other (the planted exact orbit); `loans` differs by one extra
method (planted near-orbit, NOT folded — exact-iso cells only, per GA2). Tools: Python 3.11
stdlib.

**Procedure.**
1. Freeze CODE-C from FOUNDATION.md; else instantiate C₀. Record the tuple verbatim at the top
   of the witness report.
2. Generate `toybank/` from templates (script `witness/gen_toybank.py`, seeded).
3. Write `witness/extract.py`: file → object of C (symbol table) + port object + marking map.
   Output: 16 objects, 16 markings, and the wiring diagram W (a UWD-style cospan list: which
   ports are identified across units).
4. Implement `pushout(f: J→X, g: J→Y) -> (Z, ix: X→Z, iy: Y→Z)` with (a) commutativity check
   ix∘f = iy∘g, (b) universal-property check by enumeration: for every cocone (Q, qx, qy) with
   |Q| ≤ |Z|+2 built from the toy Hom-sets, verify a unique mediating map Z→Q exists (Hom-sets
   are tiny; enumeration is exact, not sampled).
5. **The real pushout.** Glue `LoanService ⊔_J LoanRepository` along J = the
   `LoanRepositoryPort` interface symbols. Confront fresh-name/rex head-on: both bodies contain
   an internal symbol `log`; the pushout must NOT identify them. C₀ handles this because names
   are pre-qualified (`loans.LoanService#log`) — disjointness holds *inside* C, not via an
   extra-categorical renaming pass. Record whether the committed CODE-C achieves this inside C;
   if it needs an external freshening step, that is a CODE-C revision request to LENS F.
6. **System map.** Refactor `LoanService → LoanServiceV2` (rename internals, keep ports).
   Check the Def-4.22 square mechanically: the map X → X′ composed with the port marking
   equals the new marking [04, p39: system map = commuting square along an interface map].
7. **Wiring automorphism ⇒ composite iso.** σ = swap(accounts, savings) on W, plus the
   component isomorphisms φ_i. Compute both composites (glue-then-swap vs swap-then-glue);
   construct the induced map on the composite and verify it is an isomorphism in C (explicit
   bijection, checked to be a C-morphism with a C-morphism inverse — construct-then-verify,
   no isomorphism search).
8. **Functorial invariant (GA3).** Define B(X, i) = the reachability relation on exposed ports
   ("port a's implementation references port b's"), a finite relation. Verify mechanically:
   (a) every system map from steps 6–7 sends B to B (image under the interface map equals the
   target relation); (b) B of the two orbit members from step 7 agree after transport along σ.
   One nontrivial invariant, named, computed, constant on an orbit — "constant on orbits"
   stops being vacuous at witness scale.
9. **Deliberate collision.** Glue `ReportModule` with both `Money` exporters. The pushout
   computes (quotient identifies the two `Money` names if the wiring says so); κ must FIRE
   (signature-incompatible identification). Also run the clean gluings of steps 5–7 through κ:
   zero false positives required. Document what the silent merge would have produced (the
   GA1 presheaf branch made visible).
10. **Paper-conformance checks (§4/§6), all mechanical:**
    - *Action functoriality / associativity of two gluings*: for the chain
      Controller–Service–Repository, compute (A ⊔ B) ⊔ C and A ⊔ (B ⊔ C); verify the canonical
      comparison map is an iso — the toy shadow of "interactions acting on systems" being a
      genuine action [04 p34; Expl 4.8].
    - *Interface preservation*: every system map emitted anywhere in the run passes the
      Def-4.22 square check [04 p39].
    - *Ex 4.25 composition*: compose the step-6 system-map square with a step-7
      interaction-map square; verify the composite is again a valid square ("maps of
      interactions act on maps of systems") [04 p42] — the engine of the migration square-gate,
      exercised once at toy scale.
    - *Monoidal unit*: gluing along the empty port object = disjoint union; interface of ⊗ =
      coproduct [05 §3 p54; 04 p34].
11. Emit `witness/WITNESS.json` (machine) and render the checks table into the dashboard (per
    LENS R); the JSON is the artifact of record.

**Measurements.** All checks are booleans with witnesses (the explicit maps/bijections
serialized in the JSON). Counts: 4 clean gluings, 1 collision gluing, ≥3 system maps, 1
automorphism, 1 invariant computed at 2 orbit members, 2 association orders. No tokenizer
involved.

**Success criteria (pre-registered).** ALL of: steps 4–8 and 10 pass; κ fires on step 9's
planted collision and on nothing else. Partial outcomes are enumerated in the decision rules —
there is no "mostly passed."

**Decision rules.**
- All pass → "pushout," "system map," "equivariance," "invariant" are licensed in project
  documents *with the qualifier "as demonstrated on the witness"*; MUST-PROVE 1–2 stay open.
- Step 5 fails inside C (fresh names need an external hack) → CODE-C revision request to
  LENS F with the failing datum; do NOT patch locally; re-run after revision. GA1 doing its job.
- Step 7 fails → halt all equivariance/folding language project-wide; diagnose C first
  (malformed morphism class) before doubting the paper — Ex 4.25 is proved; our instantiation
  is the suspect.
- Step 9 κ misfires → collision-policy redesign before any extractor work; a compressor built
  on silent merges corrupts context invisibly.

**Effort.** Half-day (0.5 agent-day; ~400 LOC Python; no network needed).

**MAY claim after success:** a concrete Code-C exists in which one real repo-shaped example is
a module of systems with computed pushouts, checked system-map squares, a wiring automorphism
inducing a composite isomorphism, one named functorial invariant constant on that orbit, and an
explicit, tested collision policy. **MAY NOT claim:** rex-ness of C in general; a semantics
functor ⟦−⟧ to real linker/build behavior (unexercised); anything about approximate/ε orbits
(only exact-iso cells touched, per GA2); scale beyond 16 files; any MUST-PROVE.
