l = input()

lst = [0 for i in range(200)]
for a in l:
    lst[ord(a)] += 1

odd = 0
for s in lst:
    if s % 2 == 1:
        odd +=1

if odd == len(l) %2:
    print("yes")
else:
    print("no")
