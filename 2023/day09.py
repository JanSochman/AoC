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
import copy
from collections import deque, Counter
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
puzzle_day = 9
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    total = 0
    for L in data:
        pred = 0 
        hist = np.array(L.split(), np.int64)
        while hist.any():
            pred += hist[-1]
            hist = hist[1:] - hist[:-1]
        total += pred
    return total

# %% --------------------------------------------------
res_example = part1(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full)
print(res_full)

# %% --------------------------------------------------
# PART 2
example2 = example1

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    total = 0
    for L in data:
        pred = 0
        hist = np.array(L.split(), np.int64)
        while hist.any():
            pred += hist[0]
            hist = hist[:-1] - hist[1:]
        total += pred
    return total

# %% --------------------------------------------------
res_example = part2(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full)
print(res_full)

# %% --------------------------------------------------
