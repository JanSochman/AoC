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
from collections import deque

# for regular expressions debugging: https://pythex.org/


# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    total_points = 0
    
    for L in data:
        _, nums = L.split(': ')
        winning_str, mine_str = nums.split('| ')
        winning = set([int(i) for i in winning_str.strip().split()])
        mine = [int(i) for i in mine_str.strip().split()]
        num_winning = sum([1 for i in mine if i in winning])
        points = 0
        if num_winning > 0:
            points = np.power(2, num_winning-1)
        total_points += points

    return total_points

# %% --------------------------------------------------
def part2(data):
    def num_winning(card):
        _, nums = card.split(': ')
        winning_str, mine_str = nums.split('| ')
        winning = set([int(i) for i in winning_str.strip().split()])
        mine = [int(i) for i in mine_str.strip().split()]
        num = sum([1 for i in mine if i in winning])
        return num

    cached_results = {}
    card_deck = deque(range(len(data)))
    
    num_cards = 0
    while card_deck:
        card = card_deck.popleft()
        num_cards += 1
        num_matches = cached_results.get(card, num_winning(data[card]))
        cached_results[card] = num_matches
        card_deck.extend(range(card+1, card+num_matches+1))

    return num_cards

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 4
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
with open(f'examples/d{puzzle_day}p1.txt', 'r') as file:
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
