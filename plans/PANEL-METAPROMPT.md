# PANEL-METAPROMPT — one-time adversarial sign-off on the R8 deep-dive
[restored verbatim 2026-09-16; the panel ran 2026-07-30: 3× sign-off-with-required-fixes, all applied]
You are one panelist of a 3-member fable adversarial panel. This is ONE-OFF, ONE-TIME feedback:
your findings will be applied once and the artifact ships; there is no second round. Weight
accordingly — surface only what MATTERS, ranked, with concrete fixes. No style quibbles unless
they impair comprehension or honesty.

## The artifact under review
/home/claude/research/dashboard/r8-witness.html — a deep-dive dashboard whose contract is:
(1) make the R8 faithfulness witness fully understood by a smart reader who does not yet
understand it; (2) present the four decisive experiments (E1–E4) with pre-registered thresholds
verbatim; (3) represent the FIRST REAL RUN honestly (WITNESS.json: 12/12 checks pass at toy
scale — demonstrated ≠ proved; two checks were strengthened after an earlier weakness was
caught: genuine two-order associativity, and a morphism-level Ex 4.25 composition — verify the
page reflects the STRENGTHENED run, not the old one).

## Ground truth to check against
- /home/claude/research/witness/WITNESS.json (the record; includes step10_assoc and
  step10_ex425 witnesses from the strengthened run)
- /home/claude/research/witness/run_witness.py (the implementation — read it critically)
- /home/claude/research/synthesis/EXPERIMENTS.md (E1–E4 protocols; thresholds must match verbatim)
- /home/claude/research/synthesis/FOUNDATION.md (Code_X commitment; C₀ SymTab is its
  witness-scale skeleton — the page must not conflate them)
- /home/claude/research/plans/ADVERSARIAL.md + PATH-FORWARD.md (gaps, gates, claims ladder)
- Paper at /home/claude/research/paper.pdf for any formal spot-check (≤20 pages/read)

## Shared verdict format (return EXACTLY this, compact)
VERDICT: [sign-off | sign-off-with-required-fixes | reject]
REQUIRED-FIXES: numbered, each: defect → evidence (file/line/section/screenshot) → exact fix
  (these BLOCK sign-off; keep to what truly blocks)
ADVISORY: at most 5 bullets, non-blocking
ONE-LINE: your panel-record sentence

## The three lenses (you are exactly one)
- P1 MATH: is the implementation sound and honestly described? Attack run_witness.py: is the
  "pushout" really a pushout in the stated C? Is the bounded universal-property check honestly
  framed on the page? Is the automorphism check construct-then-verify as claimed? Does any
  caption overclaim (e.g., "proved", "rex", "Code_X" where it ran C₀)? Is the κ semantics
  coherent? Run the script yourself if useful.
- P2 EXPERIMENT-DESIGN: do the E1–E4 sections carry thresholds/decision rules verbatim and
  complete? Is anything presented as measured that is designed? Are kill conditions and claims-
  ladder unlocks correct per PATH-FORWARD.md? Is the sequence strip's gate logic right?
- P3 PEDAGOGY+VISUAL: render it (Playwright, /opt/pw-browsers/chromium), desktop+mobile,
  VIEW screenshots. Does a smart outsider actually come to understand what a faithfulness
  witness IS and why it matters, in one read? Where does comprehension break? Do the diagrams
  teach or decorate? Is the honesty panel discoverable or buried?

## Panel record (outcome, 2026-07-30)
P1 sign-off-with-required-fixes: Ex 4.25 lift proved vacuous (identity lift) → repaired to a
genuine naturality check; κ/C₀ framing corrected; invariant B reworded file-granular + 8(a)
added. P2 sign-off-with-required-fixes: step-4 bounded-enumeration protocol deviation disclosed.
P3 sign-off-with-required-fixes: "R8" defined on-page; mobile SVG legibility fixed. All fixes
applied; final witness 13/13.
