# Cheat sheet additions — Team cO(n)stant

Gap analysis of the current 9-slide sheet against the three course decks, plus
the material to close it. **Every C++ snippet here compiles clean under
`g++ -std=c++17 -Wall -Wextra` and passes a correctness test** (32 assertions,
all green). Nothing below is written from memory.

Suggested order to add: A, B, C are the ones that would actually cost you a
problem tomorrow.

---

## What the sheet is missing, and why it matters

The decks name their own "standard algorithms". Checking the sheet against those
lists:

| Deck says you need | On the sheet? |
|---|---|
| ProgContests s18: DFS, BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, MST, Euler tour, bipartite matching, max-flow | **None of them** |
| EffectiveProgramming s19: Union-Find — the table literally says `? (cheatsheet)` | **Missing.** The course is telling you to put it there |
| ProgContests s11: knapsack, edit distance, LCS, coin change, LIS, matrix chain | Only edit distance |
| OptimizationProb s26: "Always try if a binary search on the cost makes the problem easier" | Missing |
| ProgContests s7: "Use Sieve of Eratosthenes!" | Missing |
| ProgContests s8: "You need to know Gaussian elimination" | Missing |
| ProgContests s28: 2D convex hull (Graham scan) — in the "you can try these" list | Missing, though the rest of geometry is strong |
| ProgContests s29: Euler's formula V − E + F = C + 1 | Missing |
| ProgContests s15: hashing **or a trie**; FSM / Boyer-Moore / **KMP** | Z-function yes; trie and KMP no |
| Both decks: the complexity-from-bounds table | Missing |
| Both decks: the common-mistakes checklist | Missing |

**The graph section is the hole that will cost you.** Shortest paths are called
"a common problem during contests" in the deck, and the sheet has k-th ancestor
and LCA but no Dijkstra, no BFS, no MST and no flow.

Also: **slide 8 is blank.** It says "Hamilton" and nothing else. Fill it or cut it.

---

## SLIDE A — Decision aid (put this first, before any code)

The most useful half-page on the sheet is not an algorithm.

**Read the bound, derive the complexity, then pick the algorithm:**

| Bound | Target | Likely technique |
|---|---|---|
| n ≤ 10^9 | O(1), O(log n), O(√n) | closed form, binary search |
| n ≤ 10^6 | O(n), O(n log n) | greedy, sorting, two pointers, D&C |
| n ≤ 10^3, W ≤ 10^3 | O(nW) | DP over an n×W table |
| n ≤ 10^2 | O(n^3) | Floyd-Warshall, Gaussian elimination, interval DP |
| n ≤ 16 | O(2^n), O(n·2^n) | bitmask brute force / bitmask DP |
| n ≤ 8 | O(n!) | permutations |

**Budget ≈ 10^7 steps per test case.** If the estimate exceeds it, do not start
implementing.

**Binary search on the answer** — the deck's most reusable trick. If the problem
asks for an optimum, ask instead: *can I achieve k?* If `check(k)` is monotone,
binary search it.

```cpp
ll lo = 0, hi = HI;                 // hi must be achievable
while (lo < hi) {
    ll mid = lo + (hi - lo) / 2;    // NOT (lo+hi)/2 - overflow
    if (check(mid)) hi = mid; else lo = mid + 1;
}
// lo == smallest feasible value
```

For floating point, loop a fixed 100 iterations instead of comparing.

---

## SLIDE B — Union-Find (DSU)

The course's own table leaves this as an exercise for your cheat sheet.
Near-O(1) per operation. Kruskal, connectivity, cycle detection, grouping.

```cpp
struct DSU {
    vector<int> p, sz;
    DSU(int n): p(n), sz(n,1) { iota(p.begin(), p.end(), 0); }
    int find(int x){ while(p[x]!=x){ p[x]=p[p[x]]; x=p[x]; } return x; }
    bool unite(int a,int b){
        a=find(a); b=find(b);
        if(a==b) return false;
        if(sz[a]<sz[b]) swap(a,b);
        p[b]=a; sz[a]+=sz[b]; return true;
    }
};
```

---

## SLIDE C — Graph traversal and shortest paths

Pick using the deck's own flowchart: unweighted → **BFS**; weighted
non-negative → **Dijkstra**; negative edges → **Bellman-Ford**; all pairs →
**Floyd-Warshall**.

