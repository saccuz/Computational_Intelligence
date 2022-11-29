import logging
import random
from typing import Callable
import nim
from nim import Nim, Nimply

    #tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    #xor = tmp.sum(axis=0) % 2
    #return int("".join(str(_) for _ in xor), base=2)

def generate_individual(genome: list) -> list:
    dna = list()
    while len(dna) < 4:
        locus = random.randint(0,len(nim.strategies))
        if random.random() < genome[locus]:
            dna.append(locus)
    return dna

def make_strategy(genome: list) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = nim.cook_status(state)

        if random.random() < genome['p']:
            ply = Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))
        else:
            ply = Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

        return ply
    return evolvable

NUM_MATCHES = 100
NIM_SIZE=10

def evaluate(strategy: Callable) -> float:
    opponent = (strategy, nim.optimal_strategy)
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

def evaluate_with_average(strategy: Callable) -> float:
    won = 0
    for m in range(NUM_MATCHES):
        board = Nim(NIM_SIZE)
        player = 0
        i = 0
        while board:
            opponent = (strategy,nim.opponent_strategy(i))
            ply = opponent[player](board)
            board.nimming(ply)
            player = 1 - player
            i+=1
        if player == 1:
            won += 1
    return won/NUM_MATCHES


if __name__ == "__main__":

    genome = [0.5]*len(nim.strategies)
    for generation in range(100):
        individual = generate_individual(genome)
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

