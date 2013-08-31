import unittest
import num_field
from sudoku_field import sudoku_field
from testcases import sudoku_testcases


class TestNumField(unittest.TestCase):

    def setUp(self):
        self.field = num_field.num_field()

    def test_constructor(self):
        self.assertEqual((len(self.field._could_be_number)), 9)
        self.assertFalse(self.field._is_solved)
        self.assertEqual(self.field._value, 0)

    def test_set_num(self):
        self.field.set_num(4)
        self.assertEqual((len(self.field._could_be_number)), 0)
        self.assertTrue(self.field._is_solved)
        self.assertEqual(self.field._value, 4)

    def test_set_possibilities(self):
        self.field.set_possibilities(set([3, 4]))
        self.assertEqual((len(self.field._could_be_number)), 2)
        self.assertFalse(self.field._is_solved)
        self.assertEqual(self.field._value, 0)

    def test_set_possibilities_with_only_one_value(self):
        self.field.set_possibilities(set([4]))
        self.assertEqual((len(self.field._could_be_number)), 0)
        self.assertTrue(self.field._is_solved)
        self.assertEqual(self.field._value, 4)

    # TODo: check return value
    def test_remove_posibility(self):
        self.field.remove_posibility(5)
        self.assertEqual((len(self.field._could_be_number)), 8)
        self.assertFalse(self.field._is_solved)
        self.assertEqual(self.field._value, 0)

    def test_remove_posibility_but_one(self):
        self.field.remove_posibility(1)
        self.field.remove_posibility(2)
        self.field.remove_posibility(3)
        self.field.remove_posibility(4)
        self.field.remove_posibility(5)
        self.field.remove_posibility(7)
        self.field.remove_posibility(8)
        self.field.remove_posibility(9)
        self.assertEqual((len(self.field._could_be_number)), 0)
        self.assertTrue(self.field._is_solved)
        self.assertEqual(self.field._value, 6)


class TestSudokuField(unittest.TestCase):

    def setUp(self):
        self.empty_field = sudoku_field()
        self.field = sudoku_field(
            sudoku_testcases[1]['description'],
            sudoku_testcases[1]['testcase']
        )

    def test_constructor(self):
        for row in range(9):
            for col in range(9):
                self.assertEqual(self.empty_field._field[row][col].get_num(), 0)
        self.assertEqual(self.empty_field.description, '')

    def test_constructor_with_test_case(self):
        self.assertEqual(sudoku_testcases[1]['description'], self.field.description)
        for row in range(9):
            for col in range(9):
                if sudoku_testcases[1]['testcase'][row][col] != 0:
                    self.assertEqual(sudoku_testcases[1]['testcase'][row][col], self.field._field[row][col].get_num())

    def test_get_block_as_list(self):
        for row_start in range(0, 9, 3):
            for col_start in range(0, 9, 3):
                expected_list = []
                block_id = int(row_start + (col_start / 3) + 1)
                for row in range(row_start, row_start + 3):
                    for col in range(col_start, col_start + 3):
                        expected_list.append(self.field._field[row][col])
                self.assertEqual(self.field._get_block_as_list(block_id), expected_list,
                                 'List of block ' + str(block_id) + ' (' + str(row_start) + '/' 
                                 + str(col_start) + ') num_field objects does not match expected list.')

    def test_get_col_as_list(self):
        for col in range(0, 9):
            expected_list = []
            for row in range(0, 9):
                expected_list.append(self.field._field[row][col])
            self.assertEqual(self.field._get_col_as_list(col), expected_list, 
                             'List of column ' + str(col) + ' num_field objects does not match expected list.')

    def test_get_row_as_list(self):
        for row in range(0, 9):
            expected_list = []
            for col in range(0, 9):
                expected_list.append(self.field._field[row][col])
            self.assertEqual(self.field._get_row_as_list(row), expected_list, 
                             'List of row ' + str(row) + ' num_field objects does not match expected list.')

    def test_validate(self):
        #TODO: Complet row, col and block check
        self.assertTrue(self.field.validate())
        self.field.set_field(0, 0, 3)
        self.assertFalse(self.field.validate())

    def test_update_possibilities(self):
        self.assertSetEqual(set([1, 2, 3, 4, 5, 6, 7, 8, 9]), self.field._field[0][0].get_set())
        self.field._update_possibilities()
        self.assertSetEqual(set([6, 9]), self.field._field[0][0].get_set())

if __name__ == '__main__':
    unittest.main()
