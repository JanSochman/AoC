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
puzzle_day = 4
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def test_line(L):
    return len(re.findall('XMAS', L)) + len(re.findall('SAMX', L))

def part1(data):
    total = 0

    # original data
    for L in data:
        total += test_line(L)

    # data transposed
    data_t = [''.join(list(t)) for t in zip(*data)]
    for L in data_t:
        total += test_line(L)

    # data on diagonals
    max_col = len(data[0])
    max_row = len(data)
    diag_minor = [[] for _ in range(max_row + max_col - 1)]
    diag_major = [[] for _ in range(len(diag_minor))]
    min_diag_major = -max_row + 1
    for x in range(max_col):
        for y in range(max_row):
            diag_minor[x+y].append(data[y][x])
            diag_major[x-y-min_diag_major].append(data[y][x])

    diag_minor = [''.join(d) for d in diag_minor]
    diag_major = [''.join(d) for d in diag_major]

    for L in diag_minor:
        total += test_line(L)
    for L in diag_major:
        total += test_line(L)
    
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
    total = 0
    for r in range(1, len(data)-1):
        for c in range(1, len(data[0])-1):
            if data[r][c] == 'A':
                if ((data[r-1][c-1] == 'M' and data[r+1][c+1] == 'S') or \
                    (data[r-1][c-1] == 'S' and data[r+1][c+1] == 'M')) and \
                   ((data[r-1][c+1] == 'M' and data[r+1][c-1] == 'S') or \
                    (data[r-1][c+1] == 'S' and data[r+1][c-1] == 'M')):
                       total += 1
    
    return total

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
