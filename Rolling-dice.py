all = [[1,3,6,4], [1,2,6,5], [3,2,4,5]]

pointerUp = (1, 0)
pointerRight = (0, 0)



def up(val: int):
    pointerUp = (pointerUp, pointerUp[(pointerUp + int) % 4])
    pointerRight = (pointerRight)
    

n = int(input())
for _ in range(n):
    x_cord = 0
    y_cord = 0
    index = (0, 0)
    sign = 1
    horizontal = 0
    vertical = 1
    line = input()
    if line[0] == "-":
        sign = - 1
    segmetns = line.replace("-", "+").split( "+")
    for segment in segmetns:
        number = ""
        val = 1
        for char in segment:
            if char.isnumeric():
                number += char
                continue
            elif number != "":
                val = int(number)
                number = ""
                
            if char == "X":
                x_cord += sign * val
                right(sign * val)
            elif char == "Y":
                y_cord += sign * val
                up(sign * val)
                
                
            val = 1
        sign = - sign