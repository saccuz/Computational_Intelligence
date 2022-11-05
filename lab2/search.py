import random
import logging
import numpy as np
# just for debugging
import time

def log(fittest, NUM_GENERATIONS, g):
    logging.debug(fittest, g+1)
    if g in [NUM_GENERATIONS//4, NUM_GENERATIONS//2,NUM_GENERATIONS-NUM_GENERATIONS//4, NUM_GENERATIONS-1]:
        print(f"Status: {100 * (g+1) // NUM_GENERATIONS}%\t- Fit: {fittest}")

def evolutionary_solution(N, space, POPULATION_SIZE, OFFSPRING_SIZE, NUM_GENERATIONS):

    def collisions(sol):
        check_ = np.ones(N)*(N+1) #vettore di lunghezza N, se la soluzione e' giusta ogni elemento avrà valore pari al suo indice
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
        
        fit = (how_many_covered, -collisions_)
        return fit

    def tournament(population, tournament_size=2):
        return max(random.choices(population, k=tournament_size), key=lambda i: fitness(i, space))

    # The mutation is made by 2 bit tilts, so two lists between the current genome lists are taken/not taken
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

    # The xover is a basic xover in which the result is composed by a slice of each of the two parents.
    def cross_over(g1, g2):
        cut = random.randint(0, PROBLEM_SIZE)
        return g1[:cut] + g2[cut:]

    
    PROBLEM_SIZE = len(space)

    # The initial population is randomly created with bitmaps of 0's and only one "1" randomly chosen
    population = list()
    for genome in [tuple([0 for _ in range(PROBLEM_SIZE)]) for _ in range(POPULATION_SIZE)]:
        point = random.randint(0, PROBLEM_SIZE - 1)
        mutated = genome[:point] + (1,) + genome[point + 1 :]
        population.append(mutated)

    population = sorted(population, key=lambda i: fitness(i,space), reverse=True)

    mutation_rate = 0.3
    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            if random.random() < mutation_rate:
                p = tournament(population,1)
                o = mutation(p)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = cross_over(p1, p2)
            offspring.append(o)

        population = sorted(population, key=lambda i: fitness(i,space), reverse=True)
        fittest = (population[0],fitness(population[0], space))
        population = offspring
        population[-1] = fittest[0]

        log(fittest[1], NUM_GENERATIONS, g)

    population = sorted(population, key=lambda i: fitness(i,space), reverse=True)
    sol_fin = list()
    for i, _ in enumerate(population[0]):
        if _:
            sol_fin.append(space[i])

    check_set = set()
    for e in sol_fin:
        check_set |= set(e)
    how_many_covered = len(check_set)
    return (how_many_covered, collisions(sol_fin), sum(len(_) for _ in sol_fin))
