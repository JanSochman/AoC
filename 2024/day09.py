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
puzzle_day = 9
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """2333133121414131402"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    data = data[0]
    files = [int(f) for f in list(data[0::2])]
    spaces = [int(s) for s in list(data[1::2])]
    
    fwd_pos = 0
    f_idx = 0
    s_idx = 0
    checksum = 0
    f_bkw_idx = len(files) - 1
    while True:
        # process the file
        checksum += f_idx * (files[f_idx] * fwd_pos + sum(range(files[f_idx])))
        fwd_pos += files[f_idx]
        f_idx += 1
        
        if s_idx >= f_bkw_idx:
            break

        # fill the space
        while spaces[s_idx] > 0:
            num = min(spaces[s_idx], files[f_bkw_idx])
            checksum += f_bkw_idx * (num * fwd_pos + sum(range(num)))
            fwd_pos += num
            files[f_bkw_idx] -= num
            if files[f_bkw_idx] == 0:
                f_bkw_idx -= 1
            spaces[s_idx] -= num
        s_idx += 1

    return checksum

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
    data = data[0]
    files = [int(f) for f in list(data[0::2])]
    spaces = [int(s) for s in list(data[1::2])]
    spaces.append(0)    # for easier loops
    
    n_files = len(files)

    f_pos = []
    s_pos = []
    cur_pos = 0
    for f_idx in range(n_files):
        f_pos.append(cur_pos)
        s_pos.append(cur_pos + files[f_idx])
        cur_pos += files[f_idx] + spaces[f_idx]

    checksum = 0
    for f_idx in range(n_files-1, -1, -1):
        cur_pos = f_pos[f_idx]
        for s_idx in range(f_idx):
            if spaces[s_idx] >= files[f_idx]:
                cur_pos = s_pos[s_idx]
                spaces[s_idx] -= files[f_idx]
                s_pos[s_idx] += files[f_idx]
                break
        checksum += f_idx * (files[f_idx] * cur_pos + sum(range(files[f_idx])))

    return checksum

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

