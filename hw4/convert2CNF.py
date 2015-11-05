import sys


def parse_file(filepath):
    # read the layout file to the board array
    board = []
    fin = open(filepath)


    fin.close()
    return board

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
    # interpret the number constraints


    fout = open(output, 'w')


    fout.close()

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
    
