import os
from pathlib import Path
import typing
import json
from collections import Counter

os.chdir(Path(__file__).parent)

def parse_input(row: str):
    parts = row.split(",")
    intervals = list(map(lambda x: x.split("-"), parts))

    return intervals


def find_repetitive_nums(intervals: list[list[int]]):
    nums = []
    for start_num, end_num in intervals: 
        int_nums = set()
        for num in range(int(start_num), int(end_num)+1):
            num_str = str(num)
            num_len = len(num_str)
            for pat_len in range(1,num_len//2+1):
                if num_len % pat_len == 0 and num_str == num_str[:pat_len]*(num_len//pat_len):
                    int_nums.add(num)
        nums += list(int_nums)

    return sum(nums)

    



def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.read().strip()

    parsed_data = parse_input(data)
    d = find_repetitive_nums(parsed_data)
        
    print("Heslo:", d)

if __name__ == "__main__":
    main()