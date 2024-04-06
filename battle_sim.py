from baseline import connect_four as baseline
from simple_heuristic import connect_four as simple
from baseline import *
from tournament import connect_four as challenger

from random import randint
import numpy as np

class Model:
    def __init__(self, model, name, *args) -> None:
        self.model = model
        self.name = name
        self.args = args
    
    def run(self, board, player):
        return self.model(board, player, self.args)

def encode(matrix):
    return ",".join(("".join(col for col in row)) for row in matrix)

def run_simulation(model_1, model_2, current_board='.......,.......,.......,.......,.......,.......'):
    current_state = decode(current_board)
    single_counts, total_counts = count_consecutive_pieces(current_state)
    turn_number = 1

    while not utility(total_counts) and turn_number != 43:
        is_baseline = (turn_number % 2)
        if is_baseline:
            col = model_1.run(current_board, 'red')
            drop_piece(current_state, col, True)
        else:
            col = model_2.run(current_board, 'yellow')
            drop_piece(current_state, col, False)

        #print_board(current_state)
        current_board = encode(current_state)
        single_counts, total_counts = count_consecutive_pieces(current_state)
        turn_number += 1

    if not utility(total_counts):
        return (0.5, 0.5)
    elif utility(total_counts) > 0:
        print(f"The model {model_1.name} beat {model_2.name} in {turn_number - 1} turns!")
        return (1, 0)
    else:
        print(f"The model {model_2.name} beat {model_1.name} in {turn_number - 1} turns!")
        return (0, 1)
    

def run_tournament(players):
    n_players = len(players)
    results = np.zeros((n_players, n_players, 2))

    for i in range(n_players - 1):
        for j in range(i + 1, n_players):
            result_1 = run_simulation(players[i], players[j])
            result_2 = run_simulation(players[j], players[i])
            results[i, j, 0] += result_1[0]
            results[i, j, 1] += result_2[1]
            results[j, i, 0] += result_2[0]
            results[j, i, 1] += result_1[1]

    print(results.sum(axis=2))

def generate_players(extra_count=1):
    players = list()
    players.append(Model(baseline, "baseline"))
    players.append(Model(simple, "simple"))
    players.append(Model(challenger, "challenger"))
    for i in range(extra_count):
        a = 0.1 * randint(0, 10)
        b = 0.1 * randint(0, 10)
        players.append(Model(challenger, f"challenger({a},{b})"))

    return players

if __name__ == "__main__":
    #model_1 = Model(baseline, "baseline")
    #model_2 = Model(challenger, "challenger")
    #run_simulation(model_1, model_2)

    players = generate_players()
    run_tournament(players)