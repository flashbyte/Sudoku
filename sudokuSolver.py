#!/usr/bin/env python
import logging
import argparse
import os
import sys
import Solver
from sudoku_reader import read_soduko_from_testcase, read_sudoku_from_file
from testcases import sudoku_testcases


def main():
    my_suduko = None
    parser = argparse.ArgumentParser(description='Solves Sudokus')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enables Debuging')
    group.add_argument('-s', '--silent', dest='silent', action='store_true', help='Enables Silent Mode')
    parser.add_argument('-f', '--filename', dest='filename', help='Filename')
    parser.add_argument('-lt', '--list', dest='list_testcases', action='store_true', help='Liste availbe Sudoku Testcases')
    parser.add_argument('sudoku', help='Sudoku to solve. Could be a Testace number or filename to valid Sudokufile')
    args = parser.parse_args()

    # Debuging?
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    # List Testcases
    if args.list_testcases:
        for testcases_id in range(len(sudoku_testcases)):
            testc = read_soduko_from_testcase(testcases_id)
            print ("---- %s ---- %d" % (testc.description, testcases_id))
            print (testc)

    # Sudoku file/number
    if args.sudoku:
        if not args.filename:
            if args.sudoku.isdigit():
                if (int(args.sudoku) > -1) and (int(args.sudoku) < len(sudoku_testcases)):
                    my_suduko = read_soduko_from_testcase(int(args.sudoku))
                else:
                    logging.error('Testcase %s not found', args.sudoku)
        else:
            if os.path.isfile(args.filename):
                if args.sudoku == 0:
                    pass # TODO: Parse all sudokus
                else:
                    if args.sudoku < 0:
                        logging.error('Jow! Just positives numbers!')
                    else:
                        my_suduko = read_sudoku_from_file(os.path.abspath(args.filename), int(args.sudoku))
            else:
                logging.error('File %s not found! fuc$$!!!' % (os.path.abspath(args.filename)))
        # TODO: Implement file read

    if my_suduko:
        if not args.silent:
            print('Solving:\n%s' % my_suduko)
            solver = Solver.Solver(my_suduko)
            success = solver.solve()
            if success:
                print('Solved:\n%s' % my_suduko)
                sys.exit(0)
            else:
                print(';-( I am not smart enougth to solve this. Got so far:\n%s' % my_suduko)
                sys.exit(42)
        else:
            solver = Solver.Solver(my_suduko)
            success = solver.solve()
            if success:
                sys.exit(0)
            else:
                sys.exit(42)


if __name__ == '__main__':
    main()
