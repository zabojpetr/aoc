import os
from pathlib import Path
import typing
import json
import re
import numpy as np
import timeit
import itertools

os.chdir(Path(__file__).parent)

def generate_diskspace(data: typing.List[int]) -> typing.List:
    ds = []
    for i,n in enumerate(data):
        if i % 2 == 0:
            ds += [i//2] * n
        else:
            ds += ["."] * n
    return ds

def reorder(ds: typing.List) -> typing.List:
    i = 0
    j = len(ds)

    reordered = []
    while i != j:
        if str(ds[i]) == ".":
            while str(ds[j-1]) == "." and j-1 != i:
                j -= 1
            if (j-1 == i):
                break
            reordered.append(ds[j-1])
            j-=1
        else:
            reordered.append(ds[i])
        i += 1

    return reordered


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))[0]

    ds = generate_diskspace(list(map(int,data)))
    rds = reorder(ds)
    res = sum([i*n for i,n in enumerate(rds)])

    print("Sum:", res)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")