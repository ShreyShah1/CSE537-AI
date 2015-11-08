import sys
import copy
from sets import Set

class Board(object):
    def __init__(self, board, row, col, unknowns, variables):
    	'''
        The object contains all the properties of box object.
        '''
        self.board = board
       	self.row = row
       	self.col = col
	self.unknowns = unknowns
        self.totalVariablesUsed = variables

def parse_file(filepath):
    # read the layout file to the board array
    fileHandle = open(filepath)
    boardDimensions = fileHandle.readline().strip('\n').split(' ') 
    row = int(boardDimensions[0])
    col = int(boardDimensions[1])
    board = [[0 for x in range(col)] for x in range(row)]
    	
    unknownDict = {}
    clauseNo = 1
    for i in range(row):   
	rawState = fileHandle.readline().strip('\n').split(',')
	for j in range(col):
	    if (rawState[j] == 'X'):
		unknownDict[(i, j)] = clauseNo
                clauseNo += 1
	    board[i][j] = rawState[j]

    boardObj = Board(board, row, col, unknownDict, clauseNo - 1)        
    fileHandle.close()
    return boardObj

def get_all_neighbours(board , row, col):
 
    neighbours = []
    for i in range(row - 1, row + 2):
       if(i >= 0 and i < board.row):
           for j in range(col - 1, col +2): 
              if(j >=0  and j < board.col): 
		 neighbours.append([i,j])
    
    neighbours.remove([row, col])
    return neighbours     

def convert2CNF(board, output):
    # Try to maintain unique clauses.
    allClauses = Set() 
    # All CNF clauses.
    CNFClauses = []
    totalUsedTillNow = board.totalVariablesUsed

    for unknownCell in board.unknowns:
	neighbours = get_all_neighbours(board, unknownCell[0], unknownCell[1]) 
	for neighbour in neighbours:
            if board.board[neighbour[0]][neighbour[1]] != 'X':
            	clauses = getAClause(board, neighbour)	       
            	if not (clauses in allClauses):
	            cnfClause, totalUsedTillNow = clause_to_CNF(list(clauses), totalUsedTillNow)  
   	            allClauses.add(clauses)
                    CNFClauses.extend(cnfClause)	                         
    fout = open(output, 'w')
    firstLine = 'p cnf ' + str(totalUsedTillNow) + ' ' + str(len(CNFClauses))
    print >> fout, firstLine
    for i in range(0, len(CNFClauses)):
       clause = CNFClauses[i]
       curString = ''  
       for j in range(0, len(clause)):
          curString += str(clause[j])
          if (clause[j] != 0):
             curString += ' '
       print >> fout, curString	  
    fout.close()

def getAClause(board, cell):
    neighbours = get_all_neighbours(board, cell[0], cell[1])
    curNo = int(board.board[cell[0]][cell[1]])
    totalUnknownsList = []
    for neighbour in neighbours:
       row = neighbour[0]
       col = neighbour[1]
       if board.board[row][col] == 'X':
           totalUnknownsList.append(board.unknowns[(row, col)])
            
    if curNo > len(totalUnknownsList):
        raise ValueError('cellNo > totalUnkowns around the board is wrong state then.')

    finalClauseSet = Set([]) 
    allCombinations(len(totalUnknownsList), curNo, totalUnknownsList, [], 0, finalClauseSet)
    return finalClauseSet
              
def allCombinations(n, k, clauseList, clauseListTillNow, index, finalClauseSet):
	####################################################################
        # Returns a list all possible clauses.
        # For eg. [1,2,3] n = 3 and k = 2 
        # ---> ((1,2,-3), (1,-2,3), (-1,2,3))
        ##########################################################
        if (k == 0):
          listToPush = copy.deepcopy(clauseListTillNow)
          ## Add all the remaining elements from index.
          for i in range(index, n):
              listToPush.append(-(clauseList[i]))
         
          finalClauseSet.add(tuple(listToPush))
          return

        for i in range(index, n):
            clauseListTillNow.append(clauseList[i])
            allCombinations(n, k - 1, clauseList, clauseListTillNow, i + 1, finalClauseSet)
            clauseListTillNow.pop()
            clauseListTillNow.append(-(clauseList[i]))

        ## Pop everything.
        for i in range(0, len(clauseList) - index):
            clauseListTillNow.pop()

def clause_to_CNF(clause, max_var):
    # Converts each clause to CNF
        
    cnf_form = []
    max_len = len(clause)
    max_num_of_clauses = max_len * max_len
    
    if(max_len == 1):
      for i in range(0, len(clause[0])):
           subclause=[]
           subclause.append(clause[0][i])
           subclause.append(0)
           cnf_form.append(subclause)
      return cnf_form, max_var
     
    subclause =[]

    for i in range(1, max_len + 1):
       subclause.append(max_var + i)

    subclause.append(0)
    cnf_form.append(subclause)
    
    len_of_clause = len(clause[0])
    add =1
      
    for i in range(0, max_len):

        for j in range(0, len_of_clause):
            subclause =[]
            subclause.append(0- max_var - add)
            subclause.append(clause[i][j])
            subclause.append(0)
            cnf_form.append(subclause)

        add += 1            
           
    return cnf_form, max_var + add -1

if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
