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
puzzle_day = 16
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

example1 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

# example1 = """##########
# #.......E#
# #.##.#####
# #..#.....#
# ##.#####.#
# #S.......#
# ##########"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    maze = np.array([list(r) for r in data])
    r, c = np.argwhere(maze == 'S')[0]
    maze[r, c] = '.'
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir = 0
    
    visited_h = np.ones((maze.shape[0], maze.shape[1], 4)) * 1e25

    paths = []
    heapq.heappush(paths, (0, r, c, dir))
    while True:
        plen, r, c, dir = heapq.heappop(paths)

        if visited_h[r, c, dir] < plen:
            continue
        visited_h[r, c, dir] = plen

        if maze[r, c] == 'E':
            return plen

        # go straight
        new_r = r + dirs[dir][0]
        new_c =  c + dirs[dir][1]
        if maze[new_r, new_c] in '.E':
            if visited_h[new_r, new_c, dir] > plen + 1:
                heapq.heappush(paths, (plen+1, new_r, new_c, dir))
            
        # turn left
        dir = (dir - 1) % 4
        heapq.heappush(paths, (plen+1000, r, c, dir))
                
        # turn right
        dir = (dir + 2) % 4
        heapq.heappush(paths, (plen+1000, r, c, dir))


# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])  # 92440 too high
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = example1

# example2 = """##########
# #.......E#
# #.##.#####
# #..#.....#
# ##.#####.#
# #S.......#
# ##########"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def heuristic(r, c, dir, end_r, end_c):
    turns_to_end = {0: 1, 1: 2, 2: 2, 3: 1}

    return turns_to_end[dir] * 1000 + (end_r - r) + (end_c - c)


def part2(data):
    maze = np.array([list(r) for r in data])

    start_r, start_c = np.argwhere(maze == 'S')[0]
    maze[start_r, start_c] = '.'
    end_r, end_c = np.argwhere(maze == 'E')[0]

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir = 0
    
    best_len = np.ones((maze.shape[0], maze.shape[1], 4)) * 1e25

    # find the best path
    came_from = {}
    paths = []
    best_path_len = 1e25
    heapq.heappush(paths, (0, start_r, start_c, dir))
    while len(paths) > 0:
        plen, r, c, dir = heapq.heappop(paths)

        if plen + heuristic(r, c, dir, end_r, end_c) > best_path_len:
            continue
        
        if best_len[r, c, dir] < plen:
            continue

        if maze[r, c] == 'E':
            best_path_len = plen
            continue

        # go straight
        new_r = r + dirs[dir][0]
        new_c =  c + dirs[dir][1]
        if maze[new_r, new_c] in '.E':
            if best_len[new_r, new_c, dir] > plen + 1:
                heapq.heappush(paths, (plen+1, new_r, new_c, dir))
                came_from[(new_r, new_c, dir)] = [(r, c, dir)]
                best_len[new_r, new_c, dir] = plen + 1
            if best_len[new_r, new_c, dir] == plen + 1:
                came_from[(new_r, new_c, dir)].append((r, c, dir))
            
        # try to turn left and right
        for new_dir in [(dir - 1) % 4, (dir + 1) % 4]:
            new_r = r + dirs[new_dir][0]
            new_c =  c + dirs[new_dir][1]
            if maze[new_r, new_c] in '.E':
                if best_len[r, c, new_dir] > plen + 1000:
                    heapq.heappush(paths, (plen+1000, r, c, new_dir))
                    came_from[(r, c, new_dir)] = [(r, c, dir)]
                    best_len[r, c, new_dir] = plen + 1000
                if best_len[r, c, new_dir] == plen + 1000:
                    came_from[(r, c, new_dir)].append((r, c, dir))

    print('best path:', best_path_len)
        
    # back-track the paths
    pos = deque([(end_r, end_c, 0), (end_r, end_c, 3)])
    visited = np.zeros((maze.shape[0], maze.shape[1], 4), dtype=np.uint16)
    visited[start_r, start_c, 0] = 1
    iter = 0
    while pos:
        iter += 1
        r, c, d = pos.popleft()
        if visited[r, c, d]:
            continue
        if not (r, c, d) in came_from:
            continue
        visited[r, c, d] = 1
        cf = came_from[(r, c, d)]
        for p in cf:
            pos.append(p)
            
    plt.imshow(visited.max(axis=2))

    return visited.max(axis=2).sum()
    

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:]) 
print(res_full)

# %% --------------------------------------------------
