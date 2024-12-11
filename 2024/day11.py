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
puzzle_day = 11
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """125 17"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data, num_blinks):
    stones = Counter([s for s in data[0].split()])

    for _ in range(num_blinks):
        new_stones = Counter()
        for s, n in stones.items():
            if s == '0':
                new_stones['1'] += n
            elif len(s) > 1:
                if len(s) % 2 == 1:
                    new_stones[str(int(s) * 2024)] += n
                else:
                    new_stones[s[:len(s)//2].lstrip('0') or '0'] += n
                    new_stones[s[len(s)//2:].lstrip('0') or '0'] += n
            else:
                new_stones[str(int(s) * 2024)] += n
        stones = new_stones

    return sum(stones.values())

# %% --------------------------------------------------
res_example = part1(data_example[:], 25)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:], 25)
print(res_full)

res_full = part1(data_full[:], 75)
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
# example2 = example1

# data_example = parse_input(example2)

# # %% --------------------------------------------------
# def part2(data):
#     pass

# # %% --------------------------------------------------
# res_example = part2(data_example[:])
# print(res_example)

# # %% --------------------------------------------------
# res_full = part2(data_full[:])
# print(res_full)

# # %% --------------------------------------------------
