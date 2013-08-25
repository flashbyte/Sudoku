import num_field
import logging
import sys


# TODO: findout if there is something like for_each_for_echh
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
                if col % 3 == 2 and col < 8:
                    ret += "| "
            ret += "|\t| "
            for col in range(9):
                ret += str(len(self._field[row][col].get_set())) + ' '
                if col % 3 == 2:
                    ret += "| "
            ret += "\n"
            if row % 3 == 2 and row < 8:
                ret += "|-------+-------+-------|\t|-------+-------+-------|\n"
        ret += "+-----------------------+\t+-----------------------+"
        return ret

    def _get_block_as_list(self, block_id):
        block_hash = {
            1: (0, 0),
            2: (0, 3),
            3: (0, 6),
            4: (3, 0),
            5: (3, 3),
            6: (3, 6),
            7: (6, 0),
            8: (6, 3),
            9: (6, 6)
        }
        my_list = []
        for row in range(block_hash[block_id][0], block_hash[block_id][0]+3):
            for col in range(block_hash[block_id][1], block_hash[block_id][1]+3):
                my_list.append(self._field[row][col])
        return my_list

    def validate(self):
        valid = True
        #Validate rows
        for row in range(9):
            my_set = set()
            for col in range(9):
                if self._field[row][col].is_solved():
                    if self._field[row][col].get_num() in my_set:
                        valid = False
                    else:
                        my_set.add(self._field[row][col].get_num())
        #Validate cols
        for col in range(9):
            my_set = set()
            for row in range(9):
                if self._field[row][col].is_solved():
                    if self._field[row][col].get_num() in my_set:
                        valid = False
                    else:
                        my_set.add(self._field[row][col].get_num())

        #Validate block
        # TODO Validate block
        return valid

    def apply(self):
        result = False
        for row in range(9):
            for col in range(9):
                if self._field[row][col].apply():
                    result = True
        return result

    def solve(self):
        changed = True
        while changed:
            changed = False
            befor = str(self)
            if self._remove_possibilities():
                changed = True
            if not self.validate():
                logging.debug(befor)
                logging.debug("remove messed up")
                logging.debug(str(self))
                sys.exit(2)

            befor = str(self)
            befor_set = str(self._field[6][5].get_set())
            if self._scanning():
                changed = True
            if not self.validate():
                logging.debug(befor)
                logging.debug(befor_set)
                logging.debug("scanning messed up")
                logging.debug(str(self))
                sys.exit(2)

            if self.apply():
                changed = True

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

    def _remove_possibilities_from_block(self, block_id):
        result = False
        my_list = self._get_block_as_list(block_id)
        for element in my_list:
            if element.is_solved():
                for element_remove in my_list:
                    if element_remove.remove_posibility(element.get_num()):
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
        for block in range(1, 10):
            if self._remove_possibilities_from_block(block):
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

    def _scanning_col(self, col):
        #Make Union
        my_union = set()
        for row in range(9):
            my_union = my_union.union(self._field[row][col].get_set())

        #del intersec
        for row in range(9):
            for row_intersect in range(row+1, 9):
                my_intersect = self._field[row][col].get_set() & self._field[row_intersect][col].get_set()
                my_union = my_union - my_intersect

        if len(my_union) == 0:
            return False

        for value in my_union:
            for row in range(9):
                if value in self._field[row][col].get_set():
                    self._field[row][col].set_num(value)

        return True

    def _scanning_block(self, block_id):
        #FIXME: Breaks Stuff
        my_list = self._get_block_as_list(block_id)
        #Make Union
        my_union = set()
        for element in my_list:
            my_union = my_union.union(element.get_set())
        #make intersec list
        intersec_list = []
        for element in my_list:
            for element_intersect in my_list:
                if element == element_intersect:
                    continue
                intersec_list.append(element.get_set() & element_intersect.get_set())
        #remove intesect
        for element in intersec_list:
            my_union = my_union - element

        if len(my_union) == 0:
            return False

        for uniq in my_union:
            for element in my_list:
                if uniq in element.get_set():
                    element.set_num(uniq)

        return True

    def _scanning(self):
        # Scanning Rows
        for row in range(9):
            if self._scanning_row(row):
                return True
        for col in range(9):
            if self._scanning_col(col):
                return True
        for block in range(1, 10):
            if self._scanning_block(block):
                return True
        return False
