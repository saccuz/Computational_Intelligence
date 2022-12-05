import logging
import random
import heapq
from tqdm import tqdm
from scipy.special import expit as sigmoid
import nim
from nim import Nim, Strategy

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
    else:
        for i in range(len(genome)):
            if i in dna:
                genome[i] -= EVOL_STEP
            else:
                genome[i] += EVOL_STEP

def evaluate(player1: Strategy, player2: Strategy) -> float:
    won = 0
    for m in range(NUM_MATCHES):
        board = Nim(NIM_SIZE)
        player = 0
        i = random.randint(0,1)
        while board:
            if i % 2 != 0:
                opponent = player1.move()
                player = 0
            else:
                opponent = player2.move()
                player = 1
            ply = opponent(board)
            board.nimming(ply)
            i+=1
        if player == 0:
            won += 1
    return won/NUM_MATCHES

def print_genome(champion: list) -> None:
    for x in champion:
        print(f"  {nim.tactics[x].__name__}")

if __name__ == "__main__":
    mean_ = 0
    win = 0
    lose = 0
    champion = [0,[]] 
    genome = [.5]*len(nim.tactics)
    op_strat = ['dumb_strategy','pure random','gabriele','optimal']

    for turn in range(len(op_strat)):
        champion = [0,[]]
        print(f"Playing against {op_strat[turn]}")

        for generation in tqdm(range(GENERATIONS), desc="Playing", ascii=False):
            individual = generate_individual(genome)
            results = evaluate(make_strategy(individual), nim.opponent_strategy(turn))
            if results > champion[0]:
                champion[1] = individual
                champion[0] = results
            logging.debug(results)
            mean_ += results
            if results > .5:
                win += 1
            else:
                lose += 1
            evolve_genome(individual, results, genome)
        print_genome(champion[1])

    for x in zip(nim.tactics,genome):
        logging.info(x[0].__name__, x[1])

    logging.debug(f"mean: {mean_/GENERATIONS}")
    logging.debug(f"victory: {win/GENERATIONS *100}%")

    print("-----------------------")
    print(f"Last assigned champion vs optimal: {evaluate(make_strategy(champion[1]),nim.opponent_strategy(3))}")

    selected = list(map(genome.index, heapq.nlargest(GENM_SIZE, genome)))
    print("Evolved genome:")
    print_genome(selected)

    print(f"Evolved vs optimal: {evaluate(make_strategy(selected),nim.opponent_strategy(3))}")
    tourn = evaluate(make_strategy(selected),make_strategy(champion[1]))
    print(f"Evolved vs last assigned champion: {tourn}/{1-tourn}")

    if tourn > 0.5:
        champion = selected
    else:
        champion = champion[1]

    print("Best genome overall:")
    print_genome(champion)

    #evolved common results:  
#              gabriele      - pick_odd_max
#              gabriele      - pick_even_max       <= BEST ONE FOUND THAT OVERALL WINS almost more than 50% (except vs the optimal opponent)
#              longest_row   - gabriele
#              pick_even_max - pick_one_from_max   <= ALSO THIS IS MORE OR LESS GOOD
#              gabriele      - shortest_row        <= THIS IS VERY GOOD WITH THE FIRST TWO OPPONENTS, BUT VERY BAD WITH THE gabriele and optimal 
    #champion common results: 
#              pick_odd_max  - pick_one_from_min
#              pick_one_from_max - pick_odd_max