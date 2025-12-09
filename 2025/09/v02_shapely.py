import os
from pathlib import Path
from collections import namedtuple
import shapely
from shapely import Point

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]) -> list[Point]:
    points = []

    for row in data:
        row = row.strip()
        coords = row.split(",")
        points.append(Point(*map(int, coords)))

    return points

def area(p: Point, q: Point) -> int:
    return (abs(p.x - q.x) + 1) * (abs(p.y - q.y) + 1)

def compute_all_areas(points: list[Point]) -> dict[tuple[Point,Point], float]:
    distances = {}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p = points[i]
            q = points[j]
            distances[(p,q)] = area(p,q)

    return distances

def compute(points: list[Point]):
    space = shapely.Polygon(points + [points[0]])
    areas = compute_all_areas(points)
    areas = sorted([(k,v) for k,v in areas.items()], key = lambda x: x[1], reverse=True)

    for area in areas:
        (p, q), a = area
        rect = shapely.Polygon([p, Point(p.x, q.y), q, Point(q.x, p.y)])
        if space.contains(rect):
            return area



def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("area:", d)

if __name__ == "__main__":
    main()