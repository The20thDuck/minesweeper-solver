# Should separate program into game and solver. 
# Game functions: getBoard(), click(int col, int row)
# getBoard(): returns visible board. -1 = unopened. 0..8 = # of surrounding bombs.
# click(int col, int row) returns true for safe, false for bomb. updates board by expanding in all 8 directions recursively.
# Solver functions: 

import random
from copy import copy, deepcopy

class Game:
    def __init__(self, numCols, numRows, numMines):
        self.initialized = False
        self.numCols = numCols
        self.numRows = numRows
        self.numMines = numMines
        self.isFinished = False
        self.numRevealed = 0
        self.mines = [[0 for j in range(numRows)] for i in range(numCols)]
        self.fullBoard = [[0 for j in range(numRows)] for i in range(numCols)]
        self.board = [[-1 for j in range(numRows)] for i in range(numCols)]

    def getBoard(self):
        return deepcopy(self.board)

    def getFinished(self):
        return self.isFinished

    def click(self, col, row):
        # if not clicked yet, initialize      
        if (not self.initialized):
            minesLeft = self.numMines
            spacesLeft = self.numCols*self.numRows-1
            for i in range(self.numCols):
                for j in range(self.numRows):
                    if (i == col and row == j):
                        continue
                    r = random.randint(1, spacesLeft)
                    if (r <= minesLeft):
                        self.mines[i][j] = 1
                        minesLeft -= 1
                    spacesLeft -= 1
            dirs = [-1, 0, 1]
            for i in range(self.numCols):
                for j in range(self.numRows):
                    for c in dirs:
                        for r in dirs:
                            if (not(c==0 and r==0) and i+c >= 0 and i+c < self.numCols and j+r >= 0 and j+r < self.numRows and self.mines[i+c][j+r] == 1):
                                self.fullBoard[i][j] += 1
            self.initialized = True

        # If unseen and mine, return False
        # If unseen and 0, recurse on neighbors, return True.
        # If unseen and >0, return True
        # If seen, return True
        dirs = [-1, 0, 1]
        if (self.board[col][row] == -1):
            if (self.mines[col][row] == 1):
                print ("fail")
                self.isFinished = True
                return False
            self.numRevealed += 1
            if (self.numRevealed == self.numCols*self.numRows-self.numMines):
                print ("wow")
                self.isFinished = True
            if (self.fullBoard[col][row] == 0):
                self.board[col][row] = 0
                for c in dirs:
                    for r in dirs:
                        if (not(c==0 and r==0) and col+c >= 0 and col+c < self.numCols and row+r >= 0 and row+r < self.numRows):
                            self.click(col+c, row+r)
            else:
                self.board[col][row] = self.fullBoard[col][row]
            return True
        else:
            return True

def printArr(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print((3-len(str(a[i][j])))*" ", end = '')
            print(a[i][j], end = '')
        print('')
    print ('')

numCols = 10
numRows = 10
numFlags = 6
g = Game(numCols, numRows, numFlags)

# strategy: click in the middle. 
# Data structures: 2D array of mines, array of border squares
# Find "border" squares. For each border square, 
#                       1) if # open spots + # mines == board, fill with open spots with mines.
#                       2) if # mines == board, click open spots
""" a = g.getBoard()
a[0][0] = 12
print (g.getBoard()) """

g.click(numCols//2, numRows//2)
clickQueue = set(())
mines = [[0 for j in range(numRows)] for i in range(numCols)]
dirs = [-1, 0, 1]

count = 0
print (g.getFinished())
while (not g.getFinished() and count < 4):
    count += 1
    if (clickQueue): 
        for val in clickQueue:
            print (val[0], val[1])
            g.click(val[0], val[1])
        clickQueue = set(())
        continue
    board = g.getBoard()
    openSpots = [[0 for j in range(numRows)] for i in range(numCols)]
    mineSpots = [[0 for j in range(numRows)] for i in range(numCols)]
    borderSquares = []
    for i in range(numCols):
        for j in range(numRows):
            isBorder = False
            for c in dirs:
                for r in dirs:
                    if (not(c==0 and r==0) and i+c >= 0 and i+c < numCols and j+r >= 0 and j+r < numRows):
                        if board[i+c][j+r] == -1:
                            openSpots[i][j] += 1
                            if (board[i][j] != -1):
                                isBorder = True
                        if mines[i+c][j+r] == 1:
                            mineSpots[i][j] += 1
            if (isBorder):
                borderSquares.append([i, j])
    for sqr in borderSquares:
        i = sqr[0]
        j = sqr[1]
        if openSpots[i][j] + mineSpots[i][j] == board[i][j]: #flag mines
            for c in dirs:
                for r in dirs:
                    if (not(c==0 and r==0) and i+c >= 0 and i+c < numCols and j+r >= 0 and j+r < numRows):
                        if board[i+c][j+r] == -1:
                            mines[i+c][j+r] = 1
        if mineSpots[i][j] == board[i][j]: #click
            for c in dirs:
                for r in dirs:
                    if (not(c==0 and r==0) and i+c >= 0 and i+c < numCols and j+r >= 0 and j+r < numRows):
                        if board[i+c][j+r] == -1 and mines[i+c][j+r] != 1:
                            clickQueue.add(tuple([i+c, j+r]))
    printArr (board)
    #printArr (openSpots)
    #printArr (mineSpots)
    #printArr (borderSquares)
    print (clickQueue)
    print (g.getFinished())



printArr(g.getBoard())