# Assignment 2
# Team members: Yee Sern Tan, Damodar Panigrahi and Subramanian Venkatesan
# For implement n-k-coh-coh, the number of possible cases grow very large very rapidly
# therefore we have decided to limit our search to depth one, 
# but with consideration of how the opponent can move next,
# making it depth 2 in some sense.
# The main move decision is in the function move_AI, consisting of three different ways to move:
# move_best - the best algorithm
# move_simple - a simple algorithm
# move_any - an algorithm that takes just any move.
# move_simple makes moves by considering the result of each move,
# using the number and types of immediate neighbors.
# It is implemented with a heuristic.
# For an intuition of move_best, consider number of possible moves that will result in defeat,
# after making the move. We call it forbidden moves.
# The intuition is that when a player runs out of possible moves that do not result in defeat,
# it will lose.
# move_best considers both the consequence for self on placing on each location, and the
# "opportunity cost" for the opponent if a piece is placed on that location.
# After each move, the number of forbidden moves for self can only increase, and this number
# for the opponent can only decrease.
# For each possible placement, we scan in four directions: horizontal, vertical and two diagonals,
# the number of forbidden moves introduced to self plus the number deducted to opponent.
# We rank it the lesser the better. 
# Then we consider moves that will likely introduce forbidden moves.
# For example, when k=4, there will be forbidden moves when there are 3 piece in a contiguous
# straight line of 4 positions. Such situations can be introduced only if the following hold:
# 1. There is no opponent piece blocking the contiguous straight line.
# 2. There are already 2 pieces of self in this contiguous straight line.
# Thus if condition 1 holds, we reduce the number of situations where condition 2 holds.
# For the general case, we will evaluate in the following order:
# k, k-1, k-2, k-3 ...
# When there are ties on two placement locations, we select at random.
# Experimentally, selecting the first in each tie will lead to unfavorable outcomes.
# When the time runs out, move_best and move_simple will terminate, but move_any has to continue.
# Move_any is so simple, it only scans the whole board for positions that can be placed,
# and selects one at random.
# The preferred move is move_best, followed by move_simple, and finally move_any.
import sys
import copy
import numpy as np

from multiprocessing import Process, Value, Lock

piece_types = ['b','w','.']
is_player1_using_AI = True
is_player2_using_AI = True
# helper_mode uses AI to not make moves but only to help suggest decisions to humans
helper_mode = True
# for assignment requirement, set this to True
assignment_mode = True

# ensure proper arguments received. if proper arguments aren't specified then provide instruction 
#for proper usage
if (len(sys.argv) < 5):
    print 'Enter proper parameters.'
    print 'Usage: python nkcohcoh.py [n] [k] [state] [time_limit]'
    exit()
else:
    # global variables
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    state = sys.argv[3]
    time_limit = float(sys.argv[4])
    if n < k:
        print 'Enter proper parameters.'
        print 'n must not be less than k. Please retry.'
        exit()
    elif len(state) != n**2:
        print 'Enter proper parameters.'
        print 'The length of state must be n**2. Please retry.'
        exit()
    else:
        for piece in state:
            if piece not in piece_types:
                print 'Enter proper parameters.'    
                print 'state can contain only "b", "w" and ".". Please retry.'
                exit()

#creates list of lists (the inside list consists of the state of each row)
#from the board provided as an argument, state, to the program                
def convert_to_array(state):
    if len(state) != n**2:
        print "Error: state size"
        return
    pos = 0
    state_list = list(state)
    array = []
    while pos < len(state):
        array.append(state_list[pos:pos+n])
        pos += n
    return array

#creates a string from a list of lists (the inside list consists of the state of each row)
def convert_to_string(array):
    if len(array) != n:
        print "Error: array size"
        return
    string = ""
    for row in array:
        if len(row) != n:
            print "Error: array size"
            return
        for element in row:
            string += str(element)
    return string
    
# checks whether a move is valid
def is_valid_move(array, row, col):
    if array[row][col] == '.':
        return True
    return False
    
# returns whether the game is finished
def game_finished(array):
    for row in array:
        for element in row:
            if element == '.':
                return False
    return True    
            
# global variables
# initiates current_array
current_array = convert_to_array(state)
__WHITE__ = 0
__BLACK__ = 1

# extracts a list of the positions of black or white pieces
def extract(array, piece_type):
    pos = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == piece_type:
                pos.append([i, j])
    return pos

