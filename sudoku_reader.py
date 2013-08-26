import sudoku_field
from testcases import sudoku_testcases


def read_soduko_from_testcase(testcase_number):
    my_sudoku = sudoku_field.sudoku_field()
    grid = sudoku_testcases[testcase_number]['testcase']
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                my_sudoku.set_field(row, col, grid[row][col])
    return my_sudoku
