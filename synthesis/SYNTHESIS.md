# SYNTHESIS — recovered inventory version

## One-paragraph thesis

Treat a production codebase as a **module of systems** whose meaningful structure lives at the
interface and in the typed wiring between interfaces. On that reading, the recovery program in
this repo has three bounded goals: map wiring compositionally, identify symmetry/invariant
structure carefully enough to support orbit-style factoring, and test whether wiring-first context
beats explicit graph spelling at matched fidelity without overclaiming beyond the evidence already
recorded in the README and experiment summaries.

## Paper → codebase crosswalk (recovered)

| Paper-side construct | Repo-side construct | Current status |
|---|---|---|
| System / interface | Code unit summarized at its interface | Framed in `plans/IDEATION.md`; kept as the intake discipline in `HANDOFF.md` |
| Interaction pattern | Wiring graph over ports/interfaces | Central object of the proposed `WiringMap` |
| Module of systems | Whole codebase as compositional object | Demonstrated only at toy scale in E1 witness |
| Port-plugging / pushout spine | Formal backbone for codebase gluing | Binding repair in `plans/CONSENSUS.md` R1 |
| System maps | Refactors, ports, migrations, mocks | Migration-square reading retained as future work |
| Equivariance / orbit structure | Representative-plus-delta factoring of repeated wiring shapes | Allowed only as equivariance/invariant transfer, not Noether theorem |
| Free wiring patterns | Lossless factoring into seed/motif/instance descriptions | Minimality claim explicitly demoted |
| Compression benchmark claim | Marginal gain of L2–L4 over interface-only at matched fidelity | Still unproven here; README forbids claiming CR@F95 |

## Program state after recovery

- **E1** demonstrates the shape at toy scale (`witness/WITNESS.json`, 13/13), with the standing
  caveat: demonstrated ≠ proved.
- **E2** shows that factored serialization can be cheaper than explicit edge lists on three real
  Fineract sites, losslessly.
- **E3** shows no ≥5-point comprehension tax at pilot scale on one convention-heavy family.
- **E5.1** shows that parity through depth depends on the pack being fully reader-specifiable,
  not merely re-expandable by the builder.

## What this synthesis does and does not license

**MAY**

- Use interface-first context construction as the operative reading discipline.
- Treat E2/E3/E5 as empirical wedges for the larger program.
- Treat equivariance/orbit language as a research direction constrained by the README claims ladder.

**MAY NOT**

- Claim Noether's theorem, CR@F95, L3/L4 gains, repo-scale savings, or cross-corpus generality.
- Claim canonical minimal presentations from freeness.
- Treat the E5 v1 harness as model validation rather than harness validation.