```cpp
vector<int> bfs(vector<vector<int>>& adj, int s){
    vector<int> dist(adj.size(), -1);
    queue<int> q; dist[s]=0; q.push(s);
    while(!q.empty()){
        int v=q.front(); q.pop();
        for(int w: adj[v]) if(dist[w]==-1){ dist[w]=dist[v]+1; q.push(w); }
    }
    return dist;
}
```

```cpp
vector<int> dfs_iter(vector<vector<int>>& adj, int s){
    vector<int> seen(adj.size(),0), order;
    vector<int> st{s};
    while(!st.empty()){
        int v=st.back(); st.pop_back();
        if(seen[v]) continue;
        seen[v]=1; order.push_back(v);
        for(int w: adj[v]) if(!seen[w]) st.push_back(w);
    }
    return order;
}
```

```cpp
vector<ll> dijkstra(vector<vector<pair<int,int>>>& adj, int s){
    const ll INF = LLONG_MAX/4;
    vector<ll> d(adj.size(), INF); d[s]=0;
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    pq.push({0,s});
    while(!pq.empty()){
        auto [dv,v]=pq.top(); pq.pop();
        if(dv>d[v]) continue;                    // stale entry
        for(auto [w,wt]: adj[v])
            if(dv+wt<d[w]){ d[w]=dv+wt; pq.push({d[w],w}); }
    }
    return d;
}
```

```cpp
bool bellman_ford(int n, vector<array<ll,3>>& edges, int s, vector<ll>& d){
    const ll INF = LLONG_MAX/4;
    d.assign(n, INF); d[s]=0;
    for(int i=0;i<n-1;i++)
        for(auto& e: edges)
            if(d[e[0]]<INF && d[e[0]]+e[2]<d[e[1]]) d[e[1]]=d[e[0]]+e[2];
    for(auto& e: edges)                           // one more pass => neg cycle
        if(d[e[0]]<INF && d[e[0]]+e[2]<d[e[1]]) return false;
    return true;
}
```

```cpp
void floyd(vector<vector<ll>>& d){
    int n=d.size();
    for(int k=0;k<n;k++) for(int i=0;i<n;i++) for(int j=0;j<n;j++)
        if(d[i][k]+d[k][j] < d[i][j]) d[i][j]=d[i][k]+d[k][j];
}
```

```cpp
vector<int> toposort(vector<vector<int>>& adj){
    int n=adj.size(); vector<int> indeg(n,0), order;
    for(int v=0;v<n;v++) for(int w: adj[v]) indeg[w]++;
    queue<int> q;
    for(int v=0;v<n;v++) if(!indeg[v]) q.push(v);
    while(!q.empty()){
        int v=q.front(); q.pop(); order.push_back(v);
        for(int w: adj[v]) if(--indeg[w]==0) q.push(w);
    }
    return order;                                 // size<n  =>  graph has a cycle
}
```

**Grid BFS:** pad the grid with a wall ring so you never bounds-check.
`int dx[]={1,-1,0,0}, dy[]={0,0,1,-1};`

---

## SLIDE D — MST, SCC, matching, flow

```cpp
ll kruskal(int n, vector<array<ll,3>> edges){
    sort(edges.begin(), edges.end());             // weight first
    DSU d(n); ll total=0;
    for(auto& e: edges) if(d.unite(e[1],e[2])) total+=e[0];
    return total;
}
```

```cpp
vector<int> scc(vector<vector<int>>& adj){
    int n=adj.size();
    vector<vector<int>> rev(n);
    for(int v=0;v<n;v++) for(int w: adj[v]) rev[w].push_back(v);
    vector<int> seen(n,0), order;
    for(int s=0;s<n;s++){
        if(seen[s]) continue;
        vector<pair<int,int>> st{{s,0}};
        while(!st.empty()){
            auto& [v,i]=st.back();
            if(!i) { if(seen[v]){ st.pop_back(); continue; } seen[v]=1; }
            if(i < (int)adj[v].size()){ int w=adj[v][i++]; if(!seen[w]) st.push_back({w,0}); }
            else { order.push_back(v); st.pop_back(); }
        }
    }
    vector<int> comp(n,-1); int c=0;
    for(int i=n-1;i>=0;i--){
        int s=order[i];
        if(comp[s]!=-1) continue;
        vector<int> st{s}; comp[s]=c;
        while(!st.empty()){
            int v=st.back(); st.pop_back();
            for(int w: rev[v]) if(comp[w]==-1){ comp[w]=c; st.push_back(w); }
        }
        c++;
    }
    return comp;
}
```

