tests = int(input())
for _ in range(tests):
    n, time, mass = map(int, input().split())
    
    stones = []
    for _ in range(n):
        t, m, v = map(int, input().split())
        stones.append((v, m, t))
    
    stones.sort()
    
    cur_m = 0
    cur_t = 0
    value = 0
    for stone in stones:
        v, m, t = stone
        if (cur_m + m <= mass) and (cur_t + t <= time):
            value += v
            cur_m += m
            cur_t += t
            
    print(value)