from collections import namedtuple
from copy import deepcopy
from typing import Callable
import random

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    # this allow to use the while loop on the object (when all rows are zeroed this returns false)
    def __bool__(self):
        return sum(self._rows) > 0

    # representation "override"
    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)
    
    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

class Strategy:
    def __init__(self, dna: list) -> None:
        self._dna = dna
        self._step = 0
    
    def move(self) -> Callable:
        next_move = self._dna[self._step]
        self._step += 1
        if self._step >= len(self._dna):
            self._step = 0
        return next_move


# Sample (and silly) strategies

def nim_sum(state: Nim) -> int:
    result = state.rows[0]
    for row in state.rows[1:]:
        result = result ^ row
    return result

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k]
    cooked['active_rows_number'] = sum(o > 0 for o in state.rows)
    cooked['even_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 == 0 and x[1] != 0]
    cooked['odd_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 != 0]
    cooked['shortest_row'] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y:y[1])[0]
    cooked['longest_row'] = max((x for x in enumerate(state.rows)), key=lambda y:y[1])[0]
    cooked['nim_sum'] = nim_sum(state)

    brute_force = list()
    for m in cooked['possible_moves']:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked['brute_force'] = brute_force

    return cooked

def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    #return next(m for m in data['possible_moves'] if m[1] == data['min_sum'])
    return next((bf for bf in data['brute_force'] if bf[1] == 0), random.choice(data['brute_force']))[0]

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def shortest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))

def longest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

def pick_one_from_max(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], 1)

def pick_one_from_min(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], 1)

def pick_even_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['even_object_rows'] if data['even_object_rows'] != [] else data['odd_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, (state.rows[row_]//2)+1)

def pick_odd_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['odd_object_rows'] if data['odd_object_rows'] != [] else data['even_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, state.rows[row_]//2)

def opponent_strategy():
    return Strategy([pure_random])
    #return Strategy([shortest_row, longest_row]) #gabriele, longest_row is better

def strategy_genome(allele: int):
    return tactics[allele]

tactics = [gabriele,shortest_row,longest_row,pick_one_from_max,pick_one_from_min,pick_even_max,pick_odd_max]