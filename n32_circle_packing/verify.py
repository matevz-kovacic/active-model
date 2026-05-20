"""verify.py -- strict acceptance gate for circle_packing_n32.

Reads `solution.json` from the current directory, runs the strict
acceptance gate defined in CIRCLE_PACKING_N32_TASK.md, additionally
checks `solution.py` for shape and coordinate consistency, and exits:

    0  on PASS  -- prints "PASS  S=<sum>  feasible  threshold=<t>"
    1  on FAIL  -- prints "FAIL  <reason>"

Usage:
    python verify.py

This is the bootstrap-shipped stub. The gate logic is complete and
binding. The agent may polish diagnostics, but must NOT loosen any
tolerance and must NOT relax the strict S > 2.93957 inequality.
Tolerances may only be TIGHTENED (with a matching HARNESS_SPEC.md
section-13 decision and an update to CIRCLE_PACKING_N32_TASK.md).

TODOs left for the research agent:
  * Confirm the external Google AlphaEvolve checker uses the same
    tolerance conventions. If it is stricter, tighten TOL_GEO and
    TOL_PAIR here so that any solution passing verify.py also passes
    the external checker.
  * Optional: add a `--verbose` mode that prints per-circle slacks
    and the pair contact graph (useful while debugging local maxima).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


# ---------- Strict acceptance gate parameters (load-bearing) ----------

N_CIRCLES = 32
SUM_RADII_THRESHOLD = 2.93957       # strict gate: S MUST be > this value
TOL_POS = 1e-12                     # radius positivity
TOL_GEO = 1e-9                      # in-bounds linear slack
TOL_PAIR = 1e-9                     # pair squared-distance slack
TOL_FILE_MATCH = 1e-9               # solution.py vs solution.json per coord
TOL_SUM_CLAIMED = 1e-9              # claimed sum_radii vs computed

HERE = Path(__file__).resolve().parent
SOLUTION_JSON = HERE / "solution.json"
SOLUTION_PY = HERE / "solution.py"


def _fail(msg: str) -> "NoReturn":
    print(f"FAIL  {msg}")
    sys.exit(1)


def _load_solution_json() -> tuple[float | None, list[tuple[float, float, float]]]:
    if not SOLUTION_JSON.exists():
        _fail(f"solution.json not found at {SOLUTION_JSON}")
    try:
        data = json.loads(SOLUTION_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(f"solution.json is not valid JSON: {exc}")

    if not isinstance(data, dict):
        _fail("solution.json top-level must be a JSON object")
    if "circles" not in data:
        _fail("solution.json missing 'circles' field")

    circles_raw = data["circles"]
    if not isinstance(circles_raw, list):
        _fail("solution.json 'circles' must be a list")
    if len(circles_raw) != N_CIRCLES:
        _fail(
            f"solution.json must list exactly {N_CIRCLES} circles, "
            f"got {len(circles_raw)}"
        )

    circles: list[tuple[float, float, float]] = []
    for idx, entry in enumerate(circles_raw):
        if not isinstance(entry, dict):
            _fail(f"circle #{idx} must be a JSON object")
        for key in ("x", "y", "r"):
            if key not in entry:
                _fail(f"circle #{idx} missing field '{key}'")
            if not isinstance(entry[key], (int, float)):
                _fail(f"circle #{idx} field '{key}' must be numeric")
            if not math.isfinite(float(entry[key])):
                _fail(f"circle #{idx} field '{key}' is not finite")
        circles.append(
            (float(entry["x"]), float(entry["y"]), float(entry["r"]))
        )

    sum_claimed = data.get("sum_radii", None)
    if sum_claimed is not None:
        if not isinstance(sum_claimed, (int, float)) or not math.isfinite(
            float(sum_claimed)
        ):
            _fail("solution.json 'sum_radii' present but not a finite number")
        sum_claimed = float(sum_claimed)

    return sum_claimed, circles


def _load_solution_py_array() -> np.ndarray:
    if not SOLUTION_PY.exists():
        _fail(f"solution.py not found at {SOLUTION_PY}")

    namespace: dict = {}
    try:
        exec(  # noqa: S102 -- this file is a trusted output of the agent
            compile(
                SOLUTION_PY.read_text(encoding="utf-8"),
                str(SOLUTION_PY),
                "exec",
            ),
            namespace,
        )
    except Exception as exc:
        _fail(f"solution.py failed to execute: {exc!r}")

    if "circles" not in namespace:
        _fail("solution.py must define a top-level `circles` array")

    arr = namespace["circles"]
    if not isinstance(arr, np.ndarray):
        _fail(
            "solution.py `circles` must be a numpy.ndarray "
            f"(got {type(arr).__name__})"
        )
    if arr.shape != (N_CIRCLES, 3):
        _fail(
            f"solution.py `circles` must be shape ({N_CIRCLES}, 3), "
            f"got {arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        _fail("solution.py `circles` contains non-finite entries")

    return arr.astype(float)


def _check_in_bounds(circles: list[tuple[float, float, float]]) -> None:
    for i, (x, y, r) in enumerate(circles):
        if r < TOL_POS:
            _fail(f"circle #{i} has non-positive radius: r={r!r}")
        if x - r < -TOL_GEO:
            _fail(
                f"circle #{i} out of bounds (left wall): "
                f"x={x!r}, r={r!r}, slack={x - r:.3e}"
            )
        if 1.0 - x - r < -TOL_GEO:
            _fail(
                f"circle #{i} out of bounds (right wall): "
                f"x={x!r}, r={r!r}, slack={1.0 - x - r:.3e}"
            )
        if y - r < -TOL_GEO:
            _fail(
                f"circle #{i} out of bounds (bottom wall): "
                f"y={y!r}, r={r!r}, slack={y - r:.3e}"
            )
        if 1.0 - y - r < -TOL_GEO:
            _fail(
                f"circle #{i} out of bounds (top wall): "
                f"y={y!r}, r={r!r}, slack={1.0 - y - r:.3e}"
            )


def _check_non_overlap(circles: list[tuple[float, float, float]]) -> None:
    n = len(circles)
    for i in range(n):
        xi, yi, ri = circles[i]
        for j in range(i + 1, n):
            xj, yj, rj = circles[j]
            dx = xi - xj
            dy = yi - yj
            d2 = dx * dx + dy * dy
            sum2 = (ri + rj) ** 2
            slack = d2 - sum2
            if slack < -TOL_PAIR:
                _fail(
                    f"pair ({i},{j}) overlaps: "
                    f"d^2={d2:.15e}, (r_i+r_j)^2={sum2:.15e}, "
                    f"slack={slack:.3e}"
                )


def _check_consistency(
    json_circles: list[tuple[float, float, float]],
    py_array: np.ndarray,
) -> None:
    for i, (x, y, r) in enumerate(json_circles):
        px, py_, pr = py_array[i]
        if abs(float(px) - x) > TOL_FILE_MATCH:
            _fail(
                f"solution.py row {i} x mismatch: "
                f"json={x!r}, py={float(px)!r}"
            )
        if abs(float(py_) - y) > TOL_FILE_MATCH:
            _fail(
                f"solution.py row {i} y mismatch: "
                f"json={y!r}, py={float(py_)!r}"
            )
        if abs(float(pr) - r) > TOL_FILE_MATCH:
            _fail(
                f"solution.py row {i} r mismatch: "
                f"json={r!r}, py={float(pr)!r}"
            )


def main() -> int:
    sum_claimed, circles = _load_solution_json()
    py_arr = _load_solution_py_array()

    _check_consistency(circles, py_arr)
    _check_in_bounds(circles)
    _check_non_overlap(circles)

    sum_radii = sum(r for _, _, r in circles)
    if sum_claimed is not None and abs(sum_claimed - sum_radii) > TOL_SUM_CLAIMED:
        _fail(
            f"claimed sum_radii={sum_claimed!r} disagrees with computed "
            f"{sum_radii!r} (|delta|={abs(sum_claimed - sum_radii):.3e})"
        )

    if not (sum_radii > SUM_RADII_THRESHOLD):
        _fail(
            f"sum_radii = {sum_radii:.15f} does not strictly exceed "
            f"threshold {SUM_RADII_THRESHOLD}"
        )

    print(
        f"PASS  S={sum_radii:.15f}  feasible  "
        f"threshold={SUM_RADII_THRESHOLD}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
