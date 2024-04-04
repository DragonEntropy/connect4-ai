# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/7/

import sys
import math
import numpy as np

def opponent(player):
    if player == "red":
        return "yellow"
    elif player == "yellow":
        return "red"
    else:
        print("Invalid player colour: must be yellow or red")
        return 

def player_to_index(player):
    if player == "red":
        return 0
    elif player == "yellow":
        return 1
    else:
        # print("Invalid player colour: must be yellow or red")
        return

def colour_to_char(player):
    if player == "red":
        return 'r'
    elif player == "yellow":
        return 'y'
    else:
        # print("Invalid player colour: must be yellow or red")
        return

# def tokens_in_row(count, player_i, total_counts):
#     try:
#         return total_counts[(player_i, count)]
#     except KeyError:
#         # print(f"invalid count valid given: Key {(player_i, count)}")
#         return

# def update_count(adjacent_count, player_i, total_counts):
#     if adjacent_count > 4:
#         adjacent_count = 4
#     try:
#         total_counts[(player_i, adjacent_count)] += 1
#     except KeyError:
#         # print(f"invalid adjacent count: Key {(player_i, adjacent_count)}")
#         return

def blank_setup(state, row, col):
    # don't check for valid input - will waste time in tournament # TODO: delete this input validity check once code is working
    if row < 0 or row > 5 or col < 0 or col > 6:
        print("invalid input")
        return
    if row == 0:
        return True
    return not state[row-1, col] == '.'

def segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_setup_count):
    # calculate factors
    blanks_setup_factor = 1 + 0.2*(blanks_setup_count/blanks_count)
    token_edge_factor = 1 + 0.5*(edges_count/(tokens_count-1))
    return (1.5*tokens_count + blanks_count) * blanks_setup_factor * token_edge_factor

