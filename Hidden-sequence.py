# import sys
# import math
# from collections import deque, defaultdict, Counter
# from heapq import heappush, heappop, heapify
# from bisect import bisect_left, bisect_right, insort
# from itertools import permutations, combinations, product, accumulate
# from functools import lru_cache

# # ---------------------------------------------------------------- INPUT
# # All of stdin, read once, split in C. Never call input() below.
# _data = sys.stdin.buffer.read()
# _it = iter(_data.split())

# def nall():      return list(map(int, _it)) 




_out = []
def emit(*args): _out.append(' '.join(map(str, args)))



# playes = nall()
# emit(playes)



player = []

winners = ''
for i in range(3):
    player.append(input())

i, j, k = 0, 0, 0
while True:
    p1 = player[0][i] if (i < len(player[0])) else False
    p2 = player[1][j] if (j < len(player[1])) else False
    p3 = player[2][k] if (k < len(player[2])) else False
    if p1 == p2:
        winners += '3'
        i += 1
        j += 1
    elif p1 == p3:
        winners += '2'
        i += 1
        k += 1
    elif p3 == p2:
        winners += '1'
        k += 1
        j += 1

    if (i >= len(player[0])) and (j >= len(player[1])) and (k >= len(player[2])):
        break

print(winners)