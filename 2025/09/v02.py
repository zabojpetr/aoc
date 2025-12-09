import os
from pathlib import Path
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

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
    points = sorted(points)
    distances = {}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p = points[i]
            q = points[j]
            distances[(p,q)] = area(p,q)

    return distances

def _intersect(rect: tuple[int, int], line: tuple[int, int]):
    # když se line zaboží do rect, tak kousek rect vykousnu, pokud zůstane na hraně je to ok
    r1 = min(rect)
    r2 = max(rect)
    l1 = min(line)
    l2 = max(line)

    if r2 <= l1 or r1 >= l2:
        return False
    else:
        return True



def intersect(rect: tuple[Point, Point], line: tuple[Point, Point]):
    if (_intersect((rect[0].x, rect[1].x), (line[0].x, line[1].x)) 
        and _intersect((rect[0].y, rect[1].y), (line[0].y, line[1].y))):
        return True
    else:
        return False
    
def is_rectangle_in_area(rect: tuple[Point, Point], area: list[Point]):
    for i in range(len(area)):
        if intersect(rect, (area[i], area[(i+1)%len(area)])):
            return False
    return True

def compute(points: list[Point]):
    areas = compute_all_areas(points)
    areas = sorted([(k,v) for k,v in areas.items()], key = lambda x: x[1], reverse=True)

    for area in areas:
        rect, a = area
        if is_rectangle_in_area(rect, points):
            return area


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("area:", d)

if __name__ == "__main__":
    main()