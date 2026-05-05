# n=26 Circle Packing In The Unit Square

Goal: place 26 non-overlapping circles inside the unit square `[0, 1]^2` while
maximizing the sum of radii.

## Result

| Quantity | Value |
|---|---:|
| Sum of radii | 2.6359830849175889 |
| Reference | 2.6359830822781625 |
| Improvement | 2.6394264e-9 |

## Independent Verification

The candidate can be checked two ways.

**1. In Google's official AlphaEvolve verification workbook**

Paste the construction from `best_26_circles_np_array.py` into the n=26 cell
and run:

https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb#scrollTo=uFs-GsNweJ2h

**2. With this repo's strict-zero verifier**

```bash
python n26_circle_packing/verify.py n26_circle_packing/best_26_circles.json
```

The verifier checks every wall slack and every pair slack with the strict
non-overlap convention: all slacks must be nonnegative.

## Files

- `best_26_circles_np_array.py`: importable Python module exposing `construction_1`
- `best_26_circles.json`: raw JSON candidate
- `verify.py`: strict verifier for the candidate
