n = int(input())
cuteness = list(map(int, input().split()))

m = int(input())
moves = []



# indexes = [[cuteness[i], i ] for i in range(n)]
# operation = []



def swap(array : list, pair):
    # Select
    fro = pair[0]
    to = pair[1]
    first = array.pop(fro)
    sec = array.pop(fro + 1)
    tir = array.pop(fro + 2)
    
    array.insert(to, first)
    array.insert(to + 1, sec)
    array.insert(to + 2, tir)
    
    return array

for j in range(m):
    s = list(map(int,input().split()))
    cuteness = swap(cuteness, s)
    
print(cuteness)
    
# for i in range(n):
#     # Grab the index if the min A[i:] and move it to i
#     next = min(cuteness[i:])
#     index = cuteness.index(next)
#     if index > (n - 3):
#         last = max(cuteness[i + 2:])
#         curr_ind = last - 2 + 1
#         # put to the correct index
#         correct_index = sorted_indexex[last]
#         resulting_index = correct_index -2 + 1
#         operation.append([curr_ind, resulting_index])
        
#         next = min(cuteness[i:])
#         index = cuteness.index(next)
#         move = [index + 1, i + 1]
#         operation.append(move)
        
#     move = [index + 1, i + 1]
#     operation.append(move)
    

print(len(operation))
for line in operation:
    print(line[0], line[1])
    

