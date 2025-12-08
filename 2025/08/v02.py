import os
from pathlib import Path
import math
import heapq
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

os.chdir(Path(__file__).parent)

def distance(p:Point, q: Point):
    return math.sqrt(sum([(i-j)**2 for i,j in zip(p,q)]))

def parse_input(data: list[str]) -> list[Point]:
    points = []

    for row in data:
        row = row.strip()
        coords = row.split(",")
        points.append(Point(*map(int, coords)))

    return points

def compute_all_distances(points: list[Point]) -> dict[tuple[Point,Point], float]:
    points = sorted(points)
    distances = {}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p = points[i]
            q = points[j]
            distances[(p,q)] = distance(p,q)

    return distances

def compute(points: list[Point]):
    distances = compute_all_distances(points)
    distances = sorted([(k,v) for k,v in distances.items()], key = lambda x: x[1])
    point_in_component = {p:i for i,p in enumerate(points)}
    components = {c:[p] for p,c in point_in_component.items()}

    counter = 0
    p = None
    q = None
    while len(components) > 1:
        counter += 1
        ((p,q), dist) = distances[0]
        distances.pop(0)
        cp = point_in_component[p]
        cq = point_in_component[q]
        if cp == cq:
            # stejna komponenta -> skip
            continue

        cp_points = components[cp]
        cq_points = components[cq]

        if len(cp_points) < len(cq_points):
            # precisluj cp
            components[cq] += components[cp]
            for i in cp_points:
                point_in_component[i] = cq
                
            components.pop(cp, None)
        else:
            # precisluj cq
            components[cp] += components[cq]
            for i in cq_points:
                point_in_component[i] = cp

            components.pop(cq, None)



    return p.x * q.x



def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("size:", d)

if __name__ == "__main__":
    main()