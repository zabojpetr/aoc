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

    while True:
        id_counter = 0
        space_counter = 0
        id = None

        while str(ds[j-1]) == ".":
            j -= 1

        id = str(ds[j-1])
        while str(ds[j-1]) == id and j > 0:
            id_counter += 1
            j -= 1

        if j == 0:
            break

        for i in range(j):
            if str(ds[i]) == ".":
                space_counter += 1
            else:
                space_counter = 0

            if space_counter == id_counter:
                ds[i-id_counter+1:i+1] = [int(id)]*id_counter
                ds[j:j+id_counter] = ["."]*id_counter
                break
        

    return ds


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))[0]

    ds = generate_diskspace(list(map(int,data)))
    rds = reorder(ds)
    res = sum([i*n for i,n in enumerate(map(lambda x: 0 if x == "." else x, rds))])

    print("Sum:", res)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")