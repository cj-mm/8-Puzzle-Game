from tkinter import *
from tkinter import messagebox
import copy

# reset the board to its initial arrangement
def resetBoard(root, cells, initBoard):
    for i in range(len(initBoard)):
        row_board = []
        for j in range(len(initBoard[1])):
            if initBoard[i][j] != 0:
                cell = Button(root, text=initBoard[i][j], padx=20, pady=20, highlightthickness=5, activebackground= "lightblue", bg="lightblue", fg="black", font=('helvetica 25 bold'))
                row_board.append(cell)
                cell.grid(row=i, column=j)
            else:
                cell = Label(root, text="", padx=40, pady=40)
                row_board.append(cell)
                cell.grid(row=i, column=j)
        cells.append(row_board)
        row_board = []

# allows the user to see the solution
def solve(root, algo, initBoard):
    cells = []
    widgets = root.winfo_children()

    # destroy the current board before reset
    for i in range(1, len(initBoard)*len(initBoard)+1):
        widgets[i].destroy()

    resetBoard(root, cells, initBoard)

    if algo == "BFS":
        solution = BFS(initBoard)
    elif algo == "DFS":
        solution = DFS(initBoard)
    else:
        solution = AStar(initBoard)

    # write the solution to puzzle.out
    with open('puzzle.out', 'w') as out:
        out.write(' '.join(solution))
    
 
    solutionTxt = Label(root, text=solution, fg="gray", font="helvetica 10 bold", wraplength=130, justify=LEFT)
    solutionTxt.grid(row=5, column=0, columnspan=3, pady=10)

    # for the moves caused by clicking the next button
    moves = Label(root, text="", fg="black", font="helvetica 10 bold", wraplength=130)
    moves.grid(row=5, column=0, columnspan=2, pady=10, sticky=NW)
    moves_done = []

    # solution button and the dropdown are the last two widgets in windows
    solutionBtn = widgets[len(widgets)-1]
    dropDown = widgets[len(widgets)-2]
    solutionBtn.config(text="Next", command=lambda: next(root, cells, solution, moves_done))
    # dropDown.config(state=DISABLED)
    

# will move the tile depending on the pop element in the solution array (U, D, R, or L)
def next(root, cells, solution, moves_done):
    widgets = root.winfo_children()

    emptyTile = findEmptyTile(cells)
    emptyRow = emptyTile[0]
    emptyCol = emptyTile[1]

    move = solution.pop(0)
    moves_done.append(move)

    # configure the current last two widgets (solution labels)
    widgets[len(widgets)-1].config(text=moves_done)
    widgets[len(widgets)-2].config(text=solution)
    widgets[len(widgets)-2].grid(row=5, column=1, columnspan=2, pady=10, sticky=NE)

    if move == "U":
        newEmpRow = emptyRow-1
        newEmpCol = emptyCol
    elif move == "R":
        newEmpRow = emptyRow
        newEmpCol = emptyCol+1
    elif move == "D":
        newEmpRow = emptyRow+1
        newEmpCol = emptyCol
    elif move == "L":
        newEmpRow = emptyRow
        newEmpCol = emptyCol-1
    
    # Swap
    cells[emptyRow][emptyCol].grid(row=newEmpRow, column=newEmpCol)
    cells[newEmpRow][newEmpCol].grid(row=emptyRow, column=emptyCol)
    cells[emptyRow][emptyCol], cells[newEmpRow][newEmpCol] = cells[newEmpRow][newEmpCol], cells[emptyRow][emptyCol]

    # change the GUI and prompt the user about the path cost
    if len(solution) == 0:
        for i in range(len(cells)):
            for j in range(len(cells)):
                if i != len(cells)-1 or j != len(cells)-1:
                    cells[i][j].config(bg="gray", activebackground="gray", command="")

        # widgets array starts with the children right after the buttons that were destroyed
        widgets[0].config(text="YOU WON!", fg="green", font="helvetica 10 bold")
        widgets[3].config(state=DISABLED)
        widgets[len(widgets)-1].grid(row=5, column=0, columnspan=3, pady=10, sticky="")
        messagebox.showinfo("Information Dialog", "Path Cost: " + str(len(moves_done)))

# find empty tile (for board array of int, or the board array of widgets)
def findEmptyTile(initBoard):
    empty_tile = []

    for i in range(len(initBoard)):
        for j in range(len(initBoard)):
            if type(initBoard[0][0]) is int:
                if initBoard[i][j] == 0:
                    empty_tile.append(i)
                    empty_tile.append(j)
                    return empty_tile
            else:
                if initBoard[i][j].cget("text") == "":
                    empty_tile.append(i)
                    empty_tile.append(j)
                    return empty_tile

# Breadth-first search
def BFS(initBoard):
    empty_tile = findEmptyTile(initBoard)
    node = {
        "puzzle": initBoard,
        "empty_tile": empty_tile,
        "action": [],
        "parent": None
    }

    frontier = [node]
    explored = []

    while len(frontier) != 0:
        currentState = frontier.pop(0)
        explored.append(currentState)
        if(GoalTest(currentState)):
            # just return the action key of the goal board since it is an array containing all the moves leading to it
            return currentState["action"]
        else:
            for a in Actions(currentState):
                result = Result(currentState, a)
                result_board = result["puzzle"] # get the puzzle/board for checking because the whole node is sure to be different compare to those in explored/frontier
                if not any(node['puzzle'] == result_board for node in explored) and not any(node['puzzle'] == result_board for node in frontier):
                    frontier.append(result)


