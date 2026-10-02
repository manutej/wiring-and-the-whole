# Merge conflict review (2026-10-01)

Plain-language goal: bring **`main`** (witness docs landed in PR #5) into the open feature branches so PRs can merge without surprise.

## Branch stack (before this pass)

```
                    d96bfbd  origin/main  "witness E1 docs (#5)"
                         |
         +---------------+---------------+---------------+---------------+
         |               |               |               |               |
    witness-diagrams  interface-first  repro-runner   dogfood-l1    ascii-reporting
    (PR #5 MERGED)    (PR #6 OPEN)     (PR #7 OPEN)   (PR #8 DRAFT) (PR #9 DRAFT)
         |               |               |               |               |
    same topic as     + BUILD-OUT      + BUILD-OUT     docs only     HANDOFF note
    main (already)      memo fork        memo fork
```

**What happened:** Several branches each added `docs/roadmap/BUILD-OUT-RESEARCH.md` independently while `main` received a similar file from the merged witness PR. Git sees that as **add/add** (two new files with the same path), not a line-by-line edit conflict.

## Summary table

| Branch | Conflicted files | Simple / complicated | Action |
|--------|------------------|----------------------|--------|
| `cursor/witness-diagrams-cd12` | *(none)* | — | Merged `origin/main` cleanly; pushed merge commit. PR #5 already merged; branch is historical. |
| `cursor/interface-first-context-skill-cd12` | `docs/roadmap/BUILD-OUT-RESEARCH.md` | **Simple** | Merged `main`; kept branch **Status** rows (skill marked shipped) + struck-through “next commit” item. |
| `cursor/repro-runner-cd12-ed6e` | `docs/roadmap/BUILD-OUT-RESEARCH.md` | **Simple** | Merged `main`; kept branch **verify shipped** status; noted E5 still outside `make verify`. `make verify` **PASS** after merge. |
| `cursor/dogfood-l1-self-cd12` | *(none)* | — | Merged `origin/main` cleanly; pushed. |
| `cursor/ascii-reporting-note-cd12` | *(none)* | — | Merged `origin/main` cleanly; pushed. |

**Complicated conflicts:** none — all overlaps were the same research memo with different **progress checkboxes** (shipped vs todo).

## Simple conflict pattern (for non-git readers)

1. **`main`** got a new planning doc from the witness work.
2. **Feature branches** also added that doc when they were written, with updates like “verify harness done” or “skill minted.”
3. Git could not pick one whole file automatically.
4. Fix: **one combined doc** — keep witness content from `main`, keep each branch’s honest **Status** lines for what that branch actually ships.

## PR links (updated branches pushed)

| PR | URL |
|----|-----|
| #6 interface-first-context | https://github.com/manutej/wiring-and-the-whole/pull/6 |
| #7 repro-runner / verify | https://github.com/manutej/wiring-and-the-whole/pull/7 |
| #8 dogfood L1 | https://github.com/manutej/wiring-and-the-whole/pull/8 |
| #9 ASCII HANDOFF note | https://github.com/manutej/wiring-and-the-whole/pull/9 |
| #5 witness (merged) | https://github.com/manutej/wiring-and-the-whole/pull/5 |

## Branches still blocked

None from merge conflicts. **Ordering note (not a git block):** PR #6 and PR #7 both touch `BUILD-OUT-RESEARCH.md` status rows; merge whichever lands first, then re-sync the other if GitHub shows a new conflict on the memo only.

## Commands used

- Strategy: **`git merge origin/main`** on each branch (consistent merge, not rebase).
- Verification: **`make verify`** on `cursor/repro-runner-cd12-ed6e` after conflict resolution.
