"""Strict acceptance verifier for circle-packing-in-rectangle (n=21, perimeter=4).

Reads solution.json from the same directory and runs all checks.
Prints PASS / FAIL with the first failing check (if any) and the score.
Exit code 0 on PASS, non-zero on FAIL.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path


N_REQUIRED = 21
PERIMETER = 4.0
TOL = 1e-9


def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check(sol: dict) -> tuple[bool, str, float]:
    # 1. Rectangle present
    if "rectangle" not in sol:
        return False, "rectangle missing", 0.0
    rect = sol["rectangle"]
    if "w" not in rect or "h" not in rect:
        return False, "rectangle.w or rectangle.h missing", 0.0
    w, h = float(rect["w"]), float(rect["h"])
    if not (w > 0 and h > 0):
        return False, f"rectangle dims must be positive: w={w}, h={h}", 0.0
    if abs(2 * (w + h) - PERIMETER) > TOL:
        return False, f"perimeter check failed: 2(w+h)={2*(w+h)} vs {PERIMETER}", 0.0

    # 2. Count exactly N_REQUIRED
    circles = sol.get("circles", [])
    if len(circles) != N_REQUIRED:
        return False, f"expected {N_REQUIRED} circles, got {len(circles)}", 0.0

    # 3. Positivity of radii
    xs, ys, rs = [], [], []
    for i, c in enumerate(circles):
        if not all(k in c for k in ("x", "y", "r")):
            return False, f"circle {i} missing x/y/r", 0.0
        xi, yi, ri = float(c["x"]), float(c["y"]), float(c["r"])
        if not (ri > 0):
            return False, f"circle {i} non-positive radius r={ri}", 0.0
        xs.append(xi)
        ys.append(yi)
        rs.append(ri)

    # 4. Containment
    for i in range(N_REQUIRED):
        if not (rs[i] - xs[i] <= TOL):
            return False, f"circle {i} crosses left wall: x={xs[i]} r={rs[i]}", 0.0
        if not (xs[i] + rs[i] - w <= TOL):
            return False, f"circle {i} crosses right wall: x={xs[i]} r={rs[i]} w={w}", 0.0
        if not (rs[i] - ys[i] <= TOL):
            return False, f"circle {i} crosses bottom wall: y={ys[i]} r={rs[i]}", 0.0
        if not (ys[i] + rs[i] - h <= TOL):
            return False, f"circle {i} crosses top wall: y={ys[i]} r={rs[i]} h={h}", 0.0

    # 5. Non-overlap
    for i in range(N_REQUIRED):
        for j in range(i + 1, N_REQUIRED):
            dx = xs[i] - xs[j]
            dy = ys[i] - ys[j]
            d = math.hypot(dx, dy)
            need = rs[i] + rs[j]
            if d + TOL < need:
                return False, (
                    f"overlap circles {i} and {j}: d={d} need>={need} "
                    f"(deficit {need - d:.3e})"
                ), 0.0

    score = sum(rs)
    return True, "all checks pass", score


def main() -> int:
    here = Path(__file__).resolve().parent
    sol_path = here / "solution.json"
    if not sol_path.exists():
        print(f"FAIL: solution.json not found at {sol_path}")
        return 2
    try:
        sol = load(sol_path)
    except Exception as e:
        print(f"FAIL: could not parse solution.json: {e}")
        return 2

    ok, msg, score = check(sol)
    if ok:
        print(f"PASS: score={score:.12f} ({msg})")
        return 0
    else:
        print(f"FAIL: {msg}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