# assignment requirement: makes one move and prints the board
# and after that check if the game is lost
def play_assignment():
    white_positions = extract(state, 'w')
    black_positions = extract(state, 'b')
    whose_turn = len(white_positions) - len(black_positions)
    if whose_turn != 0 and whose_turn != 1:
        print "Error. Number of white and black pieces don't tally."
        exit()
    retry_count = 0

    print 'Thinking! Please wait...'
    move_AI(current_array, whose_turn, retry_count)
    default_player = "black"
    if whose_turn == __WHITE__:
        default_player = "white"

    if not check_ok(whose_turn):
        #print "Player 1 (", default_player, ") lost."
        print default_player, "lost."
   
# two players, human or AI, play against each other
def play():
    white_positions = extract(state, 'w')
    black_positions = extract(state, 'b')
    whose_turn = len(white_positions) - len(black_positions)
    if whose_turn != 0 and whose_turn != 1:
        print "Error. Number of white and black pieces don't tally."
        exit()
#     while not game_finished(current_array):
    retry_count = 0
    if whose_turn == __WHITE__:
        if not helper_mode and not is_player1_using_AI:
            current_move = prompt_move(whose_turn, retry_count)
            move(current_array, current_move, whose_turn)
        else: # AI decide/suggest
            move_AI(current_array, whose_turn, retry_count)
        if not check_ok(whose_turn):
            print "Player 1 (white) lost."
            print "The board is {}".format(convert_to_string(current_array))
            exit()
        whose_turn = __BLACK__
    elif whose_turn == __BLACK__:
        if not helper_mode and not is_player2_using_AI:
            current_move = prompt_move(whose_turn, retry_count)
            move(current_array, current_move, whose_turn)
        else: # AI decide/suggest
            move_AI(current_array, whose_turn, retry_count)
        if not check_ok(whose_turn):
            print "Player 2 (black) lost."
            print "The board is {}".format(convert_to_string(current_array))
            exit()
        whose_turn = __WHITE__
            
# prompt user response
def prompt_move(whose_turn, retry_count, suggestion=""):
    if whose_turn == __WHITE__:
        info1 = "You are playing as white"
    else:
        info1 = "You are playing as black"
    info2 = "The board is {}".format(convert_to_string(current_array))
    print info1
    print info2
    if len(suggestion) == 0:
        user_input = raw_input("It is your turn to move.")
    else:
        user_input = raw_input(suggestion)
    current_move = int(user_input)
    # valid user moves must be between 0 and n**2, and must not be already occupied by another piece
    if current_move < 0 or current_move >= n**2 or not is_valid_move(current_array, current_move/n, current_move%n):
        print "Invalid move."
        if retry_count > 5:
            print "You have exceeded the number of retries. Please start again."
            exit()
        else:
            print "Please retry."
            retry_count += 1
            current_move = prompt_move(whose_turn, retry_count, "")
    return current_move
    
# changes current state by making a move
def move(array, current_move, whose_turn):
    if whose_turn == __WHITE__:
        array[current_move/n][current_move%n] = 'w'
    if whose_turn == __BLACK__:
        array[current_move/n][current_move%n] = 'b'

# check whether the player loses after the turn        
def check_ok(whose_turn):
    if whose_turn == __WHITE__:
        positions = extract(current_array, 'w')
    else:
        positions = extract(current_array, 'b')
    
    if not check_horizontal(positions):
        return False
    if not check_vertical(positions):
        return False
    if not check_diag1(positions):
        return False
    if not check_diag2(positions):
        return False
    return True
    
def check_horizontal(positions):
    for i in range(len(positions)):
        row = positions[i][0]
        current_col = positions[i][1]
        my_iter = 1
        while my_iter < k and i < len(positions) - 1:
            i = i + 1
            current_col += 1
            if row != positions[i][0] or current_col != positions[i][1]:
                break
            my_iter += 1
        if my_iter >= k:
            return False
    return True
    
def check_vertical(positions):
    for i in range(len(positions)):
        current_row = positions[i][0]
        col = positions[i][1]
        my_iter = 1
        current_row += 1
        for j in range(len(positions)):
            if current_row == positions[j][0] and col == positions[j][1]:
                my_iter += 1
                current_row += 1
            if positions[j][0] > current_row:
                break
        if my_iter >= k:
            return False
    return True
    
def check_diag1(positions):
    for i in range(len(positions)):
        current_row = positions[i][0]
        current_col = positions[i][1]
        my_iter = 1
        current_row += 1
        current_col += 1
        for j in range(len(positions)):
            if current_row == positions[j][0] and current_col == positions[j][1]:
                my_iter += 1
                current_row += 1
                current_col += 1
            if positions[j][0] > current_row:
                break
        if my_iter >= k:
            return False
    return True
    
