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
puzzle_day = 19
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
# tried first regular expressions, but I learned quickly about catastrophic backtracking :)
def part1(data):
    towels = data[0].split(', ')
        
    num_matching = 0
    for L in data[2:]:
        spans = [[] for _ in range(len(L))]
        for t in towels:
            for m in re.finditer(t, L):
                spans[m.span(0)[0]].append(m.span(0)[1]-1)

        reachable = [False for _ in range(len(L)+1)]
        reachable[0] = True
        for i in range(len(L)):
            if reachable[i]:
                for s in spans[i]:
                    reachable[s+1] = True
        if reachable[-1]:
            num_matching += 1
            
    return num_matching
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
    towels = data[0].split(', ')
        
    num_ways = 0
    for L in data[2:]:
        spans = [[] for _ in range(len(L))]
        for t in towels:
            regexp = f'(?=({t}))'     # lookahead assertion to detect overlapping matches
            for m in re.finditer(regexp, L):
                spans[m.span(0)[0]].append(m.span(0)[0]+len(t))

        reachable = [0 for _ in range(len(L)+1)]
        reachable[0] = 1
        for i in range(len(L)):
            if reachable[i] > 0:
                for s in spans[i]:
                    reachable[s] += reachable[i]
        num_ways += reachable[len(L)]
            
    return num_ways

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
