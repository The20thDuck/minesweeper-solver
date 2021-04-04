import pyautogui
from time import sleep


from matplotlib import pyplot as plt

import numpy as np
import cv2 as cv
from mss import mss
from PIL import Image

def printArr(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            print((3-len(str(a[i][j])))*" ", end = '')
            print(a[i][j], end = '')
        print('')
    print ('')

class Game:
    def __init__(self, numCols, numRows, boxSide):
        self.boxSide = boxSide
        self.numCols = numCols
        self.numRows = numRows
        self.method = eval('cv.TM_SQDIFF')
        mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        sct = mss()
        sct.get_pixels(mon)
        template = Image.frombytes('RGB', (sct.width, sct.height), sct.image).convert("L")
        template = np.array(template)
        w, h = template.shape[::-1]
        corner = cv.imread('corner.png', 0)
        corner2 = corner.copy()
            

        corner = corner2.copy()
        # Apply template Matching
        res = cv.matchTemplate(corner,template,self.method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        self.top_left = min_loc
        print (self.top_left)

    def getFinished(self):
        return False

    def getBoard(self):
        pyautogui.moveTo(self.top_left[0]-15, self.top_left[1]+45, )
        sleep(0.2)
        zero = cv.imread('zero.png')
        zero = cv.cvtColor(zero, cv.COLOR_BGR2RGB)
        one = cv.imread('one.png')
        one = cv.cvtColor(one, cv.COLOR_BGR2RGB)
        two = cv.imread('two.png')
        two = cv.cvtColor(two, cv.COLOR_BGR2RGB)
        three = cv.imread('three.png')
        three = cv.cvtColor(three, cv.COLOR_BGR2RGB)
        four = cv.imread('four.png')
        four = cv.cvtColor(four, cv.COLOR_BGR2RGB)
        five = cv.imread('five.png')
        five = cv.cvtColor(five, cv.COLOR_BGR2RGB)
        six = cv.imread('six.png')
        six = cv.cvtColor(six, cv.COLOR_BGR2RGB)

        mon = {'top': self.top_left[1]+65, 'left': self.top_left[0]-5, 'width': int(self.boxSide*self.numRows), 'height': int(self.boxSide*self.numCols)}
        sct = mss()
        sct.get_pixels(mon)
        template = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        template = np.array(template)
        # w, h = template.shape[::-1]

        board = [[-1 for j in range(self.numRows)] for i in range(self.numCols)]

        nums = [zero, one, two, three, four, five, six]
        thresh = [1000000, 2500000, 2000000, 2000000, 2000000, 1000000, 2000000]
        for x in range(len(nums)):
            res = cv.matchTemplate(nums[x], template, self.method)
            loc = np.where (res <= thresh[x])
            for pt in zip(*loc[::-1]):
                i = int(pt[1]/self.boxSide)
                j = int(pt[0]/self.boxSide)
                board[i][j] = x
        return board

    def click(self, col, row):
        pyautogui.click(self.top_left[0]+5+self.boxSide*row, self.top_left[1]+75+self.boxSide*col)



boxSide = 37.5
numCols = 14
numRows = 18


'''
import opencv
a = opencv.Game(14, 18, 37.5)
a.click(5, 2)
'''

g = Game(numCols, numRows, boxSide)

g.click(numCols//2, numRows//2)
sleep(1)
clickQueue = set(())
mines = [[0 for j in range(numRows)] for i in range(numCols)]
dirs = [-1, 0, 1]

count = 0
noQ = 0
print (g.getFinished())
while (not g.getFinished() and count < 70):
    sleep(.1)
    count += 1
    if (clickQueue): 
        noQ = 0
        for val in clickQueue:
            print (val[0], val[1])
            g.click(val[0], val[1])
        clickQueue = set(())
        continue
    else:
        noQ += 1
        if noQ == 3:
            mines = [[0 for j in range(numRows)] for i in range(numCols)]
            noQ = 0
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


printArr(g.getBoard())
