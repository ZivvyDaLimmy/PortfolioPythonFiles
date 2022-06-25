from itertools import product
from copy import deepcopy

from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox

from pynput import keyboard

root = Tk()

class gridButton():
    def __init__(self, buttonNo):
        self.row, self.column = buttonNo % 9, buttonNo // 9
        self.bgCol = "#c9c9cc" if (self.row // 3 + self.column // 3) % 2 else "#9ca3a4" #indicates the colour of the squares
        self.buttonCont = Button(root, text = "", width = 6, height = 3, fg = "#646365", font = helv10, 
                                 bg = self.bgCol,command = self.activate, activebackground = "cyan") #starting attributes of button
        self.buttonCont.grid(row = self.column, column = self.row) #reverse them IDK why, and also formats them onto the screen
        self.idNo = buttonNo
    def activate(self):
        global prevButton, sudokuBoard
        if prevButton: prevButton.buttonCont.config(bg = prevButton.bgCol) #de-highlights the button
        
        sudokuBoard[self.column][self.row] = '.' #click button to clear it if clicked by accident
        self.buttonCont.config(bg = "cyan", text = "", fg = "#646365")  #highlights the button so it is easy for the user to see which button is to be modified
        prevButton = self


def isSolvable() -> bool:
    global sudokuBoard
    square3x3 = [set() for _ in range(9)]
    rowLst, columnLst = deepcopy(square3x3), deepcopy(square3x3)
    for columnNo, column in enumerate(sudokuBoard): #checks if there are no duplicates in the rows,
        for rowNo, cell in enumerate(column): #columns, or 3x3 squares
            if cell == '.': continue
            if (cell in columnLst[columnNo] or cell in rowLst[rowNo] or
                cell in square3x3[(columnNo // 3) * 3 + (rowNo // 3)]): return False
            columnLst[columnNo].add(cell); rowLst[rowNo].add(cell)
            square3x3[(columnNo // 3) * 3 + (rowNo // 3)].add(cell)

    validLst = [set() for _ in range(81)]
    s3x32, rLst2, cLst2 = deepcopy(square3x3), deepcopy(rowLst), deepcopy(columnLst)
    for columnNo, column in enumerate(sudokuBoard): #checks whether all 9 digits can be'
        for rowNo, cell in enumerate(column): #can in each row, column, 3x3 square
            currInd = columnNo * 9 + rowNo
            if cell != '.': validLst[currInd] = {cell}; continue
            dummy = columnLst[columnNo] | rowLst[rowNo] | square3x3[(columnNo // 3) * 3 + (rowNo // 3)]
            for i in range(1, 10):
                if str(i) not in dummy: validLst[currInd].add(str(i))

            if not validLst[currInd]: return False #if no options are available for a single box
            s3x32[(columnNo // 3) * 3 + (rowNo // 3)] |= validLst[currInd]
            rLst2[rowNo] |= validLst[currInd]; cLst2[columnNo] |= validLst[currInd]
            
    for miniSet in s3x32 + rLst2 + cLst2:
        if len(miniSet) < 9: return False
    return validLst
               
def checkCell(rowInd, colInd, cell) -> bool:
    global sudokuBoard
    if cell in sudokuBoard[colInd]: return False
    for i in range(0, 9):
        if cell == sudokuBoard[i][rowInd]: return False
    for c, r in product(range((colInd // 3) * 3, (colInd // 3 + 1) * 3),
                range((rowInd // 3) * 3, (rowInd // 3 + 1) * 3)):
        if cell == sudokuBoard[c][r]: return False
    return True
    
def solveSudoku(ref) -> bool:
    global sudokuBoard
    terminator = False
    
    def backTrack(ind):
        nonlocal terminator, ref; global sudokuBoard
        rowInd, colInd = ind % 9, ind // 9 #sets the rows and columns
        if ind == 81: #FOUND THE SOLUTION
            terminator = True; return #TERMINATES THE RECURSIVE THING
        if sudokuBoard[colInd][rowInd] != '.': #skips, don't have to check this box as it can't be modified
            backTrack(ind + 1); return
        for cellOption in ref[ind]: #brute forces all options
            cellOption = str(cellOption)
            if checkCell(rowInd, colInd, cellOption): #can the cell be inserted
                sudokuBoard[colInd][rowInd] = cellOption #makes the cell into the desired number
                backTrack(ind + 1) #increases the index by 1
                if terminator: return; #if goal is found, no need to search anymore, just del.
                sudokuBoard[colInd][rowInd] = '.' #reverts back the condition
    backTrack(0) #calls the function to begin finding an answer
    return terminator #returns whether a solution has been found

'''
Algorithm Explanation:
The program accesses a cell from top to bottom:
0 1 2 3 4 5 6 7 8
9 10 ...
.... 81
For each cell it tries to brute force all 9 available numbers
to see whether it matches. If there's a match, the code will
modify the board so that the selected cell will be modified with the 
available match. It will call the function again with the modified
board, to the next cell. 
'''

def solveBoard():
    global sudokuBoard, grid, prevButton
    b = isSolvable()
    if not b or not solveSudoku(b): messagebox.showinfo("Error", "Sudoku isn't valid"); return #can't be solved
    for ind, button in enumerate(grid): #changes text of boxes to the answer
        button.buttonCont.config(text = sudokuBoard[ind // 9][ind % 9], bg = button.bgCol,
                                 activebackground = button.bgCol, command = lambda: 69)
    prevButton = None

def resetBoard():
    global sudokuBoard, grid, prevButton
    sudokuBoard = [['.'] * 9 for _ in range(9)] #resets sudoku board back
    for button in grid:
        button.buttonCont.config(text = "", fg = "#646365", bg = button.bgCol, state = NORMAL,
                                 activebackground = None, command = button.activate) #resets properties back
    prevButton = None

def on_press(key):
    global prevButton, sudokuBoard
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k.isnumeric() and k != '0' and prevButton:  # keys of interest
        prevButton.buttonCont.config(text = k, fg = "black") #changes text of button if number has been clicked
        sudokuBoard[prevButton.column][prevButton.row] = k

root.title("Sudoku Solver") #puts the title on the window

helv10 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD) #intializes the font
cour14 = tkFont.Font(family='Courier', size=16, weight=tkFont.BOLD) #intializes the font

prevButton = None #keeps track of the previously clicked button 
grid = [gridButton(no) for no in range(81)] #intializes the buttons

confButton = Button(root, text = "Click to solve", command = solveBoard, font = cour14, bg = "#b3b1b2")
confButton.grid(row = 9, column = 2, columnspan = 5) #Solve BTN
resButton = Button(root, text = "Reset", command = resetBoard, font = cour14, bg = "#b3b1b2")
resButton.grid(row = 10, column = 2, columnspan = 5) #Reset BTN

sudokuBoard = [['.'] * 9 for _ in range(9)]

listener = keyboard.Listener(on_press=on_press)
listener.start()
root.mainloop()
