import os
from pathlib import Path
import typing
import json
import re
import timeit
import itertools

os.chdir(Path(__file__).parent)

def find_end_points(start_point: typing.Tuple[int, int], mapa: typing.List[typing.List[int]]) -> typing.List[typing.Tuple[int,int]]:
    directions = [
        (1,0),
        (0,1),
        (-1,0),
        (0,-1)
    ]

    end_positions = []

    if mapa[start_point[0]][start_point[1]] == 9:
        end_positions.append(start_point)
    else:
        for d in directions:
            new_possition = (start_point[0] + d[0], start_point[1] + d[1])
            if (new_possition[0] < 0 or new_possition[0] >= len(mapa)
                or new_possition[1] < 0 or new_possition[1] >= len(mapa[0])):
                continue
            
            if mapa[start_point[0]][start_point[1]] + 1 == mapa[new_possition[0]][new_possition[1]]:
                end_positions.extend(find_end_points(new_possition, mapa))

    return end_positions


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))

    mapa = [list(map(int,row)) for row in data]
    start_positions = [(i,j) for i, row in enumerate(mapa) for j, h in enumerate(row) if h == 0]

    end_positions = []
    for sp in start_positions:
        end_positions.append(find_end_points(sp, mapa))

    score = [len(x) for x in end_positions]

    print("Sum:", sum(score))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")