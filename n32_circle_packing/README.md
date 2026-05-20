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
