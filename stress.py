#!/usr/bin/env python3
"""
Stress harness for Entropy Evasion.

Runs testing_tool.py against your solution many times, across a spread of n,
and reports the numbers that decide AC vs WA:

  - the WORST command count ever seen  (must stay under 125)
  - any run that errored               (out-of-bounds, bad format, crash)
  - any run that hung                  (didn't terminate)

The interactor reseeds itself every run, so repetitions are genuinely
different random arrays. One good run proves nothing; this proves the
worst case.

Usage:
    python3 stress.py Entropy-evasion.py
    python3 stress.py Entropy-evasion.py -r 200
    python3 stress.py Entropy-evasion.py -n 1,2,3,1000 -r 500
"""

import argparse
import concurrent.futures
import os
import re
import subprocess
import sys
import tempfile
import time

LIMIT = 125          # command cap from the statement
TARGET = 70          # required percentage of ones
TLIMIT = 1.0         # time limit from the statement, in seconds

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "testing_tool.py")

OK, ERROR, TIMEOUT = "ok", "error", "timeout"


def one_run(solution, n, timeout):
    """Run the interactor once. Returns (status, commands_used, secs, detail).

    secs is wall time for the whole interaction, which includes the
    interactor itself -- so it slightly OVERSTATES your solution's time.
    Good: it errs on the safe side.
    """
    fd, path = tempfile.mkstemp(suffix=".in")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(f"{n}\n")
        t0 = time.monotonic()
        try:
            p = subprocess.run(
                [sys.executable, TOOL, "-f", path, sys.executable, solution],
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return TIMEOUT, None, timeout, f"no result within {timeout}s"
        secs = time.monotonic() - t0

        out = p.stdout + p.stderr

        m = re.search(r"Commands used:\s*(\d+)", out)
        if m and "Reached at least" in out:
            return OK, int(m.group(1)), secs, ""

        m = re.search(r"Error:\s*(.+)", out)
        if m:
            return ERROR, None, secs, m.group(1).strip()

        m = re.search(r"(\w*Error:.*)", out)
        return ERROR, None, secs, m.group(1).strip() if m else "no verdict line"
    finally:
        os.unlink(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solution", help="your solution .py")
    ap.add_argument("-n", default="1,2,3,4,5,7,10,25,50,100,250,500,1000",
                    help="comma-separated n values to test")
    ap.add_argument("-r", "--reps", type=int, default=50,
                    help="runs per n (default 50)")
    ap.add_argument("-t", "--timeout", type=float, default=15.0,
                    help="seconds before a run counts as hung")
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count(),
                    help="parallel runs")
    args = ap.parse_args()

    ns = [int(x) for x in args.n.split(",") if x.strip()]
    jobs = [(n, i) for n in ns for i in range(args.reps)]

    print(f"{args.solution}: {len(ns)} sizes x {args.reps} reps "
          f"= {len(jobs)} runs, cap {LIMIT}\n")

    results = {n: [] for n in ns}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(one_run, args.solution, n, args.timeout): n
                for n, _ in jobs}
        done = 0
        for fut in concurrent.futures.as_completed(futs):
            results[futs[fut]].append(fut.result())
            done += 1
            print(f"\r  {done}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print("\r" + " " * 24 + "\r", end="", file=sys.stderr)

    print(f"{'n':>6}  {'worst':>6}  {'mean':>6}  {'slowest':>8}  "
          f"{'fails':>6}  {'hangs':>6}")
    print("-" * 52)

    worst_overall = 0
    slowest_overall = 0.0
    bad = []
    for n in ns:
        runs = results[n]
        oks = [c for s, c, _, _ in runs if s == OK]
        secs = [t for s, _, t, _ in runs if s == OK]
        fails = [d for s, _, _, d in runs if s == ERROR]
        hangs = [1 for s, _, _, _ in runs if s == TIMEOUT]

        worst = max(oks) if oks else 0
        mean = sum(oks) / len(oks) if oks else 0
        slowest = max(secs) if secs else 0.0
        worst_overall = max(worst_overall, worst)
        slowest_overall = max(slowest_overall, slowest)

        flag = ""
        if fails or hangs:
            flag = "  <-- BROKEN"
            bad.append((n, fails, len(hangs)))
        elif worst > LIMIT:
            flag = "  <-- OVER CAP"
            bad.append((n, [f"{worst} commands > {LIMIT}"], 0))
        elif slowest > TLIMIT:
            flag = "  <-- TOO SLOW"
            bad.append((n, [f"{slowest:.2f}s > {TLIMIT}s time limit"], 0))

        print(f"{n:>6}  {worst:>6}  {mean:>6.1f}  {slowest:>7.2f}s  "
              f"{len(fails):>6}  {len(hangs):>6}{flag}")

    if args.jobs > 1:
        print(f"\nNOTE: {args.jobs} runs in parallel, so the times above are "
              f"inflated by CPU contention.\n      Re-run with -j 1 for a "
              f"trustworthy timing read.")

    if bad:
        print("\nFailures:")
        for n, fails, hangs in bad:
            if hangs:
                print(f"  n={n}: {hangs} hung")
            for msg in sorted(set(fails))[:3]:
                print(f"  n={n}: {msg}")
        print("\nVERDICT: NOT SAFE TO SUBMIT")
        return 1

    margin = LIMIT - worst_overall
    print(f"\nAll runs finished. Worst case {worst_overall}/{LIMIT} "
          f"({margin} spare).")
    print("VERDICT: looks safe" if margin >= 10
          else "VERDICT: passes, but the margin is thin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
