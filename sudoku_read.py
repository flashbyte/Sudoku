import sudoku_field

#this is a test
grid1=[[9,0,0, 0,1,7, 0,0,0], # 1
      [8,0,3, 0,2,0, 0,0,0], # 2
      [7,0,0, 0,3,5, 0,0,0], # 3

      [0,0,0, 0,7,9, 0,0,0], # 4
      [2,0,0, 0,0,8, 0,0,0], # 5
      [0,8,9, 5,0,0, 7,2,3], # 6

      [3,0,0, 0,5,1, 0,0,0], # 7
      [0,7,0, 0,8,2, 0,0,0], # 8
      [5,0,0, 0,9,3, 0,0,0]] # 9

#this is an easy one
grid2=[[0,0,7, 0,2,1, 5,3,0], # 1
      [2,0,5, 0,0,0, 0,0,0], # 2
      [8,4,1, 7,0,0, 6,0,0], # 3

      [0,0,2, 4,6,5, 0,1,3], # 4
      [0,0,0, 0,0,0, 0,0,0], # 5
      [3,1,0, 2,8,9, 7,0,0], # 6

      [0,0,4, 0,0,2, 3,6,1], # 7
      [0,0,0, 0,0,0, 9,0,8], # 8
      [0,6,9, 3,7,0, 4,0,0]] # 9


#this is a hard one
grid3=[[6,0,0, 7,8,0, 3,0,0], # 1
      [3,9,7, 0,0,0, 0,8,0], # 2
      [0,0,0, 2,0,0, 0,0,0], # 3

      [0,0,3, 0,1,9, 0,0,0], # 4
      [0,5,0, 0,0,0, 0,0,6], # 5
      [0,0,0, 0,0,2, 9,4,0], # 6

      [0,0,1, 0,4,0, 0,7,2], # 7
      [0,4,5, 8,0,0, 6,1,0], # 8
      [0,0,0, 5,0,1, 0,0,0]] # 9


def read_soduko_from_file(filename):
    grid = grid2
    my_sudoku = sudoku_field.sudoku_field()
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
              my_sudoku.set_field(row, col, grid[row][col])
    return my_sudoku
