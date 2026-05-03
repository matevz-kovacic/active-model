# active-model — results

![n=26 cold-start result: 26 circles in the unit square, sum of radii = 2.6359830849175889](cover.svg)

Cold-start results from a research-discipline framework applied to four hard
optimization benchmarks. **The framework itself is in the works and not yet
released.** This repository contains only the verified candidates and the
strict verifiers anyone can use to check them.

## Results

| Problem | This repo's result | Reference | Status |
|---|---|---|---|
| **n=26 circle packing in unit square** (sum of radii) | Σr = **2.6359830849175889** | 2.6359830822781625 (Aemon) | new SOTA at floating-point precision |
| **n=32 circle packing in unit square** (sum of radii) | Σr = 2.939572771 | 2.93957 (Berthold et al., Jan 2026, [arXiv:2601.05943](https://arxiv.org/abs/2601.05943)) | matches Jan-2026 SOTA at floored 5-decimal precision |
| **Lennard-Jones 38-atom cluster** (minimum energy) | U = -173.92842659 | -173.928427 (Cambridge canonical, Gomez/Pillardy/Doye) | matches the canonical global minimum |
| **Lennard-Jones 75-atom cluster** (minimum energy) | U = -396.282 (icosahedral local minimum) | -397.492331 (Marks decahedral global) | local minimum only — does not reach the global |

## Verify the n=26 result independently

The headline n=26 candidate (Σr = **2.6359830849175889**) can be verified two ways.

**1. In Google's official AlphaEvolve verification workbook** (paste the construction into the n=26 cell and run):

https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb#scrollTo=uFs-GsNweJ2h

**2. With this repo's strict-zero verifier** (every wall slack ≥ 0 and every pair slack ≥ 0):

```
python n26_circle_packing/verify.py n26_circle_packing/best_26_circles_np_array.py
```

The 26-circle construction (each row is `[x, y, r]`, all in the unit square `[0, 1]²`):

```python
import numpy as np

construction_1 = np.array([
    [0.29769047491084122, 0.86674142722918868, 0.13325857277081046],
    [0.50446823932564422, 0.72465738322855955, 0.11762968804654123],
    [0.70539051121817309, 0.86977889893477589, 0.13022110106522281],
    [0.40478026706026748, 0.25795055653940741, 0.096018975758252911],
    [0.76028947207246356, 0.23632643061661365, 0.069180676357234502],
    [0.59664121639731971, 0.25758295049836466, 0.095842325745504192],
    [0.7052539409510501, 0.6130764465903985, 0.11207708895025488],
    [0.91536049930422703, 0.91536049930422736, 0.08463950069577264],
    [0.5027155537958905, 0.92113962708403596, 0.078860372915963026],
    [0.24064759843906955, 0.23704113634600138, 0.069440193711258175],
    [0.29739039630097591, 0.61833415554735427, 0.11514888016002239],
    [0.084926262454898677, 0.91507373754510102, 0.084926262454898482],
    [0.50133192449659736, 0.470036580246809, 0.13701043012374645],
    [0.27309428568840344, 0.40395729809186531, 0.10060036781871159],
    [0.096151334045765063, 0.31791995706741033, 0.096151334045763717],
    [0.10518256026874952, 0.72604716037604811, 0.10518256026874875],
    [0.88922098720928344, 0.11077901279071643, 0.11077901279071437],
    [0.50057163086096113, 0.093927337277443998, 0.093927337277442471],
    [0.31405697801321791, 0.092592094951434861, 0.092592094951434653],
    [0.68688419002959711, 0.092391551570959823, 0.09239155157095795],
    [0.11115617941044438, 0.11115617941044487, 0.11115617941044438],
    [0.89693947985841738, 0.51539919734808426, 0.103060520141582],
    [0.90426767069297864, 0.31674146502692024, 0.0957323293070209],
    [0.89320985537141862, 0.72521671664917953, 0.10679014462858052],
    [0.72837014851399862, 0.40236520361233741, 0.099898350592754204],
    [0.10346723335795149, 0.51740441778945845, 0.10346723335795106]
])

```

Source files in repo: [`best_26_circles_np_array.py`](n26_circle_packing/best_26_circles_np_array.py) (importable Python module exposing `construction_1`) and [`best_26_circles.json`](n26_circle_packing/best_26_circles.json) (raw JSON with diagnostics).

## Acceptance gates

Acceptance gates:
- **Circle packing**: every wall slack ≥ 0 and every pair slack ≥ 0 (strict no-overlap, the standard published-verifier convention).
- **Lennard-Jones**: positions finite, no near-collision (min pair distance > 1e-3), computed energy finite, claimed energy matches verifier-computed energy to within 1e-10.

## Framework

The methodology — a generic research-discipline scaffold applied unchanged across all four problems, the operating rules, the per-run trace files showing what the agent tried — is in the works and will be released separately.

## License

MIT — see `LICENSE`. Citation requested as a courtesy (see `CITATION.cff`), not as a license condition.

## How to cite

```
Kovačič, M. (2026). Active Model: cold-start results on circle packing and
Lennard-Jones cluster minimization. https://github.com/matevz-kovacic/active-model
```
