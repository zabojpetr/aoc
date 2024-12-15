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
        repl = {".":"..", "#":"##", "@":"@.", "O":"[]"}
        mapa = np.array(list(map(list,map(lambda x: "".join([repl[c] for c in x]),data))))
        possition = np.where(mapa == "@")

        self.robot = np.array([possition[0][0], possition[1][0]])
        self.mapa = mapa

    def _can_move_up_down(self, direction:str, possition: np.array):
        d = self.dirs[direction]


        if self.mapa[*(possition + d)] == ".":
            return True
        elif self.mapa[*(possition + d)] == "#":
            return False
        elif self.mapa[*(possition + d)] == "[":
            l = self._can_move_up_down(direction, possition+d)
            r = self._can_move_up_down(direction, possition+d+self.dirs[">"])
            return l and r
        elif self.mapa[*(possition + d)] == "]":
            l = self._can_move_up_down(direction, possition+d+self.dirs["<"])
            r = self._can_move_up_down(direction, possition+d)
            return l and r

    def _move_up_down(self, direction:str, possition: np.array):
        d = self.dirs[direction]


        if self.mapa[*(possition + d)] == "[":
            l = self._move_up_down(direction, possition+d)
            r = self._move_up_down(direction, possition+d+self.dirs[">"])
            self.mapa[*(possition+d)] = "."
            self.mapa[*(possition+d+self.dirs[">"])] = "."
        elif self.mapa[*(possition + d)] == "]":
            l = self._move_up_down(direction, possition+d+self.dirs["<"])
            r = self._move_up_down(direction, possition+d)
            self.mapa[*(possition+d+self.dirs["<"])] = "."
            self.mapa[*(possition+d)] = "."
        
        self.mapa[*(possition + d)] = self.mapa[*possition]

    def move_if_possible(self, direction: str):
        d = self.dirs[direction]

        if direction in set(["<",">"]):
            new_pos = self.robot + d
            while not(self.mapa[*new_pos] == "." or self.mapa[*new_pos] == "#"):
                new_pos = new_pos + d

            if self.mapa[*new_pos] == ".":
                r = self.robot[0]
                c1 = min(new_pos[1], self.robot[1])
                c2 = max(new_pos[1], self.robot[1])

                self.mapa[r, c1:c2+1] = np.roll(self.mapa[r, c1:c2+1], d[1])
                self.robot += d

        else:
            if self._can_move_up_down(direction, self.robot):
                self._move_up_down(direction, self.robot)
                self.mapa[*self.robot] = "."
                self.robot = self.robot+d



    def sum_gps(self) -> int:
        x,y = np.where(self.mapa=="[")

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