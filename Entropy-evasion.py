n = int(input())
print("1 1")

while True:
    nums = list(map(int, input().split())) 
    per = int(input())
    if per >= 70:
        break
    for i in range(n):
        nums[i] = nums[i] * (-2) + 1

    for i in range(1, n):
        nums[i] += nums[i-1]
    summ = 0
    start, end = 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            sumn = nums[j] - nums[i]
            if sumn >= summ:
                summ = sumn
                start, end = i, j
                if summ >= 5: break

    print(str(start + 1) + " " + str(end + 1), flush=True)