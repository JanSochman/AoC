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

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    sum = 0
    for L in data:
        digits = re.findall("\d", L)
        number = int(digits[0] + digits[-1])
        sum += number

    return sum

# %% --------------------------------------------------
def part2(data):
    sum = 0
    tr = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    for line in data:
        digits = re.findall("\d|one|two|three|four|five|six|seven|eight|nine", line)
        digits_back = re.findall("\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin", line[::-1])
        # first_digit = digits[0] if len(digits[0]) == 1 else tr[digits[0]]
        first_digit = tr.get(digits[0], digits[0])
        # last_digit = digits_back[0] if len(digits_back[0]) == 1 else tr[digits_back[0][::-1]]
        last_digit = tr.get(digits_back[0][::-1], digits_back[0])
        number = int(first_digit + last_digit)
        sum += number

    return sum

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
