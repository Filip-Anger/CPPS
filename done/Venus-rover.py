tests = int(input())
for _ in range(tests):
    n, time_limit, mass_capacity = map(int, input().split())
    
    stones = []
    for _ in range(n):
        stones.append(list(map(int, input().split()))) # pickup time, mass, value    
    stones.sort()
    
    table  = [[[0 for _ in range(time_limit + 1)] for _ in range(mass_capacity + 1)] for _ in range(n)]
    
    for a in range(mass_capacity + 1):
        for b in range(time_limit + 1):
            t, m, v = stones[0]
            if (t <= b) and (m <= a):
                table[0][a][b] = v 

    for i in range(1, n):
        # I use stones stones[:i]
        for m in range(mass_capacity + 1):
            for t in range(time_limit + 1):
                this_t, this_m, this_v = stones[i]
                if ((m - this_m) >= 0) and ((t - this_t) >= 0): 
                    table[i][m][t] = max(table[i-1][m][t], table[i- 1][m - this_m][t - this_t] + this_v) 
                else: 
                    table[i][m][t] = table[i-1][m][t]# value using first i stones, with m and t

    print(table[n-1][mass_capacity][time_limit])