from tkinter import *
import random
import math
from functools import partial
import copy
import time
root = Tk()

def photo():
    global board,counter
    if counter % 2 == 1:
        return [photo1,2,'o']
    else:
        return [photo2,1,'x']

def disableall(x=NORMAL,y=DISABLED):
    #not necessarily disable all cause it then enables all but eh
    global whoStarts
    for i in range(len(button)):
        button[i].config(state = x)
        if x == NORMAL:
            #reverts buttons back to their original
            button[i].config(image= photop)
    resetButton.config(state=y)

    if x == NORMAL:
        global board, counter
        board = [['-','-','-'],
                 ['-','-','-'],
                 ['-','-','-']]
        if whoStarts[0] == 'bot':
            counter = 0
            bot()
        else:
            counter = 1
        if whoStarts[1] == 'multi':
            myLabel.config(text = "Player 1 turn")
        else:
            myLabel.config(text = "Player turn")
        
def check2(x = [True,False]):
##    print(board)
    #changes the UI if game is finised
    global counter, whoStarts, board
    if x[0] == True:
        if x[1] == True:
            disableall(DISABLED,NORMAL)
            return None
        elif counter == 9:
            myLabel.config(text ="Tie, you both suck")
            disableall(DISABLED,NORMAL)
            return None
        counter += 1
        if whoStarts[1] == 'single':
            bot()

def click(i):
    b = photo()
    if whoStarts[1] == 'single':
        check2(playereval(b[2],b[0],i))
    else:
        check2(playereval(b[2],b[0],i,b[1]))

def check(b):
    global counter
##    print(counter)
    return ((b[0][0] == b[0][1] == b[0][2] and b[0][2] != '-') or
            (b[1][0] == b[1][1] == b[1][2] and b[1][2] != '-') or
            (b[2][0] == b[2][1] == b[2][2] and b[2][2] != '-') or
            (b[0][0] == b[1][0] == b[2][0] and b[2][0] != '-') or
            (b[0][1] == b[1][1] == b[2][1] and b[2][1] != '-') or
            (b[0][2] == b[1][2] == b[2][2] and b[2][2] != '-') or
            (b[0][0] == b[1][1] == b[2][2] and b[2][2] != '-') or
            (b[0][2] == b[1][1] == b[2][0] and b[2][0] != '-'))
        

def playereval(logo,pic,x, player = None):
    if player == None:
        myLabel.config(text =  f"Player turn")
    else:
        myLabel.config(text = f"Player {player} turn")

    if board[math.floor((x-1)/3)][x%3 -1] == '-':
        #changes the board list not visible to the player
        board[math.floor((x-1)/3)][x%3 -1] = logo

        #changes the buttons visible to the player
        button[x-1].config(image = pic)
        if check(board) == True:
            if player == None:
                myLabel.config(text = f"Player wins")
            else:
                myLabel.config(text = f"Player {(player%2)+1} wins")
            return [True,True]
        return [True,False]
    else:
        #if u ask me why not disable when clicked but disable when the game ends
        #i just personally think the the colour of the button during the game being
        #discoloured looks a bit weird
        
        myLabel.config(text ="Occupied")
        return [False,False]

def botIterations(marker, b,returnWhenFound = True):
    duplicate = copy.deepcopy(b)
    checksVar = 0
    for i in range(3):
        for i2 in range(3):
            if b[i][i2] == '-':
                duplicate[i][i2] = marker
                if check(duplicate) == True:
                    duplicate[i][i2] = 'x'
                    if returnWhenFound == True:
                        return [True,duplicate,(i*3+i2)] #move made, returns duplicate
                    else:
                        checksVar += 1
                else:
                    duplicate = copy.deepcopy(b)
    return [False,None,checksVar]


