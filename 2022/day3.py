
priority_map = {chr(i):i-96 for i in range(97, 123)}  # lower-case
priority_map.update({chr(i):i-65+27 for i in range(65, 91)})   # upper-case

priority = 0
with open('input3.txt') as f:
    for line in f:
        line = line.strip()
        all_items = [*line]
        comp1 = set(all_items[:len(all_items) // 2])
        comp2 = set(all_items[len(all_items) // 2:])
        isect = list(comp1 & comp2)
        priority += sum([priority_map[item] for item in isect])

print(f"Total priority: {priority}.")

priority = 0
with open('input3.txt') as f:
    counter = 0
    group_items = []
    for line in f:
        line = line.strip()
        all_items = [*line]
        group_items.append(all_items)
        counter += 1
        if counter == 3:
            group_badge = list(set(group_items[0]) & set(group_items[1]) & set(group_items[2]))
            priority += priority_map[group_badge[0]]
            counter = 0
            group_items = []

print(f"Group badges priority: {priority}.")
