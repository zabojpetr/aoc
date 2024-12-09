import os
from pathlib import Path
import typing
import json
import re
import numpy as np
import timeit
import itertools

os.chdir(Path(__file__).parent)

def load_map(data: typing.List[str]) -> typing.Dict[str,typing.List[np.array]]:
    mapa = {}
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == ".":
                continue
            if c not in mapa:
                mapa[c] = []
            mapa[c].append(np.array([i,j]))

    return mapa

def generate_antinodes(antennas: typing.List[np.array]):
    combs = itertools.combinations(list(range(len(antennas))),2)
    antinodes = []
    for (a,b) in combs:
        diff = antennas[b] - antennas[a]
        antinodes.append(antennas[a] - diff)
        antinodes.append(antennas[b] + diff)

    return set(map(tuple,antinodes))

def out_of_bounds(tup, r,c):
    return tup[0] < 0 or tup[0] >= r or tup[1] < 0 or tup[1] >= c


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))

    r = len(data)
    c = len(data[0])
    mapa = load_map(data)
    antimodes = set()
    for a, p in mapa.items():
        antimodes.update(generate_antinodes(p))
        
    antimodes = set({a for a in antimodes if not out_of_bounds(a,r,c)})

    print("Sum:", len(antimodes))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")