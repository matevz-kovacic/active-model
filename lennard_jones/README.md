# Lennard-Jones Cluster Results

The Lennard-Jones objective is the standard pair potential energy:

```text
U = sum_{i<j} (r_ij^-12 - 2 r_ij^-6)
```

Lower energy is better.

## Results

| Instance | This repo's result | Reference | Status | Details |
|---|---:|---:|---|---|
| 38 atoms | U = -173.92842659 | -173.928427 (Cambridge canonical, Gomez/Pillardy/Doye) | matches the canonical global minimum | [details](lj38/README.md) |
| 75 atoms | U = -396.282 | -397.492331 (Marks decahedral global) | local minimum only; does not reach the global | [details](lj75/README.md) |
