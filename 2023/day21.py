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
from skimage.morphology import flood_fill
import cv2
from shapely.geometry import Polygon
from einops import rearrange
import networkx as nx
import heapq

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 21
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)


# %% --------------------------------------------------
def part1(data, steps):
    grid = np.array([[{'#': -1, '.': np.inf, 'S': 0}[c] for c in line] for line in data])
    s_row = ['S' in L for L in data].index(1)
    s_col = data[s_row].index('S')

    H, W = grid.shape
    
    # distance transform
    seeds = deque([(s_row, s_col)])
    deltas = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    while seeds:
        s_row, s_col = seeds.popleft()
        cur_val = grid[s_row, s_col]
        for d in deltas:
            r, c = s_row + d[0], s_col + d[1]
            if r >= 0 and r < H and c >=0 and c < W:
                if grid[r, c] > cur_val + 1:
                    grid[r, c] = cur_val + 1
                    seeds.append((r, c))

    res = np.sum((steps - grid[np.logical_and(grid <= steps, grid >= 0)]) % 2 == 0)
    
    return res

# %% --------------------------------------------------
res_example = part1(data_example[:], 6)
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
    return 0

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)
