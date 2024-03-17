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
    try:
        total_counts[(player_i, adjacent_count)] += 1
    except KeyError:
        # print(f"invalid adjacent count: Key {(player_i, adjacent_count)}")
        return

def UTILITY(state):
    global num_in_row_calc
    num_in_row_calc = False

    if NUM_IN_A_ROW(4, state, 'red'): # red: player_i = 0
        num_in_row_calc = True
        return 10000
    if NUM_IN_A_ROW(4, state, 'yellow'): # yellow: player_i = 1
        num_in_row_calc = True
        return -10000
    # ELSE: return nothing??

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
        for col in range(1, 7):
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
    return False

def connect_four_mm(contents, turn, max_depth):
    global num_in_row_calc
    current_state = decode(contents)

    # Using a stack to implement recursion. Needs to track:
    #   The path along the DFS search
    #   The current recursion depth
    column_stack = list()
    scores_stack = list(list() for i in range(max_depth))

    current_depth = 0
    current_col = 0
    is_red = turn == "red"
    nodes_examined = 0

    while (current_col != 7 or current_depth != 0):
        
        # Case to move back up in the DFS
        if current_col == 7:

            # MIN case
            if current_depth % 2:
                scores_stack[current_depth - 1].append(min(scores_stack[current_depth]))
                scores_stack[current_depth].clear()
            
            # MAX case
            else:
                scores_stack[current_depth - 1].append(max(scores_stack[current_depth]))
                scores_stack[current_depth].clear()

            # print(column_stack, current_col)
            nodes_examined += 1
            current_depth -= 1
            remove_piece(current_state, column_stack[current_depth])
            is_red = not is_red
            current_col = column_stack.pop() + 1


        # Try to place piece in current column
        elif drop_piece(current_state, current_col, is_red):

            # Case where max depth is reached terminal is reached
            score = EVALUATION(current_state)
            if current_depth == max_depth - 1 or UTILITY(current_state):
                scores_stack[current_depth].append((1 if turn == "red" else -1) * score)
                # print_board(current_state)
                remove_piece(current_state, current_col)
                # print(column_stack, current_col)
                current_col += 1
                nodes_examined += 1

            # Case to move further down in the DFS
            else:
                column_stack.append(current_col)
                current_depth += 1
                current_col = 0
                is_red = not is_red

            num_in_row_calc = False

        else:
            current_col += 1
            if current_depth == 0:
                scores_stack[0].append(-math.inf)
        
        # print_board(current_state)

    minimax_score = -math.inf
    minimax_index = -1
    nodes_examined += 1
    for i, score in enumerate(scores_stack[0]):
        if score > minimax_score:
            minimax_score = score
            minimax_index = i
    return f"{minimax_index}\n{nodes_examined}"

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    result = connect_four_mm("..y.r..,..y.r..,..y.r..,.......,.......,.......", "red", 3)
    print(result)