import sys
import math
from collections import deque, defaultdict, Counter
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right, insort
from itertools import permutations, combinations, product, accumulate
from functools import lru_cache

# ---------------------------------------------------------------- INPUT
# All of stdin, read once, split in C. Never call input() below.
_data = sys.stdin.buffer.read()
_it = iter(_data.split())

def ni():        return int(next(_it))                  # one int
def nf():        return float(next(_it))                # one float
def ns():        return next(_it).decode()       # one token
def nints(k):    return [int(next(_it)) for _ in range(k)]
def nall():      return list(map(int, _it))      # all remaining ints

# LINE MODE - only when the input has strings containing spaces.
# If you uncomment it, do NOT use ni()/ns()/nints() anywhere: the
# two readers walk the same buffer, and mixing them loses input.
# _lines = iter(_data.splitlines())
# def rline():   return next(_lines).decode()

# --------------------------------------------------------------- OUTPUT
# Buffered: one syscall at the end instead of one per line.
_out = []
def emit(*args): _out.append(' '.join(map(str, args)))

# ---------------------------------------------------------------- DEBUG
# stderr is ignored by the judge: safe to leave in on submit.
DEBUG = False
def dbg(*args):
    if DEBUG: print(*args, file=sys.stderr, flush=True)

# ---------------------------------------------------------------- SOLVE
def solve():
    # All state lives HERE, as locals. The most common WA is stale
    # data carried between test cases; locals make that impossible.

    n = ni()
    a = nints(n)

    emit(sum(a))


def main():
    # Single test case? Delete the next two lines and just call solve().
    t = ni()
    for _ in range(t):
        solve()


# ----------------------------------------------------------------- BOOT
def _run():
    sys.setrecursionlimit(1 << 20)   # default 1000: deep DFS = RTE
    main()
    if _out:
        sys.stdout.write('\n'.join(_out))
        sys.stdout.write('\n')

if __name__ == '__main__':
    # Python's C stack, not the recursion counter, is the real limit.
    # A thread with a big stack is what makes deep recursion survive.
    import threading
    try:
        threading.stack_size(1 << 27)       # 128 MB
        _t = threading.Thread(target=_run)
        _t.start()
        _t.join()
    except (ValueError, RuntimeError):   # platform refused it
        _run()