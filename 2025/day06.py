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
puzzle_day = 6
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
from operator import mul, add

def part1(data):
    matrix = [L.split() for L in data]
    matrix = list(map(list, zip(*matrix)))
    ops = {'+': add, '*': mul}
    check_sum = 0
    for r in matrix:
        res = int(r[0])
        op = ops[r[-1]]
        for v in r[1:-1]:
            res = op(res, int(v))
        check_sum += res
    
    return check_sum

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
    matrix = [list(L) for L in data]
    matrix = ["".join(r) for r in list(map(list, zip(*matrix)))]
    
    ops = {'+': add, '*': mul}

    check_sum = 0
    val = int(matrix[0][:-1])
    change_operator = True
    for r in matrix:
        if len(r.strip()) == 0:
            change_operator = True
            check_sum += val
            continue

        if change_operator:
            op = ops[r[-1]]
            val = int(r[:-1])
            change_operator = False
            continue
        
        val = op(val, int(r))
    check_sum += val
        
    return check_sum

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
