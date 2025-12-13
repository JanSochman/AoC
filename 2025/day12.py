# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print  # as rprint
import builtins                     # to get access to original print for print to file
# import parse                        # easy string parsing 
from parse import parse
from types import SimpleNamespace as sn
# from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
from itertools import combinations_with_replacement
import re                           # for parsing using regular expressions
from anytree import Node, RenderTree    # for building trees
from scipy import ndimage
from scipy.spatial.distance import cdist
from scipy.optimize import milp, LinearConstraint
import copy
from collections import deque, Counter, defaultdict, namedtuple
import parsy as ps
import portion as P     # data structure and operations for intervals
import math
import matplotlib.pyplot as plt
from skimage.morphology import flood_fill
import cv2
from shapely.geometry import Polygon, Point, MultiPoint
from einops import rearrange
import networkx as nx
import heapq
import time
from tqdm import tqdm

# for regular expressions debugging: https://pythex.org/
# for a good graph visualization use GrapViz (https://dreampuf.github.io/GraphvizOnline) - just export the graph to their format


# %% --------------------------------------------------
def parse_input_lines(input):
    lines = input.split('\n')
    return lines

def parse_input_blocks(input):
    blocks = input.split('\n\n')
    return blocks

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2025
puzzle_day = 12
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input_blocks(puzzle.examples[0].input_data)
data_full = parse_input_blocks(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    n_blocks = len(data)
    shapes = [] 
    regions = []
    for i, block in enumerate(data):
        lines = block.split('\n')
        if i < n_blocks - 1:    # shapes
            shape = np.array([[{'#': 1, '.': 0}[c] for c in line] for line in lines[1:]], dtype=np.int8)
            # rotate, flip and remove duplicates
            fshape = np.fliplr(shape)
            variants = np.unique(np.array([shape,
                        np.rot90(shape), 
                        np.rot90(np.rot90(shape)), 
                        np.rot90(np.rot90(np.rot90(shape))),
                        fshape,
                        np.rot90(fshape), 
                        np.rot90(np.rot90(fshape)), 
                        np.rot90(np.rot90(np.rot90(fshape)))]).reshape(8, -1), axis=0).reshape((-1, 3, 3))

            shapes.append(sn(shape=shape, variants=variants, num_elems=shape.sum()))
        else:                   # regions
            for L in lines:
                sz, quantities = L.split(': ')
                sz = [int(x) for x in sz.split('x')]
                quantities = [int(q) for q in quantities.split()]
                regions.append(sn(sz=sz, quantities=quantities))
                
    num_fit = 0
    for region in tqdm(regions):
        grid = np.zeros(region.sz, dtype=np.int8)
        positions_c, positions_r = np.meshgrid(range(region.sz[1]-2), range(region.sz[0]-2))
        positions_r = positions_r.flatten()
        positions_c = positions_c.flatten()
        max_pos = len(positions_r) - 1
        pos = 0
        feasible_problems = deque([(grid, pos, region.quantities)])
        while feasible_problems:
            grid, pos, quantities = feasible_problems.pop()
            
            if sum(quantities) == 0:    # found a fit
                num_fit += 1
                break
            
            # move to the next position
            pos = pos + 1
            if pos > max_pos:   # outside of the grid
                continue
            r = positions_r[pos]
            c = positions_c[pos]
            
            # check if it is even possible to finish
            free_spots = (1 - grid[r, c:]).sum() + (1 - grid[r+1:, :]).sum()
            needed_spots = sum([quantities[i] * shapes[i].num_elems for i in range(len(quantities))])
            if needed_spots > free_spots:
                continue

            # add nothing at the current positions
            feasible_problems.append((grid.copy(), pos, quantities.copy()))

            # try to place different shape variants
            for i, q in enumerate(quantities):
                grid_bit = grid[r:r+3, c:c+3]
                if q > 0:
                   for s in shapes[i].variants:
                       if (grid_bit + s).max() < 2:
                           new_grid = grid.copy() 
                           new_grid[r:r+3, c:c+3] += s
                           new_quantities = quantities.copy()
                           new_quantities[i] -= 1
                           feasible_problems.append((new_grid, pos, new_quantities))

    return num_fit

# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
t0 = time.time()
res_full = part1(data_full[:])
t1 = time.time()
print(res_full)
print(f'{t1-t0}s')

# %% --------------------------------------------------
# ========== PART 2 ==========
data_example = parse_input_blocks(puzzle.examples[-1].input_data)

# %% --------------------------------------------------
def part2(data):
    for L in data:
        break
            
    return 0

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
t0 = time.time()
res_full = part2(data_full[:])
t1 = time.time()
print(res_full)
print(f'{t1-t0}s')

# %% --------------------------------------------------
problem = Problem()
numpieces = 8
cols = range(numpieces)
rows = range(numpieces)
problem.addVariables(cols, rows)
for col1 in cols:
    for col2 in cols:
        if col1 < col2:
            problem.addConstraint(lambda row1, row2: row1 != row2,
                                  (col1, col2))
solutions = problem.getSolutions()
# %% --------------------------------------------------
