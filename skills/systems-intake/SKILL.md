# systems-intake (stub)

**Status:** outline only — not a shipped instrument. Feeds step 1 of [`interface-first-context`](../interface-first-context/SKILL.md).

## Purpose

Turn Informal Def **1.1** (six systems-theory questions) into a **scope questionnaire** before L1 port/wiring work: slice boundary, parallel products (`‖`), and omissions reasons.

## Six questions (outline)

1. **What is a system here?** — Name compilation units / services that count as nodes (not files for their own sake).
2. **What is an interface?** — Exported ports only: signatures, topics, DTO fields visible from outside.
3. **What is an interaction?** — Typed edges between interfaces (call, ref, import, …); no bodies yet.
4. **What is a system map?** — Vertical maps (refactor, port, mock) you care about for this slice.
5. **What is an interaction map?** — Horizontal compatibility (API version, protocol) across the boundary.
6. **What is omitted and why?** — Bodies, other verticals, shared libs — each with a reason tag (`out-of-slice`, `impl-local`, …).

## Outputs (target)

- Slice path + budget (file count / depth).
- Parallel product marks (`witness/.../savings/ ‖ accounts/`).
- Omissions log table (feeds L1 pack quality gate).

## When to use

- New witness slice or density fixture before writing `// refs:` lines.
- Before hand-authoring a WiringMap v0 JSON instance.

## Not in scope (stub)

- Automated extraction, doctrine proving, or Fineract-scale intake.
