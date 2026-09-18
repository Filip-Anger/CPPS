import sys

input_line = sys.stdin.readline

n = int(input_line())
print(1, 1, flush=True)

while True:
    nums = list(map(int, input_line().split()))
    per = int(input_line())
    if per >= 70:
        break

    # Score each cell: a zero is worth +1 (we want to re-roll it),
    # a one is worth -1 (re-rolling it costs us). The best window to
    # expose is the contiguous run with the largest total score.
    #
    # Maximum subarray in one pass: for a window ending at j, the sum is
    # pref[j] - pref[start-1], so we want the SMALLEST prefix seen so far.
    # Carry it in a variable instead of searching for it.

    best = 0
    bl = br = 0          # fallback window, always legal

    pref = 0
    minpref = 0          # empty prefix, i.e. "before the array starts"
    minpos = -1          # where that minimum was

    for j in range(n):
        pref += 1 if nums[j] == 0 else -1

        # compare BEFORE updating, or you allow an empty window
        if pref - minpref > best:
            best = pref - minpref
            bl, br = minpos + 1, j

        if pref < minpref:
            minpref = pref
            minpos = j

    print(bl + 1, br + 1, flush=True)