```cpp
bool try_kuhn(int v, vector<vector<int>>& adj, vector<int>& used, vector<int>& mt){
    for(int to: adj[v]){
        if(used[to]) continue;
        used[to]=1;
        if(mt[to]==-1 || try_kuhn(mt[to],adj,used,mt)){ mt[to]=v; return true; }
    }
    return false;
}
int matching(vector<vector<int>>& adj, int nRight){
    vector<int> mt(nRight,-1); int res=0;
    for(int v=0;v<(int)adj.size();v++){
        vector<int> used(nRight,0);
        if(try_kuhn(v,adj,used,mt)) res++;
    }
    return res;
}
```

```cpp
struct Dinic {
    struct E{ int to; ll cap; };
    vector<E> es; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n): g(n), lvl(n), it(n) {}
    void add(int a,int b,ll c){ g[a].push_back(es.size()); es.push_back({b,c});
                               g[b].push_back(es.size()); es.push_back({a,0}); }
    bool bfs(int s,int t){
        fill(lvl.begin(),lvl.end(),-1); queue<int> q; lvl[s]=0; q.push(s);
        while(!q.empty()){ int v=q.front(); q.pop();
            for(int id: g[v]) if(es[id].cap>0 && lvl[es[id].to]<0){
                lvl[es[id].to]=lvl[v]+1; q.push(es[id].to); } }
        return lvl[t]>=0;
    }
    ll dfs(int v,int t,ll f){
        if(v==t) return f;
        for(int& i=it[v]; i<(int)g[v].size(); i++){
            int id=g[v][i], to=es[id].to;
            if(es[id].cap>0 && lvl[to]==lvl[v]+1){
                ll d=dfs(to,t,min(f,es[id].cap));
                if(d>0){ es[id].cap-=d; es[id^1].cap+=d; return d; }
            }
        }
        return 0;
    }
    ll maxflow(int s,int t){
        ll fl=0;
        while(bfs(s,t)){ fill(it.begin(),it.end(),0);
            while(ll f=dfs(s,t,LLONG_MAX/4)) fl+=f; }
        return fl;
    }
};
```

**Max-flow = min-cut.** After `maxflow`, the vertices reachable from `s` in the
residual graph (edges with `cap > 0`) form the source side of the min cut.
Bipartite matching via flow: source → left (cap 1), left → right (cap 1),
right → sink (cap 1).

---

## SLIDE E — Standard DP

```cpp
ll knapsack(vector<int>& wt, vector<ll>& val, int W){
    vector<ll> dp(W+1,0);
    for(size_t i=0;i<wt.size();i++)
        for(int w=W; w>=wt[i]; w--)               // DESCENDING: each item once
            dp[w]=max(dp[w], dp[w-wt[i]]+val[i]);
    return dp[W];
}
```

```cpp
int lis(vector<int>& a){
    vector<int> t;
    for(int x: a){
        auto it=lower_bound(t.begin(),t.end(),x);  // upper_bound => non-decreasing
        if(it==t.end()) t.push_back(x); else *it=x;
    }
    return t.size();
}
```

```cpp
ll coin_change(vector<int>& c, int S){
    const ll INF=LLONG_MAX/4;
    vector<ll> dp(S+1,INF); dp[0]=0;
    for(int s=1;s<=S;s++) for(int x: c)
        if(x<=s && dp[s-x]+1<dp[s]) dp[s]=dp[s-x]+1;
    return dp[S];
}
```

```cpp
int lcs(string& a, string& b){
    vector<vector<int>> dp(a.size()+1, vector<int>(b.size()+1,0));
    for(size_t i=1;i<=a.size();i++) for(size_t j=1;j<=b.size();j++)
        dp[i][j] = (a[i-1]==b[j-1]) ? dp[i-1][j-1]+1 : max(dp[i-1][j],dp[i][j-1]);
    return dp[a.size()][b.size()];
}
```

**The knapsack loop runs descending on purpose.** Ascending turns 0/1 knapsack
into unbounded knapsack — each item reusable. That is the single most common DP
bug, and it is silent.

---

## SLIDE F — Number theory

```cpp
vector<int> sieve(int n){
    vector<char> is(n+1,1); is[0]=is[1]=0;
    for(int i=2;(ll)i*i<=n;i++) if(is[i]) for(int j=i*i;j<=n;j+=i) is[j]=0;
    vector<int> pr;
    for(int i=2;i<=n;i++) if(is[i]) pr.push_back(i);
    return pr;
}
```

