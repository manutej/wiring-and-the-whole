# SYNTHESIS — Paper Concept → Codebase Construct Crosswalk
[restored verbatim 2026-09-16 · GA4 correction noted inline · companions NOETHER.md and
COMPRESSION.md lost to reclamation, reconstructable from INDEX + ADVERSARIAL + this file]
Master distillation. Provenance: wiki/01–07 (page-tagged), plans/CONSENSUS.md (R1–R8).

## The one-paragraph thesis
A large codebase is not a pile of files; it is a **module of systems**: code units known only
through interfaces, glued by typed interaction patterns, with maps (refactors, ports, mocks,
tests) living over interface maps. The paper supplies exactly the algebra for this: the cospan
doctrine turns "any category with pushouts + marked ports" into a full systems theory with
composition, maps, and black-boxing recipes for free [05, p49–54; 01, p7 item 2b]. Because
wiring diagrams are FREE interactions [07, Obs 8.1, p68], wiring is specifiable by generator
data alone — the algebraic basis for cross-file compression. Because the constructions are
pseudo-functorial, isomorphic parts in isomorphic positions yield isomorphic wholes — the
license for symmetry-orbit folding and derived invariant checklists (equivariance, not Noether;
see NOETHER.md). Because system maps compose with wirings (squares) [01, p6 axiom 5; 04, Ex
4.25], migration correctness decomposes into locally checkable commuting squares — the
"million-file translation" becomes a sequence of interface-bounded steps.

## The crosswalk

| Paper construct | Formal home | Codebase construct | Program use |
|---|---|---|---|
| Interface | object of C [05, p54] | Module's exported surface: signatures, schemas, ports, contracts | The unit of context (T3-L1); catalog node (T1) |
| System `p: M→S` over interface | port map [04, p35–43] | Code unit + which internals are exposed as ports | System card |
| Interaction (loose) | cospan `M→J←N` / UWD | Import/link/composition pattern; DB table & broker topic as junction J | Wiring edge (T1); pattern token (T3-L2) |
| Composition = pushout | rex C gluing [05, Lem 6.5] | Actually linking the units along shared ports | Compositional summarization order |
| Parallel product ‖ | monoidal structure [04] | Unrelated modules side by side, no interaction | Safe context truncation boundary |
| Tight map / system map | vertical morphism | Refactor, version bump, mock/stub (coarse-graining), port to new language | Migration object (capstone) |
| Interaction map (square) | axiom 5 [01, p6] | "This refactor respects this wiring" — checkable compatibility | migration-square-checker |
| Square-composition (Ex 4.25) | [04, p42] | Local square checks compose to whole-migration correctness | R4 square-commutation metric |
| Moore machine over lens | [04, p43–48; 06] | Stateful service: state, update, readout; request/response direction | Runtime module (separate from static spine, R1) |
| F-ladder (id/powerset/Giry) | [06, p63–66] | Deterministic / nondeterministic / probabilistic service semantics | Choose fidelity of runtime model |
| Trajectory = map from clock system | [06, p62] | Execution trace; test run | T2b; behavioral verification |
| Chart into static system, Dq·u=0 | [06, fenced] | Invariant observable: quantity a service never changes | T2b conserved-quantity target |
| Doctrine (Def 5.1) | [05, p49] | Recipe: pick your code-category once, inherit the whole theory | Wiring-mapper's schema is *derived*, not designed |
| Restriction to marked generators | [03, p24–30; 07, p70–72] | [GA4 CORRECTION: restriction fixes the port-TYPE vocabulary (seed), yielding ALL wirings over it — NOT a sub-vocabulary of wiring shapes; the motif dictionary is smallest-grammar engineering with lossless-by-construction expansion] | T3-L2 pattern dictionary |
| Collapse | [03, Thm 3.15, p24] | Export composite summaries, forget provenance | Context packaging |
| Free interactions (Obs 8.1) | [07, p68–69] | Wiring = generator data (seed + marking), not spelled-out graph | T3's core lever |
| 13 diagram languages | [07, p68–75] | UWD ≈ static import/link wiring; DWD ≈ directed service calls; decorated cospans ≈ annotated edges | Serialization menu for WiringMap |
| Remark 8.12 (interfaces up-front) | [07, p73–74] | Interface catalogs stay valid across all future compositions | Product argument: build catalog once, reuse forever |

## What the codebase instantiation must supply (the "faithfulness witness" checklist, R8)
1. The category **C**: [COMMITTED post-adversarial: Code_X, copresheaves on a finite typed-
   symbol schema — FOUNDATION.md; C₀ SymTab is its witness-scale skeleton, E1 ran on it 13/13.]
2. Pushouts in C: merging units along shared symbols/ports — constructed, not assumed
   [GA1 resolution: pushouts always exist; collisions are a computable κ diagnostic on the
   quotient map, not obstructions].
3. Marked ports **P ⊆ C**: exported symbols, public APIs, schema tables, topics.
4. One worked pushout, one system map, one wiring automorphism ⇒ composite isomorphism, on a
   ≤20-file repo. [DONE: witness/ 13/13, toy scale, demonstrated ≠ proved.]

## Layered architecture of the eventual system
- **Static spine** (cospan doctrine): WiringMap = (interface catalog, UWD-style wiring with
  DB/broker junctions, system cards). Extractor per R6: AST + build graph + config parsers
  (+ optional runtime traces as ground truth).
- **Runtime overlay** (lens doctrine, separate module): services as F-Moore machines; DWD wiring
  from traces; fidelity chosen on the F-ladder.
- **Cross-doctrine composition**: explicitly conjecture/future work (R1). The two layers are
  linked only through shared interface identifiers — an annotation join, not an algebraic one.

## The meta-move (why this mirrors On-Meta-Prompting → meta-suite)
"On Meta Prompting" gave: category of prompts, functors as task→prompt maps, one paper → nine
instruments. DOTS gives: category (double, operadic) of *systems theories themselves* — a
meta-theory whose instances are theories. The analogous minting move: each doctrine and each
axiom becomes an instrument (systems-intake from Inf. Def 1.1; interface-first-context from the
interface axiom; doctrine-typer from the span/cospan/lens trichotomy; wiring-mapper from the
cospan doctrine; symmetry-lens from equivariance; migration-square-checker from axiom 5 +
Ex 4.25). The suite is the paper, operationalized — see OPTIONS.md for the build-out.
