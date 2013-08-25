import num_field


class sudoku_field(object):
    """simple"""

    def __init__(self):

        self.__filed__ = [[num_field.num_field()] * 9] * 9

    def print_me(self):
        for line in self.__filed__:
            tmp = ""
            for i in line:
                tmp = tmp + str(i) + ' '
            print tmp
