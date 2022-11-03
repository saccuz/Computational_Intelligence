import random
from itertools import combinations
import logging
import numpy as np

logging.basicConfig(format="%(message)s", level=logging.INFO)

NUM_GENERATIONS = 1000

N= 100

POPULATION_SIZE = 70        #100 o 70
OFFSPRING_SIZE =  70        #40

#PROBLEMS: 
# -con valori diversi di popolazione e offspring size non trovava soluzioni valide, arrivavamo a elitarismo di soluzioni non valide,
#     forse non stiamo dando il giusto peso alle cose, il fatto di trovare una soluzione valida (che copra tutti gli N numeri) non viene sempre
#     rispettata (rivedi fitness function con quelle proporzioni)
# -rivedere la fitness function

# List of lists generator
def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

nodes = 0

seed = 42

space = list( _ for _ in set(tuple(sorted(set(_))) for _ in problem(N, seed)))

PROBLEM_SIZE = len(space)

def collisions(sol):
    check_ = np.ones(N)*(N+1) #vettore di lunghezza N, se la soluzione e' giusta ogni elemento avra' valore pari al suo indice
    collision = 0
    for el in sol:
        for i in el:
            if check_[i] == i: #se il valore e' gia' presente segno la collisione
                collision += 1
            else:
                check_[i] = i
    return collision

def fitness(genome, space):
    sol = list()
    for i, _ in enumerate(genome):
        if _:
            sol.append(space[i])
    collisions_ = collisions(sol)

    check_set = set()
    for e in sol:
        check_set |= set(e)
    how_many_covered = len(check_set)
    #fit= -((collisions_)*0.1 + (N - how_many_covered)*0.9)  # da RIVEDERE, come dai più priorità al numero di numeri coperti?
    fit = (how_many_covered, -collisions_)
    return fit

def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: fitness(i, space))

def mutation(g):
    point1 = random.randint(0, PROBLEM_SIZE - 1)
    # Reversing one of the 1/0 in a random point of the individual/genome
    mutated = g[:point1] + (1 - g[point1],) + g[point1 + 1 :]
    point2 = random.randint(0, PROBLEM_SIZE - 1)
    if point2 == point1:
        if point1 == PROBLEM_SIZE -1:
            point2 -= 1
        elif point1 == 0:
            point2 += 1
        else:
            point2 = point1 - 1
    # Reversing one of the 1/0 in a random point of the individual/genome
    return mutated[:point2] + (1 - mutated[point2],) + mutated[point2 + 1 :]

def cross_over(g1, g2):
    cut = random.randint(0, PROBLEM_SIZE)
    return g1[:cut] + g2[cut:]


population = list()
for genome in [tuple([random.choice([1, 0]) for _ in range(PROBLEM_SIZE)]) for _ in range(POPULATION_SIZE)]:
    population.append(genome)

population = sorted(population, key=lambda i: fitness(i,space), reverse=True)

exit_ = 0
for g in range(NUM_GENERATIONS):
    offspring = list()
    for i in range(OFFSPRING_SIZE):
        if random.random() < 0.3:
            p = tournament(population)
            o = mutation(p)
        else:
            p1 = tournament(population)
            p2 = tournament(population)
            o = cross_over(p1, p2)
        f = fitness(o, space)
        offspring.append(o)
            
        ############################################
        sol_intermedia = list()
        for i, _ in enumerate(population[0]):
            if _:
                sol_intermedia.append(space[i])
        check_set = set()
       
        for e in sol_intermedia:
            check_set |= set(e)
        how_many_covered = len(check_set)
        if N==20 and how_many_covered == 20 and collisions(sol_intermedia) == 3: 
            exit_ = 1
            print(f"FOUND at {g+1}")
            break
        if N==10 and how_many_covered == 10 and collisions(sol_intermedia) == 0: 
            exit_ = 1
            print(f"FOUND at {g+1}")
            break
        if N==5 and how_many_covered == 5 and collisions(sol_intermedia) == 0: 
            exit_ = 1
            print(f"FOUND at {g+1}")
            break
        ############################################
    population += offspring
    population = sorted(population, key=lambda i: fitness(i,space), reverse=True)[:POPULATION_SIZE]
    print(fitness(population[0], space), g+1)
    if exit_:
        break

############################################


sol_fin = list()
for i, _ in enumerate(population[0]):
    if _:
        sol_fin.append(space[i])


print(f"Best solution up to now ({NUM_GENERATIONS} generations): {sol_fin}")
check_set = set()
for e in sol_fin:
    check_set |= set(e)
how_many_covered = len(check_set)
print(f"How many covered: {how_many_covered}")
print(f"Collisions: { collisions(sol_fin)}")
print(f"Weight: {sum(len(_) for _ in sol_fin)}")
############################################