def check_diag2(positions):
    for i in range(len(positions)):
        current_row = positions[i][0]
        current_col = positions[i][1]
        my_iter = 1
        current_row += 1
        current_col -= 1
        for j in range(len(positions)):
            if current_row == positions[j][0] and current_col == positions[j][1]:
                my_iter += 1
                current_row += 1
                current_col -= 1
            if positions[j][0] > current_row:
                break
        if my_iter >= k:
            return False
    return True
    
# shape of claw
# \|/
# -*-
# /|\
# the claw consists of subarrays of positions 
# within the vicinity of k consecutive positions from position i,j
def claw(current_array, i, j, whose_turn):
    y_min = i - (k - 1)
    y_max = i + (k - 1)
    x_min = j - (k - 1)
    x_max = j + (k - 1)
    if y_min < 0:
        y_min = 0
    if y_max > n - 1:
        y_max = n - 1
    if x_min < 0:
        x_min = 0
    if x_max > n - 1:
        x_max = n - 1
        
    copy_array = copy.deepcopy(current_array)
    # putatively place the piece at i, j and generate the claw
    if whose_turn == __WHITE__:
        copy_array[i][j] = 'w'
    else:
        copy_array[i][j] = 'b'
    sub_claw = []
    # sub_claw of horizontal elements
    sub_claw = [element for element in copy_array[i][x_min:x_max+1]]
    total_claw = [sub_claw]
    # sub_claw of vertical elements
    sub_claw = [row[j] for row in copy_array[y_min:y_max+1]]
    total_claw.append(sub_claw)
    # sub_claw of \ diagonal elements
    y_min = i - (k - 1)
    y_max = i + (k - 1)
    x_min = j - (k - 1)
    x_max = j + (k - 1)
    sub_claw = []
    for i_sub in range(y_min,y_max+1):
        j_sub = j + i_sub - i
        if j_sub in range(0,n) and i_sub  in range(0,n):
            sub_claw.append(copy_array[i_sub][j_sub])
    total_claw.append(sub_claw)
    # sub_claw of / diagonal elements
    sub_claw = []
    for i_sub in range(y_min,y_max+1):
        j_sub = j - i_sub + i
        if j_sub in range(0,n) and i_sub in range(0,n):
            sub_claw.append(copy_array[i_sub][j_sub])
    total_claw.append(sub_claw)
    return total_claw
    
# returns a list of number of dangerous situations 
# ordered by descending severity
# when the claw is evaluated
def score_claw(current_claw, whose_turn):
    if whose_turn == __WHITE__:
        own = 'w'
        opponent = 'b'
    else:
        own = 'b'
        opponent = 'w'
    score = [0] * (k+1)
    for sub_claw in current_claw:
        for i in range(len(sub_claw)-k+1):
            window = sub_claw[i:i+k]
            if opponent in window or own not in window:
                continue
            count = k
            for piece in window:
                if piece == own:
                    count -= 1
            score[count] += 1
    return score
        
# compares score1 versus score2
def compare_score(score1, score2):
    index = 0
    while index <= k and score1[index] == score2[index]:
        index += 1
    # the scores are equal
    if index > k:
        return 0
    # score2 is more dangerous
    if score1[index] < score2[index]:
        return 1
    # score1 is more dangerous
    if score1[index] > score2[index]:
        return -1
        
# takes any move, e.g. when there is no time or all moves result in direct defeat
def any_move(current_array, whose_turn, v_any, lock):
    possible_moves = extract(current_array,'.')
    num_possibility = len(possible_moves)
    if len(possible_moves) == 1:
        selected = 0
    else:
        selected = np.random.randint(0, num_possibility-1)
    with lock:
        v_any.value = possible_moves[selected][0]*n + possible_moves[selected][1]
    
    return 
                
