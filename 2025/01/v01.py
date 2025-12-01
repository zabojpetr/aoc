import os
from pathlib import Path
import typing
import json

os.chdir(Path(__file__).parent)

def parse_input(data:list[str]):
    parsed_data = []
    for row in data:
        row = row.strip()
        if len(row) == 0:
            continue
        direction = row[0]
        steps = int(row[1:].strip())

        parsed_data.append((direction, steps))
    return parsed_data

def compute(data: list[tuple[str, int]], start: int):
    counter = 0
    value = start
    for d,s in data:
        if d == "R":
            value = (value + s)%100
        elif d == "L":
            value = (value - s)%100
        else:
            print("Neznámý směr:", d)
        
        if value == 0:
            counter += 1

    return counter


def main() -> None:
    with open("test_input.txt", "r") as fs:
        data = fs.readlines()

    START = 50
    parsed_data = parse_input(data)
    d = compute(parsed_data, START)
        
    print("Heslo:", d)

if __name__ == "__main__":
    main()