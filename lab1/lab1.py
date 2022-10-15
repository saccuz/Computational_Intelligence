import random
import search

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

if __name__ == "__main__":
    seed = 42
    for N in [5, 10, 20, 100, 500, 1000]:
        space = problem(N, seed)
        space.sort(key=len)
        solution = search.tree_explorer_DF([], space, N)
        print(f"Possible solution for {N}: {len(solution[1])} with {sum(len(e) for e in solution[1])} elements")
    
    for N in [5, 10, 20, 100, 500, 1000]:
        space = problem(N, seed)
        space.sort(key=len)
        solution = search.tree_explorer_BF(space, N)
        print(f"Optimal solution for {N}: {len(solution[1])} with {sum(len(e) for e in solution[1])} elements")