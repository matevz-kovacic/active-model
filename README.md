# active-model - results

![n=26 cold-start result: 26 circles in the unit square, sum of radii = 2.6359830849175889](cover.svg)

This repository contains verifier-backed numerical results produced by a cold-start optimization agent.

The system currently appears strongest on continuous, geometric, and lightly constrained black-box optimization problems, including circle packing, rectangle packing, spherical codes / Tammes-type problems, and energy minimization.

This is a public result archive, not the full optimization harness. The private harness is available for serious private benchmark evaluation, collaboration, or licensing discussions under a separate agreement.

## What this is

The commercial hypothesis is simple:

> If a problem has an executable evaluator, compact candidate solutions, and feasibility can be checked or repaired automatically, a cold-start optimizer may be able to find improved incumbents without domain-specific manual tuning.

This repository documents public benchmark results where that process produced new best-known numerical results, matched known reference optima, or failed to reach the best-known result.

## Private benchmark evaluation

I am interested in private executable benchmarks where:

- the problem is continuous, geometric, or lightly constrained,
- feasible solutions can be represented compactly,
- an incumbent or baseline solution is available,
- improvement can be independently verified,
- the evaluator is deterministic or reasonably stable,
- the evaluator can be run locally or in a controlled environment.

For private benchmark evaluation or collaboration:

**Matevz Kovacic**  
Email: **matevz.celje@gmail.com**

A useful private test has the following structure:

1. You provide an executable evaluator and one or more incumbent solutions.
2. I run the optimizer without access to your proprietary internal methods.
3. I return candidate solutions, verifier logs, and a short technical report.
4. If there is a verified improvement, we can discuss paid follow-up, licensing, or collaboration.

The optimization harness itself is private. Public result files, verifier scripts, candidate solutions, and technical reports can be shared where appropriate.

## Current best fit

The current system appears best suited for:

- geometric packing,
- spherical / Grassmannian code search,
- continuous nonconvex optimization,
- energy minimization,
- lightly constrained black-box search,
- problems where candidate solutions are compact and cheap to verify.

## Current limitations

This is not a claim of a general-purpose optimizer.

So far, the system has been less successful on:

- routing / placement with many interacting constraints,
- slow or noisy simulators,
- problems dominated by feasibility engineering,
- objectives where the evaluator is hard to reproduce.


## Results

| Problem | This repo's result | Reference | Status | Details |
|---|---:|---:|---|---|
| **n=26 circle packing in unit square** (maximize sum of radii) | sum r = **2.6359830849175889** | 2.6359830822781625 (Aemon) | new SOTA at floating-point precision | [details](n26_circle_packing/README.md) |
| **n=32 circle packing in unit square** (maximize sum of radii) | sum r = 2.939572771 | 2.93957 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) | matches Jan-2026 SOTA at floored 5-decimal precision | [details](n32_circle_packing/README.md) |                                                                                                                                                                                                            
| **n=21 circle packing in a rectangle (perimeter 4)** (maximize sum of radii) | sum r = **2.365832375910822** | 2.3658321334167627 (AlphaEvolve, [DeepMind notebook B.13](https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb#scrollTo=VaSmUodSeJ2i)) | new SOTA at floating-point precision (+2.42e-7) | [details](n21_circle_packing_rectangle/README.md) |
| **n=26 circle packing in a rectangle (perimeter 4)** (maximize sum of radii) | sum r = **2.6393205704880214** | 2.63930 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) | new SOTA at 5-decimal precision (2.63932 vs 2.63930) | [details](n26_circle_packing_rectangle/README.md) |
| **n=27 circle packing in a rectangle (perimeter 4)** (maximize sum of radii) | sum r = **2.691523369458056** | 2.69015 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) | new SOTA (2.69152 vs 2.69015, +1.37e-3) | [details](n27_circle_packing_rectangle/README.md) |
| **Spherical code / Tammes problem on S^5, N=86** (minimize max pairwise dot) | max dot = **0.548916479201208** | 0.548918184883 (Henry Cohn, [spherical-codes.org](https://spherical-codes.org/), 2026, "needs more optimization") | new best numerical code at verifier precision | [details](spherical_codes/n6_N86/README.md) |
| **Spherical code / Tammes problem on S^5, N=98** (minimize max pairwise dot) | max dot = **0.571037778803683** | 0.571052839653 (Henry Cohn, [spherical-codes.org](https://spherical-codes.org/), 2026, "needs more optimization") | new best numerical code at verifier precision | [details](spherical_codes/n6_N98/README.md) |
| **Lennard-Jones 38-atom cluster** (minimum energy) | U = -173.92842659 | -173.928427 (Cambridge canonical, Gomez/Pillardy/Doye) | matches the canonical global minimum | [details](lennard_jones/lj38/README.md) |
| **Lennard-Jones 75-atom cluster** (minimum energy) | U = -396.282 (icosahedral local minimum) | -397.492331 (Marks decahedral global) | local minimum only; does not reach the global | [details](lennard_jones/lj75/README.md) |

## Verification

Each result folder contains the candidate data that is available for that
problem, the relevant reference value, and any result-specific caveats.

For the n=26 circle-packing result, the repository includes a local strict
checker:

```bash
python n26_circle_packing/verify.py n26_circle_packing/best_26_circles.json
```

The three rectangle-packing results each ship their own strict verifier; the
verifier finds the adjacent `solution.json` automatically:

```bash
python n21_circle_packing_rectangle/verify.py
python n26_circle_packing_rectangle/verify.py
python n27_circle_packing_rectangle/verify.py
```

The Tammes/spherical-code entry includes the coordinate file and the captured
verification report from the experiment run; no separate Tammes verifier is
included in this public repository.

## Framework

The public repository is a result and verification archive.

The optimization harness, operating rules, prompts, and full per-run traces are not included in this repository. They are kept separate to preserve the method for private benchmark evaluation, collaboration, or licensing.

For serious technical review, I can provide additional evidence under an appropriate agreement, including selected run logs, verifier outputs, and candidate-generation history.


## License

MIT - see `LICENSE`. Citation requested as a courtesy (see `CITATION.cff`), not
as a license condition.

## How to cite

```text
Kovacic, M. (2026). Active Model: cold-start results on circle packing,
spherical codes, and Lennard-Jones cluster minimization.
https://github.com/matevz-kovacic/active-model
```
