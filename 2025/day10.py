# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print
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

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2025
puzzle_day = 10
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    total_presses = 0
    for L in data:
        i_str, w_str, j_str = re.findall(r"\[(.*)\] (.*) \{(.*)\}", L)[0]
        i_goal = int(i_str.replace('.', '0').replace('#', '1'), 2)
        nbits = len(i_str)
        buttons = [sum([1 << (nbits - int(b) - 1) for b in bits[1:-1].split(',')]) for bits in w_str.split()]
    
        num_states = 1 << nbits
        visited = [False] * num_states
        i_states = []
        heapq.heappush(i_states, (0, 0))
        while i_states:
            num_presses, indicator = heapq.heappop(i_states)
            if indicator == i_goal:
                total_presses += num_presses
                break
            for b in buttons:
                new_indicator = indicator ^ b
                if not visited[new_indicator]:
                    visited[new_indicator] = True
                    heapq.heappush(i_states, (num_presses + 1, new_indicator))
        
    return total_presses

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
data_example = parse_input(puzzle.examples[-1].input_data)

# %% --------------------------------------------------
# Beautiful, but still too slow A* with clever pruning
def part2(data):
    total_presses = 0
    for L in data:
        print(f"processing: {L}")
        _, w_str, j_str = re.findall(r"\[(.*)\] (.*) \{(.*)\}", L)[0]
        required_joltage = [int(j) for j in j_str.split(',')]
        all_buttons = [[int(v) for v in b.split(',')] for b in re.findall(r"\(([\d,]+)\)", w_str)]

        n_slots = len(required_joltage)

        states = []
        # cost (just a heuristic now), num_presses, buttons, remaininig joltage
        num_presses = 0
        heapq.heappush(states, (min(required_joltage), num_presses, copy.deepcopy(all_buttons), required_joltage.copy()))

        iters = 0
        best_num_presses = sum(required_joltage) + 1
        while states:
            cost, num_presses, buttons, remaining_joltage = heapq.heappop(states)
            
            # found it!
            if max(remaining_joltage) == 0:
                # if num_presses < best_num_presses:
                #     best_num_presses = num_presses
                # print(f"new best num_presses: {best_num_presses}")
                # total_presses += best_num_presses
                total_presses += num_presses
                print(f'found: {num_presses}')
                break

            # if num_presses + max(required_joltage) >= best_num_presses:
            #     continue

            iters += 1

            if iters % 1000 == 0:
                print(iters, len(states), remaining_joltage)
            
            # slot to buttons mapping
            slot2buttons = {}
            for i in range(n_slots):
                slot2buttons[i] = []
            for i, b in enumerate(buttons):
                for j in b:
                    slot2buttons[j].append(i)
                    
            # how many buttons can change each slot
            slot_button_cnt = Counter([v for b in buttons for v in b])

            # no buttons to press to satisfy this
            posible = True
            for i in range(n_slots):
                if slot_button_cnt[i] == 0 and remaining_joltage[i] > 0:
                    posible = False
                    break
            if not posible:
                continue

            # try to satisfy every target joltage, slot after slot

            # find slot index with minimal non-negative joltage
            jidxs = np.argsort(remaining_joltage)
            for s_idx in jidxs:
                if remaining_joltage[s_idx] > 0:    # s_idx stays set to this one
                    break

            # a single button to press to satisfy the target_joltage - no combinations needed
            if slot_button_cnt[s_idx] == 1:
                b_idx = slot2buttons[s_idx][0]
                # press the button as many times as possible
                joltage = remaining_joltage.copy()
                for k in buttons[b_idx]:
                    joltage[k] -= remaining_joltage[s_idx]
                # remove the button from allowed buttons
                new_buttons = copy.deepcopy(buttons)
                new_buttons[b_idx] = []
                if min(joltage) >= 0:
                    heapq.heappush(states, (num_presses + remaining_joltage[s_idx] + max(joltage),
                                            num_presses + remaining_joltage[s_idx], 
                                            new_buttons, 
                                            joltage))
            else:   # more buttons - check all combinations
                # for all combinations of buttons pressing to satisfy joltage in slot s_idx
                for c in combinations_with_replacement(range(remaining_joltage[s_idx]+1), slot_button_cnt[s_idx]-1):
                    c = [0] + list(c) + [remaining_joltage[s_idx]]
                    joltage = remaining_joltage.copy()
                    new_buttons = copy.deepcopy(buttons)
                    for j in range(len(c)-1):
                        b_idx = slot2buttons[s_idx][j]
                        v = c[j+1] - c[j]
                        if v > 0:
                            for k in new_buttons[b_idx]:
                                joltage[k] -= v
                            new_buttons[b_idx] = []
                    if min(joltage) >= 0:
                        heapq.heappush(states, (num_presses + remaining_joltage[s_idx] + max(joltage), 
                                                num_presses + remaining_joltage[s_idx], 
                                                new_buttons, 
                                                joltage))
                        
    return total_presses

# %% --------------------------------------------------
# not so nice, but fast and working solution :))
def part2(data):
    total_presses = 0
    for L in data:
        _, w_str, j_str = re.findall(r"\[(.*)\] (.*) \{(.*)\}", L)[0]
        joltage = [float(j) for j in j_str.split(',')]
        buttons = [[int(v) for v in b.split(',')] for b in re.findall(r"\(([\d,]+)\)", w_str)]
        nj = len(joltage)
        nb = len(buttons)

        c = np.ones(nb)
        bu = np.array(joltage)
        bl = np.array(joltage)
        A = np.zeros((nj, nb))
        for i, b in enumerate(buttons):
            for k in b:
                A[k, i] = 1.0
        constraints = LinearConstraint(A, bl, bu)
        integrality = np.ones_like(c)
        res = milp(c, constraints=constraints, integrality=integrality)
        total_presses += np.sum(res.x)

    return int(total_presses)

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
