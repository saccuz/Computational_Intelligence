import random
import search

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


if __name__ == "__main__":

    NUM_GENERATIONS = 1000

    POPULATION_SIZE = 30
    OFFSPRING_SIZE = 20 

    seed = 42

    for N in [5, 10, 50, 100, 500, 1000, 2000, 5000]:
        space = list( _ for _ in set(tuple(sorted(set(_))) for _ in problem(N, seed)))

        how_many_covered, collisions, weight = search.evolutionary_solution(N, space, POPULATION_SIZE, OFFSPRING_SIZE, NUM_GENERATIONS)

        print(f"How many covered: {how_many_covered}")
        print(f"Collisions: {collisions}")
        print(f"Weight: {weight}")
        print(f"Population Size: {POPULATION_SIZE}")
        print(f"Offspring Size: {OFFSPRING_SIZE}")
        print(f"Generations: {NUM_GENERATIONS}")