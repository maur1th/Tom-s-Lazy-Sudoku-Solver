#!/usr/bin/env python
# Thomas Maurin, 2014
# Tom's Lazy Sudoku Solver
# -- Helper file

import sys
import os
import string


def error(kind):
    """ Handle various kinds of errors
    """
    if kind == 2:
        print "Please enter a valid file (refer to examples for format)."
    elif kind == 3:
        print "Please provide an existing file."
    elif kind == 8:
        print "Unsolvable, please check your input and/or try again, you might be luckier!"
    else:
        print "Usage: lazy_sudoku.py puzzle.txt (refer to examples for format)"
        print "       or lazy_sudoku.py --manual_input"
    sys.exit(1)


def validate(file):
    """ Check the correctness of the file input
    """
    try:
        f = open(file)
    except:
        error(3)

    # Parse f line by line and char by char and check if 1-9 or space
    y = 0
    for line in f:
        x = 0
        for char in line:
            try:
                char = int(char)
            except:
                pass
            if char == None:
                break
            elif char in range(1,10) or char.isspace():
                pass
            else:
                error(2)
            x += 1
        y += 1
        if x != 10:
            if x == 9 and y == 9:
                continue
            else:
                error(2)

    if y != 9:
        error(2)

    f.close()
    return None


def setboard(file):
    """ Set the 9x9 grid in a dict where keys are the coordinates for each cell
    """
    f = open(file)
    y = 1
    board = dict()

    # Parse f line by line and char by char and store its contents in
    # a dict as follows '(x,y) : value' (x,y) being the coordinates of the cell
    for line in f:
        x = 1
        for char in line:
            if x == 10:
                break
            try:
                board[(x, y)] = int(char)
            except:
                board[(x, y)] = 0
            x += 1
        y += 1
    f.close()
    return board


def setblank():
    """ Set a blank board
    """

    # Set a blank board
    board = dict()
    for y in xrange(1,10):
        for x in xrange(1,10):
            board[(x,y)] = 0

    for y in xrange(1,10):
        for x in xrange(1,10):
            os.system('cls' if os.name == 'nt' else 'clear')
            board[(x,y)] = '_'

            print "Please enter your board:"
            printboard(board)

            board[(x,y)] = input()

    return board


def input():
    """ Manage input on a manually entered board
    """
    while True:
        value = raw_input("Value? (1-9, enter to skip, q to quit) > ")

        try:
            value = int(value)
        except:
            pass

        if value in range(1, 10):
            return value
        elif value == "":
            return 0
        elif value == "q":
            sys.exit(0)
        else:
            continue


def edit(board):
    """ Edits the board
    """

    # Print the board with coordinates
    print "Entered board:\n"

    # Header
    print ' ' * 3,

    columns = list(string.ascii_uppercase)[:9]
    count_cols = 0
    for letter in columns:
        count_cols += 1
        if count_cols % 3 != 0:
            print letter,
        else:
            print letter + '  ',
    print
    
    print '  +' + '-' * 23 + '+'
    # Body
    for y in xrange(1,10):
        print y, '|',

        for x in xrange(1,10):
            num = board[(x,y)]
            if num == 0:
                num = ' '
            if x == 9:
                print num, '|'
            elif x % 3 == 0:
                print num, '|',
            else:
                print num,
        if y % 3 == 0 and y != 9:
            print '  |' + '-' * 7 + '+' + '-' * 7 + '+' + '-' * 7 + '|'
    # Footer
    print '  +' + '-' * 23 + '+'
    print

    # Ask for modification
    while True:
        position = raw_input("Position to edit? (format: A3) > ")

        try:
            row = int(position[1:])
        except:
            continue

        if position[0] in columns and row in range(1, 10):
            x = columns.index(position[0])+1
            y = row
            
            board[(x,y)] = input()
            return board

        else:
            continue


def printboard(board):
    """ Print the board
    """

    # Header
    print '+' + '-' * 23 + '+'
    # Body
    for y in xrange(1,10):
        print '|',
        for x in xrange(1,10):
            num = board[(x,y)]
            if num == 0:
                num = ' '
            if x == 9:
                print num, '|'
            elif x % 3 == 0:
                print num, '|',
            else:
                print num,
        if y % 3 == 0 and y != 9:
            print '|' + '-' * 7 + '+' + '-' * 7 + '+' + '-' * 7 + '|'
    # Footer
    print '+' + '-' * 23 + '+'
    print