import num_field
#import sets

class sudoku_field(object):
    """simple"""

    def __init__(self):
        self._field = []
        for rows in range(9):
            row = []
            for cols in range(9):
                row.append(num_field.num_field())
            self._field.append(row)

    def set_field(self, row, col, value):
        self._field[row][col].set_num(value)

    def __str__(self):
        ret = "+---------board---------+\t+---------debug---------+\n"
        for row in range(9):
            ret += "| "
            for col in range(9):
                ret += str(self._field[row][col]) + ' '
                if col%3 == 2 and col < 8:
                    ret += "| "
            ret += "|\t| "
            for col in range(9):
                ret += str(len(self._field[row][col].get_set())) + ' '
                if col%3 == 2:
                    ret += "| "
            ret += "\n"
            if row%3 == 2 and row < 8:
                ret += "|-------+-------+-------|\t|-------+-------+-------|\n"
        ret += "+-----------------------+\t+-----------------------+"
        return ret

    def solve(self):
        return self._remove_possibilities() or self._scanning()

    def _remove_possibilities_from_row(self, row):
        result = False
        for col in range(9):
            if self._field[row][col].is_solved():
                for col_remove in range(9):
                    if self._field[row][col_remove].remove_posibility(self._field[row][col].get_num()):
                        result = True
        return result

    def _remove_possibilities_from_col(self, col):
        result = False
        for row in range(9):
            if self._field[row][col].is_solved():
                for row_remove in range(9):
                    if self._field[row_remove][col].remove_posibility(self._field[row][col].get_num()):
                        result = True
        return result

    def _remove_possibilities(self):
        result = False
        for row in range(9):
            if self._remove_possibilities_from_row(row):
                result = True
        for col in range(9):
            if self._remove_possibilities_from_col(col):
                result = True

        return result

    def _scanning_row(self, row):
        #Make Union
        my_union = set()
        for col in range(9):
            my_union = my_union.union(self._field[row][col].get_set())

        #del intersec
        for col in range(9):
            for col_intersect in range(col+1, 9):
                my_intersect = self._field[row][col].get_set() & self._field[row][col_intersect].get_set()
                my_union = my_union - my_intersect

        if len(my_union) == 0:
            return False

        for value in my_union:
            for col in range(9):
                if value in self._field[row][col].get_set():
                    self._field[row][col].set_num(value)

        return True

    def _scanning(self):
        result = False
        # Scanning Rows
        for row in range(9):
            result = result or self._scanning_row(row)
        return result
