# PROTOCOL-E1 — recovered inventory stub

`RECOVERY.md` records that the authoritative `experiments/PROTOCOL-E1.md` was restored verbatim in
another recovery pass, but that file is not present in this checkout. This stub preserves the
recoverable protocol facts without inventing the missing step-by-step text.

## Recoverable protocol facts

- Experiment: **E1 witness**.
- Purpose: demonstrate that "codebase = module of systems" can be checked on a concrete toy gluing.
- Scope: **16-file toybank** / `C₀` SymTab scale.
- Result: **13/13** checks pass.
- Known caveats: toy scale; bounded-enumeration universal-property check; demonstrated ≠ proved.
- Repairs caught adversarially during the original session: degenerate associativity and a vacuous
  Ex 4.25 lift.

For the authoritative outcome, use `witness/WITNESS.json`, `README.md`, and `HANDOFF.md` until the
bundle copy of the verbatim protocol is re-attached.
