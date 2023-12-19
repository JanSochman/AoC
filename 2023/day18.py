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
from skimage.morphology import flood_fill
import cv2
from shapely.geometry import Polygon

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 18
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1_floodfill(data, ffseed):
    row, col = (0, 0)
    edges = []
    for L in data:
        dir, meters, color = L.split()
        meters = int(meters)
        color = color[1:-1]
        new_r = row + {'U':-1, 'R':0, 'D':1, 'L':0}[dir] * meters
        new_c = col + {'U':0, 'R':1, 'D':0, 'L':-1}[dir] * meters
        edges.append((min(row, new_r), min(col, new_c), max(row, new_r), max(col, new_c), color))
        row = new_r
        col = new_c
        
    min_row = min([e[0] for e in edges])
    min_col = min([e[2] for e in edges])
    edges = [(e[0]-min_row, e[1]-min_col, e[2]-min_row, e[3]-min_col, e[4]) for e in edges]
    max_row = max([e[2] for e in edges])
    max_col = max([e[3] for e in edges])
    
    # print(edges)
    grid = np.zeros((max_row+1, max_col+1))
    for e in edges:
        grid[e[0]:e[2]+1, e[1]:e[3]+1] = 1
        
    grid = flood_fill(grid, ffseed, 1)
    area = grid.sum()
            
    return grid, area

# %% --------------------------------------------------
def part1(data):
    row, col = (0, 0)
    edges = []
    Edge = namedtuple('Edge', ['r1', 'c1', 'r2', 'c2', 'horiz'])
    for L in data:
        dir, meters, _ = L.split()
        meters = int(meters)
        new_r = row + {'U':-1, 'R':0, 'D':1, 'L':0}[dir] * meters
        new_c = col + {'U':0, 'R':1, 'D':0, 'L':-1}[dir] * meters
        edges.append(Edge(r1=min(row, new_r), c1=min(col, new_c), r2=max(row, new_r), c2=max(col, new_c), horiz=row==new_r))
        row = new_r
        col = new_c
        
    min_row = min([e.r1 for e in edges])
    min_col = min([e.c1 for e in edges])
    edges = [Edge(e.r1-min_row, e.c1-min_col, e.r2-min_row, e.c2-min_col, e.horiz) for e in edges]
    max_row = max([e.r2 for e in edges])
    
    area = 0
    for r in range(max_row+1):
        r_edges = [e for e in edges if e.r1 <= r and e.r2 >= r]
        r_edges.sort(key=lambda e: e.c2)
        r_edges.sort(key=lambda e: e.c1)

        isin = False
        row_sum = 0
        for idx in range(len(r_edges)):
            e = r_edges[idx]
            if e.horiz:    # horizontal
                row_sum += e.c2 - e.c1 - 1
                prev_c = e.c2 - 1
                if (r_edges[idx-1].r1 == r and r_edges[idx+1].r2 == r) or (r_edges[idx-1].r2 == r and r_edges[idx+1].r1 == r):
                    isin = not isin
                continue
            else:               # vertical
                if not isin:
                    row_sum += 1
                else:
                    row_sum += e.c1 - prev_c
                prev_c = e.c1
                isin = not isin
        area += row_sum

    return area

# %% --------------------------------------------------
# res_example = part1_floodfill(data_example[:], (1, 1))
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
def single_line(r, edges):
    r_edges = [e for e in edges if e.r1 <= r and e.r2 >= r]
    r_edges.sort(key=lambda e: e.c2)
    r_edges.sort(key=lambda e: e.c1)

    isin = False
    row_sum = 0
    for idx in range(len(r_edges)):
        e = r_edges[idx]
        if e.horiz:    # horizontal
            row_sum += e.c2 - e.c1 - 1
            prev_c = e.c2 - 1
            if (r_edges[idx-1].r1 == r and r_edges[idx+1].r2 == r) or (r_edges[idx-1].r2 == r and r_edges[idx+1].r1 == r):
                isin = not isin
            continue
        else:               # vertical
            if not isin:
                row_sum += 1
            else:
                row_sum += e.c1 - prev_c
            prev_c = e.c1
            isin = not isin
    return row_sum


def part2(data):
    row, col = (0, 0)
    edges = []
    Edge = namedtuple('Edge', ['r1', 'c1', 'r2', 'c2', 'horiz'])
    for L in data:
        _, _, color = L.split()
        meters = int(color[2:7], 16)
        dir = int(color[7])
        new_r = row + {3:-1, 0:0, 1:1, 2:0}[dir] * meters
        new_c = col + {3:0, 0:1, 1:0, 2:-1}[dir] * meters
        edges.append(Edge(r1=min(row, new_r), c1=min(col, new_c), r2=max(row, new_r), c2=max(col, new_c), horiz=row==new_r))
        row = new_r
        col = new_c
        
    min_row = min([e.r1 for e in edges])
    min_col = min([e.c1 for e in edges])
    edges = [Edge(e.r1-min_row, e.c1-min_col, e.r2-min_row, e.c2-min_col, e.horiz) for e in edges]
    
    rows = set()
    for e in edges:
        rows.add(e.r1)
        rows.add(e.r2)
    rows = sorted(list(rows))
    N = len(rows)
    
    area = 0
    for idx, r in enumerate(rows):
        area += single_line(r, edges)
        if idx < N - 1 and rows[idx+1] - r > 1:
            area += single_line(r+1, edges) * (rows[idx+1] - r - 1)

    return area


# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)
# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
