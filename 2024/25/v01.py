import os
from pathlib import Path
import typing
import timeit
from collections import namedtuple
import numpy as np


os.chdir(Path(__file__).parent)

def load_data(data: typing.List[str]) -> typing.Tuple[np.array, np.array]:
    keys = []
    locks = []

    is_key = None
    block = []


    for r in data + [""]:
        if  r == "":
            item = np.sum(np.where(np.array(list(map(list,block[:-1]))) == "#", 1,0), axis=0)
            if is_key:
                keys.append(item)
            else:
                locks.append(item)

            block = []
            is_key = None
            continue

        if is_key is None:
            is_key = (r == "#"*5)
            continue

        block.append(r)

    return keys, locks
    

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    keys, locks = load_data(data)

    counter = 0
    for k in keys:
        for l in locks:
            if all(np.where((k+l) <= 5, True, False)):
                counter += 1


    print(counter)



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")