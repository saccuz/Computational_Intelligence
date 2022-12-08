import logging
import random
import heapq
from tqdm import tqdm
from scipy.special import expit as sigmoid
import nim as nim
from nim import Nim, Strategy

#logging.basicConfig(level=logging.INFO)

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
    op_strat = ['pure random','gabriele','optimal'] 
    for turn in range(3):
        champion = [0,[]]
        print(op_strat[turn])
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
    print(f"Champion: {evaluate(make_strategy(champion[1]),nim.opponent_strategy(2))}")

    selected = list(map(genome.index, heapq.nlargest(GENM_SIZE, genome)))
    print(f"Evolved: {evaluate(make_strategy(selected),nim.opponent_strategy(2))}")
    print("Evolved genome:")
    print_genome(selected)
    tourn = evaluate(make_strategy(selected),make_strategy(champion[1]))
    print(f"Tournament: evolved/champion: {tourn}/{1-tourn}")

    if tourn > 0.5:
        champion = selected
    else:
        champion = champion[1]

    print("Best genome:")
    print_genome(champion)