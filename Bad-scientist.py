def backtrack(graph, i, removed, remaining):
    if len(succ) > 0:
        if removed >= min(succ):
            return
    if removed <= k:
        if remaining == 0:
            succ.add(removed)
            return
        for j in range(i, n):
            if remaining == 0:
                return
            if len(graph[i]) == 0:
                backtrack(graph.copy(), i + 1, removed, remaining)
            else:
                if min(graph[i]) > i:
                    backtrack(graph.copy(), i + 1, removed, remaining)   
                remaining -= len(graph[i])
                for sused in graph[i]:
                    graph[sused].remove(i)
                graph[i] = set()
                removed += 1
                backtrack(graph.copy(), i + 1, removed, remaining)
                
                
t = int(input())

for _ in range(t):
    n = int(input()) + 1
    k = int(input())
    m = int(input())

    graph = [set() for _ in range(n)] # Adjencency
    for _ in range(m):
        a, b = map(int, input().split())
        graph[a].add(b)
        graph[b].add(a)

    succ = set()    

    backtrack(graph, 0, 0, m)

    if len(succ) == 0:
        print("IMPOSSIBLE")
    else: 
        print(min(succ))