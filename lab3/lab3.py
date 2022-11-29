import logging
import random
from typing import Callable
from copy import deepcopy

from nim import Nim, Nimply

# Sample (and silly) strategies

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def nim_sum(state: Nim) -> int:
    result = state.rows[0]
    for row in state.rows[1:]:
        result = result ^ row
    return result
    
    #tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    #xor = tmp.sum(axis=0) % 2
    #return int("".join(str(_) for _ in xor), base=2)

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k]
    cooked['active_rows_number'] = sum(o > 0 for o in state.rows)
    cooked['shortest_row'] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y:y[1])[0]
    cooked['longest_row'] = max((x for x in enumerate(state.rows)), key=lambda y:y[1])[0]
    cooked['nim_sum'] = nim_sum(state)

    brute_force = list()
    for m in cooked['possible_moves']:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked['brute_force'] = brute_force

    return cooked

def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    #return next(m for m in data['possible_moves'] if m[1] == data['min_sum'])
    return next((bf for bf in data['brute_force'] if bf[1] == 0), random.choice(data['brute_force']))[0]

def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome['p']:
            ply = Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))
        else:
            ply = Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

        return ply
    return evolvable

# Evaluation of a strategy

NUM_MATCHES = 100
NIM_SIZE=10

def evaluate(strategy: Callable) -> float:
    #opponent = (strategy, pure_random)
    opponent = (strategy, optimal_strategy)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won/NUM_MATCHES

#Testing
if __name__ == "__main__":
    evaluate(make_strategy({'p' : .1}))

# # (OLD) Oversimplified match

# logging.getLogger().setLevel(logging.DEBUG)

# #strategy = (pure_random, gabriele)
# strategy = (make_strategy({'p' : .1}), optimal_strategy)

# # 11 is the num of rows
# nim = Nim(11)
# logging.debug(f"status: Initial board  -> {nim}")
# player = 0
# turn = 0
# while nim:
#     ply = strategy[player](nim)
#     nim.nimming(ply)
#     turn = turn+1
#     logging.debug(f"status: After player {player} -> {nim}")
#     player = 1 - player
# winner = 1 - player


# logging.info(f"status: Player {winner} won! (At turn {turn})")

