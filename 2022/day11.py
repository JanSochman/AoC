import numpy as np
import re

monkey_pattern = re.compile(r"Monkey (\d+):\n  Starting items: (\d+(, \d+)*)\n  Operation: new = old ([*+]) (\d+|old)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)")

full_text = ''
with open('input11.txt') as f:
    for line in f:
        full_text += line

res = monkey_pattern.match(line)
for res in monkey_pattern.finditer(full_text):
    out = res.group(1, 2, 4, 5, 6, 7, 8)
    print(out)
