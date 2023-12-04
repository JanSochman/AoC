import numpy as np
import re

instruction_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)") 

# -- PART 1 --
input_grid = []
read_grid = True
towers = []
with open('input5.txt') as f:
    for line in f:
        if read_grid:
            if len(line) == 1:  # the end of the grid
                read_grid = False
                input_grid = np.array(input_grid)
                input_grid = input_grid[-2::-1, 1::4]
                for i in range(9):
                    tower = [x for x in list(input_grid[:, i]) if x != ' ']
                    towers.append(tower)
                continue
            line_chars = [*line]
            input_grid.append(line_chars)
        else:    # read the instructions
            line = line.strip()
            res = instruction_pattern.match(line)
            count = int(res.group(1))
            from_tower = int(res.group(2)) - 1
            to_tower = int(res.group(3)) - 1
            # print(towers)
            # print(f"count {count}, from {from_tower}, to {to_tower}")
            for i in range(count):
                towers[to_tower].append(towers[from_tower].pop())

# print(input_grid)
# print(towers)

print(''.join([t.pop() for t in towers]))


# -- PART 2 --
input_grid = []
read_grid = True
towers = []
with open('input5.txt') as f:
    for line in f:
        if read_grid:
            if len(line) == 1:  # the end of the grid
                read_grid = False
                input_grid = np.array(input_grid)
                input_grid = input_grid[-2::-1, 1::4]
                for i in range(9):
                    tower = [x for x in list(input_grid[:, i]) if x != ' ']
                    towers.append(tower)
                continue
            line_chars = [*line]
            input_grid.append(line_chars)
        else:    # read the instructions
            line = line.strip()
            res = instruction_pattern.match(line)
            count = int(res.group(1))
            from_tower = int(res.group(2)) - 1
            to_tower = int(res.group(3)) - 1
            towers[to_tower] += towers[from_tower][-count:]
            towers[from_tower] = towers[from_tower][:-count]

# print(input_grid)
print(towers)

print(''.join([t.pop() for t in towers]))
