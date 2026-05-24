# acopf_case13659pegase_qcqp (MINLPLib)

Goal: minimize generation cost for the [MINLPLib
`acopf_case13659pegase_qcqp`](https://www.minlplib.org/acopf_case13659pegase_qcqp.html)
instance — an AC Optimal Power Flow QCQP for the 13,659-bus European Pegase
electricity grid. Linear cost objective subject to nonlinear (lifted bilinear)
power-flow constraints and operational bounds.

## Result

| Quantity | Value |
|---|---:|
| Objective | **386106.5446322** |
| Worst constraint residual | 1.788e-12 |
| Worst bound violation | 0 |
| MINLPLib `p1` primal | 386108.80970 (infeas 1e-10) |
| MINLPLib dual bound | 225681.29 (BARON, LINDO, SCIP) |
| MINLPLib acceptance gate | `infeas_max ≤ 1e-8` |
| Improvement over `p1` | ≈ 2.265 |
| Variables | 199,281 (27,318 nonlinear) |
| Constraints | 191,097 (136,504 linear + 54,593 quadratic, indefinite curvature) |

## Different basin, not a slack-budget exploit

Worst constraint residual is 1.79e-12 — ~4 orders of magnitude inside the
published 1e-8 gate. The improvement is not sourced from the tolerance
budget; it comes from a different active set. A different set of
generators sit at their upper Pg bounds in this basin than in `p1`'s
basin. The dispatch pattern itself is different.

## How it was produced

Warm-started from MINLPLib's `p1` primal, then:

1. **Inject `p1` into the binary `.nl` initial-primal section** — overwrite
   the byte range `3235199..5626575` (199,281 records of int32 idx +
   float64 value) in place to seed IPOPT.
2. **IPOPT 3.12.13 (MUMPS) with adaptive μ** —
   `mu_strategy=adaptive`, `mu_oracle=quality-function`, `mu_init=0.1`,
   `warm_start_init_point=yes`, `bound_push=1e-4`, `bound_frac=1e-4`,
   `honor_original_bounds=no`, `nlp_scaling_method=gradient-based`,
   `max_iter=80`. The trajectory *leaves* `p1`'s basin (obj climbs to
   ≈ 386,870 around iter 14), then descends through ≈ 386,300 (iter 30),
   ≈ 386,120 (iter 60), and reaches obj ≈ 386,106.54 by iter 80 — a
   different basin than `p1`'s 386,108.81. IPOPT exits at the iteration
   cap with constraint violation ≈ 5.3e-5 (still infeasible at this
   stage; the .sol is written normally because IPOPT exits via
   "Maximum Number of Iterations Exceeded", not via signal).
3. **Gauss-Newton projection polish** — three iterations of
   `(JJᵀ) y = -r` (via `scipy.sparse.spsolve`) with backtracking on
   `x ← x + α·Jᵀ y`. Constraint violation drops
   5.3e-5 → 2.7e-5 → 9.3e-8 → **1.79e-12**, objective essentially
   unchanged.

Other strategies tried that did *not* reach this basin: voltage
perturbations of σ ∈ {0.001, 0.005} (crashed in MUMPS factorization or
converged to a worse basin around obj 386,114); generator-output
perturbations (obj climbed to 386,600+); cold flat start (IPOPT stuck in
restoration).

## Independent verification

The source-run verifier loads the official binary `.nl` via Pyomo's
`AmplNLP`, parses the binary `.sol` (Fortran-unformatted records:
length-prefix + data + length-trailer; record 6 carries the n primals),
and evaluates every active constraint residual + every bound violation in
unscaled Python floats.

To reproduce externally:

1. Download the official `.nl` from
   `https://minlplib.org/nl/acopf_case13659pegase_qcqp.nl`
   (SHA-256: `ea7892ec2c92b9f4cf77f0f908731d9e5fa0186dd3101b917d1e35b48d36b978`).
2. Load `best.sol` (provided here) and evaluate constraint residuals
   against the `.nl`. Expect obj 386106.5446322, max \|residual\| 1.788e-12.

## Files

- `best.sol` — verified candidate in MINLPLib/GAMS text `.sol` format
  (one line per variable, value right-aligned to column 51). 199,281
  assignments.
