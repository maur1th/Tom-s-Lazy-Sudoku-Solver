#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def setboard(file):
    """Set the 9x9 grid in a dict where keys are the coordinates for each cell
    """
    f = open(file)
    y = 1
    board = dict()

    # Parse f line by line and char by char and store its content in
    # a dict as follows '(x,y) : value' (x,y) being the coordinates of the cell
    for line in f:
        x = 1
        for char in line:
            if x == 10:
                break
            try:
                board[(x, y)] = int(char)
            except ValueError:
                board[(x, y)] = 0
            x += 1
        y += 1
    f.close()
    return board


def set_empty_board():
    board = dict()
    for y in xrange(1, 10):
        for x in xrange(1, 10):
            board[(x, y)] = 0
    return board


def printboard(board):          # Interface à améliorer
    """ Print the board
    """

    os.system('cls' if os.name == 'nt' else 'clear')

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