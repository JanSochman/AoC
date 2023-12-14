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
import matplotlib.pyplot as plt

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 14
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
# a good solution, but it actually does not shift the round stones, so it can't be used for part 2 :(
def part1(data):
    # transpose the input and turn it upside down
    for row, L in enumerate(data):
        data[row] = list(L)
    data = np.array(data).T
    data = data[:, ::-1]
    columns = []
    for i in range(data.shape[0]):
        columns.append("".join(data[i, :].tolist()))
        
    H = data.shape[1]
    total_load = 0
    for c in columns:
        parts = c.split('#')
        ends = [len(parts[0])]
        for p in parts[1:]:
            ends.append(len(p) + 1 + ends[-1])
        load = 0
        for pi, p in enumerate(parts):
            cnt = p.count('O')
            load += sum(range(ends[pi], ends[pi]-cnt, -1))
        total_load += load
    
    return total_load

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
def coords_rot90cw(cols, rows, S):
    new_rows = cols[:]
    new_cols = S - rows - 1
    idxs = np.lexsort((new_rows, new_cols))
    new_rows = new_rows[idxs]
    new_cols = new_cols[idxs]

    return new_cols, new_rows

def tilt(s_cols, s_rows, c_cols, c_rows):
    Ns = len(s_cols)
    Nc = len(c_cols)
    # move the circular stones north
    sidx = 0
    cidx = 0
    while sidx < Ns-1 and cidx < Nc:
        # skip # from previous columns
        if c_cols[cidx] > s_cols[sidx]:
            sidx += 1
            continue

        # skip # if the curent O is not in the section below this #
        if s_rows[sidx+1] < c_rows[cidx]:
            sidx += 1
            continue

        pos = 1
        while cidx < Nc and s_cols[sidx] == c_cols[cidx] and s_rows[sidx+1] > c_rows[cidx]:
            c_rows[cidx] = s_rows[sidx] + pos
            cidx += 1
            pos += 1

        sidx += 1
        
    return c_cols, c_rows

def print_output(s_cols, s_rows, c_cols, c_rows, S):
    out = []
    for _ in range(S):
        out.append(['.' for _ in range(S)])
    for c, r in zip(s_cols, s_rows):
        out[r][c] = '#'
    for c, r in zip(c_cols, c_rows):
        out[r][c] = 'O'
    print("\n".join(["".join(row) for row in out]))
    

def part2(data):
    # convert to numerical np.array with # all around
    data = np.array([[{'O': 1, '#': -1, '.': 0}[c] for c in line] for line in data])
    data = np.pad(data, 1, constant_values=-1)
    
    S = data.shape[0]

    load_matrix = np.tile(np.arange(S-2, 0, -1), (S-2, 1)).T
    load_matrix = np.pad(load_matrix, 1)

    s_cols, s_rows = np.where(data.T == -1)
    c_cols, c_rows = np.where(data.T == 1)
    
    load = []
    # still too slow, running just for enough time to find the period
    for _ in range(200):
        c_cols, c_rows = tilt(s_cols, s_rows, c_cols, c_rows)
        c_cols, c_rows = coords_rot90cw(c_cols, c_rows, S)
        s_cols, s_rows = coords_rot90cw(s_cols, s_rows, S)

        c_cols, c_rows = tilt(s_cols, s_rows, c_cols, c_rows)
        c_cols, c_rows = coords_rot90cw(c_cols, c_rows, S)
        s_cols, s_rows = coords_rot90cw(s_cols, s_rows, S)

        c_cols, c_rows = tilt(s_cols, s_rows, c_cols, c_rows)
        c_cols, c_rows = coords_rot90cw(c_cols, c_rows, S)
        s_cols, s_rows = coords_rot90cw(s_cols, s_rows, S)

        c_cols, c_rows = tilt(s_cols, s_rows, c_cols, c_rows)
        c_cols, c_rows = coords_rot90cw(c_cols, c_rows, S)
        s_cols, s_rows = coords_rot90cw(s_cols, s_rows, S)

        total_load = np.sum(load_matrix[c_rows, c_cols])
        load.append(total_load)

    out = np.zeros((S, S))
    out[s_rows, s_cols] = -1
    out[c_rows, c_cols] = 1

    total_load = np.sum(load_matrix[c_rows, c_cols])

    return load

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

"""
The load has some initial period after which it starts to be periodic with period 42. 
I manually found the period and how does it fit into those 1000000000 cycles.
"""

# %% --------------------------------------------------