```cpp
int gauss(vector<vector<double>> a, vector<double>& ans){
    int n=a.size(), m=a[0].size()-1;
    vector<int> where(m,-1);
    for(int col=0,row=0; col<m && row<n; col++){
        int sel=row;
        for(int i=row;i<n;i++) if(fabs(a[i][col])>fabs(a[sel][col])) sel=i;
        if(fabs(a[sel][col])<1e-9) continue;
        swap(a[sel],a[row]);
        where[col]=row;
        for(int i=0;i<n;i++) if(i!=row){
            double c=a[i][col]/a[row][col];
            for(int j=col;j<=m;j++) a[i][j]-=a[row][j]*c;
        }
        row++;
    }
    ans.assign(m,0);
    for(int i=0;i<m;i++) if(where[i]!=-1) ans[i]=a[where[i]][m]/a[where[i]][i];
    for(int i=0;i<n;i++){
        double sum=0;
        for(int j=0;j<m;j++) sum+=ans[j]*a[i][j];
        if(fabs(sum-a[i][m])>1e-6) return 0;      // no solution
    }
    for(int i=0;i<m;i++) if(where[i]==-1) return 2;  // infinitely many
    return 1;
}
```

The sheet already has extended Euclid, CRT, totient, Fermat. The sieve and
Gaussian elimination were the two the decks name that were absent.

---

## SLIDE G — Convex hull + Euler's formula

```cpp
typedef pair<ll,ll> Pt;
ll cross(Pt O, Pt A, Pt B){
    return (A.first-O.first)*(B.second-O.second) - (A.second-O.second)*(B.first-O.first);
}
vector<Pt> hull(vector<Pt> p){
    sort(p.begin(),p.end()); p.erase(unique(p.begin(),p.end()),p.end());
    int n=p.size(), k=0;
    if(n<3) return p;
    vector<Pt> h(2*n);
    for(int i=0;i<n;i++){                         // lower
        while(k>=2 && cross(h[k-2],h[k-1],p[i])<=0) k--;
        h[k++]=p[i];
    }
    for(int i=n-2,t=k+1;i>=0;i--){                // upper
        while(k>=t && cross(h[k-2],h[k-1],p[i])<=0) k--;
        h[k++]=p[i];
    }
    h.resize(k-1);
    return h;
}
```

Returns the hull counter-clockwise. `<= 0` drops collinear points; use `< 0` to
keep them. All integer arithmetic — no floating point, so no precision bugs.

**Euler's formula: V − E + F = C + 1**, where C = number of connected
components. Use it whenever you need the number of faces of a planar subdivision.

---

## SLIDE H — String matching

The sheet has hashing and the Z-function. These two are what the deck names that
are absent.

```cpp
vector<int> prefix_function(string& s){
    int n=s.size(); vector<int> pi(n,0);
    for(int i=1;i<n;i++){
        int j=pi[i-1];
        while(j>0 && s[i]!=s[j]) j=pi[j-1];
        if(s[i]==s[j]) j++;
        pi[i]=j;
    }
    return pi;
}
// occurrences of pat in txt: run prefix_function on  pat + '\1' + txt
vector<int> kmp_find(string pat, string txt){
    string s = pat + '\1' + txt;
    vector<int> pi = prefix_function(s), res;
    for(size_t i=pat.size()+1;i<s.size();i++)
        if(pi[i]==(int)pat.size()) res.push_back(i - 2*pat.size());
    return res;
}
```

```cpp
struct Trie {
    vector<array<int,26>> ch; vector<int> cnt;
    Trie(){ newNode(); }
    int newNode(){ ch.push_back({}); ch.back().fill(-1); cnt.push_back(0); return ch.size()-1; }
    void insert(const string& s){
        int v=0;
        for(char c: s){ int x=c-'a';
            if(ch[v][x]==-1) ch[v][x]=newNode();
            v=ch[v][x]; }
        cnt[v]++;
    }
    bool contains(const string& s){
        int v=0;
        for(char c: s){ int x=c-'a'; if(ch[v][x]==-1) return false; v=ch[v][x]; }
        return cnt[v]>0;
    }
};
```

---

## SLIDE I — Python (only if someone submits in Python)

Python is allowed but not recommended. If it is used, these are the things that
differ from the C++ on the rest of this sheet.

