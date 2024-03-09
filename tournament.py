# Link: https://groklearning.com/learn/usyd-comp3308-2024-s1/adv-proj1/7/

import sys

def connect_four(contents, turn):
    #TODO
    return ''

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        board = '.ryyrry,.rryry.,..y.r..,..y....,.......,.......'
        player = 'red'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    print(connect_four(board, player))