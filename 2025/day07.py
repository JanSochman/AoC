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
puzzle_day = 7
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    beams = {data[0].find('S')}
    num_splits = 0
    for L in data[1:]:
        new_beams = set()
        for b in beams:
            if L[b] == '^':
                new_beams.add(b+1)
                new_beams.add(b-1)
                num_splits += 1
            else:
                new_beams.add(b)
        beams = new_beams
            
    return num_splits

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
    beams = Counter([data[0].find('S')])
    for L in data[1:]:
        new_beams = Counter()
        for b in beams:
            if L[b] == '^':
                new_beams[b+1] += beams[b]
                new_beams[b-1] += beams[b]
            else:
                new_beams[b] += beams[b]
        beams = new_beams
        
    timelines = beams.total()
            
    return timelines

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
