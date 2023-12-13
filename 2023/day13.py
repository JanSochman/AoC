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
    # lines = input.split('\n')
    return input

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 13
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def test_symmetry(M, val=0):
    W = M.shape[1]
    for c in range(W-1):
        width = min(c+1, W-c-1)
        if np.sum(np.abs(M[:, c+1-width:c+1][:, ::-1] - M[:, c+1:c+1+width])) == val:
            return c + 1
    return 0

def part1(data, val=0):
    sum_number = 0
    blocks = data.split('\n\n')

    for block in blocks:
        M = np.array([[int(0 if c == '.' else 1) for c in row] for row in block.split('\n')])
        sum_number += test_symmetry(M, val)
        sum_number += 100 * test_symmetry(M.T, val)

    return sum_number

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    sum_number = part1(data, val=1)
    
    return sum_number

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
