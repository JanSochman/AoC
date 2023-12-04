# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print
import parse                        # easy string parsing 
from types import SimpleNamespace
from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
import re                           # for parsing using regular expressions
from anytree import Node, RenderTree    # for building trees

# for regular expressions debugging: https://pythex.org/


# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    pass

# %% --------------------------------------------------
def part2(data):
    pass

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 1
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

with open(f'examples/d{puzzle_day}p1.txt', 'r') as file:
    example1 = file.read().strip()
print(example1)

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
res_example = part1(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part1(data_full)
print(res_full)

# %% --------------------------------------------------
# PART 2
with open(f'examples/d{puzzle_day}p2.txt', 'r') as file:
    example2 = file.read().strip()
print(example2)

data_example = parse_input(example2)

# %% --------------------------------------------------
res_example = part2(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full)
print(res_full)

# %% --------------------------------------------------
