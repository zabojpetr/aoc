import os
from pathlib import Path

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]):
    intervals = []
    ingredients = []

    first_part = True
    for row in data:
        row = row.strip()
        if len(row) == 0:
            first_part = False
            continue
        if first_part:
            parts = row.split("-")
            intervals.append((tuple(map(int, parts))))
        else:
            ingredients.append(int(row))

    return intervals#, ingredients

def count_new_ids(interval:tuple[int,int], used_intervals: list[tuple[int,int]]):
    for i,(s,e) in enumerate(used_intervals):
        if s <= interval[0] and interval[1] <= e:
            # kompletne v pouzitem intervalu
            return 0
        elif interval[1] < s or interval[0] > e:
            # neprotina se
            continue
        elif interval[0] < s and e < interval[1]:
            # uvnitř je použitý interval
            num1 = count_new_ids((interval[0],s-1), used_intervals[i+1:])
            num2 = count_new_ids((e+1,interval[1]), used_intervals[i+1:])
            return num1 + num2
        elif interval[0] < s:
            # interval konci v pouzitem intervalu
            interval = (interval[0], s-1)
        elif e < interval[1]:
            # interval zacina v pouzitem intervalu
            interval = (e+1,interval[1])
    return interval[1] - interval[0] + 1
        

def compute(interval:list[tuple[int,int]]):
    num_ids = 0
    for i in range(len(interval)):
        num_ids += count_new_ids(interval[i], interval[:i])

    return num_ids





def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("fresh:", d)

if __name__ == "__main__":
    main()