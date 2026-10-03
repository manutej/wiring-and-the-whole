---
name: compound-build-loop
description: Operate a segregated multi-agent compound build — builder slices on an integration branch, independent eval/adversarial, monitoring build-log, gates before a single integration PR. Use when shipping a tiered roadmap, engine cutover, or any large change that must not self-SHIP; when the user asks for compound build, MVP push, scale build, or “large build then one PR”.
---

# Compound build loop

**Purpose:** Run a **large programme** as many **small, gated slices** on one **integration branch**, with **role-separated** agents and **one integration PR** only when the programme checklist is green and an independent evaluator has **SHIP**ped the bundle.

**Canonical instance in this repo:** [`docs/operations/COMPOUND-BUILD-SOP.md`](../../docs/operations/COMPOUND-BUILD-SOP.md), checklists [`MVP-CHECKLIST.md`](../../docs/operations/MVP-CHECKLIST.md) / [`SCALE-BUILD-2-CHECKLIST.md`](../../docs/operations/SCALE-BUILD-2-CHECKLIST.md), gates `make pulse-loop`.

---

## When to use

- Tiered roadmap (M0 → M1 → M2 …) or “large build; PR only at the end”.
- Engine cutover (e.g. Python → Rust) where **parity gates** must block drift.
- Any work where **implementers must not self-SHIP** ([`AGENTS.md`](../../AGENTS.md)).
- Cursor Cloud / multi-subagent runs with **builder / eval / adversarial / monitor** lanes.

## When NOT to use

- Single-file fix or doc typo → normal commit + small PR.
- Research-only lanes (Paris/Every) that must not touch product gates.
- Urgent hotfix to `main` without programme checklist (use explicit exception in build-log).

---

## Programme DAG (end-to-end)

```mermaid
flowchart TB
  subgraph setup [Setup once per programme]
    P[Pick programme checklist]
    B[Create integration branch cursor slash name-cd12]
    S[Write build specs per slice]
    L[Open build-log dated md]
  end

  subgraph slices [Repeat per slice Sx]
    BL[Builder reads ONE build spec only]
    IM[Implement plus commit plus push]
    GT[Run slice gate plus pulse-loop or subset]
    PAR[Parallel reviews adversarial math arch]
    EV[Independent evaluator SHIP or NO-SHIP]
    CH[Checklist row to done only on SHIP]
    LG[Monitor one line in build-log]
  end

  subgraph ship [Ship once per programme]
    PL[pulse-loop green on tip SHA]
    BX[Bundle eval SHIP on integration branch]
    PR[Single integration PR draft then ready]
    MG[Merge when CI plus human OK]
  end

  setup --> slices
  slices --> slices
  slices --> ship
```

---

## Per-slice compound loop (one checklist row)

```mermaid
flowchart LR
  spec[Build spec Sx done-when]
  build[Builder implements]
  commit[git commit push]
  gate[Automated gate]
  pulse[pulse-loop or wiring-core-check]
  adv[Adversarial note optional]
  eval[Independent eval]
  done[Checklist row done]

  spec --> build --> commit --> gate --> pulse
  pulse --> adv
  pulse --> eval
  adv --> eval
  eval -->|SHIP| done
  eval -->|NO-SHIP| build
```

**Rule:** The builder **never** marks a row **done** from self-review. Only **independent SHIP** + green gate.

---

## Role firewall DAG (who may know what)

```mermaid
flowchart TB
  subgraph builder_lane [Builder lane]
    BS[build-specs slash Sx md only]
    CODE[Product code and tests]
  end

  subgraph review_lane [Review lanes no implementer chat]
    EVL[Evaluator rubric plus diff plus gates]
    ADV[Adversarial plus ADVERSARIAL md]
    MON[Monitor checklist plus timestamps]
    ARCH[Architecture craft read-only]
  end

  subgraph steward_lane [Steward]
    PR[PR timing branch hygiene]
  end

  BS --> CODE
  CODE -->|push SHA| EVL
  CODE -->|push SHA| ADV
  CODE -->|push SHA| MON
  CODE -->|push SHA| ARCH
  EVL --> PR
  MON --> PR
```

| Role | Reads | Must NOT | Writes |
|------|--------|----------|--------|
| **Builder** | `build-specs/<slice>.md` | Eval rubric, adversarial playbook, other agents’ threads | Code, commits on integration branch |
| **Independent evaluator** | Diff, gates, build spec done-criteria | Implementer conversation | `docs/pulse/evaluations/*-independent.md` → **SHIP \| NO-SHIP** |
| **Adversarial** | Eval inputs + `plans/ADVERSARIAL.md` | Fix code (unless explicitly tasked) | `docs/pulse/adversarial/*-independent.md` |
| **Monitoring** | Checklist + gate output | Product code | `docs/operations/build-log/*.md` rows |
| **Math / limits** | Frozen JSON, token reports | Implementation | `build-log/*-math.md` |
| **Senior architecture** | Architecture docs | Slice pass/fail authority | `build-log/*-arch.md` recommendations |
| **PR steward** | Branch vs checklist | Open PR before programme gate | Build-log note; **one PR** when allowed |

---

## PR timing DAG (when to open GitHub/GitLab PR)

```mermaid
flowchart TD
  start[Integration branch active]
  hold[PR HOLD policy default]
  rows{All programme rows done?}
  bundle{Bundle independent SHIP?}
  pulse{make pulse-loop green?}
  open[Open ONE integration PR]
  merge[Merge after CI review]

  start --> hold
  hold --> rows
  rows -->|no| hold
  rows -->|yes| bundle
  bundle -->|NO-SHIP| hold
  bundle -->|SHIP| pulse
  pulse -->|fail| hold
  pulse -->|pass| open --> merge
```

