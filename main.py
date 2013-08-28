#!/usr/bin/env python
import logging
import argparse
from sudoku_reader import read_soduko_from_testcase
from testcases import sudoku_testcases

my_suduko = read_soduko_from_testcase(1)


def init():
    parser = argparse.ArgumentParser(description='Solves Sudokus')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enables Debuging')
    parser.add_argument('-lt', '--list', dest='list_testcases', action='store_true', help='Liste availbe Sudoku Testcases')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if args.list_testcases:
        for testcases_id in range(len(sudoku_testcases)):
            testc = read_soduko_from_testcase(testcases_id)
            print ("---- %s ----" % (testc.description))
            print (testc)


def main():
    init()

if __name__ == '__main__':
    main()
