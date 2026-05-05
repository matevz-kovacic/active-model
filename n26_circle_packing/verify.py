#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path


def load_candidate(path: Path) -> list[list[float]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return [[float(c) for c in row] for row in data["circles"]]

    spec = importlib.util.spec_from_file_location("candidate", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    rows = getattr(mod, "construction_1")
    if hasattr(rows, "tolist"):
        rows = rows.tolist()
    return [[float(c) for c in row] for row in rows]


def verify(circles: list[list[float]]) -> dict:
    if len(circles) != 26:
        raise ValueError(f"expected 26 circles, got {len(circles)}")
    for i, row in enumerate(circles):
        if len(row) != 3:
            raise ValueError(f"circle {i} must be [x, y, r]")
        if not all(math.isfinite(v) for v in row):
            raise ValueError(f"circle {i} has non-finite component")
        if row[2] < 0.0:
            raise ValueError(f"circle {i} has negative radius")

    wall_slacks = []
    for x, y, r in circles:
        wall_slacks.extend([x - r, 1.0 - x - r, y - r, 1.0 - y - r])

    pair_slacks = []
    worst_pair = [-1, -1]
    min_pair = math.inf
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            slack = math.hypot(xi - xj, yi - yj) - ri - rj
            pair_slacks.append(slack)
            if slack < min_pair:
                min_pair = slack
                worst_pair = [i, j]

    sum_r = sum(row[2] for row in circles)
    min_wall = min(wall_slacks)
    return {
        "status": "PASS" if min_wall >= 0.0 and min_pair >= 0.0 else "FAIL",
        "n": len(circles),
        "sum_radii": sum_r,
        "min_wall_slack": min_wall,
        "min_pair_slack": min_pair,
        "worst_pair": worst_pair,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = verify(load_candidate(args.candidate))
    except Exception as exc:
        result = {"status": "ERROR", "error": str(exc)}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return {"PASS": 0, "FAIL": 1, "ERROR": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
