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

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2024
puzzle_day = 6
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


# example1 = """.#...
# ....#
# .....
# .^.#.
# #....
# ..#.."""

# example1 = """##..
# ...#
# ....
# ^.#."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    grid = np.array([[c for c in line] for line in data])
    H, W = grid.shape
    visited = np.zeros((H, W), dtype=np.int32)
    
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    dir = 0
    pos =  np.array(np.where(grid == '^')).squeeze()
    v_num = 1
    while True:
        visited[pos[0], pos[1]] = v_num
        v_num += 1
        new_pos = pos + dirs[dir]
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= H or new_pos[1] >= W:
            break
        
        if grid[new_pos[0], new_pos[1]] == '#':
            dir = (dir + 1) % 4
            continue
        
        pos = new_pos
    
    plt.imshow(visited)

    return (visited > 0).sum()

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
# slow, but works... :)
def test_loop(grid, visited, pos, dir):
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    H, W = grid.shape
    while True:
        if dir in visited[pos[0]][pos[1]]:
            return True
        visited[pos[0]][pos[1]].append(dir)

        new_pos = pos + dirs[dir]
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= H or new_pos[1] >= W:
            break
        
        if grid[new_pos[0], new_pos[1]] == '#':
            dir = (dir + 1) % 4
            continue
        
        pos = new_pos

    return False

def part2(data):
    grid = np.array([[c for c in line] for line in data])
    H, W = grid.shape
    visited = [[[] for _ in range(W)] for _ in range(H)]
    
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    dir = 0
    pos =  np.array(np.where(grid == '^')).squeeze()
    num_loops = 0
    while True:
        visited[pos[0]][pos[1]].append(dir)

        new_pos = pos + dirs[dir]
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= H or new_pos[1] >= W:
            break
        
        if grid[new_pos[0], new_pos[1]] == '#':
            dir = (dir + 1) % 4
            continue
        
        if not visited[new_pos[0]][new_pos[1]]:
            mod_grid = grid.copy()
            mod_grid[new_pos[0], new_pos[1]] = '#'
            if test_loop(mod_grid, copy.deepcopy(visited), pos, (dir + 1) % 4):
                num_loops += 1
        
        pos = new_pos
    
    return num_loops

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
