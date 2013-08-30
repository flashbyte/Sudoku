#!/usr/bin/env python
import logging
import argparse
from sudoku_reader import read_soduko_from_testcase
from testcases import sudoku_testcases


def main():
    my_suduko = None
    parser = argparse.ArgumentParser(description='Solves Sudokus')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enables Debuging')
    parser.add_argument('-lt', '--list', dest='list_testcases', action='store_true', help='Liste availbe Sudoku Testcases')
    parser.add_argument('sudoku', nargs='?', help='Sudoku to solve. Could be a Testace number or filename to valid Sudokufile')
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
        if args.sudoku.isdigit():
            if (int(args.sudoku) > -1) and (int(args.sudoku) < len(sudoku_testcases)):
                my_suduko = read_soduko_from_testcase(int(args.sudoku))
            else:
                logging.error('Testcase %s not found', args.sudoku)

        # TODO: Implement file read

    if my_suduko:
        print('Solving:\n%s' % my_suduko)
        my_suduko.solve()
        if my_suduko.is_solved():
            print('Solved:\n%s' % my_suduko)
        else:
            print(';-( I am not smart enougth to solve this. Got so far:\n%s' % my_suduko.debug_board(my_suduko))


if __name__ == '__main__':
    main()
