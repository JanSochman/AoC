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

# %% ----------------------------
class AStar(object):
    def __init__(self, max_len=1e25):
        self.max_len = max_len
        
    def get_valid_neighbors(self, state):
        return [], []
        
    def test_end_state(self, state, end_state):
        if state == end_state:
            return True
        else:
            return False
        
    def heuristic(self, state):
        return 0
        
    def find_path(self, init_states, end_state):
        # find the best path
        best_len = {}
        came_from = defaultdict(lambda: None)
        paths = []
        best_path_len = self.max_len
        for s in init_states:
            heapq.heappush(paths, (0, s))
            came_from[s] = []
            best_len[s] = 0

        while paths:
            plen, state = heapq.heappop(paths)

            if plen + self.heuristic(state) > best_path_len:
                continue
            
            if state in best_len.keys() and best_len[state] < plen:
                continue

            if self.test_end_state(state, end_state):
                best_path_len = plen
                break

            neighs, prices = self.get_valid_neighbors(state)
            for n, p in zip(neighs, prices):
                if n not in best_len.keys() or best_len[n] > plen + p:
                    heapq.heappush(paths, (plen+p, n))
                    if n == (0, 0):
                        print(f'coming from {state}, plen={plen+p}')
                    came_from[n] = state
                    best_len[n] = plen + p

        # back-track the paths
        current = end_state
        path_states = []
        while current not in init_states:
            if current is None:
                return []
            path_states.append(current)
            current = came_from[current]
        path_states = path_states[::-1]
            
        return path_states

# %% --------------------------------------------------
class AStar18(AStar):
    def __init__(self, grid, max_len=1e+25):
        super().__init__(max_len)

        self.grid = grid
        self.H, self.W = grid.shape

    def get_valid_neighbors(self, state):
        cur_r = state[0]
        cur_c = state[1]
        
        possible_moves = [
            (cur_r+1, cur_c), (cur_r-1, cur_c),     # down, up
            (cur_r, cur_c+1), (cur_r, cur_c-1)      # right, left
        ]
        
        possible_moves = [
            (r, c) for r, c in possible_moves
            if 0 <= r < self.H and 0 <= c < self.W  # within grid bounds
            and self.grid[r, c] == 0                # not an obstacle
        ] 
        
        prices = [1] * len(possible_moves)
        
        return possible_moves, prices

    
# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2024
puzzle_day = 18
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data, grid_size, num_fallen):
    memory = np.zeros(grid_size)
    falling = []
    for L in data:
        falling.append(tuple([int(i) for i in L.split(',')]))
        
    for i in range(num_fallen):
        memory[falling[i][1], falling[i][0]] = 1
    
    astar = AStar18(memory)
    path = astar.find_path([(0, 0)], (grid_size[0]-1, grid_size[1]-1))
    
    return len(path)


# %% --------------------------------------------------
res_example = part1(data_example[:], (7, 7), 12)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:], (71, 71), 1024)
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1
data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data, grid_size, num_fallen_init):
    memory = np.zeros(grid_size)
    falling = []
    for L in data:
        falling.append(tuple([int(i) for i in L.split(',')]))
        
    for i in range(num_fallen_init):
        memory[falling[i][1], falling[i][0]] = 1
    
    for i in range(num_fallen_init, len(falling)):
        memory[falling[i][1], falling[i][0]] = 1
        astar = AStar18(memory)
        path = astar.find_path([(0, 0)], (grid_size[0]-1, grid_size[1]-1))
        if not path:
            print(f'{falling[i][0]},{falling[i][1]}')
            break
    
    return ''
    

# %% --------------------------------------------------
res_example = part2(data_example[:], (7, 7), 12)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:], (71, 71), 1024)
print(res_full)

# %% --------------------------------------------------
