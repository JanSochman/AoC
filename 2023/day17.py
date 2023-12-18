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
import portion as P
import math
import matplotlib.pyplot as plt

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 17
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def find_min_heat_loss(data, max_budget, forced_steps):
    grid = np.array([[int(c) for c in line] for line in data], dtype=np.int32)
    H, W = grid.shape

    # directions: 0: up, 1: right, 2: down, 3: left

    # r, c, direction, straight budged, accumulate heat loss
    # crucible = deque([(forced_steps, 0, 2, max_budget - forced_steps - 1, grid[1:forced_steps, 0].sum(), [(0,0), (forced_steps,0)]), 
    #                   (0, forced_steps, 1, max_budget - forced_steps - 1, grid[0, 1:forced_steps].sum(), [(0,0), (0,forced_steps)])])
    crucible = deque([(forced_steps, 0, 2, max_budget - forced_steps - 1, grid[1:forced_steps, 0].sum()), 
                      (0, forced_steps, 1, max_budget - forced_steps - 1, grid[0, 1:forced_steps].sum())])

    best_hloss = np.ones((H, W, 4, max_budget)) * np.inf     # four directions, ten budgets
    best_hloss[0, 0, 1, :max_budget] = 0 #grid[0, 1:4].sum()
    best_hloss[0, 0, 2, :max_budget] = 0 #grid[1:4, 0].sum()

    dir2delta_r = {0:-1, 1:0, 2:1, 3:0}
    dir2delta_c = {0:0, 1:1, 2:0, 3:-1}

    min_total_heat = np.inf
    # best_path = []
    while len(crucible):
        cruc = crucible.popleft()
        # r, c, dir, budget, hloss, path = cruc
        r, c, dir, budget, hloss = cruc
        hloss += grid[r, c]

        if hloss >= min_total_heat: # not worth going forward, even more heat would accumulate
            continue

        if r == H-1 and c == W-1:       # bottom right corner reached
            if hloss < min_total_heat:
                min_total_heat = hloss
                # best_path = path[:]
            continue

        # go straight
        if budget > 0 and hloss < best_hloss[r, c, dir, budget]:
            new_r = r + dir2delta_r[dir]
            new_c = c + dir2delta_c[dir]
            if new_c < W and new_c >= 0 and new_r < H and new_r >= 0:
                # crucible.append((new_r, new_c, dir, budget-1, hloss, path + [(new_r, new_c)]))
                crucible.append((new_r, new_c, dir, budget-1, hloss))
                for i in range(budget+1):
                    best_hloss[r, c, dir, i] = min(hloss, best_hloss[r, c, dir, i])

        # go left
        left_dir = (dir - 1) % 4
        if hloss < best_hloss[r, c, left_dir, max_budget-1]:
            new_r = r + dir2delta_r[left_dir] * forced_steps
            new_c = c + dir2delta_c[left_dir] * forced_steps
            if new_c < W and new_c >= 0 and new_r < H and new_r >= 0:
                if r == new_r:
                    c1, c2 = min(c, new_c), max(c, new_c)
                    acc_loss = grid[r, c1+1:c2].sum()
                else:
                    r1, r2 = min(r, new_r), max(r, new_r)
                    acc_loss = grid[r1+1:r2, c].sum()
                crucible.append((new_r, new_c, left_dir, max_budget - forced_steps - 1, hloss + acc_loss))
                # crucible.append((new_r, new_c, left_dir, max_budget - forced_steps - 1, hloss + acc_loss, path + [(new_r, new_c)]))
                for i in range(max_budget):
                    best_hloss[r, c, left_dir, i] = min(hloss, best_hloss[r, c, left_dir, i])

        # go right
        right_dir = (dir + 1) % 4
        if hloss < best_hloss[r, c, right_dir, max_budget - 1]:
            new_r = r + dir2delta_r[right_dir] * forced_steps
            new_c = c + dir2delta_c[right_dir] * forced_steps
            if new_c < W and new_c >= 0 and new_r < H and new_r >= 0:
                if r == new_r:
                    c1, c2 = min(c, new_c), max(c, new_c)
                    acc_loss = grid[r, c1+1:c2].sum()
                else:
                    r1, r2 = min(r, new_r), max(r, new_r)
                    acc_loss = grid[r1+1:r2, c].sum()
                # crucible.append((new_r, new_c, right_dir, max_budget - forced_steps - 1, hloss + acc_loss, path + [(new_r, new_c)]))
                crucible.append((new_r, new_c, right_dir, max_budget - forced_steps - 1, hloss + acc_loss))
                for i in range(max_budget):
                    best_hloss[r, c, right_dir, i] = min(hloss, best_hloss[r, c, right_dir, i])
        
    return min_total_heat


# %% --------------------------------------------------
def part1(data):
    min_total_heat = find_min_heat_loss(data, max_budget=4, forced_steps=1)

    return min_total_heat

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1
# example2 = """111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    return find_min_heat_loss(data, max_budget=10, forced_steps=4)

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
