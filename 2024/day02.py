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
puzzle_day = 2
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    num_safe = 0
    for L in data:
        values = [int(i) for i in L.split(' ')]
        dif = [a - b for a, b in zip(values[1:], values[:-1])]
        inc = dif[0] > 0
        safe = True
        for d in dif:
            if d == 0 or abs(d) > 3 or (d > 0) != inc:
                safe = False
                break
        if safe:
            num_safe += 1

    return num_safe

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
# ugly, but working :)
def is_safe(values):
    dif = [a - b for a, b in zip(values[1:], values[:-1])]
    inc = dif[0] > 0
    safe = True
    for d in dif:
        if d == 0 or abs(d) > 3 or (d > 0) != inc:
            safe = False
            break
    return safe
    
def part2(data):
    num_safe = 0
    for L in data:
        values = [int(i) for i in L.split(' ')]
        safe = False
        for i in range(len(values)):
            if is_safe(values[:i] + values[i+1:]):
                safe = True
                break
        if safe:
            num_safe += 1    

    return num_safe

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
