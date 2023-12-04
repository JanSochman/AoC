import numpy as np

def get_visibility(forest):
    N = forest.shape[0]
    visibility = np.full((N, N), False)

    for r in range(N):
        max_height = -1 
        for c in range(N):
            if forest[r, c] > max_height:
                visibility[r, c] = True
                max_height = forest[r, c]

    for r in range(N):
        max_height = -1 
        for c in reversed(range(N)):
            if forest[r, c] > max_height:
                visibility[r, c] = True
                max_height = forest[r, c]

    for c in range(N):
        max_height = -1 
        for r in range(N):
            if forest[r, c] > max_height:
                visibility[r, c] = True
                max_height = forest[r, c]

    for c in range(N):
        max_height = -1 
        for r in reversed(range(N)):
            if forest[r, c] > max_height:
                visibility[r, c] = True
                max_height = forest[r, c]

    return visibility


forest = []
with open('input8.txt') as f:
    for line in f:
        line = line.strip()
        tree_row = [*line]
        forest.append([int(t) for t in tree_row])

forest = np.array(forest)
vis = get_visibility(forest)

print(vis.sum())



# Part 2
def score_up(forest, r, c):
    score = 0
    for rr in reversed(range(r)):
        score += 1
        if forest[rr, c] >= forest[r, c]:
            break
    return score


def score_down(forest, r, c):
    N = forest.shape[0]
    score = 0
    for rr in range(r+1, N):
        score += 1
        if forest[rr, c] >= forest[r, c]:
            break
    return score


def score_left(forest, r, c):
    score = 0
    for cc in reversed(range(c)):
        score += 1
        if forest[r, cc] >= forest[r, c]:
            break
    return score


def score_right(forest, r, c):
    N = forest.shape[0]
    score = 0
    for cc in range(c+1, N):
        score += 1
        if forest[r, cc] >= forest[r, c]:
            break
    return score


def get_scenic_score(forest, r, c):
    su = score_up(forest, r, c)
    sd = score_down(forest, r, c)
    sl = score_left(forest, r, c)
    sr = score_right(forest, r, c)
    # print(su, sd, sl, sr)
    score = su * sd * sl * sr
    return score


# print(forest)
N = forest.shape[0]
best_scenic_score = 0
for r in range(N):
    for c in range(N):
        scenic_score = get_scenic_score(forest, r, c)
        if scenic_score > best_scenic_score:
            best_scenic_score = scenic_score

print(f"Best scenic score: {best_scenic_score}")
