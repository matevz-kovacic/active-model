# n=26 Circle Packing In A Rectangle (Perimeter 4)

Goal: pack 26 non-overlapping circles inside an axis-aligned rectangle whose
width `w` and height `h` satisfy `2(w+h) = 4` (perimeter exactly 4), while
maximizing the sum of radii. Both rectangle dimensions and the per-circle
positions and radii are decision variables.

## Result

| Quantity | Value |
|---|---:|
| Sum of radii | 2.6393205704880214 |
| Reference | 2.63930 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) |
| Rectangle (w × h) | 1.0545001161593104 × 0.9454998838406896 |
| Improvement over reference | ≈ 2.06e-5 (at 5-decimal precision: 2.63932 vs 2.63930) |

## Independent Verification

```bash
python n26_circle_packing_rectangle/verify.py
```

The verifier checks:

1. Rectangle perimeter equals 4 within `tol = 1e-9`.
2. Exactly 26 circles are present.
3. All radii are strictly positive.
4. Every circle is contained in the rectangle (left/right/bottom/top walls), within `tol`.
5. Every pair of circles is non-overlapping (`||c_i - c_j|| >= r_i + r_j - tol`).

## Files

- `solution.json` — verified best configuration (rectangle dimensions and 26 circles).
- `verify.py` — strict-acceptance verifier (PASS on `solution.json`).
