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
from collections import deque, Counter
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
puzzle_day = 8
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    emap = {}
    instructions = data[0].strip()
    position = 'AAA'
    for L in data[2:]:
        start, left, right = re.findall(r"(\w+)", L)
        emap[start] = [left, right]
    there = False
    steps = 0
    while not there:
        for i in instructions:
            if i == 'L':
                position = emap[position][0]
            else:
                position = emap[position][1]
            steps += 1
            if position == 'ZZZ':
                there = True
                break
            
    return steps

# %% --------------------------------------------------
res_example = part1(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full)
print(res_full)

# %% --------------------------------------------------
# PART 2
def part2(data):
    emap = {}
    instructions = data[0].strip()
    positions = [L[:3] for L in data[2:] if L[2] == 'A']
    print(positions)
    N = len(positions)
    for L in data[2:]:
        start, left, right = re.findall(r"(\w+)", L)
        emap[start] = [left, right]
    pos_start = positions[:]
    cycle_lengths = []
    for j in range(N):
        there = False
        steps = 0
        while not there:
            for i in instructions:
                if i == 'L':
                    positions[j] = emap[positions[j]][0]
                else:
                    positions[j] = emap[positions[j]][1]
                steps += 1
                if positions[j][2] == 'Z':
                    there = True
                    cycle_lengths.append(steps)
                    break
    steps = np.lcm.reduce(cycle_lengths)
            
    return steps

# %% --------------------------------------------------
example2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data_example = parse_input(example2)

# %% --------------------------------------------------
res_example = part2(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full)
print(res_full)

# %% --------------------------------------------------
