#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Solver Engine


import sys
from random import randint


# Reset counter to be tweaked if unsolvable which should be solvable
max_reset = 5

# Set a list from 1 to 9 to check against during evaluations
values = [x for x in xrange(1, 10)]


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


def inclusion_eval(board, sqr_start):
    """ Evaluate for each row, column or 3x3 sqr which numbers are yet to be
        added
    """
    
    # Evaluate for each row which numbers are yet to be added
    not_in_rows = ['']
    for y in xrange(1, 10):
        # Create a copy of the "values" list which is 1-9
        not_in_row = list(values)
        for x in xrange(1, 10):
            if board[(x, y)] in values:
                # Each time a value is found, remove it from the list
                not_in_row.remove(board[(x, y)])
        not_in_rows.append(not_in_row)

    # Evaluate for each column which numbers are yet to be added
    not_in_cols = ['']
    for x in xrange(1, 10):
        # Create a copy of the "values" list which is 1-9
        not_in_col = list(values)
        for y in xrange(1, 10):
            if board[(x, y)] in values:
                # Each time a value is found, remove it from the list
                not_in_col.remove(board[(x, y)])
        not_in_cols.append(not_in_col)

    # Evaluate for each 3x3 square which numbers are yet to be added
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
                    not_in_sqr.remove(board[(sqr_start[n][0] + x,
                                             sqr_start[n][1] + y)])
        not_in_sqrs.append(not_in_sqr)

    return not_in_rows, not_in_cols, not_in_sqrs


def solver(board):
    """ Main solver function
    """

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

    # List to keep track of previous states of the board in case a random
    # guess is wrong
    backup = list()

    # Rollback counter: keeps track of errors which may arise when using the
    # random solver
    rollbacks = 0

    # Solver Loop
    not_solved = True
    while not_solved:

        # Pointer to trigger the end of the main while loop when a solution is
        # found
        not_solved = False

        # Pointer to trigger the random guess of a number when no result by
        # Inclusion solver is possible
        no_change = True

        not_in_rows, not_in_cols, not_in_sqrs = inclusion_eval(board,
                                                               sqr_start)

        # Inclusion solver : for each cell of the grid, intersect the three
        # lists of numbers yet to be added (row, col, sqr)
        try:
            for y in xrange(1, 10):
                for x in xrange(1, 10):
                    if isinstance(board[(x, y)], list) or board[(x, y)] == 0:

                        not_solved = True

                        # Intersection
                        board[(x, y)] = list(set(not_in_rows[y])
                                             & set(not_in_cols[x])
                                             & set(not_in_sqrs[square[(x,y)]]))

                        # Handle lists of length zero which result of a "bad
                        # guess" below
                        if len(board[(x, y)]) == 0:

                            if len(backup) == 0:
                                print "Unsolvable, check your input and",
                                print "/ or try again, you may be luckier!"
                                sys.exit(0)

                            # Restore previous board and delete last backup
                            board, backup = restore_board(board, backup)

                            # Increase rollback counter for each error caught,
                            # every max_reset (yes, it is somewhat arbitrary),
                            # restore the board to a random previous state
                            rollbacks += 1
                            if rollbacks > max_reset:
                                rollbacks = 0
                                for z in xrange(randint(1, len(backup))):
                                    board, backup = restore_board(board,
                                                                  backup)
                            raise BreakLoop

                        # Input Inclusion solver results to the board
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
            min_solutions = len(min(pending_values, key=lambda x: len(x)))

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

    return board