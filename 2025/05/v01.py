import os
from pathlib import Path

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]):
    intervals = []
    ingredients = []

    first_part = True
    for row in data:
        row = row.strip()
        if len(row) == 0:
            first_part = False
            continue
        if first_part:
            parts = row.split("-")
            intervals.append((tuple(map(int, parts))))
        else:
            ingredients.append(int(row))

    return intervals, ingredients

          
def is_fresh(ingredient:int, interval:list[tuple[int,int]]):
    for s,e in interval:
        if s <= ingredient and ingredient <= e:
            return True
    return False


def compute(interval:list[tuple[int,int]], ingredients: list[int]):
    s = 0
    for i in ingredients:
        if is_fresh(i, interval):
            s+=1

    return s





def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(*parsed_data)
        
    print("fresh:", d)

if __name__ == "__main__":
    main()