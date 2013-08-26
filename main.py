#!/usr/bin/env python
import logging
from sudoku_reader import read_soduko_from_testcase


my_suduko = read_soduko_from_testcase(1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Solving: %s' % (my_suduko.description))
    print(my_suduko)
    my_suduko.solve()
    print(my_suduko)

if __name__ == '__main__':
    main()
