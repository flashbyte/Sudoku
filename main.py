#!/usr/bin/env python
import sudoku_field
import sudoku_read


def main():
    my_suduko = sudoku_read.read_soduko_from_file('/tmp/some_file')
    print (my_suduko)

if __name__ == '__main__':
    main()
