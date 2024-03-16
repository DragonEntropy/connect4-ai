# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/5/

def UTILITY(state):
    # TODO
    pass

def SCORE(state, player):
    # TODO
    if state[0][2] == 'r' and state[0][1] != 'r':
        return 1
    return 0

def EVALUATION(state):
    # TODO
    pass

def NUM_IN_A_ROW(state):
    # TODO
    pass 

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