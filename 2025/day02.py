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
puzzle_day = 2
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
# not nice, part 2 is better and would work here as well...
def part1(data):
    data = data[0].split(",")
    total = 0
    for L in data:
        low, high = L.split("-")
        high_val = int(high)
        low_val = int(low)
        if len(low) == 1:       # special case
            left = 0
        else:
            left = int(low[:len(low) // 2])
        max_left = int(high[:len(high) // 2])
        if len(high) % 2 == 1:  # special case
            max_left *= 10
        for n in range(left, max_left+1):
            str_val = f"{n}{n}"
            val = int(str_val)
            if val <= high_val and val >= low_val:
                total += val

    res = total
        
    return res

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
    data = data[0].split(",")
    total = 0
    wrong_id_pattern = re.compile(r"^(\d+)\1+$") 

    for L in data:
        left, right = L.split('-')
        Lval = int(left)
        Rval = int(right)
        for n in range(Lval, Rval+1):
            if wrong_id_pattern.match(f"{n}") != None:
                total += n
        
    return total

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