# TODO: optimise traversals 
def state_heuristic(state: np.matrix, player: str): 

    # red counts - store separately for purpose of analysing our heuristic
    red_row_heuristic_sum = 0
    red_col_heuristic_sum = 0
    red_pos_diag_heuristic_sum = 0
    red_neg_diag_heuristic_sum = 0

    # yellow counts
    yel_row_heuristic_sum = 0
    yel_col_heuristic_sum = 0
    yel_pos_diag_heuristic_sum = 0
    yel_neg_diag_heuristic_sum = 0
    
    # players' total counts (calc at end)
    red_total_heuristic = 0
    yel_total_heuristic = 0

    # players' difference: state heuristic (calc & returned at end)
    state_heuristic = 0

    # COLUMN TRAVERSALS 
    for col in range(7):
        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        consecutive_blanks = 0 # used for when segment changes player (overlap section of segments)
        blanks_setup_count = 0 # count the num blanks setup - ie able to have a token placed there without requiring below positions to be filled with tokens
        setup_count_of_consecutive_blanks = 0

        for row in range(6):
            val = state[row, col]
            # val is a blank - update variables the same way no matter current_segment_colour
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_setup(state, row, col):
                    blanks_setup_count += 1
                    setup_count_of_consecutive_blanks +=1 

            elif current_segment_colour == "red":
                if val == '.':
                    segment_len += 1
                    blanks_count += 1
                    consecutive_blanks += 1
                    if blank_setup(state, row, col):
                        blanks_setup_count += 1
                        setup_count_of_consecutive_blanks +=1
                elif val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    setup_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_setup_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_setup_count = setup_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    setup_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":
                if val == '.':
                    segment_len += 1
                    blanks_count += 1
                    consecutive_blanks += 1
                    if blank_setup(state, row, col):
                        blanks_setup_count += 1
                        setup_count_of_consecutive_blanks +=1                
                elif val == 'r':
                elif val == 'y':
                
                else:
                    print("invalid matrix character")
            
            elif current_segment_colour == "":
                if val == '.':
                
                elif val == 'r':
                
                elif val == 'y':
                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")


            if val == 'r':


            # optimising case: if a position is empty, all above positions are
            if val == '.':
                # TODO: optimise - complete this column data within this loop (given all above are blanks) & break to next col
                break

            # update previous val
            prev_val = val
            
    # HORIZONTAL/ROW TRAVERSALS 
    for row in range(6):
        # variables to update each row
        empty_row = False
        for col in range(7):
            # optimising case: if a row is empty, all above rows don't need to be traversed
            if empty_row:
                break
            val = state[row, col]

            # TODO: set row to empty if all blanks
    
    # NEGATIVE DIAGONAL TRAVERSALS (negative gradient) -> decrease row (down) and increase column (right)
    
    min_col = 0 # for optimisaton: if a given column has a lower elemnt found empty, all above are empty 
    # starting col = 0
    for col in range(0,7):
        # neg diag part 1: initial row is always 0 (blue)
        row = 0
        initial_col = col
        # variable for optimisation
        empty_diag = True
        while row <= 5 and col >= min_col:
            val = state[row, col]

            
            # TODO: set diag to false if token found

            # update row and column to continue down the diagonal
            col -= 1 # left
            row += 1 # up
        # set as empty diag if empty - or just change min_col
        if empty_diag:
            min_col = initial_col + 1

    # starting row = 5
    for col in range(2,7):
        # neg diag part 2: initial row always 5 (purple)
        row = 5
        empty_diag = True
        while col <= 6:
            val = state[row, col]

            # TODO: set empty_diag to False if a token is found on any iteration
        

            col += 1 # right
            row -= 1 # down
        if empty_diag:
            break

    # POSITIVE DIAGONAL TRAVERSALS
    max_col = 6
    for col in range(6, -1, -1): # 6, 5, 4, 3, 2, 1, 0
        row = 0
        initial_col = col
        empty_diag = True # keep true if no tokens are found
        while row <= 5 and col <= max_col:
            val = state[row, col]

            # TODO: set empty_diag to False if a token is found on any iteration

            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up
        
        if empty_diag:
            max_col = initial_col - 1

    for row in range(0,5):
        col = 0
        empty_diag = True
        while row <= 5:
            val = state[row, col]

            # TODO: set empty_diag false if a token is found

            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up
        
        if empty_diag:
            break

    
    # sum players' total value
    red_total_heuristic = red_row_heuristic_sum + red_col_heuristic_sum + red_pos_diag_heuristic_sum + red_neg_diag_heuristic_sum
    yel_total_heuristic = yel_row_heuristic_sum + yel_col_heuristic_sum + yel_pos_diag_heuristic_sum + yel_neg_diag_heuristic_sum

    # calculate state heuristic according to player & return
    if player == "red":
        state_heuristic = red_total_heuristic - yel_total_heuristic
    if player == "yellow":
        state_heuristic =  yel_total_heuristic - red_total_heuristic
    else:
        print("Invalid player colour: must be yellow or red")
        return        
    return state_heuristic

# def score(single_counts_player, total_counts_player):
#     return 10*total_counts_player[2] + 100*total_counts_player[3] + 1000*total_counts_player[4] + single_counts_player

# def utility(total_counts):
#     if total_counts[0, 4]: # red: player_i = 0
#         return 10000
#     if total_counts[1, 4]: # yellow: player_i = 1
#         return -10000
#     # ELSE: return nothing??

def print_board(state):
    print()
    for row in range(5, -1, -1):
        print("".join(col for col in state[row]))

def decode(string):
    rows = string.split(",")
    # grid = list(list(char for char in row) for row in rows) # rows on ouside lists - list of lists
    matrix = np.matrix([[char for char in row] for row in rows])
    return matrix

def drop_piece(state, col, is_red):
    colour = 'r' if is_red else 'y'
    for row in range(6):
        if state[row, col] == '.':
            state[row, col] = colour
            return True
    return False

def remove_piece(state, col):
    for row in range(5, -1, -1):
        if state[row, col] != '.':
            state[row, col] = '.'
            return True
    print("REMOVAL ERROR!")
    return False

