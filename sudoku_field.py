import num_field
import logging
import sys
import copy


# TODO: findout if there is something like for_each_for_echh
class sudoku_field(object):
    """simple"""

    def __init__(self, description='', sudoku=None):
        self._field = []
        self.description = description
        for rows in range(9):
            row = []
            for cols in range(9):
                row.append(num_field.num_field())
            self._field.append(row)
        if sudoku:
            for row in range(9):
                for col in range(9):
                    if sudoku[row][col] != 0:
                        self.set_field(row, col, sudoku[row][col])

    def __str__(self):
        lines = self.generate_printable_lines(self._field)
        interlaced_lines = self.interlace_printable_lines(lines)

        ret = ""
        for line in interlaced_lines:
            ret += line

        return ret

    def interlace_printable_lines(self, lines):
        interlaced_lines = []

        interlaced_lines.append("+---------board---------+\n")

        line_index = 1
        for line in lines:
            interlaced_lines.append(line)
            if line_index % 3 == 0:
                 interlaced_lines.append("| ----- | ----- | ----- |\n")
            line_index += 1
        interlaced_lines.append("+-----------------------+\n")

        return interlaced_lines

    def generate_printable_lines(self, field):
        lines = []
        for row in field:
            lines.append("| %s %s %s | %s %s %s | %s %s %s |\n" % tuple(row))
        return lines

    def debug_str(self):
        ret = "board and debug (num of possibilities)\n"
        ret += "+---------board---------+\t"
        ret += "+---------debug---------+\n"
        for row in range(9):
            ret += "| %s %s %s | %s %s %s | %s %s %s |\t" % (tuple(self._field[row]))
            ret += "| %s %s %s | %s %s %s | %s %s %s |\n" % ( tuple([len(i.get_set()) for i in self._field[row]]) )
            if row in (2, 5):
                ret += "| ----- | ----- | ----- |\t"
                ret += "| ----- | ----- | ----- |\n"
        ret += "+-----------------------+\t"
        ret += "+-----------------------+\n"
        return ret

    def __unicode__(self):
        return self.__str__()

    def set_field(self, row, col, value):
        self._field[row][col].set_num(value)

    def debug_board(self, befor_stat):
        header = "+---------befor---------+\t+----------now----------+"
        footer = "+-----------------------+\t+-----------------------+"
        line = "| %s %s %s | %s %s %s | %s %s %s |\t| %s %s %s | %s %s %s | %s %s %s |"
        line2 = "| ----- | ----- | ----- |\t| ----- | ----- | ----- |"
        board = "%s\n%s\n%s\n"

        board_str = ""
        for row in range(9):
            befor_row = befor_stat._field[row]
            now_row = self._field[row]
            values = tuple(befor_row) + tuple(now_row)
            board_str += line % (values)
            if row != 8:
                board_str += '\n'
            if row in (2, 5):
                board_str += line2 + '\n'

        return board % (header, board_str, footer)

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

    def _get_row_as_list(self, row):
        return self._field[row]

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

    def is_solved(self):
        for row in range(9):
            for col in range(9):
                if len(self._field[row][col].get_set()) != 0:
                    return False
        return True

    def _recursivly(self):
        self.solve()
        if self.is_solved():
            return self

        for row in range(9):
            for col in range(9):
                if len(self._field[row][col].get_set()) != 0:
                    for each in self._field[row][col].get_set():
                        new_soduko = copy.deepcopy(self)
                        new_soduko._field[row][col].set_num(each)
                        new_soduko._update_possibilities()
                        if new_soduko._recursivly():
                            return new_soduko

    def _update_possibilities(self):
        solver_remover_list = [
            self._remove_possibilities_from_rows,
            self._remove_possibilities_from_cols,
            self._remove_possibilities_from_blocks,
        ]
        changed = False
        for solver in solver_remover_list:
            if solver():
                changed = True
            if not self.validate():
                logging.error('%s medded up %s', solver)
                sys.exit(2)
        return changed

    def _scanning(self):
        """
        asdfasdf asdfasdf
        """
        solver_scanner_list = [
            self._scanning_rows,
            self._scanning_cols,
            self._scanning_blocks,
        ]
        for solver in solver_scanner_list:
            if solver():
                logging.debug('Solver %s changed something', solver.__func__)
                if not self.validate():
                    logging.error('Solver %s messed up', solver.__func__)
                    sys.exit(2)
                return True
        return False

    """ Solver functions sould only work on posibilities NOT on the number value
    the number value is updated by self._update_field """
    def solve(self):
        changed = True
        while changed:
            changed = False
            self._update_possibilities()
            if self._scanning():
                changed = True
            if self.is_solved():
                return

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
    def _scanning_bulk(self, bulk):
        changed = False
        # Make Union
        bulk_union = set()
        for element in bulk:
            bulk_union = bulk_union.union(element.get_set())
        # Make intesec list
        intesec_list = []
        for element in bulk:
            for element_intersec in bulk:
                if element != element_intersec:
                    intesec_list.append(element.get_set() & element_intersec.get_set())
        intesec_list = [element_intersec for element_intersec in intesec_list if len(element_intersec) != 0]
        # Make result set (union from everything minus every intesection)
        result_set = bulk_union
        for intersec in intesec_list:
            result_set = result_set - intersec
        # Nothing found ;-(
        if len(result_set) == 0:
            return False
        else:
            changed = True

        # Set found uniq numbers
        for num in result_set:
            element_index = 0
            for element in bulk:
                if num in element.get_set():
                    if num == 8:
                        logging.debug('Possibilities list %s for element: %s', element.get_set(), element_index)

                    my_set = set()
                    my_set.add(num)
                    element.set_possibilities(my_set)
                    logging.debug('Setting value %s for element: %s', num, element_index)
                    print(self)

                element_index += 1

        return changed

    def _scanning_rows(self):
        changed = False
        row_index = 0
        for row in self._field:
            logging.debug('Scanning row: %s', row_index)
            if self._scanning_bulk(row):
                changed = True
            row_index += 1
        return changed

    def _scanning_cols(self):
        changed = False
        for col in range(9):
            col_list = self._get_col_as_list(col)
            if self._scanning_bulk(col_list):
                changed = True
        return changed

    def _scanning_blocks(self):
        changed = False
        for block_id in range(1, 10):
            block = self._get_block_as_list(block_id)
            if self._scanning_bulk(block):
                changed = True
        return changed
