import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

def count_middle_sums(updates:typing.List[str]) -> int:
    nums = [u[len(u)//2] for u in updates]

    return sum(nums)

def create_rules(data:typing.List[str]) -> typing.Dict[int,typing.Tuple[typing.List[int], typing.List[int]]]:
    rules = {}
    for r in data:
        if len(r) == 0:
            continue
        x,y = map(int, r.split("|"))
        if x not in rules:
            rules[x] = (set(), set())
        if y not in rules:
            rules[y] = (set(),set())
        rules[x][1].add(y)
        rules[y][0].add(x)
        
    return rules

def is_correct(data: typing.List[int], rules: typing.Dict[int,typing.Tuple[typing.List[int], typing.List[int]]]) -> bool:
    correct = True
    for i in range(len(data)):
        p = data[i]
        if p in rules:
            after = rules[p][1]
            correct = len(set(data[:i]).intersection(after)) == 0
        if not correct:
            break

    return correct


def main() -> None:
    rules = {}
    updates = []
    with open("input_test.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    delim_idx = data.index("")

    rules = create_rules(data[:delim_idx])

    updates = list(map(lambda x: list(map(int,x.split(","))), filter(lambda x: len(x) > 0, data[data.index("")+1:])))

    right_updates = list(filter(lambda x: is_correct(x, rules), updates))

    d = count_middle_sums(right_updates)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()