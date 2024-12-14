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
puzzle_day = 12
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

# example1 = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
# a recursive solution just for the fun of writing it :)
global grid, H, W
global counted

def connected_comp(rID, r, c):
    global grid
    global H, W
    global counted

    if r < 0 or c < 0 or r >= H or c >= W:
        return 0, 1     # no more area, but one edge

    if counted[r, c] == 1 and grid[r, c] == rID:
        return 0, 0     # have seen it before
    
    if rID != grid[r, c]:
        return 0, 1     # edge with another region

    counted[r, c] = 1

    a1, p1 = connected_comp(rID, r+1, c)
    a2, p2 = connected_comp(rID, r-1, c)
    a3, p3 = connected_comp(rID, r, c+1)
    a4, p4 = connected_comp(rID, r, c-1)

    area = a1 + a2 + a3 + a4
    perimeter = p1 + p2 + p3 + p4

    return area + 1, perimeter

def part1(data):
    global grid
    grid = np.array([[c for c in line] for line in data])
    global H, W
    H, W = grid.shape
    global counted
    counted = np.zeros((H, W))
    
    total = 0
    for r in range(H):
        for c in range(W):
            if not counted[r, c]:
                area, perimeter = connected_comp(grid[r, c], r, c)
                total += area * perimeter

    return total

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

example2 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def connected_comp2(rID, r, c):
    global grid
    global H, W
    global counted

    if counted[r, c] == 1 and grid[r, c] == rID:
        return 0, 0     # have seen it before
    
    if rID != grid[r, c]:
        return 0, 0     # edge with another region

    counted[r, c] = 1

    # count corners (the same as counting long edges)
    cur_per = 0
    if grid[r+1, c] != rID and grid[r, c+1] != rID:
        cur_per += 1
    if grid[r, c+1] != rID and grid[r-1, c] != rID:
        cur_per += 1
    if grid[r-1, c] != rID and grid[r, c-1] != rID:
        cur_per += 1
    if grid[r, c-1] != rID and grid[r+1, c] != rID:
        cur_per += 1
        
    if grid[r+1, c] == rID and grid[r, c+1] == rID and grid[r+1, c+1] != rID:
        cur_per += 1
    if grid[r, c+1] == rID and grid[r-1, c] == rID and grid[r-1, c+1] != rID:
        cur_per += 1
    if grid[r-1, c] == rID and grid[r, c-1] == rID and grid[r-1, c-1] != rID:
        cur_per += 1
    if grid[r, c-1] == rID and grid[r+1, c] == rID and grid[r+1, c-1] != rID:
        cur_per += 1

    a1, p1 = connected_comp2(rID, r+1, c)
    a2, p2 = connected_comp2(rID, r-1, c)
    a3, p3 = connected_comp2(rID, r, c+1)
    a4, p4 = connected_comp2(rID, r, c-1)

    area = a1 + a2 + a3 + a4
    perimeter = cur_per + p1 + p2 + p3 + p4

    return area + 1, perimeter

def part2(data):
    global grid
    global H, W
    H = len(data)
    W = len(data[0])
    # expand the grid to avoid boundary tests
    grid = np.full((H+2, W+2), '.')
    grid[1:-1, 1:-1] = np.array([[c for c in line] for line in data])
    print(grid)
    H, W = grid.shape

    global counted
    counted = np.zeros((H, W))
    # boundary already counted -> no recursion there
    counted[0, :] = 1
    counted[:, 0] = 1
    counted[-1, :] = 1
    counted[:, -1] = 1
    
    total = 0
    for r in range(H):
        for c in range(W):
            if not counted[r, c]:
                area, perimeter = connected_comp2(grid[r, c], r, c)
                total += area * perimeter

    return total

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
