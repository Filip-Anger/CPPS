#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

// ---------------- DSU ----------------
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

// ---------------- BFS ----------------
vector<int> bfs(vector<vector<int>>& adj, int s){
    vector<int> dist(adj.size(), -1);
    queue<int> q; dist[s]=0; q.push(s);
    while(!q.empty()){
        int v=q.front(); q.pop();
        for(int w: adj[v]) if(dist[w]==-1){
            dist[w]=dist[v]+1; q.push(w); }
    }
    return dist;
}

// ---------------- iterative DFS ----------------
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

// ---------------- Dijkstra ----------------
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

// ---------------- Bellman-Ford (+ negative cycle) ----------------
bool bellman_ford(int n, vector<array<ll,3>>& edges,
                  int s, vector<ll>& d){
    const ll INF = LLONG_MAX/4;
    d.assign(n, INF); d[s]=0;
    for(int i=0;i<n-1;i++)
        for(auto& e: edges)
            if(d[e[0]]<INF && d[e[0]]+e[2]<d[e[1]])
                d[e[1]]=d[e[0]]+e[2];
    for(auto& e: edges)              // one more pass => neg cycle
        if(d[e[0]]<INF && d[e[0]]+e[2]<d[e[1]]) return false;
    return true;
}

// ---------------- Floyd-Warshall ----------------
void floyd(vector<vector<ll>>& d){
    int n=d.size();
    for(int k=0;k<n;k++) for(int i=0;i<n;i++) for(int j=0;j<n;j++)
        if(d[i][k]+d[k][j] < d[i][j]) d[i][j]=d[i][k]+d[k][j];
}

// ---------------- topological sort (Kahn) ----------------
vector<int> toposort(vector<vector<int>>& adj){
    int n=adj.size(); vector<int> indeg(n,0), order;
    for(int v=0;v<n;v++) for(int w: adj[v]) indeg[w]++;
    queue<int> q;
    for(int v=0;v<n;v++) if(!indeg[v]) q.push(v);
    while(!q.empty()){
        int v=q.front(); q.pop(); order.push_back(v);
        for(int w: adj[v]) if(--indeg[w]==0) q.push(w);
    }
    return order;         // size < n  =>  graph has a cycle
}

// ---------------- Kruskal MST ----------------
ll kruskal(int n, vector<array<ll,3>> edges){
    sort(edges.begin(), edges.end());             // weight first
    DSU d(n); ll total=0;
    for(auto& e: edges) if(d.unite(e[1],e[2])) total+=e[0];
    return total;
}

// ---------------- Kosaraju SCC ----------------
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
            if(!i){ if(seen[v]){ st.pop_back(); continue; }
                    seen[v]=1; }
            if(i < (int)adj[v].size()){ int w=adj[v][i++];
                if(!seen[w]) st.push_back({w,0}); }
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
            for(int w: rev[v]) if(comp[w]==-1){
                comp[w]=c; st.push_back(w); }
        }
        c++;
    }
    return comp;
}

