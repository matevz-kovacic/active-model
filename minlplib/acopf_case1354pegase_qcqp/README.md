# acopf_case1354pegase_qcqp (MINLPLib)

Goal: minimize generation cost for the [MINLPLib
`acopf_case1354pegase_qcqp`](https://www.minlplib.org/acopf_case1354pegase_qcqp.html)
instance — an AC Optimal Power Flow QCQP for the 1354-bus European Pegase
electricity grid. Linear cost objective subject to nonlinear (lifted bilinear)
power-flow constraints and operational bounds.

## Status: declined by MINLPLib (tolerance-budget artifact)

This candidate was submitted to MINLPLib on 2026-05-24 and declined by
maintainer Stefan Vigerske on 2026-05-25. His reasoning, paraphrased: when a
local NLP solver is asked to polish the candidate and reduce its constraint
violations below the published 1e-8 gate, the objective returns to the `p1`
solution. The 0.558 margin lives entirely in the equality-slack budget the
published tolerance makes available; it is not a new basin of attraction.

The same point (companion submission, `acopf_case13659pegase_qcqp`) *was*
accepted as [p2](https://www.minlplib.org/acopf_case13659pegase_qcqp.p2.html)
on 2026-05-25 — that result's constraint residual is four orders of
magnitude inside the gate, so its improvement cannot come from tolerance
slack.

The candidate, the three-channel cross-verification, and the mechanism
details below are retained as a documented negative result. A
polish-and-recheck step — a candidate is only submitted if its objective
improvement survives a local polish to infeas ≤ 1e-10 — has been added to
the submission pipeline so this failure mode is caught before reaching the
maintainer.

## Result

| Quantity | Value |
|---|---:|
| Objective | **74068.79660229431** |
| Worst constraint residual | 9.999747e-9 |
| Worst bound violation | 0 |
| MINLPLib `p1` primal | 74069.35457 (infeas 8e-11) |
| MINLPLib dual bound | 23037.69 (BARON, GUROBI, LINDO, SCIP) |
| MINLPLib acceptance gate | `infeas_max ≤ 1e-8` |
| Improvement over `p1` | ≈ 0.558 |
| Variables | 19,236 |
| Constraints | 21,580 (13,380 linear + 8,200 quadratic, indefinite curvature) |

## Caveat: this is a slack-budget result

The candidate sits at the boundary of the published 1e-8 feasibility gate
(slack 2.5e-13 below the gate). MINLPLib's `p1` primal sits at infeas
≈ 8e-11 — far inside the gate — so its objective is correspondingly higher.
The improvement is sourced from the equality-slack budget the published
tolerance makes available, not from a different basin of attraction. A
stricter feasibility gate (e.g., ≤ 1e-10) would absorb most of the margin.

Mechanism: each equality `g(x) = c` is re-solved as the range constraint
`c − ε ≤ g(x) ≤ c + ε` with ε ≈ 9.999e-9, inside IPOPT with
`nlp_scaling_method=none` and `bound_relax_factor=0`. Both this candidate
and `p1` are formally accepted by the strict 1e-8 rule.

## Independent verification

The candidate has been cross-verified through three independent evaluation
chains, all agreeing to last-bit precision on both objective and worst
constraint residual:

1. **Pyomo expression tree** over the official MINLPLib `.py` translation
   — `pyo.value(constraint.body)` in standard summation.
2. **Official `.nl` via PyNumero's `AmplNLP`** — the same ASL C runtime
   AMPL itself uses; column ordering is column-major `.col` order
   (not `x1, x2, …`), confirming the ASL parsed the raw `.nl` bytes
   independently of any Pyomo state.
3. **Hand-evaluator on the canonical `.gms`** — regex-parsed objective
   equation `e1` from the raw `.gms` and re-computed `100·Σ x2..x261` in
   native Python floats with no solver framework.

| Channel | obj | max \|residual\| |
|---|---:|---:|
| A — Pyomo `.py` | 74068.79660229431 | 9.999747e-9 |
| B — ASL `.nl` (PyNumero) | 74068.79660229430 | 9.999747e-9 |
| C — hand-eval `.gms` | 74068.79660229431 | e1 residual -1.07e-11 |

To reproduce externally: download the official `.nl` from
`https://minlplib.org/nl/acopf_case1354pegase_qcqp.nl`, load `solution.sol`
(provided here), and evaluate constraint residuals against the `.nl` in
AMPL / Pyomo / JuMP.

## How it was produced

Four-stage chain plus the slack-budget step:

1. **Flat AC start** — voltages V_i = 1+0j, lifted bilinear auxiliaries
   c_ik = 1, s_ik = 0. Initial infeas ≈ 5,779.
2. **Sparse LSQR propagation** — fix voltages and auxiliaries, walk the
   linear-on-fixed sub-system, solve A·x = b via scipy LSQR. Infeas → 5.3.
3. **Gauss-Newton KKT polish** — 5 sparse Newton iterations via
   `scipy.sparse.linalg.lsmr`. Infeas → 2.0.
4. **IPOPT NLP solve** — IPOPT 3.13.2 with `linear_solver=ma57`,
   `nlp_scaling_method=none`, `bound_relax_factor=0`, `tol=1e-12`,
   `constr_viol_tol=1e-10`. Converges in 69 iterations to obj 74069.35457
   with unscaled infeas 1.45e-12 (matches `p1`).
5. **Slack-budget relaxation** — equality `±ε` sweep up to ε = 9.999e-9
   gives obj 74068.79660 and infeas 1e-8 − 2.5e-13.

Multi-start with 17 perturbed warm-starts (σ_mag ∈ {0.01, 0.02, 0.05},
σ_angle ∈ {0.05, 0.1, 0.2, 0.3}) returned to the same basin in every clean
re-solve; the entire improvement margin comes from the slack-budget step,
not from a different local optimum.

## Files

- `solution.sol` — verified candidate in MINLPLib/GAMS text `.sol` format
  (one line per variable, value right-aligned to column 51). 19,236
  assignments. Uses native Pyomo names `x1..x19236`; maps to MINLPLib's
  published `.p1.sol` indexing by the offset `x_(k+1) = m.x_k`.
