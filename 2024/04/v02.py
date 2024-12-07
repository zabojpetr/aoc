import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)



def count_all_occurences(data:typing.List[str]) -> int:
    rows = len(data)
    cols = len(data[0])
    counter = 0

    for i in range(rows - 2):
        for j in range(cols - 2):
            if data[i+1][j+1] == "A":
                d1 = data[i][j] + data[i+2][j+2]
                d2 = data[i+2][j] + data[i][j+2]
                if d1 in ("MS", "SM") and d2 in ("MS", "SM"):
                    counter += 1

    return counter

def main() -> None:
    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0 ,map(lambda x: x.strip(), fs.readlines())))

    d = count_all_occurences(data)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()