# Depth-first search
# Same with BFS, except we used stack (we add at the end of the frontier, and explore the end first)
def DFS(initBoard):
    empty_tile = findEmptyTile(initBoard)
    node = {
        "puzzle": initBoard,
        "empty_tile": empty_tile,
        "action": [],
        "parent": None
    }

    frontier = [node]
    explored = []

    while len(frontier) != 0:
        currentState = frontier.pop(len(frontier)-1)
        explored.append(currentState)
        if(GoalTest(currentState)):
            return currentState["action"]
        else:
            for a in Actions(currentState):
                result = Result(currentState, a)
                result_board = result["puzzle"]
                if not any(node['puzzle'] == result_board for node in explored) and not any(node['puzzle'] == result_board for node in frontier):
                    frontier.append(result)

# returns all possible actions given a state
def Actions(currentState):
    actions = []
    emptyRow = currentState["empty_tile"][0]
    emptyCol = currentState["empty_tile"][1]

    if emptyRow > 0:
        actions.append("U")
    if emptyCol < 2:
        actions.append("R")
    if emptyRow < 2:
        actions.append("D")
    if emptyCol > 0:
        actions.append("L")
    
    return(actions)

# Returns the next state given a current state and an action
def Result(currentState, action):
    currentBoard = copy.deepcopy(currentState["puzzle"])
    emptyRow = currentState["empty_tile"][0]
    emptyCol = currentState["empty_tile"][1]
    new_emptyTile = []

    if action == "U":
        currentBoard[emptyRow][emptyCol], currentBoard[emptyRow-1][emptyCol] = currentBoard[emptyRow-1][emptyCol], currentBoard[emptyRow][emptyCol]
        new_emptyTile = [emptyRow-1, emptyCol]
    elif action == "R":
        currentBoard[emptyRow][emptyCol], currentBoard[emptyRow][emptyCol+1] = currentBoard[emptyRow][emptyCol+1], currentBoard[emptyRow][emptyCol]
        new_emptyTile = [emptyRow, emptyCol+1]
    elif action == "D":
        currentBoard[emptyRow][emptyCol], currentBoard[emptyRow+1][emptyCol] = currentBoard[emptyRow+1][emptyCol], currentBoard[emptyRow][emptyCol]
        new_emptyTile = [emptyRow+1, emptyCol]
    elif action == "L":
        currentBoard[emptyRow][emptyCol], currentBoard[emptyRow][emptyCol-1] = currentBoard[emptyRow][emptyCol-1], currentBoard[emptyRow][emptyCol]
        new_emptyTile = [emptyRow, emptyCol-1]

    all_actions = copy.deepcopy(currentState["action"])
    all_actions.append(action)
    
    if "f" in currentState:
        node = {
            "puzzle": currentBoard,
            "empty_tile": new_emptyTile,
            "action": all_actions,
            "parent": currentState,
            "g": len(all_actions),
            "h": None,
            "f": None
        }
    else:
        node = {
            "puzzle": currentBoard,
            "empty_tile": new_emptyTile,
            "action": all_actions,
            "parent": currentState
        }

    return node

# check if the goal has been reached 
def GoalTest(currentState):
    currentBoard = currentState["puzzle"]
    board_1D = []

    for i in range(len(currentBoard)):
        for j in range(len(currentBoard)):
            if currentBoard[i][j] != 0:
                board_1D.append(currentBoard[i][j])

    for i in range(1, len(board_1D)):
        if board_1D[i] < board_1D[i-1]:
            return False
    
    # the 0 tile should be placed at the end of the board
    if currentBoard[len(currentBoard)-1][len(currentBoard)-1] != 0:
        return False
    
    return True

# A* Search
def AStar(initBoard):
    empty_tile = findEmptyTile(initBoard)
    node = {
        "puzzle": initBoard,
        "empty_tile": empty_tile,
        "action": [],
        "parent": None,
        "g": 0,
        "h": None,
        "f": None
    }

    openList = [node]
    closedList = []

    while len(openList) != 0:
        bestNode = removeMinF(openList)
        closedList.append(bestNode)
        if(GoalTest(bestNode)):
            # just return the action key of the goal board since it is an array containing all the moves leading to it
            return bestNode["action"]
        else:
            for a in Actions(bestNode):
                result = Result(bestNode, a)
                result_g = result["g"]
                result_board = result["puzzle"] # get the puzzle/board for checking because the whole node is sure to be different compare to those in explored/frontier
                # conditions to be checked before adding the result to open list
                inOpenList = any(node['puzzle'] == result_board for node in openList)
                inClosedList = any(node['puzzle'] == result_board for node in closedList)
                inOpen_LowerG = any(node['puzzle'] == result_board and node["g"] > result_g for node in openList)
                if (not inClosedList and not inOpenList) or inOpen_LowerG:
                    openList.append(result)

# will return the lowest F among the nodes in openList
def removeMinF(openList):
    for node in openList:
        # evaluate only those nodes without f yet
        if node["f"] == None:
            node["h"] = hVal(node)
            node["f"] = node["g"] + node["h"]
    

    minF = min(openList, key=lambda x:x['f'])
    openList.remove(minF)
    return minF
    
# returns the h value of a given node/state
def hVal(node):
    board = node["puzzle"]
    correctPos = correctPositions()
    h = 0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 0:
                x1 = i
                x2 = correctPos[str(board[i][j])][0]
                y1 = j
                y2 = correctPos[str(board[i][j])][1]
                dist = abs(x1 - x2) + abs(y1 - y2)
                h += dist

    return h

# returns a dictionary containing the board labels as keys and their correct position as values
def correctPositions():
    correctPos = {}
    tile = 1
    for i in range(3):
        for j in range(3):
            if i != 2 or j != 2:
                correctPos[str(tile)] = [i, j]
                tile += 1

    return correctPos


