from tkinter import *
from tkinter import filedialog
from functools import partial
from solution import *
import copy


# convert 2D board to 1D for easier manipulation (also remove 0)
def flatten(board):
    board_1D = []

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 0:
                board_1D.append(board[i][j])
        
    return board_1D


# checked if won then prompt the user if true
def hasWon(board, cells,  prompt):
    board_1D = flatten(board)

    for i in range(1, len(board_1D)):
        if board_1D[i] < board_1D[i-1]:
            return False
    
    # the 0 tile should be placed at the end of the board
    if cells[len(cells)-1][len(cells)-1].cget('text') != "":
        return False

    for i in range(len(cells)):
        for j in range(len(cells)):
            if i != len(cells)-1 or j != len(cells)-1:
                cells[i][j].config(bg="gray", activebackground="gray", command="")
            
    prompt.config(text="YOU WON!", fg="green", font="helvetica 10 bold", wraplength=200)

    return True
    

# move function, call when tiles/cells are clicked
def move(board, cell, cells, prompt):
    row = cell.grid_info()['row']
    col = cell.grid_info()['column']

    # check for the adjacent tiles. If there are no 0 tiles: do nothing,
    # else: swap the position of the clicked tile and the 0 tile, both in gui and in board array
    Xs = [0, 1, 0, -1]
    Ys= [-1, 0, 1, 0]
    for i in range(4):
        adj_x = row + Xs[i]
        adj_y = col + Ys[i]
        if adj_x < 0 or adj_x >= len(board) or adj_y < 0 or adj_y >= len(board[0]):
            continue
        if board[adj_x][adj_y] == 0:
            board[adj_x][adj_y] = board[row][col]
            board[row][col] = 0
            cells[row][col].grid(row=adj_x, column=adj_y)
            cells[adj_x][adj_y].grid(row=row, column=col)
            cells[row][col], cells[adj_x][adj_y] = cells[adj_x][adj_y], cells[row][col]
            break
    
    # check if the player has won
    hasWon(board, cells, prompt)


# check if the 8 puzzle is solvable or not
def isSolvable(board):
    board_1D = flatten(board)
    n_inversions = 0
    
    for i in range(1, len(board_1D)):
        for j in range(i-1, -1, -1):
            if board_1D[i] < board_1D[j]:
                n_inversions += 1
    
    if n_inversions % 2 == 0:
        return True
    return False


def boardInput(board):
    for i in range(3):
        input_vals = list(map(int, input().split()))
        board.append(input_vals)


def boardSetUp(root, board):
    root.geometry("282x500")

    cells = []
    is_solvable = "Solvable. You can do this!" if isSolvable(board) else "Not solvable. \n No matter How hard you try."

    prompt = Label(root, text=is_solvable, fg="gray", font="helvetica 10 bold")
    prompt.grid(row=3, column=0, columnspan=3, pady=10)


    # loop through the board and create a widget for each element
    # also add all the widgets in the cells array to store each widget identities
    for i in range(len(board)):
        row_board = []
        for j in range(len(board[1])):
            if board[i][j] != 0:
                cell = Button(root, text=board[i][j], padx=20, pady=20, highlightthickness=5, activebackground= "lightblue", bg="lightblue", fg="black", font=('helvetica 25 bold'))
                cell.config(command=partial(move, board, cell, cells, prompt))
                row_board.append(cell)
                cell.grid(row=i, column=j)
            else:
                cell = Label(root, text="", padx=40, pady=40)
                row_board.append(cell)
                cell.grid(row=i, column=j)
        cells.append(row_board)
        row_board = []

    fileSelect = Button(root, text="Select File", command=lambda: selectFile(root, board))
    fileSelect.grid(row=4, column=0, ipadx=8, padx=0)


# resets the board
def reset(root, board, arg):
    widgets = root.winfo_children()

    for i in range(len(widgets)):
        widgets[i].destroy()

    initBoard = copy.deepcopy(board)
    
    boardSetUp(root, board)

    # if arg is string, it means that the cause of reset is that the user picked a different solution from the dropdown
    # else, if the arg is boolean, the cause of reset is that the user picked a different file/puzzle board
    if type(arg) is str:
        solutionChange(root, initBoard, arg)
    else:
        solutionGUIsetup(root, initBoard, arg)


# select different puzzle board
def selectFile(root, board):
    root.filename = filedialog.askopenfilename(initialdir="./puzzles", title="Select A File", filetypes=(("in files", "*.in"), ("all files", "*.*")))

    board = []

    for line in open(root.filename):
        boardRow = list(map(int, line.strip().split()))
        board.append(boardRow)

    # reset the board
    reset(root, board, isSolvable(board))

# when the user picked another solution
def callback(root, board, choice, *args):
    reset(root, board, choice)

# add drop down and solution button
def solutionGUIsetup(root, initBoard, isSolvable):
    options = ["BFS", "DFS", "A*Search"]
    clicked = StringVar()
    clicked.set(options[0])


    dropdown = OptionMenu(root, clicked, *options)
    dropdown.grid(row=4, column=1, columnspan=1, ipadx=0, pady=2, sticky=EW)

    solutionBtn = Button(root, text="Solution", command=lambda: solve(root, clicked.get(), initBoard))
    solutionBtn.grid(row=4, column=2, ipadx=12, ipady=1, pady=5)

    clicked.trace('w', lambda *args: callback(root, initBoard, clicked.get(), *args))

    if not isSolvable:
        dropdown.config(state=DISABLED)
        solutionBtn.config(state=DISABLED)

# solution GUI set up after the user picked a new/different solution
def solutionChange(root, initBoard, choice):
    options = ["BFS", "DFS", "A*Search"]
    clicked = StringVar()
    clicked.set(choice)

    clicked.trace('w', lambda *args: callback(root, initBoard, clicked.get(), *args))

    dropdown = OptionMenu(root, clicked, *options)
    dropdown.grid(row=4, column=1, columnspan=1, ipadx=0, pady=2, sticky=EW)

    solutionBtn = Button(root, text="Solution", command=lambda: solve(root, clicked.get(), initBoard))
    solutionBtn.grid(row=4, column=2, ipadx=12, ipady=1, pady=5)

    
    






