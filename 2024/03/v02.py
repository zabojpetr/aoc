import os
from pathlib import Path
import typing
import json
import re
import numpy as np

os.chdir(Path(__file__).parent)

def get_valid_inst(data:str) -> typing.List[str]:
    pattern = r"(mul\([0-9]{1,3},[0-9]{1,3}\))|(do\(\))|(don't\(\))"
    occurences = re.findall(pattern, data)

    occurences = [list(filter(lambda x: x!= "", o))[0] for o in occurences]

    return occurences

def compute_instruction(inst:str) -> int:
    nums = inst[inst.find("(")+1:inst.find(")")].split(",")
    nums = list(map(int, nums))

    return np.prod(nums)

def provide_instructions(data:str) -> int:
    occurences = get_valid_inst(data)
    filtered = []
    does = True
    for o in occurences:
        if o == "do()":
            does = True
        elif o == "don't()":
            does = False
        else:
            if does:
                filtered.append(o)

    result = sum(list(map(compute_instruction, filtered)))

    return result

def main() -> None:
    with open("input.txt", "r") as fs:
        data = "".join(fs.readlines())

    d = provide_instructions(data)
        
    print("Sum:", d)

if __name__ == "__main__":
    main()