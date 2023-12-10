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
from collections import deque, Counter, defaultdict
import parsy as ps
import portion as P
import math

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 10
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

example1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
# key: (cur_value, entered_from), values: ((row_delta, col_delta), where_from_coming)
navig = {("F", "S"): ((0, 1), 'W'),
         ("F", "E"): ((1, 0), 'N'),
         ("J", "N"): ((0, -1), 'E'),
         ("J", "W"): ((-1, 0), 'S'),
         ("L", "N"): ((0, 1), 'W'),
         ("L", "E"): ((-1, 0), 'S'),
         ("7", "W"): ((+1, 0), 'N'),
         ("7", "S"): ((0, -1), 'E'),
         ("-", "E"): ((0, -1), 'E'),
         ("-", "W"): ((0, 1), 'W'),
         ("|", "N"): ((1, 0), 'N'),
         ("|", "S"): ((-1, 0), 'S')}

# to disambiguate the S position pipe
start_dir = {'F': ['N', 'W'],
             'J': ['S', 'E'],
             'L': ['S', 'W'],
             '7': ['E', 'N'],
             '-': ['W', 'E'],
             '|': ['N', 'S']}

def part1(data):
    W = len(data[0])
    H = len(data)

    # S position
    s_pos = "".join(data).find('S')
    s_row = s_pos // W
    s_col = s_pos % W
    
    # find what S symbol stands for
    options = []
    if s_row > 0:
        if data[s_row-1][s_col] in ['F', '|', '7']:
            options.append(['J', 'L', '|'])
    if s_row < H-1:
        if data[s_row+1][s_col] in ['J', '|', 'L']:
            options.append(['F', '7', '|'])
    if s_col > 0:
        if data[s_row][s_col-1] in ['L', '-', 'F']:
            options.append(['J', '7', '-'])
    if s_col < W-1:
        if data[s_row][s_col+1] in ['J', '7', '-']:
            options.append(['L', 'F', '-'])
    s_options = set(options[0]) & set(options[1])
    s_symbol = s_options.pop()
    data[s_row] = data[s_row][:s_col] + s_symbol + data[s_row][s_col+1:]

    # possible directions from the start position
    cur_symbol = s_symbol
    wf_dirs = []
    for d in ['S', 'N', 'E', 'W']:
        if (s_symbol, d) in navig:
           wf_dirs.append(d) 
    pos = [s_row, s_col]
    where_from = wf_dirs[0]
    
    # the animal hunt
    steps = 0
    starting = True
    while starting or (pos[0] != s_row or pos[1] != s_col):
        cur_symbol = data[pos[0]][pos[1]]
        pos = [i + j for i, j in zip(pos, navig[(cur_symbol, where_from)][0])]
        where_from = navig[(cur_symbol, where_from)][1]

        steps += 1
        starting = False
        
    steps = steps // 2

    return steps


# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])
print(res_full)

# %% --------------------------------------------------
# PART 2
example2 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

example2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    W = len(data[0])
    H = len(data)

    # S position
    s_pos = "".join(data).find('S')
    s_row = s_pos // W
    s_col = s_pos % W
    
    # find what S symbol stands for
    options = []
    if s_row > 0:
        if data[s_row-1][s_col] in ['F', '|', '7']:
            options.append(['J', 'L', '|'])
    if s_row < H-1:
        if data[s_row+1][s_col] in ['J', '|', 'L']:
            options.append(['F', '7', '|'])
    if s_col > 0:
        if data[s_row][s_col-1] in ['L', '-', 'F']:
            options.append(['J', '7', '-'])
    if s_col < W-1:
        if data[s_row][s_col+1] in ['J', '7', '-']:
            options.append(['L', 'F', '-'])
    s_options = set(options[0]) & set(options[1])
    s_symbol = s_options.pop()
    data[s_row] = data[s_row][:s_col] + s_symbol + data[s_row][s_col+1:]

    # possible directions from the start position
    cur_symbol = s_symbol
    wf_dirs = []
    for d in ['S', 'N', 'E', 'W']:
        if (s_symbol, d) in navig:
           wf_dirs.append(d) 
    pos = [s_row, s_col]
    where_from = wf_dirs[0]
    
    # the animal hunt (single direction only to simplify the code)
    clear_map = np.empty((H, W), dtype='<U1')
    clear_map[:] = '.'
    clear_map[s_row, s_col] = s_symbol

    steps = 0
    starting = True
    while starting or (pos[0] != s_row or pos[1] != s_col):
        cur_symbol = data[pos[0]][pos[1]]
        pos = [i + j for i, j in zip(pos, navig[(cur_symbol, where_from)][0])]
        where_from = navig[(cur_symbol, where_from)][1]
        clear_map[pos[0], pos[1]] = data[pos[0]][pos[1]]

        steps += 1
        starting = False
        
    # compute the area (essentially the scanline fill algorithm)
    # X = np.zeros((H, W), dtype=np.int64)
    area = 0
    for row in range(H):
        isin = False
        prev_c = '|'
        for col in range(W):
            c = clear_map[row, col]
            if (c == '7' and prev_c == 'F') or (c == 'J' and prev_c == 'L'):
                prev_c = c
                continue
            if (c == '7' and prev_c == 'L') or (c == 'J' and prev_c == 'F'):
                prev_c = c
                isin = not isin
                continue
            if c in ['F', 'L', 'J', '7']:
                prev_c = c
                continue
            if c == '|':
                isin = not isin
                prev_c = c
            if c == '.' and isin:
                # X[row, col] = 1
                area += 1

    return area

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
