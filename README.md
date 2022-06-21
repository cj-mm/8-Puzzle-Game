# Exercise for Solving 8-puzzle using A* Search

## Task
The goal of the exercise is to implement a* search for solving the eight-puzzle game.

## Input
The initial state of the puzzle must be read from an input file called puzzle.in. The puzzle.in file will have 3 lines, each line indicating the objects in each row of the puzzle board.

## Required Output
The output of the program is the playable game interface and a puzzle.out file containing the puzzle solution.

## Programming language used
- Python (with tkinter)

## Problems encountered
- Setting up the GUI in every case. Another problem I had (since exer1) is the time it takes to solve some of the puzzle. If it takes long enough, my program crashes. 

## How the problems were resolved
- Regarding the GUI, what helped me the most is just destroying each widget every time I needed to reset the board. I just set the GUI up again. I also searched more infos about tkinter, and python in general, for syntax. About the crashes, I couldn't do anything about it.

## Learnings
- I learned how the A* search works. Before, while doing the BFS and DFS exer, I kept on wondering how to solve this puzzle without using brute force. Now, I understand how. Of course, I learned not just how the A* search works but also the implementation of it. Consequently, I also learned how the A* search differs from the two brute force algorithms we discussed (BFS and DFS).
