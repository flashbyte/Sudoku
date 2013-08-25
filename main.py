#!/usr/bin/env python
import sudoku_read
import logging
my_suduko = sudoku_read.read_soduko_from_file('/tmp/some_file')


def main():
    logging.basicConfig(level=logging.DEBUG)
    my_suduko.solve()

if __name__ == '__main__':
    main()
