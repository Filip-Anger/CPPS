# Python for ICPC-style contests — the asymptotic section

Companion to the team cheat sheet. Everything here either changes a complexity
class or prevents a wrong answer. Verbeek's slides assume C++/Java; these are the
places where Python is genuinely different.

---

## 0. Recalibrate "is it fast enough?"

The slides say: estimate worst-case steps, and **if < ~10,000,000 per test case,
start implementing.**

That number is for C++/Java. **CPython does roughly 10^6 - 10^7 simple operations
per second.** So the honest Python budget is about **10^6 - 10^7 operations
TOTAL**, not per second of headroom. Treat the slide's threshold as ~10x
optimistic.

Practical version of slide "Estimating algorithm", adjusted:

| Bound        | C++ target      | Python reality                                  |
|--------------|-----------------|-------------------------------------------------|
| n <= 10^9    | O(1), O(log n), O(sqrt n) | same                                  |
| n <= 10^6    | O(n), O(n log n) | OK **only** if the inner work is builtin-heavy (sort, join, set ops). A hand-written Python loop over 10^6 is already ~1s. |
| n <= 10^5    | O(n log n)      | comfortable                                      |
| n <= 10^3, W <= 10^3 | O(nW) DP | 10^6 cells - borderline, keep the inner loop trivial |
| n <= 10^2    | O(n^3)          | 10^6 - fine                                      |
| n <= 16      | O(2^n), O(n 2^n) | fine                                            |
| n <= 8       | O(n!)           | fine                                             |

**Rule of thumb: if the algorithm is right at the C++ limit, it will TLE in
Python.** You need one complexity class of margin, or the hot loop pushed into a
builtin.

---

## 1. Operations that are secretly O(n) - these create O(n^2)

| You write | Cost | Use instead |
|-----------|------|-------------|
| `lst.pop(0)` / `lst.insert(0, x)` | **O(n)** | `collections.deque` -> `popleft()` / `appendleft()` are O(1) |
| `x in lst` (list) | **O(n)** | `x in s` where `s` is a `set`/`dict` -> O(1) |
| `lst.remove(x)` / `lst.index(x)` | **O(n)** | set/dict, or store indices |
| `s += chunk` in a loop (str) | **O(n^2)** | collect in a list, `''.join(parts)` at the end |
| `a[i:j]` inside a loop | **O(j-i)** copy | indices, or `memoryview` for bytes |
| `d.copy()` / `list(g)` inside recursion | **O(n) per node** | mutate + undo (backtracking), never copy |
| `min(lst)` / `max(lst)` in a loop | **O(n)** each | `heapq`, or track incrementally |

The BFS trap is the common one. The slides say "easy to implement with a queue" -
in Python a `list` used as a queue makes BFS **O(V^2)**:

```python
from collections import deque
q = deque([start]); seen = {start}
while q:
    v = q.popleft()                 # O(1). list.pop(0) would be O(n)
    for w in adj[v]:
        if w not in seen:           # set, not list
            seen.add(w); q.append(w)
```

The backtracking trap is the other one. Copying state at every recursive call
multiplies your running time by O(n). Mutate and undo:

```python
def rec(i):
    for choice in options(i):
        apply(choice)               # mutate shared state
        rec(i + 1)
        undo(choice)                # restore before the next branch
```

---

## 2. Recursion is a hard cliff

Default recursion limit is **1000**. There is no tail-call optimisation. A DFS on
10^5 nodes raises `RecursionError` -> Runtime Error verdict.

```python
import sys, threading
sys.setrecursionlimit(1 << 20)
# CPython also runs out of C stack; run the solve in a big-stack thread:
threading.stack_size(1 << 26)
t = threading.Thread(target=main); t.start(); t.join()
```

