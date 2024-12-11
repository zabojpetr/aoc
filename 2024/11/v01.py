import os
from pathlib import Path
import typing
import json
import re
import timeit
import itertools


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

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))[0]

    data = list(map(int, data.split(" ")))
    N = 40

    for _ in range(N):
        data = [i for l in map(rule, data) for i in l]

    print("Sum:", len(data))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")