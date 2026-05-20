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
| 75 atoms | U = -397.4923309829 | -397.492331 (Marks decahedral global) | matches the canonical global minimum | [details](lj75/README.md) |
| 104 atoms | U = -582.0866420676 | -582.086642 (Doye2 C2v Marks-icosahedral global) | matches the canonical global minimum | [details](lj104/README.md) |
