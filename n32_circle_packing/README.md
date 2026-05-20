# n=32 Circle Packing In The Unit Square

Goal: place 32 non-overlapping circles inside the unit square `[0, 1]^2` while
maximizing the sum of radii.

## Result

| Quantity | Value |
|---|---:|
| Sum of radii | **2.9395727712007664** |
| Reference | 2.939572726664292 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943); raw data at [DominikKamp/Packing](https://github.com/DominikKamp/Packing/blob/main/square/n32/circlepacking_n32.txt)) |
| Improvement over reference | ≈ 4.45e-8 (new SOTA at floating-point precision) |

## Independent Verification

The candidate can be checked two ways.

**1. In Google's official AlphaEvolve verification workbook**

Paste the construction from [`solution.py`](solution.py) (the exact `numpy`
array of 32 `(x, y, r)` rows used to obtain the result) into the n=32 cell
(section B.12, "Packing circles inside a unit square to maximize sum of
radii") and run:

https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb#scrollTo=yBRzd7AZeJ2h

For context, AlphaEvolve's own reported best for n=32 is 2.937 (Construction 2
in the same section).

**2. With this repo's strict-zero verifier**

```bash
python n32_circle_packing/verify.py
```

The verifier checks:

1. Exactly 32 circles are present.
2. All radii are strictly positive.
3. Every circle is contained in the unit square `[0, 1]^2`, within `tol = 1e-9`.
4. Every pair of circles is non-overlapping (`||c_i - c_j|| >= r_i + r_j - tol`).

## Files

- `solution.json` — verified best configuration (32 circles).
- `solution.py` — same configuration as a `numpy.ndarray` of shape `(32, 3)` (rows `[x, y, r]`).
- `verify.py` — strict-acceptance verifier (PASS on `solution.json`).
