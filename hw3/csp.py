import readGame
import Queue as Q
import sys
from pprint import pprint
import copy
################################
# CONSTANTS
REMOVE = 1
ADD = 2
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
    solveSudokuBacktracking(board, 0, 0, 0, int(emptyCells))
    return (board.gameState, board.NoOfChecks)

def isValidMove(board, row, col, number):
    ###############################################	
    # This util checks whether the number to be placed
    # is conflicting or not	
    #############################################	

    # Check all current Row
    for i in range(0, board.dimension):
	if board.gameState[row][i] == number:
	   return False

    # Check all current Col
    for i in range(0, board.dimension):
	if board.gameState[i][col] == number:
	   return False	
   
    # Check the boxes 
    startRow = (row / board.boxRow ) * board.boxRow	
    startCol = (col / board.boxCol ) * board.boxCol
    
    for i in range(0, board.boxRow):
       for j in range(0, board.boxCol):
          if board.gameState[startRow + i][startCol + j] == number:
	     return False      	 	

    return True
    
def solveSudokuBacktracking(board, startRow, startCol, filledCells, emptyCells):	
     
    if filledCells == emptyCells:
       return True
    
    #increasing no of visited nodes
    board.NoOfChecks += 1		
    
    nextRow = startRow
    nextCol = startCol + 1
	
    if nextCol == board.dimension:
       nextRow += 1
       nextCol = 0       	
	
    if board.gameState[startRow][startCol] != 0:
       return solveSudokuBacktracking(board, nextRow, nextCol, filledCells, emptyCells)

    for number in range(1, board.dimension + 1):
	if isValidMove(board, startRow, startCol, number):
	   board.gameState[startRow][startCol] = number	
	   if solveSudokuBacktracking(board, nextRow, nextCol, filledCells + 1, emptyCells):
	       return True	
	   # Backtracking.
	   board.gameState[startRow][startCol] = 0
   
    return False

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board, emptyCells = readGame.readGameState(filename)	    

    # Each element in the remainingConstraints is a [list of of remaininig constraints, flag to indicate whether its been touched for 
    # that particular iteration]

    remainingConstraints = [[[range(1, board.dimension+1), 0] for x in range(board.dimension)] for x in range(board.dimension)]
  
    # Update the neighbour constraints values.
    for i in range(board.dimension):
       for j in range(board.dimension):	    
	   updateNeighbourConstraints(board, remainingConstraints, (i, j), REMOVE)
    solveSudokuBacktrackingMRV(board, remainingConstraints, 0, emptyCells)	
    return (board.gameState, board.NoOfChecks)

def updateNeighbourConstraints(board, remainingConstraints, (row,col), operation, cellsChanged = [] ,noConflictsList = None):
    ##############################################
    # Update all conflicts of (row, col)
    #############################################	
    
    cellVal = board.gameState[row][col]
    if cellVal != 0 and operation == REMOVE:
       # Initialize it to an empty list
       remainingConstraints[row][col] = [[],0] 
    elif operation == ADD:
       # Add back the conflict list
       remainingConstraints[row][col] = [noConflictsList, 0] 

    # Check all current Row
    for i in range(0, board.dimension):
        if (cellVal in remainingConstraints[row][i][0] and operation == REMOVE):
           remainingConstraints[row][i][0].remove(cellVal)
	   cellsChanged.append((row, i))
        elif (operation == ADD and ((row,i) in cellsChanged)):
           if cellVal not in remainingConstraints[row][i][0]:
	       remainingConstraints[row][i][0].append(cellVal)
             
    # Check all current Col
    for i in range(0, board.dimension):
        if (operation == REMOVE and cellVal in remainingConstraints[i][col][0]):
           remainingConstraints[i][col][0].remove(cellVal)
           cellsChanged.append((i, col))
        elif (operation == ADD and ((i, col) in cellsChanged)):           
	   if cellVal not in remainingConstraints[i][col][0]:
	       remainingConstraints[i][col][0].append(cellVal)

    # Check the boxes 
    startRow = (row / board.boxRow) * board.boxRow
    startCol = (col / board.boxCol) * board.boxCol

    for i in range(0, board.boxRow):
       for j in range(0, board.boxCol):
          curRow = startRow + i
          curCol = startCol + j
          if (operation == REMOVE and cellVal in remainingConstraints[curRow][curCol][0]):
             remainingConstraints[curRow][curCol][0].remove(cellVal)
             cellsChanged.append((curRow, curCol))
          elif (operation == ADD and ((curRow, curCol) in cellsChanged)):
             if cellVal not in remainingConstraints[curRow][curCol][0]:
       	         remainingConstraints[curRow][curCol][0].append(cellVal)

def findMinValue(board, remainingConstraints):
    minTillNow = sys.maxint
    row = -1
    col = -1
    for i in range(0, board.dimension):
       for j in range(0, board.dimension):
          constraintsList = remainingConstraints[i][j][0]
          if constraintsList and minTillNow > len(constraintsList):
             minTillNow = len(constraintsList)
             row = i
             col = j
    
    return (row, col), remainingConstraints[row][col][0]

def solveSudokuBacktrackingMRV(board, remainingConstraints, filledCells, emptyCells):
    
    if filledCells == emptyCells:
       return True    

    #increasing number of visited nodes	 
    board.NoOfChecks += 1		 

    # Find the next minimum cell and its List.
    minCell, noConflictsList = findMinValue(board, remainingConstraints)
   
    if not noConflictsList:
        return False
    
    for number in noConflictsList:
       board.gameState[minCell[0]][minCell[1]] = number
       cellsChanged = []
       updateNeighbourConstraints(board, remainingConstraints, minCell, REMOVE, cellsChanged)
       if (solveSudokuBacktrackingMRV(board, remainingConstraints, filledCells + 1, emptyCells)):            
          return True
       # Backtracking
       	
       updateNeighbourConstraints(board, remainingConstraints, minCell, ADD, cellsChanged, noConflictsList)	
       board.gameState[minCell[0]][minCell[1]] = 0 

    return False

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
