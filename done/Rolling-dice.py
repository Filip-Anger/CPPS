top = 1
front = 2
left = 4


def move(val: int, up : bool):
    global top, front, left
    mod = val % 4
    if mod == 0:
        return
    
    if up:
        if mod == 2:
            front = 7 - front
            top = 7 - top
        if mod == 1:
            t = top
            top = front
            front = 7 - t 
        if mod == 3:
            t = top
            top = 7 - front
            front = t
    else:
        if mod == 2:
            left = 7 - left
            top = 7 - top
        if mod == 1:
            t = top
            top = left
            left = 7 - t
        if mod == 3:
            t = top
            top = 7 - left
            left = t
        
def do_line(line):
    global x_cord, y_cord
    sign = 1
    
    if line[0] == "-":
        sign = - 1
        line = line[1:]
    segmetns = line.replace("-", "+").split( "+")
    for segment in segmetns:
        number = ""
        val = 1
        for char in segment:
            if char == ".": 
                return
            if char.isnumeric():
                number += char
                continue
            elif number != "":
                val = int(number)
                number = ""
                
            if char == "X":
                x_cord += sign * val
                move(sign * val, False)
            elif char == "Y":
                y_cord += sign * val
                move(sign * val, True)
            val = 1
        sign = - sign
                
n = int(input())
for _ in range(n):
    
    top = 1 
    front = 2
    left = 3
    
    x_cord = 0
    y_cord = 0
    line = input()
    
    do_line(line)
    pos = str(x_cord) + "," + str(y_cord)
    
    print("position (" + pos + "), " + str(top) + " dots")