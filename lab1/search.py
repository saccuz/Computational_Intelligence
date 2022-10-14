from copy import copy
import numpy as np

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

def tree_explorer_DF(sol, space, N):
    local_s = copy(sol)
    isCorrect = check_solution(sol, N)
    if  len(local_s) != 0 and len(local_s[-1]) <= isCorrect[2]: #controllo che il numero di collisioni sia minore della lunghezza della lista
        sol.pop(-1)
    if isCorrect[0]:
        return isCorrect
    for l in space:
        local_s.append(l)
        ind_l = space.index(l)
        ctrl = tree_explorer_DF(local_s, space[ind_l+1 : ], N)
        if ctrl is not None and ctrl[0]:
            return ctrl

def tree_explorer_BF(sol, space, N):

    return