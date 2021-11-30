import time
def hardytesting():
    while True:
        try:
            NUM = int(input("Enter the integer: "))
            break
        except:
            print("Put an integer lol")
    return NUM

def rec(m,n,add,depth = 0):
    
    if depth == 1000:
        return [m,False]
    
    if m%n == 0:
        return [m,True]
    else:
        return rec(m+add,n,add,depth+1)
    


while True:
    a = hardytesting()
    b = hardytesting()
    lcm = max(a,b)
    
    if a<b:
        DIVISOR = a
    else:
        DIVISOR = b

    while True:
        c = rec(lcm,DIVISOR,max(a,b))
        if c[1] == True:
            print(c[0])
            break
        else:
            lcm = c[0]
            #time.sleep(1)
