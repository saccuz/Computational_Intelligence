from copy import copy
import numpy as np
from itertools import combinations

nodes = 0

def check_solution(solution, N):
    if len(solution) == 0:
        return (False, solution, 0)
    check_ = np.ones(N)*(N+1) # array of length N, if solution is correct, every element will have value equals his index
    collision = np.zeros(N)
    for el in solution:
        for i in el:
            if check_[i] == i: # mark collision if already present
                collision[i] = 1
            else:
                check_[i] = i
    if any(j == N+1 for j in check_): # check that every element has been set
        return (False, solution, np.sum(collision))
    else:
        return (True, solution, np.sum(collision))

def tree_explorer_BF(space, N):
    """ Function that produce the best solution. It can be computationally too massive """
    nodes = 0
    solution = []
    for i in range(1,N):
        for e in combinations(space, i): # create every possible combination of element using i elements
            nodes += 1
            isCorrect = check_solution(e, N)
            if isCorrect[0]:
                if len(solution) == 0 or sum(len(e) for e in solution[1]) > sum(len(e) for e in isCorrect[1]):
                    print(isCorrect)
                    solution = isCorrect
    if len(solution) != 0:
        print(f"Visited nodes with BF: {nodes}")
        return solution
    return (False, [], 0)