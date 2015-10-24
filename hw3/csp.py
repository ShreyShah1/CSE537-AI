import readGame
import sys
from collections import deque
from pprint import pprint
import copy
import random
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
    if (False == solveSudokuBacktracking(board, 0, 0, 0, int(emptyCells))):
        return (" ERROR --> Board Not Solvable", 0 )
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

    remainingConstraints = [[[range(1, board.dimension + 1), 0] for x in range(board.dimension)] for x in range(board.dimension)]
  
    # Update the neighbour constraints values.
    for i in range(board.dimension):
       for j in range(board.dimension):	    
	   updateNeighbourConstraints(board, remainingConstraints, (i, j), REMOVE)
    if (False == solveSudokuBacktrackingMRV(board, remainingConstraints, 0, emptyCells)):
       	   return (" ERROR --> Board Not Solvable", 0 )
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
          if ((board.gameState[i][j] == 0 or constraintsList) and minTillNow > len(constraintsList)):
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
    board, emptyCells = readGame.readGameState(filename)	    

    # Each element in the remainingConstraints is a [list of of remaininig constraints, flag to indicate whether its been touched for 
    # that particular iteration]

    remainingConstraints = [[[range(1, board.dimension + 1), 0] for x in range(board.dimension)] for x in range(board.dimension)]
  
    # Update the neighbour constraints values.
    for i in range(board.dimension):
       for j in range(board.dimension):	    
	   updateNeighbourConstraints(board, remainingConstraints, (i, j), REMOVE)
    if (False == solveSudokuBacktrackingMRVfwd(board, remainingConstraints, 0, emptyCells)):
       	   return (" ERROR --> Board Not Solvable", 0 )
    return (board.gameState, board.NoOfChecks)

def forwardChecking(board, remainingConstraints ,cellsChanged):
    for cell in cellsChanged:
       if (board.gameState[cell[0]][cell[1]] == 0 and len(remainingConstraints[cell[0]][cell[1]][0]) == 0):
           return False
    return True

def solveSudokuBacktrackingMRVfwd(board, remainingConstraints, filledCells, emptyCells):
    
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

       if (False == forwardChecking(board, remainingConstraints, cellsChanged)):
          #Backtrack and return.
          updateNeighbourConstraints(board, remainingConstraints, minCell, ADD, cellsChanged, noConflictsList)	
          board.gameState[minCell[0]][minCell[1]] = 0
          return False 

       if (solveSudokuBacktrackingMRVfwd(board, remainingConstraints, filledCells + 1, emptyCells)):            
          return True

       # Backtracking
       updateNeighbourConstraints(board, remainingConstraints, minCell, ADD, cellsChanged, noConflictsList)	
       board.gameState[minCell[0]][minCell[1]] = 0 

    return False

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
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
    if (False == solveSudokuBacktrackingMRVcp(board, remainingConstraints, 0, emptyCells)):  
         return (" ERROR --> Board Not solvable ", 0)	
    return (board.gameState, board.NoOfChecks)   

def putAllArcs(board, (row, col), queue):
    # Put all rows.
    for i in range(0, board.dimension):
       arc = [(row, i), (row, col)]
       if (arc not in queue and i != col):
          queue.append(arc) 

    # Put all Cols.
    for i in range(0, board.dimension):
       arc = [(i, col), (row, col)]
       if (arc not in queue and i != row):
          queue.append(arc)
   
    # Put all boxes.
    startRow = (row / board.boxRow) * board.boxRow
    startCol = (col / board.boxCol) * board.boxCol

    for i in range(0, board.boxRow):
       for j in range(0, board.boxCol):
          curRow = startRow + i
          curCol = startCol + j
	  arc = [(curRow, curCol), (row, col)]
          if (arc not in queue and curRow != row and curCol != col):
               queue.append(arc)

def removeConstraintPropagation(board, remainingConstraints, cell, contraintCellsChanged):
    queue = deque() 
    # Put all the neighbours in queue
    putAllArcs(board, cell, queue)

    # Remove all the constraints and add new neighbours if required.	
    while len(queue) != 0:
       # arc is made up of (x --> y)
       arc = queue.popleft()
       # This means x --> y if the element in y is present in x the definitely we have to remove it.
       x = remainingConstraints[arc[0][0]][arc[0][1]][0]
       y = remainingConstraints[arc[1][0]][arc[1][1]][0]
       if (len(y) != 0 and y[0] in x):
          x.remove(y[0])
          			#(valueChanged, cell)
          contraintCellsChanged.append([y[0], arc[0]])
       	  # Just push all the arc's only if the we can make decision i.e len == 1   
          if (len(x) == 1):
          	putAllArcs(board, arc[0], queue)
	   
def addConstraintPropagation(board, remainingConstraints, constraintsCellsChanged):
    for val_cell in constraintsCellsChanged:
       row = val_cell[1][0]
       col = val_cell[1][1]
       remainingConstraints[row][col][0].append(val_cell[0])

