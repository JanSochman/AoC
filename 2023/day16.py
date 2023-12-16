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
from collections import deque, Counter, defaultdict, namedtuple
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
puzzle_day = 16
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    grid = np.array([[c for c in line] for line in data])
    H, W = grid.shape
    energy = np.zeros((H, W), dtype=np.int32)
    # r, c, dr, dc
    beams = {(0, -1, 0, 1)}
    tested = set()
    while beams:
        b = beams.pop()
        if b in tested:
            continue
        tested.add(b)

        r, c, dr, dc = b
        r += dr
        c += dc
        while c < W and c >= 0 and r < H and r >=0 and (grid[r, c] == '.' or (dr == 0 and grid[r, c] == '-') or (dc == 0 and grid[r, c] == '|')):
            energy[r, c] = 1
            r += dr
            c += dc

        if c == W or c < 0 or r == H or r < 0:  # beam left the grid
            continue

        energy[r, c] = 1

        if grid[r, c] == '\\':
            dr, dc = dc, dr
            beams.add((r, c, dr, dc))
        if grid[r, c] == '/':
            dr, dc = -dc, -dr
            beams.add((r, c, dr, dc))
        if grid[r, c] == '|':
            beams.add((r, c, -1, 0))
            beams.add((r, c, 1, 0))
        if grid[r, c] == '-':
            beams.add((r, c, 0, -1))
            beams.add((r, c, 0, 1))

    return energy.sum()
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
    grid = np.array([[c for c in line] for line in data])
    H, W = grid.shape

    # r, c, dr, dc
    start_pos = [(r, -1, 0, 1) for r in range(H)] + [(r, W, 0, -1) for r in range(H)] + [(-1, c, 1, 0) for c in range(W)] + [(H, c, -1, 0) for c in range(W)] 

    best = 0
    for pos in start_pos:
        energy = np.zeros((H, W), dtype=np.int32)
        beams = {pos}
        tested = set()
        while beams:
            b = beams.pop()
            if b in tested:
                continue
            tested.add(b)

            r, c, dr, dc = b
            r += dr
            c += dc
            while c < W and c >= 0 and r < H and r >=0 and (grid[r, c] == '.' or (dr == 0 and grid[r, c] == '-') or (dc == 0 and grid[r, c] == '|')):
                energy[r, c] = 1
                r += dr
                c += dc

            if c == W or c < 0 or r == H or r < 0:  # beam left the grid
                continue

            energy[r, c] = 1

            if grid[r, c] == '\\':
                dr, dc = dc, dr
                beams.add((r, c, dr, dc))
            if grid[r, c] == '/':
                dr, dc = -dc, -dr
                beams.add((r, c, dr, dc))
            if grid[r, c] == '|':
                beams.add((r, c, -1, 0))
                beams.add((r, c, 1, 0))
            if grid[r, c] == '-':
                beams.add((r, c, 0, -1))
                beams.add((r, c, 0, 1))

        best = max(best, energy.sum())

    return best

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
