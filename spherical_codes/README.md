# Spherical Codes

For dimension `n`, point count `N`, and unit vectors `x_i` on `S^(n-1)`, the
objective is to minimize:

```text
max_{i<j} x_i . x_j
```

Smaller is better. Equivalently, this maximizes the minimum angular distance.

## Results

| Instance | This repo's result | Reference | Status | Details |
|---|---:|---:|---|---|
| `n=6`, `N=86` | max dot = **0.548916479201208** | 0.548918184883 (Henry Cohn, spherical-codes.org, 2026) | new best numerical code at verifier precision | [details](n6_N86/README.md) |
