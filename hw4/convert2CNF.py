import sys
import copy

class Board(object):
    def __init__(self, board, row, col, unknowns):
    	'''
        The object contains all the properties of box object.
        '''
        self.board = board
       	self.row = row
       	self.col = col
	self.unknowns = unknowns

def parse_file(filepath):
    # read the layout file to the board array
    fin = open(filepath)
    boardDimensions = fileHandle.readline().strip('\n').split(' ') 
    row = int(boardDimensions[0])
    col = int(boardDimensions[1])
    board = [[0 for x in range(row)] for x in range(col)]
    	
    print " BOARD "
    print board
  
    unknownList = []
    for i in range(row):   
	rawState = fileHandle.readline().strip('\n').split(',')
	for j in range(col):
	    if (rawState[j] == 'X'):
		unknownList.append((i, j))
	    board[i][j] = rawState[j]
	   	
    boardObj = Board(board, row, col, unknownList)                    
    fin.close()
    return boardObj

def convert2CNF(board, output):
    # interpret the number constraints


    fout = open(output, 'w')


    fout.close()

def allCombinations(n, k, clauseList, clauseListTillNow, index, finalClauseList):
        if (k == 0):
          listToPush = copy.deepcopy(clauseListTillNow)
          ## Add all the remaining elements from index.
          for i in range(index, n):
              listToPush.append(-(clauseList[i]))
          finalClauseList.append(listToPush)
          return

        for i in range(index, n):
            clauseListTillNow.append(clauseList[i])
            allCombinations(n, k - 1, clauseList, clauseListTillNow, i + 1, finalClauseList)
            clauseListTillNow.pop()
            clauseListTillNow.append(-(clauseList[i]))

        ## Pop everything.
        for i in range(0, len(clauseList) - index):
            clauseListTillNow.pop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
