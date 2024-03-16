# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/5/

num_in_row_calc = False
# for the given state:
len_2_count = [0, 0]  # [red, yellow]
len_3_count = [0, 0]
len_4_count = [0, 0]
players_tokens = [0, 0]

def player_to_index(player):
    if player == "red":
        return 0
    elif player == "yellow":
        return 1
    else:
        print("Invalid player colour: must be yellow or red")
        return

def colour_to_char(player):
    if player == "red":
        return 'r'
    elif player == "yellow":
        return 'y'
    else:
        print("Invalid player colour: must be yellow or red")
        return

def tokens_in_row(count, player_i):
    if count == 2:
        return len_2_count[player_i]
    elif count == 3:
        return len_3_count[player_i]
    elif count == 4:
        return len_4_count[player_i]
    else:
        print("invalid count valid given")

def update_count(adjacent_count, player_i):
    if adjacent_count == 2:
        len_2_count[player_i] += 1
    elif adjacent_count == 3:
        len_3_count[player_i] += 1
    elif adjacent_count == 4:
        len_4_count[player_i] += 1
    else:
        print("invalid adjacent count")

def UTILITY(state):
    if tokens_in_row(4, 0): # red: player_i = 0
        return 10000
    if tokens_in_row(4, 1): # yellow: player_i = 1
        return -10000
    # ELSE: return nothing??
    return

def NUM_IN_A_ROW(count, state, player):
    # INPUT
        # state: decode(string): list of lists: state[row][column]
        # count: int 2, 3, or 4: the number of tokens in a row being counted
        # player: "red" or "yellow"
    # OUTPUT
        # int: number times "player" coloured tokens have "count" tokens in a row

    token = colour_to_char(player)
    player_i = player_to_index(player)

    if num_in_row_calc:
        return tokens_in_row(count, player_i)
    
    # ROW TRAVERSALS - note if row has ≤1 token in it then there's no point checking the row/s above it
    for row in range(6):
        # for the current row, iterate across each value in it (so column index)
        adjacent_count = 0 
        for col in range(7):
            val = state[row][col]
            if val == token:
                adjacent_count += 1
                # use the row traversals to count the total tokens of the play
                players_tokens[player_i] += 1
            # blank or other players token
            else:
                # record previous tokens in a row
                update_count(adjacent_count, player_i)
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
                update_count(adjacent_count, player_i)
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
                update_count(adjacent_count, player_i)
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
                update_count(adjacent_count, player_i)
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
                update_count(adjacent_count, player_i)
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
                update_count(adjacent_count, player_i)
                # reset to 0 tokens in a row
                adjacent_count = 0
            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up

    num_in_row_calc = True

    # return stored value required
    return tokens_in_row(count, player_i)


def SCORE(state, player):
    player_i = player_to_index(player)
    return 10*NUM_IN_A_ROW(2, state, player) + 100*NUM_IN_A_ROW(3, state, player) + 1000*NUM_IN_A_ROW(4, state, player) + players_tokens[player_i]

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
    current_state = decode(contents)

    # Using a stack to implement recursion. Needs to track:
    #   The path along the DFS search
    #   The current recursion depth
    column_stack = list()
    scores_stack = list(list() for i in range(max_depth))
    best_choice = 0

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

            nodes_examined += 1
            current_depth -= 1
            remove_piece(current_state, column_stack[current_depth])
            is_red = not is_red
            current_col = column_stack.pop() + 1


        # Try to place piece in current column
        elif drop_piece(current_state, current_col, is_red):

            # Case where max depth is reached
            if current_depth == max_depth - 1:
                scores_stack[current_depth].append(SCORE(current_state, turn))
                # print_board(current_state)
                remove_piece(current_state, current_col)
                current_col += 1
                nodes_examined += 1

            # Case to move further down in the DFS
            else:
                column_stack.append(current_col)
                current_depth += 1
                current_col = 0
                is_red = not is_red

        else:
            current_col += 1
        
        print_board(current_state)

    minimax_score = scores_stack[0][0]
    minimax_index = 0
    nodes_examined += 1
    for i, score in enumerate(scores_stack[0]):
        if score > minimax_score:
            minimax_score = score
            minimax_index = i
    return f"{minimax_index}\n{nodes_examined}" 

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    result = connect_four_mm("r......,r......,r......,r......,r......,r......", "red", 5)
    print(result)