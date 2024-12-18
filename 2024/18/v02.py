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

Node = namedtuple("Node", ["pr","pc"])
NodeValue = namedtuple("NodeValue", ["value", "pr","pc"])

class Mapa():
    def __init__(self, size):
        self.mapa: np.array = np.full((size,size), ".")
        self.seen: typing.Set[Node] = set()
        self.actual: typing.List[NodeValue] = list()
        self.end_possition: np.array = None

    def load_data(self, data, steps):
        broken = np.array(list(map(lambda x: list(map(int,x.split(","))),data)))
        self.mapa[broken[:steps,0], broken[:steps,1]] = "#"
        heapq.heappush(self.actual, NodeValue(0, 0, 0,))
        self.end_possition = np.array([self.mapa.shape[0]-1, self.mapa.shape[1]-1])


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
            v = nv.value
            n = Node(*nv[1:])

            if all(p == self.end_possition):
                return v

            if n in self.seen:
                continue
            
            if not self.is_valid(p):
                continue

            self.seen.add(n)
            for d in [
                np.array([0,1]),
                np.array([0,-1]),
                np.array([1,0]),
                np.array([-1,0]),
            ]:
                heapq.heappush(self.actual, NodeValue(v+1, *(p+d)))

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    used_steps = set([])
    SIZE = 71
    MIN_STEPS = 1025
    MAX_STEPS = len(data)-1
    while True:
        STEPS = MIN_STEPS + (MAX_STEPS - MIN_STEPS + 1)//2
        print(f"\rMIN_STEPS: {MIN_STEPS}, MAX_STEPS: {MAX_STEPS}                  ", end="")
        m = Mapa(SIZE)
        m.load_data(data, STEPS)
        score = m.find_shortest_path()
        if score == None:
            # nepovedlo se
            MAX_STEPS = STEPS
            used_steps.add((STEPS, 0))
        else:
            MIN_STEPS = STEPS
            used_steps.add((STEPS, 1))
        if MAX_STEPS - MIN_STEPS == 1:
            break
    print(f"\rMIN_STEPS: {MIN_STEPS}, MAX_STEPS: {MAX_STEPS}                  ")
    print("Possition:", data[MAX_STEPS-1])
    

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")