def solveSudokuBacktrackingMRVcp(board, remainingConstraints, filledCells, emptyCells): 
    if filledCells == emptyCells:
       return True    
   
    #increasing no of visited nodes
    board.NoOfChecks += 1
    
    # Find the next minimum cell and its List.
    minCell, noConflictsList = findMinValue(board, remainingConstraints)
   
    if not noConflictsList:
        return False
    
    for number in noConflictsList:
       board.gameState[minCell[0]][minCell[1]] = number
       cellsChanged = []
       constraintCellsChanged = []
       updateNeighbourConstraints(board, remainingConstraints, minCell, REMOVE, cellsChanged)
       # Checking the constraint Propagation here.
       for cell in cellsChanged:
           if (len(remainingConstraints[cell[0]][cell[1]][0]) == 1):
       		removeConstraintPropagation(board, remainingConstraints, cell, constraintCellsChanged) 

       if (solveSudokuBacktrackingMRVcp(board, remainingConstraints, filledCells + 1, emptyCells)):            
          return True
       # Backtracking
       	
       addConstraintPropagation(board, remainingConstraints, constraintCellsChanged)
       updateNeighbourConstraints(board, remainingConstraints, minCell, ADD, cellsChanged, noConflictsList)	
       board.gameState[minCell[0]][minCell[1]] = 0 

    return False

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    board, emptyCells = readGame.readGameState(filename)	    

    pprint(board.gameState)
    board, originalGameState = randomAssignmentOfValues(board) 
  
    print "random"
    pprint(board.gameState)
	 
    conflict_list = []
    conflictBoard = [[0 for x in range(board.dimension)] for x in range(board.dimension)] 
    noOfConflicts, conflict_list = calculateNoOfConflicts(board, originalGameState, conflictBoard)
    

    while(noOfConflicts != 0):
	num = random.randint(0, len(conflict_list)-1)
	row = conflict_list[num][0]
	col = conflict_list[num][1]
	
	minConflict = conflictBoard[row][col]
        val = board.gameState[row][col]
	val_list = []
        val_list.append(val)
        if(originalGameState[row][col] == 0 and conflictBoard[row][col]!= 0 ):
		for i in range(1, board.dimension + 1):
                     if i != board.gameState[row][col]:			
	                 curConflict = checkNeighborConflicts(board, row, col, i)
                         if (minConflict > curConflict):
                              minConflict = curConflict
                              val = i
			      del val_list[:]
			      val_list.append(i)
			 elif (minConflict == curConflict):
			      val_list.append(i)
		if(board.gameState[row][col] in val_list):
			val_list.remove(board.gameState[row][col])
			
			if(len(val_list) != 0):
			    board.gameState[row][col] = random.choice(val_list)
			"""else:
			    minC = -1
			    for i in range(1, board.dimension + 1):
                   		if i != board.gameState[row][col]:			
	                	        curConflict = checkNeighborConflicts(board, row, col, i)
					if(minC == -1):
						minC = curConflict
			                elif(minC > curConflict):
						minC = curConflict
						del val_list[:]
						val_list.append(i)
	        			elif(minC == curConflict):
						val_list.append(i)
                            board.gameState[row][col] = random.choice(val_list)"""
                else:
        		board.gameState[row][col] = val
		
                noOfConflicts, conflict_list = calculateNoOfConflicts(board, originalGameState, conflictBoard)
	
    return (board.gameState, 0)

def randomAssignmentOfValues(board):
    ###
    # Randomly assign values in empty cells
    ###

    originalGameState = copy.deepcopy(board.gameState) 

    for x in range(0, board.dimension):
	for y in range(0, board.dimension):
	    if(board.gameState[x][y] == 0):
		#board.gameState[x][y] = random.randint(1, board.dimension)
		val_list = [ v for v in range(1, board.dimension + 1)]
   
		for i in range(0, board.dimension):
		    if(originalGameState[x][i] in val_list): 
			val_list.remove(originalGameState[x][i]) 

		for i in range(0, board.dimension):
		    if(originalGameState[i][y] in val_list): 
			val_list.remove(originalGameState[i][y]) 

		startRow = (x / board.boxRow) * board.boxRow
    		startCol = (y / board.boxCol) * board.boxCol
		for i in range(startRow, startRow+board.boxRow):
                    for j in range(startCol, startCol+board.boxCol):
         	        if(originalGameState[i][j] in val_list):
                              val_list.remove(originalGameState[i][j])
                if(len(val_list) != 0):	
		     board.gameState[x][y] = random.choice(val_list)
	
    return board, originalGameState

def calculateNoOfConflicts(board, originalGameState, conflictBoard):
    ###
    # Calculate number of conflicts for given assignment of values
    ###
    
    noOfConflicts = 0
    conflict_list = []
    for x in range(0, board.dimension):
	for y in range(0, board.dimension):
	   if(originalGameState[x][y] == 0):
                 conflictBoard[x][y] = checkNeighborConflicts(board, x, y, board.gameState[x][y]) 
	         noOfConflicts += conflictBoard[x][y]
                 if(conflictBoard[x][y] != 0):
			conflict_list.append((x,y))
    return noOfConflicts, conflict_list
     		

def checkNeighborConflicts(board, x, y, value):
    ###
    # Check no of conflicts for particular cell
    ###
    noOfConflicts = 0
   
    for i in range(0, board.dimension):
	if(value == board.gameState[i][y] and x != i):
    	    noOfConflicts += 1
 
    for i in range(0, board.dimension):
	if(value == board.gameState[x][i] and y != i):
    	    noOfConflicts += 1 
      
    startRow = (x / board.boxRow) * board.boxRow
    startCol = (y / board.boxCol) * board.boxCol
    for i in range(startRow, startRow+board.boxRow):
        for j in range(startCol, startCol+board.boxCol):
         	if(value == board.gameState[i][j] and x != i and y != j):
			noOfConflicts += 1
    return noOfConflicts