def bot():
    global board, counter
    
    if botIterations('x',b=board)[0] == True:
        #1st priority: any more moves the can result in it winning?
        holderB = botIterations('x',b=board)
        board = holderB[1]
        button[holderB[2]].config(image = photo2)
        disableall(DISABLED,NORMAL)
        myLabel.config(text = "Bot wins")
        return None
    elif botIterations('o',b=board)[0] == True:
        #2nd priority: block any checks made
        holderB = botIterations('o',b=board)
        board = holderB[1]
        button[holderB[2]].config(image = photo2)
    elif counter == 1 or counter == 0:
        #2.5th priority, if starting position
        if board[1][1] == '-':
            board[1][1] = 'x'
            button[4].config(image = photo2)
        else:
            board[0][0] = 'x'
            button[0].config(image = photo2)
    else:
        #3rd priority, try to win by making its own move
        list2 = []
        duplicate2 = copy.deepcopy(board)
        threshold = -1
        holdervar = None
        for i in range(8):
            if board[math.floor(i/3)][i%3] == '-':
                duplicate2[math.floor(i/3)][i%3] = 'x'
                list2.append([botIterations('x',duplicate2, False),i,duplicate2])
                duplicate2 = copy.deepcopy(board)
        for i in range(len(list2)):
            
            if list2[i][0][2] > threshold:
                threshold = list2[i][0][2]
                holdervar = i
        try:
            board = list2[holdervar][2]
            button[list2[holdervar][1]].config(image = photo2)
        except:
            pass
    counter += 1
    if counter == 9:
        check2()

#declaring starter variables

def start(selectedType):
    b3.destroy()
    if selectedType == 'singleplayer':
        b1.config(text="Bot First", command=partial(main,'BOT',"single"))
        b2.config(text="Player first", command=partial(main,'PLAYER',"single"))
    else:
        main('PLAYER','multi')

def main(first,typ):
    b1.destroy()
    b2.destroy()
    
    global myLabel, button, resetButton, counter, playerLabel1, playerLabel2, whoStarts, board, backButton
    board = [['-','-','-'],
             ['-','-','-'],
             ['-','-','-']]
    counter = 1
    if typ == "multi":
        whoStarts[0] = 'player'
        whoStarts[1] = 'multi'
        myLabel = Label(root,text="Player 1 turn", font = ('Helvetica', 11, 'bold'))
    else:
        whoStarts[1] = 'single'
        myLabel = Label(root,text="Player turn", font = ('Helvetica', 11, 'bold'))
    myLabel.grid(row=1,column=4)

    playerLabel1 = Label(root,text="Player 1 = 'O'", font = ('Helvetica', 9))
    if typ == 'multi':
        playerLabel2 = Label(root,text="Player 2 = 'X'", font = ('Helvetica', 9))
    else:
        playerLabel2 = Label(root,text="Bot = 'X'", font = ('Helvetica', 9))
    playerLabel1.grid(row=0,column = 4)
    playerLabel2.grid(row=0,column =5)
    
    resetButton = Button(root, command = disableall, text = "Reset?", state = DISABLED)
    resetButton.grid(row=2,column=4)
    button = [Button(root, command = partial(click,1), image = photop),
              Button(root, command = partial(click,2), image = photop),
              Button(root, command = partial(click,3), image = photop),
              Button(root, command = partial(click,4), image = photop),
              Button(root, command = partial(click,5), image = photop),
              Button(root, command = partial(click,6), image = photop),
              Button(root, command = partial(click,7), image = photop),
              Button(root, command = partial(click,8), image = photop),
              Button(root, command = partial(click,9), image = photop)]

    for i in range(len(button)):
        #sets up the 3x3 grid
        button[i].grid(row=math.floor(i/3),column = (i%3))
    backButton = Button(root, text = "Back", padx=10,command=alpha)
    backButton.grid(row = 2,column = 5)
    
        
    if first != "PLAYER":
        whoStarts[0] = 'bot'
        counter = 0
        bot()

photop = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\box.png")
photo1 = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\circle.png")
photo2 = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\cross.png")

counter = 1
myLabel = None
playerLabel1 = None
playerLabel2 = None
whoStarts = ['player','single']
resetButton = None
button = None
backButton = None
root.title('Tic Tac Toe')
board = None

b1 = None
b2 = None
b3 = None
def alpha():
    global myLabel, button, resetButton, playerLabel1, playerLabel2, b1, b2, b3
    try:
        myLabel.destroy()
        for i in button:
            i.destroy()
        resetButton.destroy()
        backButton.destroy()
        playerLabel1.destroy()
        playerLabel2.destroy()
    except:
        pass
    b1 = Button(root, text="Multiplayer", command=partial(start,'multiplayer'),padx = 100, pady = 20, font = ('Helvetica', 11, 'bold'))
    b2 = Button(root, text="Singleplayer", command=partial(start,'singleplayer'),padx = 100, pady = 20, font = ('Helvetica', 11, 'bold'))
    b3 = Button(root, text="Close", command=root.destroy,padx = 100, pady = 20, font = ('Helvetica', 11, 'bold'))
    b1.grid(row=0,column=0)
    b2.grid(row=1,column=0)
    b3.grid(row=2,column=0)

alpha()
