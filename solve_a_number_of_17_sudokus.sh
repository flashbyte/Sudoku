#!/usr/bin/env bash

# This script run the sudoku solver with arg1 sodukus.
geloest=0
counts=$1
for ((i=1; i<=counts; i++))
    do
    ./sudokuSolver.py -s -f sudoku17 $i
    if [ $? -eq 0 ]
    then
        geloest=$[$geloest+1]
        echo "$geloest/$i"
    fi
done
