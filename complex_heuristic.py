# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/7/

import sys
import math
import numpy as np

global params
params = [0.2, 0.5, 0.1]

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

def segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count):
    global params
    if segment_len < 4 or tokens_count <= 0:
        return 0
    # calculate factors
    blanks_set_up_factor = 1 + params[0]*(blanks_set_up_count/blanks_count)
    token_edge_factor = 1 if (tokens_count <= 1) else 1 + params[1]*(edges_count/(tokens_count-1))
    return (1.5*tokens_count + blanks_count) * blanks_set_up_factor * token_edge_factor


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


# TODO: optimise traversals 
def state_heuristic(state: np.matrix):

    # red counts - store separately for purpose of analysing our heuristic
    red_row_heuristic_sum = 0
    red_col_heuristic_sum = 0
    red_neg_diag_heuristic_sum = 0
    red_pos_diag_heuristic_sum = 0

    # yellow counts
    yel_row_heuristic_sum = 0
    yel_col_heuristic_sum = 0
    yel_neg_diag_heuristic_sum = 0
    yel_pos_diag_heuristic_sum = 0
    
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
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens

        for row in range(6):
            val = state[row, col]
            
            # val is a blank - update variables the same way no matter current_segment_colour
            # optimisation: the rest of the positions above must also be blank
            if val == '.':
                # first blank traversed, the rest are above it
                blanks_count = 6 - row   
                segment_len += 6 - row
                blanks_set_up_count = 1 # columns can only have 1 blank set_up
                if current_segment_colour == "red":
                    red_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                break # if segment_colour = "" --> col was empty, no segment

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores. Cannot be any blanks in this complete sequence in col
                    red_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, 0, 0)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = 1
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, 0, 0)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = 1
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len = 1
                    tokens_count = 1
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len = 1
                    tokens_count = 1
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            # update previous val
            prev_val = val

            # if at the end of the column --> add the final segment to heuristic value
            if row == 5:
                if current_segment_colour == "red":
                    red_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_col_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count) 
            
    # HORIZONTAL/ROW TRAVERSALS 
    # initialise to 0 for optimisation check before traversing each row 
    blanks_count = 0
    for row in range(6):
        
        # optimisation: check if the previous row was all blanks - if so, the rest above are
        if blanks_count == 7:
            # no more segments left: the rest of rows are empty/blank
            break

        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        consecutive_blanks = 0 # used for when segment changes player (overlap section of segments)
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens
        set_up_count_of_consecutive_blanks = 0

        for col in range(7):
            val = state[row, col]

            # val is a blank - update variables the same way no matter current_segment_colour
            # optimisation: the rest of the positions above must also be blank
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_set_up(state, row, col):
                    blanks_set_up_count += 1
                    set_up_count_of_consecutive_blanks +=1 

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_row_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_row_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            # update prev value
            prev_val = val

            # check if end of row, store segment value. Unless row full of blanks
            if col == 6:
                if current_segment_colour == "red":
                    red_row_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_row_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)                     

    # NEGATIVE DIAGONAL TRAVERSALS (negative gradient) -> decrease row (down) and increase column (right)
    min_col = 0 # for optimisaton: if a given column has a lower elemnt found empty, all above are empty 
    # part 1
    # starting col = 0
    tokens_count = 0
    blanks_count = 0
    for col in range(3,7):
        # neg diag part 1: initial row is always 0 (blue)
        row = 0

        # optimisation: check if previous diagonal was all empty
        if blanks_count > 0 and tokens_count == 0:
            min_col = col # new col is the min you can go (everything to the left is empty)

        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens

        while row <= 5 and col >= min_col:
            val = state[row, col]

            # val is a blank - update variables the same way no matter current_segment_colour
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_set_up(state, row, col):
                    blanks_set_up_count += 1
                    set_up_count_of_consecutive_blanks +=1 

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            # update prev value
            prev_val = val

            # update row and column to continue down the diagonal
            col -= 1 # left
            row += 1 # up

            # check if you've reached the end of the diag's traversal
            if col < min_col or row > 5:
                if current_segment_colour == "red":
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
    # part 2
    # starting row = 5
    for col in range(2,4):
        # neg diag part 2: initial row always 5 (purple)
        row = 5

        # optimisation: check if previous diagonal was all empty
        if blanks_count > 0 and tokens_count == 0:
            # these diagonals don't start from the bottom row and thus are all above empty spaces
            break

        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens

        while col <= 6:
            val = state[row, col]

            # val is a blank - update variables the same way no matter current_segment_colour
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_set_up(state, row, col):
                    blanks_set_up_count += 1
                    set_up_count_of_consecutive_blanks += 1 

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            col += 1 # right
            row -= 1 # down

            # update prev value
            prev_val = val

            # check if end of diag - segment
            if col == 6:
                if current_segment_colour == "red":
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)

    # POSITIVE DIAGONAL TRAVERSALS
    # part 1
    max_col = 6
    tokens_count = 0
    blanks_count = 0
    for col in range(3, -1, -1): # 3, 2, 1, 0
        # part 1: diagonals that start from bottom row
        row = 0
        # optimisation: check if previous diagonal was all empty
        if blanks_count > 0 and tokens_count == 0:
            max_col = col # new col is the max you can go (everything to the left is empty)

        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens

        while row <= 5 and col <= max_col:
            val = state[row, col]

            # val is a blank - update variables the same way no matter current_segment_colour
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_set_up(state, row, col):
                    blanks_set_up_count += 1
                    set_up_count_of_consecutive_blanks +=1 

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_pos_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_pos_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up'

            # update prev value
            prev_val = val

            # check if you've reached the end of the diag's traversal
            if row > 5 or col > max_col:
                if current_segment_colour == "red":
                    red_pos_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_pos_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
    # part 2
    for row in range(1, 3):
        # part 2: inital col always 0, for traversals
        col = 0

        # optimisation: check if below diag is all empty:
        if blanks_count > 0 and tokens_count == 0:
            # these diagonals don't start from the bottom row and thus are all above empty spaces
            break 

        # variables used for heuristic calculation, for a given segment:
        current_segment_colour = "" # inital segment colour is determined after the first token is found (then the blanks are apart of its segment)
        segment_len = 0
        tokens_count = 0
        edges_count = 0
        prev_val = '' # used for checking for edges (consecutive tokens)
        blanks_count = 0
        blanks_set_up_count = 0 # count the num blanks set_up - ie able to have a token placed there without requiring below positions to be filled with tokens

        while row <= 5:
            val = state[row, col]

            # val is a blank - update variables the same way no matter current_segment_colour
            if val == '.':
                segment_len += 1
                blanks_count += 1
                consecutive_blanks += 1
                if blank_set_up(state, row, col):
                    blanks_set_up_count += 1
                    set_up_count_of_consecutive_blanks += 1 

            elif current_segment_colour == "red":
                if val == 'r':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'r' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "yellow"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")

            elif current_segment_colour == "yellow":             
                if val == 'y':
                    segment_len += 1
                    tokens_count += 1
                    edges_count += 1 if prev_val == 'y' else edges_count
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'r':
                    # PREV SEGMENT COMPLETE: update heuristic scores
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                    # begin next segment - may overlap and include blanks right before it - reset all varaibles
                    segment_len = consecutive_blanks + 1
                    blanks_count = consecutive_blanks
                    blanks_set_up_count = set_up_count_of_consecutive_blanks
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                    current_segment_colour = "red"
                    tokens_count = 1
                    edges_count = 0
                else:
                    print("invalid matrix character")
            
            # the first token has been found: it determines the colour of the first segment
            elif current_segment_colour == "":
                if val == 'r':
                    current_segment_colour = "red"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0
                elif val == 'y':
                    current_segment_colour = "yellow"
                    segment_len += 1
                    tokens_count += 1
                    consecutive_blanks = 0
                    set_up_count_of_consecutive_blanks = 0                
                else:
                    print("invalid matrix character")
            
            else:
                print("invalid segment colour")

            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up

            # update prev value
            prev_val = val

            # check if end of diag - segment
            if row == 5:
                if current_segment_colour == "red":
                    red_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
                elif current_segment_colour == "yellow":
                    yel_neg_diag_heuristic_sum += segment_heuristic(segment_len, tokens_count, edges_count, blanks_count, blanks_set_up_count)
        
    # sum players' total value
    red_total_heuristic = red_row_heuristic_sum + red_col_heuristic_sum + red_pos_diag_heuristic_sum + red_neg_diag_heuristic_sum
    yel_total_heuristic = yel_row_heuristic_sum + yel_col_heuristic_sum + yel_pos_diag_heuristic_sum + yel_neg_diag_heuristic_sum

    state_heuristic = red_total_heuristic - yel_total_heuristic
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
    
    global params
    if args:
        if len(*args) == 2:
            params = list(*args)

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
    #print(f"Score: {scores_stack[0]}, Nodes: {nodes_examined}")
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