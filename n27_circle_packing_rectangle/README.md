# n=27 Circle Packing In A Rectangle (Perimeter 4)

Goal: pack 27 non-overlapping circles inside an axis-aligned rectangle whose
width `w` and height `h` satisfy `2(w+h) = 4` (perimeter exactly 4), while
maximizing the sum of radii. Both rectangle dimensions and the per-circle
positions and radii are decision variables.

## Result

| Quantity | Value |
|---|---:|
| Sum of radii | 2.6915233694580554 |
| Reference | 2.69015 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) |
| Rectangle (w × h) | 1.0765013329741009 × 0.9234986670258991 |
| Improvement over reference | ≈ 1.37e-3 (at 5-decimal precision: 2.69152 vs 2.69015) |

## Independent Verification

```bash
python n27_circle_packing_rectangle/verify.py
```

The verifier checks:

1. Rectangle perimeter equals 4 within `tol = 1e-9`.
2. Exactly 27 circles are present.
3. All radii are strictly positive.
4. Every circle is contained in the rectangle (left/right/bottom/top walls), within `tol`.
5. Every pair of circles is non-overlapping (`||c_i - c_j|| >= r_i + r_j - tol`).

The tightest pair slack in `solution.json` is approximately `-4.0e-10`, well
inside the `1e-9` tolerance.

## Files

- `solution.json` — verified best configuration (rectangle dimensions and 27 circles).
- `verify.py` — strict-acceptance verifier (PASS on `solution.json`).
