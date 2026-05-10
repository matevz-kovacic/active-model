"""
Strict-acceptance verifier for the n=27 circle-packing-in-rectangle task.

Reads ./solution.json, runs the gates from PROBLEM_TASK.md, prints a
PASS/FAIL line, the score, and on rejection the failing check.
Exits 0 on PASS, non-zero on FAIL.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

TOL = 1e-9
N_REQUIRED = 27
PERIM_REQUIRED = 4.0


def fail(msg: str, score: float = 0.0) -> int:
    print(f"FAIL: {msg}")
    print(f"score: {score}")
    return 1


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent
    path = Path(argv[1]) if len(argv) > 1 else here / "solution.json"
    if not path.is_file():
        return fail(f"solution file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot parse JSON: {exc}")

    # Rectangle
    rect = data.get("rectangle")
    if not isinstance(rect, dict):
        return fail("rectangle missing or not an object")
    try:
        w = float(rect["w"])
        h = float(rect["h"])
    except Exception as exc:
        return fail(f"rectangle.w/.h not parseable: {exc}")

    if not (w > 0):
        return fail(f"rectangle width not positive: w={w}")
    if not (h > 0):
        return fail(f"rectangle height not positive: h={h}")
    perim = 2.0 * (w + h)
    if abs(perim - PERIM_REQUIRED) > TOL:
        return fail(f"perimeter {perim} != {PERIM_REQUIRED} (tol={TOL})")

    # Circles
    circles = data.get("circles")
    if not isinstance(circles, list):
        return fail("circles missing or not a list")
    if len(circles) != N_REQUIRED:
        return fail(f"need exactly {N_REQUIRED} circles, got {len(circles)}")

    xs = []
    ys = []
    rs = []
    for i, c in enumerate(circles):
        try:
            x = float(c["x"])
            y = float(c["y"])
            r = float(c["r"])
        except Exception as exc:
            return fail(f"circle {i} unparseable: {exc}")
        if not (r > 0):
            return fail(f"circle {i} radius not positive: r={r}")
        # Containment with tol
        if r > x + TOL:
            return fail(f"circle {i} crosses left wall (r={r}, x={x}, slack={x - r})")
        if x + r > w + TOL:
            return fail(f"circle {i} crosses right wall (x+r={x+r}, w={w}, slack={w - x - r})")
        if r > y + TOL:
            return fail(f"circle {i} crosses bottom wall (r={r}, y={y}, slack={y - r})")
        if y + r > h + TOL:
            return fail(f"circle {i} crosses top wall (y+r={y+r}, h={h}, slack={h - y - r})")
        xs.append(x)
        ys.append(y)
        rs.append(r)

    # Non-overlap
    n = len(rs)
    worst_pair = None
    worst_slack = math.inf
    for i in range(n):
        xi, yi, ri = xs[i], ys[i], rs[i]
        for j in range(i + 1, n):
            xj, yj, rj = xs[j], ys[j], rs[j]
            d = math.hypot(xi - xj, yi - yj)
            slack = d - (ri + rj)
            if slack < worst_slack:
                worst_slack = slack
                worst_pair = (i, j, d, ri + rj)
            if slack < -TOL:
                return fail(
                    f"circles {i} and {j} overlap: d={d}, r_i+r_j={ri+rj}, slack={slack}"
                )

    score = sum(rs)
    print(f"PASS: rectangle={w}x{h}, perim={perim}, n={n}, score={score:.16f}")
    if worst_pair is not None:
        i, j, d, rsum = worst_pair
        print(
            f"tightest pair: ({i},{j}) d={d:.16f} r_i+r_j={rsum:.16f} slack={worst_slack:.3e}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
