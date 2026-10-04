---
name: factory-operator
description: Define and operate a software factory — outcome metrics, build vs buy, skepticism toward sandbox-only stacks. Auto-apply when user asks software factory, coding factory, agent factory, Ramp/Inspects-style SDLC, or whether their setup is a real factory vs laptop agents.
---

# Factory operator

**Operating definition** for agentic SDLC systems: a factory is an **organization-scale loop** from intent → integrated delivery, not “model + sandbox.” Synthesizes WorkOS skepticism, Factory.com builder reality, and Warp’s environment-centric view (Paris 2026 ingested talks).

## When to use

- Deciding **build vs buy** for an internal coding factory.
- Auditing a vendor or internal pitch: “Is this just Claude Code in a VM?”
- Setting **success metrics** before scaling agent spend.
- Scoping a **long-running agent** program (weeks, many repos) with executive reporting.

## When NOT to use

- Single-session codegen or one-off scripts — use IDE agents only.
- Proving formal compression or wiring claims — use programme T1–T3 skills.
- Replacing [`process-embedded-factory`](../process-embedded-factory/SKILL.md) integration design.

## Core moves (7)

1. **Name the loop** — Intake → plan → implement → verify → ship → observe. Which stages are automated vs human?
2. **Outcome metric** — At least one: time-to-feature, incident rate, migration completion, customer-visible ship — **not** PR count or LOC (WorkOS @ 2:36, `HvboD89DyQ8`).
3. **Sandbox honesty test** — If removing Slack/Linear/Jira/webhooks leaves the same experience as a local agent, label **tier-0 demo**, not factory (WorkOS @ 3:34).
4. **Build vs buy matrix** — Enterprise need (EY/Adobe-style) vs team size; cost of harness + eval + integrations (Factory.com framing, `vGCJ7diEtrw`).
5. **Environment claim** — Terminal/IDE/cloud agent surface (Warp, `tUPPVhBBcoM`) vs headless batch only; document where humans steer.
6. **Blast-radius tiers** — Map changes to Pocock-style risk tiers before widening autonomy (pairs with [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md)).
7. **Charter boundary** — Conference narratives do not override programme MUST-PROVE; factory work here is **process design**, not paper claims.

## Quality gate

- [ ] Written **one-sentence factory definition** for your org.
- [ ] **≥1 outcome metric** with measurement source (DX platform, incidents, product analytics).
- [ ] Explicit **“not a factory yet”** list (e.g. no ticket sync, no eval gate).
- [ ] Integration map started (see process-embedded skill) or consciously deferred with reason.
- [ ] No success criterion that is only “more agent PRs merged.”

## Failure modes

| Symptom | Fix | Paris cite |
|---------|-----|------------|
| Executives see demos, not ships | Tie roadmap to outcome metric + embedded process | WorkOS |
| “Factory” is model router only | Add workflow embed + progress tracking | WorkOS @ 3:56 |
| Buy vs build undecided | Cost harness, eval, integrations, refresh loops | Factory.com |
| Agents without product surface | Pick IDE/terminal/cloud home for long runs | Warp Lloyd |

## Provenance

- Ryan Cooke — *No, That’s Not a Software Factory* (`HvboD89DyQ8`)
- Tereza Tížková — *What It Actually Takes to Build a Software Factory* (`vGCJ7diEtrw`)
- Zach Lloyd — *Self-Improving Software Factories* (`tUPPVhBBcoM`)
