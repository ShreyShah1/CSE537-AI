from util import memoize, run_search_function
import pprint
import sys
MAX = "MAX"
MIN = "MIN"

# Using Global variable for keeping track of count in minmax
#nodes_expanded = 0

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score

def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

def is_terminal_longest_streak_to_win(depth, board):
    """
    Longest streak to win terminal check, true when maximum depth is reached or
    the 20 moves of game has been done. 
    """
    return depth <= 0 or board.is_game_over_longest_streak()

def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    global nodes_expanded
    nodes_expanded = 0
     
    ## This setting helps us in new evaluate function for deciding whom to score ##
    board.set_current_max_player_id(board.get_current_player_id())

    tup =  recursiveMinimax(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, MAX)
    board.nodes_expanded = nodes_expanded
    return tup[0]

# Return Type (colNo, maxScore)
def recursiveMinimax(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, max_min):
    global nodes_expanded 
    nodes_expanded = nodes_expanded + 1

    if (is_terminal_fn(depth, board)):
        # -1 to indicate the terminal board case
	score = eval_fn(board)
    	return (-1, score)  
    			
    all_moves = get_next_moves_fn(board)
    # Min int value 
    curMax = -sys.maxint - 1
    # Max int value
    curMin = sys.maxint
    colNo = -1

    if (max_min == MAX):
    	# We have to maximize in this call
        for game_board in all_moves:
	   # Iterate over all moves and find the max
	   retTuple = recursiveMinimax(game_board[1], depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, MIN)
           # Saving the max till now.
           if (curMax < retTuple[1]):
	      curMax = retTuple[1]
              colNo = game_board[0]
       
	return (colNo, curMax)		    
    else:
	for game_board in all_moves:
            #Iterate over all moves to find the min.
    	   retTuple = recursiveMinimax(game_board[1], depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, MAX)
           # Saving the min till now.
           if (curMin > retTuple[1]):
	      curMin = retTuple[1]
              colNo = game_board[0]
        
	return (colNo, curMin)		    

def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]

def new_evaluate(board):
   ''' 
   This function evaluates the board with a new heuristic.
   If the opponent has one or more chains of length k(which is parameter for wining eg:4) then we simply
   return a negative value.
   Else we count the chains of the player whose score has to be maximized by 
   score = (Chains of length 2)*100 + (Chains of length 3)*1000 + (Chains of length 4)*100000 and so on.
   ''' 

   all_lengths = [-1,-1,2,3,-1,4,5,6,7]
   score = 0
   
   cur_player_chain = board.all_chains(board.get_current_max_player_id())
   other_player_chain = board.all_chains(board.get_current_min_player_id())


   if board.k in other_player_chain:
       # Treating it as loss and not surely not going ahead move
       score = -1000       
   else:
       for idx, length in enumerate(all_lengths): 
           if length in cur_player_chain:
	      ## This helps in weighing all the chains.   	
	      score += cur_player_chain[length] * pow(10,idx)     	        	       
   return score  	

random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)

progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)

''' Printing code  

if sys.stdout.encoding and 'UTF' in sys.stdout.encoding:
            print unicode(self._board)
        else:
            print str(self._board) 
'''
