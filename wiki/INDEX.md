# INDEX — Knowledge Base for "Towards a Double Operadic Theory of Systems"
[restored verbatim 2026-09-16; the 7 deep wiki files were lost to container reclamation —
this index preserves their page-tagged crosswalk and standing verdicts]
Libkind & Myers, arXiv:2505.18329v2 · 80 pp · digested 2026-07-24 by 7 page-disjoint subagents
(~33k words of notes). Every claim in these files was page-tagged. Program targets: T1 wiring
maps · T2a equivariance/orbit folding · T2b conserved quantities (open) · T3 token compression.
Governing repairs: plans/CONSENSUS.md R1–R8.

## Files (originals lost; payload lines preserved)
| File | Paper §, pages | One-line payload |
|---|---|---|
| 01-introduction.md | §1, 1–8 | Ontology (Fig 1), six intake questions (Inf. Def 1.1), contributions (a)–(e), lineage vs operadic/process theories |
| 02-preliminaries.md | §2, 9–18 | 2-cats, F-sketches, tight/loose, adequate triples, Span construction, lenses-as-spans; U5 verdict: ~25% load-bearing |
| 03-loose-bimodules.md | §3, 19–31 | Loose bimodules/right modules ("systems live in a module over interfaces"), collapse & restriction theorems |
| 04-modules-of-systems.md | §4, 32–48 | THE central file: formal module of systems + worked Petri/UWD (port-plugging template) and Moore/lens (runtime template) |
| 05-doctrines.md | §5–6, 49–54 | Doctrines = pseudo-functorial recipes; cospan doctrine (our spine): rex C + ports ⇒ glue-by-pushout systems theory |
| 06-moore-machines.md | §7, 55–67 | Tangencies; services as open F-coalgebras (F: det/nondet/probabilistic=POMDP); ODEs; T2b fence: conserved qty = chart into static system |
| 07-free-interactions.md | §8, 68–80 | Wiring diagrams are FREE interactions; restriction-to-generators machine; 13-entry diagram vocabulary; R3 verified |

## Concept → location → use
| Concept | Where | Feeds |
|---|---|---|
| Six systems-theory questions (Inf. Def 1.1) | 01 §3 [p5] | systems-intake instrument |
| Ontology: system/interface/interaction + 3 map kinds | 01 §3 [p5–6] | wiring-mapper data model |
| Axiom 5: interaction maps = compatibility squares | 01 §3 [p6] | migration-square-checker (T2a engine) |
| Interface sufficiency axiom | 01 [p2] | interface-first-context; T3 layer 1 |
| Adequate triples (L,R) + Span construction | 02 §2 [p12–13] | doctrine-typer lint rule |
| Lens = span with bent legs; f♯ passback | 02 §3 [p18–19] | doctrine-typer: lens vs share discriminator |
| Loose right module (systems over interfaces) | 03 [p20–22] | T1 formal backbone |
| Collapse (forget source) / Restriction (base change) | 03 §3 [p24–30] | T3: sub-vocabulary compression with compositionality guarantee |
| Module of systems (full def) | 04 §2 [p32–34] | T1 |
| Open Petri nets over UWDs (pushout gluing) | 04 §3 [p35–43] | R1 spine template; wiring-mapper |
| Moore machines over lenses; maps = trajectories | 04 §4 [p43–48] | runtime module; ε-symmetry caveat (non-unique maps) |
| Square-composition guarantee (component squares ⇒ composite square) | 04 [Ex 4.25] | R4 migration metric |
| Doctrine (Def 5.1): commuting square of cartesian pseudo-functors | 05 [p49] | black-boxing recipes; T2a license |
| Cospan doctrine: rex C ⇒ port-plugging theory | 05 [p54, Lemma 6.5] | THE codebase instantiation |
| Tangency; open F-coalgebras; POMDP ladder | 06 [p56–66] | runtime wiring; doctrine-typer lens criteria |
| Trajectory = map out of clock system; conserved qty = dual (fenced) | 06 [p61–62] | T2b program (U4) |
| Obs 8.1: wiring diagram = interaction in a FREE theory | 07 [p68–69] | T3 pattern dictionary soundness |
| Restriction to marked generators (Def 8.4/8.8, Expl 8.9) | 07 [p70–72] | T3: ship (seed, marking), not spelled-out graphs |
| 13 diagrammatic languages recovered | 07 §4 [p68–75] | T3 generator vocabulary; T1 format menu |
| Remark 8.12: interfaces designed up-front survive all later compositions | 07 §5 [p73–74] | product argument for interface catalogs |

## Standing verdicts from digestion
- R1 spine verbatim-confirmed at p.7 item 2(b); cospan machinery fully specified via
  Lemma 6.5 + §4 Petri template.
- R3 verified with refinement (07): freeness = theory-level universal property; serialize
  concrete cospans/lenses, keep (seed, marking) separate; minimality is engineering, not math.
- T2b confirmed open in-paper (§1.5 future work); nearest formal handle: conserved quantity =
  chart into a static system (Dq·u = 0), Petri P-invariants as recovery target.
- U5 discharged (02): tight/loose convention, adequate triples, Span/lens package, cospan-as-span
  are load-bearing; F-sketch plumbing is black-box-able.
- ε-symmetry caveat has an in-paper witness: non-unique system maps in Moore example (04).
- [Post-digestion, GA4/GA5 corrections in ADVERSARIAL.md refine the restriction and
  migration-square rows above.]

## Glossary (plain-language, one line each)
system = a thing with an interface · interface = all the outside can see · interaction = a
composition pattern between interfaces · tight map = structure-preserving map (vertical) ·
loose map = wiring/process (horizontal) · square = compatibility between maps and wirings ·
module of systems = the family of systems + the action of wirings on them · doctrine = recipe
turning simple data (a category with pushouts…) into a whole systems theory · black-boxing =
computing composite behavior from part behaviors + pattern · cospan = two things glued into a
middle (port-plugging) · span = two things constrained through a shared apex (variable sharing)
· lens = directed interface: outputs forward, inputs passed back · Moore machine = state +
update + readout (a service) · free interaction = wiring generated purely from combinatorial
data · restriction = shrink a theory to chosen generator interactions, keeping the action.
