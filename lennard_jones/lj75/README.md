# Lennard-Jones 75-Atom Cluster

| Quantity | Value |
|---|---:|
| Energy (submitted) | -397.4923309829 |
| Energy (verifier, double precision) | -397.4923309828756 |
| Reference global minimum | -397.492331 |
| Status | Matches the canonical global minimum at reported precision |
| Structure | D5h Marks decahedron (Doye1) |

Reference: Cambridge Cluster Database canonical LJ75 minimum
(Doye 1995, Wales 1997, Locatelli 2003).

The submitted configuration is the D5h Marks decahedron, reached from a
procedural decahedral seeder built from first geometric principles (fcc
lattice + [110]→z rotation + 72° wedge cut + 5x rotational replication
+ axial column). Parallel basin-hopping from random, Mackay-icosahedral,
fcc, and Ino-decahedron seeds all saturated at the LJ-75 anti-Mackay
icosahedral floor (-396.282249, ≈1.21 ε above the global), consistent
with the canonical LJ-75 "narrow funnel" landscape; only the
geometry-aware decahedral seed reaches the D5h global basin.

Candidate coordinates (`coords.xyz`) and the submission `energy.txt` are
included alongside this README.
