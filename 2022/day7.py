import numpy as np
import re
from anytree import Node, RenderTree

cd_pattern = re.compile(r"^\$ cd") 
ls_pattern = re.compile(r"^\$ ls") 
dir_pattern = re.compile(r"^dir") 
file_pattern = re.compile(r"^(\d)+") 

root = None
cur_dir = None
with open('input7.txt') as f:
    for line in f:
        line = line.strip()

        if cd_pattern.match(line) != None:
            dir_name = line.split(' ')[2]
            if root == None:
                root = Node(dir_name, isdir=True)
                cur_node = root
            if dir_name == "..":
                cur_node = cur_node.parent
            else:
                existing = False
                for c in cur_node.children:
                    if c.name == dir_name:
                        cur_node = c
                        existing = True
                        break
                if not existing:
                    new_node = Node(dir_name, isdir=True, parent=cur_node)
                    cur_node = new_node

            continue

        if ls_pattern.match(line) != None:
            pass

        if dir_pattern.match(line) != None:
            dir_name = line.split(' ')[1]
            existing = False
            for c in cur_node.children:
                if c.name == dir_name:
                    existing = True
                    break
            if not existing:
                new_node = Node(dir_name, isdir=True, parent=cur_node)

            continue


        if file_pattern.match(line) != None:
            file_size, file_name = line.split(' ')
            existing = False
            for c in cur_node.children:
                if c.name == file_name:
                    existing = True
                    break
            if not existing:
                new_node = Node(file_name, isdir=False, parent=cur_node, size=int(file_size))

            continue


# print(RenderTree(root))

sum_size = 0
all_nodes = root.descendants
for n in all_nodes:
    if n.isdir:
        cur_size = 0
        descs = n.descendants
        for d in descs:
            if not d.isdir:
                cur_size += d.size
        if cur_size <= 100000:
            sum_size += cur_size

print(f"Total size of small (<=100000) directories: {sum_size}")

# Part 2
total_space = 70000000
total_occupied = 0
for n in all_nodes:
    if not n.isdir:
        total_occupied += n.size

print(f"Total occupied: {total_occupied}, currently free: {total_space - total_occupied}")
to_free = 30000000 - (total_space - total_occupied)
print(f"Need to free: {to_free}")

smallest = 70000000
all_nodes = root.descendants
for n in all_nodes:
    if n.isdir:
        cur_size = 0
        descs = n.descendants
        for d in descs:
            if not d.isdir:
                cur_size += d.size
        if cur_size >= to_free and cur_size < smallest:
            smallest = cur_size

print(f"The smallest dir to delete has size: {smallest}")
