import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

def get_valid_mul(data:str) -> typing.List[str]:
    pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    occurences = re.findall(pattern, data)

    return occurences

def compute_instruction(inst:str) -> int:
    nums = inst[inst.find("(")+1:inst.find(")")].split(",")
    nums = list(map(int, nums))

    return np.prod(nums)

def provide_instructions(data:str) -> int:
    occurences = get_valid_mul(data)

    result = sum(list(map(compute_instruction, occurences)))

    return result

def main() -> None:
    with open("input.txt", "r") as fs:
        data = "".join(fs.readlines())

    d = provide_instructions(data)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()