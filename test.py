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
                self.assertEquals(self.empty_field._field[row][col].get_num(), 0)
        self.assertEquals(self.empty_field.description, '')

    def test_constructor_with_test_case(self):
        self.assertEqual(sudoku_testcases[1]['description'], self.field.description)
        for row in range(9):
            for col in range(9):
                if sudoku_testcases[1]['testcase'][row][col] != 0:
                    self.assertEqual(sudoku_testcases[1]['testcase'][row][col], self.field._field[row][col].get_num())

    def test_get_block_as_list(self):
        my_list = [i.get_num() for i in self.field._get_block_as_list(1)]
        self.assertEqual(my_list, [0, 0, 7, 2, 0, 5, 8, 4, 1])

    def test_get_col_as_list(self):
        my_list = [i.get_num() for i in self.field._get_col_as_list(0)]
        self.assertEqual(my_list, [0, 2, 8, 0, 0, 3, 0, 0, 0])

    def test_get_row_as_list(self):
        my_list = [i.get_num() for i in self.field._get_row_as_list(0)]
        self.assertEqual(my_list, [0, 0, 7, 0, 2, 1, 5, 3, 0])

    def test_validate(self):
        #TODO: Complet row, col and block check
        self.assertTrue(self.field.validate())
        self.field.set_field(0, 0, 3)
        self.assertFalse(self.field.validate())

    def test_update_possibilities(self):
        self.field._update_possibilities()
        self.assertSetEqual(set([4, 6, 9]), self.field._field[0][0].get_set())

if __name__ == '__main__':
    unittest.main()
