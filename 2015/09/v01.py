import os
from pathlib import Path
import typing
from collections import namedtuple

os.chdir(Path(__file__).parent)

Edge = namedtuple("Edge", ["to", "len"])

def parse_edge(raw: str) -> typing.Union[str, str, int]:
    cities, length = map(lambda x: x.strip(), raw.split("="))
    city_a, city_b = map(lambda x: x.strip(), cities.split(" to "))

    return city_a, city_b, int(length)

def shortest_cycle(place: str, edges: typing.Dict[str, typing.List[Edge]], used:set) -> int:
    minimum = 0
    first = True
    for dir in edges[place]:
        if dir.to in used:
            continue

        used.add(dir.to)
        sub_minimum = dir.len + shortest_cycle(dir.to, edges, used)
        if first:
            minimum = sub_minimum
        else:
            minimum = min(minimum, dir.len + shortest_cycle(dir.to, edges, used))
        used.remove(dir.to)

        first = False

    return minimum

def add_edge(edges: typing.Dict[str, typing.List[str]], city_from:str, city_to:str, length:int):
    if city_from not in edges:
        edges[city_from] = []
    
    edges[city_from].append(Edge(city_to, length))

    return edges

def main():
    edges = {}
    with open("input.txt", "r") as fs:
        for l in fs:
            city_a, city_b, length = parse_edge(l)
            edges = add_edge(edges, city_a, city_b, length)
            edges = add_edge(edges, city_b, city_a, length)

        minimum = 0
        first = True
        for c in edges:
            sub_min = shortest_cycle(c,edges,{c})
            if first:
                minimum = sub_min
            else:
                minimum = min(minimum, sub_min)

            first = False
        
    print("Minimum:", minimum)

if __name__ == "__main__":
    main()