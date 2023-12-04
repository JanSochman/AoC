# %% ----------------------------
import numpy as np
from aocd.models import Puzzle      # easy loading the puzzle data
from rich import print
# import parse                        # easy string parsing 
from parse import parse
from types import SimpleNamespace as sn
from utils import StateMachine      # a skeleton for building a state machine and run it
from itertools import combinations  # returns all k-combinations of a list elements
import re                           # for parsing using regular expressions
from anytree import Node, RenderTree    # for building trees
from scipy import ndimage
import copy

# for regular expressions debugging: https://pythex.org/


# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    total_sum = 0
    data_np = np.empty((0, len(data[0])))
    for L in data:
        row = np.array(list(L.strip()))
        data_np = np.vstack((data_np, row))
        
    symbol_mask = np.isin(data_np, np.array(['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']), invert=True) 
    struct2 = ndimage.generate_binary_structure(2, 2)
    is_neigh = ndimage.binary_dilation(symbol_mask, structure=struct2).astype(symbol_mask.dtype)
    
    i = 0
    for L in data:
        for x in re.finditer('(\d+)', L):
            num = int(x.group())
            is_close = np.any(is_neigh[i, x.span()[0]:x.span()[1]])
            if is_close:
                total_sum += num
        i += 1

    return total_sum

# %% --------------------------------------------------
def get_numbers(row_str):
    numbers = []
    for x in re.finditer('(\d+)', row_str):
        numbers.append(sn(num=int(x.group()), span=x.span()))
    return numbers

# %% --------------------------------------------------
def part2(data_):
    data = data_[:]
    total_sum = 0
    data.append('.' * len(data[0]))     # extra empty row at the end
    nums_prev = []
    nums_cur = []
    nums_next = get_numbers(data[0])
    for row in range(0, len(data)-1):
        nums_prev = copy.deepcopy(nums_cur)
        nums_cur = copy.deepcopy(nums_next)
        nums_next = get_numbers(data[row+1])
        all_nums = nums_prev + nums_cur + nums_next
        for x in re.finditer('\*', data[row]):
            pos = x.span()[0]
            n_prod = 1
            n_cnt = 0
            for i in range(len(all_nums)):
                if max(pos-1, all_nums[i].span[0]) <= min(pos+1, all_nums[i].span[1]-1):
                    n_cnt += 1
                    n_prod *= all_nums[i].num
            if n_cnt == 2:
                total_sum += n_prod

    return total_sum

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 3
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

