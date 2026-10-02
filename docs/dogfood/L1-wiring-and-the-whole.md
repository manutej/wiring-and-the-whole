# L1 — wiring-and-the-whole · meta-corpus · `main` (dogfood)

**Scope:** This repository as a *research corpus* (not toybank Java). Vertical slice: navigation spine from cold start → verify → experiments. **Budget:** ports-only; no prose dumps, no pack bodies, no `node_modules`.

**Skill under test:** [`interface-first-context`](../../skills/interface-first-context/SKILL.md).

---

## Grading facts

Frozen answers for [`L1-QUESTIONS.json`](L1-QUESTIONS.json) — parse this table in **pack I/O** mode (no repo browse).

| fact_key | value |
|----------|-------|
| `e1_witness_check_count` | 13 |
| `e2_s3_n_star_breakeven` | 5 |
| `e3_pilot_b_passes_comprehension_tax_rule` | yes |
| `adversarial_ga_register_path` | plans/ADVERSARIAL.md |
| `verify_make_target` | verify |

---

## Interface catalog

| unit_id | path | role | port_count |
|---------|------|------|------------|
| `handoff` | `HANDOFF.md` | resume / state-of-truth for agents | 4 |
| `readme` | `README.md` | public entry + results table | 3 |
| `recovery` | `RECOVERY.md` | restore ledger | 2 |
| `consensus` | `plans/CONSENSUS.md` | binding repairs R1–R8 | 8 |
| `adversarial` | `plans/ADVERSARIAL.md` | gaps GA1–GA10, MUST-PROVE, cheap artifacts | 10 |
| `synthesis` | `synthesis/SYNTHESIS.md` | paper → codebase crosswalk | 6 |
| `options` | `options/OPTIONS.md` | build options + L1/L2 sequencing | 5 |
| `wiki-index` | `wiki/INDEX.md` | page-tagged paper index | 3 |
| `witness-runner` | `witness/run_witness.py` | E1 executable checks | 2 |
| `witness-spec` | `witness/WITNESS.json` | 13 check definitions | 13 |
| `toybank` | `witness/toybank/` | E1 faithfulness substrate (16 files) | 12 |
| `proto-e1` | `experiments/PROTOCOL-E1.md` | frozen E1 protocol | 2 |
| `e2-packs` | `experiments/e2-tokens/` | token packs + `E2-RESULTS.json` | 4 |
| `e3-grades` | `experiments/e3-ablation/` | A/B/C ablation + grades | 3 |
| `e5-depth` | `experiments/e5-depth/` | depth ablation + E5.1 rerun | 3 |
| `verify` | `Makefile` + `scripts/verify.sh` | E1+E2+E3 frozen gates (PR #7) | 1 |

---

## Per-unit cards (selected)

### `handoff` (`HANDOFF.md`)

**Ports (exported only)**

- `mission` — doc: one-paragraph T1/T2/T3 programme
- `state_of_truth` — doc: E1/E2/E3/E5 status + claims ladder
- `folder_map` — doc: top-level layout
- `next_actions` — doc: ordered resume list

**Wiring (outbound)**

- → `consensus#R1-R8` (ref: claims discipline)
- → `adversarial#GA1-GA10` (ref: what program may not claim)
- → `witness-spec#checks` (ref: E1 citation)
- → `e2-packs#E2-RESULTS` (ref: token arithmetic)

### `witness-runner` (`witness/run_witness.py`)

**Ports (exported only)**

- `main()` — entry: run all checks, exit code
- `load_witness()` — fn: parse `WITNESS.json`

**Wiring (outbound)**

- → `witness-spec#checks` (read)
- → `toybank/*` (static analysis / file presence)

### `e2-packs` (`experiments/e2-tokens/`)

**Ports (exported only)**

- `pack_LEGEND.txt` — spec: L2 shorthand + re-expansion rules
- `E2-RESULTS.json` — artifact: frozen token counts + gates
- `pack_S*_A.txt` — artifact: explicit-edge arm (per site)
- `pack_S*_motif.txt` — artifact: factored arm (per site)

**Wiring (outbound)**

- → `adversarial#GA6` (closes micro-scale token question)
- → `e3-grades#E3-GRADES.json` (feeds comprehension question)

---

## Wiring edges (flat)

- `readme` → `handoff#next_actions` (ref)
- `readme` → `witness-spec#checks` (ref)
- `readme` → `e2-packs#E2-RESULTS.json` (ref)
- `readme` → `e3-grades#E3-RESULTS` (ref)
- `readme` → `e5-depth#E5-RESULTS` (ref)
- `readme` → `verify#make-target` (ref: `make verify`)
- `handoff` → `consensus#R1-R8` (ref)
- `handoff` → `adversarial#GA1-GA10` (ref)
- `options` → `synthesis#crosswalk` (ref)
- `options` → `readme#L1-L4` (ref: compression layers)
- `witness-runner` → `witness-spec#checks` (import/read)
- `witness-runner` → `toybank/accounts/AccountsController` (check target)
- `e2-packs` → `proto-e1` (method note: E1 before benchmark code)
- `e3-grades` → `e2-packs#pack_LEGEND.txt` (same legend discipline)
- `e5-depth` → `e3-grades` (extends format-comprehension to depth)

**Parallel product boundary (`‖`)**

- `wiki-index` ‖ `toybank` — paper index vs Java witness; no runtime edge
- `plans/IDEATION.md` ‖ `experiments/e2-tokens/` — framing prose ‖ measured artifacts

---

## Omissions log

- `experiments/node_modules/` — impl-local / vendored tokenizer; not L1 navigation
- `witness/toybank/**` method bodies — L1 for meta-repo; toybank L1 is a separate slice (`witness/toybank/accounts/` chain)
- `skills/interface-first-context/` — minted on `main`; this pack cites the skill path only
- `docs/witness/` — HTML witness docs on `main`; not required for L1 navigation spine
- Full `plans/*` except consensus + adversarial — out-of-slice for this cold-start pack
- Dashboard / HTML instruments — conversational deliverables; not in git on `main`

---

## Adversarial spot-check (this pack)

| Item | Pass? | Note |
|------|-------|------|
| GA7 — no unpriced indirection | ✓ | Edges name targets; no motif table without legend |
| GA10 — no authority laundering | ✓ | E1/E2/E3 cited as demonstrated, not proved |
| GA4 — L1 ≠ motif dictionary | ✓ | Catalog is units + refs, not 12-motif seed |
| Ports only | ✓ | No Java bodies, no E2 pack text inlined |
| Reader legend | ✓ | `‖` = parallel product; `ref` = markdown pointer |

---

## Dogfood verdict (self)

**Useful:** Yes — an agent can route `HANDOFF → ADVERSARIAL → witness/ → experiments/` without opening Fineract or node_modules.

**Gap:** Meta answers are **pack-local** (Grading facts table); they must stay aligned with `witness/WITNESS.json` and frozen E2/E3 on intentional updates.

**Gradable set:** [`L1-QUESTIONS.json`](L1-QUESTIONS.json) — five questions; use `grade_l1_questions.py --answer-mode io` for pack-only parsing.

**Next stable jump:** Blind pack-only LLM eval on this L1 + handler-wedge L1 (no repo browse).
