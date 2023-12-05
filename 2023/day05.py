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
from collections import deque
import parsy as ps
import portion as P

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    src = np.array(re.findall(r"(\d+)", data[0]), dtype=int)
    dst = src.copy()
    for row in range(1, len(data)):
        if not data[row]:
            src = dst.copy()
            continue

        if re.match(r"^\D", data[row]):
            dst = src.copy()
            continue

        dst_start, src_start, cnt = [int(i) for i in re.findall(r"(\d+)", data[row])]
        
        mask = np.logical_and(src >= src_start, src < src_start + cnt)
        if np.sum(mask):
            dst[mask] = src[mask] - src_start + dst_start

    return np.min(dst)

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 5
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
res_example = part1(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full)
print(res_full)

# %% --------------------------------------------------
class IntInterval(P.AbstractDiscreteInterval):
    _step = 1
    
D = P.create_api(IntInterval)

# %% --------------------------------------------------
# PART 2
def part2(data):
    seeds = np.array(re.findall(r"(\d+)", data[0]), dtype=int)
    src = D.open(P.inf, -P.inf)
    for (int_start, int_len) in zip(seeds[::2], seeds[1::2]):
        src = src.union(D.closed(int_start, int_start+int_len-1))
        
    dst = D.open(P.inf, -P.inf)
    for row in range(1, len(data)):
        if not data[row]:
            src = dst | src
            dst = D.open(P.inf, -P.inf)
            continue

        if re.match(r"^\D", data[row]):
            continue

        dst_start, src_start, cnt = [int(i) for i in re.findall(r"(\d+)", data[row])]
        
        sub_int = src.intersection(D.closedopen(src_start, src_start+cnt))
        dst = dst.union(sub_int.apply(lambda x: (x.left, x.lower - src_start + dst_start, x.upper - src_start + dst_start, x.right)))
        src = src - sub_int

    dst = dst | src
    return np.min(dst[0].lower)

# %% --------------------------------------------------
res_example = part2(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full)
print(res_full)


# %% --------------------------------------------------
