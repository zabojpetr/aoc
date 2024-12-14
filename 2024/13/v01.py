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

class State():
    A_cost = 3
    B_cost = 1
    
    def __init__(self, A:int, B:int):
        self.A = A
        self.B = B

    def cost(self):
        return self.A * self.A_cost + self.B * self.B_cost

    def __lt__(self, other):
        if not isinstance(other, State):
            return False
        else:
            return self.cost() < other.cost()

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        else:
            return self.A == other.A and self.B == other.B

    def __hash__(self):
        return hash((self.A, self.B))

    def __repr__(self):
        return f"A: {self.A}, B: {self.B}"


class Machine():
    def __init__(self, A: np.array, B: np.array, prize: np.array):
        self.A = A
        self.B = B
        self.prize = prize

    def get_min_cost(self):
        counter = 0
        h: typing.List[State] = [State(0,0)]
        tried = set(h)
        heapq.heapify(h)
        while len(h) > 0:
            s = heapq.heappop(h)
            pos = self.A*s.A + self.B*s.B
            if all(pos == self.prize):
                return s.cost()
            elif not any(pos > self.prize):
                a = State(s.A+1, s.B)
                b = State(s.A, s.B+1)
                if a not in tried:
                    heapq.heappush(h, a)
                    tried.add(a)
                if b not in tried:
                    heapq.heappush(h, b)
                    tried.add(b)
        return 0

def get_machines(data: typing.List[str]):
    machines = []
    A = None
    B = None
    prize = None
    for l in data:
        if len(l) == 0:
            machines.append(Machine(A,B,prize))
            A = None
            B = None
            prize = None
            continue

        vals = np.array(list(map(lambda x: int(x.strip()[2:]),l.split(":")[1].split(","))))
        if l.startswith("Button A"):
            A = vals
        elif l.startswith("Button B"):
            B = vals
        elif l.startswith("Prize"):
            prize = vals

    if A is not None:
        machines.append(Machine(A,B,prize))

    
    return machines


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    machines = get_machines(data)

    costs = 0
    for i, m in enumerate(machines):
        print(f"\rMachine: {i+1}/{len(machines)}", end="")
        costs += m.get_min_cost()


    print("Sum:", costs)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")