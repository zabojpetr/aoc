import os
from pathlib import Path
import numpy as np

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]) -> dict[str, list[str]]:
    edges = {}

    for row in data:
        row = row.strip()
        u, vs = row.split(":")
        vs = vs.strip().split(" ")

        edges[u] = vs

    return edges

def dfs(node: str, edges: dict[str, list[str]]) -> int:
    total = 0
    if node == 'out':
        return 1
    for u in edges.get(node, []):
        total += dfs(u, edges)

    return total


def compute(edges: dict[str, list[str]]):
    return dfs("you", edges)


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("Presses:", d)

if __name__ == "__main__":
    main()