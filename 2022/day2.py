import numpy as np

his = []
mine = []
with open('input2.txt') as f:
    for line in f:
        line = line.strip()
        he, me = line.split(' ')
        his.append(he)
        mine.append(me)

shape_map = {'X': 0, 'Y': 1, 'Z': 2}
his_shape_map = {'A': 0, 'B': 1, 'C': 2}

his = np.array([his_shape_map[he] for he in his])
mine = np.array([shape_map[me] for me in mine])


def get_score(his, mine):
    shape_score = np.sum(mine + 1)
    draw_score = np.sum(his == mine) * 3
    win_score = np.sum(mine == (his + 1) % 3) * 6

    print(f"shape score is {shape_score}.")
    print(f"draw score is {draw_score}.")
    print(f"win score is {win_score}.")

    return win_score + draw_score + shape_score


def remap(his, mine):
    new_mine = mine.copy()
    new_mine[mine == 0] = his[mine == 0] - 1
    new_mine[mine == 1] = his[mine == 1]
    new_mine[mine == 2] = his[mine == 2] + 1

    new_mine[new_mine == -1] = 2
    new_mine[new_mine == 3] = 0

    return new_mine


score = get_score(his, mine)
print(f"part1: total score is {score}.")

mine = remap(his, mine)
score = get_score(his, mine)
print(f"part2: total score is {score}.")

