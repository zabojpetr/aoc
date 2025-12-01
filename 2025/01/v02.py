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
            value = (value + s)
        elif d == "L":
            value = (value - s)
        else:
            print("Neznámý směr:", d)
        
        # prevod value na kladne cislo, protoze celociselne deleni v zaporu se chova "divne"
        counter += abs(value) // 100
        # pricist jednicku za pruchod prez 0, ale pokud jsem startoval na 0, tak nepricitej
        counter += 1 if value <= 0 and value != -1*s else 0 # +1 za 0

        value = value%100

    return counter


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    START = 50
    parsed_data = parse_input(data)
    d = compute(parsed_data, START)
        
    print("Heslo:", d)

if __name__ == "__main__":
    main()

    # <7106
    # <8474