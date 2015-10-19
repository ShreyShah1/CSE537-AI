import readGame
ROW = 12
COL = 12

BOX_ROW = 3
BOX_COL = 4

###########################################
# you need to implement five funcitons here
###########################################

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board, emptyCells = readGame.readGameState(filename)
    solveSudoku(board, 0, 0, 0, int(emptyCells))
    return (board, 0)

def isValidMove(board, row, col, number):
    ###############################################	
    # This util checks whether the number to be placed
    # is conflicting or not	
    #############################################	

    # Check all current Row
    for i in range(0, COL):
	if board[row][i] == number:
	   return False

    # Check all current Col
    for i in range(0, ROW):
	if board[i][col] == number:
	   return False	
   
    # Check the boxes 
    startIndicesRow = [0, 3, 6, 9]
    startIndicesCol = [0, 4, 8]

    startRow = startIndicesRow[row / BOX_ROW]	
    startCol = startIndicesCol[col / BOX_COL]
    
    for i in range(0, BOX_ROW):
       for j in range(0, BOX_COL):
          if board[startRow + i][startCol + j] == number:
	     return False      	 	

    return True
    
def solveSudoku(board, startRow, startCol, filledCells, emptyCells):	
 
    if filledCells == emptyCells:
       return True
	
    nextRow = startRow
    nextCol = startCol + 1
	
    if nextCol == COL:
       nextRow += 1
       nextCol = 0       	
	
    if board[startRow][startCol] != 0:
       return solveSudoku(board, nextRow, nextCol, filledCells, emptyCells)

    for number in range(1, 13):
	if isValidMove(board, startRow, startCol, number):
	   board[startRow][startCol] = number	
	   if solveSudoku(board, nextRow, nextCol, filledCells + 1, emptyCells):
	       return True	
	   # Backtracking.
	   board[startRow][startCol] = 0
   
    return False

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    return ([[],[]], 0)

def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    return ([[],[]], 0)

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    return ([[],[]], 0)

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    return ([[]], 0)
