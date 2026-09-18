#!/usr/bin/env python3
#
# Testing tool for the Entropy Evasion problem
#
# Usage:
#
#   python3 testing_tool.py -f inputfile <program invocation>
#
#
# Use the -f parameter to specify the input file, e.g. 1.in.
# Format of the input file:
# - One line with an integer n, the number of bits.
# e.g.:
# 4
#
#
# You can compile and run your solution as follows:

# C++:
#   g++ solution.cpp
#   python3 testing_tool.py -f 1.in ./a.out

# Python:
#   python3 testing_tool.py -f 1.in python3 ./Entropy-evasion.py

# Java:
#   javac solution.java
#   python3 testing_tool.py -f 1.in java solution

# Kotlin:
#   kotlinc solution.kt
#   python3 testing_tool.py -f 1.in kotlin solutionKt


# The tool is provided as-is, and you should feel free to make
# whatever alterations or augmentations you like to it.
#
# The tool attempts to detect and report common errors, but it is not an exhaustive test.
# It is not guaranteed that a program that passes this testing tool will be accepted.


import argparse
import subprocess
import traceback
import random

max_commands = 125
min_percentage = 70

parser = argparse.ArgumentParser(description="Testing tool for problem Entropy Evasion.")
parser.add_argument(
    "-f",
    dest="inputfile",
    metavar="inputfile",
    default=None,
    type=argparse.FileType("r"),
    required=True,
    help="The input file to use.",
)
parser.add_argument("program", nargs="+", help="Invocation of your solution")

args = parser.parse_args()

with (
    args.inputfile as f,
    subprocess.Popen(
        " ".join(args.program),
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        universal_newlines=True,
    ) as p,
):
    assert p.stdin is not None and p.stdout is not None
    p_in = p.stdin
    p_out = p.stdout

    def write(line: str):
        assert p.poll() is None, "Program terminated early"
        print(f"Write: {line}", flush=True)
        p_in.write(f"{line}\n")
        p_in.flush()

    def read() -> str:
        assert p.poll() is None, "Program terminated early"
        line = p_out.readline().strip()
        assert line != "", "Read empty line or closed output pipe"
        print(f"Read: {line}", flush=True)
        return line

    # Parse input
    lines = f.readlines()
    assert len(lines) == 1

    n = int(lines[0])

    arr = [0] * n

    # Simulate interaction
    try:
        write(str(n))

        commands = 0
        while True:
            l, r = map(int, read().split())
            commands += 1
            assert 1 <= l <= r <= n, f"Your command ({l} {r}) is out-of-bounds (l and r must be between 1 and {n})."
            for i in range(l - 1, r):  # Note: converting 1-based indices to 0-based indices
                arr[i] = random.randint(0, 1)
            perc = (100 * sum(arr)) // n
            write(" ".join(map(str, arr)))
            write(str(perc))
            if perc >= min_percentage:
                break

        print()
        print("Reached at least 70 percent, stopping interaction.")
        print(f"Commands used: {commands}", flush=True)
        assert (extra := p_out.readline()) == "", (
            f"Your submission printed extra commands after hitting the percentage goal: '{extra[:100].strip()}{'...' if len(extra) > 100 else ''}'"
        )
        print(f"Exit code: {p.wait()}", flush=True)
        assert p.wait() == 0, "Your submission did not exit cleanly after finishing"

    except AssertionError as e:
        print()
        print(f"Error: {e}")
        print()
        print("Killing your submission.", flush=True)
        p.kill()
        exit(1)

    except Exception:
        print()
        print("Unexpected error:")
        traceback.print_exc()
        print()
        print("Killing your submission.", flush=True)
        p.kill()
        exit(1)
