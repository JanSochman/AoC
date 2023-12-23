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
from einops import rearrange
import networkx as nx

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 20
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

example1 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)


# %% --------------------------------------------------
def hash_state(modules):
    hash_str = ''
    for m in modules.values():
        if m['type'] == 'f':
            hash_str += str(m['state'])
        if m['type'] == 'c':
            hash_str += "".join([str(val) for val in m['memory'].values()])
    return hash_str


def part1(data):
    # read the graph
    modules = {}    # (type, outputs, params)
    for L in data:
        source, targets = L.split(' -> ')
        targets = targets.split(', ')
        sname = source.replace('%', '').replace('&', '')
        if source == "broadcaster":
            modules['broadcaster'] = {'type': 'b', 'targets': targets}
        elif source[0] == '%':
            modules[sname] = {'type': 'f', 'targets': targets, 'state': 0}
        elif source[0] == '&':
            modules[sname] = {'type': 'c', 'targets': targets, 'memory': {}}

    # find output modules
    m_names = list(modules.keys())
    for m in m_names:
        params = modules[m]
        for t in params['targets']:
            if t not in modules:
                modules[t] = {'type': 'o', 'targets': []}

    # find inputs to conjunction modules
    for m, params in modules.items():
        for t in params['targets']:
            if modules[t]['type'] == 'c':
                modules[t]['memory'][m] = 0

    print(modules)

    state_history = []
    low_history = []
    high_history = []
    
    pulses = deque()

    for iter in range(100000):
        state = hash_state(modules)
        if state in state_history:
            print(f'FOUND THE CYCLE of length {len(state_history)}')
            break
        state_history.append(state)

        pulse_sums = [0, 0]
        # print('--------------------')
        # push the button
        pulses.append(('button', 'broadcaster', 0))   # source, target, low pulse
        
        while pulses:
            source, target, p_strength = pulses.popleft()
            pulse_sums[p_strength] += 1

            m = modules[target]
            if m['type'] == 'b':
                for t in m['targets']:
                    pulses.append((target, t, p_strength))
                    
            if m['type'] == 'f':
                if p_strength == 1:
                    continue
                for t in m['targets']:
                    pulses.append((target, t, 1 - m['state']))
                m['state'] = 1 - m['state']
                
            if m['type'] == 'c':
                m['memory'][source] = p_strength
                out = int(sum([1 for p in m['memory'].values() if p == 0]) > 0)
                for t in m['targets']:
                    pulses.append((target, t, out))
                    
            if m['type'] == 'o':
                if p_strength == 0:
                    print(f'RECEIVED')
                    print(f"number of pushes: {iter+1}")
                    return iter + 1
                    
        low_history.append(pulse_sums[0])
        high_history.append(pulse_sums[1])

    full = 1000 // len(state_history)
    part = 1000 % len(state_history)
    total_low = full * sum(low_history) + part * sum(low_history[:part])
    total_high = full * sum(high_history) + part * sum(high_history[:part])

    return total_low * total_high

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
def draw_graph(modules):
    module_idxs = {}
    idx = 0
    for m in modules:
        module_idxs[m] = idx
        idx += 1
        
    G = nx.DiGraph()
    colors = []
    for m in modules:
        colors.append({'b': 'lightblue', 'f': 'lightgreen', 'c': 'magenta', 'o': 'red'}[modules[m]['type']])
        G.add_node(m)

    for m in modules:
        for t in modules[m]['targets']:
            G.add_edge(m, t)
       
    plt.figure(figsize=(20, 20))
    nx.draw(G, with_labels=True, node_color=colors)

    return

# %% --------------------------------------------------
def part2(data):
    # read the graph
    modules = {}    # (type, outputs, params)
    for L in data:
        source, targets = L.split(' -> ')
        targets = targets.split(', ')
        sname = source.replace('%', '').replace('&', '')
        if source == "broadcaster":
            modules['broadcaster'] = {'type': 'b', 'targets': targets}
        elif source[0] == '%':
            modules[sname] = {'type': 'f', 'targets': targets, 'state': 0}
        elif source[0] == '&':
            modules[sname] = {'type': 'c', 'targets': targets, 'memory': {}}

    # find output modules
    m_names = list(modules.keys())
    for m in m_names:
        params = modules[m]
        for t in params['targets']:
            if t not in modules:
                modules[t] = {'type': 'o', 'targets': []}

    # *** I used this to get the understanding of the automata mechanism ***
    # draw_graph(modules)

    # find inputs to conjunction modules
    for m, params in modules.items():
        for t in params['targets']:
            if modules[t]['type'] == 'c':
                modules[t]['memory'][m] = 0

    # print(modules)

    pulses = deque()

    # for testing the last & module inputs
    nc_inputs = {}
    for inp in modules['nc']['memory']:
        nc_inputs[inp] = []

    steps = 0
    for iter in range(200000):
        # push the button
        pulses.append(('button', 'broadcaster', 0))   # source, target, low pulse
        steps += 1
        
        while pulses:
            source, current, p_strength = pulses.popleft()

            m = modules[current]
            if m['type'] == 'b':
                for t in m['targets']:
                    pulses.append((current, t, p_strength))
                    
            if m['type'] == 'f':
                if p_strength == 1:
                    continue
                for t in m['targets']:
                    pulses.append((current, t, 1 - m['state']))
                m['state'] = 1 - m['state']
                
            if m['type'] == 'c':
                m['memory'][source] = p_strength
                out = int(sum([1 for p in m['memory'].values() if p == 0]) > 0)
                for t in m['targets']:
                    pulses.append((current, t, out))
                if current == 'nc':
                    nc_inputs[source].append((steps, p_strength))
                    
            if m['type'] == 'o':
                if p_strength == 0:
                    print(f'RECEIVED')
                    print(f"number of pushes: {iter+1}")
                    return iter + 1

        # collect memory states of the final & module (named 'nc' in my case)
        for inp in modules['nc']['memory']:
            nc_inputs[inp].append((steps, modules['nc']['memory'][inp]))
                    
    return nc_inputs


# %% --------------------------------------------------
# res_example = part2(data_example[:])
# print(res_example)

# %% --------------------------------------------------
nc_inputs = part2(data_full[:])

# %% --------------------------------------------------
starts = []
period = []
for idx, con in enumerate(nc_inputs):
    inps = nc_inputs[con]
    times = np.array([val[0] for val in nc_inputs[con]])
    pulses = np.array([val[1] for val in nc_inputs[con]])
    on_idxs = np.where(pulses == 1)[0]
    period.append(times[on_idxs[1]] - times[on_idxs[0]])
    
print(f"P2 solution: {math.lcm(*period)}")

