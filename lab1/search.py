from itertools import combinations
import logging

nodes = 0

def check_solution(solution, N):
    if len(solution) == 0:
        return (False, solution)
    check_ = set(range(N)) # create a set with all the number of the requested solution
    sol = set()
    for e in solution:
        sol |= set(e)  # add in the set every number of the possible solution
    if sol == check_: #check if the solution is equal to the request, not a subset nor a overset
        return (True, solution)
    else:
        return (False, solution)

def tree_explorer_BF(space, N):
    """ Function that produce the best solution. It can be computationally too massive """
    level = 0
    nodes = []
    solution = list()
    for i in range(1,N):
        nod = 0
        for e in combinations(space, i): # create every possible combination of element using i elements
            nod += 1
            isCorrect = check_solution(e, N)
            if isCorrect[0]:
                if len(solution) == 0 or sum(len(e) for e in solution[1]) > sum(len(e) for e in isCorrect[1]): # check if the solution found is better than the already existing solution
                    solution = isCorrect
                    level = i
        nodes.append(nod)
        if level != 0 and level+1 <= i:
            break
    if len(solution) != 0:
        nodes.pop(-1)
        logging.debug(f"Visited nodes with BF: {sum(nodes)}")
        return solution
    return (False, [])

def greedy_search(space, N):
    goal = set(range(N))
    covered = set()
    solution = list()
    while goal != covered:
        x = set(space.pop(0))
        if not x < covered: # if x is not completely contained inside covered
            solution.append(x)
            covered |= x # union without repetition
    return solution