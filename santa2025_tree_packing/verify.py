#!/usr/bin/env python
"""Strict verifier for the Santa 2025 Christmas Tree Packing submission.

Wraps the OFFICIAL Kaggle metric and adds the id-integrity and format checks
the metric itself does not perform, then writes the verdict to disk.

The official metric is NOT vendored in this repository - it is competition
material. Download METRIC.py from the competition's metric notebook
(https://www.kaggle.com/code/metric/santa-2025-metric) and pass its path;
this script pins it by sha256 and refuses to run on a mismatch.

Requires shapely==2.1.2 (the version the metric is authored against).

Usage
-----
    python verify.py --submission submission.csv \\
                     --metric /path/to/METRIC.py \\
                     [--sample /path/to/sample_submission.csv] \\
                     [--out verdict.json] [--per-puzzle per_puzzle.csv]

Exit code 0 if the submission is valid and scores below the target, 1
otherwise. The verdict of record is the JSON file, not the exit code.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from decimal import Decimal

# the competition's winning score; a submission at or above this is valid but
# not an improvement
TARGET = 68.781235119300
PINNED_METRIC_SHA = "85649556b1c2c2e78d312ede88d1079bd6f59256493a92a6d0d17f691e227ad8"
REQUIRED_SHAPELY = "2.1.2"
N_ROWS = 20100


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def load_metric(path):
    spec = importlib.util.spec_from_file_location("santa_metric", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def expected_ids():
    """The official id set: NNN_i for NNN = 001..200, i = 0..NNN-1."""
    return ["%03d_%d" % (n, i) for n in range(1, 201) for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", default=None,
                    help="default: submission.csv next to this script")
    ap.add_argument("--metric", required=True,
                    help="path to the official METRIC.py")
    ap.add_argument("--sample", default=None,
                    help="optional sample_submission.csv; if omitted the id "
                         "set is generated from the official NNN_i scheme")
    ap.add_argument("--out", default=None,
                    help="default: verdict.json next to this script")
    ap.add_argument("--per-puzzle", default=None)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    sub_path = args.submission or os.path.join(here, "submission.csv")
    out_path = args.out or os.path.join(here, "verdict.json")

    t0 = time.time()
    v = {
        "accepted": False, "valid": False, "score": None,
        "error_type": None, "error_message": None, "failing_group": None,
        "submission_sha256": None, "metric_sha256": None,
        "shapely_version": None, "elapsed_s": None,
        "per_puzzle_path": args.per_puzzle, "target": TARGET,
    }

    def finish(code):
        v["elapsed_s"] = round(time.time() - t0, 3)
        tmp = out_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(v, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, out_path)
        print(json.dumps(v, indent=2))
        sys.exit(code)

    def fail(kind, msg, group=None):
        v["error_type"] = kind
        v["error_message"] = str(msg)[:2000]
        v["failing_group"] = group
        finish(1)

    # --- environment and gate provenance -------------------------------
    try:
        import shapely
        v["shapely_version"] = shapely.__version__
        if shapely.__version__ != REQUIRED_SHAPELY:
            fail("verifier_error",
                 "shapely %s != %s (the metric's pinned version)"
                 % (shapely.__version__, REQUIRED_SHAPELY))
        if not os.path.exists(args.metric):
            fail("verifier_error", "METRIC.py not found at %s" % args.metric)
        v["metric_sha256"] = sha256_file(args.metric)
        if v["metric_sha256"] != PINNED_METRIC_SHA:
            fail("verifier_error",
                 "METRIC.py sha256 mismatch:\n  got      %s\n  expected %s"
                 % (v["metric_sha256"], PINNED_METRIC_SHA))
        v["submission_sha256"] = sha256_file(sub_path)
    except SystemExit:
        raise
    except Exception as e:
        fail("verifier_error", "%s: %s" % (type(e).__name__, e))

    import pandas as pd
    metric = load_metric(args.metric)

    # --- structural checks the metric does not perform -------------------
    try:
        with open(sub_path, "r", encoding="utf-8", newline="") as f:
            header = f.readline().rstrip("\r\n")
        if header != "id,x,y,deg":
            fail("rejected", "bad header: %r" % header)
        sub = pd.read_csv(sub_path, dtype=str, keep_default_na=False)
        if list(sub.columns) != ["id", "x", "y", "deg"]:
            fail("rejected", "bad columns: %s" % list(sub.columns))
        if len(sub) != N_ROWS:
            fail("rejected", "row count %d != %d" % (len(sub), N_ROWS))
        if args.sample:
            want = pd.read_csv(args.sample, dtype=str,
                               keep_default_na=False)["id"].tolist()
        else:
            want = expected_ids()
        if set(sub["id"]) != set(want):
            miss = sorted(set(want) - set(sub["id"]))
            extra = sorted(set(sub["id"]) - set(want))
            fail("rejected", "id set mismatch: %d missing e.g. %s, "
                             "%d extra e.g. %s"
                 % (len(miss), miss[:3], len(extra), extra[:3]))
        if sub["id"].duplicated().any():
            fail("rejected", "duplicate ids")
        for c in ("x", "y", "deg"):
            col = sub[c]
            if not col.str.startswith("s").all():
                bad = col[~col.str.startswith("s")].index[:3].tolist()
                fail("rejected", "column %s: missing 's' prefix at rows %s"
                     % (c, bad))
            vals = col.str[1:].astype(float)
            if not vals.map(math.isfinite).all():
                fail("rejected", "column %s: non-finite value" % c)
            if c in ("x", "y") and ((vals < -100).any() or (vals > 100).any()):
                fail("rejected", "column %s: outside [-100, 100]" % c)
    except SystemExit:
        raise
    except Exception as e:
        fail("crash", "structural check %s: %s" % (type(e).__name__, e))

    # --- the official gate ----------------------------------------------
    try:
        S = metric.score(solution=sub[["id"]].copy(), submission=sub.copy(),
                         row_id_column_name="id")
    except metric.ParticipantVisibleError as e:
        msg = str(e)
        grp = msg.rsplit(" ", 1)[-1].strip() if "group" in msg else None
        fail("rejected", "ParticipantVisibleError: %s" % msg, grp)
    except SystemExit:
        raise
    except Exception as e:
        fail("crash", "metric raised %s: %s" % (type(e).__name__, e))

    v["valid"] = True
    v["score"] = float(S)
    v["accepted"] = bool(float(S) < TARGET)
    v["slack"] = float(S) - TARGET

    # --- per-puzzle breakdown, using the metric's OWN geometry -----------
    if args.per_puzzle:
        try:
            from shapely.ops import unary_union
            sc = metric.scale_factor
            s2 = sub.copy()
            for c in ("x", "y", "deg"):
                s2[c] = s2[c].str[1:]
            s2["g"] = s2["id"].str.split("_").str[0]
            rows, total = [], Decimal("0.0")
            for g, dfg in s2.groupby("g"):
                polys = [metric.ChristmasTree(r["x"], r["y"], r["deg"]).polygon
                         for _, r in dfg.iterrows()]
                b = unary_union(polys).bounds
                side = max(b[2] - b[0], b[3] - b[1])
                gs = (Decimal(side) ** 2) / (sc ** 2) / Decimal(len(dfg))
                total += gs
                rows.append((int(g), float(Decimal(side) / sc), float(gs)))
            v["per_puzzle_sum"] = float(total)
            v["per_puzzle_matches_score"] = bool(float(total) == v["score"])
            with open(args.per_puzzle, "w", encoding="utf-8", newline="") as f:
                f.write("n,side,group_score,strategy\n")
                for n, side, gs in sorted(rows):
                    f.write("%d,%.17g,%.17g,verified\n" % (n, side, gs))
        except Exception as e:
            v["per_puzzle_error"] = "%s: %s" % (type(e).__name__, e)

    finish(0 if v["accepted"] else 1)


if __name__ == "__main__":
    main()
