# Santa 2025 — Christmas Tree Packing

This was the Kaggle [Santa 2025 — Christmas Tree Packing](https://www.kaggle.com/competitions/santa-2025)
competition, which has since closed. We did not take part in it. The goal here
was simply to improve on the best published result — the winning solution — and
we did, by 0.005648, confirmed by Kaggle's own scorer as a late submission.

## Goal
For each `n = 1..200`, place `n` congruent copies of a fixed non-convex
15-vertex polygon (a stylised Christmas tree), freely translated and rotated,
so that no two overlap and the axis-aligned bounding **square** is as small as
possible. Minimize

```text
S = sum over n = 1..200 of  s_n^2 / n
```

where `s_n` is the side of the smallest axis-aligned square containing puzzle
`n`'s union. Smaller is better. The 200 puzzles are independent, so `S` is a
plain sum of 200 independent sub-problems — 20,100 placements in total.

## Result

| Quantity | Value |
|---|---:|
| Score `S` | **68.774985895860** |
| Seed (published 1st-place solution, re-scored locally) | 68.780634078014 |
| Improvement over the seed | **0.005648182** |
| Competition's winning score | 68.781235119300 |
| Improvement over the winning score | 0.006249223 |
| Regime | **warm-start** — seeded from a published solution |
| Verified by | the official metric locally, and Kaggle's own scorer |

The local gate predicted `68.77498589586094`; Kaggle's server returned
`68.774985895860`, agreeing to every digit Kaggle displays.

Feasibility is unforgiving: a single interior overlap of ~1e-16 in any one
puzzle rejects the entire 200-puzzle submission.

## Method

Starting from the published artifact, the optimizer applied:

1. **An exact overlap oracle.** The tree decomposes *exactly* into four convex
   parts (top triangle, two trapezoids, trunk rectangle) whose areas sum to
   exactly `A_T = 0.245625`, so a separating-axis test over the 16 part-pairs
   is an exact test for the non-convex whole — no approximation. Implemented in
   C with analytic gradients and validated against the official `shapely`
   geometry: **0 disagreements in 6000 random pair tests**, and 80/80 agreement
   at ±1e-11 from the contact boundary.
2. **An adaptive shrinking cell** (Torquato–Jiao / Lubachevsky–Stillinger
   style): shrink the bounding square, relax a penetration² + container²
   objective with L-BFGS, accept only if strictly feasible at a clearance
   margin folded into the penalty — so a converged relaxation is feasible *by
   construction*, with no separate legalisation step.
3. **Deep relaxation**, the single largest lever. Library stopping rules were
   the bottleneck: L-BFGS-B's *relative* `ftol`/`gtol` abort immediately when
   the squared objective is ~1e-18, while disabling them burns the full
   iteration budget after the answer is already found. Replacing both with
   **absolute** violation criteria made deep relaxation affordable — and depth
   was worth ~6× shallow.
4. **Destroy-and-repair (LNS)** at that depth, plus a best-of-per-puzzle merge
   across every pass.

Two full sweeps improved **200/200** and then **186/200** puzzles.

## What did not work

Recorded because the negative results were the more informative half:

- **Clearance compaction.** The seed is jammed at ~5e-10 minimum pair
  clearance; converting the remaining slack to score is worth ~1e-7 in total.
  Measuring that early closed a plausible line of attack in minutes.
- **Global rotation.** `max(w,h)` is not rotation-invariant, so the free global
  orientation looked like unexploited slack. Measured over all 200 puzzles:
  total gain **−3.7e-9**. Already spent.
- **Per-puzzle transfer** (`n` seeded from `n±1`): far worse — +0.114 and
  +0.018 in side on the puzzle tested. Adjacent `n` have genuinely different
  optimal contact topologies.
- **Small `n`.** Already globally optimal: random multistart re-found the
  incumbent's exact optimum for `n=2` in 21 of 64 starts, and `n=1` is provably
  optimal at exactly `1.15/√2`, giving `s_1² = 0.66125`.
- **A better interior.** The optimal 2-tree dimer lattice has density
  **0.807176511**, derived twice independently (random multistart of a periodic
  optimizer, and a least-squares lattice fit to the seed's own interior); a
  4-tree motif reaches the same value. The seed's interior already achieves it,
  and a *perfect*-interior lattice cut with an optimizer-repaired boundary
  **loses by +0.202** in side at `n=200`. The interior strain is the price of a
  tighter boundary, and it is a good trade.

Everything remaining is boundary cost: against the asymptotic-lattice reference
`200·A_T/ρ∞ = 60.860294`, the gap is 7.915, and all of it is the wall.

## Verification

The official verifier is Kaggle's metric notebook, which defines
`class ChristmasTree` and `def score(solution, submission, row_id_column_name)`:

https://www.kaggle.com/code/metric/santa-2025-metric/notebook

Install it, plug in `submission.csv`, and it returns the score. Requires
`shapely==2.1.2`. `verify.py` in this directory does exactly that from the
command line and additionally checks the row count, id set and value format.

## Numerical policy

The relaxation penalises `separation < 5e-10`, and a configuration is accepted
only if every pair clears **1e-10** under the kernel's separating-axis
distance, which is a proven *lower bound* on the true distance. The shipped
candidate's worst measured clearance is 4.997e-10 — about 10× the measured
kernel-vs-gate agreement noise and ~10⁶× the metric's scaled representation
noise, while costing ~1e-7 of score. Values are emitted as `'s' + repr(float)`
(shortest round-tripping form, ≤17 significant digits); the metric discards
anything beyond that.

## Files

- `submission.csv` — the verified result, 20,100 placements, Kaggle-uploadable
  as-is.
- `verdict.json` — the official gate's verdict for exactly those bytes.
- `per_puzzle.csv` — `n, side, group_score, strategy` for all 200 puzzles.
- `verify.py` — standalone strict verifier (see above).
- `NOTICE` — attribution and licensing for the derived submission.

## Attribution

The seed for this run is the published 1st-place solution by **Jeroen
Cottaar** — <https://github.com/jcottaar/packing> (branch `full`,
`res/sol_legalized_{1..200}.pickle`), licensed **CC BY-SA 4.0**. His method was
a genetic algorithm over packing motifs with GPU (CUDA) relaxation of overlap,
island populations, N±1 warm starts and point-symmetry initialisation.

The derived `submission.csv` in this directory is therefore **CC BY-SA 4.0**
(see `NOTICE`). The search code, the geometry kernel, the verifier and this
write-up are original work under the repository's own licence.

The third-party artifacts were read with a whitelisted unpickler; no
third-party code was executed.
