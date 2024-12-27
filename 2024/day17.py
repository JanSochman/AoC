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
puzzle_day = 17
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    regA = int(data[0][12:])
    regB = int(data[1][12:])
    regC = int(data[2][12:])
    instructions = [int(i) for i in data[4][9:].split(',')]
    
    idx = 0
    out = ''
    max_len = len(instructions)
    while idx < max_len:
        i = instructions[idx]
        o = instructions[idx + 1]
        o_combo = o
        if o == 4:
            o_combo = regA
        elif o == 5:
            o_combo = regB
        elif o == 6:
            o_combo = regC
        # print(f"{regA=}, {regB=}, {regC=}, {i=}, {o=}, {o_combo=}, {idx=}")
        match i:
            case 0:     # adv (division)
                regA = regA >> o_combo
            case 1:     # bxl (bitwise XOR)
                regB = regB ^ o
            case 2:     # bst (modulo)
                regB = o_combo % 8
            case 3:     # jnz (jump)
                if regA != 0:
                    idx = o * 2
                    continue
            case 4:     # bxc (bitwise XOR)
                regB = regB ^ regC
            case 5:     # out
                out += f',{int(o_combo % 8)}'
            case 6:     # bdv
                regB = regA >> o_combo
            case 7:     # cdv
                regC = regA >> o_combo

        idx += 2
        
    return out[1:]


# %% --------------------------------------------------
res_example = part1(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full[:])  # 92440 too high
print(res_full)

# %% --------------------------------------------------
# ========== PART 2 ==========
example2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

data_example = parse_input(example2)

# %% --------------------------------------------------
def part2(data):
    regA = 'X'
    regB = data[1][12:]
    regC = data[2][12:]
    instructions = [int(i) for i in data[4][9:].split(',')]
    
    idx = 0
    out_idx = 0
    out = ''
    max_len = len(instructions)
    while out_idx < max_len:
        i = instructions[idx]
        o = str(instructions[idx + 1])
        o_combo = o
        if o == '4':
            o_combo = regA
        elif o == '5':
            o_combo = regB
        elif o == '6':
            o_combo = regC
        match i:
            case 0:     # adv (division)
                regA = f'({regA}) >> ({o_combo})'
            case 1:     # bxl (bitwise XOR)
                regB = f'({regB}) ^ {o}'
            case 2:     # bst (modulo)
                regB = f'({o_combo}) % 8'
            case 3:     # jnz (jump)
                if regA != 0:
                    idx = int(o) * 2
                    continue
            case 4:     # bxc (bitwise XOR)
                regB = f'({regB}) ^ ({regC})'
            case 5:     # out
                out += f'({o_combo}) % 8 == {instructions[out_idx]}\n'
                out_idx += 1
            case 6:     # bdv
                regB = f'({regA}) >> ({o_combo})'
            case 7:     # cdv
                regC = f'({regA}) >> ({o_combo})'

        idx += 2
        
    eqs = out.strip().split('\n')
    neqs = len(eqs)
    for i in range(neqs):
        sstring = '\(X\)'
        for j in range(i):      # full
            sstring = '\(' + sstring + ' \>\> \(3\)\)'
        m = re.search(sstring, eqs[i])
        if not m:
            continue
        n = eqs[i][m.span()[0]: m.span()[1]].count('3')
        eqs[i] = re.sub(sstring, f'(X >> {n * 3})', eqs[i])
        
    return eqs
    

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:]) 
print(res_full)

# %% --------------------------------------------------
# solution of the part 2 example
# example program regA (X) requirements:
# '(X >> 3) % 8 == 0',
# '(X >> 6) % 8 == 3',
# '(X >> 9) % 8 == 5',
# '(X >> 12) % 8 == 4',
# '(X >> 15) % 8 == 3',
# '(X >> 18) % 8 == 0'
# The example program outputs for every 3 bits in regA their modulo 8 result:
#   n = # of three-bits parts in regA (zero padded)
#   (regA >> (n-i-1) * 3) % 8 == output[i]
instructions = [int(i) for i in data_example[4][9:].split(',')]
bstring = ''
for i in instructions[::-1]:
    bstring += format(i, '#05b')[2:]
bstring += '000'
print(bstring)
print(int(bstring, base=2))

# %% --------------------------------------------------
# solution to the part 2 full data
# full data program requirements:
# '(((((X >> 0) % 8) ^ 5) ^ ((X >> 0) >> (((X >> 0) % 8) ^ 5))) ^ 6) % 8 == 2',
# '(((((X >> 3) % 8) ^ 5) ^ ((X >> 3) >> (((X >> 3) % 8) ^ 5))) ^ 6) % 8 == 4',
# '(((((X >> 6) % 8) ^ 5) ^ ((X >> 6) >> (((X >> 6) % 8) ^ 5))) ^ 6) % 8 == 1',
# '(((((X >> 9) % 8) ^ 5) ^ ((X >> 9) >> (((X >> 9) % 8) ^ 5))) ^ 6) % 8 == 5',
# '(((((X >> 12) % 8) ^ 5) ^ ((X >> 12) >> (((X >> 12) % 8) ^ 5))) ^ 6) % 8 == 7',
# '(((((X >> 15) % 8) ^ 5) ^ ((X >> 15) >> (((X >> 15) % 8) ^ 5))) ^ 6) % 8 == 5',
# '(((((X >> 18) % 8) ^ 5) ^ ((X >> 18) >> (((X >> 18) % 8) ^ 5))) ^ 6) % 8 == 0',
# '(((((X >> 21) % 8) ^ 5) ^ ((X >> 21) >> (((X >> 21) % 8) ^ 5))) ^ 6) % 8 == 3',
# '(((((X >> 24) % 8) ^ 5) ^ ((X >> 24) >> (((X >> 24) % 8) ^ 5))) ^ 6) % 8 == 4',
# '(((((X >> 27) % 8) ^ 5) ^ ((X >> 27) >> (((X >> 27) % 8) ^ 5))) ^ 6) % 8 == 0',
# '(((((X >> 30) % 8) ^ 5) ^ ((X >> 30) >> (((X >> 30) % 8) ^ 5))) ^ 6) % 8 == 1',
# '(((((X >> 33) % 8) ^ 5) ^ ((X >> 33) >> (((X >> 33) % 8) ^ 5))) ^ 6) % 8 == 6',
# '(((((X >> 36) % 8) ^ 5) ^ ((X >> 36) >> (((X >> 36) % 8) ^ 5))) ^ 6) % 8 == 5',
# '(((((X >> 39) % 8) ^ 5) ^ ((X >> 39) >> (((X >> 39) % 8) ^ 5))) ^ 6) % 8 == 5',
# '(((((X >> 42) % 8) ^ 5) ^ ((X >> 42) >> (((X >> 42) % 8) ^ 5))) ^ 6) % 8 == 3',
# '(((((X >> 45) % 8) ^ 5) ^ ((X >> 45) >> (((X >> 45) % 8) ^ 5))) ^ 6) % 8 == 0'

conditions = res_full
numbers = []
valid_numbers = []
for x in range(8):
    X = x << (15 * 3)
    if eval(conditions[-1]):
        numbers.append((14, X))
while numbers:
    idx, n = numbers.pop()
    for x in range(8):
        X = n + (x << (3 * idx))
        if eval(conditions[idx-16]):
            if idx == 0:
                valid_numbers.append(X)
            else:
                numbers.append((idx-1, X))

X = min(valid_numbers)
# test if it fullfills all the conditions
[eval(conditions[i]) for i in range(len(conditions))]
print(X)