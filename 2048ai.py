# -*- coding: utf-8 -*-
from Tkinter import *
from random import randint
from time import sleep
import unittest
import random
import tkFont
import sys
import time
import math
import copy
import itertools

MARGIN = 25 # Pixels around the board
SIDE = 75 # Width of every board cell.
WIDTH = MARGIN * 2 + SIDE * 4 # Width of the whole board
HEIGHT = WIDTH # height of the whole board

class Kernel(object):
    @staticmethod
    def move_down(myList):
        is_moved = False
        score = 0
        if isinstance(myList, list):
            size = len(myList)
            #auxiliarylist = [1] * size
            for i in reversed(xrange(size)):
                for j in reversed(xrange(size-1)):
                    if myList[j+1] == myList[j] and myList[j+1] != 0 :
                        myList[j+1] *= 2
                        score = score + myList[j+1]
                       # auxiliarylist[j+1] = 0
                        myList[j] = 0
                        #auxiliarylist[j] = 1
                        is_moved = True
                    if myList[j] != 0 and myList[j+1] == 0 : 
                        myList[j+1] = myList[j]
                        #auxiliarylist[j+1] = auxiliarylist[j]
                        myList[j] = 0
                        #auxiliarylist[j] = 1
                        is_moved = True
        else:
            print "is not list"
        return [is_moved, score]
    @staticmethod
    def rotate_listoflist(matrix):
        columns = [[row[col] for row in matrix] for col in range(len(matrix[1]))]
        return columns

