import random
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

import nim
from nim import Nim, Strategy
from agent import Agent

NIM_SIZE = 5
NUM_MATCHES_EVAL = 10
EPISODES = 10000

def evaluate(robot: Agent, player2: Strategy) -> float:
    won = 0
    for _ in range(NUM_MATCHES_EVAL):
        board = Nim(NIM_SIZE)
        player = 0
        i = random.randint(0,1)
        while board:
            if i % 2 != 0:
                ply = robot.choose_action_evaluate(board, board.possible_moves())
                player = 0
            else:
                opponent = player2.move()
                ply = opponent(board)
                player = 1
            board.nimming(ply)
            i+=1
        if player == 0:
            won += 1
    return won/NUM_MATCHES_EVAL

if __name__ == "__main__":
    start = time.time()
    dict_of_states = dict()
    board = Nim(NIM_SIZE)
    player2 = nim.opponent_strategy()
    agent = Agent(board, alpha=0.1, random_factor=0.4)
    best_agent = None
    max = -1

    # Plot
    moveHistory = []
    indices = []

    for e in tqdm(range(EPISODES), desc="Playing", ascii=False):    
        i = random.randint(0,1)
        # this while loop represents an EPISODE
        while board:
            if i % 2 != 0:
                player = 0
                ply = agent.choose_action(board, board.possible_moves())
                board.nimming(ply)
                reward = board.get_reward()  # get the new reward
                agent.update_state_history(ply, reward)
            else:
                player = 1
                opponent = player2.move()
                ply = opponent(board)
                board.nimming(ply)
            i+=1
        agent.learn()

        # Evaluation of the current agent
        results=evaluate(agent, player2) 
        if e % 50 == 0:
            moveHistory.append(results)
            indices.append(e)

        # Saving the current agent if it performs better in the evaluation
        if results >= max:
            max = results
            best_agent = agent

        # Resetting the board
        board = Nim(NIM_SIZE)


    plt.subplot(211)
    plt.plot(indices, moveHistory, "b")

    moveHistory2 = []
    indices2 = []
    meanHistory2 = []
    # Final evaluation of the best agent
    for c in tqdm(range(500)):
        results = evaluate(best_agent, nim.opponent_strategy_evaluate())
        meanHistory2.append(results)
        if c % 10 == 0:
            moveHistory2.append(results)
            indices2.append(c)
    mean_ = sum(meanHistory2)/500

    print(f"The average winning rate with the final best agent is: {mean_}")

    plt.subplot(212)
    plt.plot(indices2, moveHistory2, "b")
    plt.show()