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

def blank_set_up(state, row, col):
    # don't check for valid input - will waste time in tournament # TODO: delete this input validity check once code is working
    if row < 0 or row > 5 or col < 0 or col > 6:
        print("invalid input")
        return
    if row == 0:
        return True
    return not state[row-1, col] == '.'

def count_wins(state, is_red):
    if is_red:
        opposite_token = 'y'
    else:
        opposite_token = 'r'
    wins = 0

    # Try create 4 in a row starting from every possible position
    # No duplicates by enforcing that the row moves right
    for row in range(6):
        for col in range(7):

            # Horizontal case
            if col + 3 < 7:
                if not sum(state[row, col + i] == opposite_token for i in range(4)):
                    wins += 1

            # Vertical case
            if row + 3 < 6:
                if not sum(state[row + i, col] == opposite_token for i in range(4)):
                    wins += 1

            # Pos diagonal case
            if row + 3 < 6 and col + 3 < 7:
                if not sum(state[row + i, col + i] == opposite_token for i in range(4)):
                    wins += 1

            # Neg diagonal case
            if row - 3 >= 0 and col + 3 < 7:
                if not sum(state[row - i, col + i] == opposite_token for i in range(4)):
                    wins += 1
    
    return wins



def state_heuristic(state: np.matrix): 
    pos_heuristic = count_wins(state, True)
    neg_heuristic = count_wins(state, False)
    
    state_heuristic = pos_heuristic - neg_heuristic  
    return state_heuristic

def evaluation(state, last_col):
    # First determine coordinates of the last placed piece
    last_row = -1
    for row in range(5, -1, -1):
        if state[row, last_col] != '.':
            last_row = row
            break
    last_piece = state[last_row, last_col]

    # Then check for 4-in-a-row from the new piece

    # Row check
    num_in_a_row = 0
    for row in range(max(0, last_row - 3), min(6, last_row + 4)):
        if state[row, last_col] == last_piece:
            num_in_a_row += 1
            if num_in_a_row == 4:
                #print(f"Vert win at ({last_col}, {last_row}) for {last_piece}")
                return last_piece
        else:
            num_in_a_row = 0

    # Column check
    num_in_a_row = 0
    for col in range(max(0, last_col - 3), min(7, last_col + 4)):
        if state[last_row, col] == last_piece:
            num_in_a_row += 1
            if num_in_a_row == 4:
                #print(f"Hori win at ({last_col}, {last_row}) for {last_piece}")
                return last_piece
        else:
            num_in_a_row = 0

    # Positive diagonal check
    num_in_a_row = 0
    left_span = min(3, last_col, last_row)
    right_span = min(3, 6 - last_col, 5 - last_row)
    for i in range(-left_span, right_span + 1):
        if state[last_row + i, last_col + i] == last_piece:
            num_in_a_row += 1
            if num_in_a_row == 4:
                #print(f"Diag + win at ({last_col}, {last_row}) for {last_piece}")
                return last_piece
        else:
            num_in_a_row = 0

    # Negative diagonal check
    num_in_a_row = 0
    left_span = min(3, last_col, 5 - last_row)
    right_span = min(3, 6 - last_col, last_row)
    for i in range(-left_span, right_span + 1):
        if state[last_row - i, last_col + i] == last_piece:
            num_in_a_row += 1
            if num_in_a_row == 4:
                #print(f"Diag - win at ({last_col}, {last_row}) for {last_piece}")
                return last_piece
        else:
            num_in_a_row = 0

    return None

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

def connect_four(contents, turn, *args):
    max_depth = 5
    current_state = decode(contents)
    move_index_order = [3, 2, 4, 1, 5, 0, 6]
    

    # Using a stack to implement recursion. Needs to track:
    #   The path along the DFS search
    #   The current recursion depth
    column_stack = list()
    scores_stack = list((math.inf if i % 2 else -math.inf) for i in range(max_depth)) # instead of a list of lists - it's now a list

    current_depth = 0
    current_col_index = 0
    is_red = turn == "red"
    nodes_examined = 0

    best_choice = -1

    while (current_col_index != 7 or current_depth != 0):
        is_red = (current_depth % 2 == 0) == (turn == "red")
        
        # Case to move back up in the DFS
        if current_col_index == 7:
            if current_depth % 2:
                old_score = scores_stack[current_depth - 1]
                scores_stack[current_depth - 1] = max(scores_stack[current_depth], scores_stack[current_depth - 1])
                if current_depth == 1 and old_score < scores_stack[current_depth - 1]:
                    best_choice = move_index_order[column_stack[0]]
            else:
                scores_stack[current_depth - 1] = min(scores_stack[current_depth], scores_stack[current_depth - 1])
                
            scores_stack[current_depth] = math.inf if current_depth % 2 else -math.inf


            nodes_examined += 1
            #print_board(current_state)
            #print(nodes_examined, scores_stack, column_stack, current_col, '^')
            current_depth -= 1
            remove_piece(current_state, move_index_order[column_stack[current_depth]])
            current_col_index = column_stack.pop() + 1


        # Try to place piece in current column
        elif drop_piece(current_state, move_index_order[current_col_index], is_red):

            # Case where max depth is reached terminal is reached
            util = evaluation(current_state, move_index_order[current_col_index])
            is_terminal = (current_depth == max_depth - 1) or util
            if is_terminal:
                if util:
                    score = math.inf * (1 if (util == 'r') else -1)
                else: 
                    score = state_heuristic(current_state)
                score *= (1 if (turn == "red") else -1)

                # store old_score and score: two given states comparing instead of comparing all 7 states at the end

                old_score = scores_stack[current_depth]
                scores_stack[current_depth] = max(score, old_score) if (is_red == (turn == "red")) else min(score, old_score)
                if (old_score != scores_stack[current_depth]) and current_depth == 0:
                    best_choice = move_index_order[current_col_index]

                #print_board(current_state)
                #print(nodes_examined, scores_stack, column_stack, current_col, '|')
                remove_piece(current_state, move_index_order[current_col_index])
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
                        remove_piece(current_state, move_index_order[current_col_index])
                    current_col_index = 6 # change to last column so that the remainder don't get traversed
                    pruned = True
                    #print_board(current_state)
                    #print(nodes_examined, scores_stack, column_stack, current_col, 'X')
            current_col_index += 1

            if not is_terminal:
                if not pruned:
                    #print_board(current_state)
                    #print(nodes_examined, scores_stack, column_stack, current_col, 'v')
                    column_stack.append(current_col_index - 1)
                    current_depth += 1
                    current_col_index = 0


        else:
            current_col_index += 1
        

    nodes_examined += 1 
    # print(f"Score: {scores_stack[0]}, Nodes: {nodes_examined}")
    return best_choice

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        board = '.ryyrry,.rryry.,..y.r..,..y....,.......,.......'
        # board = '.......,.......,.......,.......,.......,.......'
        player = 'yellow'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    print(connect_four(board, player))