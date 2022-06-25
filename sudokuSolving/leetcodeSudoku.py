class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        terminator = False
        def checkCell(board, rowInd, colInd, cell):
            if cell in board[colInd]: return False 
            for i in range(0, 9):
                if cell == board[i][rowInd]: return False 
            for c, r in product(range((colInd // 3) * 3, (colInd // 3 + 1) * 3),
                        range((rowInd // 3) * 3, (rowInd // 3 + 1) * 3)):
                if cell == board[c][r]: return False
            return True

        def backTrack(mockBoard, ind):
            nonlocal terminator
            rowInd, colInd = ind % 9, ind // 9
            if ind == 81:
                terminator = True; return
            if mockBoard[colInd][rowInd] != '.': 
                backTrack(mockBoard, ind + 1); return
            for cellOption in range(1, 10): 
                cellOption = str(cellOption)
                if checkCell(mockBoard, rowInd, colInd, cellOption):
                    mockBoard[colInd][rowInd] = cellOption 
                    backTrack(mockBoard, ind + 1)
                    if terminator: return; 
                    mockBoard[colInd][rowInd] = '.' 
        backTrack(board, 0)
        return board
