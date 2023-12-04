import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import textwrap


X = [1.0]
x = [0.0]

next_cycle = 20
strength = 0
with open('input10.txt') as f:
    for line in f:
        line = line.strip()
        if line == 'noop':
            x.append(x[-1] + 1.0)
            X.append(X[-1])
        else:
            _, count = line.split(' ')
            count = int(count)
            x.append(x[-1] + 2.0)
            X.append(X[-1] + count)
        if x[-1] >= next_cycle:
            print(f"cycle {next_cycle} * register {X[-2]} = {next_cycle * X[-2]}")
            strength += next_cycle * X[-2]
            next_cycle += 40

print(f"strength: {strength}")

# part 2
def draw(display, pos, cursor_pos, cycles):
    for c in range(cycles):
        if abs((pos + c) % 40 - cursor_pos) <= 1:
            display[pos+c] = '#'
    return display


display = ['.'] * 240
cursor_pos = 1
pos = 0
with open('input10.txt') as f:
    for line in f:
        line = line.strip()
        if line == 'noop':
            display = draw(display, pos, cursor_pos, 1)
            pos += 1
        else:
            display = draw(display, pos, cursor_pos, 2)
            pos += 2
            _, count = line.split(' ')
            cursor_pos += int(count)

# display the result
display = ''.join(display)
wrapper = textwrap.TextWrapper(width=40)
dlines = wrapper.wrap(text=display)
for line in dlines:
    print(line)
