# Spherical Code On S^5, N=98

Goal: find 98 unit vectors in `R^6` minimizing the maximum pairwise dot
product:

```text
max_{i<j} x_i . x_j
```

Smaller is better. Equivalently, this maximizes the minimum angular distance.

## Result

| Quantity | Value |
|---|---:|
| Ambient dimension `n` | 6 |
| Number of points `N` | 98 |
| Max pairwise dot | 0.571037778803683 |
| Minimum angle | 55.17737502697157 deg |
| Reference max pairwise dot | 0.571052839653 |
| Improvement | 1.506084932e-5 |

Reference: Henry Cohn's spherical-codes.org table lists dimension 6, `N=98`
with cosine `0.571052839653` and note "needs more optimization":
https://spherical-codes.org/

## Candidate Data

- `coords.json`: 98 vectors in `R^6`
- `report.json`: captured verification output from the experiment run
- `spherical_codes_upload_n6_N98.txt`: comma-separated one-point-per-line upload format

The upload text preserves the coordinate tokens from `coords.json` exactly.

The captured report records `STATUS: PASS`, worst pair `[25, 42]`, raw norm
range `[0.9999999999999999, 1.0000000000000002]`, and margin
`+1.506084932e-5` against the reference value.

## Method

Started from the published spherical-codes.org coordinate file for `n=6`,
`N=98`, then used LSE-surrogate L-BFGS-B with a beta-ramp polish and multiple
small tangent-perturbation restarts from the best and warm-start candidates.
