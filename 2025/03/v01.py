import json
import os
import typing
from pathlib import Path

os.chdir(Path(__file__).parent)


def parse_input(data: list[str]):
    parsed_data = []
    for row in data:
        row = row.strip()
        if len(row) == 0:
            continue

        parsed_data.append(list(map(int, list(row))))

    return parsed_data


def compute(data: list[str]):
    nums = []
    for row in data:
        first_num = max(row[:-1])
        first_idx = row.index(first_num)
        second_num = max(row[first_idx + 1 :])

        nums.append(first_num * 10 + second_num)

    return sum(nums)


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)

    print("Joltage:", d)


if __name__ == "__main__":
    main()
