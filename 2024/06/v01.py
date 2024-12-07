import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

class Map:
    def __init__(self, data = None):
        self._map: np.ndarray = np.array([])
        self._position = ()
        self._direction = None
        self._is_end = False

        if data:
            self.load_map(data)

    def _is_out_of_bounds(self, x:int,y:int) -> bool:
        is_out = x < 0 or x >= self._map.shape[0] or y < 0 or y >= self._map.shape[1] 
        return is_out

    def load_map(self, data: typing.List[str]):
        m = [list(row.strip()) for row in data]
        for i in range(len(m)):
            if "^" in m[i]:
                j = m[i].index("^")
                self._direction = np.array([-1,0])
                self._position = np.array([i,j])
            elif ">" in m[i]:
                j = m[i].index(">")
                self._direction = np.array([0,1])
                self._position = np.array([i,j])
            elif "<" in m[i]:
                j = m[i].index("<")
                self._direction = np.array([0,-1])
                self._position = np.array([i,j])
            elif "v" in m[i]:
                j = m[i].index("v")
                self._direction = np.array([1,0])
                self._position = np.array([i,j])

        m = [list(map(lambda x: -1 if x == '#' else 0, row)) for row in m] 
        self._map = np.array(m) 
        self._map[*self._position] = 1

    def _rotate(self):
        rr = np.array([[0,1],[-1,0]])
        self._direction = rr.dot(self._direction)

    def next(self):
        if not self._is_end:
            next_possition = self._position + self._direction
            if self._is_out_of_bounds(*next_possition):
                self._is_end  =True
            else:
                if self._map[*next_possition] == -1:
                    self._rotate()
                else:
                    self._position = next_possition
                    self._map[*self._position] = 1

    def is_end(self):
        return self._is_end

    def no_visited_places(self):
        unique, counts = np.unique(self._map, return_counts=True)

        d = dict(zip(unique, counts))

        return d[1]

                


def main() -> None:

    mapa = None
    position = None
    direction = None

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    m = Map(data)

    while not m.is_end():
        m.next()

        
        
    print("Sum:", m.no_visited_places())

if __name__ == "__main__":
    main()