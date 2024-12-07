import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

def try_operation(result: int, numbers: typing.List[int]) -> bool:
    if len(numbers) == 1:
        return result == numbers[0]
    else:
        if numbers[0] + numbers[1] <= result:
            r1 = try_operation(result, [numbers[0] + numbers[1]] + numbers[2:])
        else: 
            r1 = False
        if r1:
            return r1
        else:
            if numbers[0] * numbers[1] <= result:
                r2 = try_operation(result, [numbers[0] * numbers[1]] + numbers[2:])
            else: 
                r2 = False
            return r2

def find_right_equation(data: typing.List[str]) -> int:
    counter = 0
    for row in data:
        raw_result, raw_numbers = row.split(":")
        result = int(raw_result)
        numbers = list(map(int, filter(lambda x: len(x) > 0, raw_numbers.split(" "))))

        if try_operation(result, numbers):
            counter += result

    return counter

def main() -> None:
    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    d = find_right_equation(data)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()