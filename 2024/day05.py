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

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2024
puzzle_day = 5
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------

def part1(data):
    total = 0

    rules = Counter()
    mode = 'rules'
    for L in data:
        if len(L) == 0:
            mode = 'updates'
            continue

        if mode == 'rules':
            rules[L] = 1
            
        if mode == 'updates':
            pages = L.split(',')
            right_order = True
            for p_cur, p_next in zip(pages[:-1], pages[1:]):
                if rules[p_next + '|' + p_cur] > 0:
                    right_order = False
                    break
            if right_order:
                total += int(pages[len(pages) // 2])
    
    return total

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
    total = 0

    rules = Counter()
    mode = 'rules'
    for L in data:
        if len(L) == 0:
            mode = 'updates'
            continue

        if mode == 'rules':
            rules[L] = 1
            
        if mode == 'updates':
            pages = L.split(',')
            right_order = True
            for p_cur, p_next in zip(pages[:-1], pages[1:]):
                if rules[p_next + '|' + p_cur] > 0:
                    right_order = False
                    break

            if not right_order:
                # bubble sort
                swap = True
                while swap:
                    for i in range(len(pages)):
                        swap = False
                        for j in range(i+1, len(pages)):
                            if rules[pages[j] + '|' + pages[i]]:
                                pages[i], pages[j] = pages[j], pages[i]
                                swap = True

                total += int(pages[len(pages) // 2])
    
    return total

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