# simple decision that speeds up running time
def simple_move(current_array, whose_turn, v_simple, v_simple_done, lock):
    simple_heuristic = 24
    simple_moves = []
    for i in range(n):
        for j in range(n):
            if current_array[i][j] != '.':
                continue
            heuristic = 24
            if len(simple_moves) == 0:
                simple_moves.append([i, j])
            for i_neighbor in range(i-1,i+2):
                for j_neighbor in range(j-1,j+2):
                    if i_neighbor == i and j_neighbor == j:
                        continue
                    if i_neighbor not in range(0,n) or j_neighbor not in range(0,n):
                        heuristic -= 1
                        continue
                    if current_array[i_neighbor][j_neighbor] != '.':
                        heuristic += 2
            if heuristic < simple_heuristic:
                simple_heuristic = heuristic
                simple_moves = [[i, j]]
            elif heuristic == simple_heuristic:
                simple_moves.append([i,j])
    # if simple_move won't do better than any_move
    if simple_heuristic == 24:
        return
    if len(simple_moves) == 1:
        selected = 0
    else:
        selected = np.random.randint(0, len(simple_moves)-1)   
    with lock:
        v_simple.value = simple_moves[selected][0]*n + simple_moves[selected][1]
        v_simple_done.value = True
    
    return

# our best algorithm for determining moves
def best_move(current_array, whose_turn, v_best, v_best_done, lock):
    best_moves = []
    if whose_turn == __WHITE__:
        opponent = __BLACK__
    else:
        opponent = __WHITE__
    best_score = [0] * (k+1)
    # initialize best_score
    best_score[0] = 1
    for i in range(n):
        for j in range(n):
            if not is_valid_move(current_array, i, j):
                continue
            own_claw = claw(current_array, i, j, whose_turn)
            own_score = score_claw(own_claw, whose_turn)
            # a move that results in defeat
            if own_score[0] > 0:
                continue
            opponent_claw = claw(current_array, i, i, opponent)
            opponent_score = score_claw(opponent_claw, opponent)
            # compares the opportunity score of own versus opponent placing a marble piece at i,j
            current_score = [own_index + opponent_index for own_index, opponent_index in zip(own_score, opponent_score)]
            comparison = compare_score(current_score, best_score)
            # do not use current i,j
            if comparison == -1:
                continue
            # add i,j into the list for consideration
            elif comparison == 0:
                best_moves.append([i, j])
            # a new best move is found
            elif comparison == 1:
                best_moves = [[i,j]]
                best_score = current_score
    # all moves result in defeat
    if len(best_moves) == 0:
        return
    # select a random best move
    if len(best_moves) == 1:
        selected = 0
    else:
        selected = np.random.randint(0,len(best_moves)-1)
    with lock:
        v_best.value = best_moves[selected][0]*n + best_moves[selected][1]
        v_best_done.value = True
            
    return

#Multi-threading python syntaxes was referred from the following discussion group:
#ATOzTOA. (2013, Feb 17). Timeout on a function call.
#    Retrieved from http://stackoverflow.com/questions/492519/timeout-on-a-function-call

def move_AI(current_array, whose_turn, retry_count):
    
    # Start bar as three processes
    v_best = Value('i', 0)
    v_best_done = Value('i', False)
    v_simple = Value('i', 0)
    v_simple_done = Value('i', False)
    v_any = Value('i', False)
    lock = Lock()

    p_best = Process(target=best_move, args=(current_array, whose_turn, v_best, v_best_done, lock))
    p_simple = Process(target=simple_move, args=(current_array, whose_turn, v_simple, v_simple_done, lock))
    p_any = Process(target=any_move, args=(current_array, whose_turn, v_any, lock))
    
    p_best.start()
    p_simple.start()
    p_any.start()
    
    p_best.join(time_limit)
    p_simple.join(time_limit)
    # any_move must complete or else there will be no move to take
    p_any.join()
    
    if v_best_done.value == True:
#         print "here1"
        take_move = [v_best.value/n, v_best.value%n]
    elif v_simple_done.value == True:
#         print "here2"
        take_move = [v_simple.value/n, v_best.value%n]
    else:
#         print "here3"
        take_move = [v_any.value/n, v_best.value%n]
     
    if assignment_mode:
        current_move = take_move[0]*n + take_move[1]
        move(current_array, current_move, whose_turn)
        print 'New board:'
        print convert_to_string(current_array)
        return
         
#     print 'moved_best:', moved_best, ', moved_simple:', moved_simple, ',take_move:', take_move
    if helper_mode:
        recommendation_string = 'Hmm, I''d recommend putting your marble at row ' + str(take_move[0]+1) + ', column ' + str(take_move[1]+1) + '.'
        recommendation_string += "\n Please decide your move:"
        current_move = prompt_move(whose_turn, retry_count, recommendation_string)
        move(current_array, current_move, whose_turn)
    else:
        current_move = take_move[0]*n + take_move[1]
        move(current_array, current_move, whose_turn)
    return

if __name__ == '__main__':
    # Start bar as a process
    if assignment_mode:
        play_assignment()
    else:
        play()

