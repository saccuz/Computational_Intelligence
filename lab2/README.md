# Lab 2: Set Covering through a genetic algorithm

## Task
Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$ determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$ such that each number between $0$ and $N-1$ appears in at least one list and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Development

### 1. Prove that a solution exists

Through the analysis of the results obtained in the first lab, we know that a solution exists. We are committed in finding the optimal one with a wide problem space, focusing on performance with greater values of N (like 2000, 5000 and 10000). 

### 2. Find the Optimal Solution
Given the nature of the problem and the used techniques, we are not able to surely find the optimal solution.
We have two versions of the algorithm, in this repository there is the Version 2, and in the other teammates' repository there is the Version 1.\
In both cases, to find a good solution, we opted for a genetic algorithm where we represent each genome as a bitmap of 0's and only one "1" randomly chosen at the beginning to initialize the population. 

## Version 2
In each generation we take one of two possible paths: 
- the first, with a probability of 30%, in which we select a random parent and we mutate it to obtain the offspring (instead of using a tournament, to increment the randomness);
- the second, with a probability of 70%, in which we select two parents through two different tournaments of size 2, and then we cross-over these two parents to obtain the offspring;

At the end of each generation we save the fittest between the previous population, we drop the entire previous population, keeping the offsprings as the new population, together with the previous saved fittest, and then we start the new generation.\
The cross-over strategy we use composes the result picking a slice of random dimension from each of the parents, so it's a very basic one, but it still gives good results.\
The tournament is a basic tournament picking two parents at random inside the population and making them "fight" comparing their fitness.\
To determine the fitness of a potential solution we calculate the amount of covered numbers, and then we calculate the amount of collisions (duplicates) in the current solution.\
With each generation we try to maximize the covered numbers between 0 and N-1 at first, and then we try to minimize the amount of collisions (maximizing -collisions).\
To prevent elitism we apply a double mutation (two "bit tilts") with a rate of 30% as cited before.\
With a reasonable time we achieve good results for very high values of N.

Comparing to lab1, we succeeded in calculating the solution for $N$'s bigger than 20 reaching N=10000 in a quite reasonable time (it strongly depends on number of generations, and population and offspring sizes).

Here is reported a table in which we report the weight results for different values of N, changing the population and offspring sizes, and comparing the Version 1 with the Version 2 of the algorithm, including also the bloating and mean bloating.

![table](/results.png "Results")

## Improvements
We are sure that some improvements in the logic of the genetic algorithm are possible, some improving ideas we had are only cited in comments directly in the code, but we are open to suggestions and critics about our versions.

## Contributors

- [Simone Mascali](https://github.com/vmask25)
- [Fabrizio Sulpizio](https://github.com/Xiusss)