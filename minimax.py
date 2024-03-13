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

def UTILITY(state):
  # TODO
  pass

def SCORE(state, player):
    return players_tokens[]


def EVALUATION(state):
  # TODO
  pass

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
        # check stored vals
        if count == 2:
            return len_2_count[player_i]
        elif count == 3:
            return len_3_count[player_i]
        elif count == 4:
            return len_4_count[player_i]
        else:
            print("invalid count valid given")


        
    
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
            else: # blank or other players token
                # record previous tokens in a row
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
                # TODO: should be consider more cases (Seems like part 1 and 2 don't require it), there probably wouldn't be a point in predicting beyond 4 connected since that'd be the end of the game
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
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
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
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
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
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
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
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
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
                if adjacent_count == 2:
                    len_2_count[player_i] += 2
                elif adjacent_count == 3:
                    len_3_count[player_i] += 2
                elif adjacent_count == 4:
                    len_4_count[player_i] += 2
                # reset to 0 tokens in a row
                adjacent_count = 0
            # update row and coloumn to continue up the diagonal
            col += 1 # right
            row += 1 # up

    num_in_row_calc = True

    # check stored vals
    if count == 2:
        return len_2_count[player_i]
    elif count == 3:
        return len_3_count[player_i]
    elif count == 4:
        return len_4_count[player_i]
    else:
        print("invalid count valid given")











            





    # # TODO
    pass 

def decode(string):
  rows = string.split(",")
  grid = list(list(char for char in row) for row in rows) # rows on ouside lists - list of lists
  return grid

def connect_four_mm(contents, turn, max_depth):
  print(decode(contents))
  return ''

if __name__ == '__main__':
  # Example function call below, you can add your own to test the connect_four_mm function
#   connect_four_mm(".......,.......,.......,.......,.......,.......", "red", 1)
  connect_four_mm("first..,second.,.......,.......,.......,.......", "red", 1)
  NUM_IN_A_ROW(decode("first..,second.,.......,.......,.......,......."))
