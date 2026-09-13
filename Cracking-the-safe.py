s4 = {0, 1, 2, 3}

    
def product(nums):
    24 = 1 * 24 = 2 * 12 = 3 * 8 = 4 * 6
    # 0 - 4 split
    
    # 1 - 3 split
    for i in range(4):
        chosen = nums[i]
        other = nums[:i] + nums[i+1:]
        # pruduct 
        p = sum(other) * chosen
        if p == 24:return True
        
    # 2 - 2 split
        a, b, c, d = nums
        
n = int(input())
for _ in range(n):
    nums = sorted(list(map(int, input().split())), reverse=True)
    
    
    print(nums)