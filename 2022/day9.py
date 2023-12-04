import numpy as np

# ----- PART 1 -----
knots_pos = np.array([0, 0])
tail_pos = np.array([0, 0])
positions = {tuple(tail_pos)}
with open('input9.txt') as f:
    for line in f:
        line = line.strip()
        direction, count = line.split(' ')
        for i in range(int(count)):
            old_head_pos = knots_pos.copy()
            if direction == 'U':
                knots_pos[0] += 1
            elif direction == 'D':
                knots_pos[0] -= 1
            elif direction == 'L':
                knots_pos[1] -= 1
            else:
                knots_pos[1] += 1

            if np.max(np.abs(tail_pos - knots_pos)) > 1:
                tail_pos = old_head_pos.copy()
                positions.add(tuple(tail_pos))

print(len(positions))
            
# ----- PART 2 -----
knots_pos = np.tile(np.array([0, 0]), (10, 1))
positions = {tuple(knots_pos[-1, :])}
cnt = 0
with open('input9.txt') as f:
    for line in f:
        line = line.strip()
        direction, count = line.split(' ')
        for i in range(int(count)):
            old_knots_pos = knots_pos.copy()
            if direction == 'U':
                knots_pos[0, 0] += 1
            elif direction == 'D':
                knots_pos[0, 0] -= 1
            elif direction == 'L':
                knots_pos[0, 1] -= 1
            else:
                knots_pos[0, 1] += 1
            for k in range(1, 10):
                diff = knots_pos[k-1, :] - knots_pos[k, :]
                is_still_close = np.sum(np.abs(diff)) <= 1
                if np.max(np.abs(diff)) <= 1:   # no need to move
                    break
                if np.abs(diff[0]) >= 1:
                    knots_pos[k, 0] += np.sign(diff[0])
                if np.abs(diff[1]) >= 1:
                    knots_pos[k, 1] += np.sign(diff[1])

            positions.add(tuple(knots_pos[-1, :]))

print(len(positions))
