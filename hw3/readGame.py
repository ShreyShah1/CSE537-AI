##############################################
#
# In this file we have imported our game state,
# from specified command line txt file.
#
##############################################

def readGameState(filePath):
	#Reading file
	fileHandle = open(filePath, 'r')
	boardDimensions = fileHandle.readline().strip(';\n').split(',')
        dimension = int(boardDimensions[0])
	row = int(boardDimensions[1])
        col = int(boardDimensions[2])
         
	#updating game state with all 0
	sudoku = [[0 for x in range(12)] for x in range(12)]
	
	#check for dimension of given board
	if (row * col) != dimension:
		print "Wrong gameState given, check txt file"
		exit(0)
 	
        # counting number of empty spaces.
 	emptySpaces = 0 		
	#update sudoku
	for i in range(12):		
		rawState = fileHandle.readline().strip(';\n').split(',')
		for j in range(12):
			if rawState[j] == '-':
				sudoku[i][j] = 0
				emptySpaces += 1
			elif int(rawState[j]) >= 1 and int(rawState[j]) <= 12:
				sudoku[i][j] = int(rawState[j])
			else:
                                print rawState[j]
			 	print "Invalid Charachter in game state, check txt file"
				exit(0)
	
	return sudoku, emptySpaces
	
