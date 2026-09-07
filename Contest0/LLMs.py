s = input()
sl = len(s)
n = int(input())


def func():
    dict = set()
    for i in range(n):
        dict.add(input())
        


    pointers = {0}

    while len(pointers) > 0:
        doing = min(pointers)
        pointers.remove(doing)
        for length in range(6, 11):
            if s[doing: doing + length] in dict:
                l = doing + length
                if l == sl:
                    return "yes"
                pointers.add(l)
    return "no"

        
        
print(func())