import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

def get_number_of_occurences(data:str) -> int:
    pattern = r"XMAS"
    occurences = re.findall(pattern, data)

    return len(occurences)

def reverse_data(data:typing.List[str]) -> typing.List[str]:
    return [x[::-1] for x in data]

def generate_column_data(data:typing.List[str]) -> typing.List[str]:
    return list(map(lambda x: "".join(x), zip(*data)))

def generate_diagonal1_data(data:typing.List[str]) -> typing.List[str]:
    rows = len(data)
    cols = len(data[0])

    transform = []

    start_possitions = []
    start_possitions+=[(x,0) for x in range(rows)]
    start_possitions+=[(0,x) for x in range(1,cols)]

    for (i,j) in start_possitions:
        chars = []
        for s in range(max(rows,cols)):
            if i+s == rows or j+s == cols:
                break
            chars.append(data[i+s][j+s])
        transform.append("".join(chars))

    return transform

def generate_diagonal2_data(data:typing.List[str]) -> typing.List[str]:
    rows = len(data)
    cols = len(data[0])

    transform = []

    start_possitions = []
    start_possitions+=[(x,cols-1) for x in range(1,rows)]
    start_possitions+=[(0,x) for x in range(cols)]

    for (i,j) in start_possitions:
        chars = []
        for s in range(max(rows,cols)):
            if i+s == rows or j-s == -1:
                break
            chars.append(data[i+s][j-s])
        transform.append("".join(chars))

    return transform

def generate_all_directions(data: typing.List[str]) -> typing.List[str]:
    directions = []
    directions += data
    directions+=generate_column_data(data)
    directions+=generate_diagonal1_data(data)
    directions+=generate_diagonal2_data(data)
    directions+=reverse_data(directions)

    return directions

def count_all_occurences(data:typing.List[str]) -> int:
    directions = generate_all_directions(data)

    result = sum(list(map(get_number_of_occurences, directions)))

    return result

def main() -> None:
    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0 ,map(lambda x: x.strip(), fs.readlines())))

    d = count_all_occurences(data)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()