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
puzzle_day = 4
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    grid = defaultdict(lambda: '.')
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            grid[r * 1j + c] = char
            
    dirs = [dr * 1j + dc for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
    accessible = 0
    for r in range(len(data)):
        for c in range(len(data[0])):
            pos = r * 1j + c
            if grid[pos] == '.':
                continue
            accessible += sum([grid[pos + d] == '@' for d in dirs]) < 4
    
    return accessible

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
data_example = parse_input(puzzle.examples[-1].input_data)

# %% --------------------------------------------------
def part2(data):
    grid = defaultdict(lambda: '.')
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            grid[r * 1j + c] = char
            
    dirs = [dr * 1j + dc for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]

    total_accessible = 0
    while True:
        accessible = 0
        for r in range(len(data)):
            for c in range(len(data[0])):
                pos = r * 1j + c
                if grid[pos] == '.':
                    continue
                is_acc = sum([grid[pos + d] == '@' for d in dirs]) < 4
                accessible += is_acc
                if is_acc:
                    grid[pos] = '.'
        if not accessible:
            break
        total_accessible += accessible
    
    return total_accessible

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
