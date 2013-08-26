import num_field
import logging
import sys


# TODO: findout if there is something like for_each_for_echh
class sudoku_field(object):
    """simple"""

    def __init__(self):
        self._field = []
        self.description = ''
        for rows in range(9):
            row = []
            for cols in range(9):
                row.append(num_field.num_field())
            self._field.append(row)

    #TODO: constuctor with takes description and field

    def set_field(self, row, col, value):
        self._field[row][col].set_num(value)

    def set_description(self, description):
        self.description = description

    def __str__(self):
        ret = '\n'
        ret += "+---------board---------+\t+---------debug---------+\n"
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

    def _get_col_as_list(self, col):
        col_list = []
        for row in self._field:
            col_list.append(row[col])
        return col_list

    ''' Validated if field is a valid sudoku.'''
    def validate(self):
        #Validate rows
        for row in range(9):
            my_set = set()
            for col in range(9):
                if self._field[row][col].is_solved():
                    if self._field[row][col].get_num() in my_set:
                        logging.error('Row %s is broken' % (row))
                        return False
                    else:
                        my_set.add(self._field[row][col].get_num())

        #Validate cols
        for col in range(9):
            my_set = set()
            for row in range(9):
                if self._field[row][col].is_solved():
                    if self._field[row][col].get_num() in my_set:
                        logging.error('Col %s is broken' % (col))
                        return False
                    else:
                        my_set.add(self._field[row][col].get_num())

        #Validate block
        for block in range(1, 10):
            block_list = self._get_block_as_list(block)
            solved_set = set()
            for field in block_list:
                if field.is_solved():
                    if field.get_num() in solved_set:
                        logging.error('Block %s is broken' % (block))
                        return False
                    else:
                        solved_set.add(field.get_num())

        return True

    def apply(self):
        result = False
        for row in range(9):
            for col in range(9):
                if self._field[row][col].apply():
                    result = True
        return result

    def solve(self):
        solver_list = [
            self._remove_possibilities_from_rows,
            self._remove_possibilities_from_cols,
            self._remove_possibilities_from_blocks,
        ]
        changed = True
        while changed:
            changed = False
            for solver in solver_list:
                if solver():
                    changed = True
                    logging.debug('Solver %s changed something', solver.im_func)
                if not self.validate():
                    logging.error('Solver %s messed up', solver.im_func)
                    sys.exit(2)

            if self.apply():
                changed = True

    # -------- Remover algorithems --------
    """ Removes all posibilities from a bulk where bulk could be a row, a col or a block """
    def _remove_possibilities_from_bulk(self, bulk):
        changed = False
        for element in bulk:
            if element.is_solved():
                for element_remove in bulk:
                    if element_remove.remove_posibility(element.get_num()):
                        changed = True
        return changed

    def _remove_possibilities_from_rows(self):
        changed = False
        for row in self._field:
            if self._remove_possibilities_from_bulk(row):
                changed = True
        return changed

    def _remove_possibilities_from_cols(self):
        changed = False
        for col in range(9):
            col_list = self._get_col_as_list(col)
            if self._remove_possibilities_from_bulk(col_list):
                changed = True
        return changed

    def _remove_possibilities_from_blocks(self):
        changed = False
        for block_id in range(1, 10):
            block = self._get_block_as_list(block_id)
            if self._remove_possibilities_from_bulk(block):
                changed = True
        return changed

    # -------- Scanner algorithmes --------
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
