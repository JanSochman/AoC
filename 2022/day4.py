
num_full_overlap = 0
with open('input4.txt') as f:
    for line in f:
        line = line.strip()
        e1, e2 = line.split(',')
        e1_min, e1_max = [int(n) for n in e1.split('-')]
        e2_min, e2_max = [int(n) for n in e2.split('-')]
        if (e1_min >= e2_min and e1_max <= e2_max) or (e2_min >= e1_min and e2_max <= e1_max):
            num_full_overlap += 1

print(f"Number of full overlaps: {num_full_overlap}.")

num_part_overlap = 0
with open('input4.txt') as f:
    for line in f:
        line = line.strip()
        e1, e2 = line.split(',')
        e1_min, e1_max = [int(n) for n in e1.split('-')]
        e2_min, e2_max = [int(n) for n in e2.split('-')]
        if (e1_min >= e2_min and e1_max <= e2_max) or (e2_min >= e1_min and e2_max <= e1_max) or (e1_min >= e2_min and e1_min <= e2_max) or (e1_max >= e2_min and e1_max <= e2_max):
            num_part_overlap += 1

print(f"Number of partial overlaps: {num_part_overlap}.")


