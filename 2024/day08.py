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
puzzle_day = 8
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    grid = np.array([[c for c in line] for line in data])
    H, W = grid.shape
    antinodes = np.zeros((H, W), dtype=np.int32)
    frequencies = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    for f in frequencies:
        pos_r, pos_c = np.where(grid == f)
        n = len(pos_r)
        for i in range(n-1):
            for j in range(i+1, n):
                apos_r = pos_r[i] + pos_r[i] - pos_r[j]
                apos_c = pos_c[i] + pos_c[i] - pos_c[j]
                if apos_r >= 0 and apos_c >=0 and apos_r < H and apos_c < W:
                    antinodes[apos_r, apos_c] = 1
                apos_r = pos_r[j] + pos_r[j] - pos_r[i]
                apos_c = pos_c[j] + pos_c[j] - pos_c[i]
                if apos_r >= 0 and apos_c >=0 and apos_r < H and apos_c < W:
                    antinodes[apos_r, apos_c] = 1

    return antinodes.sum()

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
    antinodes = np.zeros((H, W), dtype=np.int32)
    frequencies = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    for f in frequencies:
        pos_r, pos_c = np.where(grid == f)
        n = len(pos_r)
        for i in range(n-1):
            for j in range(i+1, n):
                for k in range(H):
                    apos_r = pos_r[i] + k * (pos_r[i] - pos_r[j])
                    apos_c = pos_c[i] + k * (pos_c[i] - pos_c[j])
                    if apos_r >= 0 and apos_c >=0 and apos_r < H and apos_c < W:
                        antinodes[apos_r, apos_c] = 1
                    else:
                        break
                for k in range(H):
                    apos_r = pos_r[j] + k * (pos_r[j] - pos_r[i])
                    apos_c = pos_c[j] + k * (pos_c[j] - pos_c[i])
                    if apos_r >= 0 and apos_c >=0 and apos_r < H and apos_c < W:
                        antinodes[apos_r, apos_c] = 1
                    else:
                        break

    return antinodes.sum()

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
