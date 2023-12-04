with open('input6.txt') as f:
    for line in f:
        line = line.strip()
        all_items = [*line]

for i in range(len(all_items) - 4):
    code = set(all_items[i:i+4])
    if len(code) == 4:
        print(f"start of packet: {i+4}")
        break

for i in range(len(all_items) - 14):
    code = set(all_items[i:i+14])
    if len(code) == 14:
        print(f"start of message: {i+14}")
        break

