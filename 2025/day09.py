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
from shapely.geometry import Polygon, Point, MultiPoint
from einops import rearrange
import networkx as nx
import heapq
import time
from matplotlib.path import Path

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2025
puzzle_day = 9
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    tiles = np.array([[float(c) for c in line.split(',')] for line in data])
    N = tiles.shape[0]
    dists = cdist(tiles, tiles, 'cityblock')
    
    midx = np.argmax(dists)
    idx1 = midx // N
    idx2 = midx % N

    return int((abs(tiles[idx1, 0] - tiles[idx2, 0]) + 1) * (abs(tiles[idx1, 1] - tiles[idx2, 1]) + 1))

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
t0 = time.time()
res_full = part1(data_full[:])
t1 = time.time()
print(res_full)
print(f'{t1-t0}s')

# %% --------------------------------------------------
# ========== PART 2 ==========
data_example = parse_input(puzzle.examples[-1].input_data)

# %% --------------------------------------------------
# works only for data_full, as it is specialized to that particular edge case
def part2(data):
    tiles = np.array([[int(c) for c in line.split(',')] for line in data])
    N = tiles.shape[0]
    dists = np.linalg.norm(tiles[1:, :] - tiles[:-1, :], axis=1)
    t = np.argmax(dists) + 1
    root_tiles = [t+1, t]
    max_size = 0
    t1 = root_tiles[0]
    for t2 in range(N):
        r, c = tiles[t1, :]
        if tiles[t2, 1] >= c:
            continue

        cur_size = int((abs(r - tiles[t2, 0]) + 1) * (abs(c - tiles[t2, 1]) + 1))
        if cur_size <= max_size:
            continue
        
        if not tile_poly.covers(Point(tiles[t2, 0], c)) or not tile_poly.covers(Point(r, tiles[t2, 1])):
            continue

        max_size = cur_size

    t1 = root_tiles[1]
    for t2 in range(N):
        r, c = tiles[t1, :]
        if tiles[t2, 1] <= c:
            continue
        
        cur_size = int((abs(r - tiles[t2, 0]) + 1) * (abs(c - tiles[t2, 1]) + 1))
        if cur_size <= max_size:
            continue
        
        if not tile_poly.covers(Point(tiles[t2, 0], c)) or not tile_poly.covers(Point(r, tiles[t2, 1])):
            continue

        max_size = cur_size
        
    return max_size

# %% --------------------------------------------------
tile_poly = Polygon(np.array([[int(c) for c in line.split(',')] for line in data_example]))

res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
t0 = time.time()
tile_poly = Polygon(np.array([[int(c) for c in line.split(',')] for line in data_full]))

res_full = part2(data_full[:])
t1 = time.time()
print(res_full)
print(f'{t1-t0}s')

# %% --------------------------------------------------