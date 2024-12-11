import os
from pathlib import Path
import typing
import json
import re
import timeit
import itertools
import multiprocessing
import functools


os.chdir(Path(__file__).parent)

def rule(number: int) -> typing.List[int]:
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        s = str(number)
        hl = len(s)//2
        return [int(s[:hl]), int(s[hl:])]
    else:
        return [number*2024]
    

def apply_rule(number, N, cache):
    if (number, N) in cache:
        return cache[(number, N)]

    if N == 0:
        return 1
    else:
        s = 0
        res = rule(number)
        for i in res:
            s += apply_rule(i, N-1, cache)

        cache[(number, N)] = s
        return s


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))[0]

    data = list(map(int, data.split(" ")))
    cache = {}

    N = 75
    print()

    data = [apply_rule(x, N, cache) for x in data]

    print("Sum:", sum(data))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")