Better when you can: **write DFS iteratively with an explicit stack.** The slides
warn about this under memoization ("can be problem with recursion depth! Try to
avoid"). In Python it is not a warning, it is a wall.

---

## 3. Standard library that replaces a cheat-sheet page

| Need | One-liner |
|------|-----------|
| Priority queue (Dijkstra) | `from heapq import heappush, heappop` - O(log n) |
| Binary search on sorted list | `from bisect import bisect_left, bisect_right` |
| Memoization (DP) | `from functools import lru_cache` + `@lru_cache(maxsize=None)` |
| All permutations (n <= 8) | `from itertools import permutations` |
| All subsets (n <= 16) | `from itertools import combinations` or bitmask `for m in range(1 << n)` |
| Cartesian product | `itertools.product(range(k), repeat=n)` |
| Counting | `from collections import Counter, defaultdict` |
| GCD / LCM | `math.gcd`, `math.lcm` |
| **Exact integer sqrt** | `math.isqrt(n)` |
| Combinations count | `math.comb(n, k)`, `math.perm(n, k)` |
| Exact rationals | `from fractions import Fraction` |
| Modular inverse | `pow(a, -1, m)` (Python 3.8+) |
| Fast modular power | `pow(a, b, m)` - built in, O(log b) |

Dijkstra, complete:

```python
import heapq
def dijkstra(adj, s, n):
    INF = float('inf'); dist = [INF] * n; dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]: continue        # stale entry - skip, don't decrease-key
        for w, wt in adj[v]:
            nd = d + wt
            if nd < dist[w]:
                dist[w] = nd; heapq.heappush(pq, (nd, w))
    return dist
```

---

## 4. Where Python beats C++ - and the traps that come with it

**Integers are arbitrary precision.** The slides' entire "Overflow / use
`long long` / `scanf("%lld")`" slide does not apply to you. No overflow, ever.
Free correctness.

Costs and gotchas:

- Big-int arithmetic is **not** O(1). Multiplying d-digit numbers costs
  ~O(d^1.58). Factorials and repeated squaring of huge numbers are not free.
- `//` and `%` round toward **negative infinity**, C++/Java truncate toward zero.
  `-7 // 2 == -4` in Python, `-3` in C++. `-7 % 2 == 1` in Python, `-1` in C++.
  **This is a real WA source when you transcribe a formula off the C++ cheat
  sheet.** For C-style behaviour: `int(a / b)` (small values) or
  `-(-a // b)`.
- **`math.isqrt(n)`, never `int(n ** 0.5)`.** The float version is wrong for
  large n. The slides say "primality test, check until sqrt(n)" - do it with
  `isqrt` or you will fail on a boundary case:

```python
def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):   # deterministic < 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
```

Sieve of Eratosthenes, O(n log log n), with the slice trick that keeps the inner
loop in C:

```python
def sieve(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))   # slice assign, not a loop
    return [i for i in range(n + 1) if s[i]]
```

---

## 5. I/O - constant factor, but include it anyway

Not asymptotic. Included because the constant is real and free to take.

**Measured on this machine, 300,000 input lines and 300,000 output lines:**
buffered read + single joined write **0.27s**, vs `input()` + `print()` per line
**0.81s**. About **3x**. The gap only appears when the input has *many lines* -
on one huge line of 10^6 integers the two are identical, because `input()` is
only called three times. So: worth taking always, decisive when the line count
is large.

```python
import sys
data = sys.stdin.buffer.read().split()      # everything, as bytes tokens
it = iter(data)
def ni(): return int(next(it))
def ns(): return next(it).decode()

out = []
# ... out.append(str(answer)) ...
sys.stdout.write('\n'.join(out) + '\n')     # one write, not print() per line
```

`input()` in a loop and `print()` in a loop are both slow. Read once, write once.

---

## 6. numpy

**Not standard library.** Third-party; availability is a property of the judge
machine, not of Python. **Verify by submitting `import numpy` to the judge before
you rely on it** - training server and contest judge may differ.

Even when present, it is a constant-factor tool, not an asymptotic one. The only
case worth it is a very large sieve or bulk array arithmetic. It also reintroduces
**int64 overflow**, which plain Python ints do not have. Default answer: don't.

---

## 7. Fastest pre-contest checks

- [ ] Submit a solved problem with `import numpy` on top - is it installed?
- [ ] Is PyPy available on the contest judge? (Training server lists only CPython.
      PyPy is ~5-10x faster and changes every estimate in section 0.)
- [ ] Does deep recursion survive? (`Template.py`'s big-stack thread was verified
      to depth 200,000 on Filip's laptop - re-check on the judge.)
- [ ] Confirm the output format: trailing newline, capitalisation, `IMPOSSIBLE`
      vs `Impossible`.
