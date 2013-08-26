#!/usr/bin/env python
import logging
from sudoku_reader import read_soduko_from_testcase


my_suduko = read_soduko_from_testcase(2)


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Solving: %s' % (my_suduko.description))
    print(my_suduko)
    solved_sudoku = my_suduko._recursivly()
    print(solved_sudoku)

if __name__ == '__main__':
    main()
