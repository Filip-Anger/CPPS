import sys

def solve():
    # Read a single integer
    n = int(sys.stdin.readline())
    
    # Read a list of space-separated integers on a single line
    array = list(map(int, sys.stdin.readline().split()))
    
    # Read a string (remember to strip the trailing newline!)
    s = sys.stdin.readline().rstrip()

    print(n)
    print(array)
    print(s)
if __name__ == '__main__':
    solve()