import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np
from collections import namedtuple
import heapq
import functools

os.chdir(Path(__file__).parent)

cache = {}

def is_design_valid(design: str, combs: typing.Set[str]):
    if design in cache:
        return cache[design]
    num_combs = 0
    if design == "":
        return 1
    for c in combs:
        if design.startswith(c):
            num_combs += is_design_valid(design[len(c):], combs)
    cache[design] = num_combs
    return num_combs

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    combs = set(list(map(lambda x: x.strip(),data[0].split(","))))
    designs = data[2:]

    res = list(map(lambda x: is_design_valid(x, combs), designs))
    
    print("Sum:", sum(res))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")