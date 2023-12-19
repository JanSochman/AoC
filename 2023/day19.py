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
puzzle_day = 19
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)


# %% --------------------------------------------------
def part1(data):
    workflows = {}
    for i, L in enumerate(data):
        if not L:
            parts_idx = i + 1
            break
        wkf, instructions = L[:-1].split('{')
        instructions = instructions.split(',')
        instructions = [p.split(':') for p in instructions]
        workflows[wkf] = instructions
        
    Part = namedtuple('Part', ['x', 'm', 'a', 's'])
    parts = []
    for L in data[parts_idx:]:
        parts.append(eval('Part(' + L[1:-1] + ')'))
    
    total = 0
    for p in parts:
        cur_wkf = 'in'
        accepted = False
        rejected = False
        while not accepted and not rejected:
            instructions = workflows[cur_wkf] 
            for i in instructions: 
                if i[0] == 'A':
                    accepted = True
                    break
                if i[0] == 'R':
                    rejected = True
                    break
                if len(i) == 1:
                    cur_wkf = i[0]
                    break
                if eval('p.' + i[0]):
                    cur_wkf = i[1]
                    if cur_wkf == 'A':
                        accepted = True
                        break
                    if cur_wkf == 'R':
                        rejected = True
                        break
                    break

            if accepted:
                total += p.m + p.x + p.a + p.s
        
    return total

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
def part2(data):
    workflows = {}
    for L in data:
        if not L:
            break
        wkf, instructions = L[:-1].split('{')
        instructions = instructions.split(',')
        instructions = [p.split(':') for p in instructions]
        workflows[wkf] = instructions
        
    # wkf, x, m, a, s
    parts = [['in', [1, 4000], [1, 4000], [1, 4000], [1, 4000]]]
    rat2idx = {'x': 1, 'm': 2, 'a': 3, 's': 4}
    
    total = 0
    while parts:
        p = parts.pop()
        wkf = p[0]

        accepted = False

        instructions = workflows[wkf] 
        for i in instructions: 
            if i[0] == 'A':
                accepted = True
                break
            if i[0] == 'R':
                break
            if len(i) == 1:
                p[0] = i[0]
                parts.append(p)
                break

            # parse the condition
            rating = i[0][0]
            r_idx = rat2idx[rating]
            cond = i[0][1]
            val = int(i[0][2:])

            # tested interval
            p_int = p[r_idx]

            if cond == '>':
                good_int = [max(val+1, p_int[0]), p_int[1]] 
                bad_int = [p_int[0], min(val, p_int[1])] 
            else:
                good_int = [p_int[0], min(val-1, p_int[1])]
                bad_int = [max(val, p_int[0]), p_int[1]]
                
            # not empty
            if good_int[1] >= good_int[0]:
                new_p = p.copy()
                new_p[0] = i[1]
                new_p[r_idx] = good_int[:]
                if i[1] == 'A':
                    total += np.prod([r[1] - r[0] + 1 for r in new_p[1:]])
                elif i[1] != 'R':
                    parts.append(new_p)

            # nothing left
            if bad_int[1] < bad_int[0]:
                break

            # something left to be processed
            p[r_idx] = bad_int[:]

        if accepted:
            total += np.prod([r[1] - r[0] + 1 for r in p[1:]])
        
    return total


# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
