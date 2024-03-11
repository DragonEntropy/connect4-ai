# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/5/

def UTILITY(state):
  # TODO
  pass

def SCORE(state, player):
  # TODO
  pass

def EVALUATION(state):
  # TODO
  pass

def NUM_IN_A_ROW(state):
  # TODO
  pass 

def decode(string):
  rows = string.split(",")
  grid = list(list(char for char in row) for row in rows) # rows on ouside lists - list of lists
  return grid

def connect_four_mm(contents, turn, max_depth):
  # TODO
  return ''

if __name__ == '__main__':
  # Example function call below, you can add your own to test the connect_four_mm function
  connect_four_mm(".......,.......,.......,.......,.......,.......", "red", 1)