**Default:** `PR: **hold**` on checklist until bundle SHIP + pulse green. User may request **“large step then PR”** — same gate, no interim PRs per slice.

---

## Gate stack DAG (verification order)

```mermaid
flowchart TB
  V[make verify]
  PE[make pulse-eval functional checks]
  PL[make pulse-loop equals verify plus pulse-eval]
  SL[Optional slice gates wiring-core-check slice-matrix-check charter check]

  V --> PE --> PL
  SL -.->|before or inside pulse-eval| PE
```

**Before every merge to `main`:** `make verify` + `make pulse-loop` on integration branch tip.

**Slice-specific gates** belong in build spec **done-when** (e.g. parity script, world I/O pipeline, matrix runner).

---

## Operating procedure (host / lead agent)

### 0. Programme charter

1. Create **`docs/operations/<PROGRAMME>-CHECKLIST.md`** — table: ID, item, gate command, status.
2. Set **`PR: hold`** until programme complete.
3. Create integration branch: `cursor/<programme>-cd12` off current `main`.
4. Start **`docs/operations/build-log/YYYY-MM-DD-<programme>.md`**.

### 1. For each slice `Sx`

1. Write **`docs/operations/build-specs/Sx-<slug>.md`** with **done-when** bullets (testable, no prose essays).
2. **Builder** subagent: spec only → implement → **`git commit`** → **`git push -u origin <branch>`**.
3. Run gates listed in spec + ensure **`make pulse-loop`** still passes (or note partial gate if slice is docs-only).
4. **Parallel** (separate subagents, no builder context): adversarial, math, arch as needed.
5. **Independent evaluator** subagent: run gates on SHA → **`docs/pulse/evaluations/YYYY-MM-DD-<slice>-independent.md`**.
6. On **SHIP:** set checklist row **done (eval SHIP)**; monitor appends one build-log row.
7. On **NO-SHIP:** builder fixes → new commit → re-eval (do not mark done).

### 2. Programme completion

1. All checklist rows **done**.
2. Bundle eval **`…-<programme>-independent.md`** → **SHIP**.
3. `make pulse-loop` on tip.
4. PR steward: **one** integration PR (draft → ready → merge).
5. Update checklist **PR: merged** with link.

### 3. Craft (review-time, not new CI layers)

Apply [manutej/craft](https://github.com/manutej/craft): **effects-and-purity**, **trustworthy-tests**, **robustness-at-boundaries**, **right-sized-design**.

---

## Artifact templates

### Programme checklist (minimal)

```markdown
# <Programme> checklist

| ID | Item | Gate | Status |
|----|------|------|--------|
| S0 | … | `make verify` | pending |
| S× | … | `make …` | pending |
| **PR** | Single integration PR | All S× + eval | **hold** |

Build log: [`build-log/YYYY-MM-DD-<programme>.md`](build-log/…)
```

### Build spec (builder-facing)

```markdown
# Build spec Sx — <title>

**Done when:**
1. …
2. …
3. Gate: `…`
```

### Build-log row

```markdown
| UTC | Phase | Actor | Result |
| 2026-… | Sx | builder | `<sha>` — one line outcome |
| 2026-… | Sx eval | independent | SHIP / NO-SHIP — link to eval doc |
```

### Evaluator output (required fields)

- **Verdict:** SHIP | NO-SHIP (scope: slice or bundle)
- **SHA / branch reviewed**
- **Commands run** (copy-paste reproducible)
- **Done-when table** vs build spec
- **Conditions** (if conditional SHIP)

---

## Porting to another repository

1. Copy **`skills/compound-build-loop/`** (this skill) into target repo `skills/`.
2. Add **`docs/operations/`** with checklist, `build-specs/`, `build-log/`.
3. Point **gates** column at that repo’s real targets (`make test`, `npm test`, etc.) — keep the **same DAG**; only leaf commands change.
4. Add **`AGENTS.md`** rule: implementer self-SHIP void; independent eval required before merge.
5. Name integration branches **`cursor/<slug>-<env-suffix>`** if using Cloud Agent conventions.

---

## Example programmes (this repo)

| Programme | Checklist | Integration branch | Merge |
|-----------|-----------|-------------------|--------|
| MVP M1+M2 | [`MVP-CHECKLIST.md`](../../docs/operations/MVP-CHECKLIST.md) | `cursor/mvp-engine-push-cd12` | [#42](https://github.com/manutej/wiring-and-the-whole/pull/42) merged |
| Scale S2 | [`SCALE-BUILD-2-CHECKLIST.md`](../../docs/operations/SCALE-BUILD-2-CHECKLIST.md) | `cursor/scale-build-2-cd12` | PR **hold** until S2× SHIP |

---

## Subagent prompts (sketch)

**Builder:** “Implement only `docs/operations/build-specs/Sx-….md`. Branch `cursor/…`. Commit push. Do not read eval rubric or write SHIP.”

**Independent eval:** “Review SHA on branch. Run gates in spec. Write `docs/pulse/evaluations/…-independent.md`. Do not change code unless NO-SHIP blocker.”

**Monitor:** “Poll checklist + gates; append one row to build-log; do not edit product code.”

---

## Quick reference commands (wiring-and-the-whole)

```bash
make verify
make pulse-loop
make wiring-core-check      # Rust/Python engine parity
make pipeline-io            # WIRING_ENGINE=rust default
make slice-matrix-check     # multi-slice shard runner
make charter-1k-check       # scale-honest external slice
```

Adjust commands when porting; keep **verify → pulse-eval → pulse-loop** ordering in the gate DAG.