class UI2048(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.parent = parent
        self.row, self.col = -1, -1
        self.initUI()
        
    def initUI(self):
        self.parent.title("2048")
        self.parent.resizable(0,0)
        self.frame = Frame()
        self.label_score = Label(self.frame, text=u"你的分数是:", font=tkFont.Font(family="Verdina", size=16))
        self.label = Label(self.frame, width=16, text="0", font=tkFont.Font(family="Verdina", size=16))
        self.label_score.pack(side=LEFT)
        self.label.pack(side=RIGHT)
        self.btn0 = Button(root, text=u"自动运行A", command=auto_A)
        self.btn1 = Button(root, text=u"自动运行B", command=auto_B)
        self.btn2 = Button(root, text=u"自动运行ai", command=auto_run)
        self.btn0.pack()
        self.btn1.pack()
        self.btn2.pack()
        self.canvas = Canvas(
            width=350, height=350,
            highlightthickness=0
        )
        self.canvas.pack(side=BOTTOM,expand=True, fill=BOTH)
        self.frame.pack()
        self.draw_grid(5)
        
    def draw_grid(self, amount):
        for i in xrange(amount):
            self.canvas.create_line(
                MARGIN + i * SIDE, MARGIN,
                MARGIN + i * SIDE, WIDTH - MARGIN,
                fill="red", tag="grid" 
            )
            self.canvas.create_line(
                MARGIN, MARGIN + i * SIDE,
                WIDTH - MARGIN, MARGIN + i * SIDE,
                fill="red", tag="grid"
            )

    def get_color(self,value):
        colors = ['#eee4da','#ede0c8','#f2b179','#f59563','#f67c5f','#f65e3b','#edcf72','#edcc61','#edc850','#edc53f','#edc22e','#edb018','#ea6004','#d04500','#c63500','#c03340','#b03060', '#a12a80']
        position = 0
        while True:
            if value != 1:
                value = value/2
                position = position + 1
                if position > len(colors):
                    return '#095aaa'
            else:
                return colors[position-1]
            
    def draw_puzzle(self, x, y, text):
        self.canvas.create_rectangle(
            MARGIN+SIDE*x,
            MARGIN+SIDE*y,
            MARGIN+SIDE*x+SIDE,
            MARGIN+SIDE*y+SIDE,
            width = 3,
            fill=self.get_color(text),
            tag="field"
        )
        self.canvas.create_text(
            MARGIN+37+SIDE*x,
            MARGIN+37+SIDE*y,
            font=("Verdina",14),
            text=text,
            tag="text"
        )
   
class Game2048(object):
    def __init__(self, object):
        self.ui = object
        self.fields = []
        self.is_moving_array = []
        self.score = 0
        for i in xrange(4):
            self.fields.append([0] * 4)
        for i in xrange(4):
            self.is_moving_array.append([0] * 4)
        self.new_random_puzzle(self.fields)
        #self.new_random_puzzle(self.fields)
        self.refresh_screen()
        self.press_key()
        
    def refresh_screen(self):
        self.ui.canvas.delete("field")
        self.ui.canvas.delete("text")
        self.ui.label['text'] = self.score
        sizeof = len(self.fields)
        for i in xrange(sizeof):
            for j in xrange(sizeof):
                if self.fields[i][j] != 0:
                    self.ui.draw_puzzle(i, j, self.fields[i][j])

    def check_end_of_game(self):
        size = len(self.fields)
        for i in xrange(size):
            for j in xrange(size):
                if self.fields[i][j] == 0:
                    return 0
        for i in xrange(size):
            for j in xrange(size-1):
                if self.fields[i][j] == self.fields[i][j+1]:
                    return 0
        for i in xrange(size-1):
            for j in xrange(size):
                if self.fields[i][j] == self.fields[i+1][j]:
                    return 0             
        return 1

    def new_random_puzzle(self, object):
        self.array_puzzle = object
        p = 0.1
        while True:
            rand_field = randint(0,15)
            if self.array_puzzle[rand_field%4][rand_field/4] == 0:
                x = random.random()
                if x < p:
                    self.array_puzzle[rand_field%4][rand_field/4] = 4
                else:
                    self.array_puzzle[rand_field%4][rand_field/4] = 2
                break

    def pressed_left(self, event):
        is_moved = False
        self.fields.reverse()
        temp_fields = Kernel.rotate_listoflist(self.fields)
        for i in xrange(4):
            result = Kernel.move_down(temp_fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields = Kernel.rotate_listoflist(temp_fields)
            self.fields.reverse()
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)

    def pressed_right(self, event):
        is_moved = False
        temp_fields = Kernel.rotate_listoflist(self.fields)
        for i in xrange(4):
            result = Kernel.move_down(temp_fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields = Kernel.rotate_listoflist(temp_fields)
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)

    def pressed_up(self, event):
        is_moved = False
        for i in xrange(4):
            self.fields[i].reverse()
            result = Kernel.move_down(self.fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
            self.fields[i].reverse()
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)

    def pressed_down(self, event):
        is_moved = False
        for i in xrange(4):
            result = Kernel.move_down(self.fields[i])
            if result[0]:
                is_moved = True
                self.score = self.score + result[1]
        if is_moved:
            self.new_random_puzzle(self.fields)
            self.refresh_screen()
            if self.check_end_of_game():
                self.end_game(self.score)

    def press_key(self):
        self.ui.canvas.focus_set()
        self.ui.canvas.bind('<Left>', self.pressed_left)
        self.ui.canvas.bind('<Right>', self.pressed_right)
        self.ui.canvas.bind('<Up>', self.pressed_up)
        self.ui.canvas.bind('<Down>', self.pressed_down)

    def end_game(self, score):
        tk =    Tk()
        tk.title("Game over")
        msg = Message(tk, text=u"最终得分" + str(self.score))
        msg.pack()
        button = Button(tk, text=u"退出", command=root.destroy)
        button.pack()
        canvas = Canvas(tk,width=50,height=40,bd=0)
        canvas.pack()

    def get_current_status(self):
        return self.fields

    def get_len_of_fields(self):
        return len(self.fields)

    def get_the_number_of_cells(self):
        num=0
        for i in range(0,4):
            for j in range(0,4):
                if self.fields[i][j]!=0:
                    num=num+1
        return num

    def get_cells(self):
        listofcell=[]
        for i in range(0,4):
            for j in range(0,4):
                listofcell.append(self.fields[i][j])
        return listofcell




class Board(object):
    """
    A 2048 board
    """

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    GOAL = 204800
    SIZE = 4

    def __init__(self, goal=GOAL, size=SIZE, **kws):
        self.__size = size
        self.__size_range = xrange(0, self.__size)
        self.__goal = goal
        self.__won = False
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()

    def set_cell_contents(self,l2048):
        self.cells = l2048
    def size(self):
        """return the board size"""
        return self.__size

    def goal(self):
        """return the board goal"""
        return self.__goal

    def won(self):
        """
        return True if the board contains at least one tile with the board goal
        """
        return self.__won

    def maxValue(self):
        """
        return the max value in the board
        """
        maxVal = 0
        for y in self.__size_range:
            for x in self.__size_range:
                maxVal = max(self.getCell(x,y),maxVal)
        return maxVal

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in self.__size_range:
            for x in self.__size_range:
                c = self.getCell(x, y)
                if (x < self.__size-1 and c == self.getCell(x+1, y)) \
                        or (y < self.__size-1 and c == self.getCell(x, y+1)):
                    return True

        return False

    def validMove(self, dir):
        """
        test if a move is possible
        """
        if dir == self.UP or dir == self.DOWN:
            for x in self.__size_range:
                col = self.getCol(x)
                for y in self.__size_range:
                    if(y < self.__size-1 and col[y] == col[y+1] and col[y]!=0):
                        return True
                    if(dir == self.DOWN and y > 0 and col[y] == 0 and col[y-1]!=0):
                        return True
                    if(dir == self.UP and y < self.__size-1 and col[y] == 0 and col[y+1]!=0):
                        return True        
        
        if dir == self.LEFT or dir == self.RIGHT:
            for y in self.__size_range:
                line = self.getLine(y)
                for x in self.__size_range:
                    if(x < self.__size-1 and line[x] == line[x+1] and line[x]!=0):
                        return True
                    if(dir == self.RIGHT and x > 0 and line[x] == 0 and line[x-1]!=0):
                        return True
                    if(dir == self.LEFT and x < self.__size-1 and line[x] == 0 and line[x+1]!=0):
                        return True        
        return False

    def filled(self):
        """
        return true if the game is filled
        """
        return len(self.getEmptyCells()) == 0

    def addTile(self, value=None, choices=([2]*9+[4])):
        """
        add a random tile in an empty cell
          value: value of the tile to add.
          choices: a list of possible choices for the value of the tile.
                   default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def setCell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def getLine(self, y):
        """return the y-th line, starting at 0"""
        return self.cells[y]

    def getCol(self, x):
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in self.__size_range]

    def setLine(self, y, l):
        """set the y-th line, starting at 0"""
        self.cells[y] = l[:]

    def setCol(self, x, l):
        """set the x-th column, starting at 0"""
        for i in xrange(0, self.__size):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """return a (x, y) pair for each empty cell"""
        return [(x, y) for x in self.__size_range
                           for y in self.__size_range if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Board.LEFT or d == Board.UP):
            inc = 1
            rg = xrange(0, self.__size-1, inc)
        else:
            inc = -1
            rg = xrange(self.__size-1, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                if v == self.__goal:
                    self.__won = True

                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def move(self, d, add_tile=True):
        """
        move and return the move score
        """
        if d == Board.LEFT or d == Board.RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == Board.UP or d == Board.DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return 0

        moved = False
        score = 0

        for i in self.__size_range:
            # save the original line/col
            origin = get(i)
            # move it
            line = self.__moveLineOrCol(origin, d)
            # merge adjacent tiles
            collapsed, pts = self.__collapseLineOrCol(line, d)
            # move it again (for when tiles are merged, because empty cells are
            # inserted in the middle of the line/col)
            new = self.__moveLineOrCol(collapsed, d)
            # set it back in the board
            chg(i, new)
            # did it change?
            if origin != new:
                moved = True
            score += pts

        # don't add a new tile if nothing changed
        if moved and add_tile:
            self.addTile()

        return score
class AI(object):
    def __str__(self, margins={}):
        return ""
        

    @staticmethod
    def randomNextMove(board):
        '''
        It's just a test for the validMove function
        '''
        if board.validMove(Board.UP):
            print ("UP: ok")
        else:
            print ("UP: no")
        if board.validMove(Board.DOWN):
            print ("DOWN: ok")
        else:
            print ("DOWN: no")
        if board.validMove(Board.LEFT):
            print ("LEFT: ok")
        else:
            print ("LEFT: no")
        if board.validMove(Board.RIGHT):
            print ("RIGHT: ok")
        else:
            print ("RIGHT: no")
        rm = random.randrange(1, 5)
        print rm 
        return rm
    
    @staticmethod
    def nextMove(board,recursion_depth=3):
        m,s = AI.nextMoveRecur(board,recursion_depth,recursion_depth)
        return m
        
    @staticmethod
    def nextMoveRecur(board,depth,maxDepth,base=0.9):
        bestScore = -1.
        bestMove = 0
        for m in range(1,5):
            if(board.validMove(m)):
                newBoard = copy.deepcopy(board)
                newBoard.move(m,add_tile=False)
                
                score, critical = AI.evaluate(newBoard)
                newBoard.setCell(critical[0],critical[1],2)
                if depth != 0:
                    my_m,my_s = AI.nextMoveRecur(newBoard,depth-1,maxDepth)
                    score += my_s*pow(base,maxDepth-depth+1)
                
                if(score > bestScore):
                    bestMove = m
                    bestScore = score
        return (bestMove,bestScore);

    #Hey!!! Don't judge me for this awful piece of code!!!
    #It's just a quick test...
    @staticmethod
    def evaluate(board,commonRatio=0.25):
        linearWeightedVal = 0
        invert = False
        weight = 1.
        malus = 0
        criticalTile = (-1,-1)
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                b_y = y
                if invert:
                    b_x = board.size() - 1 - x
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile == (-1,-1)):
                    criticalTile = (b_x,b_y)
                linearWeightedVal += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        linearWeightedVal2 = 0
        invert = False
        weight = 1.
        malus = 0
        criticalTile2 = (-1,-1)
        for x in range(0,board.size()):
            for y in range(0,board.size()):
                b_x = x
                b_y = y
                if invert:
                    b_y = board.size() - 1 - y
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile2 == (-1,-1)):
                    criticalTile2 = (b_x,b_y)
                linearWeightedVal2 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        
        linearWeightedVal3 = 0
        invert = False
        weight = 1.
        malus = 0
        criticalTile3 = (-1,-1)
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                b_y = board.size() - 1 - y
                if invert:
                    b_x = board.size() - 1 - x
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile3 == (-1,-1)):
                    criticalTile3 = (b_x,b_y)
                linearWeightedVal3 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        linearWeightedVal4 = 0
        invert = False
        weight = 1.
        malus = 0
        criticalTile4 = (-1,-1)
        for x in range(0,board.size()):
            for y in range(0,board.size()):
                b_x = board.size() - 1 - x
                b_y = y
                if invert:
                    b_y = board.size() - 1 - y
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile4 == (-1,-1)):
                    criticalTile4 = (b_x,b_y)
                linearWeightedVal4 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
            
        linearWeightedVal5 = 0
        invert = True
        weight = 1.
        malus = 0
        criticalTile5 = (-1,-1)
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                b_y = y
                if invert:
                    b_x = board.size() - 1 - x
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile5 == (-1,-1)):
                    criticalTile5 = (b_x,b_y)
                linearWeightedVal5 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        linearWeightedVal6 = 0
        invert = True
        weight = 1.
        malus = 0
        criticalTile6 = (-1,-1)
        for x in range(0,board.size()):
            for y in range(0,board.size()):
                b_x = x
                b_y = y
                if invert:
                    b_y = board.size() - 1 - y
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile6 == (-1,-1)):
                    criticalTile6 = (b_x,b_y)
                linearWeightedVal6 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        
        linearWeightedVal7 = 0
        invert = True
        weight = 1.
        malus = 0
        criticalTile7 = (-1,-1)
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                b_y = board.size() - 1 - y
                if invert:
                    b_x = board.size() - 1 - x
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile7 == (-1,-1)):
                    criticalTile7 = (b_x,b_y)
                linearWeightedVal7 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        linearWeightedVal8 = 0
        invert = True
        weight = 1.
        malus = 0
        criticalTile8 = (-1,-1)
        for x in range(0,board.size()):
            for y in range(0,board.size()):
                b_x = board.size() - 1 - x
                b_y = y
                if invert:
                    b_y = board.size() - 1 - y
                #linearW
                currVal=board.getCell(b_x,b_y)
                if(currVal == 0 and criticalTile8 == (-1,-1)):
                    criticalTile8 = (b_x,b_y)
                linearWeightedVal8 += currVal*weight
                weight *= commonRatio
            invert = not invert
            
        maxVal = max(linearWeightedVal,linearWeightedVal2,linearWeightedVal3,linearWeightedVal4,linearWeightedVal5,linearWeightedVal6,linearWeightedVal7,linearWeightedVal8)
        if(linearWeightedVal2 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal2
            criticalTile = criticalTile2
        if(linearWeightedVal3 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal3
            criticalTile = criticalTile3
        if(linearWeightedVal4 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal4
            criticalTile = criticalTile4
        if(linearWeightedVal5 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal5
            criticalTile = criticalTile5
        if(linearWeightedVal6 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal6
            criticalTile = criticalTile6
        if(linearWeightedVal7 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal7
            criticalTile = criticalTile7
        if(linearWeightedVal8 > linearWeightedVal):
            linearWeightedVal = linearWeightedVal8
            criticalTile = criticalTile8
        
        return maxVal,criticalTile



def auto_A():
    current_status=game.get_current_status()
    for x in range(0,15):
        for m in range(0,100):
            temp_fields = Kernel.rotate_listoflist(current_status)
            for i in xrange(4):
                #temp_fields = Kernel.rotate_listoflist(current_status)
                down = Kernel.move_down(current_status[i])
                right = Kernel.move_down(temp_fields[i])
                left = Kernel.move_down(temp_fields[i])
                time.sleep(0.5)
                if(down[0] or right[0]):
                    game.pressed_up(game)
                    game.pressed_right(game)
                else :
                    game.pressed_down(game)
                    game.pressed_left(game)
                root.update()

def auto_B():
    #print 'test succuess!'

    for j in range(0,9999):
        #print 'times : ',j
        four_directions=[]
        current_status=game.get_current_status()
        #print current_status
        up_score=0
        down_score=0
        left_score=0
        right_score=0
        #up
        for i in xrange(4):
            current_status[i].reverse()
            up = Kernel.move_down(current_status[i])
            current_status[i].reverse()
            if up[0]:
                up_score = up_score + up[1]
        #down
        for i in xrange(4):
            down = Kernel.move_down(current_status[i])
            if down[0]:
                down_score = down_score + down[1]
        #left
        # current_status[i].reverse()
        # print current_status[i]
        temp_fields = Kernel.rotate_listoflist(current_status)
        for i in xrange(4):
            left = Kernel.move_down(temp_fields[i])
            if left[0]:
                left_score = left_score + left[1]
            current_status = Kernel.rotate_listoflist(temp_fields)
            current_status.reverse()
        #right
        temp_fields = Kernel.rotate_listoflist(current_status)
        for i in xrange(4):
            right = Kernel.move_down(temp_fields[i])
            if right[0]:
                right_score = right_score + right[1]
            current_status = Kernel.rotate_listoflist(temp_fields)
        four_score=[up_score,down_score,left_score,right_score]
        choose = four_score.index(max(four_score))
        time.sleep(0.5)
        if four_score[choose] == 0:
            choose = random.randint(0,3)
        if(choose == 1):
            game.pressed_down(game)
        if(choose == 0 ):
            game.pressed_up(game)
        if(choose == 3):
            game.pressed_right(game)
        if(choose ==2):
            game.pressed_left(game)
        root.update()
        
def auto_run():

    print 'test succuess!'
    board = Board()
    myai = AI()
    while  True:
        l2048 = Kernel.rotate_listoflist(game.get_current_status())
        
        board.set_cell_contents(l2048)
        
        move_dir = myai.nextMove(board)

        if move_dir == 1 :
            game.pressed_up(game)
        if move_dir == 2 :
            game.pressed_down(game)
        if move_dir == 3 :
            game.pressed_left(game)
        if move_dir == 4 :
            game.pressed_right(game)
        time.sleep(0.05)
        root.update()

    # print game.get_len_of_fields()
    # print game.get_the_number_of_cells()
    #for i in range(0,100):
     #   game.pressed_down(game)
        
root = Tk()
ui = UI2048(root)
game = Game2048(ui)


    
if __name__ == '__main__':
    #unittest.main()  
    root.mainloop()
