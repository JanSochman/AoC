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
import math

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
def part1(data):
    def get_hand(str):
        _, cnts = np.unique(list(str), return_counts=True)
        cnts = np.sort(cnts)[::-1]
        if cnts[0] == 5:
            hand = 6
        elif cnts[0] == 4:
            hand = 5
        elif cnts[0] == 3 and cnts[1] == 2:
            hand = 4
        elif cnts[0] == 3 and cnts[1] == 1:
            hand = 3
        elif cnts[0] == 2 and cnts[1] == 2:
            hand = 2
        elif cnts[0] == 2:
            hand = 1
        else:
            hand = 0
        
        return hand
        
    trtable = str.maketrans({"2": "0", "3": "1", "4": "2", "5": "3", "6": "4", "7": "5", "8": "6", "9": "7", "T": "8", "J": "9", "Q": "A", "K": "B", "A": "C"})
    all_cards = []
    all_bids = []
    all_cards13 = []
    all_card_nums = []

    for row in range(len(data)):
        cards, bid = data[row].split()
        hand = get_hand(cards)
        bid = int(bid)
        cards13 = cards.translate(trtable)
        cards13 = str(hand) + cards13
        cards_num = int(cards13, base=13)
        
        all_cards.append(cards)
        all_bids.append(bid)
        all_cards13.append(cards13)
        all_card_nums.append(cards_num)

    srt_idxs = np.argsort(all_card_nums)
    srt_idxs = srt_idxs[::-1]
    win = np.dot(np.array(all_bids)[srt_idxs], (np.arange(len(all_bids))+1)[::-1])

    return win

# %% --------------------------------------------------
# PART 1
year = 2023
puzzle_day = 7
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

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
    def get_hand(str):
        numJ = sum([1 for c in list(str) if c == 'J'])
        hand_wo_J = [c for c in list(str) if c != 'J']

        _, cnts = np.unique(list(hand_wo_J), return_counts=True)
        cnts = np.sort(cnts)[::-1]
        if numJ == 5:
            return 6
        cnts[0] += numJ
        if cnts[0] == 5:
            hand = 6
        elif cnts[0] == 4:
            hand = 5
        elif cnts[0] == 3 and cnts[1] == 2:
            hand = 4
        elif cnts[0] == 3 and cnts[1] == 1:
            hand = 3
        elif cnts[0] == 2 and cnts[1] == 2:
            hand = 2
        elif cnts[0] == 2:
            hand = 1
        else:
            hand = 0
        
        return hand
        
    trtable = str.maketrans({"2": "0", "3": "1", "4": "2", "5": "3", "6": "4", "7": "5", "8": "6", "9": "7", "T": "8", "J": "9", "Q": "A", "K": "B", "A": "C"})
    all_cards = []
    all_bids = []
    all_cards13 = []
    all_card_nums = []

    for row in range(len(data)):
        cards, bid = data[row].split()
        hand = get_hand(cards)
        bid = int(bid)
        cards13 = cards.translate(trtable)
        cards13 = str(hand) + cards13
        cards_num = int(cards13, base=13)
        
        all_cards.append(cards)
        all_bids.append(bid)
        all_cards13.append(cards13)
        all_card_nums.append(cards_num)

    srt_idxs = np.argsort(all_card_nums)
    srt_idxs = srt_idxs[::-1]
    win = np.dot(np.array(all_bids)[srt_idxs], (np.arange(len(all_bids))+1)[::-1])

    return win

# %% --------------------------------------------------
res_example = part2(data_example)
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full)
print(res_full)


# %% --------------------------------------------------