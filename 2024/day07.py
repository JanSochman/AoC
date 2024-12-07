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
puzzle_day = 7
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    res = 0
    for L in data:
        total, numbers = L.split(':')
        total = int(total)
        numbers = [int(i) for i in numbers.strip().split(' ')]
        end_pos = len(numbers) - 1
        opts = deque([(0, numbers[0])])
        calibrated = False
        while len(opts) > 0:
            (pos, val) = opts.pop()
            if pos == end_pos and val == total:
                calibrated = True
                break
            
            if val > total or pos == end_pos:
                continue
            
            opts.append((pos+1, val+numbers[pos+1]))
            opts.append((pos+1, val*numbers[pos+1]))
            
        if calibrated:
            res += total

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
    res = 0
    for L in data:
        total, numbers = L.split(':')
        total = int(total)
        numbers = [int(i) for i in numbers.strip().split(' ')]
        end_pos = len(numbers) - 1
        opts = deque([(0, numbers[0]), (1, int(str(numbers[0]) + str(numbers[1])))])
        calibrated = False
        while len(opts) > 0:
            (pos, val) = opts.pop()
            if pos == end_pos and val == total:
                calibrated = True
                break
            
            if val > total or pos == end_pos:
                continue
            
            opts.append((pos+1, val + numbers[pos+1]))
            opts.append((pos+1, val * numbers[pos+1]))
            opts.append((pos+1, int(str(val) + str(numbers[pos+1]))))
            
        if calibrated:
            res += total

    return res

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
