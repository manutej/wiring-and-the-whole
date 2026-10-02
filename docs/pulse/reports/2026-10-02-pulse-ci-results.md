# Pulse report — CI blind-pack results guard (2026-10-02)

## Metadata

| Field | Value |
|-------|-------|
| Pulse round name | `2026-10-02-pulse-ci-results` |
| Start time (UTC) | `2026-10-02T15:41:00Z` |
| End time (UTC) | `2026-10-02T15:44:30Z` |
| How long (minutes) | ~4 (implementation, docs, and merge checks) |
| Working branch | `cursor/pulse-ci-results-cd12` |
| Pull request | https://github.com/manutej/wiring-and-the-whole/pull/28 |

### Agents

| Role | Who | Notes |
|------|-----|-------|
| Builder | bc-97d94c63-b76c-506e-80a1-59cb646435d1 | cloud agent |
| Challenge reviewers | bc-97d94c63-b76c-506e-80a1-59cb646435d1 | adversarial notes in separate file |
| Independent scorer | bc-97d94c63-b76c-506e-80a1-59cb646435d1 | scorecard filed; rubric not shown in this report |

### Gate timing

| Check | Elapsed |
|-------|---------|
| Full repo witness check | ~1 s |
| Full pulse loop (verify plus automated test battery), first run | ~9 s |
| Full pulse loop (verify plus automated test battery), second run | ~9 s |
| Automated test battery alone (33 checks) | ~9 s |

---

## Done

- Added a command that checks the saved blind reading-pack results file against its agreed shape and confirms live stub grades still match the saved rows.
- Wired that command into the automated pulse test battery, including a test that fails when someone changes question counts in the saved file without updating the real run.
- Wrote the implementer brief, challenge notes, scorer sheet, and updated the short status page so the next scale step points at live model baselines instead of this guard.

## Tested

- The full repo witness check passed on the branch (three frozen comparison steps).
- The full pulse loop ran twice; each time the witness check and thirty-three automated tests passed with zero failures.
- Ran the depth experiment grading script once on frozen answers (not part of default verify); archived-results check and deliberate wrong saved file both behaved as expected.

## Next

- Open and merge the pull request; refresh the pinned saved results file whenever the blind harness adds or removes reading packs.
- Turn on live model baselines and fill accuracy placeholders when ready to claim real comprehension scores.
- Add a schema-only failure test for badly typed optional fields in the saved results file if the panel wants stronger negative coverage.
