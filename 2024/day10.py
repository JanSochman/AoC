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
import portion as P     # data structure and operations for intervals
import math
import matplotlib.pyplot as plt
from skimage.morphology import flood_fill
import cv2
from shapely.geometry import Polygon
from einops import rearrange
import networkx as nx
import heapq
import string

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2024
puzzle_day = 10
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

# example1 = """..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987...."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    grid = np.array([[int(c) if c != '.' else -1 for c in line] for line in data])
    H, W = grid.shape
    path = [[set() for _ in range(W)] for _ in range(H)]
    rows, cols = np.where(grid == 9)
    for id, (r, c) in enumerate(zip(rows, cols)):
        path[r][c].add(id)
    
    neigh = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    for val in range(9, 0, -1):
        rows, cols = np.where(grid == val)
        for r, c in zip(rows, cols):
            for n in neigh:
                r_n = r + n[0]
                c_n = c + n[1]
                if r_n >= 0 and r_n < H and c_n >= 0 and c_n < W:
                    if grid[r_n, c_n] == val - 1:
                        path[r_n][c_n].update(path[r][c])

    total = 0
    rows, cols = np.where(grid == 0)
    for id, (r, c) in enumerate(zip(rows, cols)):
        total += len(path[r][c])

    return total

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
    grid = np.array([[int(c) if c != '.' else -1 for c in line] for line in data])
    H, W = grid.shape
    path = np.zeros((H, W), dtype=np.int16)
    path[grid == 9] = 1
    
    neigh = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    for val in range(9, 0, -1):
        rows, cols = np.where(grid == val)
        for r, c in zip(rows, cols):
            for n in neigh:
                r_n = r + n[0]
                c_n = c + n[1]
                if r_n >= 0 and r_n < H and c_n >= 0 and c_n < W:
                    if grid[r_n, c_n] == val - 1:
                        path[r_n, c_n] += path[r, c]

    return sum(path[grid == 0])

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
