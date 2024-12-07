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
        self._history = set()
        self._is_cycle = False
        self._start_possition = ()

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

        self._start_possition = tuple(self._position)
        m = [list(map(lambda x: -1 if x == '#' else 0, row)) for row in m] 
        self._map = np.array(m) 
        self._map[*self._position] = 1

    def _rotate(self):
        rr = np.array([[0,1],[-1,0]])
        self._direction = rr.dot(self._direction)

    def _add_history(self):
        self._history.add((*self._position, *self._direction))

    def next(self):
        if (*self._position, *self._direction) in self._history:
            self._is_cycle = True
            self._is_end = True

        if not self._is_end:
            next_possition = self._position + self._direction
            if self._is_out_of_bounds(*next_possition):
                self._is_end = True
            else:
                if self._map[*next_possition] == -1:
                    self._add_history()
                    self._rotate()
                else:
                    self._add_history()
                    self._position = next_possition
                    self._map[*self._position] = 1

    def is_end(self):
        return self._is_end

    def is_cycle(self):
        return self._is_cycle

    def get_map(self):
        return self._map

    def set_obstecle(self, x, y):
        if self._start_possition != (x,y):
            self._map[x,y] = -1

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

    cycles = 0
    for i, r in enumerate(m.get_map()):
        for j, c in enumerate(r):
            if c == 1:
                
                m2 = Map(data)
                m2.set_obstecle(i,j)

                while not m2.is_end():
                    m2.next()

                ic = m2.is_cycle()
                cycles += ic
        
        
    print("Sum:", cycles)

if __name__ == "__main__":
    main()