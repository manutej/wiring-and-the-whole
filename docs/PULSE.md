# PULSE — operator protocol

**Trigger word:** `pulse` (user standing instruction)

A **pulse** is one full quality loop: implement → adversarial review → merge attempt → interface-level tests → evaluator scoring. It is **not** a synonym for "run CI" or "refresh docs."

## Trigger

When the user (or automation bound to their standing instruction) says **pulse**:

1. Confirm scope for this round (what is in / out).
2. Run the steps below in order unless the user narrows the pulse (e.g. "pulse docs only").
3. Do **not** treat a pulse as complete without the evaluator lane and merge gate.

## Roles

| Role | Who | Receives | Must not |
|------|-----|----------|----------|
| **Implementer** | Primary agent / subagent | [`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](pulse/IMPLEMENTER-BRIEF-TEMPLATE.md) filled for this round | Read [`docs/pulse/RUBRIC-EVALUATOR.md`](pulse/RUBRIC-EVALUATOR.md) or evaluator brief contents |
| **Evaluator** | Separate subagent or human | Rubric + artifacts only (no implementer chain-of-thought) | Implement fixes; negotiate scope with implementer mid-flight |
| **Adversarial panel** | Multitask / team subagents | Written meta-prompt (repo: `plans/ADVERSARIAL.md` style) | Sign off without listing concrete failure modes |

**Firewall:** The evaluator rubric lives in `docs/pulse/RUBRIC-EVALUATOR.md` (or a pulse-specific copy). The implementer brief must state explicitly that this file is forbidden for the implementer during the same pulse.

## Pulse loop (ASCII)

```
                    +------------------+
                    |  USER: "pulse"   |
                    +--------+---------+
                             |
                             v
              +------------------------------+
              | 0. Plan + implementer brief  |
              |    (scope, done criteria)    |
              +--------------+---------------+
                             |
                             v
              +------------------------------+
              | 1. IMPLEMENT planned work    |
              +--------------+---------------+
                             |
                             v
              +------------------------------+
              | 2. ADVERSARIAL PANEL         |
              |    (parallel subagents)      |
              |    -> gaps, MUST-PROVE hooks  |
              +--------------+---------------+
                             |
                             v
              +------------------------------+
              | 3. FIX or DEFER (documented) |
              +--------------+---------------+
                             |
                             v
              +------------------------------+
              | 4. MERGE GATE                |
              |    make verify               |
              |    make pulse-eval (functional)|
              |    make pulse-gate (reminder) |
              +--------------+---------------+
                             |
              +--------------+---------------+
              | pass?        | fail?          |
              v              v
     +-------------+   +------------------+
     | 5. Attempt  |   | stop; no merge   |
     | merge main  |   | report failures  |
     +------+------+   +------------------+
            |
            v
     +------------------------------+
     | 6. INTERFACE-LEVEL TESTS     |
     |    (failure modes, not echo) |
     +--------------+---------------+
                    |
                    v
     +------------------------------+
     | 7. EVALUATOR (firewalled)    |
     |    score vs RUBRIC-EVALUATOR |
     |    implementer never sees    |
     +--------------+---------------+
                    |
         +----------+----------+
         | PASS rubric         | FAIL rubric
         v                     v
   +-----------+         +----------------+
   | close     |         | open issues /  |
   | pulse     |         | next pulse     |
   +-----------+         +----------------+
```

## Steps (in order)

1. **Plan** — Fill an implementer brief from the template; list files, claims, and done criteria.
2. **Implement** — Smallest correct diff; match repo conventions (`HANDOFF.md`, existing scripts).
3. **Adversarial review** — Spawn a **separate** panel (not the implementer's own recap). Output: numbered gaps, severity, suggested cheap checks.
4. **Integrate** — Address blockers; defer others with explicit labels (CONJECTURE / DESIGN / open MUST-PROVE).
5. **Merge gate** — From repo root:
   - `make verify` (witness 13/13, E2/E3 frozen JSON parity)
   - `make pulse-gate` (runs verify + pulse reminders; does not substitute for evaluator)
6. **Merge attempt** — Integrate to `main` only if gates pass and user/policy allows; otherwise **draft PR** and stop (user may forbid merge on protocol-only work).
7. **Interface-level tests** — Exercise **behavior at boundaries**, not artifact re-read:
   - Break inputs (malformed pack, wrong witness step, missing frozen file) and confirm **actionable** failures.
   - Confirm a cold reader can navigate via **interfaces** (SKILL, wiringmap JSON, CONTEXT-COMPACT) without browsing the whole tree.
   - Avoid "tests" that only diff the same frozen JSON the harness already diffs (`make verify` territory).
8. **Evaluator lane** — Independent scorer uses `docs/pulse/RUBRIC-EVALUATOR.md` (or pulse-local copy). Deliver: dimension scores, fail conditions triggered, ship / no-ship.

## Test philosophy

| Do | Do not |
|----|--------|
| Probe **reader-spec-equivalence** (E5 lesson: information-equivalent ⇒ spec-equivalent for the reader) | Re-run `make verify` and call it "pulse testing" |
| Stress **witness integrity** (regenerate vs committed `WITNESS.json` when code changed) | Assert pass because `WITNESS.json` exists on disk |
| Validate **navigation without repo browse** (interface-first-context, wiringmap examples) | Link-spelunk every path in chat as proof |
| File regressions against **real gates** when behavior should change | Add shadow JSON fixtures that mirror production artifacts with no semantic check |

Frozen JSON echo tests belong in **`make verify`**. Pulse adds **failure-mode** and **interface** coverage the verify harness cannot see.

## Merge gate

**Required:**

- `make verify` — see `scripts/verify.sh` and `experiments/README.md`.

**Pulse-specific (human/process):**

- Adversarial panel output attached or linked in PR / handoff note.
- Evaluator completed rubric stored **outside** implementer context (separate file, separate subagent transcript).
- Interface-level test notes: what was broken on purpose and what signal was observed.

**Optional scripts:**

- `make pulse-gate` → `scripts/pulse_gate.sh` (verify + reminders)
- `make pulse-loop` → `scripts/pulse_loop_gate.sh` (verify + `pulse-eval` + loop checklist; see [`docs/pulse/LOOP-ENGINEERING.md`](pulse/LOOP-ENGINEERING.md))

## What "pulse" is NOT

- **Not** "run tests once" — verify is necessary, not sufficient.
- **Not** a license to merge without adversarial + evaluator lanes.
- **Not** doc-only churn without a scoped implementer brief.
- **Not** sharing the evaluator rubric with the implementer in the same round.
- **Not** replacing claims discipline (`HANDOFF.md` §3): demonstrated ≠ proved.

## Related

- Post-pulse executive report: [`docs/pulse/PULSE-REPORT-SPEC.md`](pulse/PULSE-REPORT-SPEC.md) · template [`docs/pulse/reports/TEMPLATE.md`](pulse/reports/TEMPLATE.md)
- Cloud agent pointer: [`/cursor/stores/self/pulse-protocol.md`](/cursor/stores/self/pulse-protocol.md) · reporting [`/cursor/stores/self/pulse-reporting.md`](/cursor/stores/self/pulse-reporting.md)
- Implementer template: [`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](pulse/IMPLEMENTER-BRIEF-TEMPLATE.md)
- Evaluator rubric (implementer must not read during pulse): [`docs/pulse/RUBRIC-EVALUATOR.md`](pulse/RUBRIC-EVALUATOR.md)
- Loop engineering + Paris paths: [`docs/pulse/LOOP-ENGINEERING.md`](pulse/LOOP-ENGINEERING.md)
