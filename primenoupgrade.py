import math
def rec(x,b, depth = 0):
    if 1 >= b:
        return False
    if depth == 1000:
        return b

    if x%b == 0:
        return True
    else:
        return rec(x,b-1,depth+1)

while True:
    '''to test whether input would be valid'''
    while True:
        try:
            NUM = int(input("Enter the integer: "))
            break
        except:
            print("Put an integer lol")

    var = math.floor(math.sqrt(NUM))
    while True:
        y = rec(NUM, var)
        if y == False:
            print("Prime No")
            break
        elif y == True:
            print("Not a Prime No")
            break
        else:
            var = y
            