**Recalibrate the budget.** The 10^7 figure on slide A is C++. CPython does
~10^6–10^7 simple ops **per second**, so you need about one complexity class of
margin, or the hot loop has to be a builtin (`sort`, `join`, set operations).

**Secretly O(n) — these create O(n²):**

| You write | Cost | Use instead |
|---|---|---|
| `lst.pop(0)` / `lst.insert(0,x)` | O(n) | `collections.deque` |
| `x in lst` | O(n) | `x in set` |
| `s += chunk` in a loop | O(n²) | `''.join(parts)` |
| `a[i:j]` in a loop | O(j−i) copy | indices |
| copying state inside recursion | O(n) per node | mutate + undo |

**Recursion limit is 1000 and there is no TCO.** DFS on 10^5 nodes is a Runtime
Error. The template below survives depth 200,000 (verified).

**Free win:** Python ints are arbitrary precision — the overflow slide does not
apply. **Trap:** `//` and `%` round toward −∞ where C++ truncates.
`-7 // 2 == -4` in Python, `-3` in C++. Transcribing a C++ formula off this
sheet is exactly when that bites.

**Use `math.isqrt(n)`, never `int(n**0.5)`** — the float version is wrong at
large n, and the "check until √n" primality test walks straight into it.

**stdlib that replaces a cheat sheet page:** `heapq` (Dijkstra), `bisect`
(binary search), `functools.lru_cache` (memoisation), `itertools.permutations /
combinations / product`, `collections.Counter / defaultdict / deque`,
`math.gcd / lcm / isqrt / comb`, `pow(a,-1,m)` (modular inverse),
`pow(a,b,m)` (fast modular power).

**Template** — full version in `~/School/CPPS/Template.py`:

```python
import sys, math
from collections import deque, defaultdict, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations, product
from functools import lru_cache

_data = sys.stdin.buffer.read()
_it = iter(_data.split())
def ni():     return int(next(_it))
def ns():     return next(_it).decode()
def nints(k): return [int(next(_it)) for _ in range(k)]

_out = []
def emit(*a): _out.append(' '.join(map(str, a)))

DEBUG = False
def dbg(*a):
    if DEBUG: print(*a, file=sys.stderr, flush=True)   # stderr: judge ignores it

def solve():
    # ALL state local -> cannot leak between test cases
    n = ni()
    a = nints(n)
    emit(sum(a))

def main():
    for _ in range(ni()):      # delete the loop if single test case
        solve()

def _run():
    sys.setrecursionlimit(1 << 20)
    main()
    if _out: sys.stdout.write('\n'.join(_out) + '\n')

if __name__ == '__main__':
    import threading
    try:
        threading.stack_size(1 << 27)
        t = threading.Thread(target=_run); t.start(); t.join()
    except (ValueError, RuntimeError):
        _run()
```

Measured: buffered read + single write is ~3x faster than `input()`/`print()`
per line over 300k lines. No gain when the input is one huge line.

---

## SLIDE J — Before you submit

Straight off the decks' common-mistakes slides. Cheapest page on the sheet.

- [ ] **Loop bounds** — especially in DP.
- [ ] **Array bounds** — big enough? `n+1`?
- [ ] **Re-initialise everything between test cases.** Clear vectors, reset
      globals. Only shows up on multi-case input.
- [ ] **Output format** — spelling, capitals, newlines. `IMPOSSIBLE` vs
      `Impossible`.
- [ ] **Overflow** — `long long`. Does an intermediate product exceed 2^31?
- [ ] **Index offset** — `A[i]` or `A[i-1]`?
- [ ] **Read the complete input**, even once the answer is known.
- [ ] **Precision** — use `double`; `setprecision`; for many multiplications use
      logs. Avoid `sqrt(-1)`, `log(0)`.
- [ ] **Rounding** — exactly as the statement prescribes.
- [ ] **Boundary cases** — n=1, empty, all-equal, maximum values.
- [ ] Wrong answer? Check input parsing first, then print intermediates to
      **stderr**.

**Verdict triage:** Runtime error → usually an out-of-bounds index. Time-limit
exceeded → algorithm too slow (you mis-estimated) or an infinite loop. Wrong
answer → the list above.

---

## Tactics worth one line on the title slide

One person writes the bugfree template first · skim **all** problems immediately
· check the scoreboard to find the easy ones · solve easy → hard · think the
problem through completely before touching the keyboard · whoever is not coding
writes hard test cases · pencode when the machine is busy · don't start with
long simulation problems.
