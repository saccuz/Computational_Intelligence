# Lab 1: Set Covering

## Task
Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$ determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$ such that each number between $0$ and $N-1$ appears in at least one list and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Development

### 1. Prove that a solution exists
Using the [greedy algorithm](https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab1_set-covering.ipynb) provided by Professor Squillero, we can prove that a solution exist for $N = 5, 10, 20, 100, 500, 1000$. However the one provided by the greedy algorithm is not the Optimal one, so we have to try a different approach.

### 2. Find the Optimal Solution
To find the optimal solution, I opted for a Breadth First search.
Using _itertools.combinations_ inside a loop, I generate all possible ordered combinations (without repetition).
For every iteration _i_ of the loop I explore all the nodes of the _i-th_ level of the search tree.
After the algorithm found a solution, it still explores the subsequent level and, in case no better solution is found, it stops the execution, because the solution is already Optimal.

This kind of search is, without doubt, much slower in respect to an Informed Strategy, and it visit a much larger number of nodes.

Due to the too high process time, the solution has been calculated only for $N$ lesser than 20 (included).

|$N$|Nodes Processed|Number of Elements in $L_{s_i}$ |
|---|---|---|
|5|2300|5|
|10|19600|10|
|20|278256|23|
|100|-|-|
|500|-|-|
|1000|-|-|

## Contributors

- [Fabrizio Sulpicio](https://github.com/Xiusss)
- [Simone Mascali](https://github.com/vmask25)