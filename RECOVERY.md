# RECOVERY.md — container-reclamation ledger (2026-09-16)
The cloud workspace was reclaimed between 2026-07-31 and 2026-09-16. This repo was rebuilt
from (a) artifacts held verbatim in the session's context and (b) re-execution. Status per file:

## Restored VERBATIM from context (authoritative)
- HANDOFF.md · plans/IDEATION.md · plans/META-PLAN.md · plans/CONSENSUS.md ·
  plans/ADVERSARIAL.md · plans/SOLUTIONS-METAPROMPT.md · plans/PANEL-METAPROMPT.md ·
  wiki/INDEX.md · synthesis/SYNTHESIS.md · options/OPTIONS.md ·
  experiments/PROTOCOL-E1.md (the E1 section of EXPERIMENTS.md, read verbatim in-session)
- witness/run_witness.py — final panel-repaired version (v3: genuine associativity,
  non-vacuous Ex 4.25 naturality, step8a). RE-RUN on restore: 13/13 checks pass;
  witness/WITNESS.json regenerated (deterministic).

## LOST from disk — but DELIVERED to the operator in-conversation (re-attach to restore)
- synthesis/FOUNDATION.md (Code_X commitment) · synthesis/EXPERIMENTS.md (frozen E1–E4) ·
  plans/PATH-FORWARD.md (gates G1–G6, claims ladder) — delivered 2026-07-30.
- dashboard/index.html (Vol I) · index-v2.html · r8-witness.html · session-run.html ·
  V2-SPEC.md — all delivered in-conversation.
- paper.pdf (arXiv:2505.18329v2) — user upload; re-attach or re-fetch from arXiv.
- wiki/01–07 digests · synthesis/NOETHER.md · COMPRESSION.md · plans/PATH-FORWARD.md ·
  explainer/BRIEF.md — NOT delivered as files (except as noted); reconstructable from
  wiki/INDEX.md + the paper if needed. INDEX.md preserves the page-tagged crosswalk.

## Reconstructed (flagged, non-authoritative)
- experiments/PROTOCOLS-E2-E3-RECONSTRUCTED.md — operative essentials of frozen E2/E3,
  reconstructed from the Lens-E abstract held in context. ANY conflict with the delivered
  EXPERIMENTS.md resolves to the delivered original. Deviations from the frozen protocols in
  today's runs are recorded inside each RESULTS file.

## Integrity note
WITNESS.json regenerated on restore matches the pre-loss result (13/13, same check names,
deterministic generator). Per program discipline: "demonstrated ≠ proved" caveats unchanged.
