import num_field


class sudoku_field(object):
    """simple"""

    def __init__(self):

        self.__filed__ = [[num_field.num_field()] * 9] * 9

    def set_field(self, row, col, value):
        self.__filed__[row][col].is_solved = True
        self.__filed__[row][col].__could_be_number__ = [value]

    def __str__(self):
        ret = ""
        for line in self.__filed__:
            tmp = ""
            for i in line:
                tmp = tmp + str(i) + ' '
            ret = ret + tmp + "\n"
        return ret
