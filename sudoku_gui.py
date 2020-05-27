import tkinter as tk
import time, copy
import csv, random
from tkinter import messagebox as mb

class SudokuBoard():
        def __init__(self, level):
                self.level = level
                self.board = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
                self.solution = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
                self.__find_a_game(self.level)


        def __find_a_game(self, level):
                if level == 'empty':
                        question = '0'*81
                        sol = '0'*81
                else:
                        with open('sudoku.csv', 'r') as f:
                                r = csv.reader(f)
                                for i in range(random.randint(0, 4000)):
                                               next(r)
                                row = next(r)
                                question = row[0]
                                sol = row[1]
                                       
                self.__transform_question(question)
                self.__transform_solution(sol)

        def __transform_question(self, question):

                k = 0
                for i in range(9):
                        for j in range(9):
                                self.board[i][j] = int(question[k])
                                k += 1

        def __transform_solution(self, sol):

                k = 0
                for i in range(9):
                        for j in range(9):
                                self.solution[i][j] = int(sol[k])
                                k += 1
                                
                

class SudokuGUI():
    MARGIN = 10
    SQUARE = 50
    HEIGHT = WIDTH = MARGIN *2 + SQUARE * 9
    
    def __init__(self, board, parent):
        self.board = board
        self.board_copy = copy.deepcopy(board)
        self.solution = int('0'*81)
        self.parent = parent
        self.row = self.column = 0
        self.__initUI()
        

    def __initUI(self):
        self.defaultbg = self.parent.cget('bg')
        self.canvas = tk.Canvas(master = self.parent, width = self.WIDTH, height = self.HEIGHT)
        self.canvas.pack( fill = tk.BOTH, side = tk.TOP)        
        
        self.__initialgrid()
        self.initialfill(self.board, self.solution)

        self.canvas.bind('<Button-1>', self.__cell_clicked)
        self.canvas.bind('<Key>', self.__key_pressed)
        self.canvas.bind('<BackSpace>', self.__delete_cell)
        self.canvas.bind('<Delete>', self.__delete_cell)
        self.canvas.bind('<Return>', self.__press_enter)
        self.canvas.bind('<Tab>', self.__press_tab)
        
    def __initialgrid(self):
        for i in range(10):
            color = 'blue' if (i % 3 == 0) else 'grey'
            
            x0 = self.MARGIN + i * self.SQUARE
            y0 = self.MARGIN
            x1 = self.MARGIN + i * self.SQUARE 
            y1 = self.HEIGHT - self.MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill = color)
            
            x0 = self.MARGIN
            y0 = self.MARGIN + i * self.SQUARE
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i * self.SQUARE
            self.canvas.create_line(x0, y0, x1, y1, fill = color)

    def initialfill(self, board, solution):
            self.board_copy = copy.deepcopy(board)
            self.solution = solution
            self.canvas.delete('numbers')
            self.canvas.delete('solution')
            self.canvas.delete('click')
            self.canvas.delete('congrats')
            for i in range(9):
                    for j in range(9):
                            value = board[i][j]
                            if value != 0 :
                                    x = self.MARGIN + self.SQUARE / 2 + j * self.SQUARE
                                    y = self.MARGIN + self.SQUARE / 2 + i * self.SQUARE
                                    self.canvas.create_text(x, y, text = value, fill = 'black', font = 'Helvetica 10', tags = 'numbers')
                            else:
                                    x = self.MARGIN + self.SQUARE / 2 + j * self.SQUARE
                                    y = self.MARGIN + self.SQUARE / 2 + i * self.SQUARE
                                    self.entry = tk.Entry(text = '')
                                    self.entry.place(relx = x, rely = y)
                            
    def __cell_clicked(self, event):
           self.canvas.delete('click')
           
           x, y = event.x, event.y
           if (self.MARGIN < x < self.WIDTH - self.MARGIN)  and (self.MARGIN < y < self.HEIGHT - self.MARGIN):
                    self.canvas.focus_set()
                    row = (y - self.MARGIN) // self.SQUARE
                    column = (x - self.MARGIN) // self.SQUARE
                    self.row, self.column = row, column
                    
                    center_column = self.MARGIN + self.SQUARE * column + self.SQUARE / 2
                    center_row = self.MARGIN + self.SQUARE * row + self.SQUARE / 2
                    self.canvas.create_rectangle(center_column-self.SQUARE/2, center_row-self.SQUARE/2,
                                                 center_column+self.SQUARE/2, center_row+self.SQUARE/2, outline = 'red', tag = 'click')
                            
    def __key_pressed(self, event):
            if self.board[self.row][self.column] == 0:
                    self.board[self.row][self.column] = int(event.char)
                    center_column = self.MARGIN + self.SQUARE * self.column + self.SQUARE / 2
                    center_row = self.MARGIN + self.SQUARE * self.row + self.SQUARE / 2
                    self.canvas.create_text(center_column, center_row, text = event.char, fill = 'orange', font = 'Helvetica 15', tag = 'solution')
                    if self.gameover():
                        self.congratulations()

    def __delete_cell(self, event):
           x, y = event.x, event.y
           if (self.MARGIN < x < self.WIDTH - self.MARGIN)  and (self.MARGIN < y < self.HEIGHT - self.MARGIN):
                    row = (y - self.MARGIN) // self.SQUARE
                    column = (x - self.MARGIN) // self.SQUARE
                    
                    if self.board[row][column] != 0:
                            self.board[row][column] = 0
                            center_column = self.MARGIN + self.SQUARE * column + self.SQUARE / 2
                            center_row = self.MARGIN + self.SQUARE * row + self.SQUARE / 2
                            self.canvas.create_oval(center_column-10, center_row-10, center_column+10,
                                                    center_row+10, fill = self.defaultbg, outline = self.defaultbg)
    def __press_tab(self, event):
            self.canvas.delete('click')
            x, y = event.x, event.y
            if (self.MARGIN < x < self.WIDTH - self.MARGIN)  and (self.MARGIN < y < self.HEIGHT - self.MARGIN):
                    self.canvas.focus_set()
                    for i in range(9):
                            for j in range(9):
                                    if (i,j) > (self.row, self.column) and (self.board[i][j] == 0):
                                        self.row, self.column = i, j
                                        center_column = self.MARGIN + self.SQUARE * j + self.SQUARE / 2
                                        center_row = self.MARGIN + self.SQUARE * i + self.SQUARE / 2
                                        self.canvas.create_rectangle(center_column-self.SQUARE/2, center_row-self.SQUARE/2,
                                        center_column+self.SQUARE/2, center_row+self.SQUARE/2, outline = 'red', tag = 'click')
                                        return ('break')               
            
    def gameover(self):
            for i in range(9):
                    for j in range(9):
                            if self.board[i][j] != self.solution[i][j]:
                                    return False
            return True
            

    def congratulations(self):
            x_middle, y_middle = (self.MARGIN + self.SQUARE * 4 + self.SQUARE/2), (self.MARGIN + self.SQUARE * 4 + self.SQUARE/2)
            self.canvas.create_oval(x_middle-120, y_middle-120, x_middle+120, y_middle+120,
                                    fill = 'orange', outline = 'orange', tag = 'congrats')
            self.canvas.create_text(x_middle, y_middle, text = 'Congratulations', font = 'Helvetica 20 bold', fill = 'brown', tag = 'congrats')
        
    def __press_enter(self, event):
            if self.gameover():
                    self.congratulations()
                    
            for i in range(9):
                    for j in range(9):
                            if (self.board[i][j] != 0) and (self.board[i][j] != self.solution[i][j]):
                                    x = self.MARGIN + self.SQUARE / 2 + self.SQUARE * j
                                    y = self.MARGIN + self.SQUARE / 2 + self.SQUARE * i        
                                    self.canvas.create_oval(x-10, y-10, x+10, y+10, fill = self.defaultbg, outline = self.defaultbg)
                                    self.canvas.create_text((x-self.SQUARE/3), (y-self.SQUARE/3),
                                                            text = self.board[i][j], fill = 'orange', font = 'Helvetica 8', tags = 'solution')
                                    self.canvas.create_text(x, y, text = self.solution[i][j],
                                                            fill = 'sea green', font = 'Helvetica 18 bold', tags = 'solution')
                                    self.board[i][j] = self.solution[i][j]
        
    def solvegrid(self, i, j, value):
        x = self.MARGIN + self.SQUARE / 2 + self.SQUARE * j
        y = self.MARGIN + self.SQUARE / 2 + self.SQUARE * i 
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill = self.defaultbg, outline = self.defaultbg)
        self.canvas.create_text(x, y, text = value, fill = 'sea green', font = 'Helvetica 18 bold', tags = 'solution')
        self.parent.update()

    def clear_all(self):
       self.canvas.delete("solution")
       for i in range(9):
               for j in range(9):
                       self.board[i][j] = self.board_copy[i][j]
        
    def valid(self, board, i , j, k):
        if k in board[i]:
            return False
        for c in range(len(board)):
            if board[c][j] == k:
                return False
        box_hp = i // 3
        box_wp = j // 3
        
        for a in range(0,3):
            for b in range(0,3):
                if board[box_hp * 3 + a][box_wp * 3 + b] == k:
                    return False
        return True

    def find_null(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    return (i,j)
        
    def solve(self):
        self.canvas.delete('click')
        if self.gameover():
                self.congratulations()
        find = self.find_null(self.board)
        
        if find is None:
            return True
        else:
            i, j = find
            for k in range(1,10):
                if self.valid(self.board, i, j, k):
                    self.board[i][j] = k
                    self.solvegrid(i, j, k)
                    time.sleep(0.1)
                    if self.solve():
                        return True
                    
                    self.board[i][j] = 0
        
       
        return False                


def pick_board(level):
   
    if level == 'easy':
        game_board = SudokuBoard("easy")
    elif level == 'inter':
        game_board = SudokuBoard("inter")
    else:
       game_board = SudokuBoard("hard")

    game.board = game_board.board
    game.solution = game_board.solution
    game.initialfill(game.board, game.solution)
    root.update()

def pick_a_game_manually():
        pass

def about():
        mb_about = mb.showinfo('About', 'Sudoku is a game of 9x9 grid.')



if __name__ == '__main__':
        
        root = tk.Tk()
        root.title("Sudoku")

        menu = tk.Menu(root)
        root.config(menu = menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label = 'File', menu = filemenu)
        filemenu.add_command(label = 'About', command = about)
        filemenu.add_separator()
        filemenu.add_command(label = 'Exit', command = root.destroy)

        helpmenu= tk.Menu(menu)
        menu.add_cascade(label = 'Help', menu = helpmenu)
        helpmenu.add_command(label = 'Software', command = about)
        

        frame1 = tk.Frame(root)
        frame1.pack(side = tk.LEFT, expand = True)

        empty_board = SudokuBoard("empty")

        game = SudokuGUI(empty_board.board, frame1)

        frame2 = tk.Frame(root)       
        frame2.pack(side = tk.RIGHT, expand = True)
        btn_easy = tk.Button(frame2, text = 'Start a new game',  height = 1, width = 16, command = lambda: pick_board("easy"))
        btn_easy.pack()

        btn_clear = tk.Button(frame2, text = 'Clear Answers',  height = 1, width = 16, command = game.clear_all)
        btn_clear.pack()

        btn_solve = tk.Button(frame2, text = 'Solve Game',  height = 1, width = 16, command = game.solve)
        btn_solve.pack()



        root.mainloop()     
        
