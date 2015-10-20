##############################################
#
# In this file we have imported our game state,
# from specified command line txt file.
#
##############################################

class Board(object):
	def __init__(self, gameState, dimension, boxRow, boxCol):
		'''
		The object contains all the properties of box object.
		'''
        	self.gameState = gameState
                self.dimension = dimension
		self.boxRow = boxRow
                self.boxCol = boxCol
	 

def readGameState(filePath):
	#Reading file
	fileHandle = open(filePath, 'r')
	boardDimensions = fileHandle.readline().strip(';\n').split(',')
        dimension = int(boardDimensions[0])
	row = int(boardDimensions[1])
        col = int(boardDimensions[2])
         
	#updating game state with all 0
	sudoku = [[0 for x in range(dimension)] for x in range(dimension)]
	
	#check for dimension of given board
	if (row * col) != dimension:
		print "Wrong gameState given, check txt file"
		exit(0)
 	
        # counting number of empty spaces.
 	emptySpaces = 0 		
	#update sudoku
	for i in range(dimension):		
		rawState = fileHandle.readline().strip(';\n').split(',')
		for j in range(dimension):
			if rawState[j] == '-':
				sudoku[i][j] = 0
				emptySpaces += 1
			elif int(rawState[j]) >= 1 and int(rawState[j]) <= dimension:
				sudoku[i][j] = int(rawState[j])
			else:
                                print rawState[j]
			 	print "Invalid Charachter in game state, check txt file"
				exit(0)
	
	return Board(sudoku, dimension, row, col) , emptySpaces

	
