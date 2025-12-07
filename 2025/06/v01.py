import os
from pathlib import Path
import typing
import math

os.chdir(Path(__file__).parent)

def parse_input(data: typing.List[str]):
    cols = None
    for row in data:
        row = row.strip()
        parts = list(filter(lambda x: x != '', row.split(" ")))
        if cols is None:
            cols = [[] for _ in parts]
        for i, p in enumerate(parts):
            cols[i].append(p)
            
    return cols
    
def compute(data: list[list[str]]):
    total_sum = 0
    for c in data:
        op = c[-1]
        nums = c[:-1]
        
        if op == "+":
            res = sum(map(int,nums))
            total_sum += res
        elif op == "*":
            res = math.prod(map(int,nums))
            total_sum += res
    return total_sum
    
    

def main() -> None:

    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)

    total_sum = compute(parsed_data)


    print(total_sum)



if __name__ == "__main__":
    main()