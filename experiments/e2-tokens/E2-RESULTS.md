# E2-RESULTS

## Question

Is the factored `(seed, marking, motif)` form actually cheaper than explicit edge lists?

## Authoritative recovered results

| Site | Family (repo-wide n) | explicit e | factored m | legend+motif F | break-even n* | verdict |
|---|---|---|---|---|---|---|
| `SavingsAccountsApiResource` | ApiResource (169) | 329 | 216 | 148 | 2 | WIN |
| `SavingsAccountRepositoryWrapper` | RepositoryWrapper (54) | 326 | 209 | 150 | 2 | WIN |
| `ActivateSavingsAccountCommandHandler` | `@CommandType` handler (514) | 62 | 27 | 152 | 5 | WIN |

## What this MAY mean

- Factored serialization is cheaper than explicit edge lists at micro-scale on these three real
  Spring/Fineract sites.
- The re-expansion gate was byte-identical.
- L2 token arithmetic is live at micro-scale.

## What this MAY NOT mean

- Repo-scale savings have been shown.
- Cross-corpus generality has been shown.
- CR@F95, L3/L4, or benchmark superiority have been shown.
