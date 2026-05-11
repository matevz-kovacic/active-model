# n=21 Circle Packing In A Rectangle (Perimeter 4)

Goal: pack 21 non-overlapping circles inside an axis-aligned rectangle whose
width `w` and height `h` satisfy `2(w+h) = 4` (perimeter exactly 4), while
maximizing the sum of radii. Both rectangle dimensions and the per-circle
positions and radii are decision variables.

## Result

| Quantity | Value |
|---|---:|
| Sum of radii | 2.365832375910822 |
| Reference | 2.3658321334167627 (AlphaEvolve, [DeepMind notebook B.13](https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb#scrollTo=VaSmUodSeJ2i)) |
| Rectangle (w × h) | 1.0232688964699053 × 0.9767311035300947 |
| Improvement over reference | ≈ 2.42e-7 (new SOTA at floating-point precision) |

## Independent Verification

```bash
python n21_circle_packing_rectangle/verify.py
```

The verifier checks:

1. Rectangle perimeter equals 4 within `tol = 1e-9`.
2. Exactly 21 circles are present.
3. All radii are strictly positive.
4. Every circle is contained in the rectangle (left/right/bottom/top walls), within `tol`.
5. Every pair of circles is non-overlapping (`||c_i - c_j|| >= r_i + r_j - tol`).

## Files

- `solution.json` — verified best configuration (rectangle dimensions and 21 circles).
- `verify.py` — strict-acceptance verifier (PASS on `solution.json`).
