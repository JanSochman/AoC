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
from collections import deque, Counter, defaultdict
import parsy as ps
import portion as P
import math

# for regular expressions debugging: https://pythex.org/

# %% --------------------------------------------------
def parse_input(input):
    lines = input.split('\n')
    return lines

# %% --------------------------------------------------
# ========== PART 1 ==========
year = 2023
puzzle_day = 12
puzzle = Puzzle(year=year, day=puzzle_day)
print(puzzle.input_data[:20])

example1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

data_example = parse_input(example1)
data_full = parse_input(puzzle.input_data)

# %% --------------------------------------------------
def part1(data):
    total_num = 0
    for L in data:
        broken_records = L.split()[0]
        cnts = [int(x) for x in re.findall(r'\d+', L)]
        N = len(broken_records)

        variants = deque()
        variants.append((broken_records[:], 0))
        while variants:
            cur_var, idx = variants.popleft()
            while idx < N and cur_var[idx] in '.#':
                idx += 1
            if idx == N:
                groups = re.findall(r'[#\?]+', cur_var)
                g_cnts = [g.count('#') for g in groups]
                if len(cnts) == len(g_cnts) and cnts == g_cnts:
                    total_num += 1
                    continue
            else:
                var1 = cur_var[:idx] + '.' + cur_var[idx+1:]
                var2 = cur_var[:idx] + '#' + cur_var[idx+1:]
                variants.append((var1, idx+1))
                variants.append((var2, idx+1))
        
    return total_num

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
def part2_nice_but_not_fast_enough(data):
    total_num = 0
    reps = 5
    # for L in data[5:6]:
    for L in data:
        num_vars = 0
        num_tests = 0
        broken_records = "?".join([L.split()[0]] * reps)
        cnts = [int(x) for x in re.findall(r'\d+', L)] * reps
        # print(broken_records, cnts)
        M = len(cnts)
        N = len(broken_records)

        variants = deque()
        variants.append((broken_records[:], 0, 0))
        while variants:
            num_tests += 1
            cur_var, idx, cnt_idx = variants.popleft()
            # print(cur_var, cnts[cnt_idx:], idx)
            
            # the remaining counts will not fit
            if N - idx < sum(cnts[cnt_idx:]) + len(cnts[cnt_idx:]) - 1:
                continue

            # always move one step right
            if idx < N:
                # but test if all solved fist...
                if cur_var.count('?') == 0:
                    groups = re.findall(r'[#\?]+', cur_var)
                    g_cnts = [g.count('#') for g in groups]
                    if len(cnts) == len(g_cnts) and cnts == g_cnts:
                        total_num += 1
                        num_vars += 1
                        # print(f'accepted 1 {cur_var}', cnts[cnt_idx:], idx)
                        continue
                if cur_var[idx] == '?':
                    next_var = cur_var[:idx] + '.' + cur_var[idx+1:]
                else:
                    next_var = cur_var[:]   # just move right

                if cnt_idx < M:
                    variants.append((next_var, idx + 1, cnt_idx))
                # print(f'added 1 {next_var}', cnts[cnt_idx:], idx+1)

            # if at the end, test if the variant is correct
            if idx == N:
                groups = re.findall(r'[#\?]+', cur_var)
                g_cnts = [g.count('#') for g in groups]
                if len(cnts) == len(g_cnts) and cnts == g_cnts:
                    total_num += 1
                    num_vars += 1
                    # print(f'accepted 2 {cur_var}', cnts[cnt_idx:], idx)
                    continue
            else:
                # all counts fullfiled -> test the correctness when all other ? are mapped to .
                if cnt_idx >= M:
                    cur_var = cur_var.replace('?', '.')
                    cur_cnts = [x.count('#') for x in re.findall(r'(#+)', cur_var)]
                    if len(cnts) == len(cur_cnts) and cnts == cur_cnts:
                        total_num += 1
                        num_vars += 1
                        # print(f'accepted 3 {cur_var}', cnts[cnt_idx:], idx)
                    # print('rejected: counts fulfilled')
                    continue
                
                # the remaining counts will not fit
                if N - idx < sum(cnts[cnt_idx:]) + len(cnts[cnt_idx:]) - 1:
                    continue

                next_len = cnts[cnt_idx]
                candidate = cur_var[idx:idx+next_len]

                if len(candidate) < next_len:   # not enough symbols to satisfy the counts
                    # print('reject: length')
                    continue

                if candidate.replace('?', '#').find('.') != -1: # . does allow to fit the count
                    # print('reject: no fit')
                    continue

                # test that the candidate is not followed by . and not at the end of the text
                if idx + next_len < N and cur_var[idx + next_len] not in '.?':
                    # print('reject: not followed by .')
                    continue

                var_good = cur_var[:idx] + '#' * next_len + '.' + cur_var[idx+next_len+1:]

                m = re.search(r'^[.#]+(\.|$)', var_good)
                good_part = m.group(0) if m else ''
                if len(good_part) == 1:
                    good_part = good_part[0]
                gp_cnts = [x.count('#') for x in re.findall(r'(#+)', good_part)]

                if len(gp_cnts) <= M and gp_cnts == cnts[:len(gp_cnts)]:
                    variants.append((var_good, idx+next_len+1, cnt_idx+1))
        print(num_vars, num_tests)
        
    return total_num

