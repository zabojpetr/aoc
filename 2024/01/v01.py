import os
from pathlib import Path
import typing
import json

os.chdir(Path(__file__).parent)

def get_lists(data: typing.List[str]) -> typing.List[typing.List[int]]:
    lists = []
    for r in data:
        nums = r.strip().split(" ")
        nums = filter(lambda x: len(x) > 0, nums)
        for i,n in enumerate(nums):
            if len(lists) < i+1:
                lists.append([])
            lists[i].append(int(n))

    return lists

def compute_distance(lists: typing.List[typing.List[int]]) -> int:
    sorted_lists = [sorted(l) for l in lists]
    distance = 0
    for n1, n2 in zip(*sorted_lists):
        distance += abs(n1-n2)

    return distance

def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    lists = get_lists(data)
    d = compute_distance(lists)
        
    print("Distance:", d)

if __name__ == "__main__":
    main()