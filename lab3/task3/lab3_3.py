import random
import time
from copy import deepcopy

import nim
from nim import Nim

# This size can be brought up to 16 with a reasonable response time
NIM_SIZE = 11
# This depth limit can be changed to 100000 or 150000 to speed up the minmax response (with winning rate disadvantages)
DEPTH = 200000

# Global variables used to limit the depth
dict_size = 0
num_moves = 0

# Printing of dictionary of states sizes and computational time
def statistics(dict_of_states: dict, start: float)-> None:
    sum = 0
    # Calculating the sum of the number of possible moves in each state
    for _ in dict_of_states.values():
        sum += len(_)
    print(f"{sum} (total possible moves - number of values in the dictionary of states)")
    # Printing the number of visited nodes
    print(f"{len(dict_of_states.keys())} (visited nodes/states - number of keys in the dictionary of states)\n")

    end = time.time()
    print(f"Computational time: {(end - start)//60} mins and {(end-start)-(((end - start)//60)*60)} secs\n")

# Allowing our player to do three turns with a random strategy (to escape the current stucked situation instead of going too deep in the tree) 
# and then zeroing the dict_size counter to return again to explore the tree and to save new states.
def manage_depth():
    global num_moves, dict_size
    
    if dict_size >= DEPTH:
        num_moves += 1
        if num_moves == 3:
            dict_size = 0
            num_moves = 0

# Checking if the current state is the end of the game (exploited by the min max to understand if the current player won)
def evaluation(state: Nim) -> int:
    if not state:
        return -1
    else:
        return 0

# Min Max recursive function
def minMax(state: Nim, dict_of_states: dict()):
    global dict_size

    # Check if the game is finished
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

        # Generating all possible moves
        for ply in [(len(state.rows)-1-r, o) for r, c in enumerate(reversed(state.rows)) for o in range(1, c + 1)]: #used list comprehension for optimization
            dict_of_states[state.rows].append((ply,-1))
            # Trying the move and recursively calling the min max on the new state
            tmp_state = deepcopy(state)
            _ , val = minMax(tmp_state.nimming(ply), dict_of_states)
            results.append((ply, -val))

            # Alpha-beta pruning, if a -val is 1 then we already found a good ply so it's unnecessary to continue the search
            if -val == 1: 
                dict_of_states[state.rows] = [(ply,-val)]
                break
    else:
        # Already explored state
        return max(dict_of_states[state.rows], key=lambda x: x[1])  

    return max(results, key=lambda x: x[1])

if __name__ == "__main__":
    start = time.time()
    try:
        # Dictionary that contains the possible states as keys and tuples (ply, ply "goodness") as values
        dict_of_states = dict()
        # Turn identifier
        i = random.randint(0,1)
        if i == 0:
            print("First player: opponent")
        else:
            print("First player: you (min max)")
        # Initial nim board
        board = Nim(NIM_SIZE)
        # The opponent player (in nim.py it's possible to change the opponent e.g. to "pure_random" or to "gabriele")
        player2 = nim.opponent_strategy()

        print(board)

        # Game
        while board:
            # Min Max turn
            if i % 2 != 0:
                player = 0
                ply, _ = minMax(board, dict_of_states)
                manage_depth()
            # Opponent turn
            else:
                player = 1
                opponent = player2.move()
                ply = opponent(board)
            
            board.nimming(ply)
            i+=1

            print(board)

        if player == 1:
            print("==> YOU LOSE")
        else:
            print("==> YOU WIN")
        
        statistics(dict_of_states, start)

    except KeyboardInterrupt: #for debug purpose
        statistics(dict_of_states, start)