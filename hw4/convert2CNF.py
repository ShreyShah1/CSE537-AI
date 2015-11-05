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
    fin = open(filepath)
    boardDimensions = fileHandle.readline().strip('\n').split(' ') 
    row = int(boardDimensions[0])
    col = int(boardDimensions[1])
    board = [[0 for x in range(row)] for x in range(col)]
    	
    print " BOARD "
    print board
  
    unknownDict = {}
    clauseNo = 1
    for i in range(row):   
	rawState = fileHandle.readline().strip('\n').split(',')
	for j in range(col):
	    if (rawState[j] == 'X'):
		unknownDict[(i, j)] = clauseNo
                clauseNo += 1
	    board[i][j] = rawState[j]
	   	
    print "Unknown Dict"
    print unknownDict
    
    boardObj = Board(board, row, col, unknownDict, clausesNo)                    
    fin.close()
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
	    clauses = getAClause(board, neighbour)	       	
            if clauses not in allClauses:
	       cnfClause, totalUsedTillNow = clause_to_CNF(clauses, totalUsedTillNow - 1)  
   	       allCauses.append(claases)
               CNFClauses.append(cnfClause)	                         	
    fout = open(output, 'w')
    fout.close()

def getAClause(board, cell):
    neighbours = get_all_neighbours(board, cell[0], cell[1])
    curNo = int(board[cell[0]][cell[1]])
    totalUnknowns = 0
    for neighbour in neighbours:
       row = neighbour[0]
       col = neighbour[1]
       if board[row][col] == 'X':
           totalUnknowns += 1
    
    if curNo > totalUnknowns:
        raise ValueError('cellNo > totalUnkowns around the board is wrong state then.')
   
    finalClauseList = []
    allCombinations(totalUnknowns, curNo, [], 0, finalClauseList)
    return finalClauseList
              
def allCombinations(n, k, clauseList, clauseListTillNow, index, finalClauseList):
	####################################################################
        # Gives all possible clauses.
        # For eg. [1,2,3] n = 3 and k = 2 
        # ---> [1,2,-3], [1,-2,3], [-1,2,3]
        ##########################################################
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

def clause_to_CNF(clause, max_var):
    # Converts each clause to CNF
        
    cnf_form = []
    max_len = len(clause)
    max_num_of_clauses = max_len * max_len
     
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
