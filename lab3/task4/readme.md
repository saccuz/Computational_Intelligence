# Laboratory 3 part 3: Nim

## Task

Write agents able to play Nim, with an arbitrary number of rows and an upper bound  on the number of objects that can be removed in a turn (a.k.a., subtraction game).

The player taking the last object wins.

- Task 3.4: An agent using Reinforcement Learning.

## Explanation

The code is structured in three files. 
- _nim.py_ is the library file in which the Nim class, the cook status, the various rules/strategies, possible moves and the rewards are defined.
- _lab3.py_ is the file containing the main and the evaluation phase.
- _agent.py_ is the library file in which we define the agent and the learning phase and we calculate the best action.

Training of the agent is performed through a certain number of **episodes**, during which we made the agent compete against an opponent in order to let the agent learn which moves lead to victory and which not. \
After every **episode** we perform an evaluation phase in which we made the agent play against the opponent without learning.
During the train phase we keep the best individual based on the evaluation.

Ended the training phase, we evaluate the best individual against the opponent, to test the best player obtained from the algorithm. \
Given that Reinforcement Learning is extremely problem specific, we decide to use _ply_ as the state, in order to maximize the effectiveness of the algorithm, giving up generalization capability.

## Results
The trained agent is able to easily defeat various strategies, with good winning rates. \
Unfortunately we can not say the same against the optimal strategy, where we can't achieve any significant result.

## Contributors

- [Simone Mascali](https://github.com/vmask25)
- [Fabrizio Sulpizio](https://github.com/Xiusss)

Professor's repository took as reference: https://github.com/squillero/computational-intelligence