// ---------------- Kuhn bipartite matching ----------------
bool try_kuhn(int v, vector<vector<int>>& adj,
              vector<int>& used, vector<int>& mt){
    for(int to: adj[v]){
        if(used[to]) continue;
        used[to]=1;
        if(mt[to]==-1 || try_kuhn(mt[to],adj,used,mt)){
            mt[to]=v; return true; }
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

// ---------------- Dinic max flow ----------------
struct Dinic {
    struct E{ int to; ll cap; };
    vector<E> es; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n): g(n), lvl(n), it(n) {}
    void add(int a,int b,ll c){
        g[a].push_back(es.size()); es.push_back({b,c});
        g[b].push_back(es.size()); es.push_back({a,0}); }
    bool bfs(int s,int t){
        fill(lvl.begin(),lvl.end(),-1);
        queue<int> q; lvl[s]=0; q.push(s);
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

// ---------------- 0/1 knapsack (1-D) ----------------
ll knapsack(vector<int>& wt, vector<ll>& val, int W){
    vector<ll> dp(W+1,0);
    for(size_t i=0;i<wt.size();i++)
        for(int w=W; w>=wt[i]; w--)    // DESCENDING: item used once
            dp[w]=max(dp[w], dp[w-wt[i]]+val[i]);
    return dp[W];
}

// ---------------- LIS  O(n log n) ----------------
int lis(vector<int>& a){
    vector<int> t;
    for(int x: a){
        // upper_bound instead => longest NON-DECREASING
        auto it=lower_bound(t.begin(),t.end(),x);
        if(it==t.end()) t.push_back(x); else *it=x;
    }
    return t.size();
}

// ---------------- coin change (min coins) ----------------
ll coin_change(vector<int>& c, int S){
    const ll INF=LLONG_MAX/4;
    vector<ll> dp(S+1,INF); dp[0]=0;
    for(int s=1;s<=S;s++) for(int x: c)
        if(x<=s && dp[s-x]+1<dp[s]) dp[s]=dp[s-x]+1;
    return dp[S];
}

// ---------------- LCS ----------------
int lcs(string& a, string& b){
    vector<vector<int>> dp(a.size()+1, vector<int>(b.size()+1,0));
    for(size_t i=1;i<=a.size();i++) for(size_t j=1;j<=b.size();j++)
        dp[i][j] = (a[i-1]==b[j-1]) ? dp[i-1][j-1]+1
                                   : max(dp[i-1][j],dp[i][j-1]);
    return dp[a.size()][b.size()];
}

// ---------------- sieve ----------------
vector<int> sieve(int n){
    vector<char> is(n+1,1); is[0]=is[1]=0;
    for(int i=2;(ll)i*i<=n;i++) if(is[i])
        for(int j=i*i;j<=n;j+=i) is[j]=0;
    vector<int> pr;
    for(int i=2;i<=n;i++) if(is[i]) pr.push_back(i);
    return pr;
}

// ---------------- Gaussian elimination ----------------
int gauss(vector<vector<double>> a, vector<double>& ans){
    int n=a.size(), m=a[0].size()-1;
    vector<int> where(m,-1);
    for(int col=0,row=0; col<m && row<n; col++){
        int sel=row;
        for(int i=row;i<n;i++)
            if(fabs(a[i][col])>fabs(a[sel][col])) sel=i;
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
    for(int i=0;i<m;i++) if(where[i]!=-1)
        ans[i]=a[where[i]][m]/a[where[i]][i];
    for(int i=0;i<n;i++){
        double sum=0;
        for(int j=0;j<m;j++) sum+=ans[j]*a[i][j];
        if(fabs(sum-a[i][m])>1e-6) return 0;      // no solution
    }
    for(int i=0;i<m;i++) if(where[i]==-1) return 2;  // infinitely many
    return 1;
}

// ---------------- convex hull (Andrew monotone chain) ----------------
typedef pair<ll,ll> Pt;
ll cross(Pt O, Pt A, Pt B){
    return (A.first-O.first)*(B.second-O.second)
         - (A.second-O.second)*(B.first-O.first);
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

// ---------------- KMP prefix function ----------------
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

// ---------------- trie ----------------
struct Trie {
    vector<array<int,26>> ch; vector<int> cnt;
    Trie(){ newNode(); }
    int newNode(){ ch.push_back({}); ch.back().fill(-1);
                   cnt.push_back(0); return ch.size()-1; }
    void insert(const string& s){
        int v=0;
        for(char c: s){ int x=c-'a';
            if(ch[v][x]==-1) ch[v][x]=newNode();
            v=ch[v][x]; }
        cnt[v]++;
    }
    bool contains(const string& s){
        int v=0;
        for(char c: s){
            int x=c-'a';
            if(ch[v][x]==-1) return false;
            v=ch[v][x];
        }
        return cnt[v]>0;
    }
};
