from tkinter import *
import random
import math
from functools import partial

root = Tk()

def photo():
    global counter
    if counter % 2 == 1:
        return [photo1,2,'o']
    else:
        return [photo2,1,'x']

def disableall(x=NORMAL,y=DISABLED):
    #not necessarily disable all cause it then enables all but eh
    
    for i in range(len(button)):
        button[i].config(state = x)
        if x == NORMAL:
            #reverts buttons back to their original
            button[i].config(image= photop)
    resetButton.config(state=y)

    if x == NORMAL:
        global board
        global counter
        myLabel.config(text = "Player 1 turn")
        counter = 1
        board = [['-','-','-'],
                 ['-','-','-'],
                 ['-','-','-']]
        
def check2(x):
    #changes the UI if game is finised
    global counter
    if x[0] == True:
        if x[1] == True:
            disableall(DISABLED,NORMAL)
        elif counter == 9:
            myLabel.config(text ="Tie, you both suck")
            disableall(DISABLED,NORMAL)
        counter += 1

def click(i):
    b = photo()
    check2(playereval(b[1],b[2],b[0],i))

def check():
    return ((board[0][0] == board[0][1] == board[0][2] and board[0][2] != '-') or
            (board[1][0] == board[1][1] == board[1][2] and board[1][2] != '-') or
            (board[2][0] == board[2][1] == board[2][2] and board[2][2] != '-') or
            (board[0][0] == board[1][0] == board[2][0] and board[2][0] != '-') or
            (board[0][1] == board[1][1] == board[2][1] and board[2][1] != '-') or
            (board[0][2] == board[1][2] == board[2][2] and board[2][2] != '-') or
            (board[0][0] == board[1][1] == board[2][2] and board[2][2] != '-') or
            (board[0][2] == board[1][1] == board[2][0] and board[2][0] != '-'))
        

def playereval(player,logo,pic,x):
    myLabel.config(text = f"Player {player} turn")

    if board[math.floor((x-1)/3)][x%3 -1] == '-':
        #changes the board list not visible to the player
        board[math.floor((x-1)/3)][x%3 -1] = logo

        #changes the buttons visible to the player
        button[x-1].config(image = pic)
        if check() == True:
            myLabel.config(text = f"Player {(player%2)+1} wins")
            return [True,True]
        return [True,False]
    else:
        #if u ask me why not disable when clicked but disable when the game ends
        #i just personally think the the colour of the button during the game being
        #discoloured looks a bit weird
        
        myLabel.config(text ="Occupied")
        return [False,False]


#declaring starter variables

photop = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\box.png")
photo1 = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\circle.png")
photo2 = PhotoImage(file = r"C:\Users\ZivLim\Desktop\Python Files\Images\cross.png")
#change ur file name accordingly

board = [['-','-','-'],
         ['-','-','-'],
         ['-','-','-']]
#board not visible to the plater


myLabel = Label(root,text="Player 1 turn", font = ('Helvetica', 11, 'bold'))
myLabel.grid(row=1,column=4)

playerLabel1 = Label(root,text="Player 1 = 'O'", font = ('Helvetica', 9))
playerLabel2 = Label(root,text="Player 2 = 'X'", font = ('Helvetica', 9))
playerLabel1.grid(row=0,column = 4)
playerLabel2.grid(row=0,column =5)

counter = 1

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

root.title('Tic Tac Toe')

for i in range(len(button)):
    #sets up the 3x3 grid
    button[i].grid(row=math.floor(i/3),column = (i%3))

