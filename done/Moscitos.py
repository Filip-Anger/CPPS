tests = int(input())

for _ in range(tests):
    hit = set()
    n = int(input())
    moscitos = []
    for i in range(n):
        x, y = map(int, input().split())
        moscitos.append((x,y))
    m = int(input())
    for i in range(m):
        x, y = map(int, input().split())
        for j in range(len(moscitos)):
            if j in hit: continue
            if x+50 >= moscitos[j][0] >= x - 50:
                if y+50 >= moscitos[j][1] >= y - 50:
                    hit.add(j)
                    
                    
    print(len(hit))