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
puzzle_day = 14
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data, H, W, num_steps = 100):
    robots = []
    for L in data:
        r = re.search(r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", L)
        robots.append((int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4))))

    num_robots = np.zeros((H, W), dtype=np.int32)
    for (pc, pr, vc, vr) in robots:
        new_pc = (pc + num_steps * vc) % W
        new_pr = (pr + num_steps * vr) % H
        num_robots[new_pr, new_pc] += 1
        
    safety_factor = num_robots[:H//2, :W//2].sum() * \
                    num_robots[H//2+1:, :W//2].sum() * \
                    num_robots[:H//2, W//2+1:].sum() * \
                    num_robots[H//2+1:, W//2+1:].sum()
                    
    plt.imshow(num_robots)

    return safety_factor


# %% --------------------------------------------------
res_example = part1(data_example[:], H=7, W=11)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:], H=103, W=101)
print(res_full)

# %% --------------------------------------------------
res_full = part1(data_full[:], H=103, W=101, num_steps=6512)
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1

data_example = parse_input(example2)

# %% --------------------------------------------------
from imageio import imwrite

def part2(data, H, W):
    robots = []
    for L in data:
        r = re.search(r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", L)
        robots.append((int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4))))

    max_num = []
    for num_steps in range(0, 10000):
        num_robots = np.zeros((H, W))
        for (pc, pr, vc, vr) in robots:
            new_pc = (pc + num_steps * vc) % W
            new_pr = (pr + num_steps * vr) % H
            num_robots[new_pr, new_pc] += 1
        max_num.append(num_robots.max())

    ee_idx = np.where(np.array(max_num) == 1)[0][0]

    return ee_idx

# %% --------------------------------------------------
# res_example = part2(data_example[:])
# print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:], H=103, W=101)
print(res_full)
part1(data_full[:], H=103, W=101, num_steps=res_full)

# %% --------------------------------------------------
