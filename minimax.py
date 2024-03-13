# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/5/

in_rows_calulated = False

def UTILITY(state):
  # TODO
  pass

def SCORE(state, player):
  # TODO
  pass

def EVALUATION(state):
  # TODO
  pass

def NUM_IN_A_ROW(count, state, player):
    # INPUT
        # state: decode(string): list of lists: state[row][column]
        # count: int 2, 3, or 4: the number of pieces in a row being counted
        # player: "red" or "yellow"
    # OUTPUT
        # int: number times "player" coloured pieces have "count" pieces in a row

    if in_rows_calulated:
        # check stored vals
        pass

    if player == "red":
        piece = "r"
    elif player == "yellow":
        piece = "y"
    else:
        piece = ""
        # throw error
        pass
    
    # ROW TRAVERSALS - note if row has ≤1 token in it then there's no point checking the row/s above it
    for row in range(6):
        # for the current row, iterate across each value in it (so column index)
        adjacent_count = 0 
        for col in range(7):
            val = state[row][col]
            # TODO: logic
            if val == piece:







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
