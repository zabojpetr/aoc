import os
from pathlib import Path
import typing
import math

os.chdir(Path(__file__).parent)

def parse_input(data: typing.List[str]):
    parsed_data = []
    for row in data:
        row = row.strip()
        if len(row) == 0:
            continue
        parsed_data.append(list(row))
        
    return parsed_data

def flow(first_row: list[str], second_row: list[str]):
    cols = len(first_row)
    splits = 0
    for c in range(cols):
        if first_row[c] in {'S', '|'}:
            if second_row[c] == '^':
                splits += 1
                second_row[c-1] = '|'
                second_row[c+1] = '|'
            else:
                second_row[c] = '|'
                
    return splits
                
        
    
def compute(data: list[list[str]]):
    splits = 0
    for i in range(len(data)-1):
        splits += flow(data[i], data[i+1])
        
    return splits
        
        
    
    

def main() -> None:

    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)

    total_sum = compute(parsed_data)


    print(total_sum)



if __name__ == "__main__":
    main()