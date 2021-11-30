import pyautogui
'''to take a screenie of the laptop and identify
a pixel's rgb value'''
import time
import keyboard
'''to detect and to press keyboard stuff'''
import win32api, win32con

Xslist=[558,660,762]
Yslist=[479,575,671]
clicklstX=[]
clicklstY=[]
lstwires=[293,470,631,810]
lstcalY=[255,503,740]

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def connect(r,g,b):
    pi1c = pyautogui.screenshot(region=(0,0, 1919, 1079))
    for i2 in range(0,4):
        rd,gd,bd = pi1c.getpixel((1298,lstwires[i2]-7))
        if rd==r and gd==g and bd==b:
            pyautogui.mouseDown()
            '''i used pyautogui instead of win32api cause it's too fast'''
            pyautogui.moveTo((1298,lstwires[i2]))
            pyautogui.mouseUp()
            break
        else:
            pass

def startwires():
    time.sleep(0.5)
    pic = pyautogui.screenshot(region=(0,0, 1919, 1079))
    for i in range(0,4):
        pyautogui.moveTo(575,lstwires[i]-7)
        time.sleep(0.1)
        r,g,b = pic.getpixel((575,lstwires[i]))
        '''gets the pixel value of the left part of the wires,
        then runs the connect function to identify which wires
        at the right part have the same colour, if the colour
        is the same, match em'''
        connect(r,g,b)

def sabotagecommspic():
    pic = pyautogui.screenshot(region=(1322,659, 1, 1))
    r,g,b = pic.getpixel((0,0))
    if r==46 and g==58 and b==58:
        '''basically when doing a comms sabotage, there would be a red light on
        if its not fixed, when it's fixed the red light would be off'''
        return True
    else:
        return False

def sabotagecomms():
    pyautogui.moveTo(1143,845)
    x=sabotagecommspic()
    pyautogui.moveTo(1184,829)
    time.sleep(2)
    pyautogui.mouseDown()
    x1, x2, x3 =True, True, True
    '''this code just brute forces the sabotaging comms process
    till the red light is off'''
    if x:
        for i in range(0,172,2):
            win32api.SetCursorPos((1143,845-i))
            x1 = sabotagecommspic()
            if x1==False:
                break
        if x1:
            for i in range(0,150,2):
                win32api.SetCursorPos((1143+i,677))
                x2 = sabotagecommspic()
                if x2==False:
                    break
            if x2:
                for i in range(0,172,2):
                    win32api.SetCursorPos((1288,677+i))
                    x3=sabotagecommspic()
                    if x3==False:
                        break
    pyautogui.mouseUp()


lstglowyx=[820,749,672,593]     
def startreactor():
    keyboard.press('space')
    '''honestly coding gore from me took me some time to shorten this code
    idk if there is gonna be a bug but yea'''
    time.sleep(1)
    pic = pyautogui.screenshot(region=(0,0, 1919, 1079))
    identified = False
    for i in range(0,4):
        r,g,b = pic.getpixel((lstglowyx[i],336))
        if r == 0 and g in range(189,193) and b in range(0,5):
            xyz=i+1
            identified = True
            break
    if identified != True:
        xyz = 5

    '''this function above picks up how many more iterations of the code has to be done
    this is based out of the green LED thingy that tells one the depth of the reactor task'''
    for i in range(1,xyz+1):
        for z in range(0,i):
            asdf=False
            while True:
                pic = pyautogui.screenshot(region=(0,0, 800, 800))
                for x in Xslist:
                    for y in Yslist:
                        r,g,b = pic.getpixel((x,y))
                        if r==68 and g==168 and b==255:
                            '''brute forces, check if a square is lit up'''
                            clicklstX.append(x)
                            clicklstY.append(y)
                            asdf=True
                            break
                    if asdf:
                        break
                if asdf:
                    break
            time.sleep(0.25)
##            while True:
##                pic = pyautogui.screenshot(region=(0,0, 800, 800))
##                r,g,b = pic.getpixel((x,y))
##                if r!=68:
##                    break
        time.sleep(0.7)
        print(clicklstX)
        print(clicklstY)
        '''the time.sleep breaks above seems to be hard coding, since i can't experiment with my code now,
        id just comment what i think would be the solution'''
        for iz in range(1):
            win32api.SetCursorPos((clicklstX[iz]+561,clicklstY[iz]))
            click()
            print(f"X: {clicklstX[iz]+561}, Y: {clicklstY[iz]}")
            
            time.sleep(0.3)
        clicklstX.clear()
        clicklstY.clear()

def electrical_callibrator():
    time.sleep(1)
    for i in lstcalY:
        win32api.SetCursorPos((1189,i+65))
        while True:
            pic=pyautogui.screenshot(region=(1189,i, 1, 1))
            '''for electrical callibrators, there would be some sort of meter at the side
            to let one know when to press a specific button, when the meter is at it's maximum
            this code presses the specified button'''
            r,g,b = pic.getpixel((0,0))
            if r != 0:
               '''the code to check whether if the meter is at its maximum or not'''
               click()
               break

def chute():
    '''very simple just press a drag mouse quickly cause im lazy lol'''
    time.sleep(0.6)
    win32api.SetCursorPos((1245,437))
    pyautogui.mouseDown()
    win32api.SetCursorPos((1245,750))
    time.sleep(1.5)
    pyautogui.mouseUp()

def swipe_card():
    
    '''this is troublesome, you need the perfect speed,
    for me, i found this to be optimal'''
    time.sleep(0.6)
    win32api.SetCursorPos((840,784))
    click()
    click()
    time.sleep(0.6)
    win32api.SetCursorPos((595,429))
    pyautogui.mouseDown()
    for i in range(38,836,38):
        win32api.SetCursorPos((595+i,429))
        time.sleep(0.025)
    pyautogui.mouseUp()


print("""CTRL + W = Wires\nCTRL + S = Simon Says\nCTRL + SHIFT = Sabotage Comms\nCTRL + X = Electrical Callibrator\nCTRL + A = O2 Chute\nCTRL + D = Swipe Card""")
while True:
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('w'):
        keyboard.press('space')
        startwires()
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('s'):
        keyboard.press('space')
        startreactor()
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('shift'):
        keyboard.press('space')
        sabotagecomms()
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('x'):
        electrical_callibrator()
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('a'):
        keyboard.press('space')
        chute()
    if keyboard.is_pressed('ctrl') == True and keyboard.is_pressed('d'):
        keyboard.press('space')
        swipe_card()
