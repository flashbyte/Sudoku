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
        possibilities_field = []

        for row in self._field:
            possibilities_field.append([len(i.get_set()) for i in row])

        p_lines = self.generate_printable_lines(possibilities_field)
        interlaced_p_lines = self.interlace_printable_lines(p_lines)

        lines = self.generate_printable_lines(self._field)
        interlaced_lines = self.interlace_printable_lines(lines)

        zipped_lines = zip(interlaced_lines, interlaced_p_lines)

        ret = ""
        for line_tuple in zipped_lines:
            ret += line_tuple[0] + "\t" + line_tuple[1] + "\n"
        return ret

    def __unicode__(self):
        return self.__str__()


    def interlace_printable_lines(self, lines):
        interlaced_lines = []

        interlaced_lines.append("+---------board---------+")

        line_index = 1
        for line in lines:
            interlaced_lines.append(line)
            if line_index % 3 == 0 and line_index != 9:
                 interlaced_lines.append("| ----- | ----- | ----- |")
            line_index += 1
        interlaced_lines.append("+-----------------------+")

        return interlaced_lines

    def generate_printable_lines(self, field):
        lines = []
        for row in field:
            lines.append("| %s %s %s | %s %s %s | %s %s %s |" % tuple(row))
        return lines


    def set_field(self, row, col, value):
        self._field[row][col].set_num(value)

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