def connect_four(contents, turn):
    max_depth = 4
    current_state = decode(contents)

    single_counts, total_counts = count_consecutive_pieces(current_state)
    if utility(total_counts):
        return "0\n1"

    # Using a stack to implement recursion. Needs to track:
    #   The path along the DFS search
    #   The current recursion depth
    column_stack = list()
    scores_stack = list((math.inf if i % 2 else -math.inf) for i in range(max_depth)) # instead of a list of lists - it's now a list

    current_depth = 0
    current_col = 0
    is_red = turn == "red"
    nodes_examined = 0

    best_choice = -1

    while (current_col != 7 or current_depth != 0):
        is_red = (current_depth % 2 == 0) == (turn == "red")
        
        # Case to move back up in the DFS
        if current_col == 7:
            if current_depth % 2:
                old_score = scores_stack[current_depth - 1]
                scores_stack[current_depth - 1] = max(scores_stack[current_depth], scores_stack[current_depth - 1])
                if current_depth == 1 and old_score < scores_stack[current_depth - 1]:
                    best_choice = column_stack[0]
            else:
                scores_stack[current_depth - 1] = min(scores_stack[current_depth], scores_stack[current_depth - 1])
                
            scores_stack[current_depth] = math.inf if current_depth % 2 else -math.inf


            nodes_examined += 1
            #print_board(current_state)
            #print(nodes_examined, scores_stack, column_stack, current_col, '^')
            current_depth -= 1
            remove_piece(current_state, column_stack[current_depth])
            current_col = column_stack.pop() + 1


        # Try to place piece in current column
        elif drop_piece(current_state, current_col, is_red):

            # Case where max depth is reached terminal is reached
            
            single_counts, total_counts = count_consecutive_pieces(current_state)
            score = evaluation(single_counts, total_counts)
            util = utility(total_counts)
            is_terminal = (current_depth == max_depth - 1) or util
            if is_terminal:
                if util:
                    score = util
                score *= (1 if (turn == "red") else -1)

                # store old_score and score: two given states comparing instead of comparing all 7 states at the end

                old_score = scores_stack[current_depth]
                scores_stack[current_depth] = max(score, old_score) if (is_red == (turn == "red")) else min(score, old_score)
                if (old_score != scores_stack[current_depth]) and current_depth == 0:
                    best_choice = current_col

                #print_board(current_state)
                #print(nodes_examined, scores_stack, column_stack, current_col, '|')
                remove_piece(current_state, current_col)
                nodes_examined += 1

            # Case to move further down in the DFS
            
            pruned = False
            if current_depth > 0: # no need to prune at top level
                # MAX choice case
                if is_red == (turn == "red"):
                    alpha = scores_stack[current_depth]
                    beta = min(scores_stack[i] for i in range(1, current_depth + 1, 2))

                # MIN choice case
                else:
                    alpha = max(scores_stack[i] for i in range(0, current_depth + 1, 2))
                    beta = scores_stack[current_depth]

                # Perform pruning
                if alpha >= beta:
                    if not is_terminal:
                        remove_piece(current_state, current_col)
                    current_col = 6 # change to last column so that the remainder don't get traversed
                    pruned = True
                    #print_board(current_state)
                    #print(nodes_examined, scores_stack, column_stack, current_col, 'X')
            current_col += 1

            if not is_terminal:
                if not pruned:
                    #print_board(current_state)
                    #print(nodes_examined, scores_stack, column_stack, current_col, 'v')
                    column_stack.append(current_col - 1)
                    current_depth += 1
                    current_col = 0


        else:
            current_col += 1
        

    nodes_examined += 1 
    #print(f"Score: {scores_stack[0]}")
    return best_choice

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        # board = '.ryyrry,.rryry.,..y.r..,..y....,.......,.......'
        board = '.......,.......,.......,.......,.......,.......'
        player = 'red'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    print(connect_four(board, player))