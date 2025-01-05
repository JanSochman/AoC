# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
# from rich import print
# import parse                        # easy string parsing 
from parse import parse
from types import SimpleNamespace as sn
# from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
from itertools import permutations  # returns all permutations of a list elements
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
puzzle_day = 22
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """1
10
100
2024"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    sum_secrets = 0
    m = 16777216 - 1
    for secret in data:
        secret = int(secret)
        for _ in range(2000):
            secret = ((secret ^ (secret << 6)) & m)
            secret = ((secret ^ (secret >> 5)) & m)
            secret = ((secret ^ (secret << 11)) & m)
        sum_secrets += secret
        
    return sum_secrets

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = """1
2
3
2024"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    m = 16777216 - 1
    num_buyers = len(data)
    prices = np.zeros((num_buyers, 2001), dtype=np.int32)
    for si, secret in enumerate(data):
        secret = int(secret)
        prices[si, 0] = secret % 10
        for i in range(2000):
            secret = ((secret ^ (secret << 6)) & m)
            secret = ((secret ^ (secret >> 5)) & m)
            secret = ((secret ^ (secret << 11)) & m)
            prices[si, i+1] = secret % 10
        
    all_options = Counter()
    dprices = prices[:, 1:] - prices[:, 0:-1]
    for buyer in range(num_buyers):
        buyer_options = Counter()
        for i in range(4, 2001):
            d = tuple(dprices[buyer, i-4:i])
            if len(d) != 4:
                print('wrong len')
            if d not in buyer_options:
                buyer_options[d] = prices[buyer, i]
        # sum the number of bananas for each options
        all_options.update(buyer_options)

    return all_options.most_common(1)[0][1]

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
