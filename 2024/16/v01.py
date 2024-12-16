import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np
from collections import namedtuple
import heapq

os.chdir(Path(__file__).parent)

Node = namedtuple("Node", ["pr","pc","dr","dc"])
NodeValue = namedtuple("NodeValue", ["value", "pr","pc","dr","dc"])

class Mapa():
    def __init__(self):
        self.mapa: np.array = None
        self.seen: typing.Set[Node] = set()
        self.actual: typing.List[NodeValue] = list()
        self.end_possition:np.array = None

    def load_data(self, data):
        self.mapa = np.array(list(map(list,data)))
        start = np.where(self.mapa == "S")
        end = np.where(self.mapa == "E")
        heapq.heappush(self.actual, NodeValue(0,start[0][0], start[1][0], 0, 1))
        self.end_possition = np.array([end[0][0], end[1][0]])



    def _rotate(self, direction:np.array, left: bool):
        mult = -1 if left else 1
        direction = np.dot(mult*np.array([[0,1],[-1,0]]), direction)
        return direction

    def rotate_left(self, direction:np.array):
        return self._rotate(direction, True)

    def rotate_right(self, direction:np.array):
        return self._rotate(direction, False)

    def step(self, possition:np.array, direction: np.array):
        return possition + direction

    def is_valid(self, possition:np.array):
        if not (all(np.array([0,0]) <= possition) and all(possition < np.array(self.mapa.shape))):
            return False
        elif self.mapa[*possition] == "#":
            return False
        else:
            return True

    def find_shortest_path(self) -> int:
        while len(self.actual) > 0:
            nv = heapq.heappop(self.actual)
            p = np.array([nv.pr, nv.pc])
            d = np.array([nv.dr, nv.dc])
            v = nv.value
            n = Node(*nv[1:])

            if all(p == self.end_possition):
                return v

            if n in self.seen:
                continue
            
            if not self.is_valid(p):
                continue

            self.seen.add(n)
            heapq.heappush(self.actual, NodeValue(v+1000, *p, *self.rotate_left(d)))
            heapq.heappush(self.actual, NodeValue(v+1000, *p, *self.rotate_right(d)))
            heapq.heappush(self.actual, NodeValue(v+1, *self.step(p, d), *d))

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    m = Mapa()
    m.load_data(data)
    score = m.find_shortest_path()
    
    print("Sum:", score)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")