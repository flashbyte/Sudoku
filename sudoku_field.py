import num_field


class sudoku_field(object):
    """simple"""

    def __init__(self):
        self._filed_ = []
        for rows in range(9):
            row = []
            for cols in range(9):
                row.append(num_field.num_field())
            self._filed_.append(row)

    def set_field(self, row, col, value):
        self._filed_[row][col].is_solved = True
        self._filed_[row][col].__could_be_number__ = [value]

    def __str__(self):
        ret = ""
        for line in self._filed_:
            tmp = ""
            for i in line:
                tmp = tmp + str(i) + ' '
            ret = ret + tmp + "\n"
        return ret

    def solve():
        return _remove_possibilities()



    def _remove_possibilities():
        result = False
        # TODO implement this function
        return result
