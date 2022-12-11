import numpy as np
from nim import Nim
import random


class Agent(object):
    def __init__(self, board, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        self.state_history = []  # state, reward
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}
        self.init_reward(board)

    def init_reward(self, board: Nim, possible_moves = None):
        if possible_moves == None:
            possible_moves = board.possible_moves() 
        for ply in possible_moves:
            if ply not in self.G:
                self.G[ply] = np.random.uniform(low=1.0, high=0.1)            

    def choose_action(self, board, possible_moves):
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        self.init_reward(board, possible_moves)
        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_move = random.choice(possible_moves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for ply in possible_moves:
                if self.G[ply] >= maxG:
                    next_move = ply
                    maxG = self.G[ply]

        return next_move

    def choose_action_evaluate(self, board, possible_moves):
        maxG = -10e15
        next_move = None
        # if exploiting, gather all possible actions and choose one with the highest G (reward)
        for ply in possible_moves:
            if ply in self.G:
                if self.G[ply] >= maxG:
                    next_move = ply
                    maxG = self.G[ply]
            else:
                next_move = random.choice(possible_moves)

        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play
                                     # to reduce the exploration favoring the exploitation