#!/usr/bin/env python
# Thomas Maurin, 2014
# Tom's Lazy Sudoku Solver

import sys
import os
import board_util
from random import randint


class BreakLoop(Exception):
    """ Break out of multiple loops
        Courtesy of http://legacy.python.org/dev/peps/pep-3136/#motivation
    """
    pass

def restore_board(board, backup):
    """ Restore the board to its previous state
    """
    board = dict(backup[-1])
    del backup[-1]
    return board, backup


if len(sys.argv) < 2 :
    board_util.error(1)

# Set a list from 1 to 9 to check against during evaluations
values = [x for x in xrange(1, 10)]

# Initialize the board and do checks
if sys.argv[1] == "--manual_input":
    board = board_util.setblank()
    while True:
        # Print the board
        os.system('cls' if os.name == 'nt' else 'clear')
        print "Entered board:"
        board_util.printboard(board)
        
        # Enquire wether the board is correct
        answer = raw_input("Is you board correct ? (y/n) > ")
        if answer == "y":
            break
        elif answer == "n":
            os.system('cls' if os.name == 'nt' else 'clear')
            board = board_util.edit(board)
        else:
            continue

elif sys.argv[1][-4:] == ".txt":
    board_util.validate(sys.argv[1])
    board = board_util.setboard(sys.argv[1])

else:
    board_util.error(1)

# Let's go!
os.system('cls' if os.name == 'nt' else 'clear')
print "Entered board:"
board_util.printboard(board)

# Store the coordinates of the initial values
initial_values = []
for coordinates in board:
    if board[coordinates] != 0:
        initial_values.append(coordinates)

# Set squares start coordinates (top-left)
sqr_start = ['']
for y in xrange(1, 10):
    for x in xrange(1, 10):
        if x % 3 == 1 and y % 3 == 1:
            sqr_start.append([x, y])

# Define squares for each set of coordinates on the board
square = {}
for x in xrange(0, 9):
    for y in xrange(0, 9):
        square[(x + 1, y + 1)] = (x / 3 + 1) + (y / 3) * 3

# Solver
not_solved = True

# List to keep track of previous states of the board in case a random
# guess is wrong
backup = list()

rollbacks = 0

while not_solved:

    # Pointer to trigger the end of the main while loop when a solution is
    # found
    not_solved = False

    # Pointer to trigger the random guess of a number when no result by
    # Inclusion solver is possible
    no_change = True

    # Evaluate for each row which numbers are still to be added to the grid
    not_in_rows = ['']
    # Cycle over each row
    for y in xrange(1, 10):
        # Create a copy of the "values" list which is 1-9
        not_in_row = list(values)
        # Cycle over each column of the y row
        for x in xrange(1, 10):
            if board[(x, y)] in values:
                # Each time a value is found, remove it from the list
                try:
                    not_in_row.remove(board[(x, y)])
                except:
                    board_util.error(8)
        not_in_rows.append(not_in_row)

    # Evaluate for each column which numbers are still to be added to the grid
    not_in_cols = ['']
    # Cycle over each column
    for x in xrange(1, 10):
        # Create a copy of the "values" list which is 1-9
        not_in_col = list(values)
        # Cycle over each row
        for y in xrange(1, 10):
            if board[(x, y)] in values:
                # Each time a value is found, remove it from the list
                try:
                    not_in_col.remove(board[(x, y)])
                except:
                    board_util.error(8)
        not_in_cols.append(not_in_col)

    # Evaluate for each 3x3 square which numbers are still
    # to be added to the grid
    not_in_sqrs = ['']
    # Cycle over each square determined by its "start" coordinates
    # (which is the top left corner of each of the 9 squares of the grid)
    for n in xrange(1, 10):
        # Create a copy of the "values" list which is 1-9
        not_in_sqr = list(values)
        for y in xrange(0, 3):
            for x in xrange(0, 3):
                if (board[(sqr_start[n][0] + x, sqr_start[n][1] + y)]
                        in values):
                    # Each time a value is found, remove it from the list
                    try:
                        not_in_sqr.remove(board[(sqr_start[n][0] + x,
                                                 sqr_start[n][1] + y)])
                    except:
                        board_util.error(8)
        not_in_sqrs.append(not_in_sqr)

    # Inclusion solver : for each cell of the grid, intersect the three lists
    # of numbers still to be added (row, col, sqr)
    try:
        for y in xrange(1, 10):
            for x in xrange(1, 10):
                if isinstance(board[(x, y)], list) or board[(x, y)] == 0:

                    not_solved = True

                    # Intersection
                    board[(x, y)] = list(set(not_in_rows[y])
                                        & set(not_in_cols[x]) 
                                        & set(not_in_sqrs[square[(x, y)]]))

                    # Handle lists of length zero which result of a "bad
                    # guess" below
                    if len(board[(x, y)]) == 0:

                        if len(backup) == 0:
                            board_util.error(8)

                        # Restore previously used board and delete last backup
                        board, backup = restore_board(board, backup)

                        # Increase a rollback counter for each error
                        # encountered, every 10 (yes, it is somewhat 
                        # arbitrary), restore the board to a
                        # previous random state
                        rollbacks += 1
                        if rollbacks > 10:
                            rollbacks = 0
                            for x in xrange(randint(1, len(backup))):
                                board, backup = restore_board(board, backup)
                        raise BreakLoop

                    # Input result in the grid or increment "errors" counter
                    elif len(board[(x, y)]) == 1:
                        board[(x, y)] = board[(x, y)][0]
                        no_change = False
                        raise BreakLoop

    except BreakLoop:
        continue

    # If Inclusion solver doesn't find any more matches (ie. lists
    # of length 1)
    if no_change:

        # Find a random unsolved item on the grid
        # with the fewest potential solutions

        # 1st, keep only unsolved items (= lists)
        pending_values = list()
        for value in board.values():
            if isinstance(value, list):
                pending_values.append(value)

        if len(pending_values) == 0:
            not_solved = False
            break

        # 2nd, find out the length of the smallest unsolved item
        min_solutions = len(min(pending_values, key=lambda z: len(z)))

        # Finally, randomly find an item with min_solutions
        while True:
            x = randint(1, 9)
            y = randint(1, 9)

            if (isinstance(board[(x, y)], list)
                    and len(board[(x, y)]) == min_solutions):
                # Backup the board in its current state
                backup.append(dict(board))

                # Choose a random solution from the item list
                num = board[(x, y)][randint(0, min_solutions - 1)]
                board[(x, y)] = int(num)

                break


while True:
    answer = raw_input("Print the (c)omplete board or only its (s)olution? > ")
    
    if answer == "c":
        os.system('cls' if os.name == 'nt' else 'clear')
        print 'Complete board:'
        board_util.printboard(board)

        raw_input("Press enter to display only the solution values. ")
        break
    elif answer == "s":
        break
    else:
        continue

os.system('cls' if os.name == 'nt' else 'clear')
print 'Solution only:'
for coord in initial_values:
    if coord in board:
        board[coord] = ' '

board_util.printboard(board)

print '-' * 3
print "Thanks for using Tom's Lazy Sudoku Solver!"
print