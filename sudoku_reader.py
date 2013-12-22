import sudoku_field
from testcases import sudoku_testcases


def read_soduko_from_testcase(testcase_number):
    my_sudoku = sudoku_field.sudoku_field(
        sudoku_testcases[testcase_number]['description'],
        sudoku_testcases[testcase_number]['testcase']
    )
    return my_sudoku

def read_sudoku_from_file(filename, sudoku_number):
    file_handler = open(filename)
    sudoku_list = file_handler.readlines()
    file_handler.close()
    sudoku_string = sudoku_list[sudoku_number].rstrip()
    filed_tmp = [
        sudoku_string[0:9],
        sudoku_string[9:18],
        sudoku_string[18:27],
        sudoku_string[27:36],
        sudoku_string[36:45],
        sudoku_string[45:54],
        sudoku_string[54:63],
        sudoku_string[63:72],
        sudoku_string[72:91]
    ]
    field = []
    for row in range(len(filed_tmp)):
        field.append([int(c) for c in filed_tmp[row]])
    my_sudoku = sudoku_field.sudoku_field(
        sudoku_string,
        field
    )
    return my_sudoku

