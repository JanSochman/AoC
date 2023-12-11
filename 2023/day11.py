# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print
# import parse                        # easy string parsing 
from parse import parse
from types import SimpleNamespace as sn
# from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
import re                           # for parsing using regular expressions
from anytree import Node, RenderTree    # for building trees
from scipy import ndimage
from scipy.spatial.distance import cdist
import copy
from collections import deque, Counter, defaultdict
import parsy as ps
import portion as P
import math

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 11
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    universe = []
    for L in data:
        universe.append(list(L.replace('.', '0').replace('#', '1')))
    universe = np.array(universe, dtype=np.int64)
    
    # expand the universe (memory inefficient, but works :) )
    idxs = np.argwhere(universe.sum(axis=0) == 0).flatten()
    universe = np.insert(universe, idxs, 0, axis=1)
    idxs = np.argwhere(universe.sum(axis=1) == 0).flatten()
    universe = np.insert(universe, idxs, 0, axis=0)

    galaxies = np.argwhere(universe)
    total_distance = np.tril(cdist(galaxies, galaxies, metric='cityblock')).sum()
    
    return total_distance


# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# PART 2
example2 = example1

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    universe = []
    for L in data:
        universe.append(list(L.replace('.', '0').replace('#', '1')))
    universe = np.array(universe, dtype=np.int64)
    
    idxs_h = np.argwhere(universe.sum(axis=0) == 0).flatten()
    idxs_v = np.argwhere(universe.sum(axis=1) == 0).flatten()

    # distances in the original universe
    galaxies = np.argwhere(universe)
    distance = np.tril(cdist(galaxies, galaxies, metric='cityblock'))
    Ng = galaxies.shape[0]

    # expansion
    Ng = galaxies.shape[0]
    exp_coef = 1000000
    for i in range(Ng):
        for j in range(i+1, Ng):
            num_empty_v = np.dot(1 * (idxs_v > min(galaxies[i, 0], galaxies[j, 0])), 1 * (idxs_v < max(galaxies[i, 0], galaxies[j, 0])))
            num_empty_h = np.dot(1 * (idxs_h > min(galaxies[i, 1], galaxies[j, 1])), 1 * (idxs_h < max(galaxies[i, 1], galaxies[j, 1])))
            distance[j, i] = distance[j, i] + (exp_coef - 1) * num_empty_h + (exp_coef - 1) * num_empty_v
    
    return np.sum(distance)

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)
