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
puzzle_day = 13
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    total_tokens = 0

    for row in range(0, len(data)):
        if not data[row]:
            continue

        r = re.search(r"A: X\+(\d+).*Y\+(\d+)", data[row])
        if r is not None:
            Adx = int(r.group(1))
            Ady = int(r.group(2))
            continue

        r = re.search(r"B: X\+(\d+).*Y\+(\d+)", data[row])
        if r is not None:
            Bdx = int(r.group(1))
            Bdy = int(r.group(2))
            continue

        r = re.search(r"X=(\d+).*Y=(\d+)", data[row])
        if r is not None:
            px = int(r.group(1))
            py = int(r.group(2))
            
            # simple test first
            if (Adx * 100 + Bdx * 100 < px) or (Ady * 100 + Bdy * 100 < py):
                continue

            min_tokens = 1e20
            for a in range(101):
                pAx = a * Adx
                pAy = a * Ady
                if pAx > px or pAy > py:
                    continue
                if (px - pAx) % Bdx or (py - pAy) % Bdy:
                    continue
                bx = (px - pAx) // Bdx
                by = (py - pAy) // Bdy
                if bx != by:
                    continue
                tokens = a * 3 + bx
                min_tokens = min(tokens, min_tokens)
            
            if min_tokens < 1e20:
                total_tokens += min_tokens

    return total_tokens


# %% --------------------------------------------------
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
def part2(data):
    total_tokens = 0

    for row in range(0, len(data)):
        if not data[row]:
            continue

        r = re.search(r"A: X\+(\d+).*Y\+(\d+)", data[row])
        if r is not None:
            Adx = int(r.group(1))
            Ady = int(r.group(2))
            continue

        r = re.search(r"B: X\+(\d+).*Y\+(\d+)", data[row])
        if r is not None:
            Bdx = int(r.group(1))
            Bdy = int(r.group(2))
            continue

        r = re.search(r"X=(\d+).*Y=(\d+)", data[row])
        if r is not None:
            px = int(r.group(1)) + 10000000000000
            py = int(r.group(2)) + 10000000000000
            
            # close-form solution of the two equations
            a = (px * Bdy - py * Bdx) / (Adx * Bdy - Ady * Bdx)
            b = (py - a * Ady) / Bdy
            
            # test for integer solution
            if a == int(a) and b == int(b):
                total_tokens += a * 3 + b

    return int(total_tokens)

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
