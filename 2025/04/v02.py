import os
from pathlib import Path
import numpy as np

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]):
    parsed_data = []
    for row in data:
        row = row.strip()
        if len(row) == 0:
            continue
        parsed_data.append(list(map(int,list(row.replace(".","0").replace("@","1")))))

    return np.array(parsed_data)

def get_value(data, i, j):
    if i < 0 or j < 0 or i >= len(data) or j >= len(data[0]):
        return 0
    else:
        return data[i][j]
    
def conv(data, i, j):
    s = 0
    for pi in range(-1,2):
        for pj in range(-1,2):
            s += get_value(data, i+pi, j+pj)
    return s

def compute(data: np.array):
    computed_data = []
    for i in range(len(data)):
        computed_data.append([])
        for j in range(len(data[0])):
            if get_value(data,i,j) == 1 and conv(data,i,j) < 5:
                computed_data[i].append(1)
            else:
                computed_data[i].append(0)
    

    return sum(map(sum,computed_data)), data - np.array(computed_data)

def iterate(data:np.array):
    s = 0
    d = data
    while True:
        r,d = compute(d)
        s+=r

        if r == 0:
            break

    return s



def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = iterate(parsed_data)
        
    print("Rolls:", d)

if __name__ == "__main__":
    main()