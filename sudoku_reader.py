import sudoku_field
from testcases import sudoku_testcases


def read_soduko_from_testcase(testcase_number):
    my_sudoku = sudoku_field.sudoku_field(
        sudoku_testcases[testcase_number]['description'],
        sudoku_testcases[testcase_number]['testcase']
    )
    return my_sudoku
