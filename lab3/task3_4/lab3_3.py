import random
import time
from copy import deepcopy

import nim
from nim import Nim

NIM_SIZE = 16
DEPTH = 200000
dict_size = 0
num_moves = 0

def statistics(dict_of_states: dict, start: float)-> None:
    sum = 0
    for _ in dict_of_states.values():
        sum += len(_)
    print(sum)
    print(len(dict_of_states.keys()))

    end = time.time()
    print(f"Computational time: {(end - start)//60} mins and {(end-start)-(((end - start)//60)*60)} secs")

def manage_depth():
    global num_moves, dict_size
    
    if dict_size >= DEPTH:
        num_moves += 1
        if num_moves == 3:
            dict_size = 0
            num_moves = 0

def evaluation(state: Nim) -> int:
    if not state:
        return -1
    else:
        return 0

def minMax(state: Nim, dict_of_states: dict()):
    global dict_size

    val = evaluation(state)
    if val != 0:
        return None, val

    # Depth limiting
    if state and dict_size >= DEPTH:
        if state.rows not in dict_of_states:
            return nim.pure_random(state),1
        else: 
            return max(dict_of_states[state.rows], key=lambda x: x[1])

    results = list()

    if state.rows not in dict_of_states and state:
        dict_of_states[state.rows] = list()
        dict_size+=1

        for ply in [(len(state.rows)-1-r, o) for r, c in enumerate(reversed(state.rows)) for o in range(1, c + 1)]: #used "list comprehension" for optimization
            dict_of_states[state.rows].append((ply,-1))

            tmp_state = deepcopy(state)
            _ , val = minMax(tmp_state.nimming(ply), dict_of_states)
            results.append((ply, -val))

            if -val == 1: #alpha-beta pruning
                dict_of_states[state.rows] = [(ply,-val)]
                break
    else:
        return max(dict_of_states[state.rows], key=lambda x: x[1])  

    return max(results, key=lambda x: x[1])

if __name__ == "__main__":
    start = time.time()
    try:
        dict_of_states = dict()
        i = random.randint(0,1)
        print(f"Player: {1-i}")
        board = Nim(NIM_SIZE)
        player2 = nim.opponent_strategy()

        print(board)

        while board:
            if i % 2 != 0:
                player = 0
                ply, _ = minMax(board, dict_of_states)
                manage_depth()
            else:
                player = 1
                opponent = player2.move()
                ply = opponent(board)
            
            board.nimming(ply)
            i+=1

            print(board)

        if player == 1:
            print("YOU LOSE")
        else:
            print("YOU WIN")
        
        statistics(dict_of_states, start)

    except KeyboardInterrupt: #for debug purpose
        statistics(dict_of_states, start)