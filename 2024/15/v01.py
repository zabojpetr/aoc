import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np

os.chdir(Path(__file__).parent)



class Mapa():
    dirs = {
        ">" : np.array([0,1]),
        "v" : np.array([1,0]),
        "<" : np.array([0,-1]),
        "^" : np.array([-1,0]),
    }

    def __init__(self, data: typing.List[str]):
        self.mapa = None
        self.robot = None

        self.load_data(data)

    def load_data(self, data: typing.List[str]):
        mapa = np.array(list(map(list,data)))
        possition = np.where(mapa == "@")

        self.robot = np.array([possition[0][0], possition[1][0]])
        self.mapa = mapa

    def move_if_possible(self, direction: str):
        d = self.dirs[direction]

        new_pos = self.robot + d
        while not(self.mapa[*new_pos] == "." or self.mapa[*new_pos] == "#"):
            new_pos = new_pos + d

        if self.mapa[*new_pos] == ".":
            self.mapa[*(self.robot+d)] = "@"
            self.mapa[*(self.robot)] = "."
            self.robot = self.robot+d
            if tuple(new_pos) != tuple(self.robot):
                self.mapa[*new_pos] = "O"

    def sum_gps(self) -> int:
        x,y = np.where(self.mapa=="O")

        return np.sum(x*100) + np.sum(y)

    def __str__(self):
        return "\n".join(map(lambda x: "".join(x), self.mapa))


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    idx = data.index("")
    mapa = data[:idx]
    dirs = data[idx:]

    m = Mapa(mapa)
    for r in dirs:
        for c in r:
            if not c:
                continue
            m.move_if_possible(c)

    print("Sum:", m.sum_gps())

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")