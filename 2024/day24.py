# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
# from rich import print
# import parse                        # easy string parsing 
from parse import parse
from types import SimpleNamespace as sn
# from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
from itertools import permutations  # returns all permutations of a list elements
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
puzzle_day = 24
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

example1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

example1 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    processin_inputs = True
    inputs = {}
    ops = deque()
    for L in data:
        if not L:
            processin_inputs = False
            continue

        if processin_inputs:
            name, value = L.split(': ')
            inputs[name] = int(value)
        else:
            in_op, output = L.split(' -> ')
            in1, op, in2 = in_op.split(' ')
            ops.append((op, in1, in2, output))
            
    while ops:
        op = ops.popleft()
        if op[1] in inputs and op[2] in inputs:
            match op[0]:
                case 'AND':
                    inputs[op[3]] = inputs[op[1]] & inputs[op[2]]
                case 'OR':
                    inputs[op[3]] = inputs[op[1]] | inputs[op[2]]
                case 'XOR':
                    inputs[op[3]] = inputs[op[1]] ^ inputs[op[2]]
        else:
            ops.append(op)
            
    z_names = sorted([n for n in list(inputs.keys()) if n[0] == 'z'], reverse=True)
    out_val = int(''.join([str(inputs[z]) for z in z_names]), base=2)
        
    return out_val

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
    processin_inputs = True
    input_nodes = set()
    output_nodes = set()
    value_nodes = set()
    carry_nodes = set()
    op_nodes = set()
    edges = []
    for L in data:
        if not L:
            processin_inputs = False
            continue

        if processin_inputs:
            name, _ = L.split(': ')
            input_nodes.add(name)
        else:
            in_op, output = L.split(' -> ')
            in1, op, in2 = in_op.split(' ')
            value_nodes.add(in1)
            value_nodes.add(in2)
            if output[0] == 'z':
                output_nodes.add(output)
            elif op == 'OR':
                carry_nodes.add(output)
            else:
                value_nodes.add(output)
            op_name = op + '_' + in1 + '_' + in2
            op_nodes.add(op_name)
            edges.append((in1, op_name))
            edges.append((in2, op_name))
            edges.append((op_name, output))

    # output the graph into graphviz format
    # we know how the graph for addition looks like, so by visual inspection
    # I have identified these wire swaps. By changing them back I was able to verify
    # that the swap was correct. We also know that there are only 4 swaps, so that
    # helps in limiting the search.
    # I visualized the graph at https://dreampuf.github.io/GraphvizOnline
    tr = {}
    for n in value_nodes:
        tr[n] = n
    for n in carry_nodes:
        tr[n] = n
    for n in input_nodes:
        tr[n] = n
    for n in output_nodes:
        tr[n] = n
    for n in op_nodes:
        tr[n] = n
    tr['z15'] = 'fph'
    tr['fph'] = 'z15'
    tr['z21'] = 'gds'
    tr['gds'] = 'z21'
    tr['jrs'] = 'wrk'
    tr['wrk'] = 'jrs'
    tr['z34'] = 'cqk'
    tr['cqk'] = 'z34'

    with open("graph.txt", "w") as f:
        for n in sorted(list(input_nodes)):
            n = tr[n]
            print(f'{n} [shape=circle]', file=f)

        for n in sorted(list(output_nodes)):
            n = tr[n]
            print(f'{n} [shape=circle]', file=f)

        for n in value_nodes:
            n = tr[n]
            print(n, file=f)

        for n in carry_nodes:
            n = tr[n]
            print(f'{n} [shape=triangle]', file=f)

        for o in op_nodes:
            color = {'A': 'blue', 'X': 'red', 'O': 'green'}[o[0]]
            print(f'{tr[o]} [shape=box, color={color}]', file=f)
            
        print(" ", file=f)
        
        for e in edges:
            print(f'{e[0]} -> {tr[e[1]]}', file=f)

        # to make the graph more regular
        for i in range(44):
            print(f'x{i:02} -> x{i+1:02}', file=f)

    return 0

# %% --------------------------------------------------
# res_example = part2(data_example[:])
# print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])

print(','.join(sorted(['fph', 'z15', 'gds', 'z21', 'wrk', 'jrs', 'cqk', 'z34'])))

# %% --------------------------------------------------
