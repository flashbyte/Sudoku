#!/usr/bin/env bash

commits="0.2 master"
counts=100

cd /tmp/Sudoku

if [ -d /tmp/Sudoku ]
then
    git checkout -q master
    git pull -q
else
    git clone git@github.com:flashbyte/Sudoku.git /tmp/Sudoku
fi

for commit in $commits
do
    git checkout -q $commit
    echo "Commit: $commit Solving:$counts"
    time (
        geloest=0
        for ((i=1; i<=counts; i++))
            do
            ./sudokuSolver.py -s -f sudoku17 $i
            if [ $? -eq 0 ]
            then
                geloest=$[$geloest+1]
            fi
        done
        echo "Geloest: $geloest"
    )
    echo
done
