# Spherical Code On S^5, N=86

Goal: find 86 unit vectors in `R^6` minimizing the maximum pairwise dot
product:

```text
max_{i<j} x_i . x_j
```

Smaller is better. Equivalently, this maximizes the minimum angular distance.

## Result

| Quantity | Value |
|---|---:|
| Ambient dimension `n` | 6 |
| Number of points `N` | 86 |
| Max pairwise dot | 0.548916479201208 |
| Minimum angle | 56.70728937071392 deg |
| Reference max pairwise dot | 0.548918184883 |
| Improvement | 1.705681792e-6 |

Reference: Henry Cohn's spherical-codes.org table lists dimension 6, `N=86`
with cosine `0.548918184883` and note "needs more optimization":
https://spherical-codes.org/

## Candidate Data

- `coords.json`: 86 vectors in `R^6`


## Method

Started from the published spherical-codes.org coordinate file for `n=6`,
`N=86`, normalized the vectors, and applied direct scipy SLSQP epigraph minimax
refinement. The saved code improves the published rounded table value by about
`1.7e-6`.
