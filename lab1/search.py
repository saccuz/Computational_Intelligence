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


def tree_explorer_DF(sol, space, N):
    """ Function that check if exists at least a solution, but not guarantees it is the best one """
    local_s = copy(sol)
    isCorrect = check_solution(sol, N)
    if  len(local_s) != 0 and len(local_s[-1]) <= isCorrect[2]: # check number of collision less or equal of list's length
        sol.pop(-1)
    if isCorrect[0]:
        return isCorrect
    for l in space:
        local_s.append(l) # adding a new element in the possible solution

        global nodes
        nodes += 1

        ind_l = space.index(l)
        ctrl = tree_explorer_DF(local_s, space[ind_l+1 : ], N)
        if ctrl is not None and ctrl[0]:
            if nodes != 0:
                print(f"Visited nodes with partial DF: {nodes}")
                nodes = 0
            return ctrl

def tree_explorer_BF(space, N):
    """ Function that produce the best solution. It can be computationally too massive """
    nodes = 0
    for i in range(N):
        for e in combinations(space, i): # create every possible combination of element using i elements
            nodes += 1
            isCorrect = check_solution(e, N)
            if isCorrect[0]:
                print(f"Visited nodes with BF: {nodes}")
                return isCorrect #if the solution is correct, it's also the best solution, because is the first I can find with minimum length
    return (False, [], 0)