elfs = []
cur_calories = 0
with open('input1.txt') as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            elfs.append(cur_calories)
            cur_calories = 0
        else:
            cur_calories += int(line.strip())

best_elf_calories = sorted(elfs, reverse=True)[0]
print(f"Elf with the most calories is carrying {best_elf_calories} calories.")
best_3elf_calories = sum(sorted(elfs, reverse=True)[:3])
print(f"Three elves with the most calories are carrying {best_3elf_calories} calories.")
