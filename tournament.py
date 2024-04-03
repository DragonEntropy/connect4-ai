# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/7/

import sys
import math

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

def tokens_in_row(count, player_i, total_counts):
    try:
        return total_counts[(player_i, count)]
    except KeyError:
        # print(f"invalid count valid given: Key {(player_i, count)}")
        return

def update_count(adjacent_count, player_i, total_counts):
    if adjacent_count > 4:
        adjacent_count = 4
    try:
        total_counts[(player_i, adjacent_count)] += 1
    except KeyError:
        # print(f"invalid adjacent count: Key {(player_i, adjacent_count)}")
        return

# TODO: if a row has no tokens the rows above don't need to be traversed
def count_consecutive_pieces(state):

    single_counts = {player_i : 0 for player_i in [0, 1]}
    total_counts = {(player_i, length) : 0 for player_i in [0, 1] for length in [2, 3, 4]}

    for player in ['red', 'yellow']:
        player_i = player_to_index(player)
        token = colour_to_char(player)

        # HORIZONTAL/ROW TRAVERSALS - note if row has ≤1 token in it then there's no point checking the row/s above it
        for row in range(6):
            # for the current row, iterate across each value in it (so column index)
            adjacent_count = 0 
            for col in range(7):
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                    # use the row traversals to count the total tokens of the play
                    single_counts[player_i] += 1
                # blank or other players token
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)
        
        # COLUMN TRAVERSALS 
        for col in range(7):
            # for the current coloumn, iterate each row value of the column
            adjacent_count = 0
            for row in range(6):
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)
        
        # NEGATIVE DIAGONAL TRAVERSALS (negative as in negative gradient) -> decrease row (down) and increase column (right)
        # starting col = 0
        for row in range(1,6):
            col = 0
            adjacent_count = 0
            while row >= 0 and col <=6:
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
                # update row and coloumn to continue down the diagonal
                col += 1 # right
                row -= 1 # down
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)
        # starting row = 5
        for col in range(1,6):
            row = 5
            adjacent_count = 0
            while row >= 0 and col <= 6:
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
                # update row and coloumn to continue down the diagonal
                col += 1 # right
                row -= 1 # down
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)

        # POSITIVE DIAGONAL TRAVERSALS
        for row in range(0,5):
            col = 0
            adjacent_count = 0
            while row <= 5 and col <= 6:
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
                # update row and coloumn to continue up the diagonal
                col += 1 # right
                row += 1 # up
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)

        for col in range(1, 6):
            row = 0
            adjacent_count = 0
            while row <= 5 and col <= 6:
                val = state[row][col]
                if val == token:
                    adjacent_count += 1
                else:
                    # record previous tokens in a row
                    update_count(adjacent_count, player_i, total_counts)
                    # reset to 0 tokens in a row
                    adjacent_count = 0
                # update row and coloumn to continue up the diagonal
                col += 1 # right
                row += 1 # up
            if adjacent_count > 1:
                update_count(adjacent_count, player_i, total_counts)
    # print(total_counts)

    return single_counts, total_counts

def score(single_counts_player, total_counts_player):
    return 10*total_counts_player[2] + 100*total_counts_player[3] + 1000*total_counts_player[4] + single_counts_player

def evaluation(single_counts, total_counts):
    return score(single_counts[0], {i : total_counts[0, i] for i in [2, 3, 4]}) - score(single_counts[1], {i : total_counts[1, i] for i in [2, 3, 4]})

def utility(total_counts):
    if total_counts[0, 4]: # red: player_i = 0
        return 10000
    if total_counts[1, 4]: # yellow: player_i = 1
        return -10000
    # ELSE: return nothing??

def print_board(state):
    print()
    for row in range(5, -1, -1):
        print("".join(col for col in state[row]))

def decode(string):
    rows = string.split(",")
    grid = list(list(char for char in row) for row in rows) # rows on ouside lists - list of lists
    return grid

def drop_piece(state, col, is_red):
    colour = 'r' if is_red else 'y'
    for row in range(6):
        if state[row][col] == '.':
            state[row][col] = colour
            return True
    return False

def remove_piece(state, col):
    for row in range(5, -1, -1):
        if state[row][col] != '.':
            state[row][col] = '.'
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