#!/usr/bin/env python
import sudoku_read
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    my_suduko = sudoku_read.read_soduko_from_file('/tmp/some_file')
    print ('???Sudoku to Solve???')
    print (my_suduko)
    my_suduko.solve()
    print ('!!!Sudoku Solved!!!')
    print (my_suduko)

if __name__ == '__main__':
    main()
