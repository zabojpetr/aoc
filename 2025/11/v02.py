import os
from pathlib import Path
import numpy as np
import collections
import math

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]) -> dict[str, list[str]]:
    edges = {}

    for row in data:
        row = row.strip()
        u, vs = row.split(":")
        vs = vs.strip().split(" ")

        edges[u] = vs

    return edges

CACHE = {}

def visits_for_cache(visits: dict[str, int]):
    hashable_visits = tuple(sorted([(k,0 if v == 0 else 1) for k,v in visits.items()]))
    return hashable_visits

def dfs(node: str, edges: dict[str, list[str]], visits: dict[str, int], path: set[str]) -> int:
    total = 0

    hashable_visits = visits_for_cache(visits)
    if (node,hashable_visits) in CACHE:
        return CACHE[(node,hashable_visits)]

    if node == 'out':
        if all(visits.values()):
            return 1
        else:
            return 0
        
    if node in path:
        # cyklus
        return 0
    path.add(node)

    for u in edges.get(node, []):
        if u in visits:
            visits[u] += 1
        total += dfs(u, edges, visits, path)
        if u in visits:
            visits[u] -= 1

    path.remove(node)
    CACHE[(node,hashable_visits)] = total
    return total


def compute(edges: dict[str, list[str]]):
    return dfs("svr", edges, {"fft": 0, "dac": 0}, set())


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("Presses:", d)

if __name__ == "__main__":
    main()