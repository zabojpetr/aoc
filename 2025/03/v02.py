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


def compute(data: list[str], batteries: int):
    nums = []
    for row in data:
        bank = 0
        idx = 0
        for b in range(len(row) - batteries + 1, len(row) + 1):
            num = max(row[idx:b])
            idx = row.index(num, idx) + 1
            bank = bank * 10 + num

        nums.append(bank)

    return sum(nums)


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data, 12)

    print("Joltage:", d)


if __name__ == "__main__":
    main()
