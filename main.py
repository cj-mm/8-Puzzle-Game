from tkinter import *
from play import *
from solution import *

root = Tk()
root.title("8-Puzzle Game")

# Main
board = []

boardInput(board)
initBoard = copy.deepcopy(board)

boardSetUp(root, board)
solutionGUIsetup(root, initBoard, isSolvable(initBoard))


root.mainloop()



# References:
# https://www.youtube.com/watch?v=YXPyB4XeYLA&t=13s
# https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable (only looked for the inversion)
# https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop/39449125
# https://stackoverflow.com/questions/37731654/how-to-retrieve-the-row-and-column-information-of-a-button-and-use-this-to-alter
# https://www.tutorialspoint.com/python/tk_button.htm
# https://www.oreilly.com/library/view/python-gui-programming/9781788835886/05db1907-59da-48b3-a361-e9ad072235d1.xhtml

# https://docs.python.org/3/library/copy.html
# https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
# https://www.geeksforgeeks.org/python-convert-list-of-strings-to-space-separated-string/

# https://stackoverflow.com/questions/5320871/in-list-of-dicts-find-min-value-of-a-common-dict-field
# https://stackoverflow.com/questions/57943886/calling-a-tkinter-var-trace-with-arguments



