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
puzzle_day = 20
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def get_next_neighbor(r, c, racetrack, times):
    H, W = racetrack.shape
    possible_moves = [
        (r+1, c), (r-1, c),     # down, up
        (r, c+1), (r, c-1)      # right, left
    ]
    
    possible_moves = [
        (r, c) for r, c in possible_moves
        if 0 <= r < H and 0 <= c < W        # within grid bounds
        and racetrack[r, c] in '.E'          # new direction
        and times[r, c] == -1
    ] 
    
    return possible_moves[0]

def get_cheats(r, c, racetrack, times):
    H, W = racetrack.shape
    possible_moves = [
        (r+2, c), (r-2, c),     # down, up
        (r, c+2), (r, c-2)      # right, left
    ]
    
    possible_moves = [
        (r_, c_) for r_, c_ in possible_moves
        if 0 <= r_ < H and 0 <= c_ < W        # within grid bounds
        and racetrack[r_, c_] in '.E'          # new direction
        and times[r_, c_] != -1
        and times[r_, c_] > times[r, c] + 2
    ] 
    
    return possible_moves

def part1(data):
    racetrack = np.array([list(r) for r in data])
    times = -1 * np.ones(racetrack.shape, dtype=np.int32)
    start_r, start_c = np.argwhere(racetrack == 'S')[0]
    times[start_r, start_c] = 0
    end_r, end_c = np.argwhere(racetrack == 'E')[0]

    r, c = (start_r, start_c)
    t = 0
    while racetrack[r, c] != 'E':
        times[r, c] = t
        r, c = get_next_neighbor(r, c, racetrack, times)
        t += 1
    times[end_r, end_c] = t
    max_time = t

    num_cheats = [0 for _ in range(max_time)]
    for t in range(max_time):
        r, c = np.argwhere(times == t)[0]
        cheats = get_cheats(r, c, racetrack, times)
        for ch in cheats:
            t2 = times[ch[0], ch[1]]
            num_cheats[t2 - t - 2] += 1

    return sum(num_cheats[100:])

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])  # 92440 too high
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1

data_example = parse_input(example2)

# %% --------------------------------------------------
def get_cheats2(r, c, racetrack, times):
    H, W = racetrack.shape
    possible_moves = []
    max_move = 20
    for dr in range(-max_move, max_move+1):
        cmax = max_move - abs(dr)
        for dc in range(-cmax, cmax+1):
            possible_moves.append((r + dr, c + dc, abs(dr) + abs(dc)))
    
    possible_moves = [
        (r_, c_, steps) for r_, c_, steps in possible_moves
        if 0 <= r_ < H and 0 <= c_ < W        # within grid bounds
        and racetrack[r_, c_] in '.E'          # new direction
        and times[r_, c_] != -1
        and times[r_, c_] > times[r, c] + steps
    ] 
    
    return possible_moves

def part2(data):
    racetrack = np.array([list(r) for r in data])
    times = -1 * np.ones(racetrack.shape, dtype=np.int32)
    start_r, start_c = np.argwhere(racetrack == 'S')[0]
    times[start_r, start_c] = 0
    end_r, end_c = np.argwhere(racetrack == 'E')[0]

    r, c = (start_r, start_c)
    t = 0
    while racetrack[r, c] != 'E':
        times[r, c] = t
        r, c = get_next_neighbor(r, c, racetrack, times)
        t += 1
    times[end_r, end_c] = t
    max_time = t

    num_cheats = [0 for _ in range(max_time)]
    for t in range(max_time):
        r, c = np.argwhere(times == t)[0]
        cheats = get_cheats2(r, c, racetrack, times)
        for ch in cheats:
            t2 = times[ch[0], ch[1]]
            steps = ch[2]
            num_cheats[t2 - t - steps] += 1

    return sum(num_cheats[100:])

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
