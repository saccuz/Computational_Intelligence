# Laboratory 3 part 1: Nim

## Task

Write agents able to play Nim, with an arbitrary number of rows and an upper bound  on the number of objects that can be removed in a turn (a.k.a., subtraction game).

The player taking the last object wins.

- Task 3.1: An agent using fixed rules based on nim-sum (i.e., an expert system)
- Task 3.2: An agent using evolved rules

The current code is actually the one to solve the _Task 3.2_ because the _3.1_ is simply a "static" version of the _3.2_ (static meant as not evolving the strategies/rules, but the initial fixed rules were the same 7 we used in the evolutionary one).

## Explanation

The code is structured in two files. \
"nim.py" is the library file in which the Nim class, the cook status and the various rules/strategies are defined. \
"lab3.py" is the file containing the main. \
We make the evolution of the strategies/rules in a four turns way:
- In the first turn our genome competes against "dumb_strategy" agent.
- In the second, with "pure_random" agent.
- In the third with "gabriele" agent (because we found out that it works not so bad with respect to random).
- In the fourth turn it competes with the Professor's "optimal_strategy" that uses the nim sum to represent the expert user.

In these way we expect to have a learning slope that is not too steep.

Our genome is composed by a *list of probabilities* and each probability represents the probability to use that strategy/rule (also an indicator of the goodness/effectiveness of the strategy/rule). \
The strategies/rules are 7 so in this case the genome is initially a list of 7 elements with 0.5 as default values, and during the evolution these values are incremented/decremented to increment the probability to pick the more winning strategies in the next individuals and to pick the best couple in the end.

For each one of these four turns, 100 generations are made, and for each generation an individual is generated picking 2 of the 7 strategies/rules we decided to use.
We make this individual compete against the opponent of the turn (e.g. dumb_strategy in the first 100 generations) and if the results are better than the current champion couple of rules we reassign this individual as champion couple (current champion strategy).

Ended the 100 rounds of this individual competing with the current opponent, the genome is evolved, so if the results are good the probabilities of the two selected strategies are incremented, and the others are decremented (the decrement step is half the increment in order not to penalize too much the strategies not selected for this individual).

At the end of each turn it's printed the champion strategy formed by the couple of rules/strategies (*maybe it could be expanded making also the number of picked rules an evolving parameter, although we found an optimal spot with  number_of_rules = 2*).

After these four turns some statistics are provided (mean and victory, we just used those to understand how the algorithm was doing) and the "Evolved genome: " presents the couple of rules/strategies that represent the evolved strategy, having the highest evolved probabilities.
This strategy is then competed with the last winning champion and the best strategy between the two is so presented in the end, but often the last champion is good against the optimal but not so good against the other or against the evolved one.

In fact, interesting results are that using e.g. pick_one_from_max alternated with pick_odd_max, or pick_one_from_min alternated with pick_odd_max lead to good results competing with the optimal_strategy (nim sum) opponent, but they perform badly with the other opponents (like pure_random only and gabriele only).

Maybe a more sophisticated evolution strategy could perform better with all the kind of opponents.
The one we call "champion" in the end performs very well against the optimal_strategy, while our "evolved" performs very badly against the optimal_strategy, while in the competition "champion" vs "evolved", often "evolved" wins very well.

An idea we didn't try to implement yet, is to have rules that are more "situational" as the Professor said in the last lesson, in sense that if the table is in a certain situation then do something, but also trying ourself to play online at nim and thinking about possible situational rules, the only one we thought at the moment is that if the rows are even then leave to the opponent an odd number of rows, or the other way round, but more sophisticated rules could improve better our current algorithm.

## Interesting results

### Evolved common results: 
              gabriele      - pick_odd_max 
              gabriele      - pick_even_max       <= BEST ONE FOUND THAT OVERALL WINS almost more than 50% (except vs the optimal opponent) 
              longest_row   - gabriele 
              pick_even_max - pick_one_from_max   <= ALSO THIS IS MORE OR LESS GOOD
              gabriele      - shortest_row        <= THIS IS VERY GOOD WITH THE FIRST TWO OPPONENTS, BUT VERY BAD WITH THE gabriele and optimal  
              trying with a dna of 3 strategies/rules also pick_even_max - gabriele - longest_row is not that bad

### Champion common results (doing well against the optimal_strategy that uses nim sum): 
              pick_odd_max  - pick_one_from_min 
              pick_one_from_max - pick_odd_max 


## Contributors

- [Simone Mascali](https://github.com/vmask25)
- [Fabrizio Sulpicio](https://github.com/Xiusss)

Professor's repository took as reference: https://github.com/squillero/computational-intelligence