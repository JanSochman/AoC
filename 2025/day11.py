# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print  # as rprint
import builtins                     # to get access to original print for print to file
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
# for a good graph visualization use GrapViz (https://dreampuf.github.io/GraphvizOnline) - just export the graph to their format


# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2025
puzzle_day = 11
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:200])

data_example = parse_input(puzzle.examples[0].input_data)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    G = nx.DiGraph()
    for L in data:
        node, connections = L.split(': ') 
        tonodes = connections.split()
        for tn in tonodes:
            G.add_edge(node, tn)
            
    return len(list(nx.all_simple_paths(G, 'you', 'out')))

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
data_example = parse_input("""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""")

# %% --------------------------------------------------
# I had to try it, just in case... :))
def part2(data):
    G = nx.DiGraph()
    for L in data:
        node, connections = L.split(': ') 
        tonodes = connections.split()
        G.add_node(node)
        G.add_nodes_from(tonodes)
        for tn in tonodes:
            G.add_edge(node, tn)
            
    svr_dac = len(list(nx.all_simple_paths(G, 'svr', 'dac')))
    svr_fft = len(list(nx.all_simple_paths(G, 'svr', 'fft')))
    fft_dac = len(list(nx.all_simple_paths(G, 'fft', 'dac')))
    dac_fft = len(list(nx.all_simple_paths(G, 'dac', 'fft')))
    fft_out = len(list(nx.all_simple_paths(G, 'fft', 'out')))
    dac_out = len(list(nx.all_simple_paths(G, 'dac', 'out')))

    return svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out

# %% --------------------------------------------------
# The solution.
def part2(data):
    G = nx.DiGraph()
    for L in data:
        # build the graph
        node, connections = L.split(': ') 
        tonodes = connections.split()
        G.add_node(node)
        G.add_nodes_from(tonodes)
        for tn in tonodes:
            G.add_edge(node, tn)
            
    # I have used this to understand the structure of the graph
    # color_map = ['red' if node in ['svr', 'out', 'fft', 'dac'] else 'green' for node in G] 
    # plt.figure(figsize=(50, 50))
    # nx.draw_kamada_kawai(G, with_labels=True, node_color=color_map)
    # 
    # And even better visualization is seen in grapviz (https://dreampuf.github.io/GraphvizOnline).
    # This is an export of the graph to their format. Just copy-paste it there...
    # with open("graph.txt", "w") as f:
    #     for e in G.edges:
    #         builtins.print(f'{e[0]} -> {e[1]}', file=f)

    node_info = {}
    for n in G:
        # node_info contains:
        #  number of incoming adges to satisfy
        #  how many paths lead to this node
        #  how many required nodes were visited to reach this node
        node_info[n] = sn(num_in = len(list(G.in_edges(n))), num_paths = 0, num_required = 0)
        
    node_info['svr'].num_paths = 1

    frontier_nodes = {'svr'}

    while node_info['out'].num_in > 0:
        to_remove = set()
        to_add = set()
        for n in frontier_nodes:
            if node_info[n].num_in == 0:    # all dependences satisfied
                if n in ['fft', 'dac']:
                    node_info[n].num_required += 1
                to_remove.add(n)
                # expand further
                for nbr in G[n]:
                    node_info[nbr].num_in -= 1
                    if node_info[nbr].num_required == node_info[n].num_required:
                        node_info[nbr].num_paths += node_info[n].num_paths
                    elif node_info[nbr].num_required < node_info[n].num_required:
                        node_info[nbr].num_paths = node_info[n].num_paths
                        node_info[nbr].num_required = node_info[n].num_required
                    if nbr not in frontier_nodes:
                        to_add.add(nbr)
        frontier_nodes.difference_update(to_remove)
        frontier_nodes.update(to_add)
        
    return node_info['out'].num_paths
        

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
t0 = time.time()
res_full = part2(data_full[:])
t1 = time.time()
print(res_full)
print(f'{t1-t0}s')
