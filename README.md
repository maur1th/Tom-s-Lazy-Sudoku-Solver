# Tom’s Lazy Sudoku Solver
## User documentation
Tom’s Lazy Sudoku Solver is a command-line Sudoku solver which I created early 2014 to submit as my [CS50](https://cs50.harvard.edu/) final project. This solver can solve a broad range of Sudoku problems thanks to using both a deterministic approach and guesses.

Tom’s Lazy Solver must be called with the Python interpreter:

`$ python lazy_sudoku.py`

It is also possible to give the program executable rights (`chmod +x`). In which case it will possible to call it by using simply:

`$ ./lazy_sudoku.py`

Two input modes are available: pre-formatted file or manual input. This is reflected by the arguments the program accept:

`Usage: lazy_sudoku.py puzzle.txt (refer to examples for format) or lazy_sudoku.py --manual_input`

### Pre-formatted file input
Pre-formatted files such as those provided in the “examples” directory must comply with the following rules:
* ASCII text files with a “.txt” extension;
* No more, no less than 9 characters per line;
* No more, no less than 9 lines long;
* Only characters accepted are: 1 through 9 and whitespace (space) character;
* Whitespace (space) characters should replace any empty cell.

### Manual input
Opting for manual input will provide you with a command-line interface to input your data cell by cell.

Once complete, a prompt will ask you if your input is correct, if not, you will be redirected to a command-line interface to edit your Sudoku problem.

## Design and Implementation
Tom’s Lazy Sudoku Solver (TLSS) was implemented in Python since this is the language I felt the most comfortable with at the time.

Its execution flow is mostly straightforward with calls to a helper file `board_util.py` to handle most of the elements displayed in the command-line as well as preliminary operations.

### Main file
The pillars of TLSS are its hash table (dictionary) `board` and its solver loop. I used a dictionary to store data from the Sudoku problems. This dictionary takes tuples as keys of the format `(x, y)` which are used throughout TLSS as a set of coordinates for each value of the Sudoku problem. This allows the code to be fairly readable and consistent, compared to the alternative of using hash keys which would have certainly improved the code compactness though.

TLSS solver loop has two main components:

1. A deterministic solver which will check all lines, all columns and all 3x3 squares to check if there are any solutions available and update the `board` dictionary accordingly. Available values for each line, column and 3x3 square are evaluated and stored in an array at the beginning of the solver loop.
Solutions for each cell are the intersection of those arrays. Possible solutions are stored in the dictionary directly as a list. If the list is of size 1, a solution is found and the list element replaced by the `int` solution at its `(x,y)` coordinates.
2. If the deterministic solver cannot find any new solution, the solver will then make “smart” hypotheses by selecting randomly one of the values of the shortest list of solutions available. The board is backed up at each of these hypotheses and rollbacks are performed when inconsistencies are found down the road, meaning (one of) the guess(es) was (were) wrong.

The “lazy” part of the solver comes from that the only deterministic solving algorithm I implemented was an inclusion solver, where several other deterministic algorithms are commonly used to solve Sudoku problems.

3x3 squares are handled in a particular fashion (far different than rows and columns) which revolves around three data structures:
* `sqr_start`, a list which stores the start coordinates (left to right, top to bottom) of each 3x3 square;
* `square`, a dictionary which associate each set of coordinates on the board to a square number (1 through 9);
* `not_in_sqr` a list which bridges the two and stores for each square the values yet to be entered in the board.


### Helper file
The helper file `board_util` is a set of “helper” functions which handle most of the elements displayed in the command-line as well as various preliminary (as in, before the solver kicks in) operations.
I created this separate set of functions to:
* Avoid code repetition;
* And avoid cluttering in the main file.

The functions I implemented first in this helper file were:
* `setboard()` to import any file passed as an argument and populate `board` dictionary accordingly
* `printboard()` to display the board.

Those functions were joined by various functions relative to interface and user input afterwards:
* `error()` which prints various errors depending on the error number passed;
* `setblank()`, `input()` and `edit()` functions which enable manual input of Sudoku problems;
* `validate()` which checks the correctness of the file input for pre-formatted file inputs.