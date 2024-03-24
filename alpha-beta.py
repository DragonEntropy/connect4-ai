# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/5/
import math

num_in_row_calc = False

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

def UTILITY(state):
    global num_in_row_calc
    num_in_row_calc = False

    if NUM_IN_A_ROW(4, state, 'red'): # red: player_i = 0
        num_in_row_calc = False
        return 10000
    if NUM_IN_A_ROW(4, state, 'yellow'): # yellow: player_i = 1
        num_in_row_calc = False
        return -10000
    num_in_row_calc = False
    # ELSE: return nothing??

# TODO: if a row has no tokens the rows above don't need to be traversed
def NUM_IN_A_ROW(count, state, player):
    # INPUT
        # state: decode(string): list of lists: state[row][column]
        # count: int 2, 3, or 4: the number of tokens in a row being counted
        # player: "red" or "yellow"
    # OUTPUT
        # int: number times "player" coloured tokens have "count" tokens in a row

    # for the given state:

    global single_counts, num_in_row_calc, total_counts
    if not num_in_row_calc:
        single_counts = {player_i : 0 for player_i in [0, 1]}
        total_counts = {(player_i, length) : 0 for player_i in [0, 1] for length in [2, 3, 4]}

    player_index = player_to_index(player)

    if num_in_row_calc:
        return tokens_in_row(count, player_index, total_counts)
    
    for player in ['red', 'yellow']:
        player_i = player_to_index(player)
        token = colour_to_char(player)

        # ROW TRAVERSALS - note if row has ≤1 token in it then there's no point checking the row/s above it
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

    num_in_row_calc = True
    # print(total_counts)

    # return stored value required
    return tokens_in_row(count, player_index, total_counts)

def SCORE(state, player):
    global single_counts
    return 10*NUM_IN_A_ROW(2, state, player) + 100*NUM_IN_A_ROW(3, state, player) + 1000*NUM_IN_A_ROW(4, state, player) + single_counts[player_to_index(player)]

def EVALUATION(state):
  return SCORE(state, "red") - SCORE(state, "yellow")

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

def connect_four_ab(contents, turn, max_depth):
    global num_in_row_calc
    current_state = decode(contents)

    if UTILITY(current_state):
        return "0\n1"

    # Using a stack to implement recursion. Needs to track:
    #   The path along the DFS search
    #   The current recursion depth
    column_stack = list()
    scores_stack = list((math.inf if i % 2 else -math.inf) for i in range(max_depth))

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
            print(nodes_examined, scores_stack, column_stack, current_col, '^')
            current_depth -= 1
            remove_piece(current_state, column_stack[current_depth])
            print_board(current_state)
            current_col = column_stack.pop() + 1


        # Try to place piece in current column
        elif drop_piece(current_state, current_col, is_red):

            # Case where max depth is reached terminal is reached
            score = EVALUATION(current_state)
            utility = UTILITY(current_state)
            is_terminal = (current_depth == max_depth - 1) or utility
            if is_terminal:
                if utility:
                    score = utility
                score *= (1 if (turn == "red") else -1)

                old_score = scores_stack[current_depth]
                scores_stack[current_depth] = max(score, old_score) if (is_red == (turn == "red")) else min(score, old_score)
                if (old_score != scores_stack[current_depth]) and current_depth == 0:
                    best_choice = current_col

                remove_piece(current_state, current_col)
                nodes_examined += 1
                print(nodes_examined, scores_stack, column_stack, current_col, '|')
                print_board(current_state)

            # Case to move further down in the DFS
            
            pruned = False
            if current_depth > 0:
                # MAX choice case
                if is_red == (turn == "red"):
                    alpha = scores_stack[current_depth]
                    beta = scores_stack[current_depth - 1]

                # MIN choice case
                else:
                    alpha = scores_stack[current_depth - 1]
                    beta = scores_stack[current_depth]

                # Perform pruning
                if alpha >= beta:
                    if not is_terminal:
                        remove_piece(current_state, current_col)
                    current_col = 6
                    pruned = True
                    print(nodes_examined, scores_stack, column_stack, current_col, 'X')
                    print_board(current_state)
            current_col += 1

            if not is_terminal:
                if not pruned:
                    print(nodes_examined, scores_stack, column_stack, current_col, 'v')
                    print_board(current_state)
                    column_stack.append(current_col - 1)
                    current_depth += 1
                    current_col = 0


        else:
            current_col += 1
        

    nodes_examined += 1 
    print(scores_stack[0])
    return f"{best_choice}\n{nodes_examined}"

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    # connect_four_ab("xxxxxxx,xxxxxxx,xxxxxxx,xxxxxxx,xxxxxxx,....xxx", "red", 4)
    # result = connect_four_ab("xxxxxxx,xxxxxxx,xxxxxxx,xxxxxxx,xxxxxxx,.......", "red", 4)
    result = connect_four_ab("r..y..r,r..y..r,......r,.......,.......,.......", "red", 2)
    print(result)