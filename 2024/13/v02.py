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
        # from equals:
        # a*A[0] + b*B[0] = P[0]
        # a*A[1] + b*B[1] = P[1]
        # where a and b are number of pushes to a and b
        
        b = (self.A[1]*self.prize[0] - self.A[0]*self.prize[1])/(self.A[1]*self.B[0] - self.A[0]*self.B[1])
        a = (self.prize[1] - b * self.B[1])/self.A[1]

        if int(a) == a and int(b) == b:
            return a*State.A_cost + b*State.B_cost
        else:
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
            prize = vals + 10000000000000

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