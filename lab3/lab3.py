import logging
import random
from scipy.special import expit as sigmoid
import nim
from nim import Nim, Strategy

    #tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    #xor = tmp.sum(axis=0) % 2
    #return int("".join(str(_) for _ in xor), base=2)
GENERATIONS = 100
NUM_MATCHES = 100
NIM_SIZE=10
GENM_SIZE = 2
RESULT_TRESH = .3
EVOL_STEP = .05

def generate_individual(genome: list) -> list:
    dna = list()
    while len(dna) < GENM_SIZE:
        locus = random.randint(0,len(nim.tactics)-1)
        if random.random() < sigmoid(genome[locus]):
            dna.append(locus)
    return dna

def make_strategy(dna: list) -> Strategy:
    used_tactics = list()

    for al, _ in zip(dna, range(len(dna))):
        used_tactics.append(nim.tactics[al])

    return Strategy(used_tactics)

def evolve_genome(dna: list, results: float, genome: list) -> None:
    if results >= RESULT_TRESH:
        for i in range(len(genome)):
            if i in dna:
                genome[i] += EVOL_STEP
            else:
                genome[i] -= EVOL_STEP/2
                # if genome[i] < 0:
                #     genome[i] = .1
        # for loc, _ in zip(dna, range(len(dna))):
        #     genome[loc] += EVOL_STEP
    
    else:
        for i in range(len(genome)):
            if i in dna:
                genome[i] -= EVOL_STEP
                # if genome[i] < 0:
                #     genome[i] = .1
            else:
                genome[i] += EVOL_STEP

        # for loc, _ in zip(dna, range(len(dna))):
        #     genome[loc] -= EVOL_STEP
        #     if genome[loc] < 0:
        #         genome[loc] = .1

def evaluate_with_average(strategy: Strategy) -> float:
    won = 0
    for m in range(NUM_MATCHES):
        board = Nim(NIM_SIZE)
        player = 0
        i = 0
        while board:
            if i % 2 != 0:
                opponent = strategy.move()
                player = 0
            else:
                opponent = nim.opponent_strategy()
                player = 1
            ply = opponent(board)
            board.nimming(ply)
            i+=1
        if player == 0:
            won += 1
    return won/NUM_MATCHES


if __name__ == "__main__":
    mean_ = 0
    win = 0
    lose = 0
    genome = [.5]*len(nim.tactics)
    for generation in range(GENERATIONS):
        individual = generate_individual(genome)
        results = evaluate_with_average(make_strategy(individual))
        print(results)
        mean_ += results
        if results > .5:
            win += 1
        else:
            lose += 1
        evolve_genome(individual, results, genome)
    for x in zip(nim.tactics,genome):
        print(x[0].__name__, x[1])
    print(f"mean: {mean_/GENERATIONS}")
    print(f"victory: {win/GENERATIONS *100}%")




 #   evaluate(make_strategy({'p' : .1}))

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