# %% --------------------------------------------------
def part2(data):
    total_num = 0
    reps = 5
    for L in data:
        num_vars = 0
        broken_records = "?".join([L.split()[0]] * reps)
        broken_records = broken_records.strip('.')      # unnecessary bits
        cnts = [int(x) for x in re.findall(r'\d+', L)] * reps
        N = len(broken_records)
        M = len(cnts)
        num_options = N - sum(cnts) - (M - 1) + 1
        ok = np.zeros((num_options, M))
        
        for i, c in enumerate(cnts):
            first = sum(cnts[:i]) + len(cnts[:i])
            for o in range(num_options): 
                start = first + o
                if start > 0:
                    if broken_records[start-1] == '#':
                        continue    # not ok position
                if start + c < N:
                    if broken_records[start + c] == '#':
                        continue    # not ok position
                if broken_records[start:start+c].count('.') > 0:
                    continue        # not ok position
                ok[o, i] = 1

        # integral image
        hash_ii = np.cumsum([int(x == '#') for x in broken_records])
        compatibility = np.triu(np.ones((num_options, num_options)))
        compatibility[ok[:, 0] == 0, :] = 0
        compatibility[:, ok[:, 1] == 0] = 0
        i = 0
        j = 1
        # test for residual #s in between the official #s
        for oi in range(num_options):
            for oj in range(oi, num_options):
                first_end = sum(cnts[:i]) + len(cnts[:i]) + oi + cnts[i]
                second_start = sum(cnts[:j]) + len(cnts[:j]) + oj - 1
                if hash_ii[second_start] - hash_ii[first_end] > 0:
                    compatibility[oi, oj] = 0
        # test for the residual # at the beginning
        for oi in range(num_options):
            first_start = sum(cnts[:i]) + len(cnts[:i]) + oi
            if first_start > 0 and hash_ii[first_start - 1] > 0:
                compatibility[oi, :] = 0
                
        for i in range(1, M-1):
            j = i + 1
            next_comp = np.triu(np.ones((num_options, num_options)))
            next_comp[ok[:, i] == 0, :] = 0
            next_comp[:, ok[:, j] == 0] = 0
            # test for residual #s in between the official #s
            for oi in range(num_options):
                for oj in range(oi, num_options):
                    first_end = sum(cnts[:i]) + len(cnts[:i]) + oi + cnts[i]
                    second_start = sum(cnts[:j]) + len(cnts[:j]) + oj - 1
                    if hash_ii[second_start] - hash_ii[first_end] > 0:
                        next_comp[oi, oj] = 0
            compatibility = np.matmul(compatibility, next_comp)
            
        # test for residual # at the end
        j = M - 1
        for oj in range(num_options):
            end = sum(cnts[:j]) + len(cnts[:j]) + oj + cnts[j]
            if end < N - 1 and hash_ii[N-1] - hash_ii[end] > 0:
                compatibility[:, oj] = 0

        num_vars = compatibility.sum()
        total_num += num_vars

    return total_num

# %% --------------------------------------------------
res_example = part2(data_example[:])
print(res_example)

# %% --------------------------------------------------
res_full = part2(data_full[:])
print(res_full)

# %% --------------------------------------------------
