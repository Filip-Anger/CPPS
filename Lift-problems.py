tests = int(input())
for _ in range(tests):
    floors = int(input())
    outs = list(map(int, input().split()))
    
    
    s = sum(outs)
    
    present = [s - o for o in outs] # anger of stopping FIXED TRUE

    want_to_get_out = []
    consum = 0
    for out in outs:
        consum += out
        want_to_get_out.append(consum) # anger of not stopping
        
    
    total_anger = sum(present)
    
    table = [[0 * floors] for i in range(floors)]
    for i in range(floors):
        table[0][i] = 
    got_out = 0
    angers = []
    
    for i in range(floors):
        if present[i] <= (want_to_get_out[i] - got_out):
            got_out = want_to_get_out[i]
            anger += present[i]
        else:
            anger += (want_to_get_out[i] - got_out)
            
        
    print (anger)