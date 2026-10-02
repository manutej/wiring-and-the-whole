# Evaluator rubric (pulse)

> **Implementer must not receive this file contents during the same pulse.**

Copy or specialize this template per pulse. Store completed scores where the implementer cannot read them (separate subagent, private note, or redacted PR comment to operator only).

## Scoring scale

| Score | Meaning |
|-------|---------|
| 0 | Missing or actively wrong |
| 1 | Present but fragile / undocumented |
| 2 | Meets bar for this repo |
| 3 | Exceeds bar; would survive adversarial + cold reader |

**Ship threshold:** no dimension at 0; no **fail condition** triggered; average ≥ 2.0 unless operator overrides.

---

## Dimensions (this repo)

### D1 — Pack reader-spec-equivalence

Does a reader armed only with the **published interface** (pack layout, SKILL, wiringmap schema) get the same obligations as the author intended?

- Check: spot-read one pack or wiringmap example; list ambiguities.
- Fail hints: hidden assumptions in prose only; COMPOSE-witness not reflected in what the reader sees.

### D2 — Witness integrity

If witness code or toybank inputs changed, is the artifact chain honest?

- Check: when relevant, `make witness` / `run_witness.py` vs committed `WITNESS.json` and 13/13 semantics.
- Fail hints: committed witness stale; checks weakened without protocol note in `experiments/PROTOCOL-E1.md` or handoff.

### D3 — Navigation without repo browse

Can a cold agent follow **`docs/CONTEXT-COMPACT.md`**, **`skills/interface-first-context`**, or wiringmap README to the right next command without tree-walking?

- Check: timed path "cold start → one verify command → one experiment folder" using only linked docs.
- Fail hints: only root README works; broken or circular pointers.

### D4 — Regression on real gates

Does the change respect **`make verify`** boundaries and avoid fake parity?

- Check: verify still passes when it should; intentional metric changes are documented and frozen files updated deliberately.
- Fail hints: new test only compares duplicate JSON; verify skipped in PR notes.

### D5 — Adversarial closure

Did the pulse include a **separate** adversarial panel, and were blockers resolved or explicitly deferred?

- Check: panel output exists; severities addressed or labeled open with MUST-PROVE / GA reference.
- Fail hints: implementer self-review labeled "adversarial."

### D6 — Interface-level tests (failure modes)

Beyond verify, did someone **break** inputs and observe useful errors?

- Check: notes describe mutated input → expected failure → actual behavior.
- Fail hints: "we ran make verify again"; no intentional fault injection.

### D7 — Scope & claims discipline

Claims match `HANDOFF.md` ladder; no banned wording (e.g. Noether as theorem); demonstrated ≠ proved stated where needed.

---

## Fail conditions (any one ⇒ no-ship)

1. Implementer had access to this rubric or evaluator brief during the same pulse.
2. Witness or frozen E2/E3 JSON drifted without intentional, documented update.
3. Adversarial panel skipped for a change touching witness, experiments, or claims.
4. Interface tests absent for user-visible behavior changes.
5. Merge to `main` attempted while `make verify` failed.

---

## Evaluator output template

```text
Pulse ID:
Commit/PR:
Date:

D1: __ / 3  notes:
D2: __ / 3  notes:
D3: __ / 3  notes:
D4: __ / 3  notes:
D5: __ / 3  notes:
D6: __ / 3  notes:
D7: __ / 3  notes:

Fail conditions triggered: (none | list)

Decision: SHIP | NO-SHIP
Operator overrides:
```
