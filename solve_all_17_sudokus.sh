#!/usr/bin/env bash
geloest=0
for i in {1..49150}
    do
    ./sudokuSolver.py -s -f sudoku17 $i
    if [ $? -eq 0 ]
    then
        geloest=$[$geloest+1]
        echo "$geloest/$i"
    fi
done
