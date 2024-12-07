import os
from pathlib import Path
import typing
import json

os.chdir(Path(__file__).parent)

def get_series(data: typing.List[str]) -> typing.List[typing.List[int]]:
    lists = []
    for r in data:
        nums = r.strip().split(" ")
        nums = filter(lambda x: len(x) > 0, nums)
        lists.append(list(map(int,nums)))

    return lists

def is_safe(data: typing.List[int]) -> bool:
    is_decreasing = True
    is_safe = True
    for i,(m,n) in enumerate(zip(data, data[1:])):
        if i == 0:
            if m < n:
                is_decreasing = False
            elif m > n:
                is_decreasing = True
            else:
                is_safe = False
                break
        if is_decreasing:
            if m - n >= 1 and m-n <= 3:
                continue
            else:
                is_safe = False
                break
        else:
            if n - m >= 1 and n-m <= 3:
                continue
            else:
                is_safe = False
                break

    return is_safe


def count_safe(lists: typing.List[typing.List[int]]) -> int:
    safe_lists = list( map(is_safe, lists))
    safe_list_count = len(list(filter(lambda x: x == True, safe_lists)))

    return safe_list_count

def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    lists = get_series(data)
    d = count_safe(lists)
        
    print("Safe series:", d)

if __name__ == "__main__":
    main()