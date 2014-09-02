# Tom’s Lazy Sudoku Solver
## User documentation
Tom’s Lazy Sudoku Solver is a command-line Sudoku solver. It can solve a wide range of Sudoku problems thanks to using both a deterministic approach and hypotheses.

Tom’s Lazy Solver must be called with the Python interpreter:

`$ python lazy_sudoku.py`

It is also possible to give the program executable rights (`chmod +x`). In which case it will possible to call it by using simply:

`$ ./lazy_sudoku.py`

Two input modes are available: pre-formatted file or manual input. This is reflected by the arguments the program accept:

`Usage: lazy_sudoku.py puzzle.txt (refer to examples for format) or lazy_sudoku.py --manual_input`

### Pre-formatted file input
Pre-formatted files such as those provided in the “examples” directory must comply with the following rules:
*ASCII text files with a “.txt” extension;
*No more, no less than 9 characters per line;
*No more, no less than 9 lines long;
*Only characters accepted are: 1 through 9 and whitespace (space) character;
*Whitespace (space) characters should replace any empty cell.

### Manual input
Opting for manual input will provide you with a command-line interface to input your data cell by cell.

Once complete, a prompt will ask you if your input is correct, if not, you will be redirected to a command-line interface to edit your Sudoku problem.
￼￼