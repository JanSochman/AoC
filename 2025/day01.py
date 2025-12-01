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
puzzle_day = 1
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    nums = [50]
    for L in data:
        if L[0] == 'L':
            nums.append(-1 * int(L[1:]))
        else:
            nums.append(int(L[1:]))
    
    cumsum = np.cumsum(nums) % 100
    res = np.sum(cumsum == 0)
        
    return res

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
    nums = [50]
    for L in data:
        if L[0] == 'L':
            nums.append(-1 * int(L[1:]))
        else:
            nums.append(int(L[1:]))
    
    num_zeros = 0
    cumsum = np.cumsum(nums)
    n = nums[0]
    for i in range(1, len(cumsum)):
        a = np.sign(nums[i])
        while n != cumsum[i]:
            if n % 100 == 0:
                num_zeros += 1
            n += a
                
    return num_zeros

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
