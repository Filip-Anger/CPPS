#include "cheatsheet-code.cpp"
#define CHECK(name, got, want) do { auto g=(got); auto w=(want); \
  printf("%-22s %s  got=%lld want=%lld\n", name, (g==w?"PASS":"**FAIL**"), (ll)g, (ll)w); \
  if(g!=w) bad++; } while(0)
int main(){
    int bad=0;

    // DSU: 5 nodes, unite 0-1, 1-2, 3-4  => 2 components
    { DSU d(5); d.unite(0,1); d.unite(1,2); d.unite(3,4);
      set<int> roots; for(int i=0;i<5;i++) roots.insert(d.find(i));
      CHECK("DSU components", (ll)roots.size(), 2LL);
      CHECK("DSU already-united", (ll)d.unite(0,2), 0LL); }

    // BFS on a path 0-1-2-3
    { vector<vector<int>> adj={{1},{0,2},{1,3},{2}};
      CHECK("BFS dist 0->3", (ll)bfs(adj,0)[3], 3LL); }

    // iterative DFS visits all
    { vector<vector<int>> adj={{1,2},{0,3},{0},{1}};
      CHECK("DFS visits all", (ll)dfs_iter(adj,0).size(), 4LL); }

    // Dijkstra: 0->1 (4), 0->2 (1), 2->1 (2)  => d[1]=3
    { vector<vector<pair<int,int>>> adj(3);
      adj[0]={{1,4},{2,1}}; adj[2]={{1,2}};
      CHECK("Dijkstra d[1]", dijkstra(adj,0)[1], 3LL); }

    // Bellman-Ford negative cycle detection
    { vector<array<ll,3>> e={{0,1,1},{1,2,-1},{2,0,-1}}; vector<ll> d;
      CHECK("BF neg cycle", (ll)bellman_ford(3,e,0,d), 0LL);
      vector<array<ll,3>> e2={{0,1,5},{1,2,-2}};
      CHECK("BF ok, d[2]", (bellman_ford(3,e2,0,d), d[2]), 3LL); }

    // Floyd-Warshall
    { const ll I=LLONG_MAX/8;
      vector<vector<ll>> d={{0,4,I},{I,0,2},{I,I,0}};
      floyd(d); CHECK("Floyd d[0][2]", d[0][2], 6LL); }

    // toposort of 0->1->3, 0->2->3
    { vector<vector<int>> adj={{1,2},{3},{3},{}};
      auto o=toposort(adj);
      CHECK("topo size", (ll)o.size(), 4LL);
      CHECK("topo starts at 0", (ll)o[0], 0LL);
      vector<vector<int>> cyc={{1},{0}};
      CHECK("topo detects cycle", (ll)toposort(cyc).size(), 0LL); }

    // Kruskal: triangle weights 1,2,3 => MST = 3
    { vector<array<ll,3>> e={{1,0,1},{2,1,2},{3,0,2}};
      CHECK("Kruskal MST", kruskal(3,e), 3LL); }

    // SCC: 0->1->2->0, 3 alone => 2 components
    { vector<vector<int>> adj={{1},{2},{0},{}};
      auto c=scc(adj); set<int> s(c.begin(),c.end());
      CHECK("SCC count", (ll)s.size(), 2LL);
      CHECK("SCC 0==1", (ll)(c[0]==c[1]), 1LL);
      CHECK("SCC 0!=3", (ll)(c[0]!=c[3]), 1LL); }

    // bipartite matching: L0-R0, L0-R1, L1-R0 => 2
    { vector<vector<int>> adj={{0,1},{0}};
      CHECK("Kuhn matching", (ll)matching(adj,2), 2LL); }

    // Dinic: s=0,t=3; 0->1 (3), 0->2 (2), 1->3 (2), 2->3 (3) => 4
    { Dinic d(4); d.add(0,1,3); d.add(0,2,2); d.add(1,3,2); d.add(2,3,3);
      CHECK("Dinic maxflow", d.maxflow(0,3), 4LL); }

    // knapsack: slide example W=18 -> 21
    { vector<int> wt={5,7,5,8,11,6}; vector<ll> val={6,7,4,10,14,5};
      CHECK("knapsack (slides)", knapsack(wt,val,18), 21LL); }

    // LIS of 1 7 3 2 3 9 4 7 11  => 6  (1,2,3,4,7,11)
    { vector<int> a={1,7,3,2,3,9,4,7,11};
      CHECK("LIS", (ll)lis(a), 6LL); }   // 1,2,3,4,7,11

    // coin change: coins 1,3,4 sum 6 => 2
    { vector<int> c={1,3,4}; CHECK("coin change", coin_change(c,6), 2LL); }

    // LCS "AGGTAB","GXTXAYB" => 4 (GTAB)
    { string a="AGGTAB", b="GXTXAYB"; CHECK("LCS", (ll)lcs(a,b), 4LL); }

    // sieve up to 30 => 10 primes
    { CHECK("sieve(30) count", (ll)sieve(30).size(), 10LL); }

    // gauss: x+y=3, x-y=1 => x=2,y=1
    { vector<vector<double>> a={{1,1,3},{1,-1,1}}; vector<double> ans;
      int r=gauss(a,ans);
      CHECK("gauss unique", (ll)r, 1LL);
      CHECK("gauss x", (ll)llround(ans[0]), 2LL);
      CHECK("gauss y", (ll)llround(ans[1]), 1LL); }

    // convex hull of unit square + interior point => 4
    { vector<Pt> p={{0,0},{2,0},{2,2},{0,2},{1,1}};
      CHECK("convex hull size", (ll)hull(p).size(), 4LL); }

    // KMP: "aba" in "abababa" => positions 0,2,4
    { auto r=kmp_find("aba","abababa");
      CHECK("kmp count", (ll)r.size(), 3LL);
      CHECK("kmp first", (ll)r[0], 0LL);
      CHECK("kmp last",  (ll)r[2], 4LL); }

    // trie
    { Trie t; t.insert("abc"); t.insert("abd");
      CHECK("trie has abc", (ll)t.contains("abc"), 1LL);
      CHECK("trie no ab",   (ll)t.contains("ab"),  0LL);
      CHECK("trie no abe",  (ll)t.contains("abe"), 0LL); }

    printf("\n%s  (%d failures)\n", bad? "SOME TESTS FAILED":"ALL TESTS PASSED", bad);
    return bad!=0;
}
