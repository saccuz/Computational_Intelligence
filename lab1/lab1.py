from copy import copy
import random
import numpy as np

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def check_solution(solution, N):
    if len(solution) == 0:
        return (False, solution, 0)
    check_ = np.ones(N)*(N+1) #vettore di lunghezza N, se la soluzione e' giusta ogni elemento avra' valore pari al suo indice
    collision = 0
    for el in solution:
        for i in el:
            if check_[i] == i: #se il valore e' gia' presente segno la collisione
                collision += 1
            else:
                check_[i] = i
    if any(j == N+1 for j in check_): #controllo che tutti gli elementi siano stati settati
        return (False, solution, collision)
    else:
        return (True, solution, collision)

def tree_explorer(sol, space, N):
    local_s = copy(sol)
    isCorrect = check_solution(sol, N)
    if  len(local_s) != 0 and len(local_s[-1]) <= isCorrect[2]: #controllo che il numero di collisioni sia minore della lunghezza della lista
        local_s.pop(-1)
    if isCorrect[0]:
        return isCorrect
    for l in space:
        local_s.append(l)
        ind_l = space.index(l)
        ctrl = tree_explorer(local_s, space[ind_l+1 : ], N)
        if ctrl[0]:
            return ctrl

if __name__ == "__main__":
    seed = 42
    for N in [5, 10, 20, 100, 500, 1000]:
    #N = 5
        space = problem(N, seed)
        space.sort(key=len, reverse=True)
        solution = []
        solution = tree_explorer([], space, N)
        print(f"Solution for {N}: {solution}")


