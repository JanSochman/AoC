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
import copy
from collections import deque
import parsy as ps
import portion as P
import math

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(times, dists):
    num_better = []
    for i in range(len(times)):
        r1, r2 = np.sort(np.roots([1, -times[i], dists[i]]))
        
        better = math.floor(r2) - math.ceil(r1) + 1
        if r1 == math.floor(r1):
            better -= 1
        if r2 == math.ceil(r2):
            better -= 1

        num_better.append(better)

        # original "lazy" version
        # better = 0
        # for t in range(times[i]):
        #    if t * (times[i] - t) > dists[i]:
        #        better += 1 
        # num_better.append(better)

    return np.prod(num_better)

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 6
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

# Time:      7  15   30
# Distance:  9  40  200
times_example = [7, 15, 30]
dists_example = [9, 40, 200]

# Time:        44     89     96     91
# Distance:   277   1136   1890   1768
times_full = [44, 89, 96, 91]
dists_full = [277, 1136, 1890, 1768]

# %% --------------------------------------------------
res_example = part1(times_example, dists_example)
print(res_example)

# %% --------------------------------------------------
res_full = part1(times_full, dists_full)
print(res_full)


# %% --------------------------------------------------
# PART 2
def part2(t, d):
    r1, r2 = np.sort(np.roots([1, -t, d]))
    
    better = math.floor(r2) - math.ceil(r1) + 1
    if r1 == math.floor(r1):
        better -= 1
    if r2 == math.ceil(r2):
        better -= 1

    return better

# %% --------------------------------------------------

# Time:      7  15   30
# Distance:  9  40  200
time_example = 71530
dist_example = 940200

# Time:        44     89     96     91
# Distance:   277   1136   1890   1768
time_full = 44899691
dist_full = 277113618901768

res_example = part2(time_example, dist_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(time_full, dist_full)
print(res_full)


