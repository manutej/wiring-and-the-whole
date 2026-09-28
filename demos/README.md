# Demos — the wiring meets the tape

Ten interactive demos live in the sibling repo, under
[`manutej/jev-tape/demos`](https://github.com/manutej/jev-tape/tree/main/demos). They put one construct of
this corpus (a wiring pack, a pushout with its κ check, the E1 witness, the E2 arithmetic, the E3/E5
grades, the operadic-interview trees, the claims ladder) next to one construct of jev-tape (a typed
question, one answer map per gate, code that routes GREEN / AMBER / RED, a tape that records across crash
and replay), and drive it with this repo's own numbers.

| # | demo | what from here | what from the tape |
|---|---|---|---|
| 01 | pack gate | pack B legend, E5 → E5.1 (D7 0.25 → 0.708) | decision gate, one batched request |
| 02 | apply-last square | E1 system map + Ex 4.25 squares | the loop, crash/replay, C10 |
| 03 | κ path zero | E1 step 9 Money collision | path 0: code, no judge |
| 04 | rank wide, read narrow | E3 pack B, 30 handlers, 4 deviants | one Score request, shortlist to the reader |
| 05 | theater detector | E5 OC trees (10 → 6 compose-valid) | witness before judge; bounded fork |
| 06 | depth router | E5.1 per-depth strict + recall | dual axis θ / floor |
| 07 | claim verify lane | MAY / MAY NOT ladder | lane 2: verified / contradicted / unsupported |
| 08 | tape as module | the pack format applied to jev-tape/src | three planes, the Activity seam |
| 09 | two clocks | E3 pack B lines + planted lines | lane 3 screen; replay keeps the block |
| 10 | witness tape | E1 13/13 | Event History, C10 at the last rung |

Every number on every page is read from the files in this repo by `jev-tape/demos/build-data.mjs`
(SHA-256 of each source is recorded in `jev-tape/demos/META/03_PROVENANCE.md`). The judge on every page is a
deterministic twin; no TypeSafe call is made. Claims discipline travels with the demos: demonstrated ≠
proved, consistency ≠ correctness, models ≠ measurements.

To rebuild the data, check out both repos side by side and run `node demos/build-data.mjs` from `jev-tape`
(set `WIRING=` if this repo is elsewhere). Real `cl100k_base` counts need `npm install` in `experiments/`.
