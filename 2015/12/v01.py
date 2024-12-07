import os
from pathlib import Path
import typing
import json

os.chdir(Path(__file__).parent)

def get_numbers(data):
    nums = []
    if isinstance(data, list):
        for i in data:
            nums.extend(get_numbers(i))
    elif isinstance(data, dict):
        for k,v in data.items():
            nums.extend(get_numbers(k))
            nums.extend(get_numbers(v))
    elif isinstance(data, int):
        nums.append(data)
    return nums

def main():
    edges = {}
    with open("input.txt", "r") as fs:
        data = json.load(fs)

    num = get_numbers(data)
    s = sum(num)
        
    print("Sum:", s)

if __name__ == "__main__":
    main()