import sudoku_field


def read_soduko_from_file(filename):
    my_sudoku = sudoku_field.sudoku_field()
    my_sudoku.set_field(3, 4, 9)
    return my_sudoku
