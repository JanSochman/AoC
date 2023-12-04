# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print
# import parse                        # easy string parsing 
from parse import parse
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
    total_sum = 0
    for L in data:
        game_str, cubes_str = L.split(': ')
        game_id = int(parse('Game {}', game_str)[0])
        draws = cubes_str.split('; ')
        good_game = True
        for d in draws:
            r_list = re.findall('(\d+) red', d)
            g_list = re.findall('(\d+) green', d)
            b_list = re.findall('(\d+) blue', d)
            
            r_n = sum([int(n) for n in r_list])
            g_n = sum([int(n) for n in g_list])
            b_n = sum([int(n) for n in b_list])
            
            if r_n > 12 or g_n > 13 or b_n > 14:
                good_game = False
                break
            
        if good_game:
            total_sum += game_id

    return total_sum

# %% --------------------------------------------------
def part2(data):
    total_sum = 0
    for L in data:
        game_str, cubes_str = L.split(': ')
        game_id = int(parse('Game {}', game_str)[0])
        draws = cubes_str.split('; ')
        r_n = 0
        g_n = 0
        b_n = 0
        for d in draws:
            r_list = re.findall('(\d+) red', d)
            g_list = re.findall('(\d+) green', d)
            b_list = re.findall('(\d+) blue', d)
            
            r_n = max([r_n, sum([int(n) for n in r_list])])
            g_n = max([g_n, sum([int(n) for n in g_list])])
            b_n = max([b_n, sum([int(n) for n in b_list])])
            
        cube_power = r_n * g_n * b_n
        total_sum += cube_power

    return total_sum

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 2
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
