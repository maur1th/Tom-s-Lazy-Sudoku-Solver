#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Thomas Maurin
# Tom's Lazy Sudoku Solver

import sys
import os
import board_util
import engine
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


# if len(sys.argv) < 2:
#     print "Usage: sudoku.py puzzle.txt"
#     sys.exit(1)


board = dict()
if len(sys.argv) == 2:
    board = board_util.setboard(sys.argv[1])
else:
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Welcome to Tom's Lazy Sudoku Solver!\n"
    print "Would you like to:"
    print "A. Input your own values?"
    print "B. Link to a recorded grid?\n"

    while True:
        choice = raw_input("A/B ? > ")
        if choice == "A":
            board = board_util.manual_input()
            break
        elif choice == "B":
            path = raw_input("Path to the recorded grid: ")
            board = board_util.setboard(path)
            break
        else:
            continue

# Initialize the sudoku board and print it
board_util.printboard(board)

# Store the coordinates of the initial values
initial_values = []
for coordinates in board:
    if board[coordinates] != 0:
        initial_values.append(coordinates)

board = engine.solver(board)

print 'Complete board:'
board_util.printboard(board)

print 'Solution only:'
for coord in initial_values:
    if coord in board:
        board[coord] = ' '

board_util.printboard(board)