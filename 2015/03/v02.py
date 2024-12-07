import os
from pathlib import Path
from collections import namedtuple
os.chdir(Path(__file__).parent)

Coord = namedtuple("Coord", ["x", "y"])

def get_new_possition(coord: Coord, direction: str):
    new_coord = None
    if direction == "^":
        new_coord = Coord(coord.x, coord.y+1)
    elif direction == ">":
        new_coord = Coord(coord.x+1, coord.y)
    elif direction == "v":
        new_coord = Coord(coord.x, coord.y-1)
    elif direction == "<":
        new_coord = Coord(coord.x-1, coord.y)
    else:
        raise Exception(f"Invalid direction '{direction}'!")
    return new_coord

def main():
    coord_santa = Coord(0,0)
    coord_robot = Coord(0,0)
    possitions = set()
    possitions.add(coord_santa)
    with open("input.txt", "r") as fs:
        directions = fs.read()
        odd = True
        for d in directions:
            if odd:
                coord_santa = get_new_possition(coord_santa, d)
                possitions.add(coord_santa)
            else:
                coord_robot = get_new_possition(coord_robot, d)
                possitions.add(coord_robot)
            odd = odd != True

    print("Wisited houses:",len(possitions))

if __name__ == "__main__":
    main()