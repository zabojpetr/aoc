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
        parsed_row = [0 if c == '.' else (1 if c == 'S' else -1) for c in list(row)]
        parsed_data.append(parsed_row)
        
        
    return parsed_data

def flow(first_row: list[str], second_row: list[str]):
    cols = len(first_row)
    for c in range(cols):
        if first_row[c] > 0:
            if second_row[c] == -1:
                second_row[c-1] += first_row[c]
                second_row[c+1] += first_row[c]
            else:
                second_row[c] += first_row[c]
                
                
        
    
def compute(data: list[list[str]]):
    for i in range(len(data)-1):
        flow(data[i], data[i+1])
        
    return sum(data[-1])
        
        
    
    

def main() -> None:

    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)

    total_sum = compute(parsed_data)


    print(total_sum)



if __name__ == "__main__":
    main()