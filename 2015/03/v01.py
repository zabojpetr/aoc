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
    coord = Coord(0,0)
    possitions = set()
    possitions.add(coord)
    with open("input.txt", "r") as fs:
        directions = fs.read()
        for d in directions:
            coord = get_new_possition(coord, d)
            possitions.add(coord)
    print("Wisited houses:",len(possitions))

if __name__ == "__main__":
    main()