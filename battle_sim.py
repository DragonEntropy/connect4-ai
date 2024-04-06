from baseline import connect_four as baseline
from simple_heuristic import connect_four as simple
from tournament import connect_four as challenger
from complex_heuristic import connect_four as complex

from baseline import *
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

def run_simulation(model_1, model_2, board_output=False, current_board='.......,.......,.......,.......,.......,.......'):
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

        if board_output:
            print_board(current_state)
        current_board = encode(current_state)
        single_counts, total_counts = count_consecutive_pieces(current_state)
        turn_number += 1

    if not utility(total_counts):
        print(f"The models {model_1.name} and {model_2.name} drew!")
        return (0.5, 0.5)
    elif utility(total_counts) > 0:
        print(f"The model {model_1.name} beat {model_2.name} in {turn_number - 1} turns going first!")
        return (1, 0)
    else:
        print(f"The model {model_2.name} beat {model_1.name} in {turn_number - 1} turns going second!")
        return (0, 1)
    

def run_tournament(players):
    n_players = len(players)
    results = np.zeros((n_players, n_players, 2))

    for i in range(n_players - 1):
        for j in range(i + 1, n_players):
            print(f"Simulating models {i} and {j}")
            result_1 = run_simulation(players[i], players[j])
            result_2 = run_simulation(players[j], players[i])
            results[i, j, 0] += result_1[0]
            results[i, j, 1] += result_2[1]
            results[j, i, 0] += result_2[0]
            results[j, i, 1] += result_1[1]

    scores = results.sum(axis=2)
    for r, row in enumerate(scores):
        print(f"{', '.join(str(value) for value in row)} - {players[r].name}")

def generate_players():
    players = list()
    players.append(Model(baseline, "baseline"))
    players.append(Model(simple, "simple"))
    players.append(Model(complex, "complex", 0.3, 0.4))
    for i in range(1):
        c = 0.1 * randint(0, 10)
        players.append(Model(challenger, f"challenger(0.3, 0.4, {c:.1f})", 0.3, 0.4, c))
    for i in range(1):
        a = 0.1 * randint(0, 10)
        b = 0.1 * randint(0, 10)
        c = 0.1 * randint(0, 10)
        players.append(Model(challenger, f"challenger({a:.1f}, {b:.1f}, {c:.1f})", a, b, c))

    return players

if __name__ == "__main__":
    #model_1 = Model(simple, "baseline")
    #model_2 = Model(challenger, "challenger")
    #run_simulation(model_1, model_2, board_output=True)

    players = generate_players()
    run_tournament(players)