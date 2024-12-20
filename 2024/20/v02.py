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
FromTo = namedtuple("FromTo", ["from_start", "to_end"])

class Mapa():
    def __init__(self):
        self.mapa: np.array = None
        self.seen: typing.Set[Node] = set()
        self.actual: typing.List[NodeValue] = list()
        self.start_possition: np.array = None
        self.end_possition: np.array = None
        self.from_to = {}
        self.cheats: typing.Dict[typing.Tuple[int,int,int,int],int] = {}

    def load_data(self, data):
        self.mapa = np.array(list(map(list,data)))
        start = np.where(self.mapa == "S")
        end = np.where(self.mapa == "E")
        self.start_possition = np.array([start[0][0], start[1][0]])
        self.end_possition = np.array([end[0][0], end[1][0]])


    def is_valid(self, possition:np.array):
        if not (all(np.array([0,0]) <= possition) and all(possition < np.array(self.mapa.shape))):
            return False
        elif self.mapa[tuple(possition)] == "#":
            return False
        else:
            return True

    def is_cheat(self, possition:np.array):
        if not (all(np.array([0,0]) <= possition) and all(possition < np.array(self.mapa.shape))):
            return False
        elif self.mapa[tuple(possition)] == "#":
            return True
        else:
            return False

    def find_path(self) -> int:
        self.seen: typing.Set[Node] = set()
        self.actual: typing.List[NodeValue] = list()
        heapq.heappush(self.actual, NodeValue(1,self.start_possition[0], self.start_possition[1]))
        while len(self.actual) > 0:
            nv = heapq.heappop(self.actual)
            p = np.array([nv.pr, nv.pc])
            v = nv.value
            n = Node(*nv[1:])

            if all(p == self.end_possition):
                self.from_to[tuple(p)] = FromTo(v,-1)
                break

            if n in self.seen:
                continue
            
            if not self.is_valid(p):
                continue

            self.seen.add(n)
            self.from_to[tuple(p)] = FromTo(v,-1)
            for d in [
                np.array([0,1]),
                np.array([0,-1]),
                np.array([1,0]),
                np.array([-1,0]),
            ]:
                heapq.heappush(self.actual, NodeValue(v+1, *(p+d)))

        updated_from_to = {}
        for k, (f, t) in self.from_to.items():
            updated_from_to[k] = FromTo(f, v-f)
        self.from_to = updated_from_to

    def find_cheat_paths(self, possition: np.array):
        ds = [
                np.array([0,1]),
                np.array([0,-1]),
                np.array([1,0]),
                np.array([-1,0]),
            ]
        for d in ds:
            sp = possition + d
            seen: typing.Set[Node] = set()
            actual: typing.List[NodeValue] = list()
            heapq.heappush(actual, NodeValue(1,(possition+d)[0], (possition+d)[1]))
            while len(actual) > 0:
                nv = heapq.heappop(actual)
                p = np.array([nv.pr, nv.pc])
                v = nv.value
                n = Node(*(nv[1:]))

                if v > 20:
                    continue

                if not self.is_cheat(p) and not self.is_valid(p):
                    continue

                if n in seen:
                    continue

                if self.is_valid(p):
                    if tuple(p) == (7,3) and tuple(possition) == (3,1):
                        pass
                    path_length =  (
                            (self.from_to[tuple(possition)].from_start + self.from_to[tuple(possition)].to_end - 1) 
                            - (self.from_to[tuple(possition)].from_start + self.from_to[tuple(p)].to_end - 1 + v)
                            )
                    if (tuple(possition), tuple(p)) not in self.cheats or self.cheats[tuple(possition), tuple(p)] < path_length:
                        self.cheats[tuple(possition), tuple(p)] = path_length
                    

                seen.add(n)
                for d in [
                    np.array([0,1]),
                    np.array([0,-1]),
                    np.array([1,0]),
                    np.array([-1,0]),
                ]:
                    heapq.heappush(actual, NodeValue(v+1, *(p+d)))


    def find_cheats(self):
        self.cheats: typing.Dict[typing.Tuple[int,int,int,int],int] = {}
        self.seen: typing.Set[Node] = set()
        self.actual: typing.List[NodeValue] = list()
        heapq.heappush(self.actual, NodeValue(0,self.start_possition[0], self.start_possition[1]))
        while len(self.actual) > 0:
            nv = heapq.heappop(self.actual)
            p = np.array([nv.pr, nv.pc])
            v = nv.value
            n = Node(*(nv[1:]))

            if all(p == self.end_possition):
                break

            if n in self.seen:
                continue
            
            if not self.is_valid(p):
                continue
            
            print(f"\rStep: {v}/{sum(self.from_to[tuple(n)])-1}", end = "")

            ds = [
                np.array([0,1]),
                np.array([0,-1]),
                np.array([1,0]),
                np.array([-1,0]),
            ]
            self.find_cheat_paths(p)

            self.seen.add(n)
            for d in ds:
                heapq.heappush(self.actual, NodeValue(v+1, *(p+d)))


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    m = Mapa()
    m.load_data(data)
    m.find_path()
    m.find_cheats()

    score = len(list(filter(lambda x: x >= 100, m.cheats.values())))
    
    print("Sum:", score)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")