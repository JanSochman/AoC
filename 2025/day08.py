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
year = 2025
puzzle_day = 8
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data, num_iters):
    jboxes = np.array([[float(c) for c in line.split(',')] for line in data])
    N = jboxes.shape[0]
    dists = cdist(jboxes, jboxes)

    dists_sorted = []
    for r in range(N):
        for c in range(r+1, N):
            heapq.heappush(dists_sorted, (dists[r, c], r, c))

    circuits_ids = np.arange(N)
    for _ in range(num_iters):
        _, r, c = heapq.heappop(dists_sorted)
        if circuits_ids[r] == circuits_ids[c]:
            continue
        low_id = min(circuits_ids[r], circuits_ids[c])
        high_id = max(circuits_ids[r], circuits_ids[c])
        circuits_ids[circuits_ids == high_id] = low_id
    csizes = Counter()
    for id in circuits_ids:
        csizes[id] += 1
    csizes = np.sort([csizes[k] for k in csizes.keys()])[::-1]

    return csizes[0] * csizes[1] * csizes[2]

# %% --------------------------------------------------
res_example = part1(data_example[:], 10)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:], 1000)
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
data_example = parse_input(puzzle.examples[-1].input_data)

# %% --------------------------------------------------
def part2(data):
    jboxes = np.array([[float(c) for c in line.split(',')] for line in data])
    N = jboxes.shape[0]
    dists = cdist(jboxes, jboxes)

    dists_sorted = []
    for r in range(N):
        for c in range(r+1, N):
            heapq.heappush(dists_sorted, (dists[r, c], r, c))

    circuits_ids = np.arange(N)
    num_circuits = N
    wall_dist = 0
    while True:
        _, r, c = heapq.heappop(dists_sorted)
        if circuits_ids[r] == circuits_ids[c]:
            continue
        low_id = min(circuits_ids[r], circuits_ids[c])
        high_id = max(circuits_ids[r], circuits_ids[c])
        circuits_ids[circuits_ids == high_id] = low_id
        num_circuits -= 1
        if num_circuits == 1:
            wall_dist = int(jboxes[r, 0] * jboxes[c, 0])
            break
        
    return wall_dist

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
