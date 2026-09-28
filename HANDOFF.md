# HANDOFF — Double Operadic Codebase Programme ("The Wiring & the Whole")
Session: 2026-07-24 → 07-30 · Operator: CETI · Written for a fresh agent or human resuming cold.
2026-09-16 addendum: container was reclaimed; see RECOVERY.md for restore status. This repo is
now git-tracked; experiments E2/E3 run today — see experiments/.
2026-09-28 addendum (v0 engineering pass, branch `claude/confident-wozniak-1geaqr`): see §7.

## 1. Mission (one paragraph)
Extract from Libkind & Myers, *Towards a Double Operadic Theory of Systems* (arXiv:2505.18329v2,
80pp) a research program + eventual paper that (T1) maps the wiring of large production
codebases as a *module of systems*, (T2) finds symmetries and derived invariants (equivariance —
"Noether" is prose-only inspiration, banned in formal claims), and (T3) beats AST-aware token
compression at matched fidelity — the way "On Meta Prompting" was turned into the meta-suite:
paper → reusable instruments + real systems.

## 2. What happened (the six phases)
1. **Framing** — meta-planning/meta-prompting → `plans/IDEATION.md`, `plans/META-PLAN.md`
   (typed work units, OC gates).
2. **Consensus** — 4 fable agents, one call → `plans/CONSENSUS.md`: repairs R1–R8 (cospan
   doctrine = single formal spine; Noether demoted to equivariance T2a/T2b/T2c; compression
   claim restated falsifiably as CR@F95 Pareto, marginal-gain-over-interface-only headline).
3. **Digestion** — 7 page-disjoint agents → wiki 01–07 (~33k words, page-tagged; lost to
   reclamation) + `wiki/INDEX.md` (restored: concept→page→use crosswalk + glossary).
4. **Synthesis & representation** — `synthesis/SYNTHESIS.md` (crosswalk), NOETHER/COMPRESSION
   (lost; reconstructable), `options/OPTIONS.md`; dashboard v1 field-notebook volume
   (delivered in-conversation).
