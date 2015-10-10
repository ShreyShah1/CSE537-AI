# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY
global nodes_expanded_alpha_beta
    
### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 0

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 0

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(new_player, basic_player)
## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

## This is for varying k.
#run_game(new_player, human_player, ConnectFourBoard(k = 5))

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):

    	#print "CurDepth is " + str(depth)		
	# Min int value 
	Min = -sys.maxint - 1
	# Max int value
        Max = sys.maxint
        
        global nodes_expanded_alpha_beta
        nodes_expanded_alpha_beta = 0
        ## Saving the current Max Player id ##
        board.set_current_max_player_id(board.get_current_player_id())

	tup =  recursiveAlphaBeta(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, MAX, Min, Max)
        board.nodes_expanded = nodes_expanded_alpha_beta
   	print " Number of expanded nodes " +  str(nodes_expanded_alpha_beta)
   	return tup[0]
	
# Return Type (colNo, maxScore)
def recursiveAlphaBeta(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, max_min,alpha, beta):
    
    global nodes_expanded_alpha_beta
    nodes_expanded_alpha_beta = nodes_expanded_alpha_beta + 1
#    print " Alpha = " + str(alpha) + " Beta = " + str(beta) + " Label = " + str(board.label)
    if (is_terminal_fn(depth, board)):
        # -1 to indicate the terminal board case
	score = eval_fn(board)
    	return (-1, score) 

    # Get all its next moves:
    all_moves = get_next_moves_fn(board)
    colNo = -1

    if (max_min == MAX):
    	# We have to maximize in this call
        for game_board in all_moves:
	   # Iterate over all moves and update alpha.

	   retTuple = recursiveAlphaBeta(game_board[1], depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, MIN, alpha, beta)
##	   print "Got tuples" + str(retTuple)
	      
           if (alpha < retTuple[1]):
	      alpha = retTuple[1]
              colNo = game_board[0]
           if (alpha > beta):
               # print " # Pruning here with alpha " + str(alpha) + " Beta " + str(beta)
                break
 
#        print "Returning " + str((colNo, curMax)) 
	return (colNo, alpha)		    
    else:
	for game_board in all_moves:
            #Iterate over all moves to find the min.
    	   retTuple = recursiveAlphaBeta(game_board[1], depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, MAX, alpha, beta)
	  
           if (beta > retTuple[1]):
	      beta = retTuple[1]
              colNo = game_board[0]
            
           if (alpha > beta):
              #print " # Pruning here with alpha " + str(alpha) + " Beta " + str(beta)
              break
 
	return (colNo, beta)

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate)

longest_streak_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate, is_terminal_fn=is_terminal_longest_streak_to_win)

## This is the longest streak run function
##run_game(longest_streak_player, longest_streak_player, ConnectFourBoard(streak = True))
#run_game(longest_streak_player,random_player, ConnectFourBoard(streak = True))

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
run_game(alphabeta_player, basic_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""

