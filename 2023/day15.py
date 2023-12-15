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
from collections import deque, Counter, defaultdict
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
puzzle_day = 15
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    data = data[0].replace('\n', '').replace('\r', '')
    parts = data.split(',')
    sum = 0
    for p in parts:
        val = 0
        for c in p:
            val = ((val + ord(c)) * 17) % 256
        sum += val
        
    return sum


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
    def which_box(s):
        val = 0
        for c in s:
            val = ((val + ord(c)) * 17) % 256
        return val
        
    data = data[0].replace('\n', '').replace('\r', '')
    lenses = data.split(',')
    boxes = [{} for _ in range(256)]
    for L in lenses:
        if '-' in L:
            label = L.replace('-', '')
            box = which_box(label)
            if label in boxes[box]:
                del boxes[box][label]
        elif '=' in L:
            label, focal_lenght = L.split('=')
            box = which_box(label)
            boxes[box][label] = int(focal_lenght)
        else:
            print('wrong input')
            
    power = 0
    for b in range(256):
        for slot, label in enumerate(boxes[b]):
            power += (b + 1) * (slot + 1) * boxes[b][label]
        
    return power

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