5. **Adversarial** — 4 fable adversaries → `plans/ADVERSARIAL.md`: gaps GA1–GA10 ("category
   theory is costume until the foundation exists"), MUST-PROVE 1–5, three decisive cheap
   artifacts, early-migration milestone.
6. **Solutions + foundation** — `plans/SOLUTIONS-METAPROMPT.md` → FOUNDATION.md (Code_X
   committed; delivered, lost from disk), EXPERIMENTS.md (frozen E1–E4; delivered, lost from
   disk; E1 preserved verbatim in `experiments/PROTOCOL-E1.md`), PATH-FORWARD.md (6-week plan,
   kill-gates G1–G6, claims ladder; delivered, lost from disk), dashboards v2 + r8-witness
   (delivered). **E1 RUN: 13/13** after two in-session repairs (degenerate associativity;
   vacuous Ex 4.25 lift — both caught adversarially). 3-member fable panel signed off the
   deep-dive; fixes applied.

## 3. Current state of truth
- **E1 witness: 13/13, re-verified on restore** (`witness/`). Caveats that travel with any
  citation: toy scale; C₀ SymTab skeleton of Code_X; universal property by bounded enumeration
  (recorded protocol deviation); demonstrated ≠ proved; MUST-PROVE 1–5 open.
- **Committed foundation:** Code_X = copresheaves on a finite typed-symbol schema; pushouts
  always exist; collisions = computable κ diagnostic; T-HULL exact-hull factorization replaces
  ε-equivariance; invariants Reach & Eff.
- **E2: WIN (2026-09-16).** All 3 real Fineract sites: re-expansion gate byte-identical,
  e>m everywhere, n* = 2–5 vs family sizes 54–514 (GA6 discharged at micro-scale).
- **E3 pilot: B PASSES (2026-09-16).** Factored packs read at parity (B 95.3% vs A 93.8%
  on the audit-surviving wiring pool; C floor 0%) at 63% of A's tokens. No ≥5-pt
  comprehension tax (GA7's core worry unsupported at pilot scale). Deviations recorded.
- **E5/E5.1: B PASSES AT DEPTH (2026-09-19).** 112 questions x 10 depth levels, 40 real
  Fineract units, veteran-QA evaluators, 10 operadic-interview trees. Raw run showed a fake
  depth-collapse; the 3-fable QA panel proved it ~80% harness artifact (undocumented '-'
  sentinel; ambiguous *Repository* glob; self-contradictory D9 key; 4/10 OC trees were
  decomposition theater — caught label-free by universal inconsistency). Two spec fixes +
  rerun: sonnet 100% at every depth in BOTH arms; pooled B-A = -3.7pts (inside the 5-pt
  rule); haiku-only residual localized to large-list enumeration affecting both arms.
  Binding lesson: information-equivalent must mean SPEC-equivalent for the reader. OC-v2
  spec recorded (COMPOSE-witness gate at build time). See experiments/e5-depth/.
- **E5 tokens (side finding, 2026-09-19, recorded in README 2026-09-28):** on the mixed 40-unit
  pack B is only 5.7% cheaper than A (11,787 vs 12,493) versus 37% on E3's uniform 30-handler
  family. L2 savings are homogeneity-dependent: only motif-shaped units compress. This is the
  measurement that points at orbit statistics (U1).
- **Reproducibility is mechanical (2026-09-28):** `sh experiments/check.sh` rebuilds the E1
  witness, every pack and every grade and fails on any committed-artifact diff; CI runs it on
  every push. The E5 build carries the OC-v2 COMPOSE witness (last sub-gold == root gold under
  the grader's equality); it recovers the panel's verdict exactly (valid Q43-45, Q55-57;
  theater Q89-91, Q101) and the E5.1 grader reads the valid set from manifest.json.
- **Claims discipline:** the PATH-FORWARD ladder is binding. Never claim: Noether's theorem
  applies; canonical minimal presentations from freeness; rex-ness of Code-C in general;
  "beats Headroom" (market comp, not benchmark arm).
- **Minting debt:** systems-intake, interface-first-context, symmetry-lens (renamed from
  noether-lens per GA10) still unminted.

## 4. Folder map
```
wiring-and-the-whole/      (git repo; GitHub default branch main)
├── README.md · HANDOFF.md · RECOVERY.md
├── .github/workflows/     check.yml — runs experiments/check.sh on every push and PR
├── plans/                 IDEATION · META-PLAN · CONSENSUS (R1–R8) · ADVERSARIAL (GA1–GA10,
│                          MUST-PROVE) · SOLUTIONS-METAPROMPT · PANEL-METAPROMPT
├── wiki/INDEX.md          page-tagged crosswalk of the 80-page paper
├── synthesis/SYNTHESIS.md paper→codebase crosswalk
├── options/OPTIONS.md     five build options (sequenced 2→1→4→3, 5 standing)
├── dashboard/index.html   three-depth editorial page (surface / mechanism / apparatus)
├── witness/               run_witness.py + WITNESS.json (13/13) + toybank/
└── experiments/           PROTOCOL-E1.md (verbatim) · PROTOCOLS-E2-E3-RECONSTRUCTED.md ·
    ├── wiring.py          ONE home for extraction, pack serialization, re-expansion, grading
    ├── check.sh           reproducibility gate (rebuild all, fail on any artifact diff)
    ├── ask.py             pinned-model evaluator call: prompt file → reply + run record
    ├── e2-tokens/         packs, node tokenizer (cl100k), E2-RESULTS
    ├── e3-ablation/       A/B/C packs, frozen hashes, grades
    └── e5-depth/          112q × 10 depths, QA-panel audit, E5.1 rerun, COMPOSE witness
```

## 5. Method notes (keep doing this)
Fable agents in single parallel batches only; Sonnet for mechanical diagnosis. Every generative
phase → adversarial phase (written meta-prompt) → solutions phase that COMMITS. Provenance
discipline: page-tagged, register-tagged, or labeled CONJECTURE/DESIGN. Consistency ≠
correctness; demonstrated ≠ proved; models ≠ measurements. Treat every "strengthened" check as
unverified until an independent reader re-derives it (this caught two real bugs).

## 6. Next actions
1. DONE 2026-09-16: E2 WIN, E3 pilot B-PASSES → claims ladder rungs unlocked:
   'L2 token arithmetic live at micro-scale' + 'no comprehension tax at pilot scale'.
   DONE 2026-09-28 (v0): pinned-model call exists (`experiments/ask.py`), so E3 deviation 2
   is closeable. Next (v0.1): full-protocol E3 — 50+10 q, mixed sites, and the minting
   firewall (a separate question-minting agent; the templates are still same-author).
2. Mint the three free instruments as SKILL.md files + one dogfood run each.
3. Upgrade witness C₀ → full Code_X (exhaustive-within-bound universal check) → attempt
   MUST-PROVE 1–2.
4. Fineract wedge (orbit statistics discharge U1) with E4 migration chain folded in. The E5
   token side-finding (5.7% on a mixed pack) is the reason this is now the next measurement.
5. Optional: /ceti-explainer film (brief was in explainer/BRIEF.md, reconstructable).

## 7. 2026-09-28 session — v0 engineering pass (resume here)
Frame: craft rules (manutej/craft) applied to the corpus. Verdict going in was SHIP-WITH-FIXES:
everything mechanical reproduced byte-identically, but the model-call step was not in the repo,
three rules were duplicated across scripts, nothing enforced the frozen hashes, and one real
finding lived only in a GitHub issue. Order of work was pin → consolidate → gate → runner → docs.

Done, in commits on `claude/confident-wozniak-1geaqr` (all pushed):
- `experiments/check.sh` written and run GREEN on the pre-refactor code first (the
  characterization test), then the refactor, then GREEN again. Every pack, questions.json,
  graph.json, WITNESS.json and all three GRADES files byte-identical across the refactor.
- `experiments/wiring.py`: extract / impl_of / block_A / MOTIF / row_B / expand_row /
  count_tokens / norm / eq / parse_answers. Net −144 lines. LEGEND texts intentionally NOT
  shared (frozen, version-pinned experimental artifacts).
- COMPOSE witness in e5_build → manifest.json `oc_compose_valid_q` / `oc_compose_theater_q`;
  e5_grade2 reads it instead of hard-coding `DEPTH in (5, 6)`. E5.1-GRADES.json unchanged.
- `experiments/ask.py` exercised against a local stand-in for POST /v1/messages (no API
  credentials in the container): end_turn writes reply + run record; max_tokens stop and
  connection refused both exit 1 and write nothing. Request body carries only
  model/max_tokens/messages — no fallbacks (would break the pin), no thinking parameter.
  NOT yet run against the real API: that is the first thing v0.1 should do, on one E3 prompt,
  and diff the reply format against `responses/`.
- CI workflow; README (E5 token row, Reproduce section, path typo, file map); dashboard row.
- GitHub: issue 1 and draft PR 2 closed as superseded by merged PR 3.

Adversarial findings on this session's own work (recorded, not hidden):
- E3 strict grading now uses the shared `eq`, which set-compares whenever EITHER side has a
  comma; the old E3 rule set-compared only when the gold had one. Identical on all recorded
  data (gate proves it) but an answer like `closeLoan,` against gold `closeLoan` is now
  strict-correct where it was strict-wrong. One rule, one home; the semantics moved to E5's.
- The COMPOSE witness checks legitimacy, not informativeness: a tree whose last sub merely
  restates the root passes it. Necessary, not sufficient (D6 stays flagged non-discriminating
  for exactly this reason). Meta-operad's "OC as rubber stamp" failure mode still applies.
- `row_B` lost the `(typ, "UNKNOWN")` fallback: a handler with zero edges now raises at build
  time instead of emitting a row that would fail the gate later. Fail loud, by design.
- check.sh flags ANY uncommitted change under witness/ or experiments/, including your own
  unstaged source edits; the message now says so.
- Not done from the original list: minting the three SKILL.md instruments (item 5). Prose,
  cheap, but each needs one real dogfood run before it ships (OPTIONS 5 kill-criterion).

Where the operadic / sheaf instruments plug in next (DESIGN, not done):
- meta-operad: the witness above is Tier-0. Full OC-v2 needs the two-condition error-
  propagation run (gold-substituted subs vs model-chained subs) and trees aimed at D7–D9.
- operadic-interview: `scripts/treelint.py` could lint the OC sub-question trees for
  node.askable / compose.stated at build time, same slot as the COMPOSE witness.
- sheaf-memory: the Fineract wedge's orbit statistics are a natural fit for staged ingestion
  (typed wiring triples; a symmetry-breaking unit = a delta with high absorption residual).
  Conjecture until run; do not cite.

Method notes that held: pin before refactor; the gate caught its own untracked file first
(honest); every claim in the commit messages has the command that